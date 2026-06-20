---
title: PiCrawler — Power-Protokoll
type: reference
status: aktiv
updated: 2026-06-14
description: Lies vor jeder Servo-Aktion am PiCrawler. Manuelle Power-Toggle-Regeln, sit-first-Pflicht, Trennung Pi-Power vs. Servo-Power vs. Speaker/Kamera.
aliases: [power-protocol, power-protokoll, servo-power, sit-first, picrawler-power]
tags: [reference/robotik, picrawler, power, safety, servo]
related: ["[[README|picrawler/README]]", "[[hardware-status]]", "[[setup]]", "[[actions]]"]
---

# Power-Protokoll

MOC-Rücklink: [[README|picrawler/README]]

PiCrawler-Servos sind standardmäßig **AUS**. Justin schaltet die Servo-Power manuell ein, erst wenn klar ist, welches Kommando als erstes läuft.

> [!danger] Erste Aktion bei Servo-Power ON: immer `sit`
> `crawler.do_step("sit", 40)` — nie `stand`/`forward` zuerst. Zusätzlich: 1 Bein defekt → keine Multi-Bein-Gänge ([[hardware-status]]).

## Power-Topologie

Der Robot-HAT hat einen **eigenen Schalter für Servo-/Motor-Power**, unabhängig vom Pi-Strom:

| Schalterzustand | Wirkung | Sicher für |
|---|---|---|
| "Roboter aus" | Servos aus, Pi läuft weiter | Reboots, Installs, File-Writes |
| "Pi aus" | beides aus | nur Hardware-Wartung |

Bei Reboots ohne Servo-Zucken: erst Servo-Switch flippen, Pi läuft weiter.

## Regeln

1. **Setup, Imports, Dry-Runs immer mit Servo-Power OFF.** `i2cdetect -y 1` zeigt dann **kein** Gerät bei `0x14` — erwartet.
2. **Vor "Power on" das erste Kommando ansagen** (z.B. "ich starte mit `sit`").
3. **Default-First-Action bei Servo-Power ON: `crawler.do_step("sit", 40)`** — nie `stand`/`forward`.
4. **Test-Scripts so wrappen**, dass Ctrl+C / Exception in `sit` enden, nicht in `stand`/`hold-pose`.

## Speaker / Kamera brauchen KEINE Servo-Power

I²S-Speaker und CSI-Kamera sind eigene Sub-Systeme. Audio-Tests + Kamera-Diagnose laufen mit Servo-Power OFF. Bei Unsicherheit Justin fragen: "Robot-Power" vs. "Pi-Power" vs. "Servo-Power".

## Hardware-Sicherheits-Layer

> [!warning] 1 Bein mechanisch defekt (Pin 11) — siehe [[hardware-status]]
> Auch mit Power-ON: keine Multi-Bein-Gänge bis repariert. `sit` bleibt sicher.

## Querverweise

[[README|picrawler/README]] · [[hardware-status]] · [[setup]] · [[actions]]

---
> *Quelle: archiv/152.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, sit-first als Danger, Defekt-Bein-Warnung verlinkt).*
