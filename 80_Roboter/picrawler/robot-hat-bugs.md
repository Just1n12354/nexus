---
title: PiCrawler — robot_hat Bugs (kanonisch)
type: reference
status: aktiv
updated: 2026-06-14
description: Kanonische Bug-Liste für robot_hat 2.3.6 auf dem PiCrawler. Warum robot_hat.TTS, enable_speaker() und HAT-Erkennung scheitern — mit Pfaden, Ursache, Workaround, Patch.
aliases: [robot-hat-bugs, robot_hat-bugs, is_installed-bug, tts-bug, enable_speaker-bug]
tags: [reference/robotik, picrawler, robot_hat, bug, workaround]
related: ["[[README|picrawler/README]]", "[[speaker-gpio]]", "[[setup]]", "[[hardware-status]]"]
---

# robot_hat — bekannte Bugs (Version 2.3.6)

MOC-Rücklink: [[README|picrawler/README]]

> Kanonische Bug-Sammlung für robot_hat. GPIO-Speaker-Bedienung steht hier (Bug 2); [[speaker-gpio]] hält nur die operative Spielsequenz kurz und verweist hierher.

## Bug-Übersicht

| # | Bug | Symptom | Workaround |
|---|---|---|---|
| 1 | `run_command()` Race → `is_installed()` immer False | `robot_hat.TTS()` wirft "… is not installed" trotz installiertem Binary | TTS direkt aufrufen / Patch |
| 2 | `enable_speaker()` setzt nur GPIO 20 | Amp stumm (nur Pop) | zusätzlich GPIO 12 LOW → [[speaker-gpio]] |
| 3 | HAT-Erkennung scheitert ohne EEPROM | Fallback auf `robot_hat_v4x` (`spk_en=20`) — passt nicht 100% | manuell GPIO 12 LOW (Bug 2) |

## Bug 1: `run_command()` Race-Condition

Pfad (Runtime): `~/robot-hat/robot_hat/utils.py` bzw. `/usr/local/lib/python3.13/dist-packages/robot_hat/utils.py`

```python
def run_command(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    result = p.stdout.read().decode('utf-8')
    status = p.poll()        # ← None, wenn Prozess noch nicht beendet
    return status, result

def is_installed(cmd):
    status, _ = run_command(f"which {cmd}")
    if status in [0, ]:      # status ist None → False
        return True
    return False
```

`p.poll()` ohne vorheriges `p.wait()` liefert meist `None` → `is_installed()` fast immer False, auch wenn das Kommando existiert.

**Folge:** `robot_hat.TTS()` wirft `"TTS engine: pico2wave is not installed."` obwohl `which pico2wave` → `/usr/bin/pico2wave`.

**Workaround:**
- TTS direkt: `pico2wave -l de-DE -w /tmp/x.wav "Text" && aplay -D plughw:3,0 /tmp/x.wav`
- Oder espeak/Piper, robot_hat komplett umgehen → [[README|picrawler/README]]

**Patch** (`~/robot-hat/robot_hat/utils.py`):
```python
def run_command(cmd):
    import subprocess
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout + result.stderr
```
Aktivieren: `pip install -e ~/robot-hat --break-system-packages`.

## Bug 2: Speaker-Enable berücksichtigt nur GPIO 20 (v4x-Default)

`robot_hat.enable_speaker()` setzt nur GPIO 20 HIGH. Auf diesem HAT muss zusätzlich **GPIO 12 LOW** sein, sonst bleibt der Amp stumm. Operative Spielsequenz + Diagnose: [[speaker-gpio]].

## Bug 3: HAT-Erkennung scheitert ohne EEPROM

`Devices.__init__()` iteriert `/proc/device-tree/` nach `hat`-Ordnern mit `uuid`-File. Auf diesem System **kein** `hat*`-Eintrag → Default-Fallback `robot_hat_v4x` (`spk_en=20`). Passt empirisch nicht 100% (siehe Bug 2). Vermutlich v5x-Board ohne EEPROM oder Hybrid.

## Upstream

SunFounder GitHub: https://github.com/sunfounder/robot-hat — PR-Wert vorhanden, niedrige Priorität.

## Querverweise

[[README|picrawler/README]] · [[speaker-gpio]] · [[setup]] · [[hardware-status]]

---
> *Quelle: archiv/162.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, Bug-Übersichtstabelle, als kanonische Bug-Liste markiert; GPIO-Speaker-Erklärung hier behalten, speaker-gpio verweist hierher).*
