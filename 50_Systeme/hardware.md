---

title: Hardware
type: reference
status: aktiv
updated: 2026-06-22
description: "Hardware-Inventar: Geräte, Hostnames, Tailscale-IPs, OS, Rollen, Detail-Specs, Rack-Planung, Mac mini Hermes/Codex, NAS, PCs, Smartphones und Spezial-Setups."
aliases: [hardware, geräte, devices, devices-specs, hardware-inventar]
tags: [infra/hardware, infra/network, tailscale, specs, llm-local, ai-agents]
related: ["[[services-mac-mini]]", "[[storage-cloud]]", "[[security-status]]", "[[game-saves]]", "[[windows-toolchain]]", "[[claude-session-hook]]"]
----------------------------------------------------------------------------------------------------------------------------------------------------

# Hardware

> Diese Datei ist der zentrale Hardware-Überblick.
> Online-/Offline-Status wird **nicht dauerhaft gespeichert**, weil er nur eine Momentaufnahme ist.

## Regeln

* Alle bekannten Geräte werden hier mit Hostname, Tailscale-IP, OS und Rolle geführt.
* Online-/Offline-Status ignorieren.
* Detail-Specs stehen direkt beim jeweiligen Gerät.
* Secrets, Passwörter und Tokens gehören nicht hierher, sondern nach `secrets.local.md` / `secrets-locations`.

---

# Geräte-Index

| Gerät / Hostname |      Tailscale-IP | OS      | Rolle                                             |
| ---------------- | ----------------: | ------- | ------------------------------------------------- |
| `gx10-bf12`      |   `100.75.47.118` | Linux   | ASUS Ascent GX10 / GB10 / AI-Arbeitsgerät         |
| `justingamingpc` |   `100.94.200.83` | Windows | Justin Gaming-PC / RTX 3090 / lokale KI-Toolchain |
| `justinmacmini`  |    `100.89.217.4` | macOS   | Mac mini M4 / Server / Hermes mit Codex-Abo       |
| `justnas`        |  `100.122.172.62` | Linux   | Synology DS923+ / NAS / Datenablage               |
| `justinmacairm4` |   `100.119.74.63` | macOS   | MacBook Air M4 / Entwicklung / CS50               |
| `s24-von-justin` |    `100.99.130.6` | Android | Justin Smartphone                                 |
| `s21-von-sarah`  |    `100.94.50.21` | Android | Sarah Smartphone                                  |
| `sarahgamingpc`  | `100.114.201.107` | Windows | Sarah Gaming-PC                                   |
| `justlaptop`     |  `100.117.38.122` | Windows | Justin Laptop                                     |
| `justpi5`        |   `100.119.30.59` | Linux   | Raspberry Pi 5 / JustPi                           |

---

# Server / KI / Infrastruktur

## ASUS Ascent GX10 / GB10

Hostname:

* `gx10-bf12`

Tailscale:

* `100.75.47.118`

OS:

* Linux

Rolle:

* lokaler AI-/Agenten-Computer
* Arbeitsgerät für lokale KI-Tests
* geplant für Ben / lokale Agenten-Workflows
* Teil des Mini-Server-/AI-Rack-Setups

Masse:

* 150 × 150 × 51 mm

Gewicht:

* 1.48 kg

Wichtig:

* zusammen mit Mac mini, Synology NAS und USV geplant
* 35-cm-Breitenlimit bei Rack-/Regalplanung beachten

---

## Mac mini M4 · Server

Hostname:

* `justinmacmini`

Tailscale:

* `100.89.217.4`

OS:

* macOS

Setup:

* 08.04.2026

RAM:

* 24 GB

Storage:

* ca. 460 GB

Python:

* 3.14.3 via Homebrew

Flask:

* 3.1.3 systemweit installiert

AnyDesk:

* Port 7070 öffentlich, bewusst so

Masse:

* 127 × 127 × 50 mm

Gewicht:

* 0.67 kg

Sudo-Passwort:

* liegt in `secrets.local.md`
* rotieren
* mindestens 12 Zeichen

### KI / Agenten

Aktueller Stand:

* Auf dem Mac mini läuft **Hermes**
* Hermes nutzt das **Codex-Abo**
* Der Mac mini dient als lokaler Agenten-/Automation-Server

Nicht mehr aktuell:

* alte lokale LLM-Modelle auf dem Mac mini
* `qwen3:30b-a3b-q3_K_L`
* `gpt-oss-20b Q4`
* `Qwen3-30B-A3B MoE Q4_K_M`
* MLX/GGUF-Optimierungsnotizen
* exo-Cluster-Regeln

Regel:

* Alte LLM-Angaben nicht mehr als aktuellen Stand verwenden
* Falls behalten, nur als Archiv-/Historiennotiz

---

## JustNAS · Synology DS923+

Hostname:

* `justnas`

Tailscale:

* `100.122.172.62`

OS:

* Linux

Rolle:

* NAS
* zentrale Datenablage
* Backups
* Archiv
* Finanzen
* Dokumente

Mount:

* `/mnt/justnas`

Symlink:

* `~/JustNAS`

Permanent via:

* `/etc/fstab`

Credentials:

* `/etc/credentials.justnas`

Hauptordner:

* AI
* Archiv
* Backups
* Dokumente
* Finanzen
* Software
* Spiele

DSM-Notify:

* aktiv

Masse:

* 199 × 223 × 166 mm

Gewicht:

* 2.24 kg

Offen:

* DSM-Pakete seit 11.04.2026 veraltet → prüfen
* n8n-Container wurde am 14.11.2025 unerwartet beendet → bei Bedarf neu starten

---

## Raspberry Pi 5 / JustPi

Hostname:

* `justpi5`

Tailscale:

* `100.119.30.59`

OS:

* Linux

Rolle:

* Raspberry Pi 5
* JustPi
* kleine lokale Services / Tests / Infrastruktur

---

# PCs / Entwicklung

## MacBook Air M4

Hostname:

* `justinmacairm4`

Tailscale:

* `100.119.74.63`

OS:

* macOS

Rolle:

* Entwicklung
* CS50
* Web-/Python-/Flask-Projekte

Python:

* 3.9.6 System
* 3.12.9 zusätzlich

Tooling:

* Homebrew
* Git
* Flask 3.1.3
* VS Code
* CS50 Toolchain

AppleCare+:

* aktiv

Wichtige UI-Regel:

* Keine Desktop-GUI mit tkinter/customtkinter/ttkbootstrap bauen
* Immer Flask Web-UI verwenden
* Grund: Python-UI-Probleme auf Mac

---

## Justin Gaming-PC

Hostname:

* `justingamingpc`

Tailscale:

* `100.94.200.83`

OS:

* Windows

GPU:

* RTX 3090

Rolle:

* Gaming
* lokale Sprach-LLM-Toolchain
* Game-Saves
* starke lokale GPU-Maschine
* relevant für KI-/Audio-/LLM-Experimente

---

## Sarah Gaming-PC

Hostname:

* `sarahgamingpc`

Tailscale:

* `100.114.201.107`

OS:

* Windows

Rolle:

* Sarahs Gaming-PC

Besonderheit:

* Claude SessionStart-Hook installiert am 02.05.2026

---

## Justin Laptop

Hostname:

* `justlaptop`

Tailscale:

* `100.117.38.122`

OS:

* Windows

Rolle:

* Justin Laptop
* mobiles Windows-Gerät

---

# Smartphones

## Justin Smartphone

Hostname:

* `s24-von-justin`

Tailscale:

* `100.99.130.6`

OS:

* Android

Rolle:

* Justin Smartphone

---

## Sarah Smartphone

Hostname:

* `s21-von-sarah`

Tailscale:

* `100.94.50.21`

OS:

* Android

Rolle:

* Sarah Smartphone

---

# Rack / Mini-Server-Setup

## Aktueller Rack-Inhalt

Das Rack ist gebaut. Aktuell gehören diese Geräte zum Mini-Server-/NAS-/AI-Rack-Setup:

* ASUS Ascent GX10 / GB10
* Netgear GS105GE Switch
* Mac mini M4
* Synology DS923+
* APC Back-UPS Pro 650 / BR650MI

## APC Back-UPS Pro 650 / BR650MI

Rolle:

* USV für Mini-Server-/NAS-/AI-Rack
* im aktuellen Setup nur über das NAS eingebunden

Masse:

* 91 × 310 × 190 mm

Gewicht:

* 6.4 kg

Wichtig:

* passt nicht sinnvoll in kleine 10"-6HE-Racks
* zu tief für das kompakte Rack
* braucht zusätzlich Kabel- und Luftspielraum

Planungsregel:

* USV separat unter/neben Rack platzieren
* oder Custom-Rack / offenes Regal bauen

## Rack-Status / Bauprinzip

Maximale Breite:

* ca. 35 cm

Tiefe:

* weniger kritisch

Ziel:

* kompaktes, sauberes All-in-One-Mini-Server-/NAS-/USV-/AI-Rack

Status:

* Custom-Mini-Rack ist umgesetzt

Grund:

* fertige kleine 10"-Racks passen schlecht zur tiefen APC-USV
* 35-cm-Breitenlimit macht Standardlösungen schwierig

## Bekannte Rack-Probleme

* APC-USV ist zu tief für kleine 10"-Racks
* Kabel-/Luftspielraum muss eingeplant werden
* USV besser separat oder in Custom-Regal integrieren
* NAS, Mac mini und ASUS GX10 können kompakt zusammen geplant werden

---

# Audio / Spezial-Setups

## Dual-Audio Mac

Use-Case:

* Justin mit Galaxy Buds4 Pro
* Sarah mit AirPods
* Beide hören gleichzeitig Filmton

Skript:

* `filmton on|off|airpods|status`

Pfad:

* `~/.local/bin/filmton`

Benötigt:

* `switchaudio-osx`

Wichtige Regel:

* Mikrofon immer auf MacBook Air-Mikrofon setzen

Sonst HFP-Falle:

* schlechte Qualität
* zweiter Hörer stumm

Grenze:

* Zwei Bluetooth-A2DP-Streams sind am Limit

Falls instabil:

* Galaxy Dual Audio
* oder Bluetooth-Transmitter mit Dual-Link

---

# Verweise

* `services-mac-mini`
* `storage-cloud`
* `security-status`
* `game-saves`
* `windows-toolchain`
* `claude-session-hook`
* `secrets-locations`

