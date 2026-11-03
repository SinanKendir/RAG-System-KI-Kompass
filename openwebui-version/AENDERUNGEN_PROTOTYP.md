# KI-Kompass – Änderungen am Prototyp

Stand: 03.11.2026 · Meilenstein „Prototyp“ (KW 45)

## Ausgangslage

Der erste Prototyp (Open WebUI 0.12.5 + Ollama, Modell `llama3.1` 8B) lieferte unbrauchbare Antworten:

- Das Modell bot Werkzeuge wie `create_tasks` oder `create_calendar_event` an, statt die Frage zu beantworten.
- Es erfand Angebote, die es nicht gibt (z. B. „KI-Nachbarschaftsnetzwerk“, „KI-Workshops der IHK“), und empfahl externe Plattformen wie Coursera oder Udemy.
- Unter den Antworten wurden keine Quellen angezeigt. Die Wissensbasis wurde also nicht genutzt.

## Änderungen und Begründung

### 1. Wissensbasis

| Änderung | Begründung |
|---|---|
| Recherche-Tabelle (PDF) in Markdown umgebaut: ein Abschnitt pro Angebot mit Anbieter, Phase, Format, Inhalt | Tabellen zerfallen beim Chunking und verlieren die Spaltenzuordnung. Eigenständige Abschnitte bleiben auch einzeln verständlich. |
| Definitionen der vier Phasen (Orientierung, Qualifizierung, Prototyping, Umsetzung) an den Anfang gestellt | Damit kann das Modell Anfragen in Alltagssprache einer Phase zuordnen. |
| Text als Datei hochgeladen; vorher stand er nur im Beschreibungsfeld der Wissensbasis | Die Wissensbasis enthielt keine Datei und war daher leer. |
| Abschnitte „Übersicht nach Phase“ und „Vergleich der Anbieter“ entfernt | Bei Phasen-Fragen wurde nur die Übersicht gefunden, die bloß Angebotsnamen enthält. Das Modell verwechselte dadurch Namen („KI.Shadowing“ statt „AI.Shadowing“) und beschrieb Angebote ungenau. Jetzt werden die einzelnen Angebotsabschnitte mit Beschreibung gefunden. |

### 2. Modell und Modelleinstellungen

| Änderung | Begründung |
|---|---|
| Sprachmodell von `llama3.1` (8B) auf `gemma3:12b` gewechselt | `llama3.1` ignorierte die Wissensbasis selbst dann, wenn sie vollständig im Prompt stand. `gemma3:12b` hält sich auf Deutsch deutlich zuverlässiger an den Kontext und läuft mit 16 GB RAM lokal. |
| Wissensbasis mit dem Modell „KI-Kompass“ verknüpft | Vorher war keine Wissensbasis angehängt. |
| Function Calling auf „Legacy“ gestellt | In Open WebUI 0.12.5 wird eine angehängte Wissensbasis nur in diesem Modus automatisch per RAG abgefragt (geprüft im Quellcode, `utils/middleware.py`). Im Standardmodus „Native“ müsste das Modell sie selbst über eingebaute Werkzeuge aufrufen. |
| Eingebaute Werkzeuge, Code-Interpreter, Terminal, Websuche, Bildgenerierung und Erinnerungen deaktiviert | Diese Werkzeuge waren die Ursache für die Vorschläge wie `create_tasks`. Der KI-Kompass braucht keine davon. |
| Kontextlänge (`num_ctx`) auf 8192, Temperatur auf 0,2 | Ollamas Standard-Kontext ist zu klein für System-Prompt plus abgerufene Abschnitte. Eine niedrige Temperatur reduziert freies Fabulieren. |

### 3. System-Prompt

| Änderung | Begründung |
|---|---|
| Nur Angebote empfehlen, deren Name exakt in der Wissensbasis steht | Verhindert erfundene oder leicht abgewandelte Angebotsnamen. |
| Kosten, Dauer und Format nur nennen, wenn sie im Kontext stehen | Das Modell hatte z. B. „ca. 2–4 Stunden“ für Elements of AI ergänzt, was nicht in der Quelle steht. |
| Bei unklarer Phase genau eine Rückfrage, sonst direkt empfehlen | Das Modell stellte vorher drei Fragen auf einmal (Branche, Größe, Ziel), auch wenn die Phase schon erkennbar war. |
| Festes Antwortformat: Name, Anbieter, Phase, Inhalt, Begründung | Einheitliche, vergleichbare Antworten; Grundlage für die spätere Auswertung. |
| Hinweis, dass keine Werkzeuge verfügbar sind | Zusätzliche Absicherung gegen Tool-Vorschläge. |

### 4. Retrieval (RAG)

| Änderung | Begründung |
|---|---|
| Embedding-Modell von `all-MiniLM-L6-v2` (englisch) auf `bge-m3` (mehrsprachig, über Ollama) gewechselt und neu indexiert | Das englische Modell fand bei deutschen Fragen die falschen Abschnitte. Mit `bge-m3` wurden z. B. bei der Mitarbeiter-Frage genau die passenden Angebote (KI.Kick-off, Elements of AI) gefunden. |
| Hybride Suche aktiviert (Stichwortsuche BM25 + Vektorsuche), Top-K = 5 | Exakte Namen wie „KI.DeepDive“ oder „digihub“ werden über die Stichwortsuche zuverlässiger gefunden. |
| Abfragegenerierung deaktiviert | Open WebUI formulierte die Nutzerfrage vor der Suche um. Dabei gingen relevante Begriffe verloren, und die Treffer waren schlechter als mit der Originalfrage. |
| RAG-Vorlage angepasst: kein Rückgriff auf eigenes Modellwissen | Die Standardvorlage erlaubte ausdrücklich, ohne passenden Kontext aus eigenem Wissen zu antworten. Das widerspricht dem Ziel, nur belegte Angebote zu nennen. |

### 5. Oberfläche (Entscheidungsbaum)

| Änderung | Begründung |
|---|---|
| Vier Einstiegs-Buttons beim Modell hinterlegt: Orientierung, Qualifizierung, Prototyping, Umsetzung | Setzt den in der Projektbeschreibung geforderten interaktiven Entscheidungsbaum um. Nutzer ohne KI-Vorwissen finden so direkt den passenden Einstieg. |

## Aktueller Systemaufbau

- Oberfläche: Open WebUI 0.12.5 (Docker), lokal
- Sprachmodell: `gemma3:12b` über Ollama
- Embeddings: `bge-m3` über Ollama
- Wissensbasis: `ki-kompass_wissensbasis.md`, aufgeteilt nach Markdown-Überschriften
- Suche: hybrid (BM25 + Vektor), Top-K = 5, ohne Abfragegenerierung
- Function Calling: Legacy (automatisches RAG)

## Ergebnisse der Stichproben

| Testfrage | Vorher (llama3.1, ohne Wissensbasis) | Jetzt |
|---|---|---|
| „Ich brauche Unterstützung für mein Unternehmen“ | Bietet `create_tasks` und `create_calendar_event` an | Eine Rückfrage nach der Phase |
| „Wie kann ich meine Mitarbeiter auf KI vorbereiten, ohne sie in den Unterricht zu schicken?“ | Erfundene Angebote, Coursera/Udemy | KI.Kick-off und Elements of AI, korrekt beschrieben |
| „Wir haben eine konkrete Idee und wollen die Machbarkeit prüfen“ | – | KI.DeepDive und Machbarkeitsstudien, korrekte Namen und Phasen |
| „Was ist der KI.DeepDive?“ | – | Korrekte Erklärung inkl. „Konzept, kein fertiger Prototyp“ |

Dies sind Einzelstichproben, noch keine systematische Messung.

## Offene Punkte

- Die Wissensbasis enthält keine Links, Kosten, Termine oder Ansprechpartner. Das System kann Nutzer deshalb noch nicht konkret weiterleiten.
- Unternehmen formulieren Fragen oft anders als die Angebotsbeschreibungen. Stichworte in Alltagssprache pro Angebot (z. B. „Mitarbeitende schulen“, „Selbstlernkurs“) dürften die Treffer weiter verbessern.
- Das Modell hängt teilweise noch unnötige Rückfragen an.
- Ein Reranker (z. B. `bge-reranker-v2-m3`) wurde noch nicht getestet.

## Ausblick: Empirische Messung (Meilenstein 3, KW 48)

Ziel ist, die Frage „Sind die Anforderungen erfüllt?“ mit Zahlen zu beantworten statt mit Einzelbeispielen.

1. **Testset erstellen:** ca. 15–20 typische Unternehmensfragen, verteilt auf alle vier Phasen, inkl. unklarer Fragen und Fragen ohne passendes Angebot. Für jede Frage wird vorab festgelegt, welche Angebote richtig sind.
2. **Messgrößen:**
   - Retrieval-Trefferquote: Ist das richtige Angebot unter den 5 gefundenen Abschnitten?
   - Empfehlungsgenauigkeit: Nennt die Antwort die richtigen Angebote?
   - Halluzinationsrate: Anteil der Antworten mit erfundenen Angeboten, Namen oder Angaben
   - Phasen-Zuordnung: Wird die Phase richtig erkannt bzw. bei Unklarheit nachgefragt?
   - Antwortzeit
3. **Vergleich der Ausbaustufen** mit identischem Testset, um den Effekt jeder Änderung zu belegen:
   - `llama3.1` ohne Wissensbasis (Ausgangszustand)
   - `gemma3:12b` mit kompletter Wissensbasis im Prompt (ohne Retrieval)
   - `gemma3:12b` + RAG mit englischen Embeddings
   - `gemma3:12b` + RAG mit `bge-m3` und hybrider Suche (aktueller Stand)
4. **Durchführung:** Die Testfragen werden automatisiert über die Open-WebUI-Schnittstelle gestellt, Antworten und gefundene Quellen protokolliert und anschließend ausgewertet. Die Ergebnisse fließen in die Evaluation der Hausarbeit ein und dienen als Basis für die zweite Messung (Meilenstein 5).
