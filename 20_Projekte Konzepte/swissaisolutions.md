# SwissAISolutions · App (Produkt)

Status: aktiv (Konzept)  ·  Version: 0.001  ·  Letztes Update: 2026-06-15

## Zweck
Plug-&-Play private KI-Box für Schweizer KMU: eigenes „ChatGPT", Daten bleiben on-premise in der Schweiz. Verkaufbares Produkt aus Projekt Solomon (ASUS Ascent GX10 + Software + Service). Der Wert ist NICHT die Box (Commodity), sondern Appliance-Image + Onboarding + monatliches Managed-Service-Abo (MRR).

## Stack / Technik (Ziel-Architektur)
- Inferenz: Ollama/vLLM/SGLang (OpenAI-kompatibel) auf der GX10. Modell: gpt-oss-120b (MoE).
- Web-UI: OpenWebUI (gebrandet, Nutzer/Rollen/Audit-Log). RAG (Plus/Pro): Ingestion → Embeddings → Qdrant → Retrieval.
- Produktwert = Management-Layer: reproduzierbares Image, Monitoring, Remote-Update, Backup, Health-Check, Lizenz/Abo.

## Stand / Funktionen
- Reines Produkt-/Geschäftskonzept, kein Code-Start. Volles Detailkonzept: `Doku/Produktkonzept.md`.
- Drei Pakete: Basic (LLM + Web-Chat), Plus (+ RAG über Firmendokumente), Pro (+ Agenten/Integrationen).
- Zielmarkt: Schweizer KMU mit Datenschutz-Druck (Treuhand, Kanzlei, Praxis, Broker), 5–30 MA. Eine Box trägt realistisch ~5–15 leichte gleichzeitige Nutzer.
- Offen vor Verkauf: Preise validieren, Berufshaftpflicht klären, Concurrency real testen. Nächste Phase: MVP-Stack auf der GX10, sobald Hardware da.
- Leitplanken: nie „100% sicher" versprechen (nur „on-premise CH"), MoE wegen GX10-Bandbreite (273 GB/s), Positionierung „guter privater Assistent" statt „ChatGPT-Ersatz".

## Verweise
- Quelle: 10_Apps/SwissAISolutions/ (Detail: Doku/Produktkonzept.md)
- Basis-Hardware/Knoten: Projekt Solomon / GX10 (bleibt getrennt vom verkauften Produkt). Verwandt: [[projectnorm]]
