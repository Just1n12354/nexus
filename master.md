---
title: Nexus — Master-Index
aliases: [master, nexus-vault, index, _index]
description: Zentrale Navigation für das gesamte Itin TechSolutions Nexus Vault — alle Domänen, Ordner und Schlüsselkonzepte auf einen Blick.
type: master-index
status: aktiv
updated: 2026-06-25
---

# Nexus — Master-Index

> **Itin TechSolutions Nexus Vault** — Das zentrale Wissenssystem von Justin Itin.
> Obsidian-Style Wikilinks, YAML-Frontmatter, append-only Logs.
> Git-Repo: `github.com/Just1n12354/nexus` (privat)

## Überblick

Das Nexus Vault ist eine **strukturierte Wissensdatenbank** mit 7 Hauptdomänen, 80+ Dateien und einem append-only Wochenlog-System.

```
┌────────────┬──────────────┬────────────┬────────────────┐
│  00_Log    │ 10_Personen  │ 20_Projekte│  30_Agenten    │
│  Wochenlogs│  Profile     │ Konzepte   │  KI-Systeme    │
├────────────┼──────────────┼────────────┼────────────────┤
│  40_Finanzen│ 50_Systeme   │ 70_Arbeit  │ 80_Roboter     │
│  Budgets   │ Hardware     │ Acino/Itin │  PiCrawler     │
├────────────┼──────────────┼────────────┼────────────────┤
│  60_Referenz│ README      │ README     │ README         │
│  Lessons,  │ 10/40/50/60  │ 70         │ 80             │
│  Improv.   │              │            │                │
└────────────┴──────────────┴────────────┴────────────────┘
```

## Domänen

### [[00_Log/README|00_Log]] — Wochenlogs

Append-only Log-System.

- Struktur: `00_Log/JJJJ/KW_NN/LOG.md` (Jahr → Kalenderwoche)
- Format: `log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde>`
- Aktuelle Woche: 2026/KW_26 (Stand 2026-06-25)
- Log-Einträge von 2002 bis 2026, insgesamt 20+ Wochen-Einträge

### [[10_Personen/]] — Personen

- [[10_Personen/privat/justin.md|Justin Itin]] — IT-Einzelunternehmer, Gründer Itin TechSolutions
  - [[biografie|Biografie]] — Persönliche Daten, Beruf, Sprachen, Hobbys
  - [[arbeitsweise|Arbeitsprinzipien]] — Arbeitsstil, Kommunikation, Agentenregeln
- [[10_Personen/privat/sarah.md|Sarah]] — Partnerin

### [[40_Finanzen/]] — Finanzen

- Finanzprinzipien, Budgets, Investments, Konten
- App: [[20_Projekte Konzepte/justfinanceprivate|JustFinancePrivate]]

### [[20_Projekte Konzepte/INDEX|20_Projekte & Konzepte]]

Portfolio aller Projekte und Konzepte:

- **Aktive Apps (22):** ai-fight-club, aieyes, claudesync, jarvis, justbetter, justfinancebusiness (8010), justfinanceprivate (8020), justlauncher (8000), justreise (8040), justsavegame (8765), justtodo (8030), justupdate, justwebsite, projectnorm, sherlock-holmes, swissaisolutions, nexus, watson, atlas, justdaybook, projectfusion, aiworld
- **Friedhof (eingestellt):** AIWorld, JustDaybook

### [[30_Agenten/]] — KI-Agenten

- [[30_Agenten/Ben/memory.md|Ben]] — Hermes-Agent (GX10 Host)
- [[30_Agenten/Luna/]] — Luna (eigener Agent mit SOUL.md, config.yaml, memories/)
- [[30_Agenten/APIKeys/]] — API-Keys (Brave, Telegram, Telegram-Ben)
  - Bewusst im privaten Repo commitet
  - Bei Repo-Wechsel auf public → Key rotieren

### [[50_Systeme/hardware.md|50_Systeme]] — Hardware

- Gerätepark mit Tailscale-Netzwerk
- GX10 (GB10) → 126 Ollama-Modelle, 1.4 TB (Ben-Host)
- Mac mini M4 → Hermes-Server, NAS-Server
- GamingPC (RTX 3090) → AI-Fight-Club
- NAS Synology DS923+ → 34 GB IT-Schulung, 1.4 TB LLM-Modelle
- MacBook Air M4, Pi 5, S24

### [[70_Arbeit/]] — Arbeit

- [[70_Arbeit/itintech-firma.md|Itin TechSolutions]] — Firma (UID CHE-359.787.114, gegründet 01.04.2026)
- [[70_Arbeit/itintech-kunden.md|Kunden]] — Kundenübersicht
- [[70_Arbeit/acino-job.md|Acino/Arcera]] — Arbeitgeber-Job, SIP-Wartung, E-Instandhaltung
- [[70_Arbeit/itintech-kollaborationen.md|Kollaborationen]] — Partner & Zusammenarbeit
- [[70_Arbeit/itintech-versicherungen.md|Versicherungen]] — Helvetia, Zurich, AXA etc.

### [[80_Roboter/README|80_Roboter]] — Physische Roboter

- [[80_Roboter/picrawler/README|PiCrawler "Manfred"]] — SunFounder Quadruped, 12 Servos, Raspberry Pi
  - Status: aktiv (1 Bein defekt, Kamera offen)
  - Detail-Wissen: `picrawler/` mit hardware-status, kinematics, camera-detection, etc.

### [[60_Referenz/README|60_Referenz]] — Referenzen

- [[60_Referenz/service-ports.md|Service-Ports]] — Alle Ports und Services (Mac mini, GX10, GamingPC, Pi 5)
- [[60_Referenz/lessons-learned.md|Lessons Learned]] — 25 Lessons (Git, Agenten, Infrastruktur, Acino)
- [[60_Referenz/improvements.md|Improvements]] — 17 Verbesserungen, 5 offene Fragen

## Konventionen

### File-Naming

- **Singular** statt Plural: `Kunde.md`, nicht `Kunden.md`
- **Keine** Sonderzeichen, nur Buchstaben, Zahlen, Bindestrich, Unterstrich
- **Kleinbuchstaben**: `justfinancedashboard.md`

### YAML-Frontmatter (alle Dateien)

```yaml
---
title: Dateiname
type: <index|log|moc|note|readme|reference>
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

### Port-Zuweisung (Mac mini, Tailscale 100.89.217.4)

| Port | Service |
|------|---------|
| 8000 | justlauncher (Dashboard, geplant) |
| 8010 | justfinancebusiness |
| 8020 | justfinanceprivate |
| 8030 | justtodo |
| 8040 | justreise |
| 8050 | justbetter (Konzept) |
| 5077 | justsavegame |
| 8765 | atlas/justsavegame (historisch) |

## Quick-Jumps

| Bereich | Stem | Beschreibung |
|---------|------|-------------|
| Alle Projekte | [[20_Projekte Konzepte/INDEX|20_Projekte & Konzepte]] | Portfolio-Übersicht mit Status & Ports |
| Firma | [[70_Arbeit/itintech-firma.md|Itin TechSolutions]] | Itin TechSolutions, UID, Rechtliches |
| Acino-Job | [[70_Arbeit/acino-job.md|Acino/Arcera]] | Acino/Arcera Jobs, Wartung, SIP |
| Agenten | [[30_Agenten/|30_Agenten]] | Ben (GX10) & Luna (KI-Agent) |
| Hardware | [[50_Systeme/hardware.md|Hardware]] | Gerätepark, Tailscale, 126 Ollama-Modelle |
| Roboter | [[80_Roboter/README|80_Roboter]] | PiCrawler Manfred, Quadruped |
| Referenzen | [[60_Referenz/README|60_Referenz]] | Service-Ports, Lessons Learned, Improvements |
| Finanzen | [[40_Finanzen/README|Finanzen]] | Budgets, Investments, Konten |
| API-Keys | [[30_Agenten/APIKeys/README.md|API-Keys]] | Brave, Telegram (privat committed) |

## History

- **2002–2023**: Leere Wochen als Lebens-Meilensteine (2019: Lehrbeginn, 2023: Acino-Start)
- **2025–2026**: Aktive Woche-Logs (20+ Einträge)
- **2026-06-08**: Topologie-Standardisierung (Jahr zuerst, dann KW)
- **2026-06-08**: Eintrags-Muster vereinheitlicht (kein Bindestrich vor "log")
- **2026-06-14**: Append-only-Hook entfernt, manuelle TREE.md-Pflege
- **2026-06-14**: `_tools/` entfernt (deprecated, check_vault.py etc. in Git-History)
- **2026-06-21**: API-Keys bewusst ins Repo commitet (private decision)
- **2026-06-24**: Master-Index angelegt
- **2026-06-25**: 60_Referenz hinzugefügt; 40_Finanzen hinzugefügt; 70_Arbeit/acino-job.md hinzugefügt; 60_Referenz/README.md hinzugefügt; 10_Personen/privat/biografie.md + arbeitsweise.md (Split von justin.md); _reports/ hinzugefügt