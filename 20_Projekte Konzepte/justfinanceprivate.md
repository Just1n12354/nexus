---
title: Justfinanceprivate
type: note
status: aktiv
updated: 2026-06-24
---

# JustFinancePrivate · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Private Finanz-App von Justin: Konten-Snapshots, Buchungen, große Ausgaben, Lotto, Digitec-Bestellungen, Steuern. Vermögensübersicht über Zeit (Snapshot je Stichtag), Bank-Import, Ausgaben-Tracking. **Strikt getrennt** von der Firma.

## Stack / Technik
- Python-stdlib (`http.server`) + Single-File-Frontend.
- `src/`: server.py, api_auth.py, index.html, finanzplanung.html, statistik.html. `data/`: data.json (LIVE), Bank/ Lohn/ Steuern/ Lotto/ GrosseAusgaben/ …
- API: /api/data, /api/buchungen|lotto|digitec, POST /api/snapshot, /api/sync-prices, POST /api/backup, /api/v1/* (KI-Agent, Bearer, read-only). Demo-Modus read-only.

## Stand / Funktionen
- Live auf dem Mac mini als LaunchAgent `com.itintechsolutions.financeapp`, läuft direkt aus dem Repo.
- `data/` enthält ECHTE Finanzdaten (Bank/Lohn/Steuer) → `.gitignore` an der Wurzel MUSS bleiben.
- Backup-Strategie ist `git push` mit Absicht → die getrackten Daten-Dateien sind kein Leck (privates Repo), nicht „bereinigen".

## Betrieb
- Mac mini, Port **8020**, env-konfigurierbar. Demo Port 8081.

## Health (Audit 2026-06-07)
- **67/100** — größtes Problem: Dev-Server in Prod, monolithisches Frontend (index.html 2'071 Z.). (CORS härtbar, auth timing-safe seit Iter2.)

## Verweise
- Quelle: 10_Apps/JustFinancePrivate/
- Verwandt: [[justfinancebusiness]] (strikt getrennt), [[justlauncher]]. Vgl. Memory: „Alles in private Repos pushen"
