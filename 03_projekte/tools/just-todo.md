---
title: Justtodo
type: note
status: aktiv
updated: 2026-06-24
---

# JustTodo · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Persönliche Todo-App von Justin, auch von Bots (Felix, Claude Code) genutzt. Schlanke, datei-basierte Todo-Verwaltung — KEIN DB-Server.

## Stack / Technik
- Flask + Jinja-Frontend (index.html als Datei).
- `src/`: server.py, app.py (Shim), api_auth.py, index.html. `data/`: todos.json (LIVE) + todo/ (.txt-Snapshots), automatisch git-versioniert.
- API: GET/POST /api/todos, /api/todos/{id}/status, DELETE /api/todos/{id}, /visitenkarte.

## Stand / Funktionen
- Live auf dem Mac mini als LaunchAgent `com.itintechsolutions.justtodo`, läuft direkt aus dem Repo.
- Kategorien als Text-Präfix (steuert UI-Filter): Acino, Privat, ItinTech, IT.
- Jeder Todo zusätzlich als .txt in `data/todo/`, mit todos.json git-committet (Auto-git-add im Server).

## Betrieb
- Mac mini, Port **8030**, Tailscale `100.89.217.4`. Flask.

## Health (Audit 2026-06-07)
- **66/100** — größtes Problem: Legacy-Shim `src/app.py`, 80× .txt-Snapshots/Write. (auth timing-safe seit Iter2.)

## Verweise
- Quelle: 10_Apps/JustTodo/
- Genutzt von: [[jarvis.md]] (Tool-API), Bots. Verwandt: [[just-launcher.md|JustLauncher]]
