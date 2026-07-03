---
title: Justlauncher
type: note
status: aktiv
updated: 2026-06-24
---

# JustLauncher · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Zentrales Dashboard für die selbst gehosteten Just-Dienste (JustFinanceBusiness, JustFinancePrivate, JustTodo, JustReise). Zeigt alle Dienste online/offline und öffnet sie per Klick.

## Stack / Technik
- Flask-Server + native Wrapper, die das Dashboard pro Plattform als App bündeln.
- `src/JustLauncherMac/` (Flask app.py + pywebview + PyInstaller), `…Android/` (Kotlin/Gradle WebView), `…Windows/` (PyInstaller), `…RaspberryPi/` (Wrapper + install.sh).

## Stand / Funktionen
- Aktiv. Mac-Server als LaunchAgent `com.itintechsolutions.justlauncher`.
- Wichtig: läuft aus dem Runtime-Klon `~/JustLauncher` (per rsync deployed), NICHT direkt aus dem Repo. Repo = Quelle.

## Betrieb
- Mac mini, Port **8000**. Deploy: `src/JustLauncherMac/` → rsync-Klon `~/JustLauncher` → `launchctl kickstart`.

## Health (Audit 2026-06-07)
- **63/100** — größtes Problem: hardcoded Tailscale-IP `100.89.217.4` in den Wrappern, 3× Code-Duplikation (`first_reachable()` + `INTERCEPT_JS`). (auth timing-safe seit Iter2.)

## Verweise
- Quelle: 10_Apps/JustLauncher/
- Bündelt: [[just-finance-business|JustFinanceBusiness]], [[just-finance-private|JustFinancePrivate]], [[just-todo|JustTodo]], [[just-reise|JustReise]], [[just-better|JustBetter]]
