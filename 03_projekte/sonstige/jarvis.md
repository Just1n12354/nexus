---
title: Jarvis
type: note
status: aktiv
updated: 2026-06-24
---

# Jarvis · App

Status: aktiv  ·  Version: 0.002  ·  Letztes Update: 2026-06-14

## Zweck
Lokaler, privater Sprach-/Aktions-Assistent auf Justins eigener Hardware: Sprache rein → verstehen → ECHTE Aktion ausführen → antworten. Kein Cloud-Zwang, Daten bleiben lokal/im Tailnet. Orchestrierungs-Schicht, die ein lokales LLM mit Justins Diensten verbindet — kein eigenes LLM (das ist ~10% der Arbeit, 90% sind Tool-Layer + Audio-Pipeline).

## Stack / Technik
- Pipeline: Mikrofon → STT → LLM-Orchestrator → TTS → Lautsprecher, plus Tool-Layer + Kurzzeit-Memory.
- STT: MLX-Whisper (Mac) / faster-whisper (Windows, GPU). LLM: Ollama (Deutsch → gemma2; Reasoning-Modelle wie qwen3 für Latenz meiden). TTS: Edge-TTS de-CH-JanNeural (für „voll lokal" später Piper).
- Tool-Inventar = bestehende Just*-APIs (JustTodo, JustFinancePrivate/Business, JustLauncher), Nexus lesen, Shell eng per Whitelist.

## Stand / Funktionen
- Zwei Instanzen: Mac (primär, always-on Mac mini) + Windows (optionale GPU-Instanz, RTX 3080).
- Mac: `briefing.py` läuft (Datum/Wetter/Kalender/Todos → gemma2 formuliert → Edge-TTS), `voice_chat.py` Push-to-talk funktioniert.
- Windows: Voice-Stack v3.001 läuft (faster-whisper GPU), 28 Unit- + 4 Integrationstests grün (2026-06-13). Open WebUI auf Port 3000.
- Verworfen: OpenJarvis v1.0 (Core-Bugs), qwen3-Reasoning für Latenz, opencode für agentic Tool-Calling.
- Phasen-Gates gegen Scope-Falle: 0 Konzept ✓ → 1 Text-Agent → 2 Stimme (<5s) → 3 always-on Mac mini → 4 Wake-Word/Komfort.

## Betrieb
- Mac mini (24/7) primär, via Tailscale erreichbar; Windows als GPU-Zweitinstanz. Open WebUI Port 3000.

## Verweise
- Quelle: 10_Apps/Jarvis/
- Verwandt: [[aieyes]] (computer-use), AIWorld/Luna (Jarvis = deren Sprach-Frontend), [[just-todo|JustTodo]], [[just-finance-private|JustFinancePrivate]]
