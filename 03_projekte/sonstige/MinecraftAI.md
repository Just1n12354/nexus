# MinecraftAI — Bot „Peter"

> 📖 Ausführliche Doku (Architektur, Aufgaben-Motor, Survival, Roadmap): [[MinecraftAI-Peter-Autonomie]]

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
- **Abbauen:** „grab stein", „bau kohleerz ab", „grab blick" (Block im Fadenkreuz) — läuft per
  Pathfinder in Reichweite und baut ab; meldet, wenn er nicht rankommt.
- **Platzieren:** „platzier werkbank", „setz truhe hin", „stell werkbank auf" — sucht ein freies
  Feld neben sich mit festem Boden und setzt den Gegenstand (kann sich so seine eigene Werkbank stellen).
- **Tool-Loop:** Das LLM kann selbst handeln, indem es `<tun>BEFEHL</tun>` in die Antwort schreibt
  (graben/platziere/craft/sammel/komm/stop/schauen). Max. 2 Runden pro Nachricht, Ergebnis geht ans LLM zurück.
  ⚠ Verlässlich sind die Keyword-Kommandos; der LLM-Loop (Qwen3.6 lokal, non-thinking) ist Kür und kann flakey sein.

### Autonomie (2026-07-09)
- **Aufgaben-Motor:** Ein Ziel läuft im Hintergrund über viele Ticks bis zum Abschluss, jederzeit per
  „stop" abbrechbar (Generation-Token). Ziele: `sammel holz N`, `mine/farm BLOCK N`, `geh zu X Y Z`.
  Mit Fortschritt, Timeout (5 Fehlversuche → Abbruch), ehrlichen Meldungen. Auch vom LLM per `<tun>` setzbar.
- **Survival-Tick (alle 3s):** Auto-Essen bei Hunger; **Selbstverteidigung** gegen feindliche Mobs —
  mit Waffe kämpfen (Pathfinder ranlaufen + `bot.attack`), bei HP≤6 fliehen. Verteidigung hat Vorrang
  vor Aufgaben. **Verifiziert:** brach einen Zombie-Death-Loop am Spawn (vorher Tod alle ~7s → danach Flucht, 0 Tode).
- ⚠ **Barhändig gewinnt Peter Kämpfe nicht** (Faust = 1 Schaden), er überlebt nur durch Flucht. Für echtes
  Bestehen braucht er eine Waffe im Inventar (per `/give` oder selbst craften) oder Tag/Peaceful.
- **Gedächtnis-Dateien** (liest+schreibt selbst):
  - `AGENTS.md` — Persona/Regeln, live editierbar ohne Neustart.
  - `MEMORY.md` — Dauergedächtnis; „merk dir: …" oder LLM-`<merken>…</merken>`.

### Erledigt am 2026-07-08 (Codeseite, live noch von Justin zu verifizieren)
- Abbauen + Platzieren implementiert (inkl. eigene Werkbank setzen) — Keyword + LLM-Tool-Loop.
- `relDir()`-Bug gefixt: war `atan2(-dx, dz)` → vorne/hinten UND links/rechts vertauscht; jetzt
  sauber über den Blickvektor (mineflayer-Konvention `yaw=atan2(-dx,-dz)`). **Muss im Spiel gegengeprüft werden.**
- Robustheit: `end`→`process.exit(1)` (systemd `Restart=always`/5s reconnectet), globale
  `unhandledRejection`/`uncaughtException`-Logs.

### Noch offen
- Server selbst als systemd-Dienst (läuft weiter als loser Hintergrund-Task; Bot ist bereits Dienst).
- LLM-Tool-Loop in der Praxis tunen (Qwen3.6 non-thinking hält sich nicht immer ans `<tun>`-Format).

## Backup
Setup (ohne node_modules/re-downloadbares) auf NAS: `/mnt/justnas/MinecraftAI/`.
