---
title: ProjectFusion — Projekt-Standard & Topologie
description: ProjectFusion: Standard-Projektstruktur und -Workflow für alle Justin-Projekte (Versionierung, Agent-Kollaboration, Topologie-Schema)
type: project
status: aktiv
phase: 5
created: 2026-06-25
updated: 2026-06-25
tags: [projekt/standard, projectfusion, topologie, agenten]
project: projectfusion
---

# ProjectFusion — Projekt-Standard & Topologie

## Konzept

ProjectFusion definiert den Standard für alle Justin-Projekte: einheitliche Topologie, Agent-Kollaboration, Versionierung.

### Topologie-Schema (V5)
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

### Versionierungs-Regel
- EIN `.Vx.xx`-Ordner pro Projekt-Änderung
- Umbenennen via `projectfusion.py version`, NIE kopieren
- Changelog-Bump im selben Ordner (nur Changelog und README aktualisieren)

### Agent-Kollaboration
- `AGENTS.md` mit Ordner-Regel in ALLEN Projekten (V5)
- Pro Agent eine Rolle + Zuständigkeit
- Keine parallelen `.Vx.xx`-Ordner (Problem behoben)

### Status
- V5 auf alle Projekte ausgerollt
- 22 Projekt-AGENTS.md angepasst (Rule-Block "Bei einer Änderung — was jede KI tun muss")
- Vorlage für neue Projekte aktualisiert
- Problem: "Parallel-Ordner statt Versions-Rename" gefixt (3× falsche Kopie → Umbenennung)

→  (Parallel-Agent-Probleme)
→ [[lessons-learned]] (Versionierungs-Lehren)