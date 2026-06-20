---
title: Roboter — Domänen-MOC
type: index
status: aktiv
updated: 2026-06-14
description: Einstiegspunkt (MOC) für alle Roboter-Projekte. Aktuell ein aktives System: PiCrawler "Manfred" (SunFounder Quadruped auf Raspberry Pi).
aliases: [roboter, robots, robotik, 80_Roboter]
tags: [domain/robotik, moc, index]
related: ["[[picrawler/README]]", "[[network-tailscale]]", "[[network-tailscale]]", "[[TREE]]"]
---

# Roboter — Domänen-MOC

> Domänen-Index für physische Roboter-Hardware. Detail-Wissen liegt pro System in Unterordnern.

## Aktive Systeme

| System | Typ | Host | Status | Stem |
|---|---|---|---|---|
| PiCrawler "Manfred die Spinne" | Quadruped, 12 Servos (4×3 DOF) | `JustinRasperryPI4` ([[network-tailscale]]) | **aktiv** (1 Bein defekt, Kamera offen) | [[picrawler/README]] |

## Sicherheits-Kurzregeln (PiCrawler)

- **Vor jedem Motion-Script:** [[picrawler/hardware-status]] lesen — Servo Pin 11 (Vorne-Links Fuß) defekt.
- **Erste Aktion bei Servo-Power ON:** `crawler.do_step("sit", 40)` — nie `stand`/`forward`. Siehe [[picrawler/power-protocol]].
- **Verkabelung weicht von Library-`PIN_LIST` ab** → nur Single-Servo-Befehle bis geklärt.

## Querverweise

[[picrawler/README]] · [[network-tailscale]] · [[network-tailscale]] · [[TREE]]

---
> *Quelle: neu angelegt 2026-06-14 (Domänen-MOC für 80_Roboter, verweist auf picrawler/README).*
