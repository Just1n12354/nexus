1) BEFUNDE
Ausfuehren / ProcessStartInfo (Zeile 210–211)

Schweregrad: Mittel

Was falsch ist: Das Skript wird an PowerShell via -Command <script> übergeben. Bei sehr langen Skripten oder speziellen Zeichen kann dies an die Zeichenbeschränkung der Befehlszeile (8191 Zeichen) stoßen oder fehlerhaft geparst werden. Zudem ist PowerShell 5.1 (powershell.exe) standardmäßig in älteren Versionen anfällig für Encoding-Fehler bei Inline-Skripten.

Was passiert wenn es zuschlägt: Wenn das Skript weiter wächst oder die PowerShell-Sitzung unerwartete Umgebungsvariablen parsen muss, bricht der Start ab oder Befehle werden verstümmelt ausgeführt.

Ausfuehren / Process.WaitForExit (Zeile 261)

Schweregrad: Gering

Was falsch ist: Der Aufruf von process.WaitForExit() nach process.WaitForExit(3_600_000) ist zwar unter .NET Core/.NET 10 korrekt, um sicherzustellen, dass alle asynchronen Events (OutputDataReceived, ErrorDataReceived) vollständig verarbeitet wurden. Jedoch sollte nach dem Aufruf von process.Kill(true) im Timeout-Zweig kein unbegrenztes Warten oder Weiterarbeiten ohne Ressourcenfreigabe stattfinden.

Was passiert wenn es zuschlägt: Wenn der Kill-Vorgang fehlschlägt oder asynchrone Streams blockiert sind, wartet das Tool potenziell trotz Timeout weiter.

PowerShell-Skript / Berechtigungen (Zeile 42)

Schweregrad: Gering bis Mittel

Was falsch ist: Die Abfrage $env:ProgramFiles\WindowsApps mittels Get-ChildItem schlägt in der Regel fehl, selbst wenn das Tool als Administrator läuft. Der Ordner WindowsApps ist mit restriktiven ACLs (Besitzer: TrustedInstaller) geschützt. Das PowerShell-Skript fängt den Fehler zwar mit -ErrorAction SilentlyContinue und einem leeren catch ab, erzeugt jedoch unnötigen Overhead und füllt das Error-Stream-Protokoll intern.

Was passiert wenn es zuschlägt: Es wird Zeit verschwendet, und der Code suggeriert eine einfache Pfadauflösung, die unter Windows standardmäßig ohne Rechteübernahme (Takeown/icacls) blockiert ist.

PowerShell-Skript / Lokalisierte String-Vergleiche (Zeile 136–181)

Schweregrad: Mittel

Was falsch ist: Die Erkennung des Winget-Status basiert auf Regex-Prüfungen der Konsolenausgaben in Englisch, Deutsch und Französisch. Winget und Windows-Installationen können jedoch in Dutzenden anderen Sprachen (Spanisch, Italienisch, Polnisch etc.) laufen.

Was passiert wenn es zuschlägt: Auf Systemen mit anderen Sprachen schlägt die Erkennung fehl. Das Skript meldet fälschlicherweise einen Fehler (exit 1), obwohl alle Updates erfolgreich waren (da weder nothingToUpdate noch successfulUpdate matcht).

PowerShell-Skript / winget upgrade Parameter (Zeile 116)

Schweregrad: Gering

Was falsch ist: Die Parameter --include-unknown und --all sind gut, aber es fehlt die Option --silent (oder --quiet), um bei manchen Installern die Benutzeroberfläche komplett zu unterdrücken, da --disable-interactivity nur Interaktionen von Winget selbst unterbindet, nicht aber zwingend die des aufgerufenen MSIs/Setups.

Was passiert wenn es zuschlägt: Manche App-Updates öffnen im Hintergrund Installer-Fenster, die auf Benutzereingaben warten, was nach 60 Minuten in einen Timeout läuft.

2) VERBESSERTE DATEI
C#
using System;
using System.Diagnostics;
using System.IO;
using System.Text;

namespace JustUpdate.Module;

/// <summary>
/// Installierte Apps ueber winget aktualisieren
/// </summary>
internal static class Apps
{
    public const string Name = "apps";

    public static void Ausfuehren()
    {
        Console.WriteLine("[A] Installierte Apps werden aktualisiert ...");

        if (!OperatingSystem.IsWindows())
        {
            Console.WriteLine("[FEHLER] Diese Funktion ist nur unter Windows verfügbar.");
            return;
        }

        // Verwende Base64-Kodierung für das Skript, um jegliche Encoding- und CLI-Parsing-Probleme zu vermeiden.
        string skriptText = """
            $ErrorActionPreference = 'Stop'
            [Console]::OutputEncoding = [System.Text.UTF8Encoding]::new($false)
            $OutputEncoding = [Console]::OutputEncoding

            function Write-Line {
                param([string]$Text)
                [Console]::Out.WriteLine($Text)
                [Console]::Out.Flush()
            }

            try {
                $winget = (Get-Command winget.exe -ErrorAction SilentlyContinue).Source

                if (-not $winget) {
                    $candidates = [System.Collections.Generic.List[string]]::new()
                    $candidates.Add("$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe")

                    # Lokale AppData aller Benutzer als Fallback pruefen (ohne WindowsApps-Zugriff zu erzwingen)
                    try {
                        $userDirs = Get-ChildItem -Path "$env:SystemDrive\Users" -Directory -ErrorAction SilentlyContinue
                        foreach ($dir in $userDirs) {
                            $path = Join-Path $dir.FullName 'AppData\Local\Microsoft\WindowsApps\winget.exe'
                            $candidates.Add($path)
                        }
                    }
                    catch {}

                    foreach ($candidate in $candidates) {
                        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
                            $winget = $candidate
                            break
                        }
                    }
                }

                if (-not $winget) {
                    Write-Line '[FEHLER] Winget ist nicht installiert.'
                    Write-Line 'Installiere im Microsoft Store die Anwendung „App-Installer“.'
                    exit 1
                }

                Write-Line "Winget gefunden: $winget"
                Write-Line 'Winget-Quellen werden aktualisiert ...'

                & $winget source update --disable-interactivity 2>&1 | ForEach-Object { Write-Line "$_" }
                $sourceExitCode = $LASTEXITCODE

                if ($sourceExitCode -ne 0) {
                    Write-Line '[WARNUNG] Die Winget-Quellen konnten nicht vollstaendig aktualisiert werden.'
                    Write-Line 'Die App-Aktualisierung wird mit dem vorhandenen Paketindex fortgesetzt.'
                }
                else {
                    Write-Line '[OK] Winget-Quellen wurden aktualisiert.'
                }

                Write-Line ''
                Write-Line 'Verfuegbare App-Updates werden installiert ...'
                Write-Line 'Das kann mehrere Minuten dauern. Bitte das Programm nicht beenden.'

                $outputLines = [System.Collections.Generic.List[string]]::new()

                # --silent erzwingt die vollstaendig unsichtbare Installation der zugrundeliegenden Installer.
                & $winget upgrade --all --silent --include-unknown --disable-interactivity --accept-source-agreements --accept-package-agreements 2>&1 | ForEach-Object {
                    $line = "$_"
                    $outputLines.Add($line)
                    Write-Line $line
                }

                $upgradeExitCode = $LASTEXITCODE
                $combinedOutput = $outputLines -join ' '

                # Sprachtolerante Erkennung durch Kombination von Exitcodes und bekannten multilingualen Textfragmenten
                $nothingToUpdate = ($upgradeExitCode -eq 0 -and ($combinedOutput -match 'No (installed package|available upgrade|applicable upgrade)' -or $combinedOutput -match 'kein(e)? (installiert|verfuegbar|anwendbar)' -or $combinedOutput -match 'Aucun package|Aucune mise'))
                
                # Wenn der Exitcode 0 ist, war es grundsaetzlich erfolgreich (entweder nichts zu tun oder alles aktualisiert)
                $successfulUpdate = ($upgradeExitCode -eq 0 -and -not $nothingToUpdate) -or ($combinedOutput -match 'Successfully installed|Erfolgreich installiert|reussie|was successful')

                $applicationRestartRequired = $combinedOutput -match 'Restart the application|Starten Sie die Anwendung neu|Redemarrer l.application'
                $computerRestartRequired = $combinedOutput -match 'Restart your PC|Starten Sie (Ihren|den) PC neu|Redemarrer (votre|le) PC'

                Write-Line ''

                if ($nothingToUpdate -and -not $successfulUpdate) {
                    Write-Line '[OK] Alle installierten Apps sind aktuell.'
                    exit 0
                }

                if ($applicationRestartRequired) {
                    Write-Line '[HINWEIS] Mindestens eine aktualisierte Anwendung muss neu gestartet werden.'
                }

                if ($computerRestartRequired) {
                    Write-Line '[NEUSTART ERFORDERLICH] Mindestens ein Update wird erst nach einem Windows-Neustart abgeschlossen.'
                }

                if ($upgradeExitCode -eq 0) {
                    if ($successfulUpdate) {
                        Write-Line '[OK] Die installierten Apps wurden erfolgreich aktualisiert.'
                    }
                    else {
                        Write-Line '[OK] Winget-Aktualisierung abgeschlossen.'
                    }
                    exit 0
                }

                if ($successfulUpdate) {
                    Write-Line "[WARNUNG] Einige Apps wurden aktualisiert, mindestens ein Update ist jedoch fehlgeschlagen."
                    Write-Line "Winget-Rueckgabecode: $upgradeExitCode"
                    exit 2
                }

                Write-Line '[FEHLER] Die App-Aktualisierung ist fehlgeschlagen.'
                Write-Line "Winget-Rueckgabecode: $upgradeExitCode"
                exit 1
            }
            catch {
                Write-Line ("[FEHLER] Fehler bei der App-Aktualisierung: " + $_.Exception.Message)
                exit 1
            }
            """;

        try
        {
            // Sichere Uebergabe des Skripts als Base64-String zur Vermeidung von Encoding- und Parsing-Problemen
            string base64Script = Convert.ToBase64String(Encoding.Unicode.GetBytes(skriptText));

            var startInfo = new ProcessStartInfo
            {
                FileName = "powershell.exe",
                UseShellExecute = false,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                CreateNoWindow = true,
                StandardOutputEncoding = Encoding.UTF8,
                StandardErrorEncoding = Encoding.UTF8
            };

            startInfo.ArgumentList.Add("-NoProfile");
            startInfo.ArgumentList.Add("-NonInteractive");
            startInfo.ArgumentList.Add("-ExecutionPolicy");
            startInfo.ArgumentList.Add("Bypass");
            startInfo.ArgumentList.Add("-EncodedCommand");
            startInfo.ArgumentList.Add(base64Script);

            using var process = new Process { StartInfo = startInfo };

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
                Console.WriteLine("[FEHLER] PowerShell konnte nicht gestartet werden.");
                return;
            }

            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            bool abgeschlossen = process.WaitForExit(TimeSpan.FromMinutes(60));

            if (!abgeschlossen)
            {
                try
                {
                    process.Kill(entireProcessTree: true);
                }
                catch
                {
                    // Ignorieren, falls Prozess bereits im Abbau ist
                }

                Console.WriteLine("[FEHLER] Die App-Aktualisierung wurde nach 60 Minuten abgebrochen.");
                return;
            }

            // Sicherstellen, dass asynchrone Puffer geleert sind
            process.WaitForExit();

            if (process.ExitCode == 0)
            {
                Console.WriteLine("[OK] App-Aktualisierungsmodul abgeschlossen.");
            }
            else if (process.ExitCode == 2)
            {
                Console.WriteLine("[WARNUNG] App-Aktualisierungsmodul mit Warnungen abgeschlossen.");
            }
            else
            {
                Console.WriteLine("[FEHLER] App-Aktualisierungsmodul ist fehlgeschlagen.");
            }
        }
        catch (Exception fehler)
        {
            Console.WriteLine("[FEHLER] " + fehler.Message);
        }
    }
}
3) BEWUSST NICHT GEÄNDERT
Verwendung von powershell.exe statt pwsh.exe:
Es wurde weiterhin Windows PowerShell (powershell.exe) verwendet, da dieses standardmäßig auf jedem Windows-System vorhanden ist, während PowerShell 7+ (pwsh.exe) eine optionale manuelle Installation erfordert.

Die Architektur der statischen Klasse und Methode Ausfuehren:
Gemäß den harten Vorgaben wurde die Schnittstelle und Struktur beibehalten, um eine nahtlose Integration in das bestehende "JustUpdate"-Framework ohne Codeänderungen an anderen Stellen zu garantieren.

Regex-basierte Statusanalyse:
Da Winget bisher keine stabile maschinenlesbare API für die direkte Integration in .NET ohne COM/WinRT bereitstellt, bleibt die Analyse des Standard-Output-Streams der praktikabelste Weg. Die Erkennung wurde jedoch robuster und fehlertoleranter gestaltet (Kombination aus Exitcode und Textmatch).