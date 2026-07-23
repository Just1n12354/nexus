---
title: Index
type: note
status: aktiv
updated: 2026-06-24
---

# Projekte & Konzepte · Übersicht

Status: aktiv  ·  Letztes Update: 2026-06-21
Quelle: `Itin-TechSolutions/20_Projekte` (READMEs je Projekt + VERSIONS.md, _audit/AUDIT.md, _audit/ROADMAP.md, 10_Apps/PORTS.md).

Das ist die nexus-Sicht auf Justins Projekt-Portfolio — ein Kurzfile pro aktivem Projekt in diesem Ordner, hier die Tabelle als Einstieg. Detail-Stand/Code liegt im Itin-TechSolutions-Repo.

## Aktive Apps

| Projekt | Status | Ver. | Port | Audit | Kurz |
|---|---|---|---|---|---|
|| [[sonstige/ai-fight-club.md]] | aktiv | 6.0.0-dev | — (GamingPC) | — | Liga-Arena: ~95 lokale Ollama-Modelle lösen 15 Challenges, Judge bewertet echte Artefakte |
| [[sonstige/aieyes.md]] | aktiv | 0.002 | — | — | Augen+Hände für KI (Screenshot + Maus/Tastatur); UIA-Hybrid auf Windows |
| [[sonstige/claudesync.md]] | prototyp | 0.006 | — | — | Single Source für Claude-Code-Config über alle Geräte; SessionStart-Hooks, /push |
| [[sonstige/jarvis.md]] | aktiv | 0.002 | 3000 (WebUI) | — | Lokaler Sprach-/Aktions-Assistent (STT→Ollama→TTS), Mac primär |
| [[sonstige/just-better.md|JustBetter]] | konzept | 0.001 | — | — | KI-Coach für Gesundheit/Lernen/Gewohnheiten (reines Konzept; 8050 ist aktuell von JustinV2 belegt) |
| [[finanzen/just-finance-business.md|JustFinanceBusiness]] | aktiv | 0.002 | 8010 | 75 | Buchhaltung Itin TechSolutions, OR-konform, stdlib http.server |
| [[finanzen/just-finance-private.md|JustFinancePrivate]] | aktiv | 0.002 | 8020 | 67 | Private Finanzen (Konten/Steuern/Lotto), git-push als Backup |
| [[tools/just-launcher.md|JustLauncher]] | aktiv | 0.002 | 8000 | 63 | Dashboard für alle Just-Dienste, Flask + native Wrapper |
| [[reise/just-reise.md|JustReise]] | aktiv | 0.002 | 8060 | 72 | Reise-Field-Guide (Flask-PWA), aktuell London-Trip |
| [[tools/just-savegame.md|JustSaveGame]] | aktiv | 0.002 | 8765 (Win) | 78 | Savegame-Backup-Manager Windows mit GitHub-Sync |
| [[tools/just-todo.md|JustTodo]] | aktiv | 0.002 | 8030 | 66 | Datei-basierte Todo-App, auch von Bots genutzt |
| [[tools/just-update.md|JustUpdate]] | aktiv | 0.002 | — (Desktop) | 72 | Windows-Wartungs-Tool + Self-Update-Pipeline für Kunden |
| [[sonstige/just-website.md|JustWebsite]] | aktiv | 0.002 | — (Netlify) | 67 | Statische Firmen-Website Itin TechSolutions |
| [[sonstige/project-fusion.md|ProjectFusion]] | aktiv | 5.0 | — | — | Projektstandard: Topologie V5, README = Single Source, Deck/AGENTS.md-Generierung, Agent-Kollaboration |
| [[sonstige/sherlock-holmes.md|SherlockHolmes]] | prototyp | 0.004 | — | — | Recherche-Agent: Idee → GitHub/Reddit nach wiederverwendbaren Repos |
| [[sonstige/swissai-solutions.md]] | aktiv | 0.001 | — | — | Verkaufsprodukt aus Solomon: Plug-&-Play KI-Box für KMU (MRR) |

## Friedhof (eingestellt — kein eigenes File, nur hier vermerkt)

| Projekt | Ver. | Audit | Kurz |
|---|---|---|---|
| AIWorld | 0.002 | 68 | Multi-Bot-Chat-Hub (produktiv v0.11 gewesen); hardcoded Pfade, plaintext Bearer |
| Atlas | 0.002 | 72 | Phase-0-Prototyp; Real-Code-Validierung fehlte |
| JustDaybook | 0.002 | 68 | Tagebuch-App v0.5 Alpha; Monolith (1'360 Z.), keine Tests |

## Portfolio-Querschnitt (Audit 2026-06-07, Iteration 2)

- Portfolio-Durchschnitt ~70/100 (Baseline 68). Repo ist **privat** — kein Live-Security-Leck, Keys liegen extern (`~/LocalSecure/`).
- Größte echte Tech-Schuld: **monolithische Frontends** (HTML+CSS+JS im Backend-String) und **Code-Duplikation** (`api_auth.py` war 4× identisch → kanonisiert in `_shared/`, timing-safe).
- DevOps niedrig: CI-Skeleton existiert, aber Tests fehlen (außer JustKarma), Logging nur `print()`.
- Roadmap-Priorität P0→P2 in `_audit/ROADMAP.md` (Quelle).

## Konventionen / Standard

|- Alle Projekte folgen **[[sonstige/project-fusion.md|ProjectFusion]]**: README an der Wurzel ist die Single Source; Deck (PowerPoint) + AGENTS.md werden daraus generiert.
- Versionsstand pro Projekt: `VERSIONS.md` im Quell-Repo. Port-Belegung: `10_Apps/PORTS.md` (verbindliches Schema: 8000er in 10er-Schritten, Mac mini, Tailscale `100.89.217.4`).

## Verweise
- Firma: [[08_arbeit/itintech-firma.md]]
- Quelle: `Itin-TechSolutions/20_Projekte`
