---
title: Service-Ports
type: reference
status: aktiv
updated: 2026-06-25
description: Alle Ports und URLs der laufenden Dienste auf den Geräten.
---

# Service-Ports

## Mac mini (100.89.217.4)

| Service | Port | Status |
|---------|------|--------|
| JustTodo | 8030 | live |
| JustFinancePrivate | 8020 | live |
| JustFinanceBusiness | 8010 | live |
| JustReise | 8060 | live |
| JustLauncher | 8000 | geplant |
| JustSavegame | 5077 | live |
| Hermes | 9000 | noch nicht live |
| AIWorld | 9000 | tot (friedhof) |
| ClaudeSync | 9000 | tot (friedhof) |

## GX10 (100.75.47.118)

| Service | Port | Status |
|---------|------|--------|
| Ollama | 11434 | live |
| 126 Ollama-Modelle | 1.4 TB | installiert |

## Gaming-PC

| Service | Port | Status |
|---------|------|--------|
| ClaudeEyes | - | live |
| OpenSSH | 22 | Tailscale-only |

## Raspberry Pi 5 (100.119.30.59)

| Feature | Wert |
|---------|------|
| Picrawler Servos | 12 (4 Beine × 3 DOF) |
| Vosk DE | small-DE-Modell (92 MB) |
| Pin 11 | defekt |
| OV5647 Cam | antwortet nicht (Kabel-Problem?) |

## Netzwerk

* Tailscale = privates Netz, KEIN Internet
* Tailscale-MagicDNS aktiv (Mac mini, NAS, etc.)