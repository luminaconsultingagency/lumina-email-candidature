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
- Le celle con sfondo bianco hanno la classe `bg-card`, la tabella esterna la classe `bg-outer`: servono al CSS del dark mode.
- Font: `'Fira Sans', Arial, Helvetica, sans-serif`. Colori del brand: arancione `#ff3b00`, verde `#acd800`,
  pulsante `#1595e7`, testo `#151515` / `#333333`, sfondo `#f4f4f4`.

## Regole che non devi rompere

1. **Punteggiatura tra gli span.** Il testo è diviso in `<span>`. Non lasciare spazi o a capo tra `</span>` e uno
   `<span>` il cui contenuto inizia con `, . ; : ! ?`, altrimenti compare uno spazio prima della punteggiatura.
   Verifica con una regex tipo `</span>\s+<span[^>]*>[,.;:!?]`: non deve trovare niente.
2. **Dark mode a due livelli** (vedi README):
   - l'immagine visibile di default (`class="light-img"`) deve essere leggibile **sia su sfondo chiaro che scuro**,
     perché Gmail ignora il CSS e inverte gli sfondi ma non le immagini. Per questo logo e icone sono "badge"
     (nero su riquadro bianco opaco);
   - la variante per il dark mode sta in `<div class="dark-img" style="display:none;overflow:hidden;max-height:0;mso-hide:all">`
     dentro `<!--[if !mso]><!--> ... <!--<![endif]-->` e viene mostrata da `@media (prefers-color-scheme: dark)` e da `[data-ogsc]`.
   - Non usare PNG trasparenti con contenuto scuro: aggiungi uno sfondo bianco pieno (con PIL: `alpha_composite` su un'immagine bianca).
3. **Immagini:** esportale al doppio della larghezza a cui appaiono (retina), sotto i 200 KB se possibile, e mantieni
   gli `alt` descrittivi. Se l'utente ti manda una nuova immagine, copiala in `immagini/` con un nome in minuscolo,
   senza spazi (quelli nei nomi rompono gli URL), e tieni l'originale in `sorgenti/`.
4. **Hosting:** mai Google Drive e mai servizi temporanei (litterbox, tmpfiles...): chi apre l'email mesi dopo vedrebbe
   le immagini rotte. Usa jsDelivr su questo repository, meglio se su un tag (`--ref v2026`) creato prima dell'invio.
5. **Privacy:** il repository è pubblico. Non committare file `.eml`, che contengono header con indirizzi personali,
   né `.env` o token.
6. Non mettere i badge di postcards.email: il template non dipende più da quel servizio.

## Come verificare le modifiche

- Servi la cartella in locale (`python3 -m http.server`) e apri `email.html`: con `file://` alcuni browser non caricano le immagini.
- Controlla la **modalità chiara e quella scura** (emulazione di `prefers-color-scheme`). Per simulare Gmail in dark mode,
  rimuovi il `<style>` dal DOM e scurisci gli sfondi: logo e icone devono restare leggibili.
- Dopo `build.py`, controlla che in `dist/email-da-inviare.html` non resti nessun `src="immagini/`.
- Prima dell'invio vero, suggerisci all'utente di mandare una prova a se stesso (Gmail iPhone in dark mode, Apple Mail, Outlook).

## Checklist dell'anno nuovo

- [ ] Date: scadenza delle candidature e Business Game (IT + EN)
- [ ] Link del Google Form in entrambi i pulsanti
- [ ] Testo "aziende con cui abbiamo collaborato" e immagine `aziende.png`
- [ ] Unit/Team: testo breve e immagini `unit-ita.png` / `unit-en.png`
- [ ] `python3 build.py`, commit, tag, `python3 build.py --ref <tag>`
- [ ] Email di prova
