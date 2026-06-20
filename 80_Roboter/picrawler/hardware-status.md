---
title: PiCrawler — Hardware-Status
type: reference
status: aktiv
updated: 2026-06-14
description: Lies vor JEDEM Motion-Kommando am PiCrawler. Aktueller Defekt-Stand pro Bein/Sensor/Aktor + physische Pin-Verkabelung. Definiert welche Gangarten sicher sind.
aliases: [hardware-status, defekt-status, picrawler-status, broken-leg, pin-11]
tags: [reference/robotik, picrawler, hardware, safety, defekt]
related: ["[[README|picrawler/README]]", "[[power-protocol]]", "[[speaker-gpio]]", "[[camera-detection]]", "[[actions]]", "[[kinematics]]"]
---

# Hardware-Status

MOC-Rücklink: [[README|picrawler/README]]

> [!danger] Vor jedem Motion-Script lesen — Stand 2026-05-25
> Servo **Pin 11** (Vorne-Links, Fuß/Knie) defekt **und** physische Verkabelung folgt nicht der Library-`PIN_LIST`. → bis geklärt **nur** direkte Single-Servo-Befehle, kein `do_step`/`do_action`.

## Stand 2026-05-25

| Komponente | Status | Notiz |
|---|---|---|
| **12× Servos (4 Beine × 3 DOF)** | ❌ **Pin 11 defekt (Vorne-Links, Fuß-Ende)** | Physische Pin-Karte (`Roboter.jpg`) erstellt; defekter Servo eindeutig **Pin 11**. Verkabelung folgt NICHT der Library-Gruppierung — siehe Tabelle unten. |
| I²S-Speaker (PCM5102A) | ✅ funktioniert | Braucht GPIO-Trick → [[speaker-gpio]] |
| Audio-Pipeline (ALSA) | ✅ konfiguriert | `aplay.service` läuft permanent, blockiert Card 3 exklusiv |
| CSI-Kamera (OV5647) | ❌ I²C-No-Response | Sensor antwortet nicht — Kabel/Polarität prüfen → [[camera-detection]] |
| I²C Robot-HAT MCU (`0x14`) | ✅ erreichbar bei Servo-Power | |
| HAT-EEPROM (`/proc/device-tree/hat*`) | ❌ fehlt | robot_hat fällt auf v4x-Defaults zurück → [[robot-hat-bugs]] |

> [!warning] PRÜFEN: Offene Hardware-Probleme seit 2026-05-25
> Defektes Bein (Pin 11) und Kamera (OV5647) sind beide noch offen. Bei Reparatur Tabelle + `updated:` aktualisieren.

## Erlaubte Aktionen bei aktuellem Status

✅ **Sicher:**
- `crawler.do_step("sit", 40)` — alle Beine am Boden, geringe Last
- `crawler.do_single_leg(...)` auf einem **bekannt heilen** Bein
- Speaker-Wiedergabe (espeak/Piper → `aplay -D plughw:3,0`)
- Body-Sway via `move_body_absolute(x,y,z)` mit kleiner Amplitude (≤20 mm) — alle Füße am Boden
- Built-in `dance` (nicht Custom-Wave!) — basiert auf `move_body_absolute`, Body-Sway ohne Lift

❌ **Nicht ohne Reparatur:**
- `forward`, `backward`, `turn left/right` — Multi-Bein-Lift-Gänge
- `wave`, `shake_hand`, `fighting`, `push_up` — heben Beine (push_up klappt Knie aktiv!)
- `stand` — Knie muss Last halten, defekter Servo gibt nach
- `excited`, `nod` — Z-Variation belastet defektes Gelenk
- Selbst-geschriebene Wave-Scripts mit Z-Lift (siehe `manfred_dance.py`-Incident 2026-05-25, [[../../00_Log/2026/KW_22/LOG|KW_22-Log]])

**Knie-Defekt-Warnung:** Auch statische Posen erfordern, dass das Knie Bein-Eigengewicht + Body-Last hält. Mechanisch defektes Knie gibt unter Last nach → Body kippt. Elektrisch defekter Servo verharrt im letzten/zufälligen Winkel.

## Physische Pin-Verkabelung (Stand 2026-05-25, aus `Roboter.jpg`)

Von Körper-Anschluss zum Fuß, pro Bein:

| Joint-Position | Vorne-Links (A) | Vorne-Rechts (B) | Hinten-Rechts (C) | Hinten-Links (D) |
|---|---|---|---|---|
| Körper (Schulter γ?) | Pin 5 | Pin 3 | Pin 8 | Pin 2 |
| Mitte (Hüfte α?) | Pin 4 | Pin 10 | Pin 7 | Pin 1 |
| Fuß (Knie β?) | **Pin 11 (DEFEKT)** | Pin 9 | Pin 6 | Pin 0 |

## ⚠ Verkabelungs-Diskrepanz zur Library

Library `PIN_LIST = [9, 10, 11, 3, 4, 5, 0, 1, 2, 6, 7, 8]` gruppiert in 3er-Blöcken als Library-Leg 0..3. Physisch liegen aber z.B. Pin 11 an Vorne-Links und Pin 9, 10 an Vorne-Rechts — die Library nimmt an, dass 9/10/11 alle zum selben Bein (Leg 0) gehören. **Konsequenz:** `do_step([leg0, leg1, leg2, leg3])` koordiniert nicht das physische Bein, das die Library als "leg 0" denkt. Das erklärt vermutlich die Eskalation des `manfred_dance.py`-Incidents (2026-05-25): kreuzweise verkabelte Servos quer durch alle 4 physischen Beine.

**Offene Fragen (späteres Testen):**
- Skizzen-Zuordnung exakt oder Annäherung?
- Joint-Funktion (Schulter/Hüfte/Knie) pro physischer Position? Typisch 3-DOF: Body=Schulter (γ), Mitte=Hüfte (α), Fuß=Knie (β).
- Servo-Reihenfolge pro Bein wie Library erwartet (β-α-γ) oder anders?

**Sichere Bewegung bis geklärt:** **NUR** direkte Single-Servo-Befehle (`Servo(pin).angle(...)` ohne `Picrawler()`-IK). Kein `do_step`/`do_action`. Action-Klassifikation komplett: [[actions]].

## Update-Workflow

- Bei Reparatur: Justin nennt gefixtes Bein → diese Datei + `updated:` aktualisieren.
- Verifikations-Sequenz nach Repair: `sit` → `stand` (kurz halten) → `sit`.
- Sobald alles heil: Defekt-Liste leeren, Tabelle auf "alle ✅", Danger-Callout entfernen.

## Querverweise

[[README|picrawler/README]] · [[power-protocol]] · [[speaker-gpio]] · [[camera-detection]] · [[actions]] · [[kinematics]]

---
> *Quelle: archiv/116.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, Danger/PRÜFEN-Marker für defektes Bein + offene Probleme, Log-Link korrigiert auf 2026/KW_22).*
