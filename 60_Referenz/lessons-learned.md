---
title: Lessons Learned
type: reference
status: aktiv
updated: 2026-06-25
description: Wichtige Lehren und Erkenntnisse aus der Arbeit mit Nexus, Agenten, und IT-Systemen.
tags: [learning, improvements, lessons]
---

# Lessons Learned

> Wichtige Erkenntnisse aus der täglichen Arbeit mit Nexus, Agenten, und IT-Systemen.

---

## Git & Versionierung

### L001: git add -A vermeiden im Nexus
- **Fehler:** `git add -A` committet versehentlich Secrets, Logs und temporäre Dateien.
- **Lektion:** Immer gezielt pro Pfad stagten (`git add path/to/file.md`).
- **Stand:** 2026-06-24 — Jetzt gilt: Nur explizite Pfade stagten, nie `git add -A` im nexus.
- **Quelle:** KW_24, Robert-Agent (doppelte Auto-Läufe, geheime Dateien)

### L002: Git-Index mmap-Problem
- **Fehler:** `IndexError: index out of range` beim Git-Index.
- **Ursache:** Zu grosser Git-Index übersteigt mmap-Grösse.
- **Lösung:** `git config core.packedGitWindowSize 256m` + `git config core.packedGitLimit 512m`
- **Stand:** 2026-06-22
- **Quelle:** KW_24

### L003: Git-Status nach Rebase prüfen
- **Fehler:** Remote hatte fremden Commit → `git push` abgelehnt.
- **Lösung:** `git pull --rebase` vor dem Push.
- **Stand:** 2026-06-22
- **Quelle:** KW_24

### L004: Push-Blocker GitHub-Credentials
- **Fehler:** `gh auth status` meldet ungültige Tokens.
- **Lösung:** `gh auth login` oder `git push` im eigenen Terminal mit GCM-Popup.
- **Stand:** 2026-06-24
- **Quelle:** KW_25

### L005: Branch-Namenskonvention für Nachtläufe
- **Empfehlung:** `nacht/2026-06-25` (Datum-basiert, eindeutig, einfach zu tracken).
- **Stand:** 2026-06-25
- **Quelle:** Nachtlauf 25.06.2026

---

## Agenten & KI

### L006: Agenten-Runner sauber killen
- **Fehler:** Auto-Lauf lief doppelt (erster Runner nicht sauber gekillt).
- **Ursache:** `ollama serve` absturz → verwaister `llama-server.exe` hielt 10 GB VRAM.
- **Lösung:** Runner-IDs tracken, process tree prüfen, `kill -9` für verwaiste Prozesse.
- **Stand:** 2026-06-24
- **Quelle:** KW_24, Robert-Agent

### L007: Zählen/Rechnen via Code
- **Fehler:** Robert zählte "Robert" 3× statt 4× (im Kopf statt per Code).
- **Lösung:** Immer via Code zählen/rechnen, nie im Kopf.
- **Stand:** 2026-06-24
- **Quelle:** KW_24, Robert-Agent Regel 9

### L008: Getestete Skill-Vorlagen nutzen
- **Fehler:** Robert bastelte eigenen PDF-Reader (holte 0 Zeichen).
- **Lösung:** Bereits getestete Skill-Vorlagen nutzen, nicht selbst neu bauen.
- **Stand:** 2026-06-24
- **Quelle:** KW_24, Robert-Agent Regel 10

### L009: ollama serve kann abstürzen
- **Fehler:** Verwaister `llama-server.exe` hielt 10 GB VRAM.
- **Ursache:** `ollama serve` crasht still.
- **Lösung:** Prozess-Status prüfen, ggf. neu starten.
- **Stand:** 2026-06-24
- **Quelle:** KW_24

### L010: ClaudeEyes Calibration Device-Specific
- **Fehler:** ClaudeEyes hard auf `PCSarah` verdrahtet → Screenshots/Logs falsch.
- **Lösung:** `device.py` als Single Source of Truth (Hostname → Device-Name).
- **Stand:** 2026-06-24
- **Quelle:** KW_24, ClaudeEyes V0.02

---

## Infrastruktur & Deployment

### L011: EDEADLK bei Cloud-Files (OneDrive dataless)
- **Fehler:** `OSError [Errno 45] EDEADLK` beim sendfile auf OneDrive-Platzhaltern.
- **Ursache:** `sendfile()` kann nicht auf `dataless` Platzhalter angewendet werden.
- **Lösung:** Datei selbst in den Speicher lesen (umgeht sendfile), dann senden.
- **Stand:** 2026-06-23
- **Quelle:** KW_23, JustReise

### L012: LaunchAgent-Prozesse dürfen Cloud nicht synchronisieren
- **Fehler:** LaunchAgent bekommt EDEADLK statt zu blockieren.
- **Lösung:** Alle Dateien einmal aus interaktiver Shell materialisieren, nicht über LaunchAgent.
- **Stand:** 2026-06-23
- **Quelle:** KW_23, JustReise

### L013: Netlify Forms senden keine Mails automatisch
- **Fehler:** Netlify Forms senden keine Emails ohne separate Einrichtung.
- **Lösung:** Email-Notifications pro Site separat einrichten.
- **Stand:** 2026-06-24
- **Quelle:** KW_24

### L014: PAT-Token in alten Backups sichtbar
- **Fehler:** PAT-Token war in alter OneDrive-Backup-Kopie sichtbar.
- **Lösung:** Token revoken/rotieren, Backup-Kopien prüfen.
- **Stand:** 2026-06-24
- **Quelle:** KW_24

### L015: Nominatim Query-Vereinfachung
- **Fehler:** Geocoding mit vollem String scheitert (0 Treffer).
- **Lösung:** Query vereinfachen: Name → Name+Stadt → Name+Stadt+PLZ (Fallback).
- **Stand:** 2026-06-23
- **Quelle:** KW_23, JustReise

---

## Hardware & Cluster

### L016: Clustern macht keinen Sinn (M4 Bottleneck)
- **Fehler:** exo-Cluster-Test zeigte: M4-Bandbreite (~120 GB/s) ist Bottleneck, nicht Clustering.
- **Erkenntnis:** Cluster lohnt erst ab M4 Max/Ultra + RDMA + Modell zu gross für 1 Gerät (70B+).
- **Stand:** 2026-06-08
- **Quelle:** KW_24, exo-Cluster-Test

### L017: Tailscale ≠ Internet
- **Fehler:** Falsche Annahme dass Tailscale-Netz Internet-Zugang hat.
- **Lektion:** Tailscale = privates Netz, KEIN Internet.
- **Stand:** 2026-06-23
- **Quelle:** KW_23, CONVENTIONS

### L018: Raspberry Pi 5 OV5647 Camera nicht ansprechbar
- **Fehler:** OV5647 antwortet nicht auf I²C.
- **Vermutung:** Kabel-Problem.
- **Stand:** 2026-06-25
- **Quelle:** KW_26, PiCrawler

### L019: PiCrawler Pin 11 defekt
- **Fehler:** Pin 11 defekt (rot markiert in Pin-Karte).
- **Lektion:** Pin 11 nicht verwenden für zukünftige Projekte.
- **Stand:** 2026-06-25
- **Quelle:** KW_26, PiCrawler

---

## Struktur & Organisation

### L020: Nichts löschen, gelöscht bleibt gelöscht
- **Prinzip:** Justins Vorgabe "nichts wiederherstellen, deleted bleibt deleted, bauen wir neu auf".
- **Umsetzung:** Tote Links entfernen (Klammern raus), Klartext bleibt. Keine Wiederherstellung gelöschter Dateien.
- **Stand:** 2026-06-24
- **Quelle:** KW_24, Nexus-Umbau

### L021: Master-Files an der Wurzel = Single Source
- **Prinzip:** README.md an der Wurzel = Single Source of Truth, daraus werden Deck (PowerPoint) und AGENTS.md generiert via `projectfusion.py`.
- **Stand:** 2026-06-24
- **Quelle:** KW_24, Projekt-Norm

### L022: 1 README pro Ordner
- **Konvention:** "1 README pro Ordner" — bisher fehlte viele READMEs.
- **Stand:** 2026-06-22
- **Quelle:** KW_22

### L023: Frontmatter-Konsistenz
- **Fehler:** Alte `name:""+metadata:`-Form → flaches Schema (`title:`).
- **Lösung:** Frontmatter-Sweep auf flaches Schema migrieren.
- **Stand:** 2026-06-22
- **Quelle:** KW_22

---

## Acino & Beruf

### L024: CirQit-OpenAPI-Achievement (358 Anlagen)
- **Fakt:** LinkedIn-Refresh 24.05.2026 — CirQit-OpenAPI mit 358 Anlagen erwähnt.
- **Lektion:** Berufliche Erfolge dokumentieren und sichtbar machen (LinkedIn).
- **Stand:** 2026-05-24
- **Quelle:** KW_21

### L025: SALär vs. Nachzahlung klar trennen
- **Fehler:** April 2026 (6'130.90) vs. Mai 2026 (5'780) verwirrend.
- **Erkenntnis:** Lohnerhöhung 04.2026 (CHF 77'042/Jahr) — April war einmaliger Nachzahlung-Bestandteil.
- **Lektion:** Salär und Nachzahlungen klar trennen in Dokumentation.
- **Stand:** 2026-05-26
- **Quelle:** KW_22

---

*Stand: 2026-06-25 — 25 Lessons Learned gesammelt.*