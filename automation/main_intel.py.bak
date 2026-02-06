import os, feedparser, sqlite3, json
from datetime import datetime
from textblob import TextBlob

# --- CONFIGURACIÓN DE RUTAS ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

# --- FUENTES Y PALABRAS CLAVE ---
DATOS_INTEL = {
    "Rusia_Eurasia": {"url": "https://tass.com/rss/v2.xml", "coord": [60.0, 90.0]},
    "Medio_Oriente": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "coord": [25.0, 45.0]},
    "Europa_DW": {"url": "https://rss.dw.com/rdf/rss-en-top", "coord": [50.0, 10.0]},
    "Asia_Nikkei": {"url": "https://asia.nikkei.com/rss/feed/nar", "coord": [35.0, 135.0]},
    "LATAM": {"url": "https://www.bbc.com/mundo/temas/america_latina/index.xml", "coord": [-15.0, -60.0]},
    "MEXICO": {"url": "https://www.jornada.com.mx/rss/ultimas.xml?v=1", "coord": [23.0, -102.0]},
    "USA_NORTE": {"url": "https://www.theguardian.com/us-news/rss", "coord": [40.0, -100.0]},
    "Africa_Sahel": {"url": "https://www.africanews.com/feed/", "coord": [15.0, 15.0]}
}

KEYWORDS_CRITICAS = ["nuclear", "misil", "atentado", "ataque", "war", "coup", "militar", "threat"]
KEYWORDS_ELECTORALES = ["election", "voters", "polling", "ballot", "elecciones", "comicios", "votación", "candidato"]

def obtener_sentimiento(texto):
    try: return TextBlob(texto).sentiment.polarity
    except: return 0.0

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
    
    print("--- INICIANDO CAPTURA CON VIGILANCIA ELECTORAL ---")
    for reg, info in DATOS_INTEL.items():
        f = feedparser.parse(info["url"], agent=USER_AGENT)
        if f.entries:
            for e in f.entries[:15]:
                pola = obtener_sentimiento(str(e.title))
                cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?, ?, ?, ?)", 
                            (reg, e.title, e.link, pola))
    conn.commit()

    # --- ANOMALÍAS Y PROCESO ELECTORAL ---
    regiones_anomalas = []
    regiones_electorales = []
    ahora = datetime.now()

    for reg in DATOS_INTEL:
        # Lógica de Anomalía (Volumen)
        cur.execute("SELECT COUNT(*) FROM news WHERE region=? AND timestamp > datetime('now', '-1 day')", (reg,))
        hoy = cur.fetchone()[0]
        if hoy > 15: regiones_anomalas.append(reg)

        # Lógica Electoral (Contenido)
        cur.execute("SELECT title FROM news WHERE region=? AND timestamp > datetime('now', '-24 hours')", (reg,))
        titulos = [row[0].lower() for row in cur.fetchall()]
        if any(any(key in t for key in KEYWORDS_ELECTORALES) for t in titulos):
            regiones_electorales.append(reg)

    # --- GENERAR JSON PARA MAPA ---
    cur.execute("SELECT region, COUNT(*), AVG(sentimiento) FROM news WHERE timestamp > datetime('now', '-24 hours') GROUP BY region")
    hotspots = []
    for r, ct, s in cur.fetchall():
        if r in DATOS_INTEL:
            color = "#f1c40f" # Amarillo base
            if r in regiones_electorales: color = "#3498db" # Azul Electoral
            elif s < -0.1: color = "#ff4b2b" # Rojo Conflicto
            
            hotspots.append({
                "name": r, "lat": DATOS_INTEL[r]["coord"][0], "lon": DATOS_INTEL[r]["coord"][1],
                "intensity": ct, "color": color, "sentiment_index": round(s, 2),
                "anomaly": (r in regiones_anomalas),
                "election_active": (r in regiones_electorales)
            })
    
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(hotspots, f, indent=4)

    # --- GENERAR INFORME HUGO ---
    cur.execute("SELECT region, title, link FROM news WHERE timestamp > datetime('now', '-24 hours') ORDER BY timestamp DESC LIMIT 80")
    alertas, electoral, normales = [], [], []
    for reg, tit, link in cur.fetchall():
        txt = f"- **[{reg}]**: {tit} ([Link]({link}))"
        if any(key in tit.lower() for key in KEYWORDS_CRITICAS): alertas.append(txt.replace("**[", "🚩 **[ALERTA] "))
        elif any(key in tit.lower() for key in KEYWORDS_ELECTORALES): electoral.append(txt.replace("**[", "🗳️ **[ELECTORAL] "))
        else: normales.append(txt)

    with open(os.path.join(POSTS_OUTPUT, f"{ahora.strftime('%Y-%m-%d')}-informe.md"), 'w') as f:
        f.write(f"---\ntitle: \"Monitor Intel - {ahora.strftime('%Y-%m-%d %H:%M')}\"\ndate: {ahora.strftime('%Y-%m-%dT%H:%M:%S')}\n---\n")
        if electoral: f.write("\n## 🗳️ VIGILANCIA ELECTORAL\n" + "\n".join(electoral) + "\n")
        if alertas: f.write("\n## ⚡ ALERTAS CRÍTICAS\n" + "\n".join(alertas) + "\n")
        f.write("\n## 🌍 RESUMEN GLOBAL\n" + "\n".join(normales[:50]))

    conn.close()
    print(f"[+] ÉXITO: {len(regiones_anomalas)} anomalías, {len(regiones_electorales)} procesos electorales.")

if __name__ == "__main__":
    ejecutar()
