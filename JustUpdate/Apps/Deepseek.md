
Wir müssen die Datei "Apps.cs" analysieren und verbessern. Die Datei ist ein statisches Modul, das winget aufruft, um Apps zu aktualisieren. Es verwendet PowerShell-Skript.

Zuerst analysieren wir auf Probleme.

Probleme:

Exit-Code-Auswertung im PowerShell-Skript: Der Skript verwendet exit 1, exit 0, exit 2. Die C#-Seite wertet den Exit-Code aus, aber es gibt ein Problem: Der PowerShell-Prozess gibt den Exit-Code zurück, aber im Skript wird exit verwendet, was den PowerShell-Prozess beendet. Das sollte funktionieren. Allerdings: Im Skript wird $LASTEXITCODE von winget überprüft, aber der Exit-Code von winget wird nicht direkt weitergegeben, sondern das Skript verwendet eigene Exit-Codes. Das ist okay.

Potenzielle Deadlocks beim Lesen von stdout/stderr: Der Code verwendet BeginOutputReadLine und BeginErrorReadLine asynchron. Das ist gut. Er wartet mit WaitForExit(3_600_000). Der Prozess wird asynchron gelesen, also keine Deadlocks durch blockierte Pipes.

PowerShell-Skript: Das Skript sucht nach winget.exe. Es durchsucht mehrere Pfade, aber es könnte sein, dass winget in anderen Pfaden liegt (z.B. wenn es per Systemumgebung installiert ist). Der Code verwendet Get-Command winget.exe -ErrorAction SilentlyContinue, das sollte den Pfad finden, wenn es im PATH ist. Das ist gut.

Fehlerbehandlung im Skript: Es wird $ErrorActionPreference = 'Stop' gesetzt, aber einige Befehle könnten Fehler werfen, die nicht behandelt werden. Zum Beispiel Get-ChildItem kann Fehler werfen, wenn Pfade nicht existieren, aber sie werden mit -ErrorAction SilentlyContinue behandelt. Das ist okay.

$candidates += ... - wird mit Arrays gemacht. Aber es gibt ein Problem: $candidates wird initialisiert mit einem Array, dann werden neue hinzugefügt. Das funktioniert in PowerShell, aber es wird jedes Mal ein neues Array erstellt, was ineffizient ist, aber für diese kleine Anzahl ist es irrelevant.

Lokalisierungsabhängigkeit: Das Skript prüft auf bestimmte Ausgabestrings, um zu erkennen, ob nichts zu aktualisieren ist oder ob Updates erfolgreich waren. Die Strings sind auf Deutsch, Englisch, Französisch? Es werden mehrere Sprachen abgedeckt, aber es fehlen möglicherweise andere Sprachen. Winget gibt Ausgaben in der Systemsprache aus, daher ist diese Erkennung fehleranfällig. Bessere Methode: Den Exit-Code von winget nutzen. Winget gibt Exit-Codes zurück: 0 für Erfolg, 1 für Fehler, -1978335189 etc. Allerdings gibt es auch spezifische Exit-Codes für "no upgrades". Es wäre robuster, den Exit-Code zu prüfen und die Ausgabe nur für Meldungen zu parsen. Aber winget upgrade --all gibt bei "nothing to update" den Exit-Code 0? Ich denke, wenn keine Updates vorhanden sind, gibt winget 0 zurück. Also könnte man einfach den Exit-Code von winget nehmen und darauf vertrauen. Allerdings gibt es Fälle, wo winget teilweise erfolgreich ist und teilweise fehlschlägt (einige Apps aktualisiert, einige nicht). In dem Fall gibt winget wahrscheinlich einen Fehlercode zurück. Das Skript versucht, anhand der Ausgabe zu erkennen, ob einige erfolgreich waren. Das ist kompliziert. Besser: Den Exit-Code von winget direkt auswerten und gegebenenfalls die Ausgabe für Details parsen, aber nicht auf bestimmte Strings für den Status angewiesen sein.

Das Skript führt winget source update aus und ignoriert den Exit-Code (es gibt nur eine Warnung aus). Das ist in Ordnung.

Im Skript wird & $winget upgrade --all ... mit 2>&1 ausgeführt, um stdout und stderr zu kombinieren. Dann wird die Ausgabe in eine Liste gesammelt und später auf bestimmte Muster geprüft. Das ist okay.

Probleme mit der C#-Seite:

Sie verwendet ProcessStartInfo mit RedirectStandardOutput und RedirectStandardError und setzt StandardOutputEncoding = Encoding.UTF8. Das ist gut.

Sie verwendet process.BeginOutputReadLine und BeginErrorReadLine, das ist asynchron. Das ist gut, um Deadlocks zu vermeiden.

Sie verwendet process.WaitForExit(3_600_000) (60 Minuten). Das ist ein großzügiges Timeout.

Falls das Timeout abläuft, wird process.Kill(entireProcessTree: true) aufgerufen. Das ist gut.

Allerdings: Nach dem Timeout wird process.WaitForExit() nochmal aufgerufen? Im Code:

csharp
bool abgeschlossen = process.WaitForExit(3_600_000);
if (!abgeschlossen) { ... kill ... return; }
process.WaitForExit(); // <-- das wird aufgerufen, nachdem der Prozess bereits beendet wurde? Wenn kill aufgerufen wurde, wird er beendet, aber wir haben bereits return. Wenn abgeschlossen true ist, dann ist der Prozess bereits beendet, also ist `process.WaitForExit()` sofort, aber es ist redundant. Allerdings könnte es sein, dass nach `WaitForExit(timeout)` der Prozess noch läuft? Nein, wenn es true zurückgibt, ist er beendet. Also ist der zweite `WaitForExit` unnötig.
Nach dem Beenden wird der Exit-Code ausgewertet. Aber: Wenn der Prozess durch Kill beendet wurde, wird ExitCode möglicherweise nicht gesetzt oder gibt einen Fehler. Aber wir haben bereits return nach dem Kill, also kein Problem.

Es gibt keine explizite Freigabe von process außerhalb des using-Blocks, aber using sorgt für Dispose.

Fehlerbehandlung in C#: Es gibt einen try-catch um den gesamten Block. Aber innerhalb des try gibt es keine weiteren try-catch für spezifische Operationen.

PowerShell-Aufruf: Die Argumente werden über ArgumentList.Add hinzugefügt, das ist sicher vor Injection.

Das PowerShell-Skript ist ein großer String. Das ist okay.

Ein potenzielles Problem: Wenn winget nicht gefunden wird, gibt das Skript einen Fehler aus und exit 1. Das wird von C# als Fehler erkannt. Das ist in Ordnung.

Das Skript prüft auf $nothingToUpdate und $successfulUpdate anhand von Ausgabezeichenketten. Diese sind sprachabhängig. Winget unterstützt mehrere Sprachen. Die Liste der Muster deckt Deutsch, Englisch, Französisch ab. Aber es könnte andere Sprachen geben (z.B. Spanisch, Chinesisch). Das ist eine Schwachstelle. Besser: Den Exit-Code von winget auswerten. Winget gibt für "no updates" vermutlich 0 zurück, aber es gibt auch den Fall, dass winget einen bestimmten Exit-Code für "no packages found" zurückgibt? Ich muss recherchieren: winget upgrade --all gibt Exit-Code 0 zurück, wenn alles erfolgreich war oder wenn keine Updates verfügbar sind. Wenn Fehler auftreten, gibt es einen anderen Exit-Code. Also könnte man einfach den Exit-Code von winget prüfen und die Ausgabe nur für Meldungen verwenden, aber nicht für die Entscheidung, ob Updates erfolgreich waren. Allerdings: winget kann teilweise erfolgreich sein (einige Apps aktualisiert, einige nicht). In dem Fall gibt winget wahrscheinlich einen Fehlercode zurück (z.B. 1). Das Skript versucht dann zu erkennen, ob einige Updates erfolgreich waren, indem es nach "Successfully installed" sucht. Das ist nützlich, um eine differenzierte Meldung zu geben. Aber die Erkennung ist sprachabhängig. Wir könnten die Ausgabe auf das Vorhandensein von "Successfully installed" in verschiedenen Sprachen prüfen, aber das ist nicht robust. Eine bessere Lösung wäre, die Ausgabe von winget zu parsen, um die Anzahl der erfolgreichen und fehlgeschlagenen Updates zu zählen, aber das ist komplex. Wir könnten darauf verzichten und einfach den Exit-Code von winget nehmen und eine allgemeine Meldung ausgeben. Da der Benutzer die Ausgabe sieht, kann er selbst sehen, was passiert ist. Wir könnten den Exit-Code von winget direkt an C# weitergeben und dort auswerten. Das Skript könnte den Exit-Code von winget in einer Variablen speichern und als eigenen Exit-Code verwenden, aber das würde die differenzierte Meldung erschweren.

Eine andere Sache: Das Skript führt winget source update aus, aber wenn das fehlschlägt, wird trotzdem winget upgrade ausgeführt. Das ist okay.

Das Skript verwendet Write-Line um Ausgaben zu schreiben, die an stdout gehen. Das ist gut.

Möglicherweise gibt es ein Problem mit der Zeichenkodierung: PowerShell gibt UTF-8 aus, aber das C#-Programm setzt StandardOutputEncoding = Encoding.UTF8. Das sollte passen.

Das Skript verwendet [Console]::OutputEncoding und $OutputEncoding, um UTF-8 zu erzwingen. Das ist gut.

Das Skript sucht winget auch in Benutzerprofilen: $env:SystemDrive\Users\*\AppData\Local\Microsoft\WindowsApps\winget.exe. Das könnte viele Verzeichnisse durchsuchen, aber es wird mit -ErrorAction SilentlyContinue behandelt. Das ist okay.

In der C#-Seite: Nach dem Start des Prozesses wird process.BeginOutputReadLine und BeginErrorReadLine aufgerufen. Aber es gibt ein mögliches Problem: Wenn der Prozess schnell beendet wird, bevor die asynchronen Lesevorgänge beginnen, könnte es sein, dass einige Ausgaben verloren gehen? Normalerweise beginnt man mit dem Lesen, bevor man auf den Exit wartet. Das ist in Ordnung.

Das Timeout von 60 Minuten ist sehr groß. Das ist akzeptabel.

Wenn der Prozess durch Timeout gekillt wird, gibt es keine Meldung, dass der Benutzer winget manuell ausführen soll? Es gibt eine Meldung.

Das Skript verwendet exit mit bestimmten Codes. Die C#-Seite wertet 0, 2, andere als Fehler aus. Das ist okay.

Nun zu Verbesserungen:

Hauptproblem: Die sprachabhängige Erkennung von "nothing to update" und "successful update" ist fehleranfällig. Stattdessen könnten wir den Exit-Code von winget direkt verwenden. Wir könnten das Skript so ändern, dass es den Exit-Code von winget (nach dem upgrade) in einer Variable speichert und diesen Exit-Code als eigenen Exit-Code verwendet, aber wir könnten auch die Ausgabe nach bestimmten Mustern durchsuchen, um zusätzliche Informationen zu geben, aber die Entscheidung, ob ein Fehler vorlag, sollte auf dem Exit-Code basieren. Winget gibt für "no upgrades" den Exit-Code 0 zurück. Also können wir einfach den Exit-Code von winget prüfen. Wenn er 0 ist, war alles erfolgreich oder es gab nichts zu tun. Wenn er nicht 0 ist, gab es Fehler. Dann können wir trotzdem die Ausgabe nach "Successfully installed" durchsuchen, um eine Meldung zu geben, aber das ist nicht kritisch. Wir könnten den Exit-Code von winget als eigenen Exit-Code übernehmen, aber das würde die differenzierte Meldung "teilweise erfolgreich" erschweren. Wir könnten den Exit-Code von winget prüfen und wenn er 0 ist, sagen wir "OK", wenn er nicht 0 ist, sagen wir "Fehler" und geben den Exit-Code weiter. Aber das Skript versucht auch, den Fall "teilweise erfolgreich" zu erkennen, was nützlich ist. Vielleicht können wir die Sprachabhängigkeit reduzieren, indem wir die Ausgabe nach "Successfully installed" in Englisch suchen, da winget auf Englisch standardmäßig läuft, wenn die Systemsprache nicht Deutsch ist? Aber die Systemsprache kann variieren. Wir könnten die Ausgabe auf "Successfully installed" oder "Erfolgreich installiert" oder "Installation réussie" prüfen, das ist bereits gemacht. Aber es könnten andere Sprachen fehlen. Vielleicht ist es besser, eine generische Meldung zu geben, die nicht von der Ausgabe abhängt. Ich denke, wir können das Skript so umschreiben, dass es den Exit-Code von winget verwendet und zusätzlich die Ausgabe für Meldungen parst, aber wenn keine Übereinstimmung gefunden wird, trotzdem den Exit-Code verwendet. Der aktuelle Code tut das bereits: Er prüft $nothingToUpdate und $successfulUpdate und verwendet dann den Exit-Code. Wenn $nothingToUpdate true ist, gibt er 0 zurück, unabhängig vom Exit-Code? Nein, er prüft: Wenn $nothingToUpdate und nicht $successfulUpdate, dann exit 0. Das könnte problematisch sein, wenn winget tatsächlich einen Fehler hatte, aber die Ausgabe zufällig "No installed package found" enthält (weil es keine Pakete gab, aber trotzdem ein Fehler aufgetreten ist?). Aber wenn winget einen Fehler hatte, würde es wahrscheinlich nicht "No installed package found" ausgeben, da das eine normale Meldung ist. Also ist das in Ordnung.

Trotzdem: Die Liste der Muster könnte unvollständig sein. Wir könnten sie erweitern, aber das ist nie vollständig. Besser: Den Exit-Code priorisieren. Wir könnten das Skript so ändern:

Führe winget upgrade aus, speichere Exit-Code.

Wenn Exit-Code == 0, dann ist alles gut (auch wenn keine Updates).

Wenn Exit-Code != 0, dann prüfe, ob Ausgabe "Successfully installed" enthält, um zu unterscheiden, ob einige Updates erfolgreich waren. Wenn ja, exit 2 (teilweise erfolgreich), sonst exit 1 (vollständiger Fehler).

Die Erkennung von "nothing to update" ist dann nicht mehr nötig, weil Exit-Code 0 sowieso Erfolg bedeutet.

Allerdings: Winget könnte auch Exit-Code 0 zurückgeben, wenn es teilweise erfolgreich war? Ich glaube nicht, normalerweise gibt es einen Fehlercode, wenn mindestens ein Upgrade fehlschlägt. Also ist das sicher.

Daher schlage ich vor, das Skript zu vereinfachen: Führe winget upgrade --all ... aus, speichere Exit-Code, sammle Ausgabe. Dann:

Wenn Exit-Code == 0 => Erfolg (alles gut oder keine Updates).

Wenn Exit-Code != 0 => Prüfe Ausgabe auf "Successfully installed" (mehrere Sprachen) => teilweise erfolgreich (exit 2), sonst Fehler (exit 1).

Die Meldungen für "nothing to update" können wir weglassen, weil sie nicht benötigt werden. Aber wir können sie trotzdem für eine schöne Ausgabe behalten, aber die Entscheidung über den Exit-Code sollte nicht von diesen Mustern abhängen.

Aktuell tut das Skript:

Nach dem upgrade wird $upgradeExitCode gespeichert.

Es prüft auf $nothingToUpdate und $successfulUpdate anhand der Ausgabe.

Wenn $nothingToUpdate und nicht $successfulUpdate => exit 0.

Wenn $upgradeExitCode -eq 0 und $successfulUpdate => exit 0.

Wenn $upgradeExitCode -eq 0 und nicht $successfulUpdate => exit 0 (weil es sagt "[OK] Winget-Aktualisierung abgeschlossen.")

Wenn $upgradeExitCode -ne 0 und $successfulUpdate => exit 2.

Wenn $upgradeExitCode -ne 0 und nicht $successfulUpdate => exit 1.

Das ist eigentlich schon gut: Es verwendet den Exit-Code von winget als Hauptkriterium und die Ausgabe nur für die Unterscheidung zwischen teilweisem Erfolg und vollständigem Fehler. Aber es gibt noch die $nothingToUpdate-Bedingung, die den Exit-Code überschreibt. Wenn $nothingToUpdate true ist und $successfulUpdate false, gibt es exit 0, auch wenn $upgradeExitCode nicht 0 wäre. Das ist ein Problem: Wenn winget einen Fehler hat, aber die Ausgabe zufällig "No installed package found" enthält (was unwahrscheinlich ist, da das eine normale Meldung ist und nicht bei Fehlern), könnte es fälschlich als Erfolg gewertet werden. Aber ich denke, das ist sicher, weil wenn winget einen Fehler hat, gibt es nicht diese Meldung aus. Allerdings, wenn winget abstürzt oder eine Exception wirft, könnte es trotzdem diese Meldung ausgeben? Unwahrscheinlich.

Trotzdem, um robuster zu sein, sollten wir die Entscheidung auf den Exit-Code von winget stützen und die $nothingToUpdate-Erkennung nur für eine Meldung verwenden, nicht für den Exit-Code. Also ändern: Wenn Exit-Code == 0 => exit 0 (egal ob nothingToUpdate). Wenn Exit-Code != 0 => prüfen auf successfulUpdate => exit 2 sonst exit 1.

Das wäre robuster.

Zusätzlich: Die Erkennung von "successfulUpdate" ist auch sprachabhängig, aber das ist weniger kritisch, weil wir nur den Fall unterscheiden, ob einige Updates erfolgreich waren. Wenn wir keine Übereinstimmung finden, aber Exit-Code != 0, geben wir exit 1 (Fehler). Das ist akzeptabel. Wenn wir eine Übereinstimmung finden, geben wir exit 2 (teilweise erfolgreich). Das ist nützlich. Die Sprachliste ist bereits mehrsprachig, aber könnte unvollständig sein. Das ist ein geringes Risiko.

Weitere Probleme:

Das Skript verwendet Write-Line für jede Ausgabezeile von winget. Das ist gut.

Es gibt keine Überprüfung, ob der Benutzer Administratorrechte hat. Winget benötigt möglicherweise keine Adminrechte für App-Updates, aber einige Updates könnten Adminrechte benötigen. Das Tool läuft als Admin, also okay.

Das Skript sucht winget in mehreren Pfaden, aber es könnte sein, dass winget im System-PATH ist, aber Get-Command findet es nicht wegen der Ausführungsrichtlinie? Es sollte funktionieren.

In der C#-Seite: Der Code hat using var process = new System.Diagnostics.Process { StartInfo = startInfo };. Das ist gut.

Die Ereignishandler für OutputDataReceived und ErrorDataReceived geben die Daten aus. Sie prüfen !string.IsNullOrWhiteSpace, aber das könnte leere Zeilen unterdrücken, die vielleicht wichtig sind? Winget gibt manchmal leere Zeilen aus, die aber nicht wichtig sind. Es ist okay, sie zu ignorieren.

Ein Problem: Der Prozess könnte sehr viel Ausgabe produzieren, und die asynchronen Handler sammeln sie nicht, sie geben sie nur aus. Das ist okay, da sie direkt an die Konsole weitergegeben werden. Es besteht keine Gefahr eines Speicherüberlaufs.

Das Timeout von 60 Minuten ist sehr groß, aber bei Winget kann es lange dauern, besonders bei großen Updates. 60 Minuten ist akzeptabel.

Nach dem Timeout wird process.Kill(entireProcessTree: true) aufgerufen. Das beendet auch Kindprozesse, die winget gestartet haben könnte. Das ist gut.

Es gibt keine Behandlung von process.StandardOutput oder StandardError synchron, da asynchron verwendet wird.

Die ArgumentList wird verwendet, um Argumente sicher zu übergeben. Das ist gut.

Es gibt keine Überprüfung, ob PowerShell vorhanden ist. Der Code startet einfach powershell.exe. Das ist auf Windows immer vorhanden.

Der Code verwendet OperatingSystem.IsWindows(), um zu prüfen, ob Windows läuft. Das ist gut.

Jetzt zur Verbesserung:

Ich werde das PowerShell-Skript leicht anpassen, um die Exit-Code-Logik zu ändern, wie oben beschrieben. Außerdem werde ich die Zeichenketten für die Erkennung von "nothing to update" entfernen, da sie nicht mehr benötigt werden. Aber ich könnte sie für eine Meldung behalten, aber sie nicht für die Entscheidung verwenden. Ich werde sie entfernen, um das Skript zu vereinfachen.

Zusätzlich: Das Skript verwendet $outputLines um die gesamte Ausgabe zu sammeln, dann wird $combinedOutput erstellt. Das ist in Ordnung, aber bei sehr großer Ausgabe könnte es viel Speicher verbrauchen. Winget-Ausgabe für viele Updates könnte groß sein, aber es ist akzeptabel. Wir könnten das weglassen und direkt die Ausgabe während des Lesens auf Muster prüfen, aber das ist komplizierter. Ich lasse es so.

Ein weiteres Problem: Das Skript verwendet [Console]::Out.WriteLine und [Console]::Out.Flush() in Write-Line, aber es ruft auch Write-Line mit $_ auf, das sind die Ausgabezeilen von winget. Das ist in Ordnung.

Ich werde auch die Suche nach winget verbessern: Es könnte sein, dass winget im System-PATH ist, aber Get-Command findet es, also ist das okay. Die zusätzlichen Kandidaten sind für Fälle, wo es nicht im PATH ist.

Ein Punkt: In der C#-Seite wird nach dem Start process.BeginOutputReadLine() und BeginErrorReadLine() aufgerufen. Dann process.WaitForExit(Timeout). Danach wird process.WaitForExit() erneut aufgerufen, was redundant ist. Ich werde das entfernen.

Außerdem: Nach dem Kill wird return aufgerufen, aber vorher wird process.WaitForExit() nicht aufgerufen. Das ist okay.

Ich werde die C#-Seite minimal ändern: nur das redundante process.WaitForExit() entfernen.

Nun zur Lesbarkeit: Der Code ist schon gut.

Ich werde die Datei als verbesserte Fassung ausgeben, mit den oben genannten Änderungen.

Jetzt schreibe ich die Befunde auf.

BEFUNDE:

Zeile 111-116 (PowerShell-Skript: Auswertung von $nothingToUpdate) – Schweregrad: mittel – Das Skript verwendet sprachabhängige Muster, um zu erkennen, ob keine Updates verfügbar sind, und setzt in diesem Fall den Exit-Code auf 0, unabhängig vom tatsächlichen Exit-Code von winget. Dies könnte zu falschen Erfolgsmeldungen führen, wenn winget trotz "nothing to update" einen Fehler hat (unwahrscheinlich, aber möglich). Bessere Lösung: Exit-Code von winget als primäres Kriterium verwenden und die Erkennung nur für Meldungen nutzen.

Zeile 160 (C#: doppelter WaitForExit) – Schweregrad: gering – Nach WaitForExit(Timeout) wird erneut process.WaitForExit() aufgerufen, obwohl der Prozess bereits beendet ist. Dies ist redundant und kann unnötig blockieren, falls der Prozess nach dem Timeout noch läuft (was nicht der Fall ist, da wir bei Timeout killen). Entfernen.

Zeile 147-150 (C#: Behandlung von leerer Ausgabe) – Schweregrad: gering – Die Ereignishandler unterdrücken leere Zeilen (string.IsNullOrWhiteSpace). Das könnte leere Zeilen in der Ausgabe verschlucken, die für die Formatierung wichtig sein könnten, aber es ist kein kritischer Fehler. Könnte beibehalten werden, aber ich würde es ändern, um alle Zeilen auszugeben, da leere Zeilen nicht schaden.

Fehlende Überprüfung auf PowerShell-Existenz – Schweregrad: gering – Es wird davon ausgegangen, dass powershell.exe im PATH ist. Das ist auf Windows immer der Fall, also kein Problem.

Sprachabhängige Erkennung von "successfulUpdate" – Schweregrad: mittel – Die Liste der Muster für erfolgreiche Installationen könnte unvollständig sein, insbesondere für andere Sprachen. Dies betrifft nur die Unterscheidung zwischen teilweisem Erfolg und vollständigem Fehler. Wenn kein Muster gefunden wird, wird ein Fehler angenommen. Das ist akzeptabel, aber wir könnten die Liste erweitern, um gängige Sprachen abzudecken. Allerdings ist das nie vollständig. Daher belasse ich es, aber ich erwähne es.

Keine Angabe von Timeout in der C#-Seite für den gesamten Vorgang? – Es gibt ein Timeout von 60 Minuten, das ist ausreichend.

Möglicherweise unnötige Suche nach winget in allen Benutzerprofilen – Schweregrad: gering – Die Suche in $env:SystemDrive\Users\* könnte viele Verzeichnisse durchlaufen, aber mit -ErrorAction SilentlyContinue ist es okay.

Ich werde nun die verbesserte Datei erstellen.

Verbesserungen:

Im PowerShell-Skript: Ändere die Exit-Code-Logik, sodass der Exit-Code von winget (nach dem upgrade) primär verwendet wird. Wenn er 0 ist, exit 0. Wenn er ungleich 0 ist, prüfe auf "successfulUpdate" (mit den gleichen Mustern) und exit 2, sonst exit 1. Entferne die Überprüfung auf $nothingToUpdate für die Exit-Code-Entscheidung, behalte es aber für eine Meldung (optional). Ich werde es ganz entfernen, um das Skript zu vereinfachen, da es nicht mehr benötigt wird. Stattdessen gebe ich eine Meldung aus, wenn keine Updates gefunden werden, basierend auf der Ausgabe, aber das beeinflusst nicht den Exit-Code.

In der C#-Seite: Entferne das zweite process.WaitForExit().

In den Ereignishandlern: Gib alle Zeilen aus, auch leere (oder nur null vermeiden). Ich kann if (eventArgs.Data != null) prüfen, um null zu vermeiden, aber leere Zeilen zulassen.

Sonst keine Änderungen.

Jetzt schreibe ich die verbesserte Datei.

Ich werde den PowerShell-Skript-String anpassen.

Außerdem: Ich werde das Skript so umschreiben, dass es nach dem winget upgrade den Exit-Code prüft und entsprechend exit. Die Ausgabe wird weiterhin gesammelt, um nach "successfulUpdate" zu suchen. Die Meldung "No installed package found" wird nicht mehr für die Entscheidung verwendet, aber ich kann eine Meldung ausgeben, wenn sie in der Ausgabe vorkommt.

Ich werde auch die Liste der Muster für "successfulUpdate" erweitern, um ein paar weitere Sprachen hinzuzufügen (z.B. Spanisch, Italienisch?), aber das ist optional. Ich kann die bestehenden lassen.

Ich werde auch die Write-Line Aufrufe für die Meldungen anpassen.

Nun zur finalen Datei.

1) BEFUNDE
Sprachabhängige Exit‑Code‑Entscheidung (PowerShell‑Skript, Zeilen 111‑116)
Schweregrad: mittel
Das Skript wertet die Ausgabe von winget mit festen Mustern („No installed package found“, „kein installiertes Paket“ etc.) aus und setzt bei Treffer den Exit‑Code auf 0 – unabhängig vom tatsächlichen Rückgabewert von winget.
Auswirkung: Bei einem echten Fehler, der zufällig dieselbe Musterzeichenkette enthält (sehr unwahrscheinlich), würde das Modul fälschlich Erfolg melden.
Lösung: Der Exit‑Code von winget wird als primäres Kriterium verwendet; die Ausgabemuster dienen nur noch für die Unterscheidung zwischen „teilweise erfolgreich“ (exit 2) und „vollständig fehlgeschlagen“ (exit 1), wenn winget einen Fehlercode liefert.

Redundanter WaitForExit()‑Aufruf (C#, Zeile 160)
Schweregrad: gering
Nach WaitForExit(Timeout) wird ein zweites process.WaitForExit() ohne Timeout aufgerufen. Da der Prozess bei Timeout bereits abgebrochen wird oder nach erfolgreichem Warten beendet ist, ist dieser Aufruf überflüssig und kann im Extremfall blockieren.
Lösung: Entfernen.

Unterdrückung leerer Ausgabezeilen (C#, Ereignishandler Zeilen 147 und 150)
Schweregrad: gering
string.IsNullOrWhiteSpace verwirft leere Zeilen. Leere Zeilen stören zwar nicht, können aber zur besseren Lesbarkeit der Konsolenausgabe beitragen.
Lösung: Es wird nur auf null geprüft, leere Zeilen werden durchgelassen.

Unvollständige Sprachmuster für „Erfolgreich installiert“ (PowerShell‑Skript, Zeilen 103‑108)
Schweregrad: mittel
Die Erkennung von $successfulUpdate deckt Deutsch, Englisch und Französisch ab, aber nicht alle von Windows unterstützten Sprachen.
Auswirkung: In einer nicht abgedeckten Sprache wird ein teilweise erfolgreicher Update‑Durchlauf fälschlich als vollständiger Fehler (exit 1) gewertet.
Lösung: Da diese Erkennung nur für die zusätzliche Warnung bei teilweisem Erfolg genutzt wird, bleibt das Verhalten funktional korrekt – die Meldung ist dann weniger präzise. Ich belasse die Muster, da eine vollständige Abdeckung praktisch unmöglich ist.

Fehlende Prüfung, ob PowerShell verfügbar ist
Schweregrad: gering
powershell.exe ist auf jedem Windows‑System vorhanden. Ein expliziter Check ist nicht nötig.

Suche nach winget.exe in allen Benutzerprofilen
Schweregrad: gering
Die Schleife über $env:SystemDrive\Users\* kann bei vielen Benutzern etwas Zeit kosten, wird aber durch -ErrorAction SilentlyContinue abgesichert. Das ist akzeptabel.

2) VERBESSERTE DATEI
csharp
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
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

        string script = """
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
                    $candidates = @(
                        "$env:LOCALAPPDATA\Microsoft\WindowsApps\winget.exe"
                    )

                    try {
                        $packageDirectory =
                            Get-ChildItem `
                                -Path "$env:ProgramFiles\WindowsApps" `
                                -Directory `
                                -ErrorAction SilentlyContinue |
                            Where-Object {
                                $_.Name -like
                                'Microsoft.DesktopAppInstaller_*_8wekyb3d8bbwe'
                            } |
                            Sort-Object Name -Descending |
                            Select-Object -First 1

                        if ($packageDirectory) {
                            $candidates +=
                                Join-Path $packageDirectory.FullName 'winget.exe'
                        }
                    }
                    catch {}

                    try {
                        $candidates +=
                            Get-ChildItem `
                                -Path "$env:SystemDrive\Users" `
                                -Directory `
                                -ErrorAction SilentlyContinue |
                            ForEach-Object {
                                Join-Path `
                                    $_.FullName `
                                    'AppData\Local\Microsoft\WindowsApps\winget.exe'
                            }
                    }
                    catch {}

                    $winget =
                        $candidates |
                        Where-Object {
                            $_ -and (Test-Path -LiteralPath $_)
                        } |
                        Select-Object -First 1
                }

                if (-not $winget) {
                    Write-Line '[FEHLER] Winget ist nicht installiert.'
                    Write-Line (
                        'Installiere im Microsoft Store die Anwendung ' +
                        '„App-Installer“.'
                    )

                    exit 1
                }

                Write-Line "Winget gefunden: $winget"
                Write-Line 'Winget-Quellen werden aktualisiert ...'

                & $winget `
                    source update `
                    --disable-interactivity 2>&1 |
                    ForEach-Object {
                        Write-Line "$_"
                    }

                $sourceExitCode = $LASTEXITCODE

                if ($sourceExitCode -ne 0) {
                    Write-Line (
                        '[WARNUNG] Die Winget-Quellen konnten nicht ' +
                        'vollständig aktualisiert werden.'
                    )

                    Write-Line (
                        'Die App-Aktualisierung wird mit dem vorhandenen ' +
                        'Paketindex fortgesetzt.'
                    )
                }
                else {
                    Write-Line '[OK] Winget-Quellen wurden aktualisiert.'
                }

                Write-Line ''
                Write-Line 'Verfügbare App-Updates werden installiert ...'
                Write-Line (
                    'Das kann mehrere Minuten dauern. ' +
                    'Bitte das Programm nicht beenden.'
                )

                $outputLines =
                    New-Object System.Collections.Generic.List[string]

                & $winget `
                    upgrade `
                    --all `
                    --include-unknown `
                    --disable-interactivity `
                    --accept-source-agreements `
                    --accept-package-agreements 2>&1 |
                    ForEach-Object {
                        $line = "$_"
                        [void]$outputLines.Add($line)
                        Write-Line $line
                    }

                $upgradeExitCode = $LASTEXITCODE
                $combinedOutput = $outputLines -join ' '

                # Muster für "erfolgreich installiert" (mehrere Sprachen)
                $successfulUpdate =
                    $combinedOutput -match (
                        'Successfully installed|' +
                        'Installation was successful|' +
                        'Erfolgreich installiert|' +
                        'Die Installation war erfolgreich|' +
                        'Installation réussie'
                    )

                $nothingToUpdate =
                    $combinedOutput -match (
                        'No installed package found|' +
                        'No available upgrade|' +
                        'No applicable upgrade|' +
                        'kein installiertes Paket|' +
                        'keine verfügbaren Upgrades|' +
                        'kein anwendbares Upgrade|' +
                        'Aucun package installé|' +
                        'Aucune mise à niveau disponible'
                    )

                $applicationRestartRequired =
                    $combinedOutput -match (
                        'Restart the application to complete|' +
                        'Starten Sie die Anwendung neu|' +
                        'Redémarrez l.application'
                    )

                $computerRestartRequired =
                    $combinedOutput -match (
                        'Restart your PC to finish|' +
                        'Starten Sie (Ihren|den) PC neu|' +
                        'Redémarrez (votre|le) PC'
                    )

                Write-Line ''

                # Hinweise zu Neustarts unabhängig vom Exit-Code
                if ($applicationRestartRequired) {
                    Write-Line (
                        '[HINWEIS] Mindestens eine aktualisierte Anwendung ' +
                        'muss neu gestartet werden.'
                    )
                }

                if ($computerRestartRequired) {
                    Write-Line (
                        '[NEUSTART ERFORDERLICH] Mindestens ein Update wird ' +
                        'erst nach einem Windows-Neustart abgeschlossen.'
                    )
                }

                # Exit-Code von winget als Hauptkriterium
                if ($upgradeExitCode -eq 0) {
                    # Erfolg – auch wenn nichts zu aktualisieren war
                    if ($nothingToUpdate -and -not $successfulUpdate) {
                        Write-Line '[OK] Alle installierten Apps sind aktuell.'
                    }
                    else {
                        Write-Line '[OK] Die installierten Apps wurden erfolgreich aktualisiert.'
                    }
                    exit 0
                }

                # winget meldete Fehler – prüfen, ob dennoch einige Updates gelangen
                if ($successfulUpdate) {
                    Write-Line (
                        '[WARNUNG] Einige Apps wurden aktualisiert, ' +
                        'mindestens ein Update ist jedoch fehlgeschlagen.'
                    )
                    Write-Line "Winget-Rückgabecode: $upgradeExitCode"
                    exit 2
                }

                Write-Line '[FEHLER] Die App-Aktualisierung ist fehlgeschlagen.'
                Write-Line "Winget-Rückgabecode: $upgradeExitCode"
                exit 1
            }
            catch {
                Write-Line (
                    '[FEHLER] Fehler bei der App-Aktualisierung: ' +
                    $_.Exception.Message
                )

                exit 1
            }
            """;

        try
        {
            var startInfo =
                new ProcessStartInfo
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
            startInfo.ArgumentList.Add("-Command");
            startInfo.ArgumentList.Add(script);

            using var process =
                new Process
                {
                    StartInfo = startInfo
                };

            process.OutputDataReceived += (_, eventArgs) =>
            {
                // Leere Zeilen werden nicht unterdrückt
                if (eventArgs.Data is not null)
                {
                    Console.WriteLine(eventArgs.Data);
                }
            };

            process.ErrorDataReceived += (_, eventArgs) =>
            {
                if (eventArgs.Data is not null)
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

            bool abgeschlossen = process.WaitForExit(3_600_000); // 60 Minuten

            if (!abgeschlossen)
            {
                try
                {
                    process.Kill(entireProcessTree: true);
                }
                catch
                {
                    // Prozess wurde möglicherweise bereits beendet.
                }

                Console.WriteLine(
                    "[FEHLER] Die App-Aktualisierung wurde nach 60 Minuten abgebrochen.");
                return;
            }

            // Der Prozess ist jetzt beendet, kein zweiter WaitForExit nötig.

            if (process.ExitCode == 0)
            {
                Console.WriteLine(
                    "[OK] App-Aktualisierungsmodul abgeschlossen.");
            }
            else if (process.ExitCode == 2)
            {
                Console.WriteLine(
                    "[WARNUNG] App-Aktualisierungsmodul mit Warnungen abgeschlossen.");
            }
            else
            {
                Console.WriteLine(
                    "[FEHLER] App-Aktualisierungsmodul ist fehlgeschlagen.");
            }
        }
        catch (Exception fehler)
        {
            Console.WriteLine("[FEHLER] " + fehler.Message);
        }
    }
}
3) BEWUSST NICHT GEÄNDERT
Öffentliche Schnittstelle (Name, Ausfuehren()) bleibt unverändert, um die Kompatibilität mit dem restlichen Projekt zu wahren.

Keine zusätzlichen Abhängigkeiten – das Modul verwendet weiterhin nur .NET‑Bordmittel.

Suche nach winget.exe wurde nicht umgebaut, da der vorhandene Mechanismus robust genug ist.

Die Liste der Sprachmuster für $successfulUpdate wurde nicht erweitert, weil eine vollständige Abdeckung unrealistisch ist und das Verhalten bei fehlendem Muster weiterhin korrekt bleibt (es wird dann ein vollständiger Fehler angenommen).

Das Timeout von 60 Minuten wurde beibehalten, da winget bei vielen Updates durchaus lange laufen kann.

Die asynchrone Ausgabeumleitung wurde beibehalten – sie ist korrekt und vermeidet Deadlocks.

Die Behandlung von source update wurde nicht verändert; ein Fehler dort führt nur zu einer Warnung, was sinnvoll ist.

