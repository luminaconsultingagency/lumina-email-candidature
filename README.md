# Email candidature Lumina

Template HTML dell'email che Lumina Consulting Agency manda ogni anno agli studenti di H-FARM College per aprire le candidature.
È bilingue (prima italiano, poi inglese) e funziona su Gmail, Apple Mail e Outlook, anche in dark mode.

> Se sei un agente AI (Claude, Codex, Cursor...), leggi anche [AGENTS.md](AGENTS.md).

---

## Com'è fatto il repository

```
email.html                 ← IL FILE DA MODIFICARE (immagini con percorsi relativi, si apre in locale)
immagini/                  ← immagini usate dall'email (vengono servite online da jsDelivr)
dist/email-da-inviare.html ← versione pronta da inviare, generata da build.py (NON modificarla a mano)
build.py                   ← trasforma i percorsi "immagini/..." in link pubblici
sorgenti/                  ← file originali ad alta risoluzione da cui sono state ricavate le immagini
strumenti/                 ← script opzionale per inviare l'email da Google Apps Script
archivio/2025/             ← l'email dell'anno precedente (fatta con postcards.email) con le sue immagini
```

## Come preparare l'email di un nuovo anno

### 1. Apri il template
Apri `email.html` con un editor (VS Code va benissimo). Per vederlo, aprilo nel browser: le immagini
compaiono perché sono nella cartella `immagini/` accanto al file.

### 2. Cambia testi, date e link
Il codice è lungo perché le email si costruiscono con tabelle e stili "inline", ma il testo si trova
facilmente con **Cerca** (Cmd+F). Le cose da aggiornare ogni anno sono di solito queste:

| Cosa | Cerca nel file | Nota |
|---|---|---|
| Scadenza candidature | `ottobre alle 18:00` e `October` | Sia la parte IT che quella EN |
| Data Business Game | `Business Game` | Sia IT che EN |
| Link al Google Form | `forms.gle` | Ci sono **2** pulsanti (IT e EN) |
| Testo dei pulsanti | `pulsante-` | Sono **immagini** (vedi sotto): per cambiare il testo rigenera il PNG e aggiorna l'`alt` |
| Aziende con cui avete lavorato | `Allianz` | Il testo; i loghi sono nell'immagine `aziende.png` |
| Descrizione delle Unit | `3 Unit` | Breve: il dettaglio è già nell'immagine |

⚠️ **Attenzione alla punteggiatura.** Il testo è spezzato in tanti `<span>`. Se tra `</span>` e il
`<span>` successivo c'è un a capo e la parte dopo inizia con una virgola o un punto, nell'email
compare uno spazio prima della punteggiatura (tipo `14:00 , attività`). La punteggiatura va attaccata:
`...14:00</span><span style="...">, attività...`.

### 3. Sostituisci le immagini
Metti la nuova immagine in `immagini/` **con lo stesso nome** di quella vecchia (così non devi toccare l'HTML),
oppure con un nome nuovo aggiornando il `src` in `email.html`.

| File | Dove appare | Formato consigliato |
|---|---|---|
| `header.png` | In alto (logo su arancione) | 1200 px di larghezza o più, sfondo pieno |
| `aziende.png` | Loghi aziende (IT + EN) | ~1000 px, **sfondo bianco pieno** |
| `unit-ita.png` / `unit-en.png` | Le 3 Unit | 1920×840, **sfondo bianco pieno** |
| `pulsante-candidati.png` / `pulsante-apply.png` | Pulsanti "Candidati" / "Apply" | Testo bianco su blu `#1595e7`, 3× (es. 657×156) |
| `logo-badge.png` | Logo nel footer | Deve leggersi sia su sfondo bianco che nero |
| `linkedin-badge.png`, `instagram-badge.png` | Icone social | Nero su cerchio bianco |

Regole d'oro:
- **Esporta al doppio della dimensione a cui l'immagine appare** (l'email è larga 600 px → header a 1200 px), così è nitida sugli schermi retina.
- **Niente PNG trasparenti con testo o loghi scuri**: in dark mode lo sfondo diventa nero e il contenuto sparisce. Usa sfondo bianco pieno.
- Tieni le immagini leggere (sotto i 200 KB l'una).

### 4. Genera la versione da inviare
Le email non possono usare file sul tuo computer: le immagini devono avere un indirizzo pubblico.
Questo repository è pubblico e jsDelivr serve i file direttamente da GitHub, gratis.

1. Fai commit e push delle modifiche (anche delle immagini nuove).
2. Lancia:
   ```bash
   python3 build.py
   ```
3. Viene creato `dist/email-da-inviare.html`, con tutte le immagini puntate a
   `https://cdn.jsdelivr.net/gh/<owner>/<repo>@main/immagini/...`. Fai commit anche di questo file.

💡 **Blocca la versione dopo l'invio.** Crea un tag (es. `git tag v2026 && git push --tags`) e rigenera con
`python3 build.py --ref v2026` **prima** di inviare: così l'email mandata continuerà a mostrare le sue
immagini anche quando l'anno dopo qualcuno le sostituisce su `main`.

ℹ️ jsDelivr tiene in cache i file per qualche ora: se sostituisci un'immagine con lo stesso nome e
non vedi il cambiamento, usa un tag nuovo oppure aspetta.

### 5. Prova prima di inviare
Manda l'email **a te stesso** e controllala su:
- Gmail da iPhone con il **dark mode** attivo (è il caso più difficile);
- Gmail da computer;
- Apple Mail (iPhone o Mac), in chiaro e in scuro;
- Outlook, se possibile.

Controlla che i due pulsanti aprano il form giusto.

### 6. Invia
**Metodo semplice (Gmail):** apri `dist/email-da-inviare.html` in Chrome, premi Cmd+A e poi Cmd+C,
apri una nuova email in Gmail e incolla con Cmd+V. Oggetto consigliato: `LUMINA - Application Form`.

Se copiando la pagina dal browser il testo diventa bianco, il browser era in dark mode: incolla invece
il codice HTML, oppure metti il Mac in modalità chiara prima di copiare.

**Alternativa (Google Apps Script):** manda l'HTML così com'è, senza copia e incolla. Usa lo script in
[`strumenti/invia_con_apps_script.gs`](strumenti/invia_con_apps_script.gs).

---

## Come funziona il dark mode

Ogni client email gestisce il dark mode a modo suo, e **Gmail**, che è quello che usano quasi tutti gli
studenti (account `@student.h-farm.com`), **non permette di controllarlo**: quando incolli l'email elimina
il CSS, e sul telefono inverte da solo i colori di sfondi e testi, ma **non delle immagini**.
Per questo la regola è una sola:

> **Tutto quello che deve avere un colore preciso in entrambe le modalità deve essere un'immagine con lo sfondo incluso.**

- **Logo e icone social**: il logo nero su sfondo trasparente spariva in dark mode (2025). Ora hanno il loro
  sfondo incorporato nell'immagine, quindi si leggono sempre.
- **Pulsanti**: se fossero testo, Gmail in dark mode trasformerebbe la scritta bianca in grigio. Sono immagini PNG
  (testo bianco su blu), con un `alt` che fa da riserva se le immagini sono bloccate.
- **Immagini con testo scuro** (loghi aziende, Unit): hanno lo sfondo bianco pieno.

❌ Non provare a "scambiare" le immagini con `@media (prefers-color-scheme: dark)` e con copie nascoste:
Gmail elimina il CSS, e le immagini nascoste hanno fatto mostrare a Gmail mobile le icone social al posto
delle immagini delle Unit (successo nel 2026, poi corretto).

---

## Storia

- **2025:** email creata con [postcards.email](https://postcards.email/) (Designmodo) e inviata dal Google Group
  `lumina@lumina.h-farm.com`. Le immagini erano ospitate su `cloudfilesdm.com`. Copia in `archivio/2025/`.
- **2026:** template "fatto in casa" ricavato da quello del 2025, con nuove immagini delle Unit, dark mode
  sistemato, punteggiatura corretta e immagini ospitate su questo repository.
