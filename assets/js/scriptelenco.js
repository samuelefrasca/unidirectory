const corpoTabella = document.getElementById("tabellauni");
const uniTrovate = document.getElementById("unitrovate");
const searchInput = document.getElementById("searchNegliAtenei");

// Rileva se la colonna studenti è presente nell'header della tabella
const haStudenti = document.querySelector("thead .studenti, thead th:last-child a[onclick*='ordinaPerStudenti']") !== null
    || document.querySelectorAll("thead th").length > 5;

// Barra di ricerca

let uniAttuale = [];

if (searchInput) {
    searchInput.addEventListener("input", function () {
        const paroleCercate = this.value.toLowerCase().trim().split(/\s+/).filter(Boolean);

        const filtrate = uniAttuale.filter(uni => {
            const contenuto = [
                uni.nome,
                uni.sigla,
                uni.citta,
                uni.regione
            ].join(" ").toLowerCase();

            return paroleCercate.every(parola => contenuto.includes(parola));
        });

        renderizzaTabella(filtrate);
    });
}

// Creazione tabella

function renderizzaTabella(lista) {
    corpoTabella.innerHTML = "";
    let n = 1;
    for (let uni of lista) {
        if (!uni.studenti) { uni.studenti = "----" }
        if (!uni.sigla) { uni.sigla = "----" }
            let slug = uni.sigla.toLowerCase().replace(/ /g, "_");
            let link = `/atenei/${slug}`;
        let studenti_display = typeof uni.studenti === "number"
            ? uni.studenti.toLocaleString("it-IT", { useGrouping: "always" })
            : uni.studenti;
        let colStudenti = haStudenti
            ? `<td class="studenti">${studenti_display}</td>`
            : "";
        let riga = `<tr data-uni="${JSON.stringify(uni).replace(/"/g, '&quot;"')}">
                <td class="num">${n}</td>
                <td><a class="uni" href="${link}">${uni.nome}</a></td>
                <td>${uni.sigla}</td>
                <td>${uni.citta}</td>
                <td>${uni.regione}</td>
                ${colStudenti}
                </tr>`;
        corpoTabella.innerHTML += riga;
        n++;
    }
    uniTrovate.textContent = `${n - 1} atenei trovati`;
}

// Carica dal DOM statico (pre-generato da Python)

function caricaTabella() {
    const righe = corpoTabella.querySelectorAll("tr[data-uni]");
    uniAttuale = Array.from(righe).map(riga => JSON.parse(riga.dataset.uni));
    uniTrovate.textContent = `${uniAttuale.length} atenei trovati`;
    ordineregione = true;
}

// ORDINE PER REGIONE

var ordineregione

function ordinaPerRegione() {
    const copia = [...uniAttuale];
    copia.sort((a, b) => a.regione.localeCompare(b.regione, "it"));
    if (ordineregione) {
        renderizzaTabella(copia.reverse());
        ordineregione = false;
    } else {
        renderizzaTabella(copia);
        ordineregione = true;
    }
    ordinecitta = false;
    ordinestudenti = false;
}

// ORDINE PER CITTÀ

var ordinecitta

function ordinaPerCitta() {
    const copia = [...uniAttuale];
    copia.sort((a, b) => a.citta.localeCompare(b.citta, "it"));
    if (ordinecitta) {
        renderizzaTabella(copia.reverse());
        ordinecitta = false;
    } else {
        renderizzaTabella(copia);
        ordinecitta = true;
    }
    ordinestudenti = false;
    ordineregione = false;
}

// ORDINE PER STUDENTI

var ordinestudenti

function ordinaPerStudenti() {
    const copia = [...uniAttuale];
    const numStudenti = (u) => (typeof u.studenti === "number" ? u.studenti : 0);
    if (ordinestudenti) {
        copia.sort((a, b) => numStudenti(a) - numStudenti(b));
        renderizzaTabella(copia);
        ordinestudenti = false;
    } else {
        copia.sort((a, b) => numStudenti(b) - numStudenti(a));
        renderizzaTabella(copia);
        ordinestudenti = true;
    }
    ordinecitta = false;
    ordineregione = false;
}
