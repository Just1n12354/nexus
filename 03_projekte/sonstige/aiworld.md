---
title: AIWorld — KI-Agenten-Orchestrierung
description: AIWorld: zentrales Framework für die 5 Agenten (Felix, Frank, Bruno, Claudio, Luna) mit Persistenz-Memory, Streaming, und Bot-Routing
type: project
status: aktiv
phase: 6
created: 2026-06-25
updated: 2026-06-25
tags: [projekt/aiworld, agenten, orchestrierung, persistenz-memories, aiworld-protocol]
project: aiworld
---

# AIWorld — KI-Agenten-Orchestrierung

## Konzept

AIWorld ist das Framework zur Orchestrierung der 5 KI-Agenten-Familien (Felix, Frank, Bruno, Claudio, Luna) mit persistenter Memory, Streaming-Response, und Bot-Routing.

### Architektur
```
AIWorld (Flask-Server)
├── bots.json          (Konfiguration aller Bots)
├── aiworld.py         (Haupt-Server-Logik)
├── /bots/
│   ├── felix/         (Steuer-Experte)
│   ├── frank/         (Rechts-Experte)
│   ├── bruno/         (Elektro-Experte)
│   ├── claudio/       (Claude-Code/API-Experte)
│   └── luna.md/memory.md  (Explorer, nur Telegram-Bot)
├── /src/
│   └── aiworld.py     (AIWorld-Protokoll-Client)
└── version: 0.06
```

### Bot-Steckbriefe (Typisch)
- **Felix**: Steuer-experte (Felix, 4.0, Steuer, Finanzen, Steuern, Schweiz, CH, Tax)
- **Frank**: Rechts-experte (Frank, 4.2, Recht, Gesetz, Vertrag, Vertrag, Schweiz, CH, Law)
- **Bruno**: Elektro-experte (Bruno, 4.2, Elektro, Strom, Sicherheit, Installation, Schweiz, CH, Electric)
- **Claudio**: Claude-Code-experte (Claudio, 4.3, Claude, Code, Programmierung, API, Dev, Code, AI)
- **Luna**: Explorer, nur Telegram-Bot (Luna, 4.1, Allgemein, Fragen, Recherche, Chat, AI, General)

### Versionen (Stand 2026-06-25)
- **V0.06**: Persistente Bot-Memory (Memory-Verzeichnis pro Bot, Memory-Regeln in Steckbriefen)
- **V0.05**: Token-Level-Streaming (TTFT 23s → 3.6s, 24 deltas, NDJSON chunked)
- **V0.04**: Persona-Guard (Smalltalk/Pings fixt, Bot-Verhalten konsistent)
- **V0.02**: Erste Bot-Configs (bots.json, Steckbriefe, Memory-Verzeichnis)

### Features
- Memory pro Bot (auto-append bei Chat, mtime-Invalidierung)
- Streaming-Response (NDJSON, chunked)
- Concurrent-Test 3 Bots in 2.89s
- Bot-Steckbriefe (Typisch, 4.0, 4.2, 4.3, 4.1, 4.1)
- Routing via Steckbrief-Typisch (Wer ist für welche Domäne zuständig?)
- Persona-Guard (Smalltalk/Pings fixt, Bot-Verhalten konsistent)

### Status
- AIWorld v0.06: Persistente Bot-Memory (Memory-Verzeichnis pro Bot)
- Token-Level-Streaming (TTFT 23s → 3.6s, 24 deltas)
- Persona-Guard: Smalltalk/Pings fixt, Bot-Verhalten konsistent
- Routing via Steckbrief-Typisch (Wer ist für welche Domäne zuständig?)

→ [[aiworld.md]] (Hauptseite, Steckbriefe, Typisch, 4.0, 4.2, 4.3, 4.1, 4.1)
→  (Logging-Routing, Typisch für Bot-Konfigurationen, 4.0, 4.2, 4.3, 4.1, 4.1)