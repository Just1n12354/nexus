---
title: JustBetter-App
type: reference
status: aktiv
updated: 2026-07-15
description: JustBetter-App auf Mac mini, Port 8050, Auth-Regeln
tags: [infra/justbetter, app]
---

# JustBetter-App

## Server
- Läuft auf Mac mini, Port 8050
- Lokal: `localhost:8050`
- Remote: `100.89.217.4:8050`
- Schreibzugriffe brauchen Auth
- Server akzeptiert BEIDES:
  - Header `X-API-Key`
  - Header `Authorization: Bearer <key>`

## API-Key
- NAS: `/mnt/justnas/Dokumente/Secrets/justbetter_api_key.txt` (44 Bytes)
- Mac mini: `/Users/imjustin/JustNAS/Dokumente/Secrets/justbetter_api_key.txt`

## Arbeitsregeln
- App-Name: **JustBetter** (nicht "JustinV2")
- Key direkt lesen, POST auf `/api/v1/day/meal` senden, Key nicht ausgeben
- Interne Services: erst `curl` auf `/api/v1/health`, dann `/`
- Kein Browser/web_extract als erster Pfad
- `/api/v1/meta` = 404
- Volle Doku: `apidocs/JustBetter_API.md`