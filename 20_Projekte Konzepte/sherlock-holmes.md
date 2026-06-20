# Sherlock Holmes · App

Status: prototyp  ·  Version: 0.004  ·  Letztes Update: 2026-06-14

## Zweck
Recherche-Agent: Justin stellt eine Idee formlos vor, Sherlock durchsucht GitHub und Reddit (später mehr), ob es dazu schon wiederverwendbare Open-Source-Projekte gibt. Leitprinzip: erst suchen, was es gibt — dann erst selbst bauen. Spart Zeit/Geld.

## Stack / Technik
- `Code/sherlock.py` (Python-Stdlib only, kein pip, kein LLM in Phase 1).
- GitHub Search API (Qualifier stars/license/language, sort=stars). Token einplanen: ohne 60 Anfragen/h, mit PAT 5'000/h.
- Reddit heikel (seit Policy 11.11.2025 freigabe-pflichtig + limitiert) → zunächst nur via Websuche (`site:reddit.com`).

## Stand / Funktionen
- Phase 1 LÄUFT: Prototyp durchsucht live GitHub, rangiert Treffer (Sterne, Lizenz, letzter Push, Heuristik), gegen echte API getestet. Markdown-Bericht (`--md`).
- Phase-0-Befund: kein fertiges Tool macht genau „Idee rein → wiederverwendbare Repos raus" → schlanke Eigenbau-Orchestrierung gerechtfertigt.
- Gelernt: GitHub verknüpft Volltext mit UND → ganzer Ideen-Satz trifft oft 0; OR-Fallback wird zu breit. → präzises Ableiten der Suchbegriffe ist der Hebel (Phase 2, LLM).
- Phasenplan: 0 Konzept ✓ → 1 Prototyp ✓ → 2 LLM (Begriffe ableiten + bewerten) → 3 Reddit/Awesome → 4 als Claude-Skill verpacken (ProjectNorm-Workflow).
- Empfehlung pro Treffer: NEHMEN / UMBAUEN / VERWERFEN.

## Verweise
- Quelle: 10_Apps/Sherlock Holmes/
- Dockt evtl. vor „neues Konzept bauen" an: [[projectnorm]]
