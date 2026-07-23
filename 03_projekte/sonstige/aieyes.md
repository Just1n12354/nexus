---
title: Aieyes
type: note
status: aktiv
updated: 2026-06-24
---

# AIEyes · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Werkzeugkasten, der einer KI (Claude) Augen und Hände auf einem Rechner gibt: Augen = Bildschirm als Screenshot, Hände = echte Maus/Tastatur (computer-use). Loop: Bild ansehen → genau EINE Aktion entscheiden → ausführen → wieder ansehen. Kein blindes Komplett-Skript — die KI ist der Fahrer.

## Stack / Technik
- Python 3.13, Pillow (Screenshots) + uiautomation (UI Automation). Maus/Tastatur via ctypes/SendInput (kein pyautogui), Tippen via KEYEVENTF_UNICODE (layout-unabhängig, QWERTZ + Umlaute).
- `device.py`: zentrale Geräte-Erkennung (ENV > Hostname-Registry > Plattform-Fallback), kein Hardcoding mehr.
- Kern-Dateien: `act_win.py` (Aktions-Schicht), `do_win.py` (KI-Loop-Treiber), `uia_probe.py` (UIA-Inspektor), `zoom.py` (Pixel-Fallback).

## Stand / Funktionen
- Zwei Stränge: macOS (MacAirM4, Phase 1, PAUSIERT — Wahrnehmung war Engpass) und Windows (vollständig gebaut + verifiziert).
- Windows-Geräte: PCSarah (RTX 3080, Erst-Verifikation) + PCJustin (RTX 3090, MAIN, kalibriert 2560×1440/scale=1).
- UIA-Hybrid: „Browser auf + maximiert + YouTube" in ~10s statt ~4 Min. Reiner Pixel-Loop nur noch Fallback.
- Alle Tests grün (DPI, Maus-Warp 0px, Unicode-Tippen, Klick trifft, UIA-Navigation).
- Neuer Engpass: Fokus/Vordergrund + Tab-Orchestrierung (SendInput geht immer ins Vordergrundfenster).

## Betrieb
- Läuft auf Windows-Geräten (PCSarah/PCJustin); Gerät zur Laufzeit über `device.py` aufgelöst.

## Verweise
- Quelle: 10_Apps/AIEyes/
- Verwandt: [[jarvis.md]] (computer-use/Tool-Layer-Thema), `vnc_grab.ps1`/ClaudeEyes
