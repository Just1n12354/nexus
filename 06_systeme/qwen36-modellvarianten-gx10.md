---
title: Qwen3.6-35B-A3B — Modellvarianten auf gx10
type: reference
status: aktiv
updated: 2026-07-21
description: "Welche Qwen3.6-35B-A3B-Varianten (BF16, FP8, NVFP4) lokal auf gx10 liegen, in welchen Ordnern, mit welcher Revision und Grösse — Grundlage für den geplanten A/B-Vergleich."
aliases: [qwen36-varianten, qwen3.6-modelle, modell-downloads-gx10]
tags: [infra/hardware, llm-local, vllm, gx10, modelle]
related: ["[[hardware]]", "[[02_hermes-infrastruktur]]"]
---

# Qwen3.6-35B-A3B — Modellvarianten auf gx10

Stand **2026-07-21**. Alle drei offiziellen Varianten liegen lokal und sind byte-genau
verifiziert. **Nur abgelegt — noch nichts gestartet, noch nicht verglichen.**

Volle Doku inkl. Prüfsummen und Startparameter-Vorschlägen:
`~/.hermes/ben-diagnostics/qwen36-model-downloads-2026-07-21/`
(`INVENTORY.md`, `SIZE-PLAN.md`, `DOWNLOADS.md`, `COMPATIBILITY.md`, `MANIFEST.json`,
`NEXT-BENCHMARK-PLAN.md`)

---

## Was liegt wo

| Variante | Pfad auf gx10 | Grösse | Revision | Status |
|---|---|---:|---|---|
| **NVFP4** (NVIDIA) | `~/.cache/huggingface/hub/models--nvidia--Qwen3.6-35B-A3B-NVFP4/snapshots/491c2f1e…` | 21,85 GiB | `491c2f1ea524c639598bf8fa787a93fed5a6fbce` | **produktiv** — Bens Hirn |
| **FP8** (Qwen) | `~/.cache/huggingface/hub/models--Qwen--Qwen3.6-35B-A3B-FP8/snapshots/95a723d0…` | 34,92 GiB | `95a723d08a9490559dae23d0cff1d9466213d989` | lag schon da, verifiziert |
| **Original BF16** (Qwen) | `/home/justin/models/qwen3.6-35b-a3b/original-bf16/` | 66,99 GiB | `995ad96eacd98c81ed38be0c5b274b04031597b0` | **am 21.07.2026 neu geladen** |

**Neu übertragen:** 66,99 GiB (nur das Original — die anderen beiden waren bereits
vollständig **und** exakt auf dem aktuellen Remote-Stand).
**Belegt zusammen:** 123,76 GiB. **Frei auf der NVMe danach:** 1109 GiB.

Alle drei: Apache-2.0, nicht gated, Architektur `Qwen3_5MoeForConditionalGeneration`,
`max_position_embeddings` 262 144. Sie unterscheiden sich **nur** in der Quantisierung.

---

## Merkposten

**Der HF-Cache ist der Produktionscache.** Der Container `vllm-qwen36` mountet
`/home/justin/.cache/huggingface` → `/root/.cache/huggingface`. Wer dort aufräumt,
räumt Bens Hirn weg. Deshalb liegt das neu geladene BF16 bewusst **ausserhalb**
unter `/home/justin/models/`.

**FP8 hat ein anderes Shard-Layout:** layerweise `layers-0…39.safetensors` plus
`outside.safetensors` und `mtp.safetensors` (42 Stück) statt der 3 Shards des NVFP4.
Beim ersten Start in Kombination mit `--load-format fastsafetensors` genau hinschauen.
Die `mtp.safetensors` deutet auf Multi-Token-Prediction — relevant, falls je
spekulatives Decoding getestet wird.

**BF16 ist auf dem GB10 grenzwertig.** 67 GiB Gewichte bei 121 GiB Unified Memory,
das sich alles teilen muss. Nur mit hoher `--gpu-memory-utilization` und stark
gekürztem Kontext, und **nie** parallel zur Produktion. Wert hat es als
Qualitäts-Referenz, nicht als Daueransatz.

---

## Benchmark-Ergebnis (21.07.2026, alle drei gemessen)

Wartungsfenster 14:31–15:33, Ben offline. Alle drei nacheinander auf Port 8000 unter
`--served-model-name nvidia/Qwen3.6-35B-A3B-NVFP4` — **Bens `config.yaml` blieb unangetastet**.
Identische Flags, `--max-model-len 32768` für alle, 8 Aufgaben × 3 Wiederholungen.

| | **NVFP4** | FP8 | BF16 |
|---|---:|---:|---:|
| Durchsatz Mittel | **77,8 tok/s** | 51,1 | 30,4 |
| relativ | **1,00×** | 0,66× | 0,39× |
| TTFT Median | **0,09 s** | 0,18 s | 0,24 s |
| Qualitätschecks (11) | alle ✅ | alle ✅ | alle ✅ |
| Fehlgeschlagene Läufe | 0/24 | 0/24 | 0/24 |

**NVFP4 gewinnt klar.** 1,5× schneller als FP8, 2,6× schneller als BF16 — bei *identischer*
Antwortqualität. Die Antworten waren teils wortgleich, Tool-Call-Argumente durchweg identisch.

**FP8 startet auf dem GB10 nur mit Sonderbehandlung:** drei Abstürze, weil vLLM blockweise
FP8-Skalen zwingend durch **DeepGEMM** schickt und dessen Kernel das Layout hier nicht kennt
(`Unknown SF transformation` / `Unknown recipe`). Erst
`VLLM_USE_DEEP_GEMM=0` + `VLLM_MOE_USE_DEEP_GEMM=0` + `--moe-backend triton` brachte es hoch.
BF16 lief dagegen auf Anhieb.

→ **Fazit: bei NVFP4 bleiben, nichts umstellen.** FP8 abhaken, BF16 nur als Qualitätsreferenz
behalten. Voller Bericht: `~/.hermes/ben-diagnostics/qwen36-model-downloads-2026-07-21/BENCHMARK.md`

## Offene Punkte

- **Echter Hebel:** Produktion läuft auf `--gpu-memory-utilization 0.40`, obwohl der Kommentar
  im Startscript `0.70` behauptet. Ungenutzter Spielraum für Prefix-Cache — das wäre der
  nächste sinnvolle Test, nicht ein weiterer Modellwechsel.
- **HF-Token liegt im Klartext** in `~/.hermes/scripts/vllm-qwen36-run.sh` und in der
  Container-Env (`docker inspect` liest ihn). Rotieren und in eine Env-Datei auslagern.

Bewusst **nicht** geladen: GGUF, MLX, AWQ, GPTQ, abliterated/uncensored, distill- und
„Fast"-Forks. Einordnung ebenfalls im Benchmark-Plan.
