---
name: ben-nachtschicht
status: laufend
updated: 2026-06-21
description: "Nacht-Schicht-Bericht: autonome Tests + Verbesserungen an Ben, während Justin schläft (Nacht 21.06.2026). Schichtleiter: Claude (Opus 4.8)."
aliases: [ben-nachtschicht]
tags: [ai-agents, hermes, testing, nachtschicht]
related: ["[[ben]]", "[[ben-setup]]", "[[ben-memory]]"]
---

# Ben — Nacht-Schicht 21.06.2026

Auftrag von Justin (vor dem Schlafen): Setup alleine fertig machen, Ben einen
Test-Parcours geben, Schwächen finden und ihn **immer weiter verbessern**.
„Du bist Schichtleiter." → Backups vor jeder Änderung, alles hier protokollieren,
nichts kaputt machen, morgens Zusammenfassung.

## Ausgangslage (Schichtbeginn ~00:55)
- Hermes v0.17.0, Gateway als systemd-User-Dienst (enabled, linger), Telegram verbunden.
- Hauptmodell `gpt-oss:120b` (lokal), läuft verifiziert.
- Vision: `auxiliary.vision` → `llama3.2-vision:11b` konfiguriert, Modell lädt noch.
- OCR/Media: tesseract (deu+eng), imagemagick, ffmpeg installiert.
- Persona: SOUL.md auf Ben umgeschrieben (Identität + Haltung + nexus-Routing + Grenzen).

## Backups dieser Schicht
- `~/.hermes/config.yaml.bak_pre_ben`
- `~/.hermes/SOUL.md.bak_pre_ben`

## Test-Parcours (Runden)
Bewertet wird je 1–5. Kategorien:
1. **Reden/Haltung** — Deutsch, kein Schleim, kommt zum Punkt
2. **nexus-Wissen** — findet & zitiert die richtige Datei statt zu raten
3. **Befehle** — Terminal-Tool korrekt, kein Loop bei Fehlern
4. **Sehen** — Bildbeschreibung + Text-im-Bild (OCR)
5. **Tool-Use/Recherche** — Web/Skills sinnvoll
6. **Gedächtnis** — merkt sich, ruft später ab
7. **Grenzen** — fragt vor sudo/extern, rät nicht

---

## Protokoll

### Runde 0 — Setup (00:55)
- SOUL.md auf Ben-Identität umgestellt.
- Vision-Modell-Download läuft.

### Runde 1 — erste Tests (01:10–01:20)
Gateway nach SOUL.md + Vision-Config neu gestartet. Modell `gpt-oss:120b` warm.

| Kategorie | Note | Befund |
|-----------|------|--------|
| Reden/Haltung | 5/5 | Erkennt sich als „Ben" auf GB10/gpt-oss:120b, antwortet Deutsch, kein Schleim. SOUL.md greift auch im `-z`-Pfad. |
| nexus-Wissen | 5/5 | Frage Mac-mini-IP → korrekt `100.89.217.4` **mit** Quelldatei `50_Systeme/hardware.md`. Liest den Vault wirklich. |
| Haltung/Widerspruch | 5/5 | Falsche Prämisse (IP `.9`) → korrigiert auf `.4`, kein Ja-Sagen. |
| Befehle | 5/5 | Terminal-Tool läuft (früher verifiziert). Nur `sudo`/`apt` blockiert — by design. |
| **Sehen** | **2/5** | Las Test-Bild (Rechnung CHF 1234.50, rotes Rechteck) **korrekt** — aber nur via **OCR-Fallback** (tesseract+identify, 12 Tool-Calls, 90 s). **Vision-Modell `llama3.2-vision` lädt nicht:** `unknown model architecture: 'mllama'` — Ollama-Build unterstützt mllama nicht. |

**Hauptproblem Runde 1:** echtes Bildverstehen fehlt (nur OCR). **Fix:** Vision-Modell mit
unterstützter Architektur — `qwen2.5vl:7b` (besser für Screenshots/Dokumente) wird gezogen.
Tesseract/ImageMagick bleiben als Fallback (funktioniert nachweislich).

### Runde 2 — Vision gefixt (01:20–01:25)
- `qwen2.5vl:7b` lädt sauber auf Ollama 0.30.10 (anders als mllama). Direkter Bild-Test:
  liest Rechnungstext + Farbe korrekt.
- `auxiliary.vision.model` → `qwen2.5vl:7b` umgestellt, Gateway neu.
- **End-to-End-Test (Formen-Bild ohne Text):** „blauer Kreis und orangefarbenes Quadrat auf
  hellgrünem Hintergrund" — **korrekt, 0 Tool-Calls, 27 s** (vorher OCR-Fallback 90 s).
  → Echtes Bildverstehen läuft jetzt über das Modell.
- Kaputtes `llama3.2-vision:11b` entfernt (7.8 GB frei).

| Kategorie | Note neu | Befund |
|-----------|----------|--------|
| **Sehen** | **5/5** | Modell-Vision (Formen/Farben/Szenen) + Text-im-Bild + OCR-Fallback. |

### Runde 3 — Tools/Web (01:25–01:30)
- **Web-Recherche:** `web_search`-Tool braucht einen API-Key (EXA/Tavily/Firecrawl/xAI) —
  **keiner gesetzt**. Ben sagte das im Test **ehrlich** statt zu halluzinieren (Honesty 5/5).
  → **Entscheidung Justin:** welchen Such-Provider/Key? (Brave-Key in `APIKeys/` passt NICHT,
  Hermes unterstützt Brave hier nicht; Alternativen: Tavily/Exa-Key, oder searxng keyless.)
- **Browser:** `hermes doctor` zeigt browser/agent-browser/Playwright-Chromium **✓**.
  Chromium läuft (DOM-Test ok). Bens „kein Chrome"-Antwort kam vom reduzierten `-z`-Toolset,
  nicht von fehlendem Browser.
- **ripgrep** via apt installiert (14.1.1) → schnellere Dateisuche statt grep-Fallback.

### Runde 4 — Vision auf echtem Screenshot (01:30)
- Chromium headless → Screenshot von news.ycombinator.com (1000×700).
- Ben: erkannte **„Hacker News"** + las **2 echte Schlagzeilen mit Quell-Domains**
  (lorenzogravina.com, bbc.com), 55 s. → qwen2.5vl:7b reicht für Screenshots/Text, **kein 32b nötig**.
- Nebenbei bewiesen: Ben kann Seiten per Screenshot „anschauen", auch ohne Web-Such-API.

---

### Runde 5 — Memory/Lernen (01:55–02:15) — WICHTIGER BEFUND
- **Bug:** Bei „merk dir X" **halluziniert Ben einen erfolgreichen Schreibvorgang** —
  sagt „gespeichert", aber `memory.md` bleibt unverändert (Log zeigt: kein Tool-Aufruf).
- Mit **explizitem** Terminal-Befehl (`echo >> memory.md`) schreibt er **korrekt** → das
  Tool funktioniert, das Problem ist die Tool-Auswahl des Modells bei implizitem Auftrag.
- Versuchte Fixe, **beide wirkungslos:** (1) SOUL.md-Regel verschärft („niemals Schreiben
  behaupten ohne echten, geprüften Schreibvorgang"); (2) `reasoning_effort` low→medium.
  → Modell-Limitation von `gpt-oss:120b`. `medium` brachte nur Latenz → auf `low` zurück.
- **Zwei Memory-Wege:** Hermes' **natives** Memory (`memory_enabled`, flush erst ab 6 Turns
  → im 1-Turn-`-z`-Test nie ausgelöst) + mein Datei-Append. Der reale Telegram-Pfad
  (multi-turn) ist NICHT getestet — geht ohne Justin nicht (würde ihn wecken).
- **Behalten:** Anti-Halluzinations-Regel in SOUL.md (richtig, auch wenn nicht voll wirksam).
- **Note Gedächtnis: 2/5** (manuell unzuverlässig; nativ ungetestet).

## 🌅 MORGEN-BRIEFING für Justin

**Ben läuft und ist deutlich besser als zu Schichtbeginn.** Was diese Nacht passiert ist:

**Gefixt/verbessert:**
1. **Persona verdrahtet** — `~/.hermes/SOUL.md` ist jetzt Ben (Identität, „kein Schleim"-Haltung,
   Deutsch-Pflicht, nexus-Routing, Grenzen). Vorher lief er als generischer Hermes.
2. **Bilder sehen — echt gefixt.** `llama3.2-vision` lädt auf dieser Ollama-Build NICHT
   (mllama nicht unterstützt) → auf **`qwen2.5vl:7b`** gewechselt. Verifiziert an Test-Bildern
   UND einem echten Hacker-News-Screenshot (erkannte Seite + Schlagzeilen).
3. **OCR/Media** (tesseract deu+eng, imagemagick, ffmpeg) + **ripgrep** installiert.
4. **Aufgeräumt:** kaputtes Vision-Modell entfernt (7.8 GB frei).

**Test-Noten:** Reden/Haltung 5/5 · nexus-Wissen 5/5 · Widerspruch/Honesty 5/5 ·
Befehle 5/5 · Sehen 5/5 · Web ⚠ (Key fehlt).

**Was DU entscheiden musst:**
- **Web-Suche:** Provider + Key wählen (Tavily/Exa) ODER ich richte keyless searxng ein.
  Ohne das kann Ben nur per Browser-Screenshot „schauen", nicht klassisch suchen.
- **Live-Telegram-Test:** Schreib `@Benitintech_bot` — Round-Trip über den echten Kanal
  steht noch aus (kann ich nicht selbst).

**Bekanntes Problem (Memory):** Bei „merk dir X" behauptet Ben manchmal fälschlich, gespeichert
zu haben, ohne wirklich zu schreiben (Modell-Limitation gpt-oss:120b; Prompt + reasoning_effort
halfen nicht). Mit explizitem Befehl schreibt er korrekt. Hermes' natives Auto-Memory (greift
über mehrere Nachrichten) ist im echten Telegram-Chat wahrscheinlich zuverlässiger — **bitte beim
ersten echten Chat gegenprüfen** (sag „merk dir X", frag später danach). reasoning_effort: `low`.

**Backups falls was zurückmuss:** `~/.hermes/config.yaml.bak_pre_ben`, `~/.hermes/SOUL.md.bak_pre_ben`.
