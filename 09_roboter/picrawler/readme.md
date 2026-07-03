---
title: PiCrawler — Stem (Manfred die Spinne)
type: domain
status: aktiv
updated: 2026-06-14
description: MOC für SunFounder PiCrawler "Manfred" (Quadruped, 12 Servos) auf Raspberry Pi. Einstieg zu Setup, Power, Hardware-Status, Kinematik, Actions, Speaker, Kamera, robot_hat-Bugs. Vor jedem Motion-Script Hardware-Status lesen.
aliases: [picrawler, Manfred, "Manfred die Spinne", spinne, quadruped, sunfounder-picrawler]
tags: [domain/robotik, picrawler, raspberry-pi, servo, moc]
related: ["[[README|09_roboter/README]]", "[[setup]]", "[[power-protocol]]", "[[hardware-status]]", "[[kinematics]]", "[[actions]]", "[[speaker-gpio]]", "[[camera-detection]]", "[[robot-hat-bugs]]", "[[network-tailscale]]"]
---

# PiCrawler — "Manfred die Spinne"

MOC-Rücklink: [[README|09_roboter/README]]

Quadruped-Roboter von SunFounder, montiert auf Raspberry Pi. Hostname `JustinRasperryPI4` ([[network-tailscale]]). Persona-Name in Sprach-Demos: **Manfred die Spinne**.

> [!danger] Vor JEDEM Motion-Script lesen
> 1 Bein mechanisch defekt (Servo **Pin 11**, Vorne-Links Fuß) + physische Verkabelung weicht von Library-`PIN_LIST` ab. → [[hardware-status]] · [[actions]]. Bis geklärt: **nur Single-Servo-Befehle**, kein `do_step`/`do_action`.

> [!warning] PRÜFEN: Status offen seit 2026-05-25
> Hostname/Modell-Inkonsistenz: SoT [[network-tailscale]] führt `JustinRasperryPI4` als **Raspberry Pi 5 Model B (8 GB)**, die PiCrawler-Quellen sagen durchgängig **Pi 4 Model B Rev 1.1**. Relevant für CSI-Ribbon-Polung/Overlay ([[camera-detection]]). Physisch am Gerät verifizieren, dann SoT oder Roboter-Notizen korrigieren.

## Hardware-Stack

| Komponente | Wert |
|---|---|
| Board | Pi 4 Model B Rev 1.1 *(PRÜFEN: SoT sagt Pi 5, s.o.)*, Debian 13 trixie aarch64, Kernel 6.18.29+rpt-rpi-v8 |
| HAT | SunFounder Robot HAT — 12 Servos (4 Beine × 3 DOF) + I²S-Speaker (PCM5102A) + OV5647-CSI-Anschluss + Ultraschall-Port + Mikrofon |
| Robot-HAT-MCU | I²C `0x14` (nur sichtbar bei Servo-Power ON) |
| Audio | Card 3 `sndrpihifiberry` (Hifiberry-Overlay) |
| Servo-Kalibrierung | Runtime `/opt/picrawler/picrawler.config` **leer (0 bytes)** → Defaults, keine Offsets. Bei Bedarf `examples/calibration/calibration.py` |

Runtime-Pfade auf dem Pi (markiert): `~/` = Home `pi`, `/boot/firmware/`, `/opt/picrawler/`, `/usr/local/lib/python3.13/dist-packages/`.

## Software-Stack (Source-Repos, Runtime-Pfade)

| Paket | Version | Source (Runtime) |
|---|---|---|
| `robot_hat` | 2.3.6 | `~/robot-hat` |
| `vilib` | 0.3.18 | `~/vilib` |
| `picrawler` | 2.1.4 | `~/picrawler` (Examples: `~/picrawler/examples/`) |
| `sunfounder_controller` | 0.0.2 | `~/sunfounder-controller` |

Test-Skript (Runtime): `/home/pi/picrawler_test.py` (selftest | keyboard | single-action).

## Detail-Notizen

| Notiz | Inhalt |
|---|---|
| [[setup]] | Installationszustand, Pfade, Python-3.13-Caveats |
| [[power-protocol]] | Servo-Strom-Workflow, `sit`-first-Pflicht |
| [[hardware-status]] | Defekt-Stand pro Bein/Sensor (kaputtes Bein Pin 11) |
| [[kinematics]] | 12-Servo-Pinout, Inverse Kinematik, Bein-Workspace, Limits |
| [[actions]] | Built-in Gaits + preset_actions, Sicherheit bei defektem Bein |
| [[speaker-gpio]] | I²S-Amp-GPIO-Trick (kurz; Bug-Details → [[robot-hat-bugs]]) |
| [[camera-detection]] | OV5647 antwortet nicht auf I²C (offen) |
| [[robot-hat-bugs]] | **Kanonische Bug-Liste** robot_hat 2.3.6 (TTS, Speaker, EEPROM) |

## TTS-Setup (kurz)

`robot_hat.TTS` ist kaputt → Bug-Details: [[robot-hat-bugs]]. Direkt nutzen:

```bash
# espeak (schnelle Tests)
espeak -v de "Text" --stdout | aplay -D plughw:3,0
# Piper (natürliche Stimme, Thorsten-medium in ~/piper-voices/)
echo "Text" | piper --model ~/piper-voices/thorsten-medium.onnx --output_file /tmp/x.wav
aplay -D plughw:3,0 /tmp/x.wav
```

Audio-Wiedergabe braucht zusätzlich den GPIO-Trick → [[speaker-gpio]].

## Querverweise

[[README|09_roboter/README]] · [[setup]] · [[power-protocol]] · [[hardware-status]] · [[kinematics]] · [[actions]] · [[speaker-gpio]] · [[camera-detection]] · [[robot-hat-bugs]] · [[network-tailscale]]

---
> *Quelle: archiv/48.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, Tabellen, Runtime-Pfade markiert, Pi4/Pi5-Drift + defektes-Bein-Danger geflaggt).*
