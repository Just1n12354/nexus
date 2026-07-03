---
title: PiCrawler — Setup-Stand
type: reference
status: aktiv
updated: 2026-06-14
description: Lies bei Frage zu installierten PiCrawler-Paketen, Source-Pfaden oder ob Setup erneut nötig ist. Quick-Check spart 100+ MB Re-Download. Python-3.13/Debian-13-Caveats.
aliases: [setup, setup-stand, picrawler-setup, installation, quick-check]
tags: [reference/robotik, picrawler, setup, installation, python]
related: ["[[README|picrawler/README]]", "[[speaker-gpio]]", "[[power-protocol]]", "[[robot-hat-bugs]]", "[[camera-detection]]"]
---

# Setup-Stand (Stand 2026-05-25)

MOC-Rücklink: [[README|picrawler/README]]

Installation auf dem Pi am 2026-05-25 durchgeführt. Bewegung verifiziert: `crawler.do_step(...)` bewegt die Servos auf dieser Hardware.

## Installierte Pakete

| Paket | Version | Source-Dir (Runtime) |
|---|---|---|
| `robot_hat` | 2.3.6 | `~/robot-hat` |
| `vilib` | 0.3.18 | `~/vilib` |
| `picrawler` | 2.1.4 | `~/picrawler` |
| `sunfounder_controller` | 0.0.2 | `~/sunfounder-controller` |

Dist-Pfad für Patches (Runtime): `/usr/local/lib/python3.13/dist-packages/<paket>/`.

## Quick-Check (vor Re-Install IMMER zuerst)

```bash
python3 -c "from picrawler import Picrawler; from robot_hat import Servo; import vilib"
```

Läuft das ohne Error → alles installiert, **nicht** neu klonen. Anpassungen lieber in `~/`-Source-Repos editieren (oder dist-packages hot-patchen).

## Audio (i2samp.sh-Artefakte bereits vorhanden)

`~/picrawler/i2samp.sh` gelaufen. Resultat (Runtime-Pfade):
- `/etc/asound.conf` mit `speakerbonnet` + `dmixer` (Card 3, 44100 Hz fix)
- `aplay.service` aktiv (spielt `/dev/zero`, hält Amp warm) — **blockiert Card 3 exklusiv**
- `auto_sound_card.service` (oneshot)
- Overlays in `/boot/firmware/config.txt`: `hifiberry-dac`, `i2s-mmap`

Aber: Speaker spielt nur mit zusätzlichem GPIO-Trick → [[speaker-gpio]] (Ursache: [[robot-hat-bugs]]).

## Python 3.13 / Debian 13 — Caveats

- `mediapipe` und `tflite-runtime` haben **keine aarch64-Wheels** für Py3.13 → übersprungen. **AI-Vision in vilib geht nicht**; Basis-Kamera-Streaming geht (sobald Kamera detektiert, [[camera-detection]]).
- `pip install` braucht `--break-system-packages` (PEP 668). SunFounder-`install.py` handhabt das automatisch.
- `i2samp.sh` gelaufen, aber `i2s-amp`-Test-Stelle hatte interaktive Prompts.

## System-Konfiguration

- I²C + SPI aktiv in `/boot/firmware/config.txt`
- User `pi` in Gruppen: `gpio`, `i2c`, `spi`
- I²C-Bus 1: Robot-HAT-MCU bei `0x14` (sichtbar bei Servo-Power ON → [[power-protocol]])

## Querverweise

[[README|picrawler/README]] · [[speaker-gpio]] · [[power-protocol]] · [[robot-hat-bugs]] · [[camera-detection]]

---
> *Quelle: archiv/167.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, Runtime-Pfade markiert, Querverweise erweitert).*
