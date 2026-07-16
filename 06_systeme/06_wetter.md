---
title: Wetter (Open-Meteo)
type: reference
status: aktiv
updated: 2026-07-15
description: Weather-Tool auf Open-Meteo, kein API-Key nötig
tags: [infra/weather, plugin]
---

# Wetter (Open-Meteo)

## Tool
- Seit 14.07.2026 aktiv: `get_weather`
- Plugin: `/home/justin/.hermes/plugins/weather/`
- Toolset: "weather"
- In `config.yaml` unter `plugins.enabled`

## Backend
- Open-Meteo — **KEIN API-Key**
- Kann Geocoding, aktuelles Wetter, bis zu 7 Tage Vorhersage
- Nur Python-Stdlib

## Schnelltest
```bash
hermes -z "Wetter in Zürich?"
```

## OpenWeather (NICHT genutzt)
- Zwei gültige Keys liegen brach
- Doku: `apidocs/OpenWeather_API.md`
- **Falle**: Frisch erstellte OpenWeather-Keys antworten bis zu 2 Stunden mit "401 Invalid API key" — nicht vorschnell wegwerfen
- Free-Tier: 2.5/weather, 2.5/forecast, 2.5/air_pollution, geo/1.0
- 3.0/onecall: Benötigt separates Abo (nicht gebucht)