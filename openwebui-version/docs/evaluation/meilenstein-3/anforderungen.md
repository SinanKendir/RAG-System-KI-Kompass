# Anforderungen (Meilenstein 3)

Abgeleitet aus der Aufgabenstellung (Orientierung von KMU über einen Entscheidungsbaum mit vier Phasen) und dem System-Prompt des KI-Kompass.

| ID | Anforderung | Beschreibung | Testfälle | Schwelle |
|---|---|---|---|---|
| A1 | Phasenzuordnung | Das Anliegen wird der richtigen Phase (Orientierung, Qualifizierung, Prototyping, Umsetzung) zugeordnet. | F01–F12 ohne F08, F11 | ≥ 80 % |
| A2 | Inhaltliche Korrektheit | Mindestens ein erwartetes Angebot wird mit korrektem Namen genannt bzw. die Sachfrage wird richtig beantwortet. | F01–F12 | ≥ 80 % |
| A3 | Keine Halluzination | Keine erfundenen Angebote, Leistungen, Kosten, Termine, Quellen oder Ansprechpersonen. | F01–F16 | 100 % |
| A4 | Umgang mit Wissenslücken | Fehlende Information wird offen benannt, nichts erfunden, Verweis an IHK/Anbieter. | F14, F15 | 100 % |
| A5 | Dialogführung (Entscheidungsbaum) | Unklare Phase: genau eine Rückfrage. Klare Phase: direkt 1–3 Angebote, keine überflüssige Phasen-Rückfrage. | F01–F16 | ≥ 80 % |
| A6 | Themenabgrenzung | Fragen ohne Bezug zu KI-Angeboten werden freundlich abgegrenzt. | F16 | 100 % |
| A7 | Zielgruppengerechte Sprache | Deutsch, durchgängig Sie-Form, ohne Fachjargon. | F01–F16 | ≥ 90 % |
| A8 | Antwortzeit | Median der Antwortzeit auf dem Mac ≤ 30 Sekunden. | alle | ≤ 30 s |
| A9 | Nachvollziehbarkeit | Zu jeder Empfehlung werden die genutzten Quellen angezeigt. | alle | 100 % |

**Bewertung:** 1 = erfüllt, 0,5 = teilweise, 0 = nicht erfüllt. Erfüllungsgrad = Mittelwert über die anwendbaren Testfälle.
