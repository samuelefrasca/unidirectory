#!/usr/bin/env python3
"""
Genera un file HTML per ogni ateneo presente in universita.json.
I file vengono salvati nella cartella atenei/{sigla-lowercase-con-underscore}.html

Utilizza:
  - data/universita.json           → dati anagrafici ateneo
  - data/corsi_per_classe.json     → corsi universitari
  - data/corsi_afam_per_area.json  → corsi AFAM
"""

import json
import re
import html as html_mod
from pathlib import Path
from collections import defaultdict, OrderedDict

# ── Percorsi ──────────────────────────────────────────────────────────────────
DATA_DIR = Path("data")
UNIV_JSON = DATA_DIR / "universita.json"
CORSI_JSON = DATA_DIR / "corsi_per_classe.json"
AFAM_JSON = DATA_DIR / "corsi_afam_per_area.json"
OUTPUT_DIR = Path("atenei")

# ── Caricamento dati ──────────────────────────────────────────────────────────
with open(UNIV_JSON, encoding="utf-8") as f:
    universita_list = json.load(f)

with open(CORSI_JSON, encoding="utf-8") as f:
    corsi_per_classe = json.load(f)

with open(AFAM_JSON, encoding="utf-8") as f:
    corsi_afam = json.load(f)

# ── Costanti ──────────────────────────────────────────────────────────────────

CATEGORIE_UNIVERSITA = {"statali", "nonstatali", "telematiche", "superiori"}
CATEGORIE_AFAM = {"abastatali", "accnazionali", "afamprivati",
                  "conservatori", "isia", "ssml"}

CATEGORIA_LABEL = {
    "statali":      "Università statale",
    "nonstatali":   "Università non statale",
    "telematiche":  "Università telematica",
    "superiori":    "Scuola superiore universitaria",
    "abastatali":   "Accademia di belle arti statale",
    "accnazionali": "Accademia nazionale",
    "afamprivati":  "Istituzione AFAM privata",
    "conservatori": "Conservatorio",
    "isia":         "ISIA",
    "ssml":         "SSML",
}

CICLO_UNICO = {
    "LM-41", "LM-42", "LM-46", "LM-4cu", "LM-13",
    "LM-85 bis", "LMG/01", "LMR/02",
}


# ── Funzioni helper ───────────────────────────────────────────────────────────

def codice_to_slug(codice: str) -> str:
    """Converte un codice classe nel suo slug per il nome file HTML."""
    slug = codice.rstrip(".")
    slug = slug.replace("/", "-")
    slug = slug.replace(".", "-")
    slug = slug.replace(" ", "")
    return slug.lower()


def slugify(text: str) -> str:
    """Converte testo generico in slug URL-friendly."""
    slug = text.lower().strip()
    slug = slug.replace("\u2019", "-").replace("'", "-")
    slug = re.sub(r"[^a-z0-9\-]", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")


def ateneo_to_slug(sigla: str) -> str:
    """Converte la sigla dell'ateneo nel nome del file HTML."""
    return sigla.lower().replace(" ", "_")


def format_number(n) -> str:
    """Formatta un numero con il punto come separatore migliaia."""
    if not n or n == 0:
        return "N/D"
    return f"{n:,}".replace(",", ".")


def esc(text) -> str:
    """Escape HTML entities."""
    return html_mod.escape(str(text))


def classify_codice(codice: str) -> str:
    """Classifica un codice classe: triennale | magistrale | ciclo_unico."""
    if codice in CICLO_UNICO:
        return "ciclo_unico"
    if codice.upper().startswith("LM"):
        return "magistrale"
    return "triennale"


def classify_afam(nome: str) -> str:
    """Classifica un corso AFAM: primo_livello | secondo_livello."""
    if "II livello" in nome:
        return "secondo_livello"
    return "primo_livello"


# ── Indice corsi per ateneo ───────────────────────────────────────────────────

def build_corsi_index() -> dict:
    """Costruisce un dizionario sigla → lista di corsi offerti."""
    index: dict[str, list] = defaultdict(list)

    # Corsi universitari
    for codice, classe in corsi_per_classe.items():
        area = classe.get("area", "")
        nome_classe = classe.get("nome", "")
        for offerta in classe.get("offerte", []):
            gruppo = classe.get("gruppo", "")
            didattica = offerta.get("didattica", "")
            lingua = offerta.get("lingua", "")
            sigla = offerta.get("universita", "")
            if sigla:
                index[sigla].append({
                    "tipo":            "universita",
                    "codice":          codice,
                    "nomeClasse":      nome_classe,
                    "nomeCorso":       offerta.get("nomeCorso", ""),
                    "sede":            offerta.get("sede", ""),
                    "area":            area,
                    "classificazione": classify_codice(codice),
                    "gruppo":          gruppo,
                    "didattica":       didattica,
                    "lingua":          lingua,
                    "accessoLibero":   offerta.get("accessoLibero"),
                    "link":            f"../classi/{codice_to_slug(codice)}.html",
                })

    # Corsi AFAM
    for codice, classe in corsi_afam.items():
        area = classe.get("area", "")
        nome_classe = classe.get("nome", "")
        livello = classify_afam(nome_classe)
        area_slug = slugify(area)
        for offerta in classe.get("offerte", []):
            sigla = offerta.get("universita", "")
            if sigla:
                index[sigla].append({
                    "tipo":            "afam",
                    "codice":          codice,
                    "nomeClasse":      nome_classe,
                    "nomeCorso":       offerta.get("nomeCorso", ""),
                    "sede":            offerta.get("sede", ""),
                    "area":            area,
                    "gruppo":          "",
                    "didattica":       offerta.get("didattica", ""),
                    "lingua":          offerta.get("lingua", ""),
                    "accessoLibero":   offerta.get("accessoLibero"),
                    "classificazione": livello,
                    "link":            f"../afam/{area_slug}/{codice_to_slug(codice)}.html",
                })

    return dict(index)


corsi_index = build_corsi_index()


# ── Generazione sezioni HTML ──────────────────────────────────────────────────

def genera_corsi_html(corsi: list, categoria: str) -> tuple[str, int]:
    """Genera l'HTML della sezione corsi e restituisce (html, totale)."""
    is_afam = categoria in CATEGORIE_AFAM

    if is_afam:
        groups = OrderedDict([
            ("primo_livello",  {"label": "Corsi di I livello",  "corsi": []}),
            ("secondo_livello", {"label": "Corsi di II livello", "corsi": []}),
        ])
    else:
        groups = OrderedDict([
            ("triennale",   {"label": "Lauree triennali",                   "corsi": []}),
            ("ciclo_unico", {"label": "Lauree magistrali a ciclo unico",    "corsi": []}),
            ("magistrale",  {"label": "Lauree magistrali",                  "corsi": []}),
        ])

    for corso in corsi:
        cls = corso["classificazione"]
        if cls in groups:
            groups[cls]["corsi"].append(corso)

    # Ordina alfabeticamente per nomeCorso
    for g in groups.values():
        g["corsi"].sort(key=lambda c: c["nomeCorso"].lower())

    parts = []
    total = sum(len(g["corsi"]) for g in groups.values())

    for group in groups.values():
        if not group["corsi"]:
            continue

        count = len(group["corsi"])
        parts.append(f"""
                <div class="categoria-corsi">

                    <h3>
                        {esc(group['label'])}
                        <span>{count}</span>
                    </h3>

                    <div class="lista-corsi">
""")

        for corso in group["corsi"]:
            dettagli = [f"📖 {esc(corso['codice'])}"]
            if corso.get("sede"):
                dettagli.append(f"📍 {esc(corso['sede'])}")
            if corso.get("lingua"):
                dettagli.append(f"🌐 {esc(corso['lingua'])}")
            if corso.get("didattica"):
                dettagli.append(f"🎓 {esc(corso['didattica'])}")
            if corso.get("accessoLibero") is not None:
                accesso = "✅ Accesso Libero" if corso["accessoLibero"] else "🔒 Accesso Programmato"
                dettagli.append(accesso)
            if corso.get("area"):
                dettagli.append(f"🧭 {esc(corso['area'])}")
            if corso.get("gruppo"):
                dettagli.append(f"🗂️ {esc(corso['gruppo'])}")
            dettagli_html = " · ".join(dettagli)
            parts.append(f"""
                        <a href="{esc(corso['link'])}" class="corso">

                            <div>
                                <strong>{esc(corso['nomeCorso'])}</strong>
                                <span>{dettagli_html}</span>
                            </div>

                            <i class="fa-solid fa-chevron-right"></i>

                        </a>
""")

        parts.append("""
                    </div>

                </div>
""")

    return "".join(parts), total


def genera_barre_html(corsi: list) -> str:
    """Genera l'HTML del grafico a barre per area."""
    area_counts: dict[str, int] = defaultdict(int)
    for corso in corsi:
        area = corso.get("area", "")
        if area:
            area_counts[area] += 1

    if not area_counts:
        return ""

    sorted_areas = sorted(area_counts.items(), key=lambda x: -x[1])
    max_count = sorted_areas[0][1]

    barre = []
    for area, count in sorted_areas:
        pct = max(round((count / max_count) * 100), 8)
        barre.append(f"""
                    <div class="barra">

                        <div class="barra-label">
                            {esc(area)}
                        </div>

                        <div class="barra-container">
                            <div class="barra-valore" style="width: {pct}%;">
                                {count}
                            </div>
                        </div>

                    </div>
""")

    return "".join(barre)


def genera_sedi_html(corsi: list) -> str:
    """Genera l'HTML della sezione sedi."""
    sede_counts: dict[str, int] = defaultdict(int)
    for corso in corsi:
        sede = corso.get("sede", "")
        if sede:
            sede_counts[sede] += 1

    if not sede_counts:
        return ""

    sorted_sedi = sorted(sede_counts.items(), key=lambda x: (-x[1], x[0]))
    parts = []
    for sede, count in sorted_sedi:
        label = "corso" if count == 1 else "corsi"
        parts.append(f"""
                    <div class="sede">

                        <div>
                            <strong>{esc(sede)}</strong>
                        </div>

                        <span>{count} {label}</span>

                    </div>
""")

    return "".join(parts)


# ── Template HTML completo ────────────────────────────────────────────────────

def genera_html_ateneo(uni: dict, corsi: list) -> str:
    """Genera la pagina HTML completa per un ateneo."""

    sigla     = uni["sigla"]
    nome      = uni["nome"]
    citta     = uni.get("citta", "")
    regione   = uni.get("regione", "")
    link      = uni.get("link", "#")
    studenti  = uni.get("studenti", 0)
    categoria = uni.get("categoria", "")
    slug      = ateneo_to_slug(sigla)

    cat_label   = CATEGORIA_LABEL.get(categoria, categoria)
    n_corsi     = len(corsi)
    sedi_uniche = len({c["sede"] for c in corsi if c.get("sede")})

    # Genera sotto-sezioni
    corsi_section, _   = genera_corsi_html(corsi, categoria)
    barre_section       = genera_barre_html(corsi)
    sedi_section        = genera_sedi_html(corsi)

    # Formattazione
    studenti_str = format_number(studenti)
    corsi_str    = str(n_corsi) if n_corsi else "N/D"
    sedi_str     = str(sedi_uniche) if sedi_uniche else "N/D"
    sedi_label   = "sede" if sedi_uniche == 1 else "sedi"

    # SEO
    base_url  = f"https://unidirectory.it/atenei/{slug}"
    title_seo = f"{nome} | Unidirectory"
    desc_seo  = (f"{nome}: studenti, corsi di laurea, sedi e "
                 f"informazioni sull'ateneo.")

    corsi_header = "Corsi" if categoria in CATEGORIE_AFAM else "Corsi di laurea"
    corsi_label  = "corso" if n_corsi == 1 else "corsi"

    # ── Sezione CORSI ─────────────────────────────────────────────────────
    corsi_section_html = ""
    if n_corsi > 0:
        corsi_section_html = f"""

            <!-- CORSI -->
            <section class="sezione sezione-corsi">

                <div class="sezione-header">

                    <h2>
                        <i class="fa-solid fa-graduation-cap"></i>
                        {corsi_header}
                    </h2>

                    <span class="numero-corsi">
                        {n_corsi} {corsi_label}
                    </span>

                </div>


                <!-- RICERCA -->
                <div class="ricerca-corsi">

                    <input
                        type="search"
                        id="cercaCorso"
                        placeholder="Cerca un corso...">

                </div>

{corsi_section}

                <a href="#" class="mostra-tutti">
                    Vedi tutti i corsi →
                </a>

            </section>
"""
    else:
        if link and link != "#":
            sito_ufficiale = (
                f'<a class="link-ateneovuoto" href="{esc(link)}" target="_blank" '
                f'rel="noopener noreferrer">sito ufficiale dell\'ateneo</a>'
            )
        else:
            sito_ufficiale = "sito ufficiale dell'ateneo"

        corsi_section_html = f"""

            <!-- INFORMAZIONI CORSI -->
            <section class="sezione">

                <div class="sezione-header">

                    <h2>
                        <i class="fa-solid fa-circle-info"></i>
                        Informazioni sui corsi
                    </h2>

                </div>

                <p>
                    Per maggiori informazioni sui corsi, visita il {sito_ufficiale}.
                </p>

            </section>
"""

    # ── Sezione DISTRIBUZIONE ─────────────────────────────────────────────
    distribuzione_html = ""
    if barre_section:
        distribuzione_html = f"""

            <!-- DISTRIBUZIONE -->
            <section class="sezione">

                <div class="sezione-header">

                    <h2>
                        <i class="fa-solid fa-chart-column"></i>
                        Corsi per area
                    </h2>

                </div>

                <div class="grafico">
{barre_section}
                </div>

            </section>
"""

    # ── Sezione SEDI ──────────────────────────────────────────────────────
    sedi_html = ""
    if sedi_section:
        sedi_html = f"""

            <!-- SEDI -->
            <section class="sezione">

                <div class="sezione-header">

                    <h2>
                        <i class="fa-solid fa-location-dot"></i>
                        Sedi
                    </h2>

                </div>

                <div class="sedi">
{sedi_section}
                </div>

            </section>
"""

    # ── Pagina completa ───────────────────────────────────────────────────
    return f"""<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{esc(title_seo)}</title>
    <meta name="description"
        content="{esc(desc_seo)}">
    <meta name="robots" content="index,follow">

    <link rel="canonical" href="{base_url}">
    <script>
        if (window.location.hostname === 'samuelefrasca.github.io' || window.location.hostname === 'unidirectory.pages.dev') {{
            const path = window.location.pathname
                .replace('/unidirectory', '')
                .replace(/\\.html$/, '');
            window.location.replace('https://unidirectory.it' + path + window.location.search);
        }}
    </script>

    <meta property="og:site_name" content="Unidirectory">
    <meta property="og:title" content="{esc(title_seo)}">
    <meta property="og:description"
        content="{esc(desc_seo)}">
    <meta property="og:type" content="website">
    <meta property="og:url" content="{base_url}">
    <meta property="og:image"
        content="https://unidirectory.it/assets/img/iud_icon.png">

    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="{esc(title_seo)}">
    <meta name="twitter:description"
        content="{esc(desc_seo)}">
    <meta name="twitter:image"
        content="https://unidirectory.it/assets/img/iud_icon.png">

    <link rel="icon" type="image/png" href="../assets/img/iud_icon.png">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="stylesheet" href="../assets/css/atenei.css">
    <link rel="stylesheet"
        href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "CollegeOrUniversity",
        "name": "{esc(nome)}",
        "url": "{base_url}",
        "description": "{esc(desc_seo)}"
    }}
    </script>
</head>


<body>

    <!-- HEADER -->
    <header>
        <div class="container">

            <div class="header">

                <div class="header1">
                    <a href="/">
                        <img class="logo"
                            src="../assets/img/iud_image.png"
                            alt="Logo Unidirectory">
                    </a>
                </div>

                <div class="header2">
                    <h1 class="title">unidirectory</h1>
                    <h2 class="subtitle">{esc(nome)}</h2>
                </div>

                <div class="header3"></div>

            </div>

        </div>
    </header>


    <main>

        <div class="container">


            <!-- INTRODUZIONE ATENEO -->
            <section class="ateneo-intro">

                <div class="ateneo-titolo">

                    <h1>{esc(nome)}</h1>

                    <p class="ateneo-localita">
                        <i class="fa-solid fa-location-dot"></i>
                        {esc(citta)} &mdash; {esc(regione)}
                    </p>

                </div>


                <a class="sito-ateneo"
                    href="{esc(link)}"
                    target="_blank"
                    rel="noopener noreferrer">

                    <i class="fa-solid fa-arrow-up-right-from-square"></i>
                    Sito ufficiale

                </a>

            </section>



            <!-- STATISTICHE -->
            <section class="statistiche">

                <div class="stat-card">

                    <div class="stat-icon">
                        <i class="fa-solid fa-user-graduate"></i>
                    </div>

                    <div>
                        <strong>{studenti_str}</strong>
                        <span>studenti</span>
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon">
                        <i class="fa-solid fa-book"></i>
                    </div>

                    <div>
                        <strong>{corsi_str}</strong>
                        <span>{corsi_label}</span>
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon">
                        <i class="fa-solid fa-location-dot"></i>
                    </div>

                    <div>
                        <strong>{sedi_str}</strong>
                        <span>{sedi_label}</span>
                    </div>

                </div>


                <div class="stat-card">

                    <div class="stat-icon">
                        <i class="fa-solid fa-landmark"></i>
                    </div>

                    <div>
                        <strong>{esc(cat_label)}</strong>
                        <span>tipologia</span>
                    </div>

                </div>

            </section>

{corsi_section_html}
{distribuzione_html}
{sedi_html}

            <!-- INFORMAZIONI -->
            <section class="sezione">

                <div class="sezione-header">

                    <h2>
                        <i class="fa-solid fa-circle-info"></i>
                        Informazioni
                    </h2>

                </div>


                <div class="informazioni">

                    <div class="info-riga">
                        <span>Nome</span>
                        <strong>{esc(nome)}</strong>
                    </div>

                    <div class="info-riga">
                        <span>Sigla</span>
                        <strong>{esc(sigla)}</strong>
                    </div>

                    <div class="info-riga">
                        <span>Città</span>
                        <strong>{esc(citta)}</strong>
                    </div>

                    <div class="info-riga">
                        <span>Regione</span>
                        <strong>{esc(regione)}</strong>
                    </div>

                    <div class="info-riga">
                        <span>Categoria</span>
                        <strong>{esc(cat_label)}</strong>
                    </div>

                </div>

            </section>



            <!-- NOTA -->
            <p class="data-note">

                Dati sugli atenei e sui corsi provenienti dalle fonti
                indicate da Unidirectory.

            </p>


        </div>

    </main>



    <!-- FOOTER -->
    <footer>

        <div class="subfooter">

            <p>
                &copy; 2026 Unidirectory &middot;
                <a class="a_footer"
                    href="https://samuelefrasca.github.io/"
                    target="_blank"
                    rel="noopener noreferrer">
                    Samuele Frasca
                </a>
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

            <p>
                Dati:
                <a class="a_footer"
                    href="https://www.mur.gov.it/">
                    MUR
                </a>
                &middot;
                <a class="a_footer"
                    href="https://ustat.mur.gov.it/">
                    USTAT
                </a>
            </p>

            <p>
                <a class="a_footer" href="../about.html">
                    About
                </a>
            </p>

            <p>
                <a class="a_footer" href="../privacy.html">
                    Privacy Policy
                </a>
            </p>

            <p>
                <a class="a_footer" href="../sitemap.xml">
                    Sitemap
                </a>
            </p>

            <p>
                <a class="a_footer" href="mailto:info@unidirectory.it">
                    Contattaci
                </a>
            </p>

        </div>

    </footer>


    <script src="../assets/js/scriptatenei.js"></script>

</body>

</html>"""


# ── Main ──────────────────────────────────────────────────────────────────────

OUTPUT_DIR.mkdir(exist_ok=True)

# Rileva duplicati di sigla (case-insensitive) e aggiungi suffisso categoria
slug_count: dict[str, int] = defaultdict(int)
for uni in universita_list:
    slug_count[ateneo_to_slug(uni["sigla"])] += 1

nomi_usati: dict[str, int] = {}

for uni in universita_list:
    sigla = uni["sigla"]
    slug = ateneo_to_slug(sigla)
    corsi = corsi_index.get(sigla, [])

    # In caso di duplicato, aggiungi la categoria come suffisso
    if slug_count[slug] > 1:
        slug = f"{slug}-{uni.get('categoria', 'x')}"

    html_content = genera_html_ateneo(uni, corsi)
    nome_file = f"{slug}.html"
    (OUTPUT_DIR / nome_file).write_text(html_content, encoding="utf-8")

# ── Statistiche ───────────────────────────────────────────────────────────────

print(f"\n-- RISULTATI --")
print(f"  Atenei generati:  {len(universita_list)}")

con_corsi = sum(1 for u in universita_list if corsi_index.get(u["sigla"]))
senza_corsi = len(universita_list) - con_corsi
print(f"  Con corsi:        {con_corsi}")
print(f"  Senza corsi:      {senza_corsi}")

if senza_corsi:
    nomi_senza = sorted(u["sigla"] for u in universita_list
                        if not corsi_index.get(u["sigla"]))
    print(f"\n  Atenei senza corsi ({senza_corsi}):")
    for n in nomi_senza:
        print(f"    - {n}")

print(f"\n  Output:           {OUTPUT_DIR}/")

# Anteprima
primo = universita_list[0]
n_corsi_primo = len(corsi_index.get(primo["sigla"], []))
print(f"\n-- Anteprima: {primo['sigla']} ({n_corsi_primo} corsi) --")
