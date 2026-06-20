# APIKeys

Status: aktiv  ·  Letztes Update: 2026-06-21

## Zweck
Sammelstelle für API-Keys / Bearer-Tokens, die der nexus-Vault braucht.

## Wichtig — bewusst eingecheckt
- Die Keys in diesem Ordner werden **absichtlich** ins (private) nexus-Repo committet und gepusht.
  Das ist Justins ausdrückliche Entscheidung (2026-06-21), nicht ein Versehen.
- Voraussetzung: Das nexus-Repo bleibt **privat** (`github.com/Just1n12354/nexus`).
- Bewusstes Risiko: Ein einmal gepushter Key gilt als exponiert — GitHub kann ihn cachen/indexieren,
  auch nach späterem Löschen. Bei Verdacht auf Leak / Repo-Wechsel auf public → Key **rotieren**.

## Inhalt
- `BraveAPI.txt` — Brave Search API
- `Telegram.txt` — Telegram (vgl. Ping-Bot `@pingitintechbot`)

## Verweise
- Weitere Keys außerhalb nexus: Mac mini `~/LocalSecure/Keys/`, PC `C:\Users\jitin\LocalSecure\Keys\`.
