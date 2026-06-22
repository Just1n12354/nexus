---
title: LOG KW 26
description: Log-Einträge für Kalenderwoche 26 (Referenz 2026: 22.06.–28.06.2026)
type: log
kw: 26
range_2026: 22.06.–28.06.2026
entries: 1
---

# LOG KW 26  (Referenz 2026: 22.06.–28.06.2026)

Neueste Einträge oben. Format: `log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde gemacht>`

log 22.06.2026 12:25 Claude Code (Linux / NVIDIA GB10 «DGX Spark», gx10-bf12) — **/push: 1 Repo gepusht + AI-Fight-Club-Benchmark repariert.** **[[itintech-firma]] / Itin-TechSolutions** `a0cad2a` (`fix:`) — **Benchmark-Bewertung war kaputt, jetzt korrekt.** Justin liess Liga 1 (122 lokale Ollama-Modelle) über Nacht durchlaufen; beim Prüfen fiel auf: **Coding + Thinking-l2/l3 bei ALLEN 118 Modellen 0/60** — weil **pytest fehlte**, schlug der Hidden-Test-Runner (`engine/hidden_runner.py` ruft `python -m pytest`) still fehl (kein Crash, 0/N). Decke lag bei 180/300, gpt-oss:120b gleichauf mit qwen3:4b. **Fix ohne Neulauf:** pytest installiert (`--break-system-packages`) + `requirements.txt` angelegt (verhindert Wiederholung), Liga 1 aus den gespeicherten `results/raw/`-Outputs **neu bewertet** (`tools/regrade.py`, 79 s, kein Ollama) → Schnitt **124→183**, qwen2.5-coder:32b 180→**290**, GLM/gpt-oss:120b korrekt auf 280. **Zwei weitere Bugs gefixt:** (1) `parse_files` crashte bei „Schwätzer"-Modellen (exaone-deep, lfm2.5) mit „File name too long" (Rambling als Dateiname) → kappen/mappen statt crashen; die **4 Ausgefallenen nachgewertet**, `lfm2.5:8b-a1b-q8_0` (210) kam dadurch fair in die Top 60. (2) `build_prompt` versteckte die **Eingabedatei** vor dem Modell, wenn sie als `ref` diente (toolcalling-Kopier-Aufgaben unmöglich) → im Aufgabentext genannte Inputs sichtbar lassen, echte Lösungs-Refs (`erwartet_*`) bleiben versteckt (greift für **Liga 2–5**, Liga 1 bleibt intern fair/unverändert). (3) Watchdog-Marker-Bug: Wrapper schrieb „FERTIG" nur auf Telegram, nicht ins Log → Watchdog startete endlos Neu-Läufe (4 Zombie-Prozesse aufgeräumt), jetzt `print` ins Log. **Liga 2 gestartet** mit dem korrekten **Top-60-Schnitt** (`tools/prepare_liga2.py`, deterministischer Tiebreak; `start_liga2.sh` mit `--models ""` → liest `qualifiers.json` statt versehentlich aller 128), Telegram-Pings an. **Übersprungen:** PrivateBackup (behind 1 — fremder Commit, nicht meine Arbeit; erst `pull` nötig), Rest sauber. → [[itintech-firma]] [[rechner-gb10]] [[claudesync]]
