# AGENTS.md — contesto per agenti AI

Questo repository contiene l'email HTML con cui Lumina Consulting Agency (la consulting agency studentesca di
H-FARM College) apre ogni anno le candidature. Chi te lo chiede di solito è uno studente, spesso poco tecnico,
che deve preparare l'email dell'anno nuovo. Rispondi nella lingua dell'utente (di solito italiano).
Il README spiega tutto dal punto di vista umano: qui ci sono le regole da rispettare quando modifichi il codice.

## File

- `email.html`: **l'unico sorgente da modificare.** Le immagini hanno `src="immagini/..."` (percorsi relativi).
- `dist/email-da-inviare.html`: generato. Non modificarlo a mano: rigeneralo con `python3 build.py [--repo owner/nome] [--ref tag]`.
- `immagini/`: le immagini servite online con jsDelivr (`https://cdn.jsdelivr.net/gh/<owner>/<repo>@<ref>/immagini/<file>`).
- `sorgenti/`: gli originali ad alta risoluzione. `archivio/2025/`: l'email precedente (generata da postcards.email). Solo come riferimento.

## Struttura di `email.html`

- Layout email classico: tabelle annidate, contenitore largo 600 px, stili **inline**. Non convertirlo a flex/grid
  o a CSS esterno: Gmail e Outlook lo romperebbero.
- Ordine: header (immagine) → IT (intro, aziende, "Come Siamo Organizzati" + `unit-ita.png`, CTA, Business Game)
  → EN (stesse sezioni, `unit-en.png`) → footer (firma, logo, icone social).
- IT ed EN sono **duplicati**: ogni modifica al testo (date, link, descrizioni) va fatta in entrambe le lingue.
  I pulsanti di candidatura sono 2 (`href="https://forms.gle/..."`).
- Font: `'Fira Sans', Arial, Helvetica, sans-serif`. Colori del brand: arancione `#ff3b00`, verde `#acd800`,
  pulsante `#1595e7`, testo `#151515` / `#333333`, sfondo `#f4f4f4`.

## Regole che non devi rompere

1. **Punteggiatura tra gli span.** Il testo è diviso in `<span>`. Non lasciare spazi o a capo tra `</span>` e uno
   `<span>` il cui contenuto inizia con `, . ; : ! ?`, altrimenti compare uno spazio prima della punteggiatura.
   Verifica con una regex tipo `</span>\s+<span[^>]*>[,.;:!?]`: non deve trovare niente.
2. **Dark mode: niente CSS, niente immagini nascoste.** L'email si invia incollandola in Gmail, che elimina il `<style>`
   e in dark mode su mobile ricolora sfondi e testi, ma non le immagini. Quindi:
   - tutto ciò che deve restare di un colore preciso (pulsanti, logo, icone) è un **PNG con lo sfondo incluso**;
   - i pulsanti CTA sono immagini (`immagini/pulsante-*.png`, generate con Fira Sans Medium 16px, padding 14/19px, raggio 8px,
     a 3x) dentro un `<a>`, con un `alt` uguale al testo;
   - **non** reintrodurre lo scambio di immagini con `@media (prefers-color-scheme: dark)` e `display:none`: le copie nascoste
     hanno fatto mostrare a Gmail mobile le icone social al posto delle immagini delle Unit;
   - non usare PNG trasparenti con contenuto scuro: aggiungi uno sfondo pieno (con PIL: `alpha_composite` su un'immagine bianca).
3. **Immagini:** esportale al doppio della larghezza a cui appaiono (retina), sotto i 200 KB se possibile, e mantieni
   gli `alt` descrittivi. Se l'utente ti manda una nuova immagine, copiala in `immagini/` con un nome in minuscolo,
   senza spazi (quelli nei nomi rompono gli URL), e tieni l'originale in `sorgenti/`.
4. **Hosting:** mai Google Drive e mai servizi temporanei (litterbox, tmpfiles...): chi apre l'email mesi dopo vedrebbe
   le immagini rotte. Usa jsDelivr su questo repository, su un tag o sull'hash di un commit (`--ref`). Se jsDelivr risponde 404 subito dopo un push, ha memorizzato il 404: usa l'hash completo del commit invece del tag.
5. **Privacy:** il repository è pubblico. Non committare file `.eml`, che contengono header con indirizzi personali,
   né `.env` o token.
6. Non mettere i badge di postcards.email: il template non dipende più da quel servizio.

## Come verificare le modifiche

- Servi la cartella in locale (`python3 -m http.server`) e apri `email.html`: con `file://` alcuni browser non caricano le immagini.
- Per simulare Gmail in dark mode, scurisci via JS gli sfondi e schiarisci i testi: logo, icone e pulsanti devono restare leggibili.
- Dopo `build.py`, controlla che in `dist/email-da-inviare.html` non resti nessun `src="immagini/`.
- Prima dell'invio vero, suggerisci all'utente di mandare una prova a se stesso (Gmail iPhone in dark mode, Apple Mail, Outlook).

## Checklist dell'anno nuovo

- [ ] Date: scadenza delle candidature e Business Game (IT + EN)
- [ ] Link del Google Form in entrambi i pulsanti
- [ ] Testo "aziende con cui abbiamo collaborato" e immagine `aziende.png`
- [ ] Unit/Team: testo breve e immagini `unit-ita.png` / `unit-en.png`
- [ ] `python3 build.py`, commit, tag, `python3 build.py --ref <tag>`
- [ ] Email di prova
