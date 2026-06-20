# JustSavegame · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Savegame-Backup-Manager für Windows mit GitHub-Sync. Sichert Spiel-Savegames per Klick in hochgezählte Ordner (17 → 18 → 19 …) und pusht sie automatisch in ein Git-Repository.

## Stack / Technik
- Python-stdlib only (keine Pakete), Git muss im PATH sein. Web-UI im Browser.
- `src/` (server.py), `config/` (profiles.json = versioniert/synct, secret.json = lokaler Bearer-Token, gitignored).

## Stand / Funktionen
- Aktiv (Windows-App). Start: „Start JustSavegame.bat" → Browser `http://127.0.0.1:8765`, oder `python src\server.py`.
- Profil = Name + VON (Savegame-Ordner) + ZU (Ziel-Basis). Liegt ZU in einem Git-Repo, wird der neue Ordner committet + (optional) gepusht. Commit-Message mit Platzhaltern `{name}{folder}{timestamp}{source}{target}`.
- V0.02: Profile in `config/profiles.json` versioniert (auf anderem PC via `git pull` da). Profile speichern absolute Pfade → bei abweichendem Laufwerk/Benutzer einmal anpassen.
- Fernsteuerung: Server lauscht `0.0.0.0:8765`, im Tailnet erreichbar; Remote-Aktionen brauchen Bearer-Token, localhost token-frei.

## Betrieb
- Windows-App, Port 8765 (außerhalb Mac-mini-Schema).

## Health (Audit 2026-06-07)
- **78/100** (höchster Score im Portfolio) — Hinweise: keine CSRF/CSP, blockierende Backups.

## Verweise
- Quelle: 10_Apps/JustSavegame/
- Verwandt: Just-Reihe, [[justlauncher]]
