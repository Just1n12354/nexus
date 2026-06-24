---
title: Watson — Git-History aufräumen
description: Watson: Nachträglich Git-History nach Conventional-Commits umschreiben, 1er-Commits entfernen, konsistente Messages sicherstellen
type: project
status: konzept
phase: 1
created: 2026-06-25
updated: 2026-06-25
tags: [projekt/git, watson, history, conventional-commits]
project: watson
---

# Watson — Git-History aufräumen

## Konzept

Watson ist ein Tool, das nachträglich die Git-History von Repos durchgeht und unstrukturierte Commit-Messages (wie `1` oder `fix`) in aussagekräftige Conventional-Commit-Messages umschreibt.

### Phase 1 (Prototyp)
- `watson.py`: backup/check/scan/diffs/apply/verify
- Rewriting nur Messages, keine Diffs neu anwenden (keine Konflikte)
- `git filter-branch --msg-filter` oder eigene Engine (filter-branch bei Merge-Konflikten)
- Commit-Template: Conventional-Commits-Pattern
- Backup per Tag vor Änderungen

### Phase 2 (Standardisierung)
- `watson install` auf alle Repos (zentrale `commit.template`)
- Watson-Vorlage als Standard in neue Projekte
- `Doku/STANDARD.md` als Single Source

### Erkenntnisse
- `git rebase` scheitert an echten Merge-Konflikten (zwei-Geräte-History)
- Zweite Engine `git filter-branch --msg-filter` ist konfliktfrei (nur Messages, keine Diffs)
- cp1252-Falle: Windows-subprocess liest git-Ausgabe als cp1252 statt UTF-8 → Mojibake

### Status
- Phase 1 auf Gaming-PC (DESKTOP-92I5S0F) prototypisch umgesetzt
- 5 Repos normalisiert (173 Commits nexus, 8 Merges erhalten)
- PrivateBackup, Itin-TechSolutions, nexus durchgelaufen

→  (Watson-Commit war von Claudio, nicht Watson-Session)