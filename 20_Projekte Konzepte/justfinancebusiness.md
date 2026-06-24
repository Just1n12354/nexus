---
title: Justfinancebusiness
type: note
status: aktiv
updated: 2026-06-24
---

# JustFinanceBusiness · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Selbst gebaute Buchhaltungs-App für Itin TechSolutions (Einzelunternehmen Diepflingen BL): Einnahmen/Ausgaben, Kunden, Rechnungen (PDF via Chrome Headless), Schweizer KMU-Kontenrahmen. OR-konform (Aufbewahrungspflicht, fortlaufende Rechnungsnummern).

## Stack / Technik
- Python-stdlib (`http.server`, kein Flask) + Single-File-Frontend (Dark Theme).
- `src/`: server.py, api_auth.py, index.html, qr_bank.png. `data/`: data.json (LIVE), quittungen/, rechnung/ (PDFs).
- API: /api/data, POST /api/ausgaben, /api/rechnungen (PDF-Gen), /api/dashboard, /api/v1/* (KI-Agent, Bearer, read-only).

## Stand / Funktionen
- Live auf dem Mac mini als LaunchAgent `com.itintechsolutions.finance`, läuft direkt aus dem Repo (`src/server.py`).
- Harte rechtliche Konventionen: `_rechnung_counter` NIE manuell zurücksetzen (OR 957a, keine Doppelnummern); jede Rechnung `aufbewahrbar_bis` = erstellt + 10 Jahre (OR 957).
- `data/` enthält echte Firmenzahlen → `.gitignore` an der Wurzel MUSS bleiben.

## Betrieb
- Mac mini, Port **8010**, Tailscale `100.89.217.4`. stdlib http.server.

## Health (Audit 2026-06-07)
- **75/100** — größtes Problem: monolithisches HTML (1'235 Z.), keine Tests. (CORS härtbar, auth timing-safe seit Iter2.)

## Verweise
- Quelle: 10_Apps/JustFinanceBusiness/
- Firma: [[itintech-firma]]. Verwandt: [[justfinanceprivate]] (strikt getrennt), [[justlauncher]]
