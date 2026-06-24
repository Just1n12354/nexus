---
title: Nexus — Personal Wiki & Vault
description: Nexus: Justin Itins personal Wiki (Obsidian-Style), 400+ .md-Dateien, 6 nummerierte Ordner (00-80_), System für Lebens- und Arbeitswissen
type: project
status: aktiv
created: 2026-06-25
updated: 2026-06-25
tags: [projekt/nexus, wiki, vault, obsidian, nexus-hardening]
project: nexus
---

# Nexus — Personal Wiki & Vault

## Konzept

Das Nexus-Vault ist das zentrale Wiki für Justin Itins Leben und Arbeit: Personen, Projekte, Systeme, Agenten, Logbücher, Referenzen.

### Struktur (6 nummerierte Ordner)
- 00_Log — Wochen- und Jahres-Logs (2002–2026, ~215 Einträge)
- 10_Personen — Privat & Arbeit (Justin, Sarah, Acino, etc.)
- 20_Projekte — Konzepte und aktive Projekte
- 30_Agenten — KI-Agenten (Robert, Felix, Frank, Bruno, Luna, Claudio, Ben)
- 50_Systeme — Infrastruktur, Ports, Tailscale, Hardware
- 60_Referenz — Rechts, Steuer, Gesetze (Schweizer Quellen)
- 70_Arbeit — ItinTech, Kunden, Finanzen
- 80_Roboter — PiCrawler, Robotik
- archiv — Veraltete/alte Versionen

### Kern-Features
- Wikilinks für Vernetzung (900+ Links)
- YAML-Frontmatter pro Datei (title, type, status, updated, tags)
- Append-only für Logs
- check_vault.py: Frontmatter, Links, Drift-Audit
- pre-commit-Hooks: Persona-Guard, Append-only, Drift
- Obsidian-Style (aber ohne Obsidian-Abhängigkeit)

### Hardening-Phasen
- Phase 1: Vault-Scan + Lint (check_vault.py)
- Phase 2: Meta-Layer-Entfernung (MASTER.md, TREE.md, RULES)
- Phase 3: Ghost-Link-Reparatur (232 Links, 58 Dateien)
- Phase 4: Drift-Geländer (check_nexus.py + pre-commit)
- Phase 5: Log-System auf Jahres-Topologie
- Phase 6: Wissens-Konsolidierung (Itin-TechSolutions → Nexus)

### Status
- Haupt-Vault auf Git-GitHub, Sync über Mac mini/Gaming-PC
- 400+ .md-Dateien, ~900 Wikilinks
- Sehr aktiv gepflegt, 0 stale >90 Tage

→  (Hardening-Philosophie und Tools)
→  (Wissensübernahme aus Itin-TechSolutions-Repo)