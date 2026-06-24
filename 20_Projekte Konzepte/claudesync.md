---
title: Claudesync
type: note
status: aktiv
updated: 2026-06-24
---

# ClaudeSync · App

Status: prototyp  ·  Version: 0.006 (Milestone V0.02)  ·  Letztes Update: 2026-06-14

## Zweck
Single Source of Truth für Justins Claude-Code-Konfiguration über ALLE Geräte (MacBook Air M4, Mac mini, Gaming-PCs). Jedes Gerät bekommt dieselben Hooks, Settings, Keybindings, globalen Instruktionen; Abweichungen werden beim Sync erkannt und (reversibel) aufgeräumt.

## Stack / Technik
- Quelle = `claude/` (Soll-Zustand, wird nach `~/.claude/` gespiegelt). Motor = `bootstrap.sh` / `bootstrap.ps1` (einmal pro Gerät).
- `manifest.json` (Soll-Liste), `local/<hostname>.json` (geräte-spezifische Overrides). Fremdes wandert nach `~/.claude/_attic/<ts>/` statt löschen.
- Mitgelieferter `/push`-Slash-Command + read-only Scan-Helfer `push_scan.py` (geräte-weiter Commit/Push im Watson/Conventional-Commits-Stil + nexus-Wochenlog).

## Stand / Funktionen
- Lauffähiges Gerüst, noch nicht mit der echten produktiven `~/.claude`-Config befüllt.
- **Token-Lehre V0.02** (auf JUSTINGAMINGPC aufgedeckt): ein lokaler `UserPromptSubmit`-Hook injizierte pro Prompt die volle TREE.md (~23,5 KB) → ein Task fraß ~700k Tokens. Fix: Vault-Bootstrap gehört in **SessionStart** (1×/Session, 1,3 KB), nie per-Prompt.
- Windows braucht Pflicht-Override `local/<COMPUTERNAME>.json` (Basis-settings verdrahtet bash-Hook, läuft auf Windows nicht).
- tree.md-Überschrift muss == `%COMPUTERNAME%` sein (Hook schneidet per exaktem Match aus).

## Betrieb
- Pro Gerät `bootstrap` ausführen; Default Symlink-Spiegelung (`--copy` für rsync-Kopie).

## Verweise
- Quelle: 10_Apps/ClaudeSync/
- Hängt an nexus `MASTER.md` (Routing-Zeiger statt Volltext-Dump). Verwandt: [[projectnorm]]
