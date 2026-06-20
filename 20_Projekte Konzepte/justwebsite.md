# JustWebsite · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Statische Firmen-Website von Itin TechSolutions (HTML/CSS/JS). Öffentlicher Web-Auftritt: Startseite, Vision, Erfolgsseite + rechtliche Seiten (Impressum, Datenschutz, AGB).

## Stack / Technik
- Statisches HTML/CSS/JS. `src/`: aktuelle V2 (HTML, itin.css, bilder/). `docs/`: Konzepte/Notizen/Screenshots. `archive/V1/`: alte Version.

## Stand / Funktionen
- Aktiv, V2 ist aktuell (V1 archiviert).
- Offen: Deploy-/Hosting-Ziel dokumentieren, Bilder optimieren/komprimieren, prüfen ob V1 noch gebraucht wird.

## Betrieb
- Statisch via Netlify (kein lokaler Port). Domain laut Firma: `itintechsolutions.ch` (Dev `justdomain.ch`).

## Health (Audit 2026-06-07)
- **67/100** — größtes Problem: Navbar + Theme-Toggle 6× dupliziert, inline CSS. Iter2: −3.6 MB Bilder (PNG→JPEG), totes Hintergrund.png raus; V1-Archive (14 MB) bleibt vorerst.

## Verweise
- Quelle: 10_Apps/JustWebsite/
- Firma: [[itintech-firma]] (Hosting Netlify, Kontaktformular-Eigenheiten)
