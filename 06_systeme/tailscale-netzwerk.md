---
title: Tailscale-Netzwerk
type: reference
status: aktiv
updated: 2026-06-25
description: Tailscale-MagicDNS und IP-Adressen aller Geräte im privaten Netzwerk.
tags: [infra, netscale, tailscale, magicdns]
---

# Tailscale-Netzwerk

> Eigenes Tailscale-Netzwerk mit MagicDNS (tail8b5081.ts.net)

## Geräte-Übersicht

| 1 | **macmini** | 1 001 272 806 | 100.89.217.4 | `macmini.tail8b5081.ts.net` | 22 | `ssh imjustin@macmini.tail8b5081.ts.net` |
| 2 | **macairm4** | 1 537 221 056 | 100.119.74.63 | `justinmacairm4.tail8b5081.ts.net` | 22 | `ssh <user>@justinmacairm4.tail8b5081.ts.net` |
| 3 | **justnas** | n/a | 100.122.172.62 | `justnas.tail8b5081.ts.net` | 22 | `ssh JustinNAS@justnas.tail8b5081.ts.net` |
| 4 | **gx10** | 1 787 907 288 | 100.75.47.118 | `gx10.tail8b5081.ts.net` | 22 | `ssh justin@gx10.tail8b5081.ts.net` |
| 5 | **justpc** | 1 913 259 152 | 100.94.200.83 | `justpc.tail8b5081.ts.net` | 22 | `ssh jitin@justpc.tail8b5081.ts.net` |
| 6 | **justlaptop** | n/a | 100.117.38.122 | `justlaptop.tail8b5081.ts.net` | 22 | `ssh <user>@justlaptop.tail8b5081.ts.net` |
| 7 | **sarahpc** | n/a | 100.114.201.107 | `sarahgamingpc.tail8b5081.ts.net` | 22 | `ssh <user>@sarahgamingpc.tail8b5081.ts.net` |
| 8 | **s24-von-justin** | n/a | 100.65.158.30 | `s24-von-justin.tail8b5081.ts.net` | n/a | n/a |
| 9 | **s21-von-sarah** | n/a | 100.94.50.21 | `s21-von-sarah.tail8b5081.ts.net` | n/a | n/a |

## Netzwerk-Info

- **MagicDNS-Suffix:** `.tail8b5081.ts.net`
- **Typ:** Privates Tailscale-Netzwerk (home setup)
- **Geräte mit SSH:** macmini, macairm4, justnas, gx10, justpc, justlaptop, sarahpc
- **Geräte ohne SSH (Mobile):** s24-von-justin, s21-von-sarah

## Schnelle SSH-Befehle

```bash
# Mac mini (Hermes Server)
ssh imjustsin@macmini.tail8b5081.ts.net

# GX10 (Ben-Host)
ssh justin@gx10.tail8b5081.ts.net

# Synology NAS
ssh JustinNAS@justnas.tail8b5081.ts.net

# MacBook Air M4
ssh <user>@justinmacairm4.tail8b5081.ts.net

# JustPC (Gaming-PC, vormals justmain)
ssh jitin@justpc.tail8b5081.ts.net

# JustLaptop
ssh <user>@justlaptop.tail8b5081.ts.net

# Sarahs GamingPC
ssh <user>@sarahgamingpc.tail8b5081.ts.net
```

## Verweise

- [[06_systeme/hardware.md|Hardware]] — Gerätelisten und Specs
- [[06_systeme/README.md|50_Systeme]] — Infrastruktur-Übersicht