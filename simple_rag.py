"""
Ganz einfaches RAG mit Entscheidungsbaum:

  0. ENTSCHEIDUNGSBAUM – Fragen mit Antwortmöglichkeiten
  1. RETRIEVAL         – passende Angebote heraussuchen
  2. AUGMENTED         – Antworten + gefundene Angebote in einen Prompt packen
  3. GENERATION        – ein Sprachmodell (LLM) formuliert die Empfehlung

Benötigt nur Python und Ollama (kostenloses, lokales LLM): https://ollama.com
Vorher einmal im Terminal:  ollama pull llama3.2
"""

import json
import re
import urllib.request

OLLAMA_URL = "http://localhost:11434/api/generate"
MODELL = "llama3.2"

# ------------------------------------------------------------------
# Wissensdatenbank – BEISPIEL-Angebote, keine echten Daten
# ------------------------------------------------------------------
ANGEBOTE = [
    {"phase": "Orientierung", "text": "IHK (Beispiel): Kostenlose KI-Sprechstunde. Erstgespräch für Unternehmen "
     "ohne KI-Erfahrung, um zu klären, wo KI im Betrieb sinnvoll ist."},
    {"phase": "Orientierung", "text": "KI.NRW (Beispiel): Kostenlose Webinar-Reihe zu KI-Grundlagen für "
     "Geschäftsführung und Fachkräfte. Erklärt, was KI kann und was nicht."},
    {"phase": "Qualifizierung", "text": "Hochschule (Beispiel): Mehrwöchige Weiterbildung, in der Mitarbeitende "
     "lernen, KI-Werkzeuge im Alltag einzusetzen. Kostenpflichtig."},
    {"phase": "Qualifizierung", "text": "AI Village (Beispiel): Eintägiger Workshop zu ChatGPT im Büro für "
     "Verwaltung, Vertrieb und Marketing, damit Mitarbeitende entlastet werden."},
    {"phase": "Prototyping", "text": "digihub (Beispiel): Prototyp-Sprint, in dem KMU mit einer konkreten Idee "
     "zusammen mit einem Start-up einen ersten Prototyp bauen, z. B. um Abläufe zu automatisieren. Teilweise gefördert."},
    {"phase": "Prototyping", "text": "Hochschule (Beispiel): Studentisches Praxisprojekt, in dem Studierende einen "
     "Prototyp für eine KI-Anwendung im Unternehmen entwickeln, z. B. um Qualität zu verbessern. Kostenlos."},
    {"phase": "Umsetzung", "text": "KI.NRW (Beispiel): Kostenlose Umsetzungsberatung und Hilfe bei der Suche nach "
     "Fördermitteln, um eine KI-Lösung dauerhaft im Betrieb einzuführen."},
]

# ------------------------------------------------------------------
# Entscheidungsbaum
# Jede Antwort führt entweder zur nächsten Frage ("weiter") oder zur Phase ("phase").
# ------------------------------------------------------------------
PROFILFRAGEN = [
    ("Branche", "In welcher Branche ist Ihr Unternehmen tätig?",
     ["Handwerk", "Produktion / Industrie", "Handel", "Dienstleistung", "Sonstiges"]),
    ("Größe", "Wie viele Mitarbeitende hat Ihr Unternehmen?",
     ["1–9", "10–49", "50–249", "250 oder mehr"]),
    ("Ziel", "Was möchten Sie mit KI vor allem erreichen?",
     ["Abläufe automatisieren", "Kunden besser bedienen", "Qualität verbessern",
      "Mitarbeitende entlasten", "Weiß ich noch nicht"]),
]

BAUM = {
    "erfahrung": ("Wie viel Erfahrung hat Ihr Unternehmen bereits mit KI?", [
        ("Noch keine", {"weiter": "anwendungsfall"}),
        ("Erste Versuche, z. B. mit ChatGPT", {"weiter": "idee"}),
        ("KI ist bei uns schon im Einsatz", {"phase": "Umsetzung"}),
    ]),
    "anwendungsfall": ("Wissen Sie schon, wofür Sie KI nutzen möchten?", [
        ("Nein, wir wollen erst verstehen, was möglich ist", {"phase": "Orientierung"}),
        ("Ja, ungefähr", {"weiter": "engpass"}),
    ]),
    "idee": ("Haben Sie eine konkrete Projektidee?", [
        ("Ja", {"weiter": "prototyp"}),
        ("Nein, noch nicht", {"weiter": "engpass"}),
    ]),
    "engpass": ("Was fehlt Ihnen gerade am meisten?", [
        ("Wissen und Fähigkeiten im Team", {"phase": "Qualifizierung"}),
        ("Jemand, der mit uns etwas ausprobiert und baut", {"phase": "Prototyping"}),
    ]),
    "prototyp": ("Gibt es bereits einen getesteten Prototyp?", [
        ("Nein", {"phase": "Prototyping"}),
        ("Ja, er soll jetzt in den Betrieb", {"phase": "Umsetzung"}),
    ]),
}


def auswahl(frage: str, optionen: list[str]) -> int:
    """Zeigt eine Frage mit nummerierten Antworten und gibt die gewählte Nummer (ab 0) zurück."""
    print(f"\n{frage}")
    for i, text in enumerate(optionen, start=1):
        print(f"  {i}) {text}")
    while True:
        eingabe = input("Ihre Wahl> ").strip()
        if eingabe.isdigit() and 1 <= int(eingabe) <= len(optionen):
            return int(eingabe) - 1
        print(f"  Bitte eine Zahl von 1 bis {len(optionen)} eingeben.")


def entscheidungsbaum() -> tuple[dict, str]:
    """Stellt Profil- und Baumfragen. Gibt (Antworten, Phase) zurück."""
    antworten = {}
    for schluessel, frage, optionen in PROFILFRAGEN:
        antworten[schluessel] = optionen[auswahl(frage, optionen)]

    knoten = "erfahrung"
    while True:                                   # Schleife: bis der Bedarf eindeutig ist
        frage, optionen = BAUM[knoten]
        text, ziel = optionen[auswahl(frage, [o[0] for o in optionen])]
        antworten[frage] = text
        if "phase" in ziel:
            return antworten, ziel["phase"]
        knoten = ziel["weiter"]


# ------------------------------------------------------------------
# Schritt 1: RETRIEVAL – Angebote der Phase, sortiert nach Wort-Übereinstimmung
# (Ein echtes RAG nutzt hier Embeddings und eine Vektor-Datenbank.)
# ------------------------------------------------------------------
def woerter(text: str) -> set[str]:
    return {w for w in re.findall(r"\w+", text.lower()) if len(w) > 3}


def suchen(antworten: dict, phase: str, anzahl: int = 2) -> tuple[list[str], bool]:
    """Gibt (gefundene Angebote, alternative?) zurück."""
    suchwoerter = woerter(" ".join(antworten.values()))
    passende = [a["text"] for a in ANGEBOTE if a["phase"] == phase]
    alternative = not passende
    if alternative:                               # [nein]-Zweig: allgemeine Angebote
        passende = [a["text"] for a in ANGEBOTE if a["phase"] == "Orientierung"]
    passende.sort(key=lambda t: len(suchwoerter & woerter(t)), reverse=True)
    return passende[:anzahl], alternative


# ------------------------------------------------------------------
# Schritt 2: AUGMENTED – Prompt aus Antworten + Angeboten bauen
# ------------------------------------------------------------------
def prompt_bauen(antworten: dict, phase: str, angebote: list[str]) -> str:
    profil = "\n".join(f"- {k}: {v}" for k, v in antworten.items())
    kontext = "\n".join(f"- {a}" for a in angebote)
    return (
        "Du bist ein Berater für kleine und mittlere Unternehmen.\n"
        "Empfiehl dem Unternehmen in 3–4 Sätzen die passenden Angebote. "
        "Nutze NUR die folgenden Angebote und nenne jeweils den Anbieter.\n\n"
        f"Angaben des Unternehmens:\n{profil}\n"
        f"Ermittelter Unterstützungsbedarf: {phase}\n\n"
        f"Angebote:\n{kontext}\n\n"
        "Empfehlung (auf Deutsch):"
    )


# ------------------------------------------------------------------
# Schritt 3: GENERATION – das LLM formuliert die Empfehlung
# ------------------------------------------------------------------
def llm_fragen(prompt: str) -> str:
    daten = json.dumps({"model": MODELL, "prompt": prompt, "stream": False}).encode()
    anfrage = urllib.request.Request(OLLAMA_URL, data=daten, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(anfrage, timeout=180) as antwort:
        return json.loads(antwort.read())["response"]


# ------------------------------------------------------------------
# Alles zusammen
# ------------------------------------------------------------------
def main():
    print("KI-Kompass für den Mittelstand")
    print("Beantworten Sie die Fragen mit der Nummer der passenden Antwort.")

    while True:
        antworten, phase = entscheidungsbaum()
        angebote, alternative = suchen(antworten, phase)

        print("\n" + "=" * 60)
        print(f"Ihr Unterstützungsbedarf: {phase}")
        if alternative:
            print("Für diese Phase gibt es noch keine Angebote – hier allgemeine Alternativen:")
        print("\n[Gefundene Angebote]")
        for a in angebote:
            print(" -", a)

        print("\n[Empfehlung] wird erstellt …")
        try:
            print(llm_fragen(prompt_bauen(antworten, phase, angebote)))
        except OSError:
            print("(Ollama läuft nicht. Starte die Ollama-App und führe einmal "
                  "'ollama pull llama3.2' im Terminal aus.)")
        print("=" * 60)

        if auswahl("Möchten Sie noch einmal starten?", ["Ja", "Nein, beenden"]) == 1:
            break


if __name__ == "__main__":
    main()