---
title: Projectnorm
type: note
status: aktiv
updated: 2026-06-24
---

# ProjectNorm · App (Standard/Tooling)

Status: aktiv  ·  Version: 0.000  ·  Letztes Update: 2026-06-14

## Zweck
Ein einheitlicher Standard für alle Projekte & Konzepte: EINE Quelle (`README.md` an der Wurzel), aus der das Tooling Deck (PowerPoint) und die AGENTS.md-Essenz deterministisch erzeugt. Ziel: jedes Projekt sieht gleich aus — Mensch ODER KI versteht es sofort. Ändern heißt: nur die README bearbeiten, den Rest macht das Tool.

## Stack / Technik
- `Tooling/projectfusion.py` (Python). README → Deck via python-pptx (liest #/##/- Markdown). README → AGENTS.md: Essenz zwischen Marker-Kommentaren regeneriert, handgepflegte Abschnitte bleiben.
- pre-commit-Hook regeneriert Deck bei jeder geänderten README (ohne Versions-Bump → kein Binär-Wildwuchs).
- Topologie-Regel: Wurzel = nur Ordner + erlaubte lose Dateien (README.md, AGENTS.md, .gitignore, .gitattributes). Standard-Ordner: PowerPoint/, Archiv/ (nie hart löschen).

## Stand / Funktionen
- V5 neu gebaut: README als Single Source, Briefing-Konzept abgelöst. Tooling: init/pptx(+--bump)/agents/validate/archive/tree/install-hook.
- Ordner-Versionierung (`.V0.01` am Ordnernamen) ist **Opt-in** (Setup-Frage in `pf-config.json`) — Umbenennen ändert Pfade und kann LaunchAgents/Deploy/Imports brechen. Auch ohne sie kennt Nexus den Stand (Version im README-Header, Changelog, VERSIONS.md).
- Offen: Theme-template.pptx hinterlegen; Rollout auf die ~18 bestehenden Projekte abschließen.

## Verweise
- Quelle: 10_Apps/ProjectNorm/
- Standard für ALLE Projekte hier; vgl. VERSIONS.md im Quell-Repo. Verwandt: [[claudesync]]
