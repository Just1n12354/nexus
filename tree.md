---
title: Nexus — File Tree
aliases: [tree, file-structure, directory-tree]
description: Vollständige Verzeichnisstruktur des Nexus Vault (v1-Struktur, restrukturiert) mit Dateibesprechungen.
type: tree
status: aktiv
updated: 2026-07-03
---

# Nexus — File Tree

> Vollständige Verzeichnisstruktur des Nexus Vault — Stand v1-Restrukturierung (2026-07-03).
> Domänen lowercase & durchnummeriert (01–09), Logs flach, Projekte gruppiert.
> Secrets, Code und Obsidian-Config liegen in `_quarantine/` (per `.gitignore` ausserhalb des Vaults).

```
Nexus_KI_v1/
├── README.md                       # KI-optimierter Hauptindex
├── TODO.md                         # Offene Aufgaben
├── tree.md                         # Diese Datei (Vault-Baum)
├── .gitignore                      # Exkludiert _meta/, _quarantine/, .obsidian/
│
├── 01_log/                         # Wochenlogs (append-only), FLACH: YYYY-WNN.md
│   ├── README.md                   # Log-Topologie, Eintrags-Muster, Workflow
│   └── logs/
│       ├── 2002-W46.md
│       ├── 2005-W07.md
│       ├── 2019-W31.md             # Lehrbeginn
│       ├── 2022-W14.md             # Sarah
│       ├── 2022-W35.md
│       ├── 2023-W31.md             # Acino-Start
│       ├── 2025-W01.md             # Militär-Kaderausbildung
│       ├── 2025-W40.md
│       ├── 2026-W09.md … 2026-W25.md   # Wochen 2026
│       ├── 2026-W26-2026-06-22.md … 2026-W26-2026-06-28.md  # W26 aufgeteilt
│       ├── 2026-W26.md                 # W26-Index (verweist auf Tagesdateien)
│
├── 02_personen/                    # Personen-Profile
│   ├── README.md                   # Personen-Übersicht
│   └── privat/
│       ├── justin.md               # Justin Itin — IT-Einzelunternehmer (Hub-Index)
│       ├── biografie.md            # Justin — Biografie (persönliche Daten, Beruf, Hobbys)
│       ├── arbeitsweise.md         # Justin — Arbeitsprinzipien (Kommunikation, Agentenregeln)
│       └── sarah.md                # Sarah — Partnerin
│
├── 03_projekte/                    # Projekt-Portfolio (gruppiert)
│   ├── INDEX.md                    # Portfolio-Übersicht (alle Projekte)
│   ├── README.md                   # Ordner-README
│   ├── autos/
│   │   └── VW-Polo.md              # VW Polo Comfortline 1.0 TSI — MIB2, FEC, Infotainment
│   ├── finanzen/
│   │   ├── just-finance-business.md    # Buchhaltung Itin TechSolutions (Port 8010)
│   │   └── just-finance-private.md     # Private Finanzen (Port 8020)
│   ├── reise/
│   │   ├── just-reise.md               # Reise-Field-Guide (Port 8060)
│   │   └── just-reise-persistence.md   # Reise-Persistenz
│   ├── tools/
│   │   ├── just-launcher.md            # Dashboard für alle Just-Dienste (Port 8000)
│   │   ├── just-savegame.md            # Savegame-Backup-Manager Windows (Port 8765)
│   │   ├── just-todo.md                # Datei-basierte Todo-App (Port 8030)
│   │   └── just-update.md              # Windows-Wartungs-Tool + Self-Update
│   └── sonstige/
│       ├── ai-fight-club.md            # Liga-Arena: ~95 Ollama-Modelle, 15 Challenges
│       ├── aieyes.md                   # Augen+Hände für KI (Screenshot + Maus/Tastatur)
│       ├── aiworld.md                  # Bot-Orchestrierung (Friedhof)
│       ├── atlas.md                    # Wissenskartierung
│       ├── claudesync.md               # Single Source für Claude-Code-Config
│       ├── jarvis.md                   # Lokaler Sprach-/Aktions-Assistent
│       ├── just-better.md              # KI-Coach (Konzept)
│       ├── just-daybook.md             # Flask-Tagebuch (archiviert)
│       ├── just-website.md             # Statische Firmen-Website (Netlify)
│       ├── nexus-projekt.md            # Haupt-Projekt: Nexus Vault
│       ├── minecraftai.md                  # Minecraft-KI-Agent Peter (mineflayer, Qwen3.6)
│       ├── minecraftai-peter-autonomie.md  # Peter: Autonomer Agent, Aufgaben-Motor, Survival
│       ├── project-fusion.md           # Projekt-Standard V5
│       ├── project-norm.md             # Projekt-Standard (README = Single Source)
│       ├── sherlock-holmes.md          # Recherche-Agent (GitHub/Reddit)
│       ├── swissai-solutions.md        # Plug-&-Play KI-Box für KMU (MRR)
│       └── watson.md                   # Git-History-Tool (Conventional Commits)
│
├── 04_agenten/                     # KI-Agenten
│   ├── README.md                   # Agenten-Übersicht
│   ├── ben/                        # Ben-Agent (Rolle/Wissen)
│   │   ├── ben.md                  # Ben-Agent (Rolle/Wissen)
│   │   ├── arbeitslog.md           # Ben-Arbeitsprotokoll
│   │   ├── memory.md               # Ben-Agent Gedächtnis
│   │   └── ben-review-2026-06-23.txt   # Review-Notiz
│   └── luna/                       # Luna (KI-Agent mit eigenem SOUL)
│       ├── readme.md               # Luna-Übersicht
│       ├── SOUL.md                 # Persönlichkeit
│       ├── TOPOLOGY.md             # Topologie-Übersicht
│       ├── config.yaml             # Konfiguration
│       └── memories/
│           ├── memory.md           # System-Wissen
│           └── user.md             # User-Profil
│
├── 05_finanzen/                    # Finanzübersicht
│   └── README.md                   # Finanzprinzipien, Budgets, Quick-Jumps
│
├── 06_systeme/                     # Systeme & Hardware
│   ├── README.md                   # Systeme-Übersicht
│   ├── hardware.md                 # Gerätepark, Tailscale, lokale Ollama-Modelle
│   ├── tailscale-netzwerk.md       # Tailscale-Netz (Hosts, IPs)
│   └── acino-lohn-vorbereitung.md  # Acino Lohn-Vorbereitung
│
├── 07_referenz/                    # Referenzen & Wissen
│   ├── README.md                   # Referenz-Index
│   ├── improvements.md             # Verbesserungen & offene Fragen
│   ├── lessons-learned.md          # Lessons (Git, Agenten, Infra, Acino)
│   └── service-ports.md            # Alle Service-Ports (Mac mini, GX10, etc.)
│
├── 08_arbeit/                      # Arbeitskontext
│   ├── README.md                   # Arbeit-Übersicht
│   ├── acino-job.md                # Acino/Arcera — Arbeitgeber-Job, Themen, Kontakte
│   ├── itintech-firma.md           # Itin TechSolutions, UID, Rechtliches
│   ├── itintech-kunden.md          # Kundenübersicht
│   ├── itintech-kollaborationen.md # Partner & Zusammenarbeit
│   └── itintech-versicherungen.md  # Helvetia, Zurich, AXA etc.
│
├── 09_roboter/                     # Physische Roboter
│   ├── README.md                   # Domänen-MOC
│   └── picrawler/                  # PiCrawler "Manfred die Spinne"
│       ├── readme.md               # Hauptdokumentation (MOC)
│       ├── actions.md              # Bewegungs-Actions
│       ├── camera-detection.md     # Kameradetection
│       ├── hardware-status.md      # Hardware-Status (Servo-Defekte etc.)
│       ├── kinematics.md           # Kinematik & Servo-Steuerung
│       ├── power-protocol.md       # Power-On/Off Protokoll
│       ├── robot-hat-bugs.md       # Known Bugs (Robot HAT)
│       ├── setup.md                # Installation & Setup
│       └── speaker-gpio.md         # GPIO-Speaker-Steuerung
│
├── JustUpdate/                     # Windows-Wartungs-Daten (Vergleiche: Deepseek, Gemini, Chatgpt, Verbessert, Defender, SystemReparatur)
└── _quarantine/                    # NICHT im Vault (per .gitignore ausgeschlossen)
    ├── README.md
    ├── secrets/                    # API-Keys / Bot-Tokens (nie im Vault!)
    ├── code/                       # Python-Utils (nexus_parser, vault_parser)
    └── obsidian/                   # Obsidian-UI-Konfiguration
```

## Datei-Typen

| Typ | Anzahl | Beschreibung |
|-----|--------|-------------|
| **Log-Dateien** | 34 | Wochenlogs, flach (YYYY-WNN.md), append-only (W26 aufgeteilt) |
| **Projekt-Files** | 26 | Projekt-Dokumentation (autos/finanzen/reise/tools/sonstige) |
| **Agenten-Files** | 8 | Ben (3 md + 1 txt) & Luna (4 md/config + 2 memories) |
| **Roboter-Files** | 9 | PiCrawler "Manfred" (picrawler/) |
| **Personen-Files** | 4 | Justin (3), Sarah (1) |
| **Arbeits-Files** | 5 | Firma, Kunden, Acino, Kollaboration, Versicherungen |
| **System-Files** | 3 | Hardware, Tailscale-Netz, Acino-Lohn |
| **Referenz-Files** | 3 | Lessons, Improvements, Service-Ports |
| **Finanz-Files** | 0 | nur Ordner-README |
| **README/Index** | 11 | Root (3) + Ordner-READMEs + INDEX |

## Wichtige Pfade

| Datei | Pfad | Beschreibung |
|-------|------|-------------|
| Hauptindex | `README.md` | Alle Domänen auf einen Blick |
| File Tree | `tree.md` | Diese Datei |
| Log-Index | `01_log/README.md` | Log-Topologie & Workflow |
| Projekt-Index | `03_projekte/INDEX.md` | Portfolio-Übersicht |
| Roboter-MOC | `09_roboter/README.md` | Domänen-Index Roboter |
| Ben memory | `04_agenten/ben/memory.md` | Ben-Agent Gedächtnis |
| Luna SOUL | `04_agenten/luna/SOUL.md` | Luna-Persönlichkeit |
| Hardware | `06_systeme/hardware.md` | Gerätepark |
| Service-Ports | `07_referenz/service-ports.md` | Alle Ports |
| Lessons Learned | `07_referenz/lessons-learned.md` | Lessons |
| Improvements | `07_referenz/improvements.md` | Verbesserungen |
| Acino-Job | `08_arbeit/acino-job.md` | Arbeitgeber-Kontext |
| Finanzen | `05_finanzen/README.md` | Budgets, Investments |
