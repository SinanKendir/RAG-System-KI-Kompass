# KI-Kompass für den Mittelstand

KI-gestütztes Empfehlungssystem zur Identifikation geeigneter
KI-Unterstützungsangebote für kleine und mittlere Unternehmen (KMU)
mithilfe von Retrieval-Augmented Generation (RAG).

## Projekt

Dieses Projekt entwickelt einen interaktiven KI-Kompass, der kleine und
mittlere Unternehmen (KMU) bei der Suche nach geeigneten
KI-Unterstützungsangeboten unterstützt.

Viele Unternehmen stehen vor der Herausforderung, passende Beratungs-,
Qualifizierungs- und Umsetzungsangebote im Bereich Künstliche Intelligenz
zu identifizieren.

Ziel ist es, mithilfe eines **interaktiven Entscheidungsbaums** den
individuellen Unterstützungsbedarf eines Unternehmens zu ermitteln
und anschließend durch ein **RAG-System (Retrieval-Augmented Generation)**
geeignete Angebote aus einer Wissensdatenbank zu empfehlen.

Das System kombiniert:

- **Interaktive Bedarfsanalyse** zur Erfassung der Unternehmenssituation
- **Regelbasierten Entscheidungsbaum** zur Klassifizierung des Unterstützungsbedarfs
- **Wissensdatenbank** mit KI-Unterstützungsangeboten verschiedener Organisationen
- **Semantische Suche** zur Identifikation relevanter Angebote
- **Large Language Model (LLM)** zur Generierung personalisierter Empfehlungen
- **Quellenangaben** zur Nachvollziehbarkeit der Ergebnisse

Die Unterstützungsangebote werden in vier Kategorien unterteilt:

1. **Orientierung** – Einstieg in das Thema Künstliche Intelligenz
2. **Qualifizierung** – Aufbau von KI-Kompetenzen und Weiterbildung
3. **Prototyping** – Entwicklung und Erprobung erster KI-Anwendungen
4. **Umsetzung** – Einführung und Integration von KI-Lösungen

## Features

### Geplante Kernfunktionen

- Erfassung relevanter Unternehmensinformationen
- Angabe individueller KI-Ziele und Herausforderungen
- Interaktiver Entscheidungsbaum zur Bedarfsanalyse
- Automatische Zuordnung zu einer Unterstützungskategorie
- Semantische Suche nach geeigneten KI-Unterstützungsangeboten
- Generierung personalisierter Empfehlungen
- Bereitstellung von Quellen und weiterführenden Informationen

### Geplante Erweiterungen

- Filterung von Empfehlungen nach zusätzlichen Kriterien
- Rückfragen zu empfohlenen Unterstützungsangeboten
- Erweiterung und Aktualisierung der Wissensdatenbank
- Verbesserung der Empfehlungsqualität durch Evaluation

## Inhaltsverzeichnis

- [Projekt](#projekt)
- [Features](#features)
- [Funktionsweise](#funktionsweise)
- [Systemarchitektur](#systemarchitektur)
- [Technologien](#technologien)
- [Wissensdatenbank](#wissensdatenbank)
- [Installation](#installation)
- [Konfiguration](#konfiguration)
- [Anwendungsbeispiel](#anwendungsbeispiel)
- [Evaluation](#evaluation)
- [Projektstatus](#projektstatus)

## Funktionsweise

Der KI-Kompass unterstützt Unternehmen durch einen mehrstufigen
Beratungsprozess.

### 1. Unternehmensinformationen erfassen

Der Nutzer gibt Informationen zu seinem Unternehmen ein.

Beispielsweise:

- Branche
- Unternehmensgröße
- Bisherige KI-Erfahrungen
- KI-Ziele
- Aktuelle Herausforderungen

### 2. Unterstützungsbedarf ermitteln

Ein interaktiver Entscheidungsbaum analysiert die Angaben
des Unternehmens.

Auf Grundlage definierter Entscheidungsregeln wird der
Unterstützungsbedarf einer der vier Kategorien zugeordnet:

- Orientierung
- Qualifizierung
- Prototyping
- Umsetzung

### 3. Relevante Angebote suchen

Das RAG-System erstellt auf Grundlage des Unternehmensprofils
und des ermittelten Unterstützungsbedarfs eine Suchanfrage.

Die Wissensdatenbank wird mithilfe einer semantischen Suche
nach relevanten Unterstützungsangeboten durchsucht.

### 4. Personalisierte Empfehlungen generieren

Die gefundenen Informationen werden einem Large Language Model
als Kontext bereitgestellt.

Das Sprachmodell erstellt auf dieser Grundlage eine
personalisierte Empfehlung.

### 5. Ergebnisse bereitstellen

Der Nutzer erhält:

- Empfohlene Unterstützungskategorie
- Passende KI-Unterstützungsangebote
- Begründung der Empfehlungen
- Informationen zu den jeweiligen Anbietern
- Quellen und weiterführende Links

Falls keine ausreichend relevanten Angebote gefunden werden,
soll das System einen entsprechenden Hinweis ausgeben.

## Systemarchitektur

Die geplante Architektur basiert auf der Kombination eines
regelbasierten Entscheidungsbaums mit einem RAG-System.

### Verarbeitungsablauf

```text
                 Unternehmensvertreter (KMU)
                              |
                              v
                    Streamlit-Oberfläche
                              |
                              v
                    Unternehmensprofil
                       und KI-Ziele
                              |
                              v
                   Interaktiver
                   Entscheidungsbaum
                              |
                              v
                  Bedarfsklassifizierung
                              |
                              v
                       RAG-System
                              |
                              v
                    Semantische Suche
                              |
                              v
                      Wissensdatenbank
                              |
                              v
                  Relevante Informationen
                              |
                              v
                     Sprachmodell (LLM)
                              |
                              v
                 Personalisierte Empfehlung
                              |
                              v
                    Ausgabe mit Quellen
```

### RAG-Verarbeitung

Retrieval-Augmented Generation kombiniert die Suche nach
relevanten Informationen mit der Textgenerierung durch
ein Sprachmodell.

Das System besteht aus zwei wesentlichen Prozessen:

**1. Datenaufbereitung und Indexierung**

- Unterstützungsangebote recherchieren
- Informationen strukturieren
- Texte aufbereiten
- Embeddings erzeugen
- Daten in einer Vektordatenbank indexieren

**2. Informationsabruf und Antwortgenerierung**

- Nutzeranfrage verarbeiten
- Relevante Dokumente abrufen
- Suchergebnisse als Kontext bereitstellen
- Empfehlung durch ein Sprachmodell generieren
- Quellen und Angebotsinformationen ausgeben

## Technologien

Für die Umsetzung sind folgende Technologien vorgesehen:

| Technologie | Funktion |
|------------|----------|
| Python | Programmiersprache und Anwendungslogik |
| Streamlit | Webbasierte Benutzeroberfläche |
| LlamaIndex | RAG-Verarbeitung und Anbindung der Wissensdatenbank |
| ChromaDB | Vektordatenbank für die semantische Suche |
| Embedding-Modell | Umwandlung von Texten in Vektorrepräsentationen |
| Large Language Model (LLM) | Generierung personalisierter Empfehlungen |
| GitHub | Versionsverwaltung und Projektdokumentation |
| PlantUML | Modellierung der Systemarchitektur und Prozesse |

**Hinweis:** Die genannten Technologien stellen die aktuell
vorgesehene technische Architektur dar und können im Verlauf
der Projektentwicklung angepasst werden.

## Wissensdatenbank

Die Wissensdatenbank bildet die Grundlage des RAG-Systems.

Sie soll Informationen über KI-Unterstützungsangebote
verschiedener Organisationen enthalten.

### Vorgesehene Informationsquellen

| Organisation | Website |
|-------------|---------|
| IHK Mittlerer Niederrhein | https://mittlerer-niederrhein.ihk.de/ |
| KI.NRW | https://www.ki.nrw/ |
| AI Village | https://aivillage.de/ |
| digihub | https://digihub.de/ |
| Hochschulen | Jeweilige Hochschulwebsites |

### Geplante Datenstruktur

Für jedes Unterstützungsangebot sollen relevante
Informationen gespeichert werden.

Beispielsweise:

| Datenfeld | Beschreibung |
|----------|--------------|
| Anbieter | Organisation, die das Angebot bereitstellt |
| Angebotsname | Bezeichnung des Unterstützungsangebots |
| Kategorie | Orientierung, Qualifizierung, Prototyping oder Umsetzung |
| Beschreibung | Inhalt und Zielsetzung des Angebots |
| Zielgruppe | Unternehmen bzw. Personen, für die das Angebot geeignet ist |
| Region | Geografischer Geltungsbereich |
| Quelle | Link zur ursprünglichen Informationsquelle |

Die gesammelten Informationen können zunächst in einer
CSV-Datei strukturiert und anschließend für die
semantische Suche indexiert werden.

## Installation

**Status: Geplant – noch nicht implementiert**

Die folgende Installation beschreibt den vorgesehenen
technischen Aufbau. Die konkreten Installationsschritte
werden nach der Implementierung ergänzt und überprüft.

### Voraussetzungen

- Python 3.12 oder eine mit den verwendeten Bibliotheken kompatible Version
- Git
- Visual Studio Code oder eine vergleichbare Entwicklungsumgebung
- Zugang zu einem geeigneten Sprachmodell
- Gegebenenfalls ein API-Schlüssel für den gewählten LLM-Anbieter

### Setup-Anleitung

#### 1. Repository klonen

```bash
git clone https://github.com/SinanKendir/RAG-System-KI-Kompass
```

#### 2. Virtuelle Umgebung erstellen

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

#### 3. Bibliotheken installieren

Nach Erstellung der entsprechenden Projektdatei:

```bash
pip install -r requirements.txt
```

#### 4. Anwendung starten

Bei Umsetzung der Benutzeroberfläche mit Streamlit:

```bash
streamlit run app.py
```

Der tatsächliche Dateiname und die Startanweisung
werden im Verlauf der Implementierung festgelegt.

## Konfiguration

### Sprachmodell

Für die Generierung personalisierter Empfehlungen
wird ein geeignetes Sprachmodell benötigt.

Die konkrete Auswahl ist noch offen.

Mögliche Varianten:

- Cloudbasiertes Sprachmodell über eine API
- Lokal betriebenes Open-Source-Sprachmodell

### API-Konfiguration

Falls ein cloudbasiertes Sprachmodell verwendet wird,
können erforderliche Zugangsdaten über Umgebungsvariablen
verwaltet werden.

Beispiel einer möglichen `.env`-Datei:

```env
LLM_API_KEY=your_api_key_here
```

Der konkrete Variablenname hängt vom gewählten
Sprachmodell beziehungsweise API-Anbieter ab.

**Wichtig:** API-Schlüssel dürfen nicht öffentlich
im GitHub-Repository gespeichert werden.

## Anwendungsbeispiel

### Beispiel: Maschinenbauunternehmen

Ein mittelständisches Maschinenbauunternehmen möchte
Künstliche Intelligenz zur automatisierten Qualitätskontrolle
einsetzen.

Das Unternehmen verfügt bisher über wenig KI-Erfahrung
und möchte zunächst die technische Machbarkeit überprüfen.

### Nutzereingaben

```json
{
  "branche": "Maschinenbau",
  "mitarbeiter": 80,
  "ki_erfahrung": "Keine",
  "ki_ziel": "Automatisierte Qualitätskontrolle",
  "unterstuetzungsbedarf": "KI-Idee testen"
}
```

### Bedarfsklassifizierung

Der Entscheidungsbaum ordnet das Unternehmen
folgender Kategorie zu:

```json
{
  "kategorie": "Prototyping"
}
```

### Beispielhafte Systemausgabe

```json
{
  "kategorie": "Prototyping",
  "empfehlung": "Erprobung einer KI-basierten Qualitätskontrolle",
  "angebote": [
    {
      "anbieter": "Beispielorganisation",
      "angebot": "KI-Prototyping-Unterstützung",
      "begruendung": "Das Angebot unterstützt Unternehmen bei der praktischen Erprobung von KI-Anwendungen.",
      "quelle": "https://example.org"
    }
  ]
}
```

**Hinweis:** Die dargestellten Daten und Empfehlungen
sind ausschließlich illustrative Beispiele.
Es handelt sich nicht um tatsächlich recherchierte Angebote.

## Evaluation

Die Qualität des KI-Kompasses soll im Projektverlauf
systematisch untersucht werden.

### Mögliche Bewertungskriterien

- Relevanz der empfohlenen Unterstützungsangebote
- Korrektheit der Bedarfsklassifizierung
- Nachvollziehbarkeit der Empfehlungen
- Qualität der Quellenangaben
- Benutzerfreundlichkeit
- Antwortzeit des Systems

### Geplantes Vorgehen

1. Definition geeigneter Testszenarien
2. Erstellung beispielhafter Unternehmensprofile
3. Durchführung von Testanfragen
4. Bewertung der generierten Empfehlungen
5. Identifikation von Verbesserungspotenzialen
6. Überarbeitung des Systems
7. Erneute Evaluation

Die konkreten Evaluationsmethoden und Messgrößen
werden im weiteren Projektverlauf festgelegt.

## Projektstatus

**Aktueller Stand: Konzeption und technische Planung**

Das Projekt wird im Rahmen des Hochschulmoduls
„KI-Anwendungen in der betrieblichen Praxis“ entwickelt.

Die Entwicklung erfolgt anhand mehrerer Meilensteine.

| Meilenstein | Inhalt | Zeitraum |
|------------|--------|----------|
| 1 | Technische Konzeption und UML-Modellierung | KW 42 |
| 2 | Entwicklung eines ersten Prototyps | KW 45 |
| 3 | Erste empirische Evaluation | KW 48 |
| 4 | Überarbeitung und Version 2.0 | KW 50 |
| 5 | Zweite empirische Evaluation | KW 1 |
| Abschluss | Projektdokumentation und Präsentation | KW 4 / 2027 |

## Projektziel

Ziel ist die Entwicklung eines funktionsfähigen
KI-Kompasses, der kleinen und mittleren Unternehmen
den Zugang zu geeigneten KI-Unterstützungsangeboten
erleichtert.

Durch die Kombination aus interaktivem Entscheidungsbaum,
semantischer Suche und KI-generierten Empfehlungen
soll eine nachvollziehbare und bedarfsgerechte
Orientierung innerhalb bestehender Unterstützungsangebote
ermöglicht werden.
