---
title: Hermes-Infrastruktur
type: reference
status: aktiv
updated: 2026-07-15
description: Hermes-Agent Config, Gateway, Cron, Modell-Setup
tags: [infra/hermes, gateway, cron]
---

# Hermes-Infrastruktur

## Config
- Config: `/home/justin/.hermes/config.yaml`
- `_config_version`: 33, 717 Zeilen
- Backup/Sync: `/mnt/justnas/Dokumente/Hermesconfig/config.yaml`

## Modell
- `nvidia/Qwen3.6-35B-A3B-NVFP4`
- Provider: "custom"
- Endpoint: `http://localhost:8000/v1` (vLLM, direkt, NICHT über Ollama)
- Port 8001 (100.75.47.118:8001) = Caddy-Auth-Proxy, NICHT der aktive Endpoint

## Gateway-Regel
- Memory (`MEMORY.md`), Plugins und `config.yaml` werden beim GATEWAY-START in den System-Prompt geladen, nicht pro Turn
- Nach jeder Änderung: `hermes gateway restart`
- Ohne Restart läuft der Telegram-Ben mit altem Wissen und altem Code
- **Nebenwirkung**: Nach Reboot ist Ben ~4 Min. nicht nutzbar — vLLM lädt das 35B-Modell, Gateway wartet nicht und wirft `APIConnectionError`

## Cron-Jobs
- **Aktiver Job**: "Tägliches Tagesbriefing" (`bf2b9b234724`)
  - Täglich 06:00, Script `daily_briefing.py`, Modus `no-agent`
  - Inhalt: Wetter, Kalender, Todos, E-Mails, Empfehlungen, Tagesziel, Motivation
- **Entfernt**: "Morgengruss Vordermattweg 10" (`56be73c61b9f`) — erledigt

## Ben-Stand (13.07.2026)
- Reliability: 100% (17/17 Tests)
- Behavior: 100%
- Speed: 8.2s, 435 Tokens, 71 GiB RAM
- Baseline vorher: 80% / 50% / 30.4s / 1815 Tokens / 109 GiB
- **Verbesserung**: +42–45% gesamt
- Skill-Builder: 17/17 E2E-Tests stabil
- **Ziele bis ~20.07.2026**: 7s, 350 Tokens, 65 GiB, Monitoring-Dashboards
- **Langfristig**: Self-Healing, LoRA, Semantic Search, Memory, Planner