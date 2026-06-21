---
name: ben-memory
status: aktiv
updated: 2026-06-21
description: "Bens persistentes Gedächtnis — datierte Fakten/Präferenzen, die Ben über Justin und sein Setup gelernt hat. Ben hängt hier selbst an."
aliases: [ben-memory]
tags: [ai-agents, hermes, memory]
related: ["[[ben]]", "[[ben-setup]]"]
---

# Ben — Gedächtnis

> Ben hängt hier datierte Einträge an (Lern-Pflicht, siehe [[ben]]). Ein Fakt pro Block,
> knapp und prüfbar. **Keine Secrets/Tokens hier** — die liegen in `APIKeys/`.

## Einträge

- 2026-06-21 — Ben angelegt: persönlicher Allround-Agent auf dem GB10, lokal auf
  Ollama `gpt-oss:120b`, erreichbar via Telegram (eigener Bot). Justins Telegram-User-ID
  für die Allowlist: `7856421425`.
- 2026-06-21 — Hermes v0.17.0 installiert und verifiziert: lokales Modell läuft
  (provider=custom → Ollama `/v1`), Telegram-Bot `@Benitintech_bot` verbunden, Gateway
  als systemd-User-Dienst mit Boot-Autostart (linger). Details: [[ben-setup]].
