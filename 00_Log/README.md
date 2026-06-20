---
title: 00_Log — Wochenlogs-Index
aliases: ["_log-index"]
description: Lies bei Frage "was wurde wann gemacht". Jahres-Topologie (JJJJ/KW_NN), verbindliches Eintrags-Muster + Workflow zum Anlegen einer neuen Woche.
type: index
status: aktiv
updated: 2026-06-08
---

# 00_Log — Wochenlogs

> Topologie seit 2026-06-08: **Jahr zuerst, dann Kalenderwoche** — `00_Log/<JJJJ>/KW_NN/LOG.md`.
> Pro KW eine `LOG.md`, chronologisch, neueste oben, **append-only**.
> Aktuelle Woche: **2026/KW_25** → [[KW_25/LOG|KW 25]]

## Topologie

```
00_Log/
├── 2026/  KW_09, KW_12 … KW_25   (aktuelles Jahr)
├── 2025/  KW_01, KW_40
├── 2023/  KW_31
├── 2022/  KW_14, KW_35
├── 2019/  KW_31
├── 2005/  KW_07
└── 2002/  KW_46
```

- **`<JJJJ>/`** = ein Ordner pro Jahr, das Einträge hat. Es gibt **keinen Sammel-Ordner** — jede KW liegt in ihrem echten Jahr (auch alte: 2005, 2002 …).
- Einträge sind nach **ISO-Kalenderwoche** abgelegt (z.B. 1. August = KW 31). Dieselbe KW kann in mehreren Jahren existieren (z.B. `2019/KW_31` + `2023/KW_31`) — die Jahres-Ebene trennt sie sauber.
- Leere Wochen werden **nicht** auf Vorrat gehalten (2026-06-08 alle entfernt).

## Verbindliches Eintrags-Muster (EINHEITLICH)

```
log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde gemacht>   → [[stem]] [[stem]]
```

- **Kein** Bindestrich davor (`- log …` wurde 2026-06-08 vereinheitlicht zu `log …`).
- Neueste Einträge **oben**, eine Leerzeile zwischen Einträgen, Zeit unbekannt → `--:--`.
- Persona/Gerät klar nennen (z.B. `Claude Code (Mac mini)`, `Luna (Hermes)`). Querverweise am Ende: `→ [[stem]]`.
- **Append-only:** alte Einträge nie editieren/löschen — gilt jetzt als Disziplin (der erzwingende `check_append_only.py`-Hook wurde 2026-06-14 mit `_tools/` entfernt).

## Scope-Regel

Im nexus ist `00_Log/.../LOG.md` das **zentrale Log-System**.

- Wenn Justin oder ein Bot einfach nur **"log"** sagt, ist standardmässig dieses Wochenlog gemeint.
- Bot-lokale Dateien unter `30_Agenten/<Bot>/` gelten **nicht** als das zentrale Log, sondern als lokale Arbeitsnotizen mit Funktionsnamen wie `handoff.md` oder `improvement-log.md`.
- Details dazu: [[30_Agenten/LOGGING]].

## Neue Kalenderwoche anlegen (Workflow)

**Sobald eine neue KW beginnt und `<aktuelles Jahr>/KW_NN/LOG.md` fehlt:** anlegen.

1. `mkdir -p 00_Log/<JJJJ>/KW_NN` (z.B. `00_Log/2026/KW_25`).
2. `LOG.md` aus der Vorlage erstellen:

```markdown
---
title: LOG KW NN
description: Log-Einträge für Kalenderwoche NN (JJJJ: TT.MM.–TT.MM.)
type: log
kw: NN
range: TT.MM.–TT.MM.JJJJ
entries: 0
---

# LOG KW NN  (JJJJ: TT.MM.–TT.MM.)

Neueste Einträge oben. Format: `log TT.MM.JJJJ HH:MM <Gerät/Persona> — <was wurde gemacht>`

<!-- noch keine Einträge -->
```

3. Danach `TREE.md` von Hand nachziehen, falls sich die Topologie geändert hat (das frühere `_tools/gen_tree_index.py`-Autogen wurde 2026-06-14 entfernt).

> Der `entries:`-Zähler im Frontmatter ist optional und keine Audit-Quelle — kann beim Eintragen einfach ignoriert werden (siehe `offen.md`).

## Kontext-Hubs

- [[profile]] — Person · [[acino-job]] — Acino/Arcera · [[itintech-firma]] — Firma
- [[20_Projekte/README]] — Projekte · [[service-ports]] · [[storage-cloud]] — Infrastruktur · [[linkedin]]

## Vorhandene Wochen (Stand 2026-06-08)

### 2026
[[KW_09/LOG|KW 09]] · [[KW_12/LOG|12]] · [[KW_13/LOG|13]] · [[2026/KW_14/LOG|14]] · [[KW_15/LOG|15]] · [[KW_16/LOG|16]] · [[KW_17/LOG|17]] · [[KW_18/LOG|18]] · [[KW_19/LOG|19]] · [[KW_20/LOG|20]] · [[KW_21/LOG|21]] · [[KW_22/LOG|22]] · [[KW_23/LOG|23]] · [[KW_24/LOG|24]] · [[KW_25/LOG|25]] ⭐

### 2025
[[2025/KW_01/LOG|KW 01]] (Militär-Kaderausbildung) · [[2025/KW_40/LOG|KW 40]]

### Frühere Jahre (Lebens-Meilensteine nach ISO-Woche)
- **2023:** [[2023/KW_31/LOG|KW 31]] (Acino-Start)
- **2022:** [[2022/KW_14/LOG|KW 14]] (Sarah) · [[2022/KW_35/LOG|KW 35]]
- **2019:** [[2019/KW_31/LOG|KW 31]] (Lehrbeginn)
- **2005:** [[2005/KW_07/LOG|KW 07]]
- **2002:** [[2002/KW_46/LOG|KW 46]]
