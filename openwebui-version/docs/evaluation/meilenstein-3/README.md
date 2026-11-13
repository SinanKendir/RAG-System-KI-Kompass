# Meilenstein 3 – Empirische Messung

**Leitfrage:** Erfüllt Prototyp 1 des KI-Kompass die Anforderungen?
Durchgeführt am 13.11.2026 lokal (Ollama + Open WebUI 0.12 auf einem Mac), Datenbasis unverändert aus Prototyp 1 (29 Angebote, 5 Anbieter).

## Inhalt dieses Ordners

| Datei | Inhalt |
|---|---|
| `anforderungen.md` | Anforderungen A1–A9 mit Schwellenwerten |
| `testset.md` | 16 Testfragen mit Soll-Antworten und erwarteten Angeboten |
| `bewertung.csv` | Bewertung jeder Antwort (1 = erfüllt, 0,5 = teilweise, 0 = nicht, leer = nicht anwendbar), Antwortzeit, Kommentar |
| `rohdaten_teil1_varianten.json` | 64 Antworten im Wortlaut inkl. gefundener Abschnitte |
| `rohdaten_teil2_einstellungen.json` | 128 Antworten im Wortlaut inkl. gefundener Abschnitte |
| `testskript.js` | Skript zum Wiederholen der Messung |

## Testdesign

**Teil 1 – Varianten (64 Antworten):** 2 Modelle × mit/ohne RAG, sonst identische Einstellungen (System-Prompt des KI-Kompass, Temperatur 0,2, num_ctx 8192, Top-K 5, hybride Suche, Function Calling „Legacy“).

| Variante | Modell | RAG |
|---|---|---|
| V1 | llama3.1 (8B) | ohne |
| V2 | llama3.1 (8B) | mit |
| V3 | gemma3:12b | ohne |
| V4 | gemma3:12b | mit = Prototyp 1 |

**Teil 2 – Einstellungen (128 Antworten):** beide Modelle mit RAG, je eine Einstellung verändert: Top-K 3, Top-K 10, nur Vektorsuche, Temperatur 0,7.

Je ein Durchlauf pro Frage. Die Bewertung erfolgte KI-gestützt (Claude) anhand der vorab festgelegten Kriterien und Soll-Antworten; sie wurde nicht unabhängig doppelt geprüft.

## Ergebnisse Teil 1

| | V1 | V2 | V3 | V4 |
|---|---|---|---|---|
| A1 Phasenzuordnung (≥ 80 %) | 90 % | 90 % | 70 % | 90 % |
| A2 Inhaltliche Korrektheit (≥ 80 %) | 0 % | 88 % | 8 % | 88 % |
| A3 Keine Halluzination (100 %) | 50 % | 100 % | 50 % | 100 % |
| A4 Umgang mit Wissenslücken (100 %) | 25 % | 100 % | 50 % | 75 % |
| A5 Dialogführung (≥ 80 %) | 88 % | 94 % | 62 % | 69 % |
| A6 Themenabgrenzung (100 %) | 100 % | 100 % | 100 % | 100 % |
| A7 Sie-Form (≥ 90 %) | 69 % | 88 % | 94 % | 100 % |
| A8 Median Antwortzeit (≤ 30 s) | 7,4 s | 9,5 s | 15,2 s | 26,9 s |
| A9 Quellenanzeige (100 %) | 0 % | 100 % | 0 % | 100 % |
| **Erfüllt** | **4/9** | **8/9** | **3/9** | **7/9** |

- Ohne RAG enthalten 8 von 16 Antworten erfundene Angebote, mit RAG keine.
- Die Suche liefert in 11 von 12 Fällen das erwartete Angebot; F01 („erste Beratung“) findet die Sprechstunden nicht.
- Prototyp 1 verfehlt A5 (überflüssige Phasen-Rückfrage in 8 von 16 Antworten) und A4 (F15 ohne Verweis an die IHK).

## Ergebnisse Teil 2

| Konfiguration | llama3.1 erfüllt | gemma3 erfüllt | gemma3 Median-Zeit |
|---|---|---|---|
| Basis (Top-K 5, hybrid, T 0,2) | 8/9 | 7/9 | 26,9 s |
| Top-K 3 | 8/9 | 7/9 | 19,9 s |
| Top-K 10 | 8/9 | 7/9 | 50,7 s |
| Nur Vektorsuche | 8/9 | 5/9 | 37,7 s |
| Temperatur 0,7 | 8/9 | 9/9 | 17,9 s |

- Die gefundenen Abschnitte sind bei allen Sucheinstellungen gleich (11 von 12).
- „Nur Vektorsuche“ bei gemma3 (5/9): gleiche Abschnitte wie bei hybrider Suche; die längere Antwortzeit lag vermutlich an der Auslastung des Macs, nicht an der Einstellung.
- Top-K 10 verdoppelt die Antwortzeit von gemma3; llama3.1 erfindet dabei Seitenangaben.
- Temperatur 0,7 bei gemma3: 9/9, hängt aber an 2–3 Einzelantworten und ist bei einem Durchlauf nicht belastbar.
- Antwortzeiten schwanken mit der Auslastung des Macs.

## Fazit und nächste Schritte

Die Wissensdatenbank ist der entscheidende Faktor, die Einstellungen sind es nicht. Für Prototyp 2: System-Prompt (Phasen-Rückfrage nur bei unklarer Phase, Verweis an die IHK bei Lücken, durchgängig Sie-Form), Wissensbasis erweitern (Synonyme wie „Beratung“), Modellwahl llama3.1 vs. gemma3 prüfen. In Meilenstein 5 wird die Messung mit denselben Fragen und mehreren Durchläufen wiederholt.

## Messung wiederholen

1. Open WebUI unter http://localhost:3000 öffnen und anmelden.
2. Entwicklerkonsole des Browsers öffnen (Cmd + Alt + J), Inhalt von `testskript.js` einfügen, ggf. `VARIANTEN` und `KB_ID` anpassen.
3. Nach dem Lauf liegen die Ergebnisse unter `localStorage.evalErgebnisse` und werden als JSON heruntergeladen.
