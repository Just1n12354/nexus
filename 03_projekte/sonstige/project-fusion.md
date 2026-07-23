---
title: ProjectFusion — Projektstandard & Tooling
description: ProjektFusion: Standard-Projektstruktur, Tooling und Workflow für alle Justin-Projekte (Topologie V5, Agent-Kollaboration, README als Single Source, Deck/AGENTS.md-Generierung)
type: project
status: aktiv
phase: 5
created: 2026-06-25
updated: 2026-07-21
tags: [projekt/standard, projectfusion, topologie, agenten, tooling]
project: projectfusion
---

# ProjectFusion — Projektstandard & Tooling

## Konzept

ProjectFusion definiert den Standard für alle Justin-Projekte: einheitliche Topologie, Agent-Kollaboration, Versionierung, und deterministisches Tooling.

## Topologie-Schema (V5)

```
20_Projekte/
  10_Apps/          (Lauffähige Apps)
    Aktiv/          (Aktive Projekte)
      <AppName>/
        README.md
        CHANGELOG.md
        TODO.md
        docs/
        src/
        data/
        config/
        tests/
        archive/
        temp/
    Friedhof/       (Archivierte/Experimente)
      <AppName>/
  20_Konzepte/      (Ideen/Prototypen ohne Live-Deploy)
    <Konzept>/
  30_Friedhof/      (Endgültig archiviert)
```

**Topologie-Regel:** Wurzel = nur Ordner + erlaubte lose Dateien (README.md, AGENTS.md, .gitignore, .gitattributes). Standard-Ordner: PowerPoint/, Archiv/ (nie hart löschen).

## README als Single Source

Ziel: jedes Projekt sieht gleich aus — Mensch ODER KI versteht es sofort. Ändern heißt: nur die README bearbeiten, den Rest macht das Tool.

## Stack / Technik

- `Tooling/projectfusion.py` (Python). README → Deck via python-pptx (liest #/##/- Markdown). README → AGENTS.md: Essenz zwischen Marker-Kommentaren regeneriert, handgepflegte Abschnitte bleiben.
- pre-commit-Hook regeneriert Deck bei jeder geänderten README (ohne Versions-Bump → kein Binär-Wildwuchs).
- `pf-config.json`: Setup-Fragen (inkl. Ordner-Versionierung: Opt-in).

## Versionierung

- EIN `.Vx.xx`-Ordner pro Projekt-Änderung.
- Umbenennen via `projectfusion.py version`, NIE kopieren.
- Changelog-Bump im selben Ordner (nur Changelog und README aktualisieren).
- Ordner-Versionierung (`.V0.01` am Ordnernamen) ist **Opt-in** — Umbenennen ändert Pfade und kann LaunchAgents/Deploy/Imports brechen. Auch ohne sie kennt Nexus den Stand (Version im README-Header, Changelog, VERSIONS.md).

## Agent-Kollaboration

- `AGENTS.md` mit Ordner-Regel in ALLEN Projekten (V5).
- Pro Agent eine Rolle + Zuständigkeit.
- Keine parallelen `.Vx.xx`-Ordner (Problem behoben: 3× falsche Kopie → Umbenennung).

## Stand / Funktionen

- V5 auf alle Projekte ausgerollt.
- 22 Projekt-AGENTS.md angepasst (Rule-Block: "Bei einer Änderung — was jede KI tun muss").
- Vorlage für neue Projekte aktualisiert.
- Problem: "Parallel-Ordner statt Versions-Rename" gefixt.
- Offen: Theme-template.pptx hinterlegen; Rollout auf die ~18 bestehenden Projekte abschließen.

## Health (Audit 2026-06-07)

- Portfolio-Durchschnitt ~70/100. Repo ist **privat** — kein Live-Security-Leck.
- Größte Tech-Schuld: monolithische Frontends und Code-Duplikation (`api_auth.py` war 4× identisch → kanonisiert in `_shared/`).

## Verweise

- Quelle: `10_Apps/ProjectNorm/` (Itin-TechSolutions Repo)
- Standard für ALLE Projekte; vgl. VERSIONS.md. Verwandt: [[claudesync.md]]
- Portfolio-Übersicht: [[../INDEX.md]]
- Projektstruktur im Vault: [[tree]]

→ [[../../07_referenz/lessons-learned.md]] (Versionierungs-Lehren)