1) BEFUNDE

Geprüfte Datei:

Zeilen 152–191, Auswertung von $nothingToUpdate — kritisch
Die textbasierte Erkennung wird vor dem Exit-Code ausgewertet. Enthält die Ausgabe bei einem fehlgeschlagenen winget upgrade zufällig einen der erkannten Texte, beendet das Skript sich mit Exit-Code 0, obwohl Winget einen Fehler gemeldet hat. Das Wartungstool meldet dadurch einen falschen Erfolg.
Zeilen 152–185, Analyse der Winget-Ausgabe — mittel
Erfolg, keine Updates und Neustartanforderungen werden über englische, deutsche und französische Textfragmente erkannt. Das ist abhängig von Windows-Sprache, Winget-Version und exakter Formulierung. Auf anderen Sprachen oder nach einer Textänderung kann die Klassifizierung falsch sein. Exit-Codes sind für die grundlegende Erfolgsbewertung verlässlicher.
Zeilen 164–229, $successfulUpdate — mittel
Ein einzelner erkannter Erfolgstext führt bei einem nicht erfolgreichen Winget-Exit-Code zur Aussage, einige Apps seien erfolgreich aktualisiert worden. Das muss nicht stimmen: Der Text kann aus einer Installer-Ausgabe stammen, während Winget den eigentlichen Vorgang anders bewertet. Eine sichere Teil-Erfolgsbewertung ist ohne strukturierte, stabile Winget-Ausgabe nicht möglich.
Zeilen 67–79, Suche in allen Benutzerprofilen — mittel
Die Datei sucht unter C:\Users\... nach winget.exe. Winget beziehungsweise der App-Installer ist benutzerbezogen registriert. Eine ausführbare Datei aus einem fremden Benutzerprofil kann unzugänglich, nicht korrekt registriert oder für den aktuellen Benutzer ungeeignet sein. Zusätzlich wird unnötig über fremde Profile iteriert.
Zeilen 47–79, leere catch-Blöcke — mittel
Fehler beim Zugriff auf WindowsApps und Benutzerprofile werden vollständig verschluckt. Bei Berechtigungs-, Dateisystem- oder Pfadproblemen ist später nicht mehr nachvollziehbar, weshalb Winget nicht gefunden wurde.
Zeilen 111–124 und 320–324, fehlgeschlagenes source update — mittel
Ein fehlgeschlagenes Quellenupdate wird zunächst korrekt als Warnung behandelt. Wenn das anschließende Upgrade Exit-Code 0 liefert, meldet C# am Ende dennoch uneingeschränkt, das Modul sei erfolgreich abgeschlossen. Die vorherige Warnung geht in der abschließenden Bewertung verloren.
Zeilen 247–266, PowerShell mit ExecutionPolicy Bypass — mittel
Für den Aufruf von Winget ist PowerShell nicht erforderlich. Dadurch entsteht eine zusätzliche Fehlerquelle: PowerShell kann fehlen, blockiert sein oder durch Richtlinien beziehungsweise Sicherheitssoftware eingeschränkt werden. ExecutionPolicy Bypass ist hier unnötig. Winget kann mit ProcessStartInfo.ArgumentList direkt und injectionsicher gestartet werden.
Zeilen 302–315, Timeout-Behandlung — gering
Nach Kill(entireProcessTree: true) wird nicht darauf gewartet, dass der Prozess tatsächlich beendet wurde und die asynchronen Ausgabeleser abgeschlossen sind. Dadurch können letzte Ausgaben verloren gehen oder Prozesse noch kurz weiterlaufen, während das Modul bereits zurückkehrt.
Zeilen 274–288, Ausgabeereignisse — gering
Standardausgabe und Standardfehler werden parallel direkt auf dieselbe Konsole geschrieben. Ein Deadlock wird dadurch zwar vermieden, aber die Reihenfolge beider Streams ist nicht garantiert. Das ist technisch nicht vollständig vermeidbar, solange beide Streams getrennt bleiben.
Zeilen 1–6 und mehrfach vollständig qualifizierte Typnamen — gering
Mehrere using-Direktiven sind unbenutzt, während Process, ProcessStartInfo und Encoding trotzdem vollständig qualifiziert werden. Das verursacht keinen Laufzeitfehler, erschwert aber die Wartung leicht.
2) VERBESSERTE DATEI
using System.ComponentModel;
using System.Diagnostics;
using System.Text;

namespace JustUpdate.Module;

/// <summary>
/// Installierte Apps ueber winget aktualisieren
/// </summary>
internal static class Apps
{
    public const string Name = "apps";

    private static readonly TimeSpan QuellenTimeout = TimeSpan.FromMinutes(10);
    private static readonly TimeSpan UpgradeTimeout = TimeSpan.FromMinutes(60);

    public static void Ausfuehren()
    {
        Console.WriteLine("[A] Installierte Apps werden aktualisiert ...");

        if (!OperatingSystem.IsWindows())
        {
            Console.WriteLine(
                "[FEHLER] Diese Funktion ist nur unter Windows verfuegbar.");
            return;
        }

        try
        {
            string wingetPfad = ErmittleWingetPfad();

            Console.WriteLine($"Winget wird verwendet: {wingetPfad}");
            Console.WriteLine("Winget-Quellen werden aktualisiert ...");

            ProzessErgebnis quellenErgebnis = FuehreProzessAusAsync(
                    wingetPfad,
                    [
                        "source",
                        "update",
                        "--disable-interactivity"
                    ],
                    QuellenTimeout)
                .GetAwaiter()
                .GetResult();

            bool quellenWarnung;

            if (quellenErgebnis.Zeitueberschreitung)
            {
                quellenWarnung = true;

                Console.WriteLine(
                    "[WARNUNG] Das Aktualisieren der Winget-Quellen wurde " +
                    "nach 10 Minuten abgebrochen.");

                Console.WriteLine(
                    "Die App-Aktualisierung wird mit dem vorhandenen " +
                    "Paketindex fortgesetzt.");
            }
            else if (quellenErgebnis.ExitCode != 0)
            {
                quellenWarnung = true;

                Console.WriteLine(
                    "[WARNUNG] Die Winget-Quellen konnten nicht vollstaendig " +
                    "aktualisiert werden.");

                Console.WriteLine(
                    $"Winget-Rueckgabecode: " +
                    $"{FormatiereExitCode(quellenErgebnis.ExitCode)}");

                Console.WriteLine(
                    "Die App-Aktualisierung wird mit dem vorhandenen " +
                    "Paketindex fortgesetzt.");
            }
            else
            {
                quellenWarnung = false;
                Console.WriteLine("[OK] Winget-Quellen wurden aktualisiert.");
            }

            Console.WriteLine();
            Console.WriteLine(
                "Verfuegbare App-Updates werden installiert ...");

            Console.WriteLine(
                "Das kann mehrere Minuten dauern. " +
                "Bitte das Programm nicht beenden.");

            ProzessErgebnis upgradeErgebnis = FuehreProzessAusAsync(
                    wingetPfad,
                    [
                        "upgrade",
                        "--all",
                        "--include-unknown",
                        "--disable-interactivity",
                        "--accept-source-agreements",
                        "--accept-package-agreements"
                    ],
                    UpgradeTimeout)
                .GetAwaiter()
                .GetResult();

            Console.WriteLine();

            if (upgradeErgebnis.Zeitueberschreitung)
            {
                Console.WriteLine(
                    "[FEHLER] Die App-Aktualisierung wurde nach 60 Minuten " +
                    "abgebrochen.");
                return;
            }

            if (upgradeErgebnis.ExitCode != 0)
            {
                Console.WriteLine(
                    "[FEHLER] Die App-Aktualisierung ist fehlgeschlagen.");

                Console.WriteLine(
                    $"Winget-Rueckgabecode: " +
                    $"{FormatiereExitCode(upgradeErgebnis.ExitCode)}");

                Console.WriteLine(
                    "[HINWEIS] Einzelne Pakete koennen bereits aktualisiert " +
                    "worden sein. Massgebend ist die vorangehende " +
                    "Winget-Ausgabe.");

                return;
            }

            if (quellenWarnung)
            {
                Console.WriteLine(
                    "[WARNUNG] Die App-Aktualisierung wurde abgeschlossen, " +
                    "aber die Winget-Quellen konnten zuvor nicht " +
                    "vollstaendig aktualisiert werden.");
            }
            else
            {
                Console.WriteLine(
                    "[OK] App-Aktualisierungsmodul abgeschlossen.");
            }
        }
        catch (Win32Exception fehler)
            when (fehler.NativeErrorCode is 2 or 3)
        {
            Console.WriteLine(
                "[FEHLER] Winget konnte nicht gestartet werden.");

            Console.WriteLine(
                "Installiere oder repariere im Microsoft Store die " +
                "Anwendung \"App-Installer\".");
        }
        catch (Win32Exception fehler)
            when (fehler.NativeErrorCode == 5)
        {
            Console.WriteLine(
                "[FEHLER] Der Zugriff auf Winget wurde verweigert.");

            Console.WriteLine(
                "Pruefe die Windows-App-Ausfuehrungsaliase und die " +
                "Berechtigungen des aktuellen Benutzers.");
        }
        catch (UnauthorizedAccessException fehler)
        {
            Console.WriteLine(
                "[FEHLER] Fuer die App-Aktualisierung fehlen Berechtigungen.");

            Console.WriteLine($"Details: {fehler.Message}");
        }
        catch (Exception fehler)
        {
            Console.WriteLine(
                "[FEHLER] Unerwarteter Fehler bei der App-Aktualisierung:");

            Console.WriteLine(fehler.Message);
        }
    }

    private static string ErmittleWingetPfad()
    {
        string? lokalerAppPfad =
            Environment.GetFolderPath(
                Environment.SpecialFolder.LocalApplicationData);

        if (!string.IsNullOrWhiteSpace(lokalerAppPfad))
        {
            string aliasPfad = Path.Combine(
                lokalerAppPfad,
                "Microsoft",
                "WindowsApps",
                "winget.exe");

            if (File.Exists(aliasPfad))
            {
                return aliasPfad;
            }
        }

        string? pathVariable = Environment.GetEnvironmentVariable("PATH");

        if (!string.IsNullOrWhiteSpace(pathVariable))
        {
            foreach (string verzeichnis in pathVariable.Split(
                         Path.PathSeparator,
                         StringSplitOptions.RemoveEmptyEntries |
                         StringSplitOptions.TrimEntries))
            {
                string bereinigtesVerzeichnis =
                    verzeichnis.Trim().Trim('"');

                if (string.IsNullOrWhiteSpace(bereinigtesVerzeichnis))
                {
                    continue;
                }

                string kandidat = Path.Combine(
                    bereinigtesVerzeichnis,
                    "winget.exe");

                try
                {
                    if (File.Exists(kandidat))
                    {
                        return kandidat;
                    }
                }
                catch (Exception fehler)
                    when (fehler is ArgumentException
                        or NotSupportedException
                        or PathTooLongException)
                {
                    // Ungueltige einzelne PATH-Eintraege werden ignoriert.
                }
            }
        }

        // Der direkte Start liefert bei fehlendem Winget einen
        // aussagekraeftigen Win32Exception-Fehler.
        return "winget.exe";
    }

    private static async Task<ProzessErgebnis> FuehreProzessAusAsync(
        string dateiname,
        IReadOnlyList<string> argumente,
        TimeSpan timeout)
    {
        var startInfo = new ProcessStartInfo
        {
            FileName = dateiname,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true,
            CreateNoWindow = true,
            StandardOutputEncoding = new UTF8Encoding(false),
            StandardErrorEncoding = new UTF8Encoding(false)
        };

        foreach (string argument in argumente)
        {
            startInfo.ArgumentList.Add(argument);
        }

        using var prozess = new Process
        {
            StartInfo = startInfo
        };

        if (!prozess.Start())
        {
            throw new InvalidOperationException(
                $"Der Prozess \"{dateiname}\" konnte nicht gestartet werden.");
        }

        Task standardausgabeTask = KopiereAusgabeAsync(
            prozess.StandardOutput,
            istFehlerausgabe: false);

        Task fehlerausgabeTask = KopiereAusgabeAsync(
            prozess.StandardError,
            istFehlerausgabe: true);

        using var timeoutQuelle = new CancellationTokenSource(timeout);

        try
        {
            await prozess.WaitForExitAsync(timeoutQuelle.Token)
                .ConfigureAwait(false);
        }
        catch (OperationCanceledException)
            when (timeoutQuelle.IsCancellationRequested)
        {
            try
            {
                prozess.Kill(entireProcessTree: true);
            }
            catch (InvalidOperationException)
            {
                // Der Prozess wurde zwischenzeitlich bereits beendet.
            }
            catch (Win32Exception)
            {
                // Das Beenden kann wegen eines gleichzeitigen Prozessendes
                // oder fehlender Rechte fehlschlagen.
            }

            try
            {
                await prozess.WaitForExitAsync().ConfigureAwait(false);
            }
            catch (InvalidOperationException)
            {
                // Der Prozess besitzt keinen laufenden Prozess mehr.
            }

            await Task.WhenAll(
                    standardausgabeTask,
                    fehlerausgabeTask)
                .ConfigureAwait(false);

            return new ProzessErgebnis(
                ExitCode: -1,
                Zeitueberschreitung: true);
        }

        await Task.WhenAll(
                standardausgabeTask,
                fehlerausgabeTask)
            .ConfigureAwait(false);

        return new ProzessErgebnis(
            ExitCode: prozess.ExitCode,
            Zeitueberschreitung: false);
    }

    private static async Task KopiereAusgabeAsync(
        StreamReader leser,
        bool istFehlerausgabe)
    {
        while (await leser.ReadLineAsync().ConfigureAwait(false)
               is { } zeile)
        {
            if (istFehlerausgabe)
            {
                Console.Error.WriteLine(zeile);
            }
            else
            {
                Console.WriteLine(zeile);
            }
        }
    }

    private static string FormatiereExitCode(int exitCode)
    {
        return $"{exitCode} (0x{unchecked((uint)exitCode):X8})";
    }

    private readonly record struct ProzessErgebnis(
        int ExitCode,
        bool Zeitueberschreitung);
}
3) BEWUSST NICHT GEÄNDERT
Öffentliche Schnittstelle: Name und Ausfuehren() bleiben unverändert. Auch Klassenname, Namespace und Sichtbarkeit wurden nicht verändert.
winget upgrade --all: Das Modul aktualisiert weiterhin alle verfügbaren Apps. Das entspricht klar dem bisherigen Zweck des Moduls.
--include-unknown: Die Option bleibt erhalten, da ansonsten Pakete ohne erkennbare installierte Version ausgelassen werden könnten.
Quellenfehler sind weiterhin nicht zwingend fatal: Ein vorhandener Paketindex kann noch verwendbar sein. Die Abschlussmeldung bewahrt die Warnung nun jedoch sichtbar auf.
Keine sprachabhängige Interpretation der Ausgabe: Meldungen wie „keine Updates“, „Teil-Erfolg“ oder „Neustart erforderlich“ werden nicht mehr aus lokalisierten Texten abgeleitet. Winget zeigt seine Originalausgabe weiterhin vollständig an.
Keine spezielle Behandlung einzelner Winget-HRESULTs: Ohne eine verbindlich stabile Liste für die konkret eingesetzte Winget-Version wäre eine harte Zuordnung bestimmter numerischer Codes spekulativ. Der Code zeigt deshalb Dezimal- und Hexwert an.
Getrennte Ausgabe von stdout und stderr: Beide Streams werden gleichzeitig gelesen, damit kein Pipe-Deadlock entstehen kann. Ihre exakte zeitliche Reihenfolge kann betriebssystembedingt weiterhin leicht abweichen.
60-Minuten-Timeout: Der vorhandene Grenzwert wurde beibehalten, weil große Pakete oder langsame Installer tatsächlich längere Zeit benötigen können.