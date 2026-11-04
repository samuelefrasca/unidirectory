# Unidirectory

Sito per orientarsi tra le università italiane e i loro corsi: istituti, classi di laurea e diplomi AFAM, con i dati ufficiali del MUR.

Sito: https://unidirectory.it

## Cosa contiene

Il sito ha tre sezioni collegate tra loro.

**Atenei.** 290 istituti divisi per categoria: università statali, non statali e telematiche, scuole superiori, conservatori, accademie di belle arti, ISIA, SSML e altri enti AFAM. Ogni istituto ha una pagina con studenti, sedi, corsi attivi e un grafico dei corsi per area disciplinare.

**Corsi per classe.** Triennali, magistrali e magistrali a ciclo unico. Si sceglie una classe (ad esempio L-31) e si vedono i corsi di quella classe in tutti gli atenei, con modalità didattica, lingua, tipo di accesso e sede del corso, che non sempre coincide con quella dell'ateneo.

**AFAM.** Diplomi accademici di primo e secondo livello. Si sceglie l'area (musicale o artistica), poi la categoria (ad esempio canto e teatro musicale), poi il livello (ad esempio DCPL06 e DCSL06). Le pagine dei diplomi hanno la stessa struttura delle classi di laurea, ma senza lingua, didattica e accesso, che nei dati AFAM non ci sono.

Gli elenchi hanno ricerca e ordinamento; le pagine delle classi hanno anche un filtro per modalità didattica.

## Come funziona

È un sito statico: niente backend, niente framework. Le pagine sono generate da script Python a partire da file JSON e committate nel repository. Tabelle e liste sono già nell'HTML, quindi i motori di ricerca le indicizzano; JavaScript aggiunge solo ricerca, filtri e ordinamento. Il grafico delle pagine ateneo è HTML e CSS prodotto dallo script.

```
CSV (MUR, USTAT)  →  scripts/genera_*  →  data/*.json  →  scripts/crea*  →  pagine HTML
```

## Struttura del repository

```
.
├── index.html, uni.html, triennali.html,
│   magistrali.html, magistralicu.html, afam.html 
│   about.html, privacy.html, 404.html
│   sitemap.xml, robots.txt
├── data/        JSON da cui nascono tutte le pagine
├── scripts/     script Python (CSV → JSON, JSON → HTML)
├── uni/         elenchi degli istituti per categoria (generati)
├── atenei/      una pagina per istituto (generate)
├── classi/      una pagina per classe di laurea (generate)
├── afam/        una cartella per area, con una pagina per diploma (generate)
└── assets/
    ├── css/
    ├── js/
    ├── fonts/   Inter
    └── img/
```

**`data/`**
- `universita.json`: anagrafica degli istituti (nome, sigla, città, regione, link, categoria, studenti). La sigla collega i corsi agli istituti.
- `corsi_per_classe.json`: corsi universitari raggruppati per classe.
- `corsi_afam_per_area.json`: corsi AFAM raggruppati per codice di diploma.

**`scripts/`**
- `genera_corsi.py`: CSV MUR dei corsi di laurea → `corsi_per_classe.json`
- `genera_corsi_afam.py`: CSV USTAT dell'AFAM → `corsi_afam_per_area.json`
- `creaElenchiUniHtml.py`: genera `uni/`
- `creaAteneiHtml.py`: genera `atenei/`
- `creaClassiHtml.py`: genera `classi/` (l'elenco delle classi è scritto dentro lo script)
- `creaClassiAfamHtml.py`: genera `afam/<area>/`

**`assets/js/`**
- `scriptindex.js`: ricerca tra le classi nella home
- `scriptelenco.js`: ricerca e ordinamento negli elenchi degli istituti
- `scriptatenei.js`: pagina ateneo, ricerca nei corsi ed espansione dell'elenco
- `scriptclassi.js`: pagine delle classi, ricerca, filtro e ordinamento
- `scriptafam.js`: lo stesso per le pagine AFAM

## Aggiornare i dati

Servono Python 3 e pandas (solo per gli script `genera_*`). Gli script vanno lanciati dalla radice del repository, perché usano percorsi relativi.

1. **Corsi universitari.** Scarica dagli open data del MUR il CSV dell'offerta formativa dei corsi di laurea e lancia `python scripts/genera_corsi.py`. I percorsi del CSV e dell'output sono costanti in cima allo script. Gli atenei che lo script non riconosce vengono scartati e scritti in `skippati.json`: per includerli, aggiungi la corrispondenza nome MUR → sigla in `MAPPING_ATENEO`.
2. **Corsi AFAM.** Copia in `data/` il CSV USTAT con nome `offerta_formativa_afam_mur.csv` e lancia `python scripts/genera_corsi_afam.py`. Le righe scartate finiscono in `data/skippati_afam.json`.
3. **Istituti.** `data/universita.json` non è generato da nessuno script: nuovi istituti, link e numero di studenti si modificano a mano.
4. **Pagine.** Rigenera l'HTML:

```
python scripts/creaElenchiUniHtml.py
python scripts/creaAteneiHtml.py
python scripts/creaClassiHtml.py
python scripts/creaClassiAfamHtml.py
```

## Fonti e limiti dei dati

- Corsi: open data del MUR. Studenti: USTAT.
- L'anno di riferimento degli studenti è indicato in ogni elenco. Per le scuole superiori universitarie il conteggio riguarda solo i dottorati, l'unico dato disponibile in USTAT.
- I dati sono elaborati automaticamente: eventuali errori possono dipendere dalla fonte.

## Segnalazioni

Per errori nei dati o istituti e corsi mancanti apri una issue, oppure scrivi a info@unidirectory.it.

## Licenza

Tutti i diritti riservati. Il codice è visibile ma non open source: senza permesso scritto non si può copiare, modificare o distribuire. Vedi `LICENSE`. I dati MUR e USTAT restano soggetti ai loro termini.