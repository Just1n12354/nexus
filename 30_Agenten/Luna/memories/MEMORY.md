nexus at /Users/imjustin/Documents/GitHub/nexus is Luna’s durable source of truth; current live entrypoints are MASTER.md and TREE.md, and some older memories/docs about 30_Agenten/Luna or MASTER_INDEX.md are stale.
§
nexus and Itin-TechSolutions are separate repos/namespaces; use live vault structure over old bootstrap assumptions because the slimmed-down nexus removed many legacy entry files and folders.
§
Wo was liegt in nexus: Justin-Fakten → 10_Personen/profile.md · Finanzen → 40_Finanzen/ · Systeme & Mac mini → 50_Systeme/ (Hermes-Gateway LaunchAgent ai.hermes.gateway: services-mac-mini.md; Ports inkl. JustReise:8060: service-ports.md; OneDrive-Root + 00_InputLuna-Inbox: storage-cloud.md; Keys: 60_Referenz/secrets-locations.md) · Projekte → 20_Projekte/ (JustReise: justreise.md) · Arbeit → 70_Arbeit/.
§
JustReise (Quick-Fact): source /Users/imjustin/Documents/GitHub/Itin-TechSolutions/20_Projekte/10_Apps/Aktiv/JustReise; live runtime /Users/imjustin/JustReise via LaunchAgent com.itintechsolutions.justreise auf Port 8060 (http://justinmacmini.tail8b5081.ts.net:8060/); London-Livedaten nur unter data/london/; Runtime-Änderungen immer auch in src/ spiegeln (Details: arbeitsordner.md).
§
nexus-Dateien können macOS File-Provider-Platzhalter sein → vor dem Lesen mit brctl download materialisieren, via fileproviderctl evaluate prüfen.
§
Bearer-authentifizierte interne Apps laufen auf einem Tailscale-Host; bei Bedarf direkt abrufen (Key-Speicherorte siehe 60_Referenz/secrets-locations.md).
§
Lunas visuelle Identität: elegant, ruhig, futuristisch, leicht mysteriös/high-tech; Dark-Mode mit blau/violetten Neon-Akzenten. Standard-Avatar: nexus 30_Agenten/Luna/LunaPB.png (junge Frau, lange dunkelbraune Wellen, ruhiger direkter Blick, dunkles elegant-futuristisches Outfit mit Leuchtakzenten).
§
Lunas Eingangskorb 00_InputLuna ist kein Ablageordner; neue Dateien müssen vollständig abgearbeitet, live verifiziert und im LOG.md dokumentiert werden, bis nur die Steuerdateien übrig sind.
§
Wartungspass 2026-06-12: Hermes-Home ist deutlich verbessert — Websuche läuft jetzt (brave-free; web_extract weiter ohne Backend → Browser-Tool nutzen), Zeitzone/STT/TTS auf Schweiz/Deutsch, Memory-Limits 4000/2500, Sessions-Auto-Prune an. Vollständige Karte + Vorher/Nachher + Update-Regeln: ~/.hermes/TOPOLOGY.md. Alles update-sicher (nur Standard-Config-Keys, nichts verschoben), Vorher-Stände in ~/.hermes/backups/.
§
Justin is integrating or experimenting with a 'Mythos' layer above Luna/Hermes and may want clear handoff documentation of Luna's paths, memory locations, skills, and runtime topology for that integration.
§
AI Fight Club lives at /Users/imjustin/Documents/GitHub/Itin-TechSolutions/20_Projekte/20_Konzepte/AI Fight Club. Current inspection anchors are VERSION, app/registry.py, app/board6.py, app/doctor.py, and data/run_all_native_status.json / run_all_text_status.json / run_all_lenient_status.json; the nexus note can lag behind the repo implementation version.
§
Live nexus state on 2026-06-14 evening: nexus has been slimmed down. Root entrypoints are now MASTER.md and TREE.md; the _meta/_registry/_tools/_attic layer, README.md, MASTER_INDEX.md, legacy alias folders, and most persona/memory files were removed. Many notes still reference removed targets like [[devices]], [[personas]], [[PROJECT_DIRECTORY]], [[CONVENTIONS]], [[RULES]], and [[30_Agenten/README]], so the vault currently has substantial ghost-link/documentation drift.
§
Default weather location for Justin/Luna is Diepflingen 4442, Switzerland, using Open-Meteo coordinates around 47.45, 7.84 unless a different place is specified.
§
JustinV2 exposes a REST API on localhost:8050 and Tailscale 100.89.217.4:8050; GET endpoints are open by default, while POST/PUT/DELETE require X-API-Key. The key should be kept only in the local non-git file ~/LocalSecure/Keys/justinv2_api_key.txt, not in git-backed notes or Hermes memory.