# JustUpdate · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Windows-Wartungs-Tool „System Maintenance Pro" (PowerShell-GUI) inkl. Release-Pipeline und Inno-Setup-Installer. Wird mit Self-Update an Kunden verteilt.

## Stack / Technik
- PowerShell-GUI. `src/`: build.ps1, fleet-report.ps1, MaintenanceProGUI_MODERN.ps1. `config/`: VERSION (Single Source of Truth), JustUpdate_Setup.iss, Icon.
- Ein-Befehl-Release: `build.ps1` liest Version, patcht GUI+Installer, baut EXE (PS2EXE) + Installer (Inno Setup), legt Release unter `archive/Releases/` ab, synct Verteil-Repo.

## Stand / Funktionen
- Aktiv. Läuft/baut auf Windows; auf dem Mac wird nur die Struktur gepflegt.
- `CHANGELOG.md` ist kunden-facing, wird von build.ps1 ins Verteil-Repo gespiegelt → bleibt bewusst an der Wurzel (nicht nach Doku/ verschieben, sonst bricht der Build).
- Offen: nach Topologie-Umbau einmal vollständigen Build auf Windows verifizieren.

## Betrieb
- Windows-Desktop-App, kein HTTP-Service. Build: `cd src; .\build.ps1` (`-Push` für Commit+Push beider Repos).

## Health (Audit 2026-06-07)
- **72/100** — größtes Problem: fehlende Code-Signatur (Authenticode für Self-Update), PowerShell-Monolith (3'499 Z.), Doku veraltet.

## Verweise
- Quelle: 10_Apps/JustUpdate/
- Firma/Kunden: [[itintech-firma]], [[itintech-kunden]]
