---
name: ben-readme
status: aktiv
updated: 2026-06-21
description: "Überblick über den Ben-Agenten-Ordner: Persona, Setup, Memory."
aliases: [ben-readme]
tags: [ai-agents, hermes]
related: ["[[ben]]", "[[ben-setup]]", "[[ben-memory]]"]
---

# Ben (30_Agenten/Ben)

**Ben** = Justins persönlicher Allround-Agent auf dem GB10. Hermes Agent (Nous Research),
lokal auf Ollama `gpt-oss:120b`, erreichbar via Telegram. Voller nexus-Zugriff.

Ben = lokaler **Arbeiter-Agent** auf dem GX10 (Luna = übergeordnete Assistenz-Referenz,
Claude Code = Supervisor/Schichtleiter, Ben = ausführender Arbeiter).

## Dateien
- **[[ben]]** (`ben.md`) — Steckbrief/Rolle (Auftrag, Haltung, Datenquellen, Regeln).
- **[[ben-setup]]** (`SETUP.md`) — Installation + Konfiguration (Modell, Vision, Web, Telegram, Autostart, Keep-Alive).
- **[[ben-arbeitskarte]]** (`ARBEITSKARTE.md`) — **zuerst lesen**: Projektordner, nexus-Struktur, Pfade.
- **[[ben-arbeitslog]]** (`ARBEITSLOG.md`) — Arbeitsprotokoll (Aufgabe/gelesen/geändert/Ergebnis/offen).
- **[[ben-memory]]** (`memory.md`) — persistentes Gedächtnis; Ben hängt Gelerntes an.
- **[[ben-nachtschicht]]** (`NACHTSCHICHT.md`) — Setup-/Test-Historie.
- Der wirksame System-Prompt liegt in `~/.hermes/SOUL.md` (nicht im Repo).

## Kurzfakten
| | |
|---|---|
| Gerät | GB10 / DGX Spark, Host `gx10-bf12` |
| Modell | Ollama `gpt-oss:120b` (lokal, `localhost:11434`) |
| Kanal | Telegram `@Benitintech_bot`, Allowlist User `7856421425` |
| Token | `30_Agenten/APIKeys/Telegram-Ben.txt` (im privaten Repo) |
| Hermes | v0.17.0, `~/.hermes/`, systemd-User-Dienst `hermes-gateway` (enabled, linger) |
| Status | **läuft** — lokales Modell + Telegram + Autostart verifiziert 2026-06-21 (siehe [[ben-setup]]) |
