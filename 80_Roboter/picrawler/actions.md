---
title: PiCrawler — Action-Katalog
type: reference
status: aktiv
updated: 2026-06-14
description: Vollständige Liste aller Built-in-Gangarten + preset_actions mit Sicherheits-Klassifikation bei defektem Bein. Lies bevor du eine Action triggerst oder ein neues Motion-Script schreibst.
aliases: [actions, action-katalog, gaits, gangarten, picrawler-actions, do_action]
tags: [reference/robotik, picrawler, motion, safety]
related: ["[[README|picrawler/README]]", "[[kinematics]]", "[[hardware-status]]", "[[power-protocol]]"]
---

# Action-Katalog

MOC-Rücklink: [[README|picrawler/README]]

> [!danger] Aktuell 1 Bein defekt (Pin 11) + Verkabelungs-Diskrepanz
> Solange [[hardware-status]] nicht "alle ✅" zeigt: **keine** ❌-Actions, und wegen der `PIN_LIST`-Diskrepanz möglichst gar kein `do_step`/`do_action` — nur Single-Servo. Spalte "Bei 1 defektem Bein" gilt erst wieder verlässlich nach Verkabelungs-Klärung.

## Built-in `do_action(name)` — aus `Picrawler.MoveList` (`picrawler.py`)

| Action | Beschreibung | Lift-Beine? | Bei 1 defektem Bein |
|---|---|---|---|
| `sit` | Diagonal-Pose, alle 4 Füße am Boden, Z=-30 | nein | ✅ sicher |
| `stand` | Quadratisch ausgerichtet, Z=-50, 5-Stufen-Ramp | nein | ⚠️ Last verteilt sich ungleichmäßig |
| `forward` | 1 Step vorwärts, Trab-Gang (1 Bein hoch zur Zeit) | **ja** | ❌ verboten |
| `backward` | 1 Step rückwärts | **ja** | ❌ verboten |
| `turn left` / `turn right` | Drehung über 4 Phasen | **ja** | ❌ verboten |
| `turn left angle` / `turn right angle` | parametrisierter Turn (Class-Var `angle=30`) | **ja** | ❌ verboten |
| `wave` | Bein 1 winkt (Z_WAVE=60, hoch in der Luft) | **ja, 1 Bein** | ⚠️ nur wenn Bein 1 heil ist UND defektes Bein nicht in Hauptlast |
| `look_left` / `look_right` | Body-Drehung über Schulter-Sweep | nein\* | ✅ ungefähr — Body-Sway, keine Lift |
| `look_up` | Hinten-Beine drücken hoch | nein | ⚠️ Belastung hinten asymmetrisch |
| `look_down` | Vorne-Beine senken | nein | ⚠️ Belastung vorne asymmetrisch |
| `push_up` | Vorne hoch+runter (Z_PUSH=-76 ↔ Z_TURN=-40) | nein | ⚠️ extreme Last vorne |
| `dance` | Body-Sway in Kreisbewegung + Roll/Pitch — **alle 4 Füße bleiben am Boden** (`move_body_absolute`) | nein | ✅ sofern Amplitude (40 mm) das defekte Bein nicht über Workspace zwingt — vorher mit `israise=True` testen |

\* `look_left/right` mit `mode=1` decorator — siehe `normal_action`.

## Community-Level `preset_actions.py` (`~/picrawler/examples/preset_actions.py`)

| Funktion | Beschreibung | Bei 1 defektem Bein |
|---|---|---|
| `sit(spider)` | Wrapper für `do_action('sit')` | ✅ sicher |
| `stand(spider)` | Wrapper für `do_action('stand')` | ⚠️ siehe oben |
| `look_up` / `look_down` | Custom Coord-Sequenz | ⚠️ ähnliche Last-Verteilung |
| `dance(spider)` | Ruft `do_action('dance')` — body-sway, keine Lift | ✅ |
| `wave_hand` | Bein 1 winkt mit Z=120, Speed 60 | ❌ wenn defektes Bein zur Stütze beiträgt |
| `shake_hand` | Bein 1 streckt sich aus (`[5, 280, 80]` — out of normal envelope!) | ❌ |
| `fighting` | Multi-Phase: ready → twist_butt → pounce_bite → return | ❌ |
| `excited` | Bounce up-down (alle Füße am Boden) | ⚠️ alle Beine belastet, aber gleichzeitig — kann gehen |
| `play_dead` | Beine nach oben (Z=100, "Käfer-Position") | ⚠️ kein Stand-Risiko, aber defekter Servo überfordert |
| `nod` | Vorne-runter / hinten-hoch, alle Füße bleiben | ⚠️ asymmetrische Last |
| `shake_head` | twist_butt-artige Body-Drehung | ⚠️ Body-Sway, alle Füße am Boden, OK falls Workspace passt |
| `look_left` / `look_right` | Custom Implementation | ⚠️ ähnlich |
| `warm_up` | Body-Sway in Kreisbewegung + Rotation | ✅ wie `dance` — alle Füße bleiben |
| `push_up` | Wie built-in, aber asymmetrische Stützen-Pose | ❌ |

## Faustregel "Lift-Test"

Eine Pose hebt ein Bein, wenn **irgendein Bein-Z > -10** (über Boden) oder **ein Bein bei `Z_UP=-30` steht während andere bei `Z_DEFAULT=-50`**. Bei defektem Bein = hohes Kipp-Risiko.

Sichere-Pose-Indikatoren:
- Alle 4 z-Werte ≈ gleich (statische Pose)
- Z-Werte zwischen -76 (push_up unten) und -10 (Workspace-Top)
- `coord_list` aus `move_body_absolute(x,y,z)` → garantiert keine Lift

## Pre-Flight-Check beim Script-Schreiben

```python
def is_safe_for_broken_leg(coords_sequence):
    for step in coords_sequence:
        zs = [leg[2] for leg in step]
        if max(zs) - min(zs) > 15:   # >15 mm Unterschied = Lift
            return False
    return True
```

Faustregel: **nicht durch `move_body_absolute` erzeugt → defaultmäßig verboten**, außer Justin segnet es ab.

## Querverweise

[[README|picrawler/README]] · [[kinematics]] · [[hardware-status]] · [[power-protocol]]

---
> *Quelle: archiv/75.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, defektes-Bein-Danger + Verkabelungs-Hinweis geflaggt).*
