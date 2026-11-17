const corpoTabella = document.getElementById("tabellauni");
const corsiTrovati = document.getElementById("corsitrovati");
const searchInput = document.getElementById("searchNelleClassi");

// Barra di ricerca

let offerteAttuali = [];
let tutteLeOfferte = [];
let mappaUniversitaAttuale = {};

if (searchInput) {
    searchInput.addEventListener("input", function () {
        const paroleCercate = this.value.toLowerCase().trim().split(/\s+/).filter(Boolean);

        const offerteFiltrate = offerteAttuali.filter(offerta => {
            const uniData = mappaUniversitaAttuale[offerta.universita] || {};

            const contenuto = [
                offerta.nomeCorso,
                offerta.sede,
                offerta.regione,
                uniData.nome,
                uniData.regione,
                uniData.citta
            ].join(" ").toLowerCase().replace(/\s+/g, " ");

            return paroleCercate.every(parola => contenuto.includes(parola));
        });

        renderizzaTabella(offerteFiltrate, mappaUniversitaAttuale);
    });
}

// Creazione tabella

function renderizzaTabella(offerte, mappaUniversita) {
    corpoTabella.innerHTML = "";
    let n = 0;
    for (let offerta of offerte) {
        const uniData = mappaUniversita[offerta.universita] || {};
        const slug = offerta.universita.toLowerCase().replace(/ /g, "_");
        const link = `/atenei/${slug}`;
        const regione = offerta.regione ? offerta.regione : uniData.regione || "----";
        const nomeUni = uniData.nome || offerta.universita;

        corpoTabella.innerHTML += `
        <tr class="riga-principale">
            <td><a class="uni" href="${link}">${nomeUni}</a></td>
            <td colspan="4"><strong>${offerta.nomeCorso}</strong></td>
        </tr>
        <tr class="riga-dettagli">
            <td colspan="5" class="dettaglio">📍 ${offerta.sede} — ${regione}</td>
        </tr>`;
        n++;
    }
    corsiTrovati.textContent = `${n} corsi trovati`;
}

function caricaTabella() {
    fetch(`/data/universita.json`).then(r => r.json())
        .then(universita => {
            const mappaUniversita = {};
            for (let uni of universita) {
                mappaUniversita[uni.sigla] = uni;
            }
            mappaUniversitaAttuale = mappaUniversita;

            // Legge le righe già presenti nell'HTML statico
            // e ricostruisce offerteAttuali dal DOM
            const righe = corpoTabella.querySelectorAll("tr.riga-principale");
            offerteAttuali = Array.from(righe).map(riga => {
                return JSON.parse(riga.dataset.offerta);
            });

            tutteLeOfferte = [...offerteAttuali];

            corsiTrovati.textContent = `${offerteAttuali.length} corsi trovati`;
        });
}

// ORDINE PER NOME DEL CORSO

var ordinecorso

function ordinaPerCorso() {
    const copia = [...offerteAttuali];
    if (ordinecorso) {
        renderizzaTabella(copia.reverse(), mappaUniversitaAttuale);
        ordinecorso = false;
    } else {
        renderizzaTabella(copia, mappaUniversitaAttuale);
        ordinecorso = true;
    }
    ordinecitta = false;
    ordineregione = false;
}

// ORDINE PER REGIONE

var ordineregione;

function ordinaPerRegione() {
    const copia = [...offerteAttuali].sort((a, b) => {
        const regioneA = a.regione || mappaUniversitaAttuale[a.universita]?.regione || "";
        const regioneB = b.regione || mappaUniversitaAttuale[b.universita]?.regione || "";
        return regioneA.localeCompare(regioneB, "it");
    });
    if (ordineregione) {
        renderizzaTabella(copia.reverse(), mappaUniversitaAttuale);
        ordineregione = false;
    } else {
        renderizzaTabella(copia, mappaUniversitaAttuale);
        ordineregione = true;
    }
    ordinecorso = false;
    ordinecitta = false;
}

// ORDINE PER CITTÀ

var ordinecitta;

function ordinaPerSede() {
    const copia = [...offerteAttuali].sort((a, b) => {
        const cittaA = a.sede || mappaUniversitaAttuale[a.universita]?.citta || "";
        const cittaB = b.sede || mappaUniversitaAttuale[b.universita]?.citta || "";
        const cmpCitta = cittaA.localeCompare(cittaB, "it");
        if (cmpCitta !== 0) return cmpCitta;
        const nomeA = mappaUniversitaAttuale[a.universita]?.nome || "";
        const nomeB = mappaUniversitaAttuale[b.universita]?.nome || "";
        return nomeA.localeCompare(nomeB, "it");
    });
    if (ordinecitta) {
        renderizzaTabella(copia.reverse(), mappaUniversitaAttuale);
        ordinecitta = false;
    } else {
        renderizzaTabella(copia, mappaUniversitaAttuale);
        ordinecitta = true;
    }
    ordinecorso = false;
    ordineregione = false;
}