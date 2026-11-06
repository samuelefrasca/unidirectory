import json
import re
from pathlib import Path

# ── Carica dati ───────────────────────────────────────────────────────────────
with open("data/corsi_afam_per_area.json", encoding="utf-8") as f:
    corsi_per_classe = json.load(f)

with open("data/universita.json", encoding="utf-8") as f:
    universita_list = json.load(f)

mappa_universita = {u["sigla"]: u for u in universita_list}

# ── Genera slug ───────────────────────────────────────────────────────────────
def genera_slug(codice):
    """Converte un codice AFAM in slug URL-friendly (es. 'DADPL02' -> 'dadpl02')."""
    return re.sub(r'[^a-z0-9]+', '-', codice.lower()).strip('-')

def genera_slug_area(area):
    """Converte un nome area in slug (es. 'Arti del teatro' -> 'arti-del-teatro')."""
    return re.sub(r'[^a-z0-9]+', '-', area.lower()).strip('-')

# ── Genera righe HTML statiche ────────────────────────────────────────────────
def genera_righe_html(codice):
    corso = corsi_per_classe.get(codice)
    if not corso:
        return ""

    righe = []
    for offerta in corso["offerte"]:
        uni = mappa_universita.get(offerta["universita"], {})
        sigla = offerta["universita"]
        slug = sigla.lower().replace(" ", "_")
        link = f"../../atenei/{slug}.html"
        nome_uni = uni.get("nome", offerta["universita"])
        regione = offerta.get("regione", uni.get("regione", "----"))

        # Serializza l'offerta come data attribute per il JS
        data_offerta = json.dumps(offerta, ensure_ascii=False).replace('"', '&quot;')

        righe.append(f"""
                    <tr class="riga-principale" data-offerta="{data_offerta}">
                        <td><a class="uni" href="{link}">{nome_uni}</a></td>
                        <td colspan="4"><strong>{offerta["nomeCorso"]}</strong></td>
                    </tr>
                    <tr class="riga-dettagli">
                        <td colspan="5" class="dettaglio">📍 {offerta["sede"]} — {regione}</td>
                    </tr>""")

    return "\n".join(righe)

# ── Template HTML ─────────────────────────────────────────────────────────────
template = """<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <title>Corsi AFAM in {{NOME}} ({{CODICE}}): istituti e sedi | Unidirectory</title>
    <meta name="description"
        content="Scopri in quali istituti AFAM e sedi è attivo il corso in {{NOME}} ({{CODICE}}) in Italia. Elenco chiaro e aggiornato delle sedi disponibili.">
    <meta name="robots" content="index,follow">


    <link rel="canonical" href="https://unidirectory.it/afam/{{AREA_SLUG}}/{{SLUG}}">
    <script>
        if (window.location.hostname === 'samuelefrasca.github.io' || window.location.hostname === 'unidirectory.pages.dev') {
            const path = window.location.pathname
                .replace('/unidirectory', '')
                .replace(/\\.html$/, '');
            window.location.replace('https://unidirectory.it' + path + window.location.search);
        }
    </script>

    <meta property="og:site_name" content="Unidirectory">
    <meta property="og:title" content="Corsi AFAM in {{NOME}} ({{CODICE}}): istituti e sedi | Unidirectory">
    <meta property="og:description"
        content="Scopri in quali istituti AFAM e sedi è attivo il corso in {{NOME}} ({{CODICE}}) in Italia.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://unidirectory.it/afam/{{AREA_SLUG}}/{{SLUG}}">
    <meta property="og:image"
        content="https://unidirectory.it/assets/img/iud_icon.png">


    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Corsi AFAM in {{NOME}} ({{CODICE}}): istituti e sedi | Unidirectory">
    <meta name="twitter:description"
        content="Scopri in quali istituti AFAM e sedi è attivo il corso in {{NOME}} ({{CODICE}}) in Italia.">
    <meta name="twitter:image"
        content="https://unidirectory.it/assets/img/iud_icon.png">


    <link rel="icon" type="image/png" href="../../assets/img/iud_icon.png">
    <link rel="stylesheet" href="../../assets/css/style.css">
    <link rel="stylesheet" href="../../assets/css/classi.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Corsi AFAM in {{NOME}} ({{CODICE}}): istituti e sedi | Unidirectory",
        "url": "https://unidirectory.it/afam/{{AREA_SLUG}}/{{SLUG}}",
        "description": "Scopri in quali istituti AFAM e sedi è attivo il corso in {{NOME}} ({{CODICE}}) in Italia. Elenco chiaro e aggiornato delle sedi disponibili."
    }
    </script>
</head>


<body>
    <header>
        <div class="container">
            <div class="header">
                <div class="header1">
                    <a href="/">
                        <img class="logo" src="../../assets/img/iud_image.png" alt="Logo Unidirectory">
                    </a>
                </div>
                <div class="header2">
                    <h1 class="title">unidirectory</h1>
                    <h2 class="subtitle">{{CODICE}} - {{NOME}}</h2>
                </div>
                <div class="header3"></div>
            </div>
        </div>
    </header>
    <main>
        <div class="container table-responsive">
            <div class="toolbar-tabella">
                <div class="ordina">
                    <button type="button" onclick="ordinaPerCorso('{{CODICE}}')">Ordina per corso</button>
                    <button type="button" onclick="ordinaPerSede('{{CODICE}}')">Ordina per sede</button>
                    <button type="button" onclick="ordinaPerRegione('{{CODICE}}')">Ordina per regione</button>
                </div>
            </div>
            <input type="search" id="searchNelleClassi" placeholder="Cerca istituto, sede, regione o corso...">
            <h3 id ="corsitrovati"></h3>
            <table>
                <tbody id="tabellauni">{{RIGHE}}</tbody>
            </table>
            <p class="data-note">
                Dati corsi dal MUR (USTAT). Alcuni corsi di natura più sporadica potrebbero non essere presenti nei dati di riferimento.
            </p>
        </div>
    </main>
    <footer>
        <div class="subfooter">
            <p>&copy; 2026 Unidirectory ·
                <a class="a_footer" href="https://samuelefrasca.github.io/" target="_blank" rel="noopener noreferrer">Samuele Frasca</a>
            </p>
            <p>
                <a class="a_footer github" href="https://github.com/samuelefrasca/unidirectory" target="_blank"
                    rel="noopener noreferrer">
                    <i class="fa-brands fa-github"></i> GitHub
                </a>
            </p>
            <p>
                <a class="a_footer github" href="https://www.instagram.com/unidirectory/" target="_blank"
                    rel="noopener noreferrer">
                    <i class="fa-brands fa-instagram"></i> Instagram
                </a>
            </p>
            <p>
                <a class="a_footer" href="https://paypal.me/SamueleFrasca18" target="_blank" rel="noopener noreferrer">
                    <i class="fa-solid fa-mug-hot"></i> Sostieni il progetto
                </a>
            </p>
        </div>
        <div class="subfooter">
            <p>Dati:
                <a class="a_footer" href="https://www.mur.gov.it/it/aree-tematiche/universita/le-universita"
                    target="_blank" rel="noopener noreferrer">MUR</a>
                &middot;
                <a class="a_footer" href="https://ustat.mur.gov.it/" target="_blank" rel="noopener noreferrer">USTAT</a>
            </p>
            <p><a class="a_footer" href="../../about.html">About</a></p>
            <p><a class="a_footer" href="../../privacy.html">Privacy Policy</a></p>
            <p><a class="a_footer" href="../../sitemap.xml">Sitemap</a></p>
            <p><a class="a_footer" href="mailto:info@unidirectory.it">Contattaci</a></p>
        </div>
    </footer>
    <script src="../../assets/js/footer.js"></script>
    <script src="../../assets/js/scriptafam.js"></script>
    <script>
        caricaTabella("{{CODICE}}");
        ordinecorso = true;
        ordinecitta = false;
        ordineregione = false;
    </script>
</body>

</html>
"""

# ── Generazione file HTML ─────────────────────────────────────────────────────
cartella_base = Path("afam")
cartella_base.mkdir(exist_ok=True)

conteggio = 0
aree_create = set()
for codice, dati in corsi_per_classe.items():
    nome = dati["nome"]
    area = dati["area"]
    slug = genera_slug(codice)
    area_slug = genera_slug_area(area)

    # Crea sottocartella per area
    cartella_area = cartella_base / area_slug
    cartella_area.mkdir(exist_ok=True)
    aree_create.add(area_slug)

    contenuto = (
        template
        .replace("{{NOME}}", nome)
        .replace("{{CODICE}}", codice)
        .replace("{{SLUG}}", slug)
        .replace("{{AREA_SLUG}}", area_slug)
        .replace("{{RIGHE}}", genera_righe_html(codice))
    )

    nome_file = f"{slug}.html"
    (cartella_area / nome_file).write_text(contenuto, encoding="utf-8")
    conteggio += 1

print(f"Creati {conteggio} file HTML in {len(aree_create)} cartelle area dentro '{cartella_base}'.")
