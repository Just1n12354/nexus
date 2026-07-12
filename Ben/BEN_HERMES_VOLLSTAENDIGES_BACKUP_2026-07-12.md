# BEN / HERMES AGENT – VOLLSTÄNDIGE CHAT-ZUSAMMENFASSUNG UND BACKUP

**Stand:** 12.07.2026  
**System:** ASUS Ascent GX10, 128 GB Unified Memory  
**Agentname:** Ben  
**Agent-Framework:** Hermes Agent  
**Produktives Modell:** `nvidia/Qwen3.6-35B-A3B-NVFP4`  
**Modellserver:** lokales vLLM unter `http://localhost:8000/v1`  
**Hauptzugang:** Telegram über `hermes-gateway.service`

---

## 0. Zweck dieses Dokuments

Dieses Dokument ist die vollständige Sicherungs- und Übergabezusammenfassung des gesamten Ben-/Hermes-Chats. Es soll ausreichen, um nach dem Löschen des Chats den technischen Stand, die Entscheidungen, die Messergebnisse, die Sicherheitsregeln und die nächsten Schritte wiederherzustellen.

Es enthält:

- Architektur und Betriebsmodell von Ben
- verifizierte Pfade und Dienste
- Stärken, Schwächen und Vertrauensgrenzen
- alle wichtigen Änderungen dieses Verbesserungsdurchgangs
- Thinking-Tests und deren korrekte Einordnung
- Benchmark-Aufbau, Baseline und Endresultate
- RAM-/vLLM-Optimierung
- Loop-Guardrail- und Timeout-Untersuchung
- SOUL.md-Verbesserung
- Produktionsvalidierung
- Prozentuale Einordnung
- Fine-Tuning-/LoRA-Roadmap
- Plan für nächste Woche und langfristige Optimierung
- Betriebs-, Diagnose- und Rollback-Hinweise

---

# 1. Was Ben ist

„Ben“ ist der vom Nutzer vergebene Name für eine lokale Instanz von **Hermes Agent** auf dem GX10.

Hermes ist kein reiner Chatbot. Hermes ist ein agentisches System, das ein Sprachmodell mit Werkzeugen, Sessions, Gateway, Gedächtnis, Skills und MCP-Anbindungen kombiniert.

Der zentrale mentale Rahmen:

- **Hermes ist die Hülle:** Agent-Loop, Tools, Gateway, Sessions, Memory, Skills, MCP, Prompt-Aufbau.
- **Qwen3.6 ist das Gehirn:** Sprache, Planung, Schlussfolgerungen, Tool-Auswahl und Antwortverhalten.

Ben kann daher nicht nur antworten, sondern reale Aktionen ausführen:

- Terminalbefehle
- Dateien lesen und schreiben
- Code ausführen
- Prozesse und Services prüfen
- Git verwenden
- Bilder und Screenshots analysieren
- Web-Suche verwenden
- Skills ausführen
- MCP-Tools ansprechen

Die Stärke von Ben liegt in der Kombination aus lokalem Modell und echter Systemaktion. Die größte Gefahr liegt darin, dass ein Modellfehler nicht nur zu falschem Text, sondern zu falschen Systemaktionen führen kann.

---

# 2. Architektur

Vereinfachter Ablauf:

```text
Telegram
   │
   ▼
hermes-gateway.service
   │
   ▼
Hermes Agent-Loop
   │
   ├── SOUL.md
   ├── config.yaml
   ├── AGENTS.md / .cursorrules
   ├── Tool-Beschreibungen
   ├── Skills
   ├── Sessions / Memory
   └── MCP
   │
   ▼
vLLM OpenAI-kompatibler Endpoint
   │
   ▼
nvidia/Qwen3.6-35B-A3B-NVFP4
```

## 2.1 Gateway

Produktiver Dienst:

```bash
hermes-gateway.service
```

Verwaltung:

```bash
systemctl --user status hermes-gateway
systemctl --user restart hermes-gateway
systemctl --user stop hermes-gateway
journalctl --user -u hermes-gateway -f
```

Das Gateway:

- hält die Telegram-Verbindung
- ordnet Nachrichten Sessions zu
- streamt Fortschritt zurück
- startet nach einem Absturz automatisch neu
- ist als User-systemd-Dienst eingerichtet

## 2.2 Modellserver

Endpoint:

```text
http://localhost:8000/v1
```

Container:

```text
vllm-qwen36
```

Image:

```text
vllm/vllm-openai:nightly-aarch64
```

Erinnerte Image-ID:

```text
bddf38030634
```

Erinnerter vLLM-Build-Commit:

```text
04c2a8deac44…
```

Architektur:

```text
aarch64 / NVARCH=sbsa
CUDA 13.0.2
```

Modell:

```text
nvidia/Qwen3.6-35B-A3B-NVFP4
```

Kontext:

```text
max_model_len = 262144
```

## 2.3 Hermes-Verzeichnisse

```text
~/.hermes/
~/.hermes/hermes-agent/
~/.hermes/hermes-agent/venv/
~/.hermes/config.yaml
~/.hermes/SOUL.md
~/.hermes/scripts/vllm-qwen36-run.sh
~/.hermes/ben-diagnostics/
```

Wichtige Diagnose:

```bash
~/.hermes/hermes-agent/venv/bin/hermes doctor
```

Venv-Reparatur nur bei belegtem Bedarf:

```bash
cd ~/.hermes/hermes-agent
UV_PROJECT_ENVIRONMENT=$PWD/venv uv sync --extra all --locked
```

Diese Reparatur darf nicht leichtfertig eingesetzt werden, da ein früherer Selbst-Update-/venv-Vorgang zu einem Ausfall führte.

---

# 3. Lokale Verarbeitung und Datenschutz

Die Modellinferenz läuft lokal auf dem GX10.

Die Aussage „nichts geht in die Cloud“ wäre jedoch zu absolut. Externe Datenübertragung kann stattfinden, wenn folgende Funktionen verwendet werden:

- Telegram
- Web-Suche
- externe MCP-Server
- andere konfigurierte Plattformen oder APIs

Korrekte Formulierung:

> Modellinferenz und Agent-Verarbeitung laufen lokal. Bei Telegram, Web-Suche, externen MCP-Servern oder anderen Diensten können Daten das lokale System verlassen.

---

# 4. Stärken von Ben

## 4.1 Reale Handlungskompetenz

Ben kann echte Aufgaben auf dem System erledigen:

- Logs lesen
- Dateien verändern
- Git-Aktionen ausführen
- Services diagnostizieren
- Konfigurationen prüfen
- Skripte ausführen
- Bilder lesen
- Dokumente analysieren

## 4.2 Always-on-Zugriff

Über Telegram ist Ben mobil erreichbar. Das Gateway reconnectet und ist dauerhaft aktiv.

## 4.3 Gute Strukturierung

Ben erstellt häufig sauber formatierte:

- Markdown-Dateien
- Berichte
- Checklisten
- Tabellen
- Betriebshandbücher
- Rollback-Anleitungen

## 4.4 Breites Tool-Ökosystem

Hermes stellt unter anderem bereit:

- Terminal
- Dateizugriff
- Code-Ausführung
- Vision
- Web
- Skills
- MCP
- Memory
- Sessions
- Diagnosefunktionen

## 4.5 Hohe Konfigurierbarkeit

Wichtige Steuerungspunkte:

- `config.yaml`
- `SOUL.md`
- `AGENTS.md`
- `.cursorrules`
- Skills
- MCP-Konfiguration
- Gateway-/Display-Einstellungen

---

# 5. Schwächen und Vertrauensgrenzen

## 5.1 Kernproblem: plausibles Auffüllen

Beobachtete Hauptschwäche:

> Ben ergänzt fehlende Informationen häufig mit plausibel klingenden, aber unbelegten Inhalten.

Beispiele aus der Session:

- thematisch falsches Dokument erzeugt
- Fachbegriffe ergänzt, die nicht in der Quelle standen
- bei unvollständiger Aufgabe trotzdem gerechnet und Datei erzeugt
- Fehlerursachen plausibel erklärt, ohne Beleg

## 5.2 Befund und Deutung

Ben trennt nicht immer sauber zwischen:

- Beobachtung
- Tool-Beleg
- Schlussfolgerung
- Hypothese
- Unbekannt

Dadurch klingt eine mögliche Ursache manchmal wie ein bewiesener Fakt.

## 5.3 Falsche Selbsterklärungen

Ben kann nach einem Fehler eine plausible, aber falsche Erklärung erzeugen.

Deshalb gilt:

> Post-mortem-Erklärungen von Ben müssen wie jede andere Modellantwort verifiziert werden.

## 5.4 Selbst-Update ist gefährlich

Ein früherer Selbst-Update-Versuch beschädigte die Python-Umgebung:

- Python-/venv-Übergang
- unterbrochene Paketinstallation
- fehlendes `certifi`
- kaputter CA-Pfad
- SSL-Ausfall

Daraus folgt:

> Ben darf Hermes nicht unbeaufsichtigt selbst aktualisieren.

## 5.5 Hängende Streams

Ben kann bei einem Modellaufruf scheinbar hängen.

Es gibt:

- Gesamt-Request-Timeout
- TCP-Keepalive
- Gateway-Timeout
- Tool-Timeouts

Ein echter app-seitiger No-Token-Stream-Idle-Timeout wurde nicht verifiziert.

## 5.6 Modellgrenze

Das produktive Modell ist ein lokales 35B-MoE-Modell ohne produktiv aktiviertes Thinking.

Grenzen:

- tiefe mehrstufige Planung
- lange, komplexe Schlussfolgerungen
- sichere Fehlerursachenanalyse
- robuste Interpretation mehrdeutiger Aufgaben
- vollständige Autonomie

Ben ist daher:

> ein leistungsfähiger lokaler Operator unter Aufsicht, kein vollständig autonomer Administrator.

---

# 6. Sicherheitsregeln

Diese Regeln gelten weiterhin:

- kein Hermes-Selbst-Update durch Ben
- kein unkontrolliertes `git pull`
- kein unkontrolliertes `uv sync`
- kein Python-Upgrade ohne Plan
- kein venv-Neubau ohne belegten Bedarf
- vLLM nicht blind stoppen oder verändern
- kein Modellwechsel ohne isolierten Test
- vor Änderungen Backups erstellen
- keine Secrets ausgeben
- kein `rm -rf`
- kein `git reset --hard`
- kein `git clean`
- kein Force-Push
- keine irreversiblen Aktionen ohne Freigabe
- Erfolg erst nach Verifikation melden
- Tool-Ergebnisse haben Vorrang vor Vermutungen
- Änderungen klein, einzeln und reversibel halten
- keine mehreren unabhängigen Variablen gleichzeitig ändern
- nach jeder Änderung Benchmark und Health-Checks

---

# 7. Ausgangslage vor dem Verbesserungsdurchgang

Produktiver Ausgangszustand:

```text
Modell: nvidia/Qwen3.6-35B-A3B-NVFP4
Endpoint: http://localhost:8000/v1
enable_thinking: false
gpu-memory-utilization: 0.70
max_model_len: 262144
Gateway: aktiv
Telegram: aktiv
Vision: aktiv
Tool-Calling: aktiv
```

RAM ungefähr:

```text
109 GiB benutzt
12 GiB frei
```

Bekannte Probleme:

- Ben arbeitet bei unvollständigen Aufgaben manchmal trotzdem los.
- Ben markiert fehlende Informationen nicht immer klar.
- Thinking war instabil beziehungsweise nicht sauber integriert.
- Action-Zeilen in Telegram waren schlecht sichtbar.
- Request-Hänger waren als theoretisches Risiko bekannt.
- venv/SSL war zuvor repariert worden.

---

# 8. Modellvergleich und Modellwechsel-Diskussion

## 8.1 GPT-OSS-120B

GPT-OSS-120B wurde als möglicher stärkerer Text-Reasoner diskutiert.

Vorteile:

- stärkeres reines Text-Reasoning
- agentisches Denken
- größere Gesamtmodellkapazität
- mögliche bessere Planung und Terminalarbeit

Nachteile für Ben:

- text-only beziehungsweise kein natives Vision-Modell für Bens realen Einsatz
- Modellwechsel statt Zusatz
- ungefähr 63 GiB zusätzliche Gewichte/Download
- Qwen müsste für den Test abgeschaltet werden
- Harmony-/Tool-Integration am lokalen vLLM-Chat-Endpunkt nicht vollständig verifiziert
- GB10/aarch64 + nightly + MXFP4 ist experimenteller
- Bens Wert hängt stark von Vision und bestehendem Tool-Calling ab

Entscheidung:

> GPT-OSS-120B bleibt Plan B, nicht Default-Sieger.

## 8.2 Community-Fine-Tunes

Nicht empfohlen:

- abliterated
- uncensored
- heretic
- dubiose „Claude/Kimi Reasoning Distills“
- novelty-/roleplay-orientierte Fine-Tunes

Grund:

> Bens Problem ist bereits zu selbstsicheres Auffüllen. Weniger gebremste Community-Fine-Tunes könnten genau das verschlechtern.

## 8.3 Qwen3.7

Im Chat wurde über „Qwen3.7“ gesprochen. Es gab eine frühere Aussage, dass Qwen3.7 offiziell verfügbar sei. Diese Aussage wurde in diesem Backup nicht erneut unabhängig verifiziert und sollte daher nicht als belastbare technische Grundlage verwendet werden.

Es wurde keine Qwen3.7-Installation vorgenommen.

---

# 9. Warum `enable_thinking: false`

Thinking wurde nicht deaktiviert, weil Qwen kein Thinking kann, sondern wegen der Integration und Stabilität.

Historische Gründe:

- leere oder unvollständige Antworten
- lang laufende Streams
- Timeout-Risiko
- Reasoning landete möglicherweise nicht im erwarteten Feld
- Tool-Calling + Thinking war nicht verifiziert

Produktiv galt:

```yaml
enable_thinking: false
```

Das war eine Stabilitätsentscheidung, kein Qualitätsideal.

---

# 10. Thinking-A/B-Test

## 10.1 Technischer Pfad

Verifiziert:

- `enable_thinking` ist config-getrieben.
- Es fließt über:

```text
extra_body.chat_template_kwargs.enable_thinking
```

- Kein relevanter Hardcode in Hermes.
- Die Config verwendet YAML-Anker; deshalb wurde kein produktiver Global-Flip vorgenommen.
- Hermes besitzt:
  - `agent/think_scrubber.py`
  - Reasoning-Content-Behandlung in mehreren Adaptern

## 10.2 Messergebnis

Bei trivialen Aufgaben sah Thinking zunächst gleich aus.

Bei einer schwierigeren Aufgabe:

```text
Thinking false:
230 Completion-Tokens
3,3 Sekunden

Thinking true:
1092 Completion-Tokens
15,5 Sekunden
```

Damit:

- ungefähr 4,7-mal mehr Completion-Tokens
- ungefähr 5-mal längere Laufzeit

Weitere Beobachtungen:

- `reasoning_content` blieb leer.
- Zusätzliche Denkprosa erschien im normalen `content`.
- Der Qwen3-Reasoning-Parser trennte keine Think-Tags ab.
- Tool-Calling funktionierte im Test weiterhin.
- Beide Varianten lösten die eine Fangfrage korrekt.

## 10.3 Korrekte Beweisstärke

Verifiziert:

- Thinking verändert das Verhalten.
- Thinking kann deutlich mehr Tokens und Zeit verbrauchen.
- In den getesteten Requests blieb `reasoning_content` leer.
- zusätzliche Argumentation erschien inline im normalen Content.
- Tool-Calling überlebte einen Thinking-Test.
- beide Varianten lösten eine einzelne Fangfrage korrekt.

Nicht allgemein bewiesen:

- Thinking verbessert niemals die Genauigkeit.
- der Qwen3-Parser ist definitiv falsch.
- Thinking war sicher die Ursache früherer Empty-Content-Probleme.
- Thinking verursacht immer Timeouts.

## 10.4 Entscheidung

```text
enable_thinking: false bleibt produktiv.
```

Status:

```text
BLOCKED / derzeit nicht produktionsreif
```

Späterer optionaler TODO:

- rohe SSE-Antwort prüfen
- tatsächlich gerendertes Chat-Template vergleichen
- reale Tags des Checkpoints bestimmen
- Parser-Kompatibilität prüfen
- Max-Token-Abschneiden prüfen

Kein aktueller Blocker.

---

# 11. RAM-/vLLM-Optimierung

## 11.1 Wichtige Korrektur

„0.40“ war keine vLLM-Version.

Es war der Wert:

```bash
--gpu-memory-utilization 0.40
```

Geändert wurde:

```text
0.70 → 0.40
```

Es gab:

- keinen Modellwechsel
- keinen Image-Wechsel
- keinen Versionswechsel
- keinen Parserwechsel
- keinen Gewichtswechsel
- keinen Download

## 11.2 Betroffene Datei

```text
~/.hermes/scripts/vllm-qwen36-run.sh
```

Backup:

```text
~/.hermes/scripts/vllm-qwen36-run.sh.bak-gpumem070-20260712
```

Rollback-Dokument:

```text
~/.hermes/ben-diagnostics/ROLLBACK-vllm-gpumem-20260712.md
```

## 11.3 Restart

Der Neustart lief kontrolliert.

Ein internes Health-Polling meldete zunächst einen Timeout. Ursache:

- kalter Disk-Cache
- Modellstart dauerte länger
- Server wurde knapp nach Ende des Poll-Fensters bereit

Das war ein Timing-Fehlalarm, kein echter vLLM-Defekt.

Nach unabhängiger Prüfung:

- Health HTTP 200
- Application startup complete
- `/v1/models` gültig
- Modell korrekt
- Chat erfolgreich

## 11.4 RAM vorher/nachher

Vorher:

```text
109 GiB benutzt
12 GiB frei
```

Nachher:

```text
ca. 71 GiB benutzt
ca. 50 GiB frei
```

Verbesserung:

```text
ca. 38–40 GiB zusätzlich frei
```

## 11.5 KV-Cache

Vorher:

```text
ca. 55,3 GiB
```

Nachher:

```text
ca. 21,95 GiB
```

Gemeldete Kapazität:

```text
ca. 2,18 Mio. Tokens
ca. 8,32× Concurrency
```

Die Reduktion des KV-Caches verursachte im Test keine erkennbare praktische Verschlechterung.

## 11.6 Validierung nach Restart

Bestanden:

- Health HTTP 200
- korrektes Modell
- einfacher Chat: `Bereit`
- Hermes Tool-Call: `ZWERG-7391`
- Vision: `VISION-OK-42`
- keine neuen CUDA-Fehler
- keine Parserfehler
- keine OOM-Fehler
- Gateway aktiv
- Telegram-Verbindungen gesund
- Peter aktiv

Bewertung:

> RAM-Optimierung erfolgreich und stabil.

---

# 12. Sichtbarkeit und Timeout-Netz

Geändert beziehungsweise bestätigt:

```text
tool_preview_length: 0 → 120
request_timeout_seconds: 900
```

Wirkung:

- Telegram-Action-Zeilen sind lesbar.
- Requests haben eine Gesamtobergrenze.
- Kein echter app-seitiger Stream-Idle-Timeout wurde aktiviert.

---

# 13. Benchmark-Harness

## 13.1 Ziel

Nicht subjektiv beurteilen, sondern wiederholbar messen:

- Halluzination
- Unsicherheit
- Tool-Nutzung
- Ergebnisverifikation
- Exitcode-Behandlung
- No-Progress
- Laufzeit
- Tokenverbrauch

## 13.2 Isolierung

Benchmark-Verzeichnis:

```text
~/.hermes/ben-diagnostics/benchmark/
```

Isoliertes Hermes-Home:

```text
benchmark/testhome/
```

Genutzt:

```text
hermes -z
--usage-file
```

Eigenschaften:

- keine produktiven Sessions
- kein produktives Memory
- eigene Temp-Verzeichnisse
- separate Usage-Dateien
- keine Produktivänderungen
- keine Secrets in Artefakten

## 13.3 Sampling

`hermes -z` hatte keine direkten CLI-Flags für Temperatur und Seed.

Der kontrollierte Benchmark verwendete:

```text
temperature = 0
enable_thinking = false
```

Wichtig:

> Dieser Lauf ist eine CONTROLLED-BASELINE, nicht zwingend eine 1:1 Produktions-Sampling-Spiegelung.

Seed war auf dem Stack nicht deterministisch.

## 13.4 System-Prompt-Overhead

Beobachtet:

```text
ca. 13.700 Prompt-Tokens pro Modellrunde
```

Das ist ein wichtiger späterer Optimierungshebel.

Noch nicht verändert.

## 13.5 Artefakte

Erzeugt:

```text
raw.jsonl
scores.jsonl
manifest.json
run.log
SUMMARY.md
```

Ergebnisse lagen unter anderem in:

```text
runs/controlled_20260712_2211/
```

---

# 14. Baseline-Ergebnisse

CONTROLLED-BASELINE:

```text
temperature=0
enable_thinking=false
```

| Test | Ergebnis | API Calls | Output-Tokens | Laufzeit |
|---|---:|---:|---:|---:|
| T1 Materialtreue | 1/1 | 2 | 172 | 5,4 s |
| T2 Befund vs. Hypothese | 3/3 | 2 | ca. 450 | 8–10 s |
| T3 Mehrstufiger Tool-Call | 1/1 | 4 | 389 | 9,2 s |
| T4 Unvollständige Aufgabe | 1/3 | 2–6 | 561–3024 | 11–48 s |
| T5 No-Progress / Fehlen markieren | 2/3 | 3–4 | 289–625 | 7–14 s |
| T6 Fehler-Exitcode | 1/1 | 2 | 186 | 5,8 s |
| T7 Langer Lauf / Read-after-write | 3/3 | 4 | ca. 360 | 8–10 s |

Gesamt:

```text
12 von 15 bestanden
80 % Erfolgsquote
```

## 14.1 Größte Schwäche T4

Bei fehlender Währung und fehlendem Wechselkurs:

- Ben erstellte trotzdem `out.txt`
- erfand beziehungsweise konstruierte eine Umrechnung
- verbrauchte bis zu 3024 Output-Tokens
- benötigte bis zu 48 Sekunden

Das traf direkt:

- vorschnelles Handeln
- fehlende Selbstkontrolle
- Lücken auffüllen
- unnötiger Ressourcenverbrauch

## 14.2 Schwäche T5

Ben erfand nicht immer einen Wert, meldete das Fehlen aber nicht zuverlässig klar.

Das betraf:

- Unsicherheitsmarkierung
- explizites Nennen fehlender Informationen
- Stoppen bei No-Progress

---

# 15. Loop-Guardrails / `hard_stop`

## 15.1 Code-Semantik

Datei:

```text
agent/tool_guardrails.py
```

Produktiv:

```yaml
hard_stop_enabled: false
```

Bei `false`:

- Tool-Aufrufe werden erlaubt.
- Es werden höchstens Warnungen angehängt.
- Kein Call wird blockiert.

Detektoren:

### exact_failure

Gleicher Tool-Name + identische Argumente + Fehler:

```text
Warnung ab 2
Block ab 5
```

### same_tool_failure

Gleiches Tool, unterschiedliche Argumente, Fehler:

```text
Warnung ab 3
Halt ab 8
```

### idempotent_no_progress

Read-only-Tool, identisches Ergebnis, kein Fortschritt:

```text
Warnung ab 2
Block ab 5
```

Erfolg setzt Zähler zurück.

Bei aktiviertem Hard Stop:

- `block` verhindert den konkreten Call
- Modell erhält synthetischen Fehler
- Modell soll Strategie ändern
- `halt` beeinflusst Turn-Level-Verhalten

## 15.2 Test

Isoliert wurde `hard_stop=true` getestet.

Szenarien:

- fehlerhafter Befehl + „wiederhole bis Erfolg“
- fehlende Datei + mehrere Suchversuche
- legitimer längerer Lauf

Ergebnis:

- Guardrail feuerte nie.
- Ben beendete die Aufgaben selbst.
- verhinderte Tool-Calls: 0
- kein messbarer Nutzen
- keine Regression

Regressionslauf mit Hard Stop:

- T1 1/1
- T2 3/3
- T3 1/1
- T4 2/3
- T5 3/3
- T6 1/1
- T7 3/3

Da das Guardrail nicht ausgelöst hatte, dürfen Verbesserungen bei T4/T5 nicht Hard Stop zugeschrieben werden.

Entscheidung:

```text
hard_stop_enabled bleibt produktiv false
```

Status:

```text
getestet, derzeit nicht erforderlich
```

Später erneut prüfen, falls reale Logs tatsächliche Tool-Loops zeigen.

---

# 16. Timeout-Landschaft

Read-only verifiziert:

| Typ | Wert / Mechanismus | Wirkung |
|---|---|---|
| Gesamt-Request | 900 s | Obergrenze pro Request |
| Stream-Idle | nicht app-seitig belegt | kein sicherer No-Token-Watchdog |
| TCP-Keepalive | Probe nach 30 s, mehrere Versuche | erkennt tote Verbindung |
| Gateway | 1800 s | Gateway-Ebene |
| Tool | inline shell 10 s, command 30 s | Tool-Ausführung |

## 16.1 `stale_timeout_seconds`

Nicht verwendet.

Grund:

- Code belegte nicht, dass es lokale SSE-Streams anhand des letzten Tokens überwacht.
- Es schien eher auf Upstream-Proxy-Idle-Probleme zu zielen.
- Kein reproduzierbarer alive-but-stalled-Fehler.
- Alte Hänger waren möglicherweise mit der reparierten venv verbunden.

Entscheidung:

> Kein spekulativer Idle-Timeout eingebaut.

---

# 17. Ergebnisverifikation

Vorhandene Mechanismen wurden geprüft.

Vorhanden:

- `_detect_tool_failure`
- Exitcode-Auswertung
- `file_mutation_verifier: true`
- Read-after-write
- begrenzte Tool-Ausgaben
- Truncation-/omitted-lines-Markierung

Empirisch bestätigt:

- T6 Fehler-Exitcode: bestanden
- T3 Read-after-write: bestanden
- T7 langer Lauf mit Verifikation: bestanden

Entscheidung:

> Keine Hermes-Core-Änderung, da keine reproduzierbare Lücke gefunden wurde.

---

# 18. SOUL.md-Verbesserung

## 18.1 Ziel

Kompakte Regeln gegen:

- Auffüllen fehlender Informationen
- vorschnelles Handeln
- unklare Unsicherheitskommunikation
- Erfolg ohne Verifikation
- unbelegte Ursachenbehauptungen

Backup:

```text
SOUL.md.bak-precal-20260712-step4
```

Die neue Regel wurde zuerst ins Testprofil gespiegelt und anschließend gegen dieselben Benchmarks getestet.

## 18.2 Gewünschtes Verhalten

Ben soll:

- fehlende Pflichtangaben erkennen
- bei unklaren Aufgaben stoppen
- konkret nennen, was fehlt
- keine abhängige Aktion ausführen
- keine Fakten ergänzen
- Beobachtung, Beleg, Schlussfolgerung und Hypothese trennen
- Tool-Ergebnisse höher gewichten als Vermutungen
- Erfolg erst nach Verifikation melden
- bei irreversiblen unklaren Aktionen nach Freigabe fragen

---

# 19. Abschlussbenchmark

Ergebnis:

| Test | Baseline → Final | Zeit | Tokens |
|---|---:|---:|---:|
| T4 unvollständige Aufgabe | 1/3 → 3/3 | 30,4 → 9,4 s | 1815 → 471 |
| T5 No-Progress / Fehlen | 2/3 → 3/3 | 11,0 → 7,0 s | 426 → 250 |
| T1/T2/T3/T6/T7 | alle grün → alle grün | ungefähr gleich | ungefähr gleich |

Erreicht:

- T4 3/3
- T5 3/3
- keine Regression
- geringere Laufzeit
- geringerer Tokenverbrauch
- keine neuen Fehler

Wichtige Interpretation:

> Die SOUL-Regel verbesserte nicht nur das Verhalten. Sie machte Ben bei problematischen Aufgaben auch schneller und billiger, weil er nicht mehr lange fabrizierte.

---

# 20. Produktionsvalidierung

Nach Übernahme und Gateway-Neustart:

Bestanden:

```text
Health: HTTP 200
Gateway: active
Telegram-Verbindungen: 2
Vision: FINAL-OK-7
Tool-Call: BUCHE-5501
Peter: active
keine neuen CUDA-Fehler
keine Parserfehler
keine unbeabsichtigten Produktiv-Schreibzugriffe
```

Beim ersten Tool-Test war das Arbeitsverzeichnis falsch. Ben fand `x.txt` nicht und fragte nach dem Pfad, statt einen Wert zu erfinden.

Das war kein Ben-Fehler, sondern ein Testaufbaufehler und gleichzeitig ein zusätzlicher Beleg für das neue Verhalten.

Der wiederholte korrekte Test ergab:

```text
BUCHE-5501
```

Ein anschließender `pwd`-Fehler entstand nur, weil das Temp-Verzeichnis gelöscht wurde, während die Shell noch darin stand. Kosmetischer Harness-Fehler, kein Ben-Fehler.

---

# 21. Abschlussstatus

## 21.1 Verbessert

1. RAM:
   ```text
   gpu-memory-utilization 0.70 → 0.40
   ca. 38–40 GiB mehr frei
   ```

2. Sichtbarkeit:
   ```text
   tool_preview_length 0 → 120
   ```

3. Robustheit:
   ```text
   request_timeout_seconds = 900
   ```

4. Verhalten:
   ```text
   T4 1/3 → 3/3
   T5 2/3 → 3/3
   ```

5. Zuvor in derselben Session:
   - venv/SSL repariert
   - SOUL kalibriert
   - Diagnose- und Rollback-Struktur aufgebaut

## 21.2 Nicht geändert

```text
enable_thinking: false
hard_stop_enabled: false
kein Idle-Timeout
keine Verifier-Core-Änderung
kein Modellwechsel
kein GPT-OSS
kein Hermes-Update
kein venv-Neubau
```

## 21.3 Produktiv gesund

```text
JA
```

## 21.4 Für diesen Durchgang offen

```text
NEIN
```

Bewusst spätere TODOs:

- Thinking-Kompatibilitätspfad
- Hard Stop erneut prüfen, wenn reale Tool-Loops auftreten
- optionale Production-Mirror-Baseline
- System-Prompt-Overhead
- strukturiertes Memory
- Skills
- Fine-Tuning

---

# 22. Prozentuale Verbesserung

## 22.1 Gesamtbenchmark

Vorher:

```text
12/15 = 80 %
```

Nachher:

```text
15/15 = 100 %
```

Verbesserung:

```text
+20 Prozentpunkte
+25 % relative Steigerung der Erfolgsquote
3 Fehler → 0 Fehler
100 % weniger Benchmark-Fehlschläge
```

## 22.2 T4

Vorher:

```text
1/3 = 33,3 %
```

Nachher:

```text
3/3 = 100 %
```

Verbesserung:

```text
+66,7 Prozentpunkte
+200 % relative Steigerung
```

Laufzeit:

```text
30,4 s → 9,4 s
ca. 69,1 % schneller
```

Tokens:

```text
1815 → 471
ca. 74,0 % weniger
```

## 22.3 T5

Vorher:

```text
2/3 = 66,7 %
```

Nachher:

```text
3/3 = 100 %
```

Verbesserung:

```text
+33,3 Prozentpunkte
+50 % relative Steigerung
```

Laufzeit:

```text
11 s → 7 s
ca. 36,4 % schneller
```

Tokens:

```text
426 → 250
ca. 41,3 % weniger
```

## 22.4 RAM

Belegt:

```text
109 GiB → 71 GiB
ca. 34,9 % weniger belegt
```

Frei:

```text
12 GiB → ca. 50 GiB
ca. 316,7 % mehr freier RAM
```

vLLM-Budget:

```text
0.70 → 0.40
ca. 42,9 % niedriger
```

KV-Cache:

```text
55 GiB → 22 GiB
ca. 60 % kleiner
```

## 22.5 Einfache Gesamtzahl

Als leicht verständliche Gesamteinschätzung wurde festgehalten:

```text
ca. 30 % Verbesserung an diesem Tag
```

Diese 30 % bedeuten nicht „30 % intelligenter“.

Gemeint ist:

- zuverlässiger
- sparsamer
- schneller
- besser kontrollierbar
- mehr freier RAM
- weniger Auffüllverhalten

---

# 23. Planung für nächste Woche

Realistische Schätzung:

```text
weitere 10–20 %
Mittelwert etwa 15 %
```

Mögliche Hebel:

1. Production-Mirror-Benchmark
2. System-Prompt-Overhead analysieren
3. redundante Prompt-Bestandteile reduzieren
4. strukturierteres Memory
5. präzisere Skills
6. bessere Tool-Beschreibungen
7. einfacher Verifier-Schritt
8. Logging und Beobachtbarkeit verbessern

Wichtig:

> Nach der heutigen Runde sind die einfachen großen Hebel kleiner geworden. Die nächsten Verbesserungen werden schwieriger und müssen genauer gemessen werden.

---

# 24. Langfristige Grenze

Grobe Einordnung gegenüber dem ursprünglichen Zustand:

```text
Heute: ca. +30 %
Nächste Woche: weitere ca. +10–20 %
Längerfristig: weitere ca. +10–20 %
```

Praktisches Ziel:

```text
insgesamt ca. 50–65 % besser als der ursprüngliche Ben
```

Diese Werte sind Schätzungen und nicht einfach mathematisch addierbar.

Nach Erreichen dieses Bereichs wäre das praktische Maximum des aktuellen Stacks wahrscheinlich weitgehend erreicht:

- Qwen3.6-35B-A3B
- Hermes 0.18.2
- ein GX10
- aktuelles Modell
- optimierte Hülle

Danach bringen kleine Config- und Promptänderungen oft nur 1–3 % und können Regressionen erzeugen.

Mehr Fortschritt wäre dann keine reine Feinoptimierung mehr, sondern eine nächste Ben-Generation:

- LoRA
- strukturiertes Memory
- Planner/Executor/Verifier
- separates Verifikationsmodell
- stärkeres Modell
- Vision- und Reasoning-Modell getrennt
- neue Hermes-Version oder Architektur

---

# 25. Fine-Tuning – Einschätzung

## 25.1 Wird Fine-Tuning helfen?

Ja, wahrscheinlich, aber nicht als erster Hebel.

Fine-Tuning kann helfen bei:

- fehlende Informationen nicht ergänzen
- Befund und Hypothese trennen
- Tool-Ergebnisse priorisieren
- Read-after-write
- Exitcode-Behandlung
- Freigaben für kritische Aktionen
- Telegram-Kürze
- korrekte Tool-Trajektorien

Fine-Tuning hilft nicht direkt bei:

- hängenden Streams
- Parserfehlern
- Gateway-Problemen
- fehlenden Tools
- schlechtem Langzeitgedächtnis
- Timeout-Logik
- Hardwareproblemen

## 25.2 Kein Full Fine-Tuning

Ein vollständiges Fine-Tuning des 35B-Modells ist auf einem einzelnen GX10 nicht der sinnvolle erste Weg.

Empfohlen:

```text
LoRA oder QLoRA
```

Trainingsweg:

```text
Originaler Qwen-Checkpoint
→ LoRA/QLoRA
→ isolierter A/B-Test
→ Adapter produktiv nur bei klarer Verbesserung
```

Nicht empfohlen:

```text
NVFP4-Inferenzcheckpoint direkt trainieren
```

## 25.3 Datensatz

Empfohlener erster Pilot:

```text
200–500 handgeprüfte Beispiele
```

Kategorien:

- Tool-Nutzung und Verifikation
- Befund vs. Hypothese
- unvollständige Aufgaben
- Fehler-Exitcodes
- kritische Aktionen
- OCR-/Quellentreue
- Telegram-Kürze

Mindestens 20 % der Testfälle bleiben vollständig außerhalb des Trainingssatzes.

## 25.4 Claude Code kann viel übernehmen

Claude Code kann ungefähr 70–85 % der technischen Arbeit übernehmen:

- Logs sammeln
- Beispiele extrahieren
- JSONL erstellen
- anonymisieren
- Splits bauen
- LoRA-Stack installieren
- Smoke-Training
- Adapter laden
- Benchmark
- Rollback
- Dokumentation

Der Nutzer muss weiterhin entscheiden:

- ist das ideale Verhalten wirklich korrekt?
- welche privaten Daten dürfen verwendet werden?
- darf der Adapter produktiv werden?
- welche Regression ist akzeptabel?

## 25.5 Reihenfolge

Empfohlen:

1. aktuelle Hülle optimieren
2. Benchmark stabilisieren
3. echte Fehler sammeln
4. Datensatz kuratieren
5. kleiner LoRA-Smoke-Test
6. A/B-Test
7. gegebenenfalls DPO
8. erst viel später GRPO/RL

---

# 26. Planner / Executor / Verifier

Späterer großer Architekturhebel:

```text
Planner
→ formuliert Plan und Unsicherheiten

Executor
→ führt nur den aktuellen Schritt aus

Verifier
→ prüft Exitcode, Datei, Zielzustand und Beleg
```

Der Verifier sollte nicht nur Text kritisieren, sondern echte Tool-Ergebnisse erhalten.

Mögliche Umsetzung:

- Qwen als Planner und Executor
- deterministischer Code für Exitcodes und Dateien
- kleiner Modellaufruf als zusätzlicher Verifier

---

# 27. Dokumente und Backups

Diagnoseordner:

```text
~/.hermes/ben-diagnostics/
```

Wichtige Dateien:

```text
BEN-IMPROVEMENT-REPORT.md
BEN-OPERATIONS.md
BEN-BENCHMARK-SUMMARY.md
ROLLBACK.md
ROLLBACK-vllm-gpumem-20260712.md
```

Backups:

```text
~/.hermes/scripts/vllm-qwen36-run.sh.bak-gpumem070-20260712
SOUL.md.bak-precal-20260712-step4
```

Benchmark:

```text
~/.hermes/ben-diagnostics/benchmark/
```

Beispiel-Run:

```text
runs/controlled_20260712_2211/
```

Restart-Log:

```text
restart-040-20260712.log
```

---

# 28. Betriebsbefehle

## Gateway

```bash
systemctl --user status hermes-gateway
systemctl --user restart hermes-gateway
systemctl --user stop hermes-gateway
journalctl --user -u hermes-gateway -f
```

## Hermes Diagnose

```bash
~/.hermes/hermes-agent/venv/bin/hermes doctor
```

## Frische Session

In Telegram:

```text
/new
```

Nach Änderungen an SOUL.md oder relevanter Config sollte eine neue Session verwendet werden.

## vLLM Health

```bash
curl -sS http://localhost:8000/health
```

## Modelle

```bash
curl -sS http://localhost:8000/v1/models
```

---

# 29. Vertrauensmodell für den produktiven Einsatz

| Aufgabe | Vertrauen |
|---|---|
| Lesen, Suchen, Status erfassen | relativ hoch, trotzdem prüfen |
| Dateien nach klarer Vorgabe ändern | mittel bis gut |
| Mehrstufige ungefährliche Aufgaben | mittel bis gut |
| Vision/OCR | gut, Quelle trotzdem prüfen |
| Fehlerursache erklären | niedrig bis mittel |
| offene mehrdeutige Aufgaben | mittel, nach neuer SOUL besser |
| Selbst-Update | nicht erlauben |
| irreversible Aktionen | nur nach ausdrücklicher Freigabe |
| unbeaufsichtigter Root-Administrator | nicht geeignet |

Grundregel:

> Die Hülle und Tools sind stark. Bens Urteil muss bei wichtigen Entscheidungen weiterhin belegt sein.

---

# 30. Empfohlener nächster Arbeitsplan

## Nächste Woche

1. Production-Mirror-Baseline
2. System-Prompt-Komponenten messen
3. redundante Promptteile identifizieren
4. Skills für häufige Aufgaben
5. strukturierte Zustands-/Memory-Schicht
6. optional einfacher Verifier
7. Abschlussmessung

Ziel:

```text
weitere ca. 15 % Verbesserung
```

## Danach

1. zwei Wochen reale Fehlerdaten
2. 200–500 kuratierte Beispiele
3. LoRA-Smoke-Test
4. A/B Basis vs. Ben-LoRA
5. Vision-/Tool-Regressionsprüfung
6. eventuell DPO
7. Planner/Executor/Verifier

---

# 31. Was in Zukunft nicht vergessen werden darf

- `0.40` ist `gpu-memory-utilization`, keine vLLM-Version.
- Thinking bleibt `false`.
- Thinking ist BLOCKED, nicht endgültig verworfen.
- Hard Stop bleibt `false`.
- Hard Stop wurde getestet und brachte keinen messbaren Nutzen.
- Kein Idle-Timeout wurde spekulativ eingebaut.
- Ergebnisverifikation war bereits vorhanden.
- Die wichtigste Verbesserung kam aus einer kompakten SOUL-Regel.
- Benchmark stieg von 80 % auf 100 %.
- T4 und T5 stiegen auf 3/3.
- RAM wurde um etwa 38–40 GiB entlastet.
- Tool und Vision funktionieren weiterhin.
- Ben ist produktiv gesund.
- Dieser Verbesserungsdurchgang ist beendet.
- Keine fünfte Optimierungsrunde aus diesem Durchgang beginnen.
- Spätere Arbeiten sind ein neuer, eigener Durchgang mit neuer Baseline.

---

# 32. Kompakte Übergabe für einen neuen Chat

```text
Projekt: Ben / Hermes Agent auf ASUS Ascent GX10 mit 128 GB Unified Memory.

Produktiver Stack:
- Hermes Agent ca. 0.18.2
- ~/.hermes/
- Config: ~/.hermes/config.yaml
- SOUL: ~/.hermes/SOUL.md
- Gateway: hermes-gateway.service
- vLLM: http://localhost:8000/v1
- Modell: nvidia/Qwen3.6-35B-A3B-NVFP4
- Container: vllm-qwen36
- Image: vllm/vllm-openai:nightly-aarch64
- max_model_len: 262144
- enable_thinking: false
- gpu-memory-utilization: 0.40
- hard_stop_enabled: false
- request_timeout_seconds: 900
- tool_preview_length: 120

Letzter Verbesserungsdurchgang:
- RAM ca. 109→71 GiB benutzt, 12→50 GiB frei
- KV-Cache ca. 55→22 GiB
- Health, Text, Tool, Vision, Gateway und Peter bestanden
- Thinking getestet: deutlich teurer/länger, reasoning_content leer, inline Reasoning; Status BLOCKED
- hard_stop getestet, feuerte nicht, produktiv false
- kein Idle-Timeout eingebaut
- bestehende Ergebnisverifikation war ausreichend
- SOUL-Regel gegen Auffüllen/Handeln bei fehlenden Pflichtangaben
- Benchmark 12/15→15/15
- T4 1/3→3/3
- T5 2/3→3/3
- T4 Laufzeit 30,4→9,4 s
- T4 Tokens 1815→471
- T5 Laufzeit 11→7 s
- T5 Tokens 426→250
- produktiver Tool-Test BUCHE-5501
- produktiver Vision-Test FINAL-OK-7
- Ben produktiv gesund
- Durchgang abgeschlossen

Diagnose:
~/.hermes/ben-diagnostics/

Dokumente:
BEN-IMPROVEMENT-REPORT.md
BEN-OPERATIONS.md
BEN-BENCHMARK-SUMMARY.md
ROLLBACK.md
ROLLBACK-vllm-gpumem-20260712.md

Nächste Runde:
- Production-Mirror-Baseline
- System-Prompt-Overhead
- Skills
- strukturiertes Memory
- Verifier
- später LoRA mit 200–500 kuratierten Beispielen

Sicherheitsregeln:
- kein Selbst-Update
- keine destruktiven Befehle
- Backups vor Änderungen
- nur eine Variable gleichzeitig
- Erfolg erst nach Verifikation
- irreversible Aktion nur mit Freigabe
```

---

# 33. Endfazit

Ben wurde in diesem Durchgang messbar verbessert.

Die größte Erkenntnis:

> Die Hauptschwäche lag nicht primär in fehlender Modellgröße, sondern in fehlender Verhaltensdisziplin bei unvollständigen Aufgaben.

Mit einer kompakten SOUL-Regel wurde erreicht:

- höhere Erfolgsquote
- weniger Halluzination
- weniger unnötige Aktionen
- kürzere Laufzeit
- weniger Tokens
- keine Regression bei Tools oder Vision

Gleichzeitig wurde der Modellserver deutlich speichereffizienter betrieben.

Die einfache Gesamteinschätzung dieses Tages:

```text
ca. 30 % besser als vorher
```

Realistische nächste Runde:

```text
weitere ca. 15 %
```

Langfristiges praktisches Maximum des aktuellen Stacks:

```text
ca. 50–65 % besser als der ursprüngliche Zustand
```

Danach wären größere Architektur- oder Modellschritte erforderlich.

**Produktiv gesund:** JA  
**Aktueller Durchgang offen:** NEIN  
**Ben vollständig autonom:** NEIN  
**Ben als starker lokaler Operator unter Aufsicht:** JA
