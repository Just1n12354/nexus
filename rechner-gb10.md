---
title: Rechner GB10
type: reference
status: aktiv
description: NVIDIA GB10 (DGX Spark) — Host-Device für Ben, vLLM, Minecraft-Bots.
tags: [infra, gb10, gx10, hardware]
---

# Rechner GB10

> Detaillierte Hardware-Spezifikationen und Konfiguration: [Rechner GB10](../Itin-TechSolutions/Rechner-Profil_GB10.md) (Itin-TechSolutions-Repo).

Der NVIDIA GB10 (auch DGX Spark genannt) dient als lokaler AI-Host auf Tailscale `100.75.47.118`.
Darauf laufen:

- **Ben** — Hermes-Agent (Ollama gpt-oss:120b)
- **vLLM** — lokaler LLM-Endpoint (Qwen3.6-35B)
- **Minecraft-Bots** — Peter, Olaf (mineflayer)
- **Git-Nexus** — `~/Documents/GitHub/nexus`
