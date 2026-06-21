# Hermes Home Topologie

Stand: 2026-06-12 (Wartungspass durch Claude / Fable 5)
Aktives Profil: `default`

Diese Datei ist die Karte des laufenden `~/.hermes` auf dem Mac mini.
**Für Luna:** Das ist dein operatives Zuhause. Dein dauerhaftes Brain liegt NICHT hier,
sondern im nexus: `/Users/imjustin/Documents/GitHub/nexus/30_Agenten/Luna/`.

## ✅ Zustand nach dem Wartungspass 2026-06-12 — deutlich besser als vorher

Was jetzt funktioniert, was vorher kaputt oder schlecht war:

| Bereich | Vorher | Jetzt |
|---|---|---|
| **Websuche** | `firecrawl` ohne API-Key → `web_search` lieferte **nichts** | `search_backend: brave-free` → echte Resultate (getestet), 2'000 Suchen/Monat |
| **Memory-Puffer** | 2'200/1'375 Zeichen, lief permanent über → Schreibfehler | 4'000/2'500 + dedupliziert → viel Luft |
| **Zeitzone** | leer (UTC-Raten bei Cron/Timestamps) | `Europe/Zurich` |
| **Spracherkennung (STT)** | Whisper ohne Sprachvorgabe | fest auf `de` |
| **Stimme (TTS)** | englische Stimme (en-US-Aria) | `de-DE-KatjaNeural` |
| **Sessions-DB** | 110 MB nach 2 Wochen, kein Pruning | Auto-Prune an (90 Tage Retention) |
| **SOUL.md** | alter nexus-Bootstrap, kein Eingangskorb-Check | V3-Bootstrap + `00_InputLuna`-Check + Persistenz-Regel |
| **Aufgeräumtheit** | 8 `.bak`-Dateileichen im Home verstreut | alle unter `backups/` |
| **.env** | doppelter Key `BRAVIAPI` | entfernt (Duplikat von `BRAVE_SEARCH_API_KEY`) |

**Wichtig für Luna:** `web_extract` hat weiterhin **kein** Backend (bräuchte Firecrawl-/Tavily-Key).
Für Seiteninhalte → Browser-Tool nutzen. Suche selbst läuft über Brave.

## 🔒 Update-Sicherheit (wichtig)

Dieser Umbau ist **bewusst update-sicher** gehalten — `pipx upgrade hermes-agent` und
Hermes-Config-Migrationen werden dadurch NICHT gestört:

- **Nur Standard-Config-Keys geändert** (`web.search_backend`, `timezone`, `stt`, `tts`,
  `memory.*_limit`, `sessions.auto_prune`) — alles offizielle Felder, `_config_version` unangetastet.
- **Keine Runtime-Datei verschoben oder umbenannt.** Alle Pfade, die Hermes erwartet
  (config.yaml, .env, auth.json, state.db, memories/, sessions/, skills/, logs/, cron/), liegen wo immer.
- **`backups/` ist rein additiv** — Hermes kennt den Ordner nicht und ignoriert ihn. Dort liegen
  die Vorher-Stände (config.yaml, .env, alte .bak-Dateien). Bei Probleme: von dort zurückkopieren.
- **SOUL.md / TOPOLOGY.md sind Doku/Persona** — werden von Updates nicht angefasst und fassen
  selbst nichts an.

Wenn ein Hermes-Update neue Config-Defaults bringt, merged Hermes die selbst in config.yaml —
die gesetzten Werte oben bleiben dabei erhalten.

## Karte

```text
~/.hermes
├── config.yaml                # Hauptkonfiguration (Stand 2026-06-12, s. Tabelle oben)
├── .env                       # Secrets: Telegram, Brave, Spotify
├── auth.json                  # OAuth (openai-codex, spotify) + Credential-Pool
├── SOUL.md                    # Lunas Persona + nexus-V3-Bootstrap (wird jede Session geladen)
├── TOPOLOGY.md                # diese Datei
├── gateway_state.json         # Gateway-Laufzeitzustand
│
├── memories/                  # MEMORY.md + USER.md — NUR Index/Cache, Wahrheit = nexus
├── sessions/                  # Session-Artefakte
├── state.db*                  # kanonische Session-DB (Auto-Prune 90 Tage aktiv)
├── kanban.db*                 # Kanban-Board
│
├── skills/                    # 123 aktive Skills + .archive/ + CATALOG.md
├── hooks/ · bin/ · lsp/       # Capability-Ebene
│
├── logs/                      # agent.log, gateway.log, errors.log (Rotation 5 MB)
├── cron/                      # jobs.json (Morgengruss 6:00, AIFightClub-Watch 120m) + output/
├── scripts/                   # eigene Cron-Skripte (aifightclub_v5_watch.py)
├── backups/                   # ← NEU: alle Vorher-Stände & .bak-Dateien (additiv, update-neutral)
└── cache/ · image_cache/ · audio_cache/ · sandboxes/   # Wegwerf-Artefakte
```

## Funktionsebenen (unverändert gültig)

1. **Control plane** — config.yaml, .env, auth.json, gateway_state.json, SOUL.md
   → nie aus Ästhetik verschieben.
2. **Memory + State** — memories/, sessions/, state.db*, kanban.db
   → operative Datenbanken, keine Putz-Ziele.
3. **Capability** — skills/, hooks/, bin/, lsp/
   → hier darf verbessert werden (Skills, Doku, Kataloge).
4. **Generierte Artefakte** — logs/, cron/output/, caches, sandboxes/
   → Cleanup-Kandidaten bei Plattenplatz-Bedarf.

## Regeln für künftige Wartung (Luna & andere Agenten)

**Gute Änderungen:**
- Config-Werte über offizielle Keys anpassen (vorher Kopie nach `backups/`)
- Skills pflegen, Kataloge/Doku aktualisieren
- Stale Skills nach `.archive/` statt löschen
- Diese Datei nach jedem Wartungspass aktualisieren (Stand-Datum oben!)

**Verbotene Änderungen ohne expliziten Auftrag:**
- DBs, memories/, sessions/, logs/ verschieben oder umbenennen
- `_config_version` oder unbekannte Config-Keys erfinden
- .env-Keys löschen, die irgendwo referenziert sein könnten (erst grep über das Hermes-Package)
- Caches löschen, während das Gateway aktiv arbeitet

## Historie der Wartungspässe

- **2026-06-07** — Pass 1+2: Skill-Ordner kanonisch benannt, Platzhalter-Kategorien entfernt, CATALOG.md
- **2026-06-08** — Self-Repair: Compression auf copilot/gpt-4.1 (Threshold 0.42), Skills entschärft
- **2026-06-12** — Großer Wartungspass (s. Tabelle oben): Websuche gefixt, Lokalisierung CH/DE,
  Memory-Limits, Auto-Prune, SOUL.md V3, backups/ eingeführt. Doku im nexus:
  `30_Agenten/Luna/memory.md` (Eintrag 2026-06-12) + `handoff.md`.
