---
title: Justreise
type: note
status: aktiv
updated: 2026-06-24
---

# JustReise · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Reise-Field-Guide als Flask-PWA. Geteilter Guide (Justin & Sarah): Flüge, Hotel, Aktivitäten, Spots, geteilte Checkliste, editierbare Tagespläne, Reise-Dokumente, Schritte-Tracking. Aktuelle Reise: London (3.–9. Juni 2026). Eigenständiger Service (aus JustLauncher ausgegliedert).

## Stack / Technik
- Flask-PWA. `src/`: app.py, justreise_data.py, templates/, static/. `config/`: Dockerfile, docker-compose.yml, requirements.txt, *.plist.
- Routen: / (Field Guide), /todos, /dayplan, /doc/<datei>, /manifest.webmanifest, /api/v1/health.

## Stand / Funktionen
- Aktiv, war live für den London-Trip. LaunchAgent `com.itintechsolutions.justreise`, läuft aus Runtime-Klon `~/JustReise`.
- Daten in `data/london/` (Pässe, Buchungen, Finanzen, State-JSONs lokal/git-ignoriert; nur london.md im Git). Pfad per Env `JUSTREISE_LONDON_DIR` überschreibbar.

## Betrieb
- Mac mini, Port **8040**. Start: `python3 src/app.py` oder Docker Compose.

## Health (Audit 2026-06-07)
- **72/100** — größtes Problem: hardcoded „London"-Konstanten, manuelles Deploy, keine Tests. Generalisierung (London → Trip) nur lohnend bei weiteren Reisen.

## Verweise
- Quelle: 10_Apps/JustReise/
- Verwandt: [[justlauncher]] (Ursprung)
