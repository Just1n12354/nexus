# VW Polo 2019 — Technische Projektdokumentation

Zentrale Wissensdatenbank für den **VW Polo Comfortline 1.0 TSI** (95 PS, Modelljahr 2019). Ziel ist es, das Fahrzeug — insbesondere das Infotainmentsystem (MIB2) — vollständig zu analysieren, zu dokumentieren und vorhandene Funktionen sicher freizuschalten. Dieses Repository soll langfristig wachsen und als technische Referenz für das Fahrzeug und zukünftige Erweiterungen dienen.

> **Quellenhinweis:** Die MIB2-Systemwerte (Infotainment, HMI, FEC/SWaP, Temperaturen, Speicher usw.) stammen aus ausgewerteten Foto-Screenshots des Geräts — es wurde nichts ergänzt, was nicht sichtbar war. Fahrzeug-Infrastruktur, Ziele und Planung stammen aus eigenen Angaben und sind entsprechend gekennzeichnet.

---

## Hauptziele

### 1. App-Connect freischalten — **Priorität**

Wichtigstes Ziel. Aktivierung von App-Connect:
- Android Auto
- Apple CarPlay
- MirrorLink (falls unterstützt)

Falls notwendig, sollen dazu die FEC-/SWaP-Lizenzen analysiert werden.

### 2. Versteckte Funktionen freischalten

Alle Funktionen identifizieren, die das Fahrzeug bereits unterstützt, ab Werk aber deaktiviert sind:
- Komfortfunktionen
- Infotainmentfunktionen
- Diagnosefunktionen
- Entwickler-/Engineering-Funktionen
- Fahrzeuganzeigen

### 3. Rückfahrkamera nachrüsten — *langfristig*

Nachrüstung einer originalen Rückfahrkamera. Bereits jetzt vorbereiten:
- notwendige Codierungen verstehen
- benötigte Hardware dokumentieren
- Softwarevoraussetzungen analysieren

### 4. MIB2 vollständig dokumentieren

Sämtliche Informationen erfassen: Hardware, Software, Firmware, Linux-System, HMI, Skin, Display, Netzwerk, Dateisystem, FEC, SWaP, Temperaturen, Speicher, Bootprozess, Konfiguration.

### 5. Sichere Änderungen

Vor jeder Änderung:
- Backup erstellen
- Dump erzeugen
- Änderung dokumentieren

Ziel: Änderungen jederzeit nachvollziehen und rückgängig machen zu können.

---

## Fahrzeug

| Feld | Wert |
|---|---|
| Fahrzeug | VW Polo Comfortline |
| Motor | 1.0 l TSI OPF/GPF |
| Leistung | 70 kW (95 PS) |
| Modelljahr | 2019 |
| Lackierung | Deep Black Perleffekt |
| FIN | WVWZZZAWZKU092828 |

---

## Infotainment

### Gerät

| Feld | Wert |
|---|---|
| MIB-Generation | MIB2 Standard Navigation (STD2) |
| Train | `MST2_EU_VW_ZR_P0472T` |
| Installierte MU-Version | 0472 |
| Software-Version | `H29.319.58_STD2Nav_EU` |
| Teilenummer | 3Q0035846B |

### Display

| Feld | Wert |
|---|---|
| Display-Teilenummer | 5G6919605B |
| Display-Software | 8130 |
| Display-Hardware | H52 |

### Betriebsdaten

| Feld | Wert |
|---|---|
| Betriebsstunden | 2291 h 50 min |
| Lüfter | 4500 rpm |
| Klemme 30 Spannung | 12.2 V |

### Speicher (eMMC)

| Feld | Wert |
|---|---|
| Gesamt | 7.634.880 kB |
| Benutzt | 2.717.648 kB |
| Frei | 4.917.232 kB |

→ Noch rund **4,9 GB** freier Speicher verfügbar.

### Temperaturen

| Komponente | Temperatur |
|---|---|
| PCB intern | 57 °C |
| PCB extern | 59 °C |
| i.MX6 CPU | 76 °C |
| Power Controller | 69 °C |
| Bluetooth-Modul | 67 °C |

→ Alle Temperaturen im normalen Betriebsbereich.

---

## Bluetooth

### Verbundene Geräte

**Samsung Galaxy S24+**
- HFP 1.7
- A2DP
- FctAVP

**Samsung Galaxy S21**
- HFP 1.7
- A2DP
- FctAVP

---

## WLAN

- Internes WLAN-Modul vorhanden
- Interne IP-Adresse: `192.168.0.136`

Weitere interne Adressen:
- `127.0.0.1`
- `10.200.1.1`
- `192.168.0.136`

---

## Toolbox

| Feld | Wert |
|---|---|
| Installiert | MIB STD2 PQ/ZR Toolbox |
| Version | 1.5 |
| Startbildschirm | `Welcome to MIB STD2 PQ/ZR Toolbox v1.5` |

**Vorhandene Menüs:**
- about
- customization
- dump
- mib_info
- network
- tools
- update_and_uninstall

### Toolbox — Netzwerk

Vorhandene Funktionen:
- Activate telnet and ftp access until next reboot
- Activate qconn access until next reboot
- Activate console access until next reboot
- Deactivate telnet, ftp and qconn access
- **Activate permanent telnet and console access**
- Deactivate permanent telnet and console access
- Test internet connection

→ Sowohl **temporärer** als auch **permanenter** Zugriff aktivierbar.

### Toolbox — Systeminformationen

Vorhandene Funktionen:
- Show short system info
- Save extended system info to Toolbox drive

→ Vollständige Systeminformationen exportierbar.

---

## Engineering Menu

Installiert: **GEM 4.11t**

**Vorhandene Menüs:**
- analogtuner_asia
- analogtuner_v3.1
- debugging
- engineering
- debugging mlp
- irc
- navigation
- mibstd2_toolbox

---

## HMI

| Feld | Wert |
|---|---|
| HMI-Software | `H29.319.58_STD2Nav_EU` |
| Model | `GuideModel_29.319.18` |
| Software Base | `H29.319.58-201801301818` |
| CGRun | `H29.319.58-201801301822_STD2Nav_EU...` |
| Skin Editor | LSEV |
| Skin Model | `MS29.319.18` |
| Skin Build | `BH29.319.58-201801301818` |
| Skin Short | `VW_STD8_Skin_A-STD2Nav_EU-2` |
| Skin SPF | `VW_HIGH_Skin_A.spf` |
| Speller | `GuideModel_11.10.4` |
| Text Translation | `VWTexte_88.21.5_H29.315.4` |

---

## VW Service-Modus

**Freigeschaltete Menüs:**
- Software-Aktualisierung / Versionen
- HMI-Versionen
- Funktionscodes (FEC, SWaP)
- Testmode
- ITR
- Logging

**Software-Stand:**
- Aktuelle Version: `MST2_EU_VW_ZR_P0472T` (0472)
- Update: `MST2_EU_VW_ZR_P0472T` (0472-1)

---

## FEC / SWaP — Funktionscodes

### Unterstützte Codes (sichtbar auf den Bildern)

```
00040100
00050000
00060100
00060200
00060300
00060400
00060800
00060900
00060B00
00070200
00070400
0740002C
08400002
09400003
0C400003
```

### Installierte Codes (sichtbar)

| Code | Status |
|---|---|
| 00040100 | Gültig |
| 09400008 | Gültig |
| 00050000 | Gültig |
| 00030000 | Gültig |
| 00060100 | Gültig |
| 00060200 | Gültig |

→ Alle angezeigten installierten Codes besitzen den Status **„Gültig"**.

---

## Car-Net

**Vorhanden:**
- Car-Net Aktivierung
- PIN-Eingabe möglich
- Diensteverwaltung
- Privater Modus
- Guide & Inform

Beim Aufruf erscheint:
> „Service ist nicht verfügbar."

→ Die Software unterstützt Car-Net, die zugehörigen Online-Dienste sind jedoch nicht mehr verfügbar (VW hat die alten Dienste beendet). Kein Fehler des Radios.

---

## Hardware (MIB2)

Im Handschuhfach vorhanden:
- DVD-/CD-Laufwerk
- SD-Kartenslot 1 (SD1)
- SD-Kartenslot 2 (SD2)

---

## Fahrzeug-Infrastruktur

> Eigene Strom- und Netzwerk-Infrastruktur im Fahrzeug (eigene Angaben, nicht aus MIB2-Fotos).

### Anker Solix C300X DC (Powerstation)

- Standort: Kofferraum
- Laden während der Fahrt über **USB-C (65 W Input)** vom Zigarettenanzünder im Cockpit
- Langes USB-C-Kabel vom Kofferraum nach vorne → Geräte im Cockpit können direkt über die Powerstation geladen/betrieben werden

### USB-C-Kabel

Zwei hochwertige **MicroConnect** USB-C-Kabel:
- 4 Meter
- USB 3.2 Gen2
- bis 100 W
- Daten- und Stromübertragung

### Mobiler Router — ZTE U30 Air

- Standort: Kofferraum
- Soll als mobiles Netzwerk dienen

Geplant:
- Internet im Fahrzeug
- WLAN
- Netzwerkzugriff auf Geräte
- möglicher Dateiaustausch über SD-Karte
- zukünftige Fahrzeugdienste

---

## Diagnose

> Werkzeug für Diagnose und Codierung (eigene Angaben).

### OBDeleven 3 Pro Pack

Vorgesehene Verwendung:
- Diagnose
- Long Coding
- Anpassungen
- Steuergeräte
- Fehlerspeicher
- Servicefunktionen
- Dokumentation
- Backups von Codierungen

---

## Aktueller Gesamtzustand

Das System verfügt über:
- Aktivierten VW Service-Modus
- Aktiviertes GEM 4.11t Engineering Menu
- Installierte MIB STD2 PQ/ZR Toolbox v1.5
- Netzwerkwerkzeuge inkl. Telnet-, FTP-, QConn- und Console-Zugang
- Exportfunktion für Systeminformationen
- Vollständige HMI-Informationen
- Anzeige der Hardwaretemperaturen
- Anzeige des eMMC-Speichers
- Anzeige der Display-Hardware und -Software
- Anzeige der Betriebsstunden
- Anzeige installierter und unterstützter FEC-/SWaP-Codes
- Car-Net-Konfiguration mit Aktivierungsdialog
- Zwei SD-Kartensteckplätze sowie optisches Laufwerk

Insgesamt dokumentieren die Bilder ein weitgehend freigeschaltetes und sehr gut zugängliches MIB2-STD2-Navigationssystem, bei dem sowohl die offiziellen VW-Servicefunktionen als auch erweiterte Engineering- und Toolbox-Funktionen verfügbar sind.

**Bewertung des Zustands: ★★★★★ (9,5/10)** — praktisch alles freigeschaltet, was auf einem MST2 ZR ohne Hardwareeingriffe erreichbar ist. Es fehlt im Grunde nur noch die eigentliche Nutzung dieser Möglichkeiten.

---

## Nächste Schritte

- [ ] Vollständigen System-Dump sichern (über die Toolbox)
- [ ] FEC-/SWaP-Lizenzen vollständig auslesen (alle Codes als Text/Dump)
- [ ] Telnet dauerhaft testen
- [ ] Linux-Dateisystem dokumentieren
- [ ] Rückfahrkamera-Nachrüstung vorbereiten
- [ ] App-Connect/FECs genauer analysieren

---

## Vorgehensweise — Änderungen sicher durchführen

**Regel:** Vor jeder Änderung zuerst die Analyse, dann die Aktion.

1. **Vollständigen Fahrzeugscan** mit OBDeleven durchführen
2. **Fehlercodes sichern** (nicht löschen, erst notieren)
3. **Wichtige Steuergeräte dokumentieren** (insbesondere 5F = Infotainment, 19 = CAN Gateway)
4. **Systemdumps und FEC-/SWaP-Daten** mit der MIB Toolbox sichern
5. **Vor jeder Änderung Backup erstellen**
6. **Änderungen einzeln durchführen** — nie mehrere auf einmal
7. **Jede Änderung dokumentieren** (Was, Warum, Ergebnis)
8. **Erst nach vollständiger Analyse** Codierungen oder Freischaltungen beginnen

> **Wichtig:** Router, SIM-Karte oder Hotspot können keine VW-Funktionen freischalten. Sie liefern nur Internet und Netzwerk für Diagnosegeräte und externe Tools.

---

## Langfristige Vision

Dieses Repository soll nicht nur eine Sammlung einzelner Notizen sein, sondern eine vollständige technische Dokumentation des VW Polo. Das Projekt soll über längere Zeit wachsen und u. a. folgende Themen umfassen:

- Fahrzeugdokumentation
- Hardware
- Steuergeräte
- CAN-Bus
- OBD
- MIB2
- Linux
- FEC
- SWaP
- Nachrüstungen
- Codierungen
- Diagnose
- Reverse Engineering
- Stromversorgung
- Netzwerk
- Raspberry Pi
- Automatisierungen
- KI-gestützte Fahrzeugfunktionen
- Mobile Server
- Datenlogger
- Wartung
- Reparaturen
- Backup-Strategien
- Eigene Tools und Skripte

---

## Arbeitsweise

- Möglichst strukturiert arbeiten, jede Erkenntnis nachvollziehbar dokumentieren.
- Fehlende Informationen als **offen** markieren.
- **Bestätigte Fakten** klar von **Annahmen** trennen.
- Änderungen nachvollziehbar angeben.
- Verbesserungen für Dokumentation oder Projektstruktur vorschlagen.
- Ziel: ein hochwertiges, langfristig gepflegtes Repository als technische Referenz.
