---
title: Ai-Fight-Club
type: note
status: aktiv
updated: 2026-06-24
---

# AI Fight Club · App

Status: aktiv  ·  Version: 6.0.0-dev  ·  Letztes Update: 2026-06-12

## Zweck
Liga-Arena für lokale LLMs. ~95 Ollama-Modelle treten auf demselben Rechner (JUSTINGAMINGPC, RTX 3090) in 5 Disziplinen × 3 Level an. Bewertet wird das **echte Artefakt auf der Platte**, nicht die Behauptung des Modells. Zeigt, welches kleine Modell „über seiner Gewichtsklasse boxt".

## Stack / Technik
- Python; Ollama lokal (`/api/chat`, `localhost:11434`). Binary auf `D:\ollama\app\ollama.exe` (nicht im PATH), Modelle `D:\ollama\models`.
- Drei Runner pro Modell: `native_runner` (echte Tool-Calls, streng), `text_runner` (reines Sprachmodell), `lenient_runner` (Text-Tool-Calls tolerant geparst).
- Hybrid-Judge `grade_model.py` (deterministisch + Code-Ausführung + Heuristik/Schiri). Single-File-Board `board6.py` → offline HTML.

## Stand / Funktionen
- 95 Modelle im Roster, 85 nativ getestet. Top nativ: gemma4 273, qwen3:4b 249, qwen2.5:7b 219 (von 300).
- Kern-These belegt: nativ-0-Modelle (kein Tool-Format) holen als reines Sprachmodell oft 100–180/300.
- Scoring: Σ(Sterne×Level) je Skill (max 60), Gesamt max 300, Pound-4-Pound = Score ÷ VRAM-GB.
- Board: Podium/Liga-Tabelle, Weg-Switcher (nativ/lenient/text), VS-Modus, Radar-Profile, Divisionen.

## Betrieb
- Läuft lokal auf JUSTINGAMINGPC (RTX 3090), nicht Mac mini. Topologie nach ProjectNorm V5: Code unter `Code/`.

## Verweise
- Quelle: 10_Apps/AI Fight Club/
- Verwandt: [[project-norm|ProjectNorm]]; früher Stack `opencode → smol_proxy → Ollama` (zerstörte Tool-Calls → Runner direkt)
