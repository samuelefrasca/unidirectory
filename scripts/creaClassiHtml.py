import json
from pathlib import Path

classi = [
  {"nome":"Beni Culturali","codice":"L-1","slug":"l-1"},
  {"nome":"Biotecnologie","codice":"L-2","slug":"l-2"},
  {"nome":"Discipline delle Arti Figurative, della Musica, dello Spettacolo e della Moda","codice":"L-3","slug":"l-3"},
  {"nome":"Disegno Industriale","codice":"L-4","slug":"l-4"},
  {"nome":"Filosofia","codice":"L-5","slug":"l-5"},
  {"nome":"Geografia","codice":"L-6","slug":"l-6"},
  {"nome":"Ingegneria Civile e Ambientale","codice":"L-7","slug":"l-7"},
  {"nome":"Ingegneria dell'Informazione","codice":"L-8","slug":"l-8"},
  {"nome":"Ingegneria Industriale","codice":"L-9","slug":"l-9"},
  {"nome":"Lettere","codice":"L-10","slug":"l-10"},
  {"nome":"Lingue e Culture Moderne","codice":"L-11","slug":"l-11"},
  {"nome":"Mediazione Linguistica","codice":"L-12","slug":"l-12"},
  {"nome":"Scienze Biologiche","codice":"L-13","slug":"l-13"},
  {"nome":"Scienze dei Servizi Giuridici","codice":"L-14","slug":"l-14"},
  {"nome":"Scienze del Turismo","codice":"L-15","slug":"l-15"},
  {"nome":"Scienze dell'Amministrazione e dell'Organizzazione","codice":"L-16","slug":"l-16"},
  {"nome":"Scienze dell'Architettura","codice":"L-17","slug":"l-17"},
  {"nome":"Scienze dell'Economia e della Gestione Aziendale","codice":"L-18","slug":"l-18"},
  {"nome":"Scienze dell'Educazione e della Formazione","codice":"L-19","slug":"l-19"},
  {"nome":"Scienze della Comunicazione","codice":"L-20","slug":"l-20"},
  {"nome":"Scienze della Pianificazione Territoriale, Urbanistica, Paesaggistica e Ambientale","codice":"L-21","slug":"l-21"},
  {"nome":"Scienze delle Attività Motorie e Sportive","codice":"L-22","slug":"l-22"},
  {"nome":"Scienze e Tecniche dell'Edilizia","codice":"L-23","slug":"l-23"},
  {"nome":"Scienze e Tecniche Psicologiche","codice":"L-24","slug":"l-24"},
  {"nome":"Scienze e Tecnologie Agrarie e Forestali","codice":"L-25","slug":"l-25"},
  {"nome":"Scienze e Tecnologie Agro-Alimentari","codice":"L-26","slug":"l-26"},
  {"nome":"Scienze e Tecnologie Chimiche","codice":"L-27","slug":"l-27"},
  {"nome":"Scienze e Tecnologie della Navigazione","codice":"L-28","slug":"l-28"},
  {"nome":"Scienze e Tecnologie Farmaceutiche","codice":"L-29","slug":"l-29"},
  {"nome":"Scienze e Tecnologie Fisiche","codice":"L-30","slug":"l-30"},
  {"nome":"Scienze e Tecnologie Informatiche","codice":"L-31","slug":"l-31"},
  {"nome":"Scienze e Tecnologie per l'Ambiente e la Natura","codice":"L-32","slug":"l-32"},
  {"nome":"Scienze Economiche","codice":"L-33","slug":"l-33"},
  {"nome":"Scienze Geologiche","codice":"L-34","slug":"l-34"},
  {"nome":"Scienze Matematiche","codice":"L-35","slug":"l-35"},
  {"nome":"Scienze Politiche e delle Relazioni Internazionali","codice":"L-36","slug":"l-36"},
  {"nome":"Scienze Sociali per la Cooperazione, lo Sviluppo e la Pace","codice":"L-37","slug":"l-37"},
  {"nome":"Scienze Zootecniche e Tecnologie delle Produzioni Animali","codice":"L-38","slug":"l-38"},
  {"nome":"Servizio Sociale","codice":"L-39","slug":"l-39"},
  {"nome":"Sociologia","codice":"L-40","slug":"l-40"},
  {"nome":"Statistica","codice":"L-41","slug":"l-41"},
  {"nome":"Storia","codice":"L-42","slug":"l-42"},
  {"nome":"Diagnostica per la conservazione dei beni culturali","codice":"L-43","slug":"l-43"},
  {"nome":"Scienze dei materiali","codice":"L-Sc.Mat.","slug":"l-sc-mat"},
  {"nome":"Scienze, culture e politiche della gastronomia","codice":"L/GASTR","slug":"l-gastr"},
  {"nome":"Scienze della difesa e della sicurezza","codice":"L/DS","slug":"l-ds"},
  {"nome":"Professioni sanitarie, infermieristiche e professione sanitaria ostetrica","codice":"L/SNT1","slug":"l-snt1"},
  {"nome":"Professioni sanitarie della riabilitazione","codice":"L/SNT2","slug":"l-snt2"},
  {"nome":"Professioni sanitarie tecniche","codice":"L/SNT3","slug":"l-snt3"},
  {"nome":"Professioni sanitarie della prevenzione","codice":"L/SNT4","slug":"l-snt4"},
  {"nome":"Professioni tecniche per l'edilizia e il territorio","codice":"L-P01","slug":"l-p01"},
  {"nome":"Professioni tecniche agrarie, alimentari e forestali","codice":"L-P02","slug":"l-p02"},
  {"nome":"Professioni tecniche industriali e dell'informazione","codice":"L-P03","slug":"l-p03"},
  {"nome":"Antropologia culturale ed etnologia","codice":"LM-1","slug":"lm-1"},
  {"nome":"Archeologia","codice":"LM-2","slug":"lm-2"},
  {"nome":"Architettura del paesaggio","codice":"LM-3","slug":"lm-3"},
  {"nome":"Architettura e ingegneria edile-architettura","codice":"LM-4","slug":"lm-4"},
  {"nome":"Architettura e ingegneria edile-architettura (quinquennale)","codice":"LM-4cu","slug":"lm-4cu"},
  {"nome":"Archivistica e biblioteconomia","codice":"LM-5","slug":"lm-5"},
  {"nome":"Biologia","codice":"LM-6","slug":"lm-6"},
  {"nome":"Biotecnologie agrarie","codice":"LM-7","slug":"lm-7"},
  {"nome":"Biotecnologie industriali","codice":"LM-8","slug":"lm-8"},
  {"nome":"Biotecnologie mediche, veterinarie e farmaceutiche","codice":"LM-9","slug":"lm-9"},
  {"nome":"Conservazione dei beni architettonici e ambientali","codice":"LM-10","slug":"lm-10"},
  {"nome":"Scienze per la conservazione e restauro dei beni culturali","codice":"LM-11","slug":"lm-11"},
  {"nome":"Design","codice":"LM-12","slug":"lm-12"},
  {"nome":"Farmacia e farmacia industriale","codice":"LM-13","slug":"lm-13"},
  {"nome":"Filologia moderna","codice":"LM-14","slug":"lm-14"},
  {"nome":"Filologia, letterature e storia dell'antichità","codice":"LM-15","slug":"lm-15"},
  {"nome":"Finanza","codice":"LM-16","slug":"lm-16"},
  {"nome":"Fisica","codice":"LM-17","slug":"lm-17"},
  {"nome":"Informatica","codice":"LM-18","slug":"lm-18"},
  {"nome":"Informazione e sistemi editoriali","codice":"LM-19","slug":"lm-19"},
  {"nome":"Ingegneria aerospaziale e astronautica","codice":"LM-20","slug":"lm-20"},
  {"nome":"Ingegneria biomedica","codice":"LM-21","slug":"lm-21"},
  {"nome":"Ingegneria chimica","codice":"LM-22","slug":"lm-22"},
  {"nome":"Ingegneria civile","codice":"LM-23","slug":"lm-23"},
  {"nome":"Ingegneria dei sistemi edilizi","codice":"LM-24","slug":"lm-24"},
  {"nome":"Ingegneria dell'automazione","codice":"LM-25","slug":"lm-25"},
  {"nome":"Ingegneria della sicurezza","codice":"LM-26","slug":"lm-26"},
  {"nome":"Ingegneria delle telecomunicazioni","codice":"LM-27","slug":"lm-27"},
  {"nome":"Ingegneria elettrica","codice":"LM-28","slug":"lm-28"},
  {"nome":"Ingegneria elettronica","codice":"LM-29","slug":"lm-29"},
  {"nome":"Ingegneria energetica e nucleare","codice":"LM-30","slug":"lm-30"},
  {"nome":"Ingegneria gestionale","codice":"LM-31","slug":"lm-31"},
  {"nome":"Ingegneria informatica","codice":"LM-32","slug":"lm-32"},
  {"nome":"Ingegneria meccanica","codice":"LM-33","slug":"lm-33"},
  {"nome":"Ingegneria navale","codice":"LM-34","slug":"lm-34"},
  {"nome":"Ingegneria per l'ambiente e il territorio","codice":"LM-35","slug":"lm-35"},
  {"nome":"Lingue e letterature dell'Africa e dell'Asia","codice":"LM-36","slug":"lm-36"},
  {"nome":"Lingue e letterature moderne europee e americane","codice":"LM-37","slug":"lm-37"},
  {"nome":"Lingue moderne per la comunicazione e la cooperazione internazionale","codice":"LM-38","slug":"lm-38"},
  {"nome":"Linguistica","codice":"LM-39","slug":"lm-39"},
  {"nome":"Matematica","codice":"LM-40","slug":"lm-40"},
  {"nome":"Medicina e chirurgia","codice":"LM-41","slug":"lm-41"},
  {"nome":"Medicina veterinaria","codice":"LM-42","slug":"lm-42"},
  {"nome":"Metodologie informatiche per le discipline umanistiche","codice":"LM-43","slug":"lm-43"},
  {"nome":"Modellistica matematico-fisica per l'ingegneria","codice":"LM-44","slug":"lm-44"},
  {"nome":"Musicologia e beni musicali","codice":"LM-45","slug":"lm-45"},
  {"nome":"Odontoiatria e protesi dentaria","codice":"LM-46","slug":"lm-46"},
  {"nome":"Organizzazione e gestione dei servizi per lo sport e le attività motorie","codice":"LM-47","slug":"lm-47"},
  {"nome":"Pianificazione territoriale urbanistica e ambientale","codice":"LM-48","slug":"lm-48"},
  {"nome":"Progettazione e gestione dei sistemi turistici","codice":"LM-49","slug":"lm-49"},
  {"nome":"Programmazione e gestione dei servizi educativi","codice":"LM-50","slug":"lm-50"},
  {"nome":"Psicologia","codice":"LM-51","slug":"lm-51"},
  {"nome":"Relazioni internazionali","codice":"LM-52","slug":"lm-52"},
  {"nome":"Scienza e ingegneria dei materiali","codice":"LM-53","slug":"lm-53"},
  {"nome":"Scienze chimiche","codice":"LM-54","slug":"lm-54"},
  {"nome":"Scienze cognitive","codice":"LM-55","slug":"lm-55"},
  {"nome":"Scienze dell'economia","codice":"LM-56","slug":"lm-56"},
  {"nome":"Scienze dell'educazione degli adulti e della formazione continua","codice":"LM-57","slug":"lm-57"},
  {"nome":"Scienze dell'universo","codice":"LM-58","slug":"lm-58"},
  {"nome":"Scienze della comunicazione pubblica, d'impresa e pubblicità","codice":"LM-59","slug":"lm-59"},
  {"nome":"Scienze della natura","codice":"LM-60","slug":"lm-60"},
  {"nome":"Scienze della nutrizione umana","codice":"LM-61","slug":"lm-61"},
  {"nome":"Scienze della politica","codice":"LM-62","slug":"lm-62"},
  {"nome":"Scienze delle pubbliche amministrazioni","codice":"LM-63","slug":"lm-63"},
  {"nome":"Scienze delle religioni","codice":"LM-64","slug":"lm-64"},
  {"nome":"Scienze dello spettacolo e produzione multimediale","codice":"LM-65","slug":"lm-65"},
  {"nome":"Sicurezza informatica","codice":"LM-66","slug":"lm-66"},
  {"nome":"Scienze e tecniche delle attività motorie preventive e adattate","codice":"LM-67","slug":"lm-67"},
  {"nome":"Scienze e tecniche dello sport","codice":"LM-68","slug":"lm-68"},
  {"nome":"Scienze e tecnologie agrarie","codice":"LM-69","slug":"lm-69"},
  {"nome":"Scienze e tecnologie alimentari","codice":"LM-70","slug":"lm-70"},
  {"nome":"Scienze e tecnologie della chimica industriale","codice":"LM-71","slug":"lm-71"},
  {"nome":"Scienze e tecnologie della navigazione","codice":"LM-72","slug":"lm-72"},
  {"nome":"Scienze e tecnologie forestali ed ambientali","codice":"LM-73","slug":"lm-73"},
  {"nome":"Scienze e tecnologie geologiche","codice":"LM-74","slug":"lm-74"},
  {"nome":"Scienze e tecnologie per l'ambiente e il territorio","codice":"LM-75","slug":"lm-75"},
  {"nome":"Scienze economiche per l'ambiente e la cultura","codice":"LM-76","slug":"lm-76"},
  {"nome":"Scienze economico-aziendali","codice":"LM-77","slug":"lm-77"},
  {"nome":"Scienze filosofiche","codice":"LM-78","slug":"lm-78"},
  {"nome":"Scienze geofisiche","codice":"LM-79","slug":"lm-79"},
  {"nome":"Scienze geografiche","codice":"LM-80","slug":"lm-80"},
  {"nome":"Scienze per la cooperazione allo sviluppo","codice":"LM-81","slug":"lm-81"},
  {"nome":"Scienze statistiche","codice":"LM-82","slug":"lm-82"},
  {"nome":"Scienze statistiche attuariali e finanziarie","codice":"LM-83","slug":"lm-83"},
  {"nome":"Scienze storiche","codice":"LM-84","slug":"lm-84"},
  {"nome":"Scienze pedagogiche","codice":"LM-85","slug":"lm-85"},
  {"nome":"Scienze della formazione primaria","codice":"LM-85 bis","slug":"lm-85bis"},
  {"nome":"Scienze zootecniche e tecnologie animali","codice":"LM-86","slug":"lm-86"},
  {"nome":"Servizio sociale e politiche sociali","codice":"LM-87","slug":"lm-87"},
  {"nome":"Sociologia e ricerca sociale","codice":"LM-88","slug":"lm-88"},
  {"nome":"Storia dell'arte","codice":"LM-89","slug":"lm-89"},
  {"nome":"Studi europei","codice":"LM-90","slug":"lm-90"},
  {"nome":"Tecniche e metodi per la società dell'informazione","codice":"LM-91","slug":"lm-91"},
  {"nome":"Teorie della comunicazione","codice":"LM-92","slug":"lm-92"},
  {"nome":"Teorie e metodologie dell'E-Learning e della media education","codice":"LM-93","slug":"lm-93"},
  {"nome":"Traduzione specialistica e interpretariato","codice":"LM-94","slug":"lm-94"},
  {"nome":"Data Science","codice":"LM-Data","slug":"lm-data"},
  {"nome":"Scienze dei materiali","codice":"LM-Sc.Mat.","slug":"lm-sc-mat"},
  {"nome":"Scienze della difesa e della sicurezza","codice":"LM/DS","slug":"lm-ds"},
  {"nome":"Scienze economiche e sociali della gastronomia","codice":"LM/GASTR","slug":"lm-gastr"},
  {"nome":"Scienze Giuridiche","codice":"LM/SC-GIUR","slug":"lm-sc-giur"},
  {"nome":"Professioni sanitarie infermieristiche e professione sanitaria ostetrica","codice":"LM/SNT1","slug":"lm-snt1"},
  {"nome":"Professioni sanitarie della riabilitazione","codice":"LM/SNT2","slug":"lm-snt2"},
  {"nome":"Professioni sanitarie tecniche","codice":"LM/SNT3","slug":"lm-snt3"},
  {"nome":"Professioni sanitarie della prevenzione","codice":"LM/SNT4","slug":"lm-snt4"},
  {"nome":"Giurisprudenza","codice":"LMG/01","slug":"lmg-01"},
  {"nome":"Conservazione e restauro dei beni culturali","codice":"LMR/02","slug":"lmr-02"}
]

with open("data/corsi_per_classe.json", encoding="utf-8") as f:
    corsi_per_classe = json.load(f)

with open("data/universita.json", encoding="utf-8") as f:
    universita_list = json.load(f)

mappa_universita = {u["sigla"]: u for u in universita_list}

def genera_righe_html(codice):
    corso = corsi_per_classe.get(codice)
    if not corso:
        return ""
    
    righe = []
    for offerta in corso["offerte"]:
        uni = mappa_universita.get(offerta["universita"], {})
        sigla = offerta["universita"]
        slug = sigla.lower().replace(" ", "_")
        link = f"../atenei/{slug}.html"
        nome_uni = uni.get("nome", offerta["universita"])
        regione = offerta.get("regione", uni.get("regione", "----"))
        accesso = "✅ Accesso Libero" if offerta["accessoLibero"] else "🔒 Accesso Programmato"
        
        # Serializza l'offerta come data attribute per il JS
        data_offerta = json.dumps(offerta, ensure_ascii=False).replace('"', '&quot;')
        
        righe.append(f"""
                    <tr class="riga-principale" data-offerta="{data_offerta}">
                        <td><a class="uni" href="{link}">{nome_uni}</a></td>
                        <td colspan="4"><strong>{offerta["nomeCorso"]}</strong></td>
                    </tr>
                    <tr class="riga-dettagli">
                        <td colspan="2" class="dettaglio">📍 {offerta["sede"]} — {regione}</td>
                        <td class="dettaglio">🎓 {offerta["didattica"]}</td>
                        <td class="dettaglio">🌐 {offerta["lingua"]} &nbsp;|&nbsp; {accesso}</td>
                    </tr>""")
    
    return "\n".join(righe)

template = """<!DOCTYPE html>
<html lang="it">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <title>Corsi di laurea in {{NOME}} ({{CODICE}}): università e sedi | Unidirectory</title>
    <meta name="description"
        content="Scopri in quali università e sedi è attivo il corso di laurea in {{NOME}} ({{CODICE}}) in Italia. Elenco chiaro e aggiornato delle sedi disponibili.">
    <meta name="robots" content="index,follow">


    <link rel="canonical" href="https://unidirectory.it/classi/{{SLUG}}">
    <script>
        if (window.location.hostname === 'samuelefrasca.github.io' || window.location.hostname === 'unidirectory.pages.dev') {
            const path = window.location.pathname
                .replace('/unidirectory', '')
                .replace(/\.html$/, '');
            window.location.replace('https://unidirectory.it' + path + window.location.search);
        }
    </script>

    <meta property="og:site_name" content="Unidirectory">
    <meta property="og:title" content="Corsi di laurea in {{NOME}} ({{CODICE}}): università e sedi | Unidirectory">
    <meta property="og:description"
        content="Scopri in quali università e sedi è attivo il corso di laurea in {{NOME}} ({{CODICE}}) in Italia.">
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://unidirectory.it/classi/{{SLUG}}">
    <meta property="og:image"
        content="https://unidirectory.it/assets/img/iud_icon.png">


    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="Corsi di laurea in {{NOME}} ({{CODICE}}): università e sedi | Unidirectory">
    <meta name="twitter:description"
        content="Scopri in quali università e sedi è attivo il corso di laurea in {{NOME}} ({{CODICE}}) in Italia.">
    <meta name="twitter:image"
        content="https://unidirectory.it/assets/img/iud_icon.png">


    <link rel="icon" type="image/png" href="../assets/img/iud_icon.png">
    <link rel="stylesheet" href="../assets/css/style.css">
    <link rel="stylesheet" href="../assets/css/classi.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">

    <script type="application/ld+json">
    {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Corsi di laurea in {{NOME}} ({{CODICE}}): università e sedi | Unidirectory",
        "url": "https://unidirectory.it/classi/{{SLUG}}",
        "description": "Scopri in quali università e sedi è attivo il corso di laurea in {{NOME}} ({{CODICE}}) in Italia. Elenco chiaro e aggiornato delle sedi disponibili."
    }
    </script>
</head>


<body>
    <header>
        <div class="container">
            <div class="header">
                <div class="header1">
                    <a href="/">
                        <img class="logo" src="../assets/img/iud_image.png" alt="Logo Unidirectory">
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
                <div class="filtri">
                    <select id="filtroLingua" onchange="gestisciFiltroLingua(this.value, '{{CODICE}}')">
                        <option value="">Tutte le lingue</option>
                        <option value="italiano">Italiano</option>
                        <option value="inglese">Inglese</option>
                        <option value="tedesco">Tedesco</option>
                        <option value="francese">Francese</option>
                        <option value="ladino">Ladino</option>
                    </select>
                    <select id="filtroAccesso" onchange="gestisciFiltroAccesso(this.value, '{{CODICE}}')">
                        <option value="">Tutti gli accessi</option>
                        <option value="libero">Accesso libero</option>
                        <option value="programmato">Accesso programmato</option>
                    </select>
                    <select id="filtroDidattica" onchange="gestisciFiltroDidattica(this.value, '{{CODICE}}')">
                        <option value="">Tutte le didattiche</option>
                        <option value="presenza">In presenza</option>
                        <option value="distanza">A distanza</option>
                        <option value="mista">Mista</option>
                    </select>
                </div>
                <div class="ordina">
                    <button type="button" onclick="ordinaPerCorso('{{CODICE}}')">Ordina per corso</button>
                    <button type="button" onclick="ordinaPerSede('{{CODICE}}')">Ordina per sede</button>
                    <button type="button" onclick="ordinaPerRegione('{{CODICE}}')">Ordina per regione</button>
                </div>
            </div>
            <input type="search" id="searchNelleClassi" placeholder="Cerca università, sede, regione o corso...">
            <h3 id ="corsitrovati"></h3>
            <table>
                <tbody id="tabellauni">{{RIGHE}}</tbody>
            </table>
            <p class="data-note">
                Dati dei corsi dal MUR (USTAT), aggiornati al 2025 ed elaborati automaticamente. Eventuali errori possono dipendere dai dati di origine.
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
            <p><a class="a_footer" href="../about.html">About</a></p>
            <p><a class="a_footer" href="../privacy.html">Privacy Policy</a></p>
            <p><a class="a_footer" href="../sitemap.xml">Sitemap</a></p>
            <p><a class="a_footer" href="mailto:info@unidirectory.it">Contattaci</a></p>
        </div>
    </footer>
    <script src="../assets/js/footer.js"></script>
    <script src="../assets/js/scriptclassi.js"></script>
    <script>
        caricaTabella("{{CODICE}}");
        ordinecorso = true;
        ordinecitta = false;
        ordineregione = false;
    </script>
</body>

</html>
"""

cartella_output = Path("classi")
cartella_output.mkdir(exist_ok=True)

for classe in classi:
    contenuto = (
        template
        .replace("{{NOME}}", classe["nome"])
        .replace("{{CODICE}}", classe["codice"])
        .replace("{{SLUG}}", classe["slug"])
        .replace("{{RIGHE}}", genera_righe_html(classe["codice"]))
    )

    nome_file = f"{classe['slug']}.html"
    (cartella_output / nome_file).write_text(contenuto, encoding="utf-8")

print("Creati", len(classi), "file HTML.")