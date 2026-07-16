---
title: Brave Search
type: reference
status: aktiv
updated: 2026-07-15
description: Websuche-Backend, Auth-Header, Rate-Limits
tags: [infra/brave, search]
---

# Brave Search

## Config
- Aktives Websuche-Backend: `config.yaml search_backend: brave`
- Key in `.env` als `BRAVE_API_KEY`
- Doku: `apidocs/Brave_Search_API.md`

## Auth
- Header: `X-Subscription-Token`
- **NICHT** als Query-Parameter

## Rate-Limits (gemessen 14.07.2026)
- **1 Request/Sekunde** (kein Burst)
- **2000 Requests/Monat**

## Fehlerdiagnose
- Hängt die Websuche oder kommt leer zurück: Erst an HTTP 429 denken, nicht an kaputten Key
- Key wurde am 14.07.2026 versehentlich im Klartext ausgegeben → Rotation empfohlen