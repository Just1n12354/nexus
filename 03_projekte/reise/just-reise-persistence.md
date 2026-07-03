---
title: JustReise — Launchd-Config
type: note
status: aktiv
updated: 2026-06-25
description: launchd-Plist für JustReise (Flask, Port 8060). Pfade 2026-06-25 korrigiert.
tags: [infra, justreise, launchd, flask]
---

# JustReise — launchd-Config

> Port 8060 auf Mac mini (100.89.217.4)

## launchd-Plist

**Pfad:** `~/Library/LaunchAgents/com.itintechsolutions.justreise.plist`

**Status:** 2026-06-25 korrigiert — alte Pfade `/Users/imjustin/JustReise/*` durch neue `~/Documents/GitHub/Itin-TechSolutions/20_Projekte/10_Apps/JustReise/Code/*` ersetzt.

## Pfade

| Variable | Pfad |
|----------|------|
| **Executable** | `/opt/homebrew/bin/python3` |
| **App-File** | `/Users/imjustin/Documents/GitHub/Itin-TechSolutions/20_Projekte/10_Apps/JustReise/Code/src/app.py` |
| **WorkingDirectory** | `/Users/imjustin/Documents/GitHub/Itin-TechSolutions/20_Projekte/10_Apps/JustReise/Code` |
| **London-Dir** | `/Users/imjustin/Documents/GitHub/Itin-TechSolutions/20_Projekte/10_Apps/JustReise/Code/data/london` |

## Port

- **Port:** 8060
- **ENV:** `JUSTREISE_PORT=8060`
- **Status:** ✅ LIVE (200 OK, 2026-06-25 07:06 UTC)

## Bekannte Fehler

- **Exit 78 (2026-06-24 → 2026-06-25):** Plist-Pfad falsch (`/Users/imjustin/JustReise/app.py` existierte nicht)
- **Fix:** `perl -i -pe 's|/Users/imjustin/JustReise|...|' Plist`

## Verweise

- [[03_projekte/justreise.md|JustReise]]
- [[06_systeme/tailscale-netzwerk.md|Tailscale-Netzwerk]]
- [[07_referenz/service-ports.md|Service-Ports]]