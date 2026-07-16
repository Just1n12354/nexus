---
title: .env-Fallstrick
type: reference
status: aktiv
updated: 2026-07-15
description: Literal \\n in .env macht Zeilen zu Kommentaren
tags: [infra/.env, pitfalls]
---

# .env-Fallstrick

## Problem (14.07.2026 real passiert)
- In `/home/justin/.hermes/.env` standen literale `\n`-Zeichen statt echter Newlines
- Folge: Ganze Zeile wird zum Kommentar (`#...`)
- `OPENWEATHER_API_KEY` und `BRAVE_API_KEY` waren NIE gesetzt — ohne Fehlermeldung

## Korrektur
Echte Newlines beim Schreiben verwenden und danach prüfen:

```bash
set -a; . .env; set +a; echo "[$VARNAME]"
```

- Leerer Output = Zeile kaputt