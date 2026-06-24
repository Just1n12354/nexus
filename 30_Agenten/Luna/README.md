---
title: Readme
type: note
status: aktiv
updated: 2026-06-24
---

# Luna

Persistentes Brain von **Luna** im Vault. Luna ist die Hermes-Runtime, die live unter
`~/.hermes` läuft (Mac mini M4, gateway pid wechselt). Dieser Ordner ist der
**committete Spiegel** ihrer dauerhaften Identität + ein lokales Restore-Backup.

## Inhalt

| Datei/Ordner | Was | In Git? |
|---|---|---|
| `SOUL.md` | Lunas Wesen/Persönlichkeit (aus `~/.hermes/SOUL.md`) | ✅ |
| `TOPOLOGY.md` | Ihr Weltmodell / Topologie | ✅ |
| `config.yaml` | Hermes-Setup (api_keys leer → kommen via Bitwarden/env, **keine Secrets**) | ✅ |
| `memories/MEMORY.md` | Lunas Langzeitgedächtnis | ✅ |
| `memories/USER.md` | Was Luna über Justin weiss | ✅ |
| `_backup/` | **Vollständiger Restore-Snapshot** von `~/.hermes` (Tarball) | ❌ gitignored |

## Source of Truth

Die **lebende** SoT ist `~/.hermes`. Dieser Ordner ist ein Spiegel/Backup. Beim
Aktualisieren: aus `~/.hermes` hierher kopieren, nicht umgekehrt (sonst überschreibt
man Lunas live-Stand).

## Warum `_backup/` nicht in Git

Das Tarball enthält `.env` + `auth.json` (Telegram-/Brave-/Spotify-Tokens) und die
~160 MB `state.db`. Secrets gehören nicht in ein gepushtes Repo, und die DB würde das
Repo aufblähen → per `.gitignore` ausgeschlossen, bleibt nur lokal auf dem Mac mini.

Stand des Spiegels + Backups: **2026-06-21**.
