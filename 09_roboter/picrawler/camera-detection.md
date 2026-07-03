---
title: PiCrawler — Kamera-Detektion (offen)
type: reference
status: aktiv
updated: 2026-06-14
description: Lies bei Frage warum die PiCrawler-Kamera nicht erkannt wird. OV5647-Sensor antwortet nicht auf I²C (Stand 2026-05-25) — Kabel-/Polaritäts-Diagnose-Checkliste + Fix-Workflow.
aliases: [camera-detection, kamera, ov5647, csi-kamera, picrawler-kamera]
tags: [reference/robotik, picrawler, kamera, ov5647, csi, offen]
related: ["[[README|picrawler/README]]", "[[setup]]", "[[hardware-status]]", "[[robot-hat-bugs]]"]
---

# Kamera-Detektion (offenes Problem)

MOC-Rücklink: [[README|picrawler/README]]

PiCrawler nutzt das **OV5647**-Modul (5 MP, F1.8, 65° FOV, 1080p30) über CSI. Stand 2026-05-25: **wird nicht erkannt**.

> [!warning] PRÜFEN: Status offen seit 2026-05-25
> Software ausgeschlossen → physisches Problem (Ribbon/Sensor). Diagnose-Checkliste unten abarbeiten und Ergebnis hier nachtragen.

> [!warning] PRÜFEN: Board-Modell für Ribbon-Polung
> Polung/Slot-Lage unterscheiden sich Pi 4 ↔ Pi 5. SoT [[network-tailscale]] sagt **Pi 5**, Roboter-Notizen sagen **Pi 4** ([[README|picrawler/README]]). Vor dem Umstecken Board physisch verifizieren — sonst falsche Polung.

## Symptome

```
$ rpicam-hello --list-cameras
No cameras available!
```

Mit explizitem Runtime-Overlay:
```
$ sudo dtoverlay ov5647
$ dmesg | tail
ov5647 10-0036: ov5647_read: i2c read error, reg: 300a = -5
ov5647 10-0036: ov5647_read: i2c read error, reg: 100  = -5
ov5647 10-0036: probe with driver ov5647 failed with error -5
```

Error -5 = `EIO`. Treiber lädt, will Sensor bei I²C `0x36` auf Bus 10 (CSI-I²C) lesen → keine Antwort. **Sensor kommuniziert nicht.**

## Konfiguration ist ok (Software ausgeschlossen)

- `camera_auto_detect=1` in Runtime `/boot/firmware/config.txt`
- `picamera2 0.3.36` importierbar
- `vilib 0.3.18` lädt (wirft nur IndexError weil keine Kamera)
- Keine USB-Kameras am Pi (`lsusb`: nur Tastatur/Maus/USB-Audio/Stick)

## Ursachen-Wahrscheinlichkeit (physisch)

| # | Ursache | Prüfung |
|---|---|---|
| 1 | CSI-Ribbon locker | Schwarzer Riegel beidseitig (Pi- **und** Kamera-Buchse) komplett unten. Pi vorher aus. |
| 2 | Ribbon falsch gepolt | Pi 4: silbrige Kontakte zur **HDMI-Seite**, blauer Versteifer zur **Ethernet-Seite**; am Modul meist umgekehrt. *(PRÜFEN bei Pi 5 — Lage abweichend.)* |
| 3 | Falscher Slot (CSI vs DSI) | Pi 4: CSI liegt zwischen HDMI und Audio-Buchse, DSI zwischen Power-In und microSD. |
| 4 | Defektes Ribbon oder OV5647-Modul | Ersatzkabel/-modul testen. |

## Fix-Workflow (sobald Hardware geprüft)

```bash
# explizit Overlay setzen — auto_detect klappt bei SunFounder-OV5647 oft nicht
sudo tee -a /boot/firmware/config.txt <<< "dtoverlay=ov5647"
sudo reboot
# nach Boot:
rpicam-hello --list-cameras   # Erwartung: 1 camera available, [ov5647]
```

## Software-Bereitschaft (alles parat)

| Tool | Status | Pfad (Runtime) |
|---|---|---|
| `picamera2` | installiert | `/usr/local/lib/python3.13/dist-packages/picamera2/` |
| `vilib` | installiert | `~/vilib` (AI-Vision fehlt — siehe [[setup]]) |
| `rpicam-hello` / `rpicam-still` | installiert | `/usr/bin/` |
| `libcamera-hello` (Alt-Name) | nicht installiert | nicht nötig |

## Querverweise

[[README|picrawler/README]] · [[setup]] · [[hardware-status]] · [[robot-hat-bugs]]

---
> *Quelle: archiv/85.md, überarbeitet 2026-06-14 (AI-first verdichtet, Frontmatter komplett, offen-Status + Pi4/Pi5-Polungs-Flag). HINWEIS: Auftrag nannte archiv/84.md, das ist aber die Bruno-Persona — korrekte Kamera-Quelle ist 85.md.*
