---
name: ben-arbeitskarte
status: aktiv
updated: 2026-06-21
description: "Bens Arbeitskarte: Projektordner, nexus-Struktur, Memory-/Log-/Hardware-Pfade. Ben liest das ZUERST bei Projekt-/Wissensfragen, statt zu raten."
aliases: [ben-arbeitskarte, ben-projekte]
tags: [ai-agents, hermes, nexus, routing]
related: ["[[ben]]", "[[ben-setup]]", "[[ben-memory]]", "[[ben-arbeitslog]]"]
---

# Ben — Arbeitskarte (zuerst lesen)

Bei Projekt-, Pfad- oder Wissensfragen: **zuerst hier nachsehen**, dann die konkrete
Datei laden. Nicht raten, nicht alles auf einmal laden.

## Geräte-Kontext
- Host `gx10-bf12` (ASUS Ascent GX10 / NVIDIA DGX Spark GB10), Ubuntu, aarch64.
- Hauptmodell `gpt-oss:120b` (lokal, Ollama, keep-alive Forever). Augen: `qwen2.5vl:7b`.

## nexus-Vault — Justins Wissensbasis
Wurzel: `~/Documents/GitHub/nexus/` (= `~/Dokumente/GitHub/nexus/`)

| Ordner | Inhalt |
|--------|--------|
| `00_Log/<Jahr>/KW_NN/LOG.md` | Wochen-Logs (was wann gemacht wurde) |
| `20_Projekte Konzepte/` | Projekt-Konzepte (`INDEX.md` als Einstieg) |
| `30_Agenten/` | KI-Agenten — **Bens eigener Ordner: `30_Agenten/Ben/`**; Keys in `30_Agenten/APIKeys/` |
| `50_Systeme/hardware.md` | Geräte, Hostnames, Tailscale-IPs, OS, Rollen |
| `70_Arbeit/` | Firma/Arbeit (ItinTech, Acino, Versicherungen) |
| `80_Roboter/` | PiCrawler u. a. Robotik |

## Bens eigene Dateien (`30_Agenten/Ben/`)
- `ben.md` — Steckbrief/Rolle · `SETUP.md` — Technik · `README.md` — Übersicht
- `memory.md` — Gelerntes (datierte Fakten) · `ARBEITSLOG.md` — Arbeitsprotokoll
- `ARBEITSKARTE.md` — diese Datei · `NACHTSCHICHT.md` — Setup-Historie

## Projektordner (Itin-TechSolutions)
Wurzel: `~/Documents/GitHub/Itin-TechSolutions/`
Aktive Apps unter `20_Projekte/10_Apps/`: AIEyes, AI Fight Club, ClaudeSync, Jarvis,
JustBetter, JustFinanceBusiness, JustFinancePrivate, JustLauncher, JustReise,
JustSavegame, JustTodo, JustUpdate, JustWebsite, ProjectNorm, Sherlock Holmes, SwissAISolutions.

→ Vor Arbeit an einer App: deren `README`/`CHANGELOG`/`TODO` + `src/` lesen, dann handeln.

## Weitere Repos auf dem Gerät
`~/Documents/GitHub/`: Acino, JorllyJustinTransfer, PrivateBackup, itintechsolutionswebsite,
rack-viewer (+ nexus, Itin-TechSolutions).

## Hermes/Ben-Technik (NICHT in Git)
- Config: `~/.hermes/config.yaml` · Secrets: `~/.hermes/.env` · Identität: `~/.hermes/SOUL.md`
- Logs: `~/.hermes/logs/{gateway,agent,errors}.log`
- Dienst: `systemctl --user {status|restart} hermes-gateway`

## Wo NICHT ohne Auftrag rein
- `30_Agenten/APIKeys/`, `~/.hermes/.env`, NAS-Share `/mnt/justnas/Connect/` (Zugangsdaten) —
  nur lesen, wenn die Aufgabe es klar verlangt; nie Inhalte in Antworten/Logs/Memory ausgeben.
