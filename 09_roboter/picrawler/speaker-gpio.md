---
title: PiCrawler — Speaker-GPIO-Trick
type: reference
status: aktiv
updated: 2026-06-14
description: Lies vor jeder Audio-Wiedergabe am PiCrawler. GPIO 20 HIGH UND GPIO 12 LOW nötig, sonst nur Pop-Geräusch. Operative Spielsequenz hier; Bug-Hintergrund → robot-hat-bugs.
aliases: [speaker-gpio, speaker, gpio-trick, i2s-amp, pinctrl, audio-wiedergabe]
tags: [reference/robotik, picrawler, speaker, gpio, audio]
related: ["[[README|picrawler/README]]", "[[robot-hat-bugs]]", "[[setup]]"]
---

# Speaker-GPIO-Trick

MOC-Rücklink: [[README|picrawler/README]]

Der I²S-Speaker auf dem Robot-HAT spielt **nur** mit dieser GPIO-Kombination:

```bash
pinctrl set 20 op dh   # GPIO 20 = HIGH  (robot_hat setzt das)
pinctrl set 12 op dl   # GPIO 12 = LOW   (robot_hat lässt das aus!)
```

> **Warum reicht der robot_hat-Default nicht?** Fehlendes HAT-EEPROM → robot_hat fällt auf `v4x` (nur GPIO 20) zurück; GPIO 12 LOW fehlt. **→ Bug-Details: [[robot-hat-bugs]]** (Bug 2 + Bug 3). Hier nur die operative Sequenz.

## Korrekte Spielsequenz

```bash
sudo systemctl stop aplay     # /dev/zero-Keepalive blockiert Card 3 exklusiv
pinctrl set 20 op dh
pinctrl set 12 op dl
aplay -D plughw:3,0 /pfad/zur.wav
sudo systemctl start aplay    # optional wieder hoch (hält Amp warm)
```

## Diagnose-Symptome (bevor der Trick gefunden war)

- `aplay`/`speaker-test` melden "RUNNING", `hw_ptr` läuft → Daten fließen
- I²C `0x14` antwortet → HAT hat Strom
- Mixer auf 100% (`PCM`-Control, Card 3)
- **Nur kurze "Pop"-Geräusche** bei GPIO-Transitions, kein Ton
- GPIO 12 auf LOW → voller Ton

## ALSA-Pipeline-Details

- Card 3 = `sndrpihifiberry` (PCM5102A-Overlay)
- `dmixer` (`/etc/asound.conf`) auf **44100 Hz fix** — `speaker-test`-Default 48000 Hz scheitert mit "Rate not available"
- `aplay.service` greift Card 3 **exklusiv** → vor direktem `hw:3,0`-Test stoppen

## Querverweise

[[README|picrawler/README]] · [[robot-hat-bugs]] · [[setup]]

---
> *Quelle: archiv/169.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett; GPIO-Hintergrund NICHT dupliziert → Verweis auf kanonische [[robot-hat-bugs]], hier nur operative Sequenz).*
