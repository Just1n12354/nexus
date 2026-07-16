---
title: Secrets & Zugangsdaten
type: reference
status: aktiv
updated: 2026-07-15
description: Regel für sicheren Umgang mit Secrets und Schlüsseln
tags: [infra/security, secrets]
---

# Secrets & Zugangsdaten

## Regel
- Keywerte **NIEMALS** im Chat ausgeben
- Nur aus der Datei lesen und benutzen
- Falls doch im Klartext ausgegeben: sofort Rotation empfehlen
- Gespeichert in `/home/justin/.hermes/.env` und `/home/justin/.hermes/apidocs/`
- Die Regel ist "nicht zeigen", nicht "nicht speichern"

## Speicherorte
- `.env`: `/home/justin/.hermes/.env`
- API-Dokus: `/home/justin/.hermes/apidocs/`
- NAS Secrets: `/mnt/justnas/Dokumente/Secrets/`
- Mac mini Secrets: `/Users/imjustin/JustNAS/Dokumente/Secrets/`