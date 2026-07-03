---
title: 00_Log — Wochenlogs
type: moc
status: aktiv
updated: 2026-06-25
description: Domänen-MOC für Wochenlogs im Nexus Vault.
---

# 00_Log — Wochenlogs

Append-only Log-System für alle Ereignisse im Vault.

## Struktur

- `00_Log/JJJJ/KW_NN/LOG.md` — Wochenlog pro Kalenderwoche
- Format: `log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde>`
- Neue Einträge immer oben (neueste zuerst)

## Siehe auch

- [[00_Log/README.md|README]] — Log-Topologie, Eintrags-Muster, Workflow