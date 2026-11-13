// KI-Kompass – Testskript für die empirische Messung (Meilenstein 3)
// Ausführen in der Browser-Konsole auf http://localhost:3000 (angemeldet in Open WebUI).
// Stellt jede Testfrage an jede Variante, misst die Zeit und speichert Antwort + gefundene Abschnitte.

const KB_ID = 'dfe85288-baa1-4b8f-b6fa-6dd92c09a987'; // ID der Wissensbasis „KI-Kompass Wissensbasis“ (Workspace → Knowledge)

const FRAGEN = [
 [
  "F01",
  "Orientierung",
  "Wir sind ein Handwerksbetrieb mit 20 Mitarbeitenden und wollen mit KI anfangen. Wo bekommen wir eine erste Beratung?"
 ],
 [
  "F02",
  "Orientierung",
  "Gibt es Veranstaltungen, bei denen ich mich mit anderen Geschäftsführungen über den KI-Einsatz austauschen kann?"
 ],
 [
  "F03",
  "Orientierung",
  "Was müssen wir rechtlich beachten, wenn wir KI im Unternehmen einsetzen? Wo finden wir Informationen dazu?"
 ],
 [
  "F04",
  "Qualifizierung",
  "Unsere Mitarbeitenden haben keine KI-Vorkenntnisse. Gibt es einen kostenlosen Online-Kurs zu den Grundlagen?"
 ],
 [
  "F05",
  "Qualifizierung",
  "Gibt es eine kurze Einführung in KI und maschinelles Lernen für unser Team, gerne online?"
 ],
 [
  "F06",
  "Prototyping",
  "Wir haben die Idee, die Qualitätskontrolle in der Produktion mit einer Kamera und KI zu automatisieren. Wer kann prüfen, ob das technisch machbar ist?"
 ],
 [
  "F07",
  "Prototyping",
  "Kann die Hochschule Niederrhein für uns einen KI-Prototypen entwickeln, zum Beispiel im Rahmen einer studentischen Arbeit?"
 ],
 [
  "F08",
  "Sachfrage",
  "Bekommen wir beim KI.DeepDive von KI.NRW einen fertigen Prototypen?"
 ],
 [
  "F09",
  "Orientierung / Prototyping",
  "Wir wissen noch nicht, welche KI-Anwendungsfälle es in unserem Unternehmen überhaupt gibt. Wer hilft uns, diese zu identifizieren und zu bewerten?"
 ],
 [
  "F10",
  "Umsetzung",
  "Wir suchen ein Start-up, das mit uns eine KI-Lösung umsetzt. Welche Angebote helfen dabei?"
 ],
 [
  "F11",
  "Sachfrage",
  "Entwickelt AI Village die KI-Software für uns?"
 ],
 [
  "F12",
  "Umsetzung",
  "Wir haben über AI Village einen Lösungsanbieter gefunden. Gibt es danach noch Unterstützung?"
 ],
 [
  "F13",
  "Unklar",
  "Wir interessieren uns für KI."
 ],
 [
  "F14",
  "Wissenslücke",
  "Wie viel Euro Förderung bekommen wir für ein KI-Forschungsprojekt mit der Hochschule Niederrhein und wer ist dort unser Ansprechpartner?"
 ],
 [
  "F15",
  "Wissenslücke",
  "Bietet die IHK Mittlerer Niederrhein den „KI-Gutschein NRW“ an und wie beantrage ich ihn?"
 ],
 [
  "F16",
  "Off-Topic",
  "Wie wird morgen das Wetter in Krefeld?"
 ]
];

// rag: true = Wissensbasis per files-Parameter, 'model' = Modell ki-kompass mit angehängter Wissensbasis
const VARIANTEN = {
  V1: { model: 'llama3.1:latest', rag: false },
  V2: { model: 'llama3.1:latest', rag: true },
  V3: { model: 'gemma3:12b', rag: false },
  V4: { model: 'ki-kompass', rag: 'model' },
};
const TEMPERATUR = 0.2;
// Sucheinstellungen (Top-K, hybride Suche) gelten global: Admin-Panel → Settings → Documents
// oder per POST /api/v1/retrieval/config/update {TOP_K, TOP_K_RERANKER, ENABLE_RAG_HYBRID_SEARCH}.

(async () => {
  const h = { Authorization: 'Bearer ' + localStorage.token, 'Content-Type': 'application/json' };
  const modell = await (await fetch('/api/v1/models/model?id=ki-kompass', { headers: h })).json();
  const SYSTEM = modell.params.system; // gleicher System-Prompt für alle Varianten
  const erg = JSON.parse(localStorage.getItem('evalErgebnisse') || '{}');
  for (const [vk, v] of Object.entries(VARIANTEN)) {
    const body = (frage) => {
      const b = { model: v.model, stream: false, messages: [] };
      if (v.model !== 'ki-kompass') {
        b.params = { temperature: TEMPERATUR, num_ctx: 8192, function_calling: 'legacy' };
        b.messages.push({ role: 'system', content: SYSTEM });
      }
      if (v.rag === true) b.files = [{ type: 'collection', id: KB_ID }];
      b.messages.push({ role: 'user', content: frage });
      return JSON.stringify(b);
    };
    await fetch('/api/chat/completions', { method: 'POST', headers: h, body: body('Hallo') }); // Modell vorladen
    for (const [id, , frage] of FRAGEN) {
      const key = vk + '_' + id;
      if (erg[key]) continue;
      const t0 = performance.now();
      const j = await (await fetch('/api/chat/completions', { method: 'POST', headers: h, body: body(frage) })).json();
      erg[key] = {
        ms: Math.round(performance.now() - t0),
        a: j.choices?.[0]?.message?.content,
        docs: (j.sources || []).flatMap((s) => s.document || []).map((d) => (d.match(/### ([^\n]+)/) || [])[1]).filter(Boolean),
      };
      localStorage.setItem('evalErgebnisse', JSON.stringify(erg));
      console.log(key, erg[key].ms + ' ms');
    }
  }
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(erg, null, 1)], { type: 'application/json' }));
  a.download = 'ergebnisse.json';
  a.click();
})();
