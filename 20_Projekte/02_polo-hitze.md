---
title: Polo Hitze-Szenario
type: reference
status: aktiv
updated: 2026-07-15
description: Hitze-Risiko für ZTE U30 Air Router und Anker Solix C300X im Polo
tags: [projekt/auto, polo, hitze]
---

# Polo Hitze-Szenario

## Geräte
- **ZTE U30 Air 5G-Router** (Li-Ion, im Kofferraum unter Abdeckung)
- **Anker Solix C300X** (LiFePO₄)

## Messwerte
- Powerbank 28→45 °C bei 28 °C aussen

## Risiko
- Hauptschwachstelle: **Router-Akku** (klein, 5G-Eigenwärme)
- Altert schneller, kann sich aufblähen

## Temperatur-Grenzen
- Bis 40 °C: safe
- 40–50 °C: beobachten
- Über 55–60 °C: Geräte raus

## Lösung
- Temperatur-Logging mit Pi + DS18B20/BME280 an 3 Positionen
- Router-Akku entfernen, wenn möglich