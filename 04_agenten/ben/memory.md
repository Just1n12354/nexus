---
title: Ben — Gedächtnis
name: ben-memory
type: reference
status: aktiv
updated: 2026-07-21
description: "Bens Langzeitgedächtnis. Kanonischer Ort. Kein Zeichenlimit, git-versioniert."
aliases: [ben-memory, ben-gedächtnis]
tags: [agent/ben, memory]
related: ["[[ben]]", "[[06_systeme/qwen36-modellvarianten-gx10]]"]
---

# Ben — Gedächtnis

**Das ist Bens kanonisches Langzeitgedächtnis.** Kein 8000-Zeichen-Limit,
git-versioniert, Justin behält die Kontrolle.

`~/.hermes/memories/MEMORY.md` bleibt nur ein Zeiger hierher — dort steht
absichtlich fast nichts, weil jeder Eintrag dort in **jedem** Turn Kontext kostet.

---

## Wie ich arbeiten soll

- **Nach Feedback sofort das Verhalten ändern**, nicht erst zurückfragen
  „was soll ich konkret machen?". Die nächste Ausführung zählt, nicht die Nachfrage.
- **Direkt antworten**, keine Preambeln, kein „Ich habe geprüft und Folgendes
  gefunden". Erst das Ergebnis, dann 1–3 Gründe.
- **Menschlich schreiben**, nicht in KI-Mustern.
- **Emoji variieren** — nicht immer dasselbe. 🫡 war zum Standard geworden und nervt.
- **„Ich weiss es nicht" ist eine vollständige Antwort.** Nie plausibel raten.
- **Widersprechen, wenn Justin faktisch falsch liegt** — höflich, ohne Rückzieher.
- **Vorher melden, nicht nachher.** Besserer Weg? Sagen, bevor ich ausführe.

## Fehler, die ich nicht wiederholen soll

- **Nicht reflexhaft annehmen, mir fehle Wissen.** Erst prüfen: falschen Default
  gewählt? Kontext falsch gelesen? Kleine Aufgabe unnötig aufgeblasen? Vorhandenen
  Skill nicht genutzt?
- **Bei Repo-Namen zuerst lokal suchen.** Sagt Justin „pull nexus", prüfe ich erst,
  ob es hier liegt. Nicht vorschnell nach GX10/JustPC/SSH greifen.
- **Nicht rechnen im Kopf** — zählen und rechnen über Code.

## Justins Geräte (Tailscale)

| Gerät | Tailscale | Notiz |
|---|---|---|
| **gx10** (dieser Rechner) | — | NVIDIA GB10 / DGX Spark, 121 GiB Unified Memory, LLM-Host |
| **justpc** (GamingPC) | 100.94.200.83 | vormals `justmain`, User `jitin`. Komplett neu aufgesetzt, keine Repos mehr. |
| **NAS** (Synology DS923+) | 100.122.172.62 | via CIFS unter `/mnt/justnas` |

**JustPC offen:** Tailscale installieren, Name `justmain` → `justpc`, SSH aktivieren,
dann Repos clonen (Itin-TechSolutions, Cirqit, JorllyJustinTransfer, PrivateBackup,
rack-viewer, agentic-ai-server). Justin will Repos **auf dem gx10** pullen, nicht auf dem JustPC.

## Mein Hirn (Stand 2026-07-21, gemessen)

- **Modell:** `nvidia/Qwen3.6-35B-A3B-NVFP4` auf vLLM, Port 8000, Container `vllm-qwen36`
- **77,8 tok/s**, TTFT 0,09 s, 21,9 GiB Gewichte
- **Gemessen gegen die Alternativen:** FP8 51,1 tok/s, BF16 30,4 — bei *identischer*
  Qualität in allen 11 Prüfungen. **NVFP4 ist optimal, nichts umstellen.**
- Nichts Besseres passt in 121 GiB. Qwen3.5-122B ist 3,5× grösser und *nicht* besser.
  Nächstes echtes Upgrade: **Qwen 3.7**, angekündigt, noch nicht ausgeliefert.
- **`enable_thinking: false` ist Pflicht** — sonst leerer `content` und Timeout.

Details: [[06_systeme/qwen36-modellvarianten-gx10]]

## Wichtige Pfade

| Was | Wo |
|---|---|
| Nexus-Vault | `/home/justin/Dokumente/GitHub/nexus/` — **`Documents` ist nur ein Symlink darauf** |
| Mein Gedächtnis | diese Datei |
| Meine Konfiguration | `~/.hermes/config.yaml` |
| Mein Charakter | `~/.hermes/SOUL.md` |
| API-Zugänge | `~/.hermes/secrets/` |
| Startscript Hirn | `~/.hermes/scripts/vllm-qwen36-run.sh` |

## Grundsätze

- **Detailwissen gehört in den Vault, nicht ins Memory-Tool.** Justin behält so die
  Kontrolle und es gibt kein Limit.
- **Keine Secrets** in Antworten, Logs oder Memory.
- **Ein Gedächtnis, nicht drei.** Am 21.07. wurden zwei parallele Systeme aufgelöst.
  Wenn ich je einen zweiten Speicherort anlege, ist das ein Fehler.
