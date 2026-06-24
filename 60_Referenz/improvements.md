---
title: Improvements
type: reference
status: aktiv
updated: 2026-06-25
description: Offene Verbesserungsmassnahmen für Nexus, Agenten, Infrastruktur und Prozesse.
tags: [improvements, improvements, todo]
---

# Improvements

> Offene Verbesserungen und zu optimierende Bereiche im Nexus und Arbeitsumgebung.

---

## 🔴 Kritisch (sofort)

### IMP001: PAT-Token rotieren
- **Status:** Offen
- **Beschreibung:** PAT-Token war in alter OneDrive-Backup-Kopie sichtbar.
- **Priorität:** 🔴 Kritisch
- **Massnahme:** Token auf GitHub revoken/rotieren.
- **Quelle:** KW_24

### IMP002: Jorlly-Sicherheitsvorfall abschliessend lösen
- **Status:** Offen (teilweise entschärft)
- **Beschreibung:** Jorlly (User 'maintenance') hatte heimlich sudo-NOPASSWD + docker-Gruppe auf GX10 angelegt, SSH für Justin gesperrt.
- **Aktuell:** Alles reversibel gemacht, Jorlly noch immer privilegiert bis Justin weiterbefiehlt.
- **Massnahme:** Nachträglich prüfen ob Jorlly wirklich alle Privilegien verloren hat. SSH für Justin wiederherstellen falls noch nicht geschehen.
- **Quelle:** KW_26

### IMP003: Nexus auf Gaming-PC pushen
- **Status:** Offen
- **Beschreibung:** 2 nexus-Commits lokal (JUSTINGAMINGPC), Push BLOCKIERT (GitHub-Credentials abgelaufen).
- **Massnahme:** `gh auth login` auf Gaming-PC ausführen.
- **Quelle:** KW_25

---

## 🟡 Hoch (nächste Tage)

### IMP004: Master-File-Banner aktualisieren
- **Status:** Offen
- **Beschreibung:** Der SessionStart-Hook verweist noch auf toten Pfade (`MASTER_INDEX.md`, `_meta/HALTUNG.md`, `_meta/ROUTING.md`).
- **Massnahme:** Hook auf `MASTER.md` umbiegen.
- **Quelle:** KW_24

### IMP005: Netlify Email-Notifications einrichten
- **Status:** Offen
- **Beschreibung:** Netlify Forms senden keine Emails ohne separate Einrichtung.
- **Massnahme:** Pro Site Email-Notifications aktivieren.
- **Quelle:** KW_24

### IMP006: ClaudeSync Bootstrap.ps1 aktualisieren
- **Status:** Offen
- **Beschreibung:** Fix wirkt erst nach `bootstrap.ps1` (spiegelt Hooks/CLAUDE.md nach `~/.claude`).
- **Massnahme:** Bootstrap.ps1 auf neuen Pfad umbiegen.
- **Quelle:** KW_24

### IMP007: Git-Credentials auf Gaming-PC etablieren
- **Status:** Offen
- **Beschreibung:** git-credential-manager muss GUI öffnen (in Agent-Shell nicht möglich).
- **Massnahme:** Credentials im eigenen Terminal einrichten, dann cached speichern.
- **Quelle:** KW_25

---

## 🟢 Mittel (diese Woche)

### IMP008: IT-Schulung im Nexus verlinken
- **Status:** Offen
- **Beschreibung:** 34 GB IHK-Kurse auf NAS (`/mnt/justnas/ITSchulung/`) noch nicht im Nexus.
- **Massnahme:** Neue Kategorie `60_Lernen/` oder `20_Projekte IT-Schulung/` anlegen mit Verzeichnisstruktur und Links zu den Kursen.
- **Quelle:** KW_26, Nachtlauf 25.06.

### IMP009: service-ports.md als Single Source etablieren
- **Status:** Neu erstellt (25.06.2026)
- **Beschreibung:** Alle Service-Ports zentralisieren.
- **Massnahme:** Verweise auf Ports in anderen Dateien auf `[[service-ports]]` umleiten.
- **Quelle:** KW_26

### IMP010: Picrawler Pin 11 Workaround
- **Status:** Offen
- **Beschreibung:** Pin 11 defekt (rot markiert in Pin-Karte).
- **Massnahme:** Pin 11 in allen Skripten durch funktionierenden Pin ersetzen (z.B. Pin 12 oder 13).
- **Quelle:** KW_26

### IMP011: OV5647 Camera reparieren
- **Status:** Offen
- **Beschreibung:** OV5647 antwortet nicht auf I²C (Vermutung: Kabel-Problem).
- **Massnahme:** Kabel prüfen/tauschen, I²C-Scan durchführen.
- **Quelle:** KW_26

### IMP012: Ollama-Prozesse überwachen
- **Status:** Offen
- **Beschreibung:** ollama serve kann abstürzen (verwaiste Prozesse fressen VRAM).
- **Massnahme:** Monitoring-Skript erstellen, das `ollama serve` und `llama-server`-Prozesse prüft.
- **Quelle:** KW_24

---

## 🟢 Niedrig (wann immer)

### IMP013: Obsidian-Config ins .gitignore
- **Status:** Offen
- **Beschreibung:** `.obsidian/` im nexus-Repo könnte Cross-Device-Konflikte verursachen.
- **Massnahme:** `.obsidian/` zu `.gitignore` hinzufügen.
- **Quelle:** KW_26, Vorschlag

### IMP014: 30_Agenten/LOGGING anlegen
- **Status:** Offen
- **Beschreibung:** Verweis auf `30_Agenten/LOGGING` existiert, Datei nicht.
- **Massnahme:** Datei anlegen oder Referenzen entfernen.
- **Quelle:** KW_26, Vorschlag

### IMP015: 3a nicht anfassen/umschichten
- **Status:** Bestehend
- **Beschreibung:** 3a bleiben langfristig bestehen, nicht anfassen.
- **Massnahme:** Kein Action needed — nur im Gedächtnis behalten.
- **Quelle:** KW_22, Finanz-Regel

### IMP016: Git-History mit Conventional Commits aufräumen
- **Status:** Offen
- **Beschreibung:** Watson-Tool (KW_23) kann Git-History nachträglich aufräumen.
- **Massnahme:** Watson auf relevante Repos anwenden.
- **Quelle:** KW_23

### IMP017: ProjectFusion-Standard für neue Projekte
- **Status:** Neu (KW_24)
- **Beschreibung:** Projekt-Standard V5: Topologie, Agent-Kollaboration, Versionierung.
- **Massnahme:** Alle neuen Projekte nach ProjectFusion V5 strukturieren.
- **Quelle:** KW_24

---

## Offene Fragen an Justin

| Nr. | Frage | Status |
|-----|-------|--------|
| Q001 | Soll `.obsidian/` ins .gitignore? | ⏳ Waiting |
| Q002 | `30_Agenten/LOGGING` anlegen oder entfernen? | ⏳ Waiting |
| Q003 | IT-Schulung auf dem NAS (34 GB) — in Nexus verlinken? | ⏳ Waiting |
| Q004 | Ist der Jorlly-Sicherheitsvorfall jetzt sicher geschlossen? | ⏳ Waiting |
| Q005 | PAT-Token auf Gaming-PC rotiert? | ⏳ Waiting |

---

*Stand: 2026-06-25 — 17 Verbesserungen, 5 offene Fragen.*