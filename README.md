# Nexus KI v1

KI-optimierte Version des Nexus Vault. Strukturiert für bessere Lesbarkeit durch Menschen und Maschinen.

## Struktur

```
Nexus_KI_v1/
├── README.md          ← Diese Datei (Hauptindex)
├── TODO.md            ← Offene Aufgaben
├── tree.md            ← Baumdarstellung des Vaults
│
├── 01_log/            ← Wochenlogs aller Jahre
├── 02_personen/       ← Personenprofile (privat)
├── 03_projekte/       ← Alle Projekte (gruppiert)
├── 04_agenten/        ← Ben + Luna Agenten
├── 05_finanzen/       ← Finanzen
├── 06_systeme/        ← Hardware, Netzwerke, Systeme
├── 07_referenz/       ← improvements, lessons-learned, service-ports
├── 08_arbeit/         ← Arbeitsthemen (Itin TechSolutions, Acino)
├── 09_roboter/        ← PiCrawler Roboterdokumentation
│
├── _meta/             ← Migration-Dokumente (audit, issues, mapping)
└── _quarantine/       ← Separat: APIKeys, Obsidian-Konfig, Python-Code
```

## Design-Prinzipien

- **Keine Leerzeichen in Pfaden** — alles lowercase mit Bindestrich
- **Projekte gruppiert** — finanzen, reise, tools, sonstige
- **Code vom Content getrennt** — Python-Parsers in _quarantine/code/
- **Secrets niemals im Vault** — APIKeys in _quarantine/secrets/ (nie kopieren!)

## Migration

Diese Version wurde aus `/mnt/justnas/Test/Original` migriert am 2026-07-02.
Alle Reports und Mappings: siehe `_meta/`.

---

*Original bleibt unverändert in /mnt/justnas/Test/Original/*
