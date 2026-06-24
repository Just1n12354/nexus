---
title: Nexus — File Tree
aliases: [tree, file-structure, directory-tree]
description: Vollständige Verzeichnisstruktur des Nexus Vault mit Dateibesprechungen.
type: tree
status: aktiv
updated: 2026-06-25
---

# Nexus — File Tree

> Vollständige Verzeichnisstruktur des Nexus Vault (Stand 2026-06-25).
> Quelle: `~/Documents/GitHub/nexus/`

```
nexus/
├── .git/                           # Git-Repository (privat)
├── .gitignore
├── .obsidian/                      # Obsidian-Konfiguration
│   ├── appearance.json
│   ├── app.json
│   └── core-plugins.json
│
├── master.md                       # Master-Index (diese Datei)
├── tree.md                         # File Tree (diese Datei)
│
├── 00_Log/                         # Wochenlogs (append-only)
│   ├── README.md                   # Log-Topologie, Eintrags-Muster, Workflow
│   ├── 2002/KW_46/LOG.md           # 2002, KW 46
│   ├── 2005/KW_07/LOG.md           # 2005, KW 7
│   ├── 2019/KW_31/LOG.md           # 2019, KW 31 (Lehrbeginn)
│   ├── 2022/KW_14/LOG.md           # 2022, KW 14 (Sarah)
│   ├── 2022/KW_35/LOG.md           # 2022, KW 35
│   ├── 2023/KW_31/LOG.md           # 2023, KW 31 (Acino-Start)
│   ├── 2025/KW_01/LOG.md           # 2025, KW 1 (Militär-Kaderausbildung)
│   ├── 2025/KW_40/LOG.md           # 2025, KW 40
│   ├── 2026/
│   │   ├── KW_09/LOG.md            # 2026, KW 9
│   │   ├── KW_12/LOG.md            # 2026, KW 12
│   │   ├── KW_13/LOG.md            # 2026, KW 13
│   │   ├── KW_14/LOG.md            # 2026, KW 14
│   │   ├── KW_15/LOG.md            # 2026, KW 15
│   │   ├── KW_16/LOG.md            # 2026, KW 16
│   │   ├── KW_17/LOG.md            # 2026, KW 17
│   │   ├── KW_18/LOG.md            # 2026, KW 18
│   │   ├── KW_19/LOG.md            # 2026, KW 19
│   │   ├── KW_20/LOG.md            # 2026, KW 20
│   │   ├── KW_21/LOG.md            # 2026, KW 21
│   │   ├── KW_22/LOG.md            # 2026, KW 22
│   │   ├── KW_23/LOG.md            # 2026, KW 23
│   │   ├── KW_24/LOG.md            # 2026, KW 24
│   │   ├── KW_25/LOG.md            # 2026, KW 25
│   │   └── KW_26/LOG.md            # 2026, KW 26 (aktuelle)
│   └── README.md                   # Log-Topologie, Eintrags-Muster, Workflow
│
├── 10_Personen/                    # Personen-Profile
│   └── privat/
│       ├── justin.md               # Justin Itin — IT-Einzelunternehmer
│       └── sarah.md                # Sarah — Partnerin
│
├── 20_Projekte Konzepte/           # Projekt-Portfolio
│   ├── INDEX.md                    # Portfolio-Übersicht (alle Projekte)
│   ├── ai-fight-club.md            # Liga-Arena: ~95 Ollama-Modelle, 15 Challenges
│   ├── aieyes.md                   # Augen+Hände für KI (Screenshot + Maus/Tastatur)
│   ├── aiworld.md                  # Bot-Orchestrierung (Friedhof)
│   ├── atlas.md                    # Wissenskartierung
│   ├── claudesync.md               # Single Source für Claude-Code-Config
│   ├── jarvis.md                   # Lokaler Sprach-/Aktions-Assistent
│   ├── justbetter.md               # KI-Coach (Konzept)
│   ├── justdaybook.md              # Flask-Tagebuch (archiviert)
│   ├── justfinancebusiness.md      # Buchhaltung Itin TechSolutions (Port 8010)
│   ├── justfinanceprivate.md       # Private Finanzen (Port 8020)
│   ├── justlauncher.md             # Dashboard für alle Just-Dienste (Port 8000)
│   ├── justreise.md                # Reise-Field-Guide (Port 8040)
│   ├── justsavegame.md             # Savegame-Backup-Manager Windows (Port 8765)
│   ├── justtodo.md                 # Datei-basierte Todo-App (Port 8030)
│   ├── justupdate.md               # Windows-Wartungs-Tool + Self-Update
│   ├── justwebsite.md              # Statische Firmen-Website (Netlify)
│   ├── nexus.md                    # Haupt-Projekt: Nexus Vault
│   ├── projectfusion.md            # Projekt-Standard V5
│   ├── projectnorm.md              # Projekt-Standard (README = Single Source)
│   ├── sherlock-holmes.md          # Recherche-Agent (GitHub/Reddit)
│   ├── swissaisolutions.md         # Plug-&-Play KI-Box für KMU (MRR)
│   └── watson.md                   # Git-History-Tool (Conventional Commits)
│
├── 30_Agenten/                     # KI-Agenten
│   ├── APIKeys/                    # API-Keys (bewusst im privaten Repo committed)
│   │   ├── README.md               # Dokumentation der API-Keys
│   │   ├── BraveAPI.txt            # Brave Search API
│   │   ├── Telegram.txt            # Telegram (Ping-Bot)
│   │   └── Telegram-Ben.txt        # Telegram-Bot für Ben
│   ├── Ben/
│   │   ├── ARBEITSLOG.md           # Ben-Arbeitsprotokoll
│   │   ├── ben.md                  # Ben-Agent (Rolle/Wissen)
│   │   └── memory.md               # Ben-Agent Gedächtnis
│   └── Luna/                       # Luna (KI-Agent mit eigenem SOUL)
│       ├── README.md
│       ├── config.yaml             # Konfiguration
│       ├── SOUL.md                 # Persönlichkeit
│       ├── TOPOLOGY.md             # Topologie-Übersicht
│       └── memories/
│           ├── MEMORY.md           # System-Wissen
│           └── USER.md             # User-Profile
│
├── 50_Systeme/                     # Systeme & Hardware
│   └── hardware.md                 # Gerätepark, Tailscale, 126 Ollama-Modelle
│
├── 60_Referenz/                    # Referenzen & Wissen
│   ├── improvements.md             # 17 Verbesserungen, 5 offene Fragen
│   ├── lessons-learned.md          # 25 Lessons (Git, Agenten, Infra, Acino)
│   └── service-ports.md            # Alle Service-Ports (Mac mini, GX10, etc.)
│
├── 70_Arbeit/                      # Arbeitskontext
│   ├── itintech-firma.md           # Itin TechSolutions, UID, Rechtliches
│   ├── itintech-kollaborationen.md # Partner & Zusammenarbeit
│   ├── itintech-kunden.md          # Kundenübersicht
│   └── itintech-versicherungen.md  # Helvetia, Zurich, AXA etc.
│
├── 80_Roboter/                     # Physische Roboter
│   ├── README.md                   # Domänen-MOC (Rover)
│   └── picrawler/                  # PiCrawler "Manfred die Spinne"
│       ├── README.md               # Hauptdokumentation
│       ├── actions.md              # Bewegungs-Actions
│       ├── camera-detection.md     # Kameradetection
│       ├── hardware-status.md      # Hardware-Status (Servo-Defekte etc.)
│       ├── kinematics.md           # Kinematik & Servo-Steuerung
│       ├── power-protocol.md       # Power-On/Off Protokoll
│       ├── robot-hat-bugs.md       # Known Bugs (Robot HAT)
│       ├── setup.md                # Installation & Setup
│       └── speaker-gpio.md         # GPIO-Speaker-Steuerung
│
└── _reports/                       # Lauf-Report
    └── NACHT_2026-06-25.md         # Nachtlauf-Report 25.06.2026
```

## Datei-Typen

| Typ | Anzahl | Beschreibung |
|-----|--------|-------------|
| **Log-Dateien** (LOG.md) | 23 | Wochenlogs, append-only |
| **Projekt-Files** | 22 | Projekt-Dokumentation |
| **Agenten-Files** | 9 | Ben & Luna |
| **Roboter-Files** | 9 | PiCrawler "Manfred" |
| **Personen-Files** | 2 | Justin & Sarah |
| **Arbeits-Files** | 4 | Firma, Kunden, Kollaboration, Versicherungen |
| **System-Files** | 1 | Hardware |
| **Referenz-Files** | 3 | Lessons, Improvements, Service-Ports |
| **README/Index** | 6 | Top-level & Domänen-Index |
| **API-Keys** | 3 | Brave, Telegram, Telegram-Ben |
| **Obsidian-Config** | 3 | appearance, app, core-plugins |
| **Report** | 1 | Nachtlauf 25.06.2026 |

## Wichtige Pfade

| Datei | Pfad | Beschreibung |
|-------|------|-------------|
| Master-Index | `master.md` | Alle Domänen auf einen Blick |
| File Tree | `tree.md` | Diese Datei |
| Log-Index | `00_Log/README.md` | Log-Topologie & Workflow |
| Projekt-Index | `20_Projekte Konzepte/INDEX.md` | Portfolio-Übersicht |
| Roboter-MOC | `80_Roboter/README.md` | Domänen-Index Roboter |
| Ben memory | `30_Agenten/Ben/memory.md` | Ben-Agent Gedächtnis |
| Luna SOUL | `30_Agenten/Luna/SOUL.md` | Luna-Persönlichkeit |
| Hardware | `50_Systeme/hardware.md` | Gerätepark |
| Service-Ports | `60_Referenz/service-ports.md` | Alle Ports |
| Lessons Learned | `60_Referenz/lessons-learned.md` | 25 Lessons |
| Improvements | `60_Referenz/improvements.md` | 17 Verbesserungen |
| API-Keys | `30_Agenten/APIKeys/README.md` | Keys-Doku |