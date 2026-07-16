---
title: NAS-Operationen
type: reference
status: aktiv
updated: 2026-07-15
description: NAS-Regeln und Dateibehandlung auf dem Synology-Volume
tags: [infra/nas, operations]
---

# NAS-Dateioperationen

## Mountpoint
- `/mnt/justnas/...`

## #recycle/-Bin
- Löschen verschiebt nur, löscht nicht
- **VOR dem Löschen**: Immer mit `find` prüfen, ob Dateien noch existieren
- **Für Wichtiges**: `copy-then-delete`
- **Struktur**: Flach, nummeriert (00_, 01_, 02_), keine leeren Platzhalter-Ordner