import os, feedparser, sqlite3, json
from datetime import datetime
from textblob import TextBlob

# --- CONFIGURACIÓN DE RUTAS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")
USA_LOG_CSV = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_LOG_CSV = os.path.join(BASE_DIR, "data/spain_trend.csv")
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

# --- FUENTES Y PALABRAS CLAVE ---
FEEDS_SPAIN = [
    "https://elpais.com/rss/politica/portada.xml",
    "https://www.elmundo.es/e/rss/espana.xml"
]
FEEDS_ARGENTINA = [
    "https://www.lanacion.com.ar/arc/outboundfeeds/rss/?outputType=xml",
    "https://www.clarin.com/rss/politica/"
]
FEEDS_BRASIL = [
    "https://feeds.folha.uol.com.br/poder/rss091.xml",
    "https://agenciabrasil.ebc.com.br/rss/politica/feed.xml",
    "https://noticias.uol.com.br/politica/index.xml"
]

DATOS_INTEL = {
    "Rusia_Eurasia": {"url": "https://tass.com/rss/v2.xml", "coord": [60.0, 90.0]},
    "Medio_Oriente": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "coord": [25.0, 45.0]},
    "Europa_DW": {"url": "https://rss.dw.com/rdf/rss-en-top", "coord": [50.0, 10.0]},
    "Asia_Nikkei": {"url": "https://asia.nikkei.com/rss/feed/nar", "coord": [35.0, 135.0]},
    "LATAM_General": {"url": "https://www.bbc.com/mundo/temas/america_latina/index.xml", "coord": [5.0, -70.0]},
    "ARGENTINA": {"url": "COMBO_ARG", "coord": [-34.6, -58.4]},
    "BRASIL": {"url": "COMBO_BR", "coord": [-15.7, -47.8]},
    "MEXICO": {"url": "https://www.jornada.com.mx/rss/ultimas.xml?v=1", "coord": [23.0, -102.0]},
    "USA_NORTE": {"url": "https://www.theguardian.com/us-news/rss", "coord": [40.0, -100.0]},
    "ESPAÑA": {"url": "COMBO", "coord": [40.4, -3.7]},
    "Africa_Sahel": {"url": "https://www.africanews.com/feed/", "coord": [15.0, 15.0]}
}

KEYWORDS_CRITICAS = ["nuclear", "misil", "atentado", "ataque", "war", "coup", "militar", "threat", "sanción", "tensión"]
KEYWORDS_ELECTORALES = ["election", "voters", "polling", "ballot", "elecciones", "comicios", "votación", "candidato", "campaña"]

def obtener_sentimiento(texto):
    try: return TextBlob(texto).sentiment.polarity
    except: return 0.0

def registrar_tendencia(path, valor, fecha):
    if not os.path.exists(path):
        with open(path, 'w') as f: f.write("timestamp,avg_sentiment\n")
    with open(path, 'a') as f:
        f.write(f"{fecha},{round(valor, 4)}\n")

def ejecutar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(POSTS_OUTPUT, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS news 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                   region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL)''')
    cur.execute("DELETE FROM news WHERE timestamp < datetime('now', '-7 days')")
    
    ahora = datetime.now()
    fecha_str = ahora.strftime('%Y-%m-%d %H:%M')

    print("--- INICIANDO CAPTURA (MODO MULTI-REGIONAL) ---")
    total_articulos = 0
    for reg, info in DATOS_INTEL.items():
        # Lógica de selección de feeds corregida
        if info["url"] == "COMBO":
            feeds_a_procesar = FEEDS_SPAIN
        elif info["url"] == "COMBO_ARG":
            feeds_a_procesar = FEEDS_ARGENTINA
        elif info["url"] == "COMBO_BR":
            feeds_a_procesar = FEEDS_BRASIL
        else:
            feeds_a_procesar = [info["url"]]

        for url in feeds_a_procesar:
            f_parse = feedparser.parse(url, agent=USER_AGENT)
            for e in f_parse.entries[:10]:
                pola = obtener_sentimiento(str(e.title))
                cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?, ?, ?, ?)", 
                            (reg, e.title, e.link, pola))
                total_articulos += 1
    conn.commit()

    # --- CÁLCULO DE RADARES ---
    def get_avg(region):
        cur.execute("SELECT AVG(sentimiento) FROM news WHERE region=? AND timestamp > datetime('now', '-24 hours')", (region,))
        return cur.fetchone()[0] or 0.0

    avg_usa = get_avg('USA_NORTE')
    avg_spain = get_avg('ESPAÑA')
    registrar_tendencia(USA_LOG_CSV, avg_usa, fecha_str)
    registrar_tendencia(SPAIN_LOG_CSV, avg_spain, fecha_str)

    # --- CATEGORÍAS PARA HUGO ---
    cur.execute("SELECT DISTINCT region FROM news WHERE timestamp > datetime('now', '-24 hours')")
    regiones_presentes = [row[0] for row in cur.fetchall()]
    categorias_str = ", ".join([f'"{r}"' for r in regiones_presentes])

    # --- GENERAR JSON PARA MAPA ---
    cur.execute("SELECT region, COUNT(*), AVG(sentimiento) FROM news WHERE timestamp > datetime('now', '-24 hours') GROUP BY region")
    hotspots = []
    for r, ct, s in cur.fetchall():
        if r in DATOS_INTEL:
            color = "#f1c40f"
            if s < -0.05: color = "#ff4b2b"
            hotspots.append({
                "name": r, "lat": DATOS_INTEL[r]["coord"][0], "lon": DATOS_INTEL[r]["coord"][1],
                "intensity": ct, "color": color, "sentiment_index": round(s, 2)
            })
    with open(JSON_OUTPUT, 'w') as f_json: json.dump(hotspots, f_json, indent=4)

    # --- INFORME HUGO ---
    filename = f"{ahora.strftime('%Y-%m-%d')}-informe.md"
    with open(os.path.join(POSTS_OUTPUT, filename), 'w') as f:
        f.write(f"---\n")
        f.write(f"title: \"Monitor Intel: {ahora.strftime('%H:%M')} (UTC)\"\n")
        f.write(f"date: {ahora.strftime('%Y-%m-%dT%H:%M:%S')}\n")
        f.write(f"categories: [{categorias_str}]\n")
        f.write(f"description: \"Análisis de sentimiento global. Foco especial en LATAM y Cono Sur.\"\n")
        f.write(f"---\n\n")

        f.write(f"## 🛡️ ESTADO DEL NODO\n\n")
        f.write(f"| Indicador | Valor |\n")
        f.write(f"| :--- | :--- |\n")
        f.write(f"| **STATUS** | 🟢 **OPERATIVO** |\n")
        f.write(f"| **NODO** | `Odroid-C2-Madrid` |\n")
        f.write(f"| **ARTÍCULOS PROCESADOS** | {total_articulos} |\n\n")

        f.write(f"## 📈 RADARES DE TENDENCIA\n\n")
        f.write(f"| Región | Sentimiento |\n")
        f.write(f"| :--- | :--- |\n")
        f.write(f"| 🇺🇸 USA | **{round(avg_usa, 4)}** |\n")
        f.write(f"| 🇪🇸 ESPAÑA | **{round(avg_spain, 4)}** |\n\n")

        cur.execute("SELECT region, title, link FROM news WHERE timestamp > datetime('now', '-24 hours') ORDER BY timestamp DESC LIMIT 80")
        alertas, electoral, normales = [], [], []
        vistas = set()

        for reg, tit, link in cur.fetchall():
            if tit in vistas: continue
            vistas.add(tit)
            txt = f"- **[{reg}]**: {tit} ([Link]({link}))"
            tit_l = tit.lower()
            if any(key in tit_l for key in KEYWORDS_CRITICAS):
                alertas.append(txt.replace("**[", "🚩 **[ALERTA] "))
            elif any(key in tit_l for key in KEYWORDS_ELECTORALES):
                electoral.append(txt.replace("**[", "🗳️ **[ELECTORAL] "))
            else:
                normales.append(txt)

        if alertas:
            f.write(f"### ⚡ ALERTAS CRÍTICAS\n\n")
            f.write("\n".join(alertas) + "\n\n")

        if electoral:
            f.write(f"### 🗳️ VIGILANCIA ELECTORAL\n\n")
            f.write("\n".join(electoral) + "\n\n")

        f.write(f"### 🌍 RESUMEN GLOBAL\n\n")
        f.write("\n".join(normales[:50]))

    conn.close()
    print(f"[+] INFORME GENERADO EXITOSAMENTE: {filename}")

if __name__ == "__main__":
    ejecutar()
