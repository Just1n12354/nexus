# MinecraftAI — Bot „Peter"

Kurz: Eigener lokaler Minecraft-Server + KI-Mitspieler **Peter** auf **gx10**, gebaut am
2026-07-08 mit reinem **mineflayer** (Ersatz für das gelöschte Olaf/Ben-Projekt).

## Server
- **Paper 1.21.4** (build 232), Java 21, in `~/minecraft-server/`. Start: `./start.sh`.
- Join über **Tailscale**: `100.75.47.118:25565`. `online-mode=false` (damit der Bot joint), Justin ist OP.
- Feste Map (Seed `-8805009358920899152`).
- ⚠ **spark-Profiler aus** (`config/paper-global.yml` → `spark.enabled: false`) — crasht sonst die JVM
  auf ARM64. Läuft noch als loser Hintergrund-Task, **nicht** als systemd-Dienst.

## Bot Peter — `~/minecraft-bot/`
- Node 24 + mineflayer + mineflayer-pathfinder. Läuft als **systemd-User-Dienst** `mc-peter`
  (Auto-Restart, linger → reboot-fest). Nur EINE Instanz (sonst gegenseitiger Kick).
- Verwalten: `systemctl --user {status,restart,stop} mc-peter`, Logs `journalctl --user -u mc-peter -f`.
- **Chat/Denken** via lokalem vLLM **Qwen3.6** (`localhost:8000`). Nötig: `enable_thinking=false`
  und nur EINE `system`-Message (Qwen-Template-Eigenheiten).

### Was Peter kann
- **Reden:** antwortet frei im Chat, kurzes Gesprächsgedächtnis.
- **Bewegen:** „komm" / „folg mir" (Pathfinder zum Spieler), „stop".
- **Wahrnehmung als DATEN** (keine Vision-KI): Wesen (Distanz + Richtung), Nahfeld-Blöcke ehrlich
  (Türen/Planken/… ohne Doppelzählung mehrhoher Blöcke), Ressourcen im Umkreis, Biom/Zeit/Wetter,
  Blickpunkt, Inventar → alles als `[Wahrnehmung]` ins LLM. Kommando „was siehst du".
- **Craften:** „craft werkbank", „craft 4 stöcke", „baue truhe" — aus Inventar; 3×3-Rezepte brauchen
  eine Werkbank in ≤4 Blöcken. Meldet ehrlich, wenn Zutaten/Werkbank fehlen.
- **Gedächtnis-Dateien** (liest+schreibt selbst):
  - `AGENTS.md` — Persona/Regeln, live editierbar ohne Neustart.
  - `MEMORY.md` — Dauergedächtnis; „merk dir: …" oder LLM-`<merken>…</merken>`.

### Noch offen
- Blöcke abbauen/platzieren (Peter kann noch keine Werkbank selbst setzen).
- Server als systemd-Dienst (dann komplett reboot-fest).
- links/rechts-Konvention in `relDir()` gegenprüfen.

## Backup
Setup (ohne node_modules/re-downloadbares) auf NAS: `/mnt/justnas/MinecraftAI/`.
