---
title: Nexus — Master-Index
aliases: [master, nexus-vault, index, _index]
description: Zentrale Navigation für das gesamte Itin TechSolutions Nexus Vault — alle Domänen, Ordner und Schlüsselkonzepte auf einen Blick.
type: master-index
status: aktiv
updated: 2026-06-24
---

# Nexus — Master-Index

> **Itin TechSolutions Nexus Vault** — Das zentrale Wissenssystem von Justin Itin.
> Obsidian-Style Wikilinks, YAML-Frontmatter, append-only Logs.
> Git-Repo: `github.com/Just1n12354/nexus` (privat)

## Überblick

Das Nexus Vault ist eine **strukturierte Wissensdatenbank** mit 8 Hauptdomänen, 40+ Dateien und einem append-only Wochenlog-System. Es dient als Single Source of Truth für Firma, Privat, Projekte, Agenten, Systeme und Roboter.

```
┌──────────────────────────────────────────────────────────┐
│                    NEXUS VAULT                           │
├────────────┬──────────────┬────────────┬────────────────┤
│  00_Log    │ 10_Personen  │ 20_Projekte│  30_Agenten    │
│  Wochenlogs│  Profile     │ Konzepte   │  KI-Systeme    │
├────────────┼──────────────┼────────────┼────────────────┤
│  50_Systeme│ 70_Arbeit    │ 80_Roboter │  _tools        │
│  Hardware  │ Acino/Itin   │  PiCrawler │  (deprecated) │
└────────────┴──────────────┴────────────┴────────────────┘
```

---

## Domänen

### [[00_Log/README|00_Log]] — Wochenlogs
Append-only Log-System mit append-only Wochenlogs mit append-only Log-System mit append-only Wochenlogs.
- Struktur: `00_Log/JJJJ/KW_NN/LOG.md` (Jahr → Kalenderwoche)
- Format: `log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde>`
- Aktuelle Woche: 2026/KW_25 (Stand 2026-06-24)
- Log-Einträge von 2002 bis 2026, insgesamt 20+ Wochen-Einträge

### [[10_Personen/]] — Personen
- [[10_Personen/privat/justin.md|Justin Itin]] — IT-Einzelunternehmer, Gründer Itin TechSolutions
- [[10_Personen/privat/sarah.md|Sarah]] — Partnerin

### [[20_Projekte Konzepte/INDEX|20_Projekte & Konzepte]]
Portfolio aller Projekte und Konzepte:
- **Aktive Apps (14):** ai-fight-club, aieyes, claudesync, jarvis, justbetter, justfinancebusiness (8010), justfinanceprivate (8020), justlauncher (8000), justreise (8040), justsavegame (8765), justtodo (8030), justupdate, justwebsite, projectnorm, sherlock-holmes, swissaisolutions
- **Prototypen:** claudesync, sherlock-holmes
- **Konzept:** justbetter
- **Friedhof (eingestellt):** AIWorld, Atlas, JustDaybook

### [[30_Agenten/]] — KI-Agenten
- [[30_Agenten/Ben/memory.md|Ben]] — Hermes-Agent (Mac mini Host)
- [[30_Agenten/Luna/]] — Luna (eigener Agent mit SOUL.md, config.yaml, memories/)
- [[30_Agenten/APIKeys/]] — API-Keys (Brave, Telegram, Telegram-Ben)
  - Bewusst im privaten Repo commitet
  - Bei Repo-Wechsel auf public → Key rotieren

### [[50_Systeme/hardware.md|50_Systeme]] — Hardware
- Gerätepark mit Tailscale-Netzwerk
- GX10 (DGX Spark/GB10) → Ben-Host
- Mac mini M4 → Hermes-Server, NAS-Server
- GamingPC (RTX 3090) → AI-Fight-Club, NoMachine
- NAS Synology DS923+ → 1.4 TB LLM-Modelle
- MacBook Air M4, Pi 5, S24

### [[70_Arbeit/]] — Arbeit
- [[70_Arbeit/itintech-firma.md|Itin TechSolutions]] — Firma (UID CHE-359.787.114, gegründet 01.04.2026)
- [[70_Arbeit/itintech-kunden.md|Kunden]] — Kundenübersicht
- [[70_Arbeit/itintech-kollaborationen.md|Kollaborationen]] — Partner & Zusammenarbeit
- [[70_Arbeit/itintech-versicherungen.md|Versicherungen]] — Helvetia, Zurich, AXA etc.
- [[acino-job|Acino/Arcera]] — Arbeitgeber-Job, SIP-Wartung, E-Instandhaltung

### [[80_Roboter/README|80_Roboter]] — Physische Roboter
- [[80_Roboter/picrawler/README|PiCrawler "Manfred"] ] — SunFounder Quadruped, 12 Servos, Raspberry Pi
  - Status: aktiv (1 Bein defekt, Kamera offen)
  - Detail-Wissen: `picrawler/` mit hardware-status, kinematics, camera-detection, etc.

---

## Konventionen

### File-Naming
- **Singular** statt Plural: `Kunde.md`, nicht `Kunden.md`
- **Keine** Sonderzeichen, nur Buchstaben, Zahlen, Bindestrich, Unterstrich
- **Kleinbuchstaben**: `justfinancedashboard.md`

### YAML-Frontmatter (alle Dateien)
```yaml
---
title: Dateiname
type: <index|log|moc|note|readme>
status: <aktiv|konzept|prototyp|erledigt|archiviert>
updated: YYYY-MM-DD
description: Kurze Beschreibung
---
```

### Wikilinks
- Verweise innerhalb des Nexus: `[[Dateiname]]`
- Mit Alias: `[[Dateiname|Sichtbarer Text]]`
- Querverweise am Ende einer Datei in einer Zeile

### Wochenlog (append-only)
- Format: `log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde gemacht>`
- Einträge chronologisch (neueste zuerst)
- Alte Einträge **niemals** editieren oder löschen
- Append-only-Prinzip gilt als verbindliche Disziplin

### Versionsnummerierung (Projekte)
- `MAJOR.MINOR.PATCH-dev` (z.B. `6.0.0-dev`, `0.002`)
- Alle Versionen in `VERSIONS.md` pro Projekt

### Port-Zuweisung (Mac mini, Tailscale 100.89.217.4)
- 8000: justlauncher (Dashboard)
- 8010: justfinancebusiness
- 8020: justfinanceprivate
- 8030: justtodo
- 8040: justreise
- 8050: justbetter (Konzept)
- 3000: jarvis
- 3000: jarvis

---

## Quick-Jumps

| Bereich | Stem | Beschreibung |
|---------|------|-------------|
| Alle Projekte | [[20_Projekte/INDEX]] | Portfolio-Übersicht mit Status & Ports |
| Firma | [[itintech-firma]] | Itin TechSolutions, UID, Rechtliches |
| Acino-Job | [[acino-job]] | Acino/Arcera Jobs, Wartung, SIP |
| Agenten | [[30_Agenten/]] | Ben (Hermes) & Luna (KI-Agent) |
| Hardware | [[50_Systeme/hardware]] | Gerätepark, Tailscale, Ports |
| Roboter | [[80_Roboter/README]] | PiCrawler Manfred, Quadruped |
| API-Keys | [[30_Agenten/APIKeys]] | Brave, Telegram (privat committed) |

---

## History

- **2002–2023**: Leere Wochen als Lebens-Meilensteine (2019: Lehrbeginn, 2023: Acino-Start)
- **2025–2026**: Aktive Woche-Logs (20+ Einträge)
- **2026-06-08**: Topologie-Standardisierung (Jahr zuerst, dann KW)
- **2026-06-08**: Eintrags-Muster vereinheitlicht (kein Bindestrich vor "log")
- **2026-06-14**: Append-only-Hook entfernt, manuelle TREE.md-Pflege
- **2026-06-21**: API-Keys bewusst ins Repo commitet (private decision)
- **2026-06-24**: Master-Index angelegt