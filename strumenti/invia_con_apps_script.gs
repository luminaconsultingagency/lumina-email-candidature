/**
 * Invio dell'email con Google Apps Script, mantenendo intatto l'HTML (compreso il <style> del dark mode),
 * che invece Gmail elimina quando si incolla l'email nella finestra di scrittura.
 *
 * Come si usa:
 * 1. Vai su https://script.google.com con l'account che deve inviare (es. lumina@lumina.h-farm.com).
 * 2. Nuovo progetto → incolla questo file.
 * 3. Controlla DESTINATARI e OGGETTO qui sotto.
 * 4. Lancia prima `inviaProva` (arriva solo a te), controlla l'email, poi lancia `inviaATutti`.
 *    La prima volta Google ti chiede di autorizzare l'accesso a Gmail.
 */

const URL_HTML = 'https://cdn.jsdelivr.net/gh/luminaconsultingagency/lumina-email-candidature@main/dist/email-da-inviare.html'; // (punta sempre all'ultima versione su main)
const OGGETTO = 'LUMINA - Application Form';
const NOME_MITTENTE = 'Lumina Consulting Agency';
const DESTINATARI = 'lumina@lumina.h-farm.com'; // gruppo o lista, separati da virgola

function leggiHtml_() {
  return UrlFetchApp.fetch(URL_HTML).getContentText('UTF-8');
}

function inviaProva() {
  const me = Session.getActiveUser().getEmail();
  GmailApp.sendEmail(me, '[PROVA] ' + OGGETTO, 'Apri questa email con un client che supporta l\'HTML.', {
    htmlBody: leggiHtml_(),
    name: NOME_MITTENTE,
  });
}

function inviaATutti() {
  GmailApp.sendEmail(DESTINATARI, OGGETTO, 'Apri questa email con un client che supporta l\'HTML.', {
    htmlBody: leggiHtml_(),
    name: NOME_MITTENTE,
  });
}
