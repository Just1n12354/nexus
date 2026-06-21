---
name: ben-setup
status: aktiv
updated: 2026-06-21
description: "Ben-Setup: Hermes Agent v0.17 auf dem GB10, lokal auf Ollama gpt-oss:120b, Telegram-Gateway (@Benitintech_bot, User-Allowlist) als systemd-User-Dienst mit Boot-Autostart. Verifiziert 2026-06-21."
aliases: [ben-setup, hermes-gb10-setup]
tags: [ai-agents, hermes, llm-local, infra/ai, setup]
related: ["[[ben]]", "[[hardware]]"]
---

# Ben — Setup (Hermes Agent auf dem GB10)

Persona/Auftrag: [[ben]]. Diese Datei = wie Ben technisch läuft. **Stand 2026-06-21: läuft,
alle drei kritischen Punkte real verifiziert** (lokales Modell, Telegram, Autostart).

## Geräte-Kontext
- Host: `gx10-bf12` (NVIDIA GB10 / DGX Spark, Ubuntu 24.04, aarch64), Tailscale `100.75.47.118`
- Ollama lokal auf `http://127.0.0.1:11434`, OpenAI-Endpoint `http://127.0.0.1:11434/v1`,
  Modell **`gpt-oss:120b`** (~65 GB, lädt 100 % auf GPU).
- Hermes Agent **v0.17.0**, installiert unter `~/.hermes/hermes-agent` (venv).

## Dateien & Pfade
- Config: `~/.hermes/config.yaml`
- Secrets: `~/.hermes/.env`  (Token + Allowlist — **nicht in Git**)
- Logs: `~/.hermes/logs/gateway.log`, `agent.log`, `errors.log`
- systemd-Unit: `~/.config/systemd/user/hermes-gateway.service`
- Config-Backup vor Ben-Umbau: `~/.hermes/config.yaml.bak_pre_ben`

## 1. Installation (erledigt)
```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash -s -- --skip-setup
hermes --version    # v0.17.0
```

## 2. Lokales Modell (Ollama gpt-oss:120b) — VERIFIZIERT ✅
Der Installer erkennt Ollama automatisch und legt einen `custom_providers`-Eintrag an.
Der `model`-Block musste aber von den OpenRouter-Defaults auf den Custom-Provider
umgestellt werden. Wirksame Config in `~/.hermes/config.yaml`:
```yaml
model:
  default: gpt-oss:120b          # Modellname OHNE 'ollama/'-Prefix (so heisst er am /v1-Endpoint)
  provider: custom               # 'custom' → nutzt custom_providers, nicht OpenRouter
  base_url: http://127.0.0.1:11434/v1   # MIT /v1 (OpenAI-SDK hängt /chat/completions an)
  api_mode: chat_completions
custom_providers:
- name: ollama
  base_url: http://127.0.0.1:11434/v1   # muss zum model.base_url passen
  api_key: ollama                       # Ollama prüft keinen — Dummy nötig (leer schlägt fehl)
  api_mode: chat_completions
```
Test: `hermes -z "..." --cli` → liefert Antwort von gpt-oss:120b (verifiziert 2026-06-21).
Modell wechseln: `hermes model` (interaktiv) oder `model.default` editieren
(z.B. `MichelRosselli/GLM-4.5-Air:Q4_K_M`).

## 3. Telegram-Gateway — VERIFIZIERT ✅
- **Bot:** `@Benitintech_bot` (Name „Ben", Bot-ID `8759110019`).
- Konfiguration über `~/.hermes/.env` (kein interaktives `gateway setup` nötig):
  ```
  TELEGRAM_BOT_TOKEN=<aus 30_Agenten/APIKeys/Telegram-Ben.txt>
  TELEGRAM_ALLOWED_USERS=7856421425   # nur Justin (User-ID), kommagetrennt für mehrere
  ```
  Sobald `TELEGRAM_BOT_TOKEN` gesetzt ist, aktiviert sich die Plattform automatisch.
- Autorisierung zusätzlich via Pairing-Codes: `hermes pairing list|approve|revoke`.
- Test: Gateway-Log zeigt `✓ telegram connected` (verifiziert 2026-06-21).

## 4. Dauerbetrieb / Autostart — VERIFIZIERT ✅
Als systemd-**User**-Dienst installiert (kein sudo nötig):
```bash
hermes gateway install        # legt ~/.config/systemd/user/hermes-gateway.service an, enabled
# Linger wurde aktiviert → Dienst überlebt Logout + startet bei Boot
```
Steuerung:
```bash
hermes gateway status                       # oder: systemctl --user status hermes-gateway
hermes gateway start | stop | restart
journalctl --user -u hermes-gateway -f      # Live-Logs
```
Stand: `enabled` + `active (running)`, Linger an.

> Alternativ System-Dienst (Boot-Start unabhängig vom User-Login):
> `sudo hermes gateway install --system` — hier bewusst NICHT genutzt, User-Dienst +
> Linger reicht für den always-on GB10.

## 4b. Bilder sehen (Vision) — VERIFIZIERT ✅
`gpt-oss:120b` ist textonly. Hermes routet Bilder an ein separates **Vision-Modell**
(`auxiliary.vision`). Wirksame Config:
```yaml
auxiliary:
  vision:
    provider: custom
    model: qwen2.5vl:7b           # lädt auf Ollama 0.30.10; gut für Screenshots/Dokumente
    base_url: http://127.0.0.1:11434/v1
    api_key: ollama
    timeout: 180
```
- **Wichtig:** `llama3.2-vision` (Architektur `mllama`) lädt auf dieser Ollama-Build
  **nicht** (`unknown model architecture: 'mllama'`) → verworfen. `qwen2.5vl:7b` läuft.
- OCR-Fallback: `tesseract` (deu+eng) + ImageMagick `identify`/`convert` + `ffmpeg`
  installiert (apt). Greift, wenn das Vision-Modell nicht reicht (reiner Text-im-Bild).
- Test: `hermes chat -q "Beschreibe das Bild" --image <pfad>` → Beschreibung über das
  Modell, 0 Tool-Calls (verifiziert 2026-06-21).

## 4c. Persona / Identität — VERIFIZIERT ✅
Hermes lädt `~/.hermes/SOUL.md` als primären Identity-/System-Prompt. Dort steht jetzt
**Bens** Identität (Rolle, Haltung „kein Schleim", Deutsch-Pflicht, nexus-Routing, Grenzen)
— inhaltlich gespiegelt aus [[ben]]. Backup der alten Datei: `~/.hermes/SOUL.md.bak_pre_ben`.
Test: „Wer bist du?" → identifiziert sich als Ben auf GB10/gpt-oss:120b, Deutsch (verifiziert).
> Hinweis: SOUL.md lebt in `~/.hermes/` (nicht im nexus-Repo). Bei Änderung an [[ben]]
> die SOUL.md nachziehen — sie ist die wirksame Datei.

## 5. nexus-Zugriff
Bens Terminal-/Datei-Tools laufen mit `terminal.backend: local` und `cwd: .`. Für vollen
Vault-Zugriff Bens Arbeitsverzeichnis auf den nexus-Pfad setzen bzw. ihn in der Persona
auf `~/Documents/GitHub/nexus/` verweisen (siehe [[ben]]). Sandbox-Optionen
(`terminal.backend`: local/docker/ssh/…) bei Bedarf in `config.yaml`.

## 6. Web-Suche — VERIFIZIERT ✅ (2026-06-21 morgens)
Hermes hat einen `brave-free`-Provider (Free-Tier 2'000 Queries/Mt). Brave-Key aus
`30_Agenten/APIKeys/BraveAPI.txt` → `~/.hermes/.env` als `BRAVE_SEARCH_API_KEY`, dazu
in `config.yaml`:
```yaml
web:
  search_backend: brave-free
```
`hermes doctor` zeigt `✓ web`; Test „aktuelle Python-Version?" → Antwort mit Quelle (verifiziert).

## 7. Keep-Alive gpt-oss:120b — VERIFIZIERT ✅ (2026-06-21 morgens)
Damit das 65-GB-Hauptmodell nicht entladen wird (kein Reload-Delay), im Ollama-System-Dienst
`/etc/systemd/system/ollama.service`: `Environment="OLLAMA_KEEP_ALIVE=-1"` (vorher `60m`),
`daemon-reload` + `restart`. `ollama ps` → gpt-oss:120b `UNTIL = Forever`.
Backup: `/etc/systemd/system/ollama.service.bak_pre_ben`. Gilt global; bei Parallelbetrieb
mit GLM (robert) lagert Ollama bei Speicherbedarf um.

## Offene / optionale Punkte
- [x] Persona als System-Prompt verdrahtet (SOUL.md, 2026-06-21)
- [x] Vision über lokales Modell (qwen2.5vl) verifiziert
- [x] Web-Suche (brave-free) verdrahtet + verifiziert
- [x] Keep-Alive gpt-oss:120b (Forever)
- [ ] Live-Round-Trip über Telegram (Justin schreibt `@Benitintech_bot`) — Antwort + Latenz prüfen
- [ ] Memory im echten Telegram-Chat gegenprüfen (siehe NACHTSCHICHT Runde 5)
- [ ] Tool-Freigaben pro Plattform (`hermes tools`) prüfen, falls Ben schreiben/bashen soll
