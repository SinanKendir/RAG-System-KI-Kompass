# KI-Kompass für den Mittelstand – Open-WebUI-Version

RAG-System, das kleinen und mittleren Unternehmen (KMU) hilft, passende KI-Unterstützungsangebote von IHK, KI.NRW, AI Village, digihub und Hochschulen zu finden. Es führt durch die Phasen **Orientierung, Qualifizierung, Prototyping und Umsetzung**.

Projekt im Kurs „KI-Anwendungen in der betrieblichen Praxis“, Hochschule Niederrhein, WS 2026/27.
Team: [Namen eintragen]

## Aufbau

| Komponente | Aufgabe |
|---|---|
| **Ollama** | Lässt die Sprachmodelle lokal laufen: `llama3.1` (Antworten) und `nomic-embed-text` (Embeddings für die Dokumentensuche) |
| **Open WebUI** | Weboberfläche mit Texteingabefeld und eingebauter Wissensdatenbank (RAG), keine Programmierung nötig |
| **Docker** | Startet Open WebUI mit einem Befehl |

Ablauf: Frage im Chat → Open WebUI sucht die passenden Angebotsdateien in der Wissensdatenbank → `llama3.1` formuliert die Antwort auf Basis dieser Stellen und des System-Prompts.

## Voraussetzungen

- Ollama (Desktop-App) installiert
- Docker Desktop installiert
- ca. 6 GB freier Speicher für die Modelle

## Installation

**1. Modelle laden**
```bash
ollama pull llama3.1
ollama pull nomic-embed-text
```

**2. Open WebUI starten** (in diesem Ordner)
```bash
docker compose up -d
```

**3. Im Browser öffnen:** http://localhost:3000 und einen Admin-Account anlegen.

**4. Einrichten**
- Admin-Panel → Settings → Documents: Embedding-Engine **Ollama**, Modell `nomic-embed-text`
- Workspace → Knowledge → Wissensdatenbank „KI-Angebote“ anlegen und alle Dateien aus `daten/` hochladen
- Workspace → Models → Modell „KI-Kompass“ anlegen: Basismodell `llama3.1`, Inhalt von `system-prompt.md` als System-Prompt, Wissensdatenbank anhängen
  (oder: **Import** der JSON-Datei aus `openwebui-export/`)

## Ordnerstruktur

| Datei / Ordner | Inhalt |
|---|---|
| `docker-compose.yml` | Startkonfiguration für Open WebUI |
| `system-prompt.md` | Rolle und Regeln des KI-Kompass |
| `daten/` | Unterstützungsangebote, eine Datei pro Angebot (Quelldokumente für das RAG) |
| `daten/angebot-vorlage.md` | Vorlage zum Erfassen neuer Angebote |
| `openwebui-export/` | Exportiertes Modell aus Open WebUI (JSON) |
| `docs/` | UML-Diagramme, Screenshots, Evaluation |

**Warum eine Datei pro Angebot?** Die Suche findet kleine, klar gegliederte Dokumente zuverlässiger als eine große Sammeldatei. Das Feld „Phase“ hilft bei der Zuordnung, „Stand der Information“ bei der Aktualisierung.

## Beispielfragen

- „Ich habe einen Handwerksbetrieb mit 20 Mitarbeitenden und will mit KI anfangen. Wo bekomme ich eine erste Beratung?“
- „Welche Angebote gibt es, um einen KI-Prototypen zu entwickeln?“
- „Wo können sich meine Mitarbeitenden zu KI weiterbilden?“

## Stoppen

```bash
docker compose down
```

## Aktueller Stand und Ausblick

- Läuft derzeit nur lokal (http://localhost:3000).
- Für den dauerhaften Betrieb wird ein Server benötigt – Abstimmung mit der Hochschule offen.
