---
title: PiCrawler — Kinematik & Servo-Pinout
type: reference
status: aktiv
updated: 2026-06-14
description: Lies VOR jedem Motion-Script. 12 Servos (4 Beine × 3 DOF), IK-Pipeline, sichere Koordinaten-Grenzen, Servo-Limits, Pin-zu-Bein-Mapping aus picrawler.py 2.1.4.
aliases: [kinematics, kinematik, servo-pinout, inverse-kinematik, coord2polar, pin-list]
tags: [reference/robotik, picrawler, kinematik, servo, ik]
related: ["[[README|picrawler/README]]", "[[actions]]", "[[hardware-status]]", "[[power-protocol]]"]
---

# PiCrawler Kinematik

MOC-Rücklink: [[README|picrawler/README]]

> [!warning] Library-Mapping ≠ physische Verkabelung
> Das `PIN_LIST`-Mapping unten ist die **Library-Annahme**. Physisch sind die Servos anders verkabelt → [[hardware-status]]. Bis geklärt keine IK-basierten `do_step`/`do_action`.

## 12 Servos — Pin-zu-Bein-Mapping (Library)

Quelle: `PIN_LIST = [9, 10, 11, 3, 4, 5, 0, 1, 2, 6, 7, 8]` in `~/picrawler/picrawler/picrawler.py`. Library indexiert Servos 0..11 in dieser Reihenfolge, gruppiert zu 4 Beinen × 3 Servos:

| Bein-Index | Servo-Pins (PCA9685) | DOF-Rolle |
|---|---|---|
| Leg 0 | 9, 10, 11 | beta (Hip), alpha (Knee), gamma (Shoulder) |
| Leg 1 | 3, 4, 5 | beta (Hip), alpha (Knee), gamma (Shoulder) |
| Leg 2 | 0, 1, 2 | beta (Hip), alpha (Knee), gamma (Shoulder) |
| Leg 3 | 6, 7, 8 | beta (Hip), alpha (Knee), gamma (Shoulder) |

Achtung: Servo-Output-Reihenfolge ist `[beta, alpha, gamma]`, nicht `[alpha, beta, gamma]` — siehe `do_step` → `set_angle`-Swap.

**Geometrische Bein-Zuordnung** (vorne-links/-rechts, hinten-links/-rechts) nicht eindeutig im Code. Aus dem `sit`-Pattern (Beine 0+3 `Y_DEFAULT=45`, Beine 1+2 `Y_START=0`) folgt nur die Diagonal-Paar-Struktur; konkrete Zuordnung physisch verifizieren (Servo 0 ansteuern, schauen welches Bein zuckt) bzw. [[hardware-status]].

## Link-Längen (mm)

Constants in `Picrawler`-Klasse:

| Symbol | Wert | Bedeutung |
|---|---:|---|
| `A` | 48 mm | Femur (Oberschenkel) |
| `B` | 78 mm | Tibia (Unterschenkel) |
| `C` | 33 mm | Coxa (Schulter-Offset zur Hüfte) |

Reichweite L: `C ≤ L ≤ A+B+C` = 33..159 mm. Außerhalb normalisiert `coord2polar` automatisch.

## Inverse Kinematik (`coord2polar`)

Input `[x, y, z]` (End-Effector relativ zur Schulter-Basis) → Output `[alpha, beta, gamma]` in Grad. Pipeline (`picrawler.py:41-77`):

1. `L = sqrt(x² + y² + z²)`
2. Skaliere `(x,y,z)` falls L < C oder L > A+B+C
3. `w = sqrt(x² + y²)`, `v = w - C`, `u = sqrt(z² + v²)`
4. `u` geclampt auf `[30, 91.58]` — physikalische Obergrenze
5. `beta  = acos((B² + A² - u²) / (2·B·A))` → Knie
6. `alpha = atan2(z, v) + acos((A² + u² - B²) / (2·A·u))` → Hüfte
7. `gamma = atan2(y, x)` → Schulter-Rotation
8. Grad + Offsets: `alpha = 90 - α°`, `beta = β° - 90`, `gamma = -(γ° - 45)`

## Servo-Winkel-Limits (`limit_angle`)

| Winkel | Min | Max | Bedeutung |
|---|---:|---:|---|
| alpha | -90° | 90° | Hüfte vor/zurück |
| beta | -10° | 90° | Knie strecken/beugen |
| gamma | -60° | 60° | Schulter-Rotation um Pi-Z-Achse |

Greift ein Limit, läuft `set_angle` mit `israise=False` über `polar2coord` zurück → **ausgeführte Pose ≠ gewünschte**, `current_coord`-State driftet. Bei `israise=True` → `ValueError`.

## Sicheres Koordinaten-Envelope

Aus `cali_helper_web` (`picrawler.py:236-238`) — einziger Ort mit explizitem Clamp:

| Achse | Min | Max | Bemerkung |
|---|---:|---:|---|
| x | 40 | 80 | "vorne" relativ zur Bein-Basis |
| y | -20 | 20 | seitlich |
| z | -50 | -10 | nach unten (Standhöhe) |

Bewegungen außerhalb dieser Box sind nicht garantiert mechanisch sicher. `wave` (z=60) verlässt die Box bewusst und braucht die anderen Beine als Stütze.

## Pose-Konstanten (`MoveList`-Klasse)

| Konstante | Wert | Verwendung |
|---|---:|---|
| `LENGTH_SIDE` | 77 | Body-Seitenlänge (Square 77×77 mm) |
| `X_DEFAULT` | 45 | normale "vorne-Position" |
| `X_TURN` | 70 | weit-vorne (Turn) |
| `X_START` | 0 | neutral X (Wave) |
| `Y_DEFAULT` | 45 | normale seitliche Position |
| `Y_TURN` | 130 | Push-Up Y |
| `Y_WAVE` | 120 | Wave Y |
| `Y_START` | 0 | neutral Y |
| `Z_DEFAULT` | -50 | **Stand-Höhe** |
| `Z_UP` | -30 | **Sit-Höhe** (höher) |
| `Z_WAVE` | 60 | Bein-in-Luft Wave |
| `Z_TURN` | -40 | Push-Up Hub-Tiefe |
| `Z_PUSH` | -76 | Push-Up unten |

## `do_step` vs `do_action` vs `move_body_absolute`

| Methode | Verhalten |
|---|---|
| `do_step(coord, speed)` | atomare Pose; `coord` = `[[x,y,z]×4]` oder String `"sit"`/`"stand"` |
| `do_action(name, step, speed)` | Sequenz von do_steps für Gangart (`forward`, `wave`, …) |
| `do_single_leg(leg, coord, speed)` | bewegt nur 1 Bein, Rest bleibt auf `current_coord` |
| `move_body_absolute(x, y, z)` | Body-Translation, **alle 4 Füße bleiben am Boden** — **safest** bei broken-leg, sofern defektes Bein nicht über Limit gezwungen wird |

## Querverweise

[[README|picrawler/README]] · [[actions]] · [[hardware-status]] · [[power-protocol]]

---
> *Quelle: archiv/134.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, Tabellen für Limits/Konstanten/Methoden, Verkabelungs-Warnung verlinkt).*
