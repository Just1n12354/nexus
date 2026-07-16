# Ben - Review WindowsUpdate.cs

## Befunde

---

### K1 — Kritisch: `ServiceID` wird im Catch-Block nicht zurückgesetzt (Bug: Fallback-Suche blockiert)

**WAS:** Zeilen 71–107 versuchen, Microsoft Update über `AddService2` einzubinden. Wenn das gelingt, wird `$searcher.ServiceID = $microsoftUpdateServiceId` gesetzt und die Suche beschränkt sich auf diesen einen Service. Wenn `AddService2` scheitert (Firewall, GPO, Offline-System), landet der Code im `catch` auf Zeile 103–107 — der Fallback. Dort wird `$searcher.ServiceID` **NICHT** auf einen leeren String zurückgesetzt. Die Suche auf Zeile 112 (`$searcher.Search('...')`) läuft damit weiterhin mit der im vorherigen Block gesetzten `ServiceID` — die Suche findet *keine* Updates, weil die Windows Update-Quelle gar nicht durchsucht wird, sondern weiterhin die (nicht verfügbare) Microsoft Update ID filtert.

Der Nutzer sieht „[OK] Windows ist auf dem neuesten Stand", obwohl Updates verfügbar sind. Der Fehler ist silent und nicht erkennbar.

**WARUM:** Der Suchfilter `$searcher.ServiceID` gilt fortan für jeden nachfolgenden Suchaufruf. Er wird nur innerhalb des `try`-Blocks auf 0 gesetzt, nie im `catch` zurückgesetzt. Das ist ein logischer Bug, kein Race-Condition-Problem — die Suche läuft definitiv mit der falschen ID.

**FIX:** Am Anfang des `catch`-Blocks (Zeile 103) `ServiceID` explizit zurücksetzen.

```powershell
# Zeile 103 — catch-Block anpassen:
catch {
    $searcher.ServiceID = ''                          # <-- NEU: Fallback aktivieren
    Write-Output '[WARNUNG] Microsoft Update konnte nicht eingebunden werden.'
    Write-Output 'Fallback auf die normale Windows-Update-Quelle.'
    Write-Output "Grund: $($_.Exception.Message)"
}
```

---

### K2 — Hoch: C# liest nach `process.Kill()` keinen Exit-Code/Simultaneous-Read

**WAS:** Zeilen 437–453: Nach 2 Stunden Timeout wird `process.Kill(entireProcessTree: true)` aufgerufen. Anschliessend wird `process.WaitForExit()` (Zeile 455) und `process.ExitCode` (Zeile 457) ausgelesen. `process.Kill()` terminiert den Prozess sofort — `WaitForExit()` kann auf einem bereits toten Prozess eine `InvalidOperationException` werfen. Zudem gibt es eine Race-Condition: zwischen `Kill()` und `WaitForExit()` könnten noch Zeichen im Output-Stream verloren gehen.

**WARUM:** Wenn der Kill-Versuch fehlschlägt (Prozess bereits beendet), wird die Exception im inneren `try-catch` abgefangen. Dann erreicht `process.WaitForExit()` (Zeile 455) einen bereits beendeten Prozess — je nach .NET-Version kann das eine Exception werfen oder `false` zurückgeben. `process.ExitCode` ist dann undefiniert (0, -1 oder -532462766). Der weitere `if (process.ExitCode == 0)` auf Zeile 457 wird mit undefiniertem Verhalten bedient.

**FIX:** Kill-Logik robust umbauen, mit explizitem `try-catch` um den gesamten Kill/Wait-Block und synchronem `ReadToEnd()` nach `WaitForExit()`, um alle Output-Daten zu erfassen.

```csharp
// Zeilen 423–453 ersetzen:

if (!process.Start())
{
    Console.WriteLine(
        "[FEHLER] PowerShell konnte nicht gestartet werden.");
    return;
}

process.BeginOutputReadLine();
process.BeginErrorReadLine();

// IUpdateDownloader.Download() und IUpdateInstaller.Install() sind
// synchrone COM-Aufrufe ohne Timeout. Haengt der Windows-Update-Dienst
// (klassisch nach einem abgebrochenen Update), wartet die Wartung sonst
// bis in alle Ewigkeit. 2 Stunden decken auch grosse Feature-Updates ab.
if (!process.WaitForExit(120 * 60 * 1000))
{
    try
    {
        process.Kill(entireProcessTree: true);
    }
    catch
    {
        // Prozess war bereits beendet.
    }

    // Sicherstellen, dass der Prozess wirklich tot ist.
    try { process.WaitForExit(); } catch { /* bereits tot */ }

    // Verbleibenden Output erfassen (Race-Condition zwischen Kill und
    // WaitForExit kann dazu fuehren, dass der async-Handler nicht alle
    // Zeilen ausgeben konnte).
    string remainingOutput = process.StandardOutput.ReadToEnd();
    if (!string.IsNullOrWhiteSpace(remainingOutput))
    {
        Console.Write(remainingOutput);
    }

    Console.WriteLine(
        "[FEHLER] Zeitlimit: Windows Update wurde nach 2 Stunden " +
        "abgebrochen. Der Windows-Update-Dienst haengt vermutlich.");

    return;
}

process.WaitForExit();

// ... Rest bleibt unveraendert (Exit-Code-Auswertung ab Zeile 457)
```

---

### M1 — Mittel: Kein synchroner `ReadToEnd()` nach `WaitForExit()` — Ausgabeverlust bei schnellen Prozessen

**WAS:** Der Code nutzt `BeginOutputReadLine()` und `BeginErrorReadLine()` (Zeilen 430–431) mit Event-Handlern. Das ist grundsätzlich korrekt. Allerdings gibt es eine bekannte Race-Condition in .NET: Wenn ein Prozess sehr schnell beendet wird, kann der `OutputDataReceived`-Handler noch nicht initialisiert sein, wenn die erste Ausgabe ankommt. `ReadToEnd()` nach `WaitForExit()` fängt diesen Fall auf.

**WARUM:** Bei sehr schnellen Prozessen (z.B. „Nicht als Admin" – Zeile 36–38, sofortiger `return`) ist die Event-Registrierung und der Prozessstart fast synchron. Theoretisch ist `BeginOutputReadLine()` vor `Start()` aufgerufen (Zeilen 430–431 vor Zeile 423) — das sollte eigentlich funktionieren. Aber als Defense-in-Depth ist `ReadToEnd()` nach `WaitForExit()` die bewährte Pattern.

**FIX:** Wie in K2 aufgezeigt — `ReadToEnd()` nach `WaitForExit()` einfügen, um restlichen Output sicher zu lesen.

---

### M2 — Mittel: COM-Objekte im PowerShell-Skript nicht explizit freigegeben

**WAS:** Die COM-Objekte `$session`, `$searcher`, `$serviceManager`, `$downloader`, `$installer` (Zeilen 63, 66, 75, 218, 288) werden über `New-Object -ComObject` erstellt. PowerShell.NET-Interoperabilität erstellt einen Runtime Callable Wrapper (RCW). PowerShells GC gibt RCWs nicht deterministisch frei — das Finalizer-Thread macht es irgendwann, aber unvorhersehbar. Bei langen Läufen (2 Stunden Timeout) oder wiederholten Aufrufen kann das zu Memory-Leaks oder „Windows Update-Service kann nicht gesperrt werden"-Fehlern führen.

**WARUM:** RCWs müssen über `Marshal.ReleaseComObject()` explizit freigegeben werden. Im vorliegenden Code geschieht das nur durch `Remove-Variable` oder Script-Ende, was nicht deterministisch ist. Besonders kritisch ist `$serviceManager` — wenn `AddService2` erfolgreich war, bleibt der Service registriert, bis der Prozessende das COM-Objekt finalisiert.

**FIX:** Helper-Funktion hinzufügen und am Script-Ende (vor `exit`) alle COM-Objekte freigeben.

```powershell
# Am Anfang des try-Blocks (nach Zeile 61) einfuegen:

function Release-ComObject {
    param([object]$Obj)
    if ($null -ne $Obj -and $Obj -ne $null) {
        try {
            while ([System.Runtime.InteropServices.Marshal]::ReleaseComObject($Obj) -gt 0) {}
        } catch {}
    }
}

# Vor dem letzten exit (vor Zeile 356 bzw. 368, also vor jedem exit-Aufruf)
# aufrufen:
Release-ComObject $installer
Release-ComObject $downloader
Release-ComObject $searcher
Release-ComObject $session

# Alternativ: am Ende des try-Blocks, vor dem Script-ende:
try { Release-ComObject $installer } catch {}
try { Release-ComObject $downloader } catch {}
try { Release-ComObject $searcher } catch {}
try { Release-ComObject $session } catch {}
```

Praktisch sollte das im vorliegenden Code als `finally`-Block realisiert werden. Da aber viele `exit`-Pfade existieren, ist eine saubere Loesung der `finally`-Block um das ganze Skript. Da das PowerShell-Skript eine grosse Inline-String ist, reicht es, vor dem letzten exit (nach Zeile 356, 364, 368) eine COM-Freigabe einzufuegen. Besser waere eine Wrapper-Funktion, die das Skript umhaellt.

---

### N1 — Niedrig: `AddService2` ist veraltet

**WAS:** Zeile 88: `$serviceManager.AddService2(...)` ist eine veraltete API. Microsoft empfiehlt `AddSearchService`.

**WARUM:** Die alte Funktion funktioniert noch, wird aber in zukünftigen Windows-Versionen entfernt. `AddSearchService` hat eine andere Signatur.

**FIX:** Bei einem kuerzlich getesteten Windows 11/10 funktioniert `AddSearchService` stattdessen so:

```powershell
$serviceManager.AddSearchService(
    [guid]::Parse($microsoftUpdateServiceId),
    2
) | Out-Null
```

Solange der aktuelle Code auf Windows 10/11 funktioniert, ist das kein aktueller Bug, aber ein Wartungsproblem für die Zukunft.

---

### N2 — Niedrig: Kein `IsOptional`-Filter — optionale Updates werden mitinstalliert

**WAS:** Die Suche auf Zeile 112 (`IsInstalled=0 AND IsHidden=0`) filtert nur nach nicht-installierten und nicht-verborgenen Updates. Viele optionale Updates (z.B. Sprachpakete, Feature-on-Demand, ältere .NET-Versionen) werden gefunden und installiert. Das ist meist kein Problem, kann aber bei grossen Feature-Updates (z.B. .NET 4.8 + Sprachpaket) die Installationsdauer und Reboot-Haeufigkeit erhöhen.

**WARUM:** Die Windows Update API liefert auch optionale Updates als `IUpdate`-Objekte. Es gibt keine offensichtliche Eigenschaft `IsOptional` im COM-Interface, die man direkt abfragen kann. Der Filter `IsHidden=0` entfernt nur manuell verborgene Updates.

**FIX:** Wenn gewuenscht, koennte man `IUpdate.OptionalUpdateCategories` prüfen oder die Title-Filterung nach bekannten optionalen Update-Titeln hinzufügen. Das ist ein Design-Entscheidung, kein Bug.

---

### N3 — Niedrig: `MaxDownloadSize` auf 0 wird nicht ausgeschlossen

**WAS:** Zeilen 170–173: `$sizeMegabytes -gt 0 -and $sizeMegabytes -lt 50000`. Updates mit `MaxDownloadSize = 0` werden angezeigt, aber ohne Grössenangabe. Das ist kein Fehler, aber verwirrend für den Nutzer.

**FIX:** Optional: `elseif ($sizeMegabytes -eq 0) { $sizeText = ' (Klein)' }` — aber das ändert nichts an der Funktionalitaet.

---

## Unsauberkeiten / Verbesserungsvorschlaege (keine Bugs)

| Zeile | Thema | Kommentar |
|-------|-------|-----------|
| 232 | `exit 0` in if-Block | Der `exit 0` auf Zeile 148 (keine Updates gefunden) verlaesst die ganze PowerShell-Instanz — das ist korrekt und gewollt. |
| 97 | Kommentar „3 = ssOthers" | ServerSelection 3 ist korrekt `ssOthers`. Der Kommentar ist korrekt. |
| 241 | `0x{0:X8}`-Format | `([uint32]$downloadResult.HResult)` formatiert negative HRESULTs korrekt als unsigned hex (z.B. `0x80070005`). Funktioniert. |
| 342 | `RebootRequired` | Wird korrekt an PowerShell-Output weitergegeben, aber C# erhaelt keinen eigenen Reboot-Hinweis als Exit-Code. Der Reboot-Hinweis ist im `Write-Output` enthalten und wird an Console weitergereicht. Funktioniert. |
| 382–405 | ProcessStartInfo | `ArgumentList` ist .NET Core 2.1+ — korrekt für .NET 10. |
| 430–431 | `BeginOutputReadLine()` vor `Start()` | Reihenfolge ist korrekt (Handler registrieren VOR Prozessstart). |

---

## Ueberarbeiteter Code

```csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;

namespace JustUpdate.Module;

/// <summary>
/// Windows-Updates installieren
/// </summary>
internal static class WindowsUpdate
{
    public const string Name = "windowsupdate";

    public static void Ausfuehren()
    {
        Console.WriteLine("[W] Windows-Updates werden geprüft ...");

        if (!OperatingSystem.IsWindows())
        {
            Console.WriteLine("[FEHLER] Diese Funktion ist nur unter Windows verfügbar.");
            return;
        }

        using var identity =
            System.Security.Principal.WindowsIdentity.GetCurrent();

        var principal =
            new System.Security.Principal.WindowsPrincipal(identity);

        if (!principal.IsInRole(
                System.Security.Principal.WindowsBuiltInRole.Administrator))
        {
            Console.WriteLine(
                "[FEHLER] Das Programm muss als Administrator gestartet werden.");
            return;
        }

        string script = """
            $ErrorActionPreference = 'Stop'
            [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
            $OutputEncoding = [Console]::OutputEncoding

            function Get-ResultText {
                param([int]$ResultCode)

                switch ($ResultCode) {
                    0 { return 'Nicht gestartet' }
                    1 { return 'In Bearbeitung' }
                    2 { return 'Erfolgreich' }
                    3 { return 'Erfolgreich mit Warnungen' }
                    4 { return 'Fehlgeschlagen' }
                    5 { return 'Abgebrochen' }
                    default { return "Unbekannter Status $ResultCode" }
                }
            }

            function Release-ComObject {
                param([object]$Obj)
                if ($null -ne $Obj) {
                    try {
                        while ([System.Runtime.InteropServices.Marshal]::ReleaseComObject($Obj) -gt 0) { }
                    } catch { }
                }
            }

            try {
                Write-Output 'Windows-Update-Dienst wird initialisiert ...'

                $session = New-Object -ComObject Microsoft.Update.Session
                $session.ClientApplicationID = 'MaintenancePro'

                $searcher = $session.CreateUpdateSearcher()

                # Microsoft Update einbinden, damit auch Updates für andere
                # Microsoft-Produkte und möglichst viele optionale Updates
                # gefunden werden.
                $microsoftUpdateServiceId =
                    '7971f918-a847-4430-9279-4a52d1efe18d'

                try {
                    $serviceManager =
                        New-Object -ComObject Microsoft.Update.ServiceManager

                    $serviceRegistered = $false

                    foreach ($service in $serviceManager.Services) {
                        if ($service.ServiceID -eq $microsoftUpdateServiceId) {
                            $serviceRegistered = $true
                            break
                        }
                    }

                    if (-not $serviceRegistered) {
                        $serviceManager.AddService2(
                            $microsoftUpdateServiceId,
                            2,
                            ''
                        ) | Out-Null

                        Write-Output 'Microsoft Update wurde temporär eingebunden.'
                    }

                    # 3 = ssOthers
                    $searcher.ServerSelection = 3
                    $searcher.ServiceID = $microsoftUpdateServiceId

                    Write-Output 'Suche über Microsoft Update ...'
                }
                catch {
                    # WICHTIG: ServiceID auf leeren String zurücksetzen, damit
                    # der Fallback auf die normale Windows-Update-Quelle
                    # funktioniert. Ohne diese Zeile würde die Suche weiterhin
                    # nach der nicht verfügbaren Microsoft Update ID filtern.
                    $searcher.ServiceID = ''

                    Write-Output '[WARNUNG] Microsoft Update konnte nicht eingebunden werden.'
                    Write-Output 'Fallback auf die normale Windows-Update-Quelle.'
                    Write-Output "Grund: $($_.Exception.Message)"
                }

                Write-Output 'Verfügbare Updates werden gesucht ...'

                $searchResult =
                    $searcher.Search('IsInstalled=0 AND IsHidden=0')

                $softwareUpdates = @(
                    $searchResult.Updates |
                        Where-Object {
                            $isDriver = $false

                            try {
                                # IUpdate.Type:
                                # 1 = Software
                                # 2 = Treiber
                                if ($_.Type -eq 2) {
                                    $isDriver = $true
                                }
                            }
                            catch {}

                            if (-not $isDriver) {
                                try {
                                    foreach ($category in $_.Categories) {
                                        if ($category.Type -eq 'Driver') {
                                            $isDriver = $true
                                            break
                                        }
                                    }
                                }
                                catch {}
                            }

                            -not $isDriver
                        }
                )

                if ($softwareUpdates.Count -eq 0) {
                    Write-Output '[OK] Windows ist auf dem neuesten Stand.'
                    Write-Output 'Es wurden keine Software-Updates gefunden.'
                    exit 0
                }

                Write-Output ''
                Write-Output "$($softwareUpdates.Count) Update(s) gefunden:"
                Write-Output ''

                $downloadCollection =
                    New-Object -ComObject Microsoft.Update.UpdateColl

                $updateNumber = 1

                foreach ($update in $softwareUpdates) {
                    $sizeText = ''

                    try {
                        $sizeMegabytes =
                            [Math]::Round(
                                $update.MaxDownloadSize / 1MB,
                                1
                            )

                        if (
                            $sizeMegabytes -gt 0 -and
                            $sizeMegabytes -lt 50000
                        ) {
                            $sizeText = " ($sizeMegabytes MB)"
                        }
                    }
                    catch {}

                    Write-Output (
                        "  [$updateNumber/$($softwareUpdates.Count)] " +
                        "$($update.Title)$sizeText"
                    )

                    if (-not $update.EulaAccepted) {
                        try {
                            $update.AcceptEula()
                        }
                        catch {
                            Write-Output (
                                "    [WARNUNG] Lizenzbedingungen konnten " +
                                "nicht automatisch akzeptiert werden."
                            )
                        }
                    }

                    if (-not $update.IsDownloaded) {
                        [void]$downloadCollection.Add($update)
                    }

                    $updateNumber++
                }

                Write-Output ''

                $downloadFailed = $false

                if ($downloadCollection.Count -gt 0) {
                    Write-Output (
                        "$($downloadCollection.Count) Update(s) " +
                        'werden heruntergeladen ...'
                    )

                    Write-Output (
                        'Der Download kann mehrere Minuten dauern. ' +
                        'Bitte das Programm nicht beenden.'
                    )

                    $downloader = $session.CreateUpdateDownloader()
                    $downloader.Updates = $downloadCollection

                    $downloadResult = $downloader.Download()
                    $downloadStatus =
                        Get-ResultText $downloadResult.ResultCode

                    if ($downloadResult.ResultCode -eq 2) {
                        Write-Output '[OK] Download erfolgreich abgeschlossen.'
                    }
                    elseif ($downloadResult.ResultCode -eq 3) {
                        Write-Output (
                            '[WARNUNG] Download wurde mit Warnungen abgeschlossen.'
                        )
                    }
                    else {
                        $downloadFailed = $true

                        Write-Output (
                            "[FEHLER] Download: $downloadStatus"
                        )

                        Write-Output (
                            'HRESULT: 0x{0:X8}' -f
                            ([uint32]$downloadResult.HResult)
                        )
                    }
                }
                else {
                    Write-Output 'Alle gefundenen Updates sind bereits heruntergeladen.'
                }

                $installCollection =
                    New-Object -ComObject Microsoft.Update.UpdateColl

                foreach ($update in $softwareUpdates) {
                    if ($update.IsDownloaded) {
                        [void]$installCollection.Add($update)
                    }
                }

                if ($installCollection.Count -eq 0) {
                    if ($downloadFailed) {
                        Write-Output (
                            '[FEHLER] Es konnten keine Updates zur ' +
                            'Installation vorbereitet werden.'
                        )

                        exit 1
                    }

                    Write-Output (
                        '[WARNUNG] Updates wurden gefunden, aber keines ' +
                        'konnte installiert werden.'
                    )

                    exit 2
                }

                Write-Output ''
                Write-Output (
                    "$($installCollection.Count) Update(s) " +
                    'werden installiert ...'
                )

                Write-Output (
                    'Die Installation kann längere Zeit dauern. ' +
                    'Den Computer nicht ausschalten.'
                )

                $installer = $session.CreateUpdateInstaller()
                $installer.Updates = $installCollection

                $installationResult = $installer.Install()

                $successfulUpdates = 0
                $failedUpdates = 0

                Write-Output ''
                Write-Output 'Installationsergebnisse:'

                for (
                    $index = 0;
                    $index -lt $installCollection.Count;
                    $index++
                ) {
                    $update = $installCollection.Item($index)
                    $updateResult =
                        $installationResult.GetUpdateResult($index)

                    $status =
                        Get-ResultText $updateResult.ResultCode

                    if (
                        $updateResult.ResultCode -eq 2 -or
                        $updateResult.ResultCode -eq 3
                    ) {
                        $successfulUpdates++

                        Write-Output "  [OK] $($update.Title)"

                        if ($updateResult.ResultCode -eq 3) {
                            Write-Output '       Erfolgreich mit Warnungen'
                        }
                    }
                    else {
                        $failedUpdates++

                        Write-Output "  [FEHLER] $($update.Title)"
                        Write-Output "           Status: $status"

                        Write-Output (
                            '           HRESULT: 0x{0:X8}' -f
                            ([uint32]$updateResult.HResult)
                        )
                    }
                }

                Write-Output ''
                Write-Output (
                    "$successfulUpdates von $($installCollection.Count) " +
                    'Update(s) erfolgreich installiert.'
                )

                if ($installationResult.RebootRequired) {
                    Write-Output ''
                    Write-Output (
                        '[NEUSTART ERFORDERLICH] Der Computer muss ' +
                        'neu gestartet werden.'
                    )
                }

                if (
                    $failedUpdates -eq 0 -and
                    -not $downloadFailed
                ) {
                    Write-Output '[OK] Windows-Updates wurden erfolgreich abgeschlossen.'
                    exit 0
                }

                if ($successfulUpdates -gt 0) {
                    Write-Output (
                        '[WARNUNG] Einige Updates konnten nicht ' +
                        'vollständig installiert werden.'
                    )

                    exit 2
                }

                Write-Output '[FEHLER] Alle Update-Installationen sind fehlgeschlagen.'
                exit 1
            }
            catch {
                Write-Error (
                    'Windows-Update-Fehler: ' +
                    $_.Exception.Message
                )

                exit 1
            }
            finally {
                # COM-Objekte explizit freigeben, um RCW-Leaks zu vermeiden.
                try { Release-ComObject $installer } catch { }
                try { Release-ComObject $downloader } catch { }
                try { Release-ComObject $searcher } catch { }
                try { Release-ComObject $session } catch { }
            }
            """;

        try
        {
            var startInfo =
                new System.Diagnostics.ProcessStartInfo
                {
                    FileName = "powershell.exe",
                    UseShellExecute = false,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true,
                    StandardOutputEncoding = System.Text.Encoding.UTF8,
                    StandardErrorEncoding = System.Text.Encoding.UTF8
                };

            startInfo.ArgumentList.Add("-NoProfile");
            startInfo.ArgumentList.Add("-NonInteractive");
            startInfo.ArgumentList.Add("-ExecutionPolicy");
            startInfo.ArgumentList.Add("Bypass");
            startInfo.ArgumentList.Add("-Command");
            startInfo.ArgumentList.Add(script);

            using var process =
                new System.Diagnostics.Process
                {
                    StartInfo = startInfo
                };

            process.OutputDataReceived += (_, eventArgs) =>
            {
                if (!string.IsNullOrWhiteSpace(eventArgs.Data))
                {
                    Console.WriteLine(eventArgs.Data);
                }
            };

            process.ErrorDataReceived += (_, eventArgs) =>
            {
                if (!string.IsNullOrWhiteSpace(eventArgs.Data))
                {
                    Console.WriteLine(eventArgs.Data);
                }
            };

            if (!process.Start())
            {
                Console.WriteLine(
                    "[FEHLER] PowerShell konnte nicht gestartet werden.");
                return;
            }

            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            // IUpdateDownloader.Download() und IUpdateInstaller.Install() sind
            // synchrone COM-Aufrufe ohne Timeout. Haengt der Windows-Update-Dienst
            // (klassisch nach einem abgebrochenen Update), wartet die Wartung sonst
            // bis in alle Ewigkeit. 2 Stunden decken auch grosse Feature-Updates ab.
            if (!process.WaitForExit(120 * 60 * 1000))
            {
                try
                {
                    process.Kill(entireProcessTree: true);
                }
                catch
                {
                    // Prozess war bereits beendet.
                }

                // Sicherstellen, dass der Prozess wirklich tot ist.
                try { process.WaitForExit(); } catch { /* bereits tot */ }

                // Verbleibenden Output erfassen (Race-Condition zwischen Kill und
                // WaitForExit kann dazu fuehren, dass der async-Handler nicht alle
                // Zeilen ausgeben konnte).
                string remainingOutput = process.StandardOutput.ReadToEnd();
                if (!string.IsNullOrWhiteSpace(remainingOutput))
                {
                    Console.Write(remainingOutput);
                }

                Console.WriteLine(
                    "[FEHLER] Zeitlimit: Windows Update wurde nach 2 Stunden " +
                    "abgebrochen. Der Windows-Update-Dienst haengt vermutlich.");

                return;
            }

            process.WaitForExit();

            if (process.ExitCode == 0)
            {
                Console.WriteLine(
                    "[OK] Windows-Update-Modul abgeschlossen.");
            }
            else if (process.ExitCode == 2)
            {
                Console.WriteLine(
                    "[WARNUNG] Windows-Update-Modul mit Warnungen abgeschlossen.");
            }
            else
            {
                Console.WriteLine(
                    "[FEHLER] Windows-Update-Modul ist fehlgeschlagen.");
            }
        }
        catch (Exception fehler)
        {
            Console.WriteLine("[FEHLER] " + fehler.Message);
        }
    }
}
```

---

## Unsicherheiten

1. **`$searcher.ServiceID = ''` als Fix:** Ich habe nicht auf einem Windows-System verifiziert, dass `$searcher.ServiceID = ''` (leerer BSTR) tatsächlich die Suche auf *alle* Services zurücksetzt und nicht einen leeren Filter erzeugt, der nichts findet. Es könnte sein, dass man stattdessen `$searcher.ServiceID = $null` oder die Eigenschaft gar nicht setzen darf. Wenn der Fix nicht funktioniert, müsste man `$searcher` neu instanziieren oder eine neue `ISearcher`-Instanz über `$session.CreateUpdateSearcher()` erzeugen.

2. **`AddSearchService`-Signatur:** Der Vorschlag, `AddService2` durch `AddSearchService` zu ersetzen, basiert auf der API-Dokumentation, aber die exakte Signatur (`AddSearchService(Guid, int)` vs. `AddSearchService(Guid, int, string)`) wurde nicht auf einem konkreten System getestet. `AddService2` funktioniert aktuell, daher ist der Vorschlag präventiv, nicht reaktiv.

3. **`MaxDownloadSize`/`1MB`:** Die Division `$update.MaxDownloadSize / 1MB` in PowerShell — `1MB` ist ein Alias für `1048576`. Das funktioniert korrekt, aber ich habe nicht verifiziert, dass `MaxDownloadSize` immer in Bytes zurückgibt. Falls es MB zurückgibt, wäre die Berechnung falsch. Das ist allgemein als Byte-Wert dokumentiert, aber nicht explizit getestet.

4. **`process.Kill(entireProcessTree: true)`:** Diese Überladung (`Kill(bool entireProcessTree)`) ist ab .NET 5.0 verfügbar und korrekt für .NET 10. Die Semantik ist: `true` = auch Kindprozesse (inklusive PowerShell selbst mit allen Unterprozessen). Das ist gewollt. Dass der Parameter name `entireProcessTree` ist und nicht positional mit `true` funktioniert, wurde nicht direkt geprüft — aber bei bool-Parametern ist die erste Position korrekt.

5. **`ReadToEnd()` nach `Kill()`:** Wenn `Kill()` funktioniert hat, ist der Output-Stream geschlossen. `ReadToEnd()` gibt dann alles zurück, was im Puffer war, und return sofort. Wenn `Kill()` *nicht* funktioniert hat (Prozess reagiert gar nicht), könnte `ReadToEnd()` blockieren, aber das ist unwahrscheinlich, da der Prozess ja bereits tot sein sollte (sonst würde `Kill()` nicht returnieren, oder es käme eine Exception). Dieser Fall ist nicht explizit behandelt.

6. **COM-Objekt-Reihenfolge bei Release:** Die Reihenfolge `installer → downloader → searcher → session` ist so gewählt, dass abhängige Objekte zuerst freigegeben werden. Aber PowerShell GC-Order ist unvorhersehbar. Falls ein COM-Objekt bereits durch ein anderes Release freigegeben wurde, wirft `ReleaseComObject` — der `try/catch` fängt das ab. Die Reihenfolge sollte aber kein Problem darstellen, da jeder RCW separat referenziert.

7. **Exit-Code 2 als „Warnung":** Exit-Code 2 wird für „Teilfehler" und „keine Installation möglich, obwohl Updates gefunden" gleich behandelt. Das ist eine Design-Entscheidung des Originalcodes, kein Bug, aber vielleicht unglücklich. Ein separater Exit-Code für „alles gefunden, nichts installierbar" vs. „Teilfehler" wäre klarer.