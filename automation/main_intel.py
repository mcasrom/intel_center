import os, feedparser, sqlite3, json, socket
from datetime import datetime
from textblob import TextBlob

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = os.path.expanduser("~/intel_center_test")
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

FEEDS = {
    "Rusia_Eurasia": "https://tass.com/rss/v2.xml",
    "Medio_Oriente": "https://www.aljazeera.com/xml/rss/all.xml",
    "Europa_DW": "https://rss.dw.com/rdf/rss-en-top",
    "Asia_Nikkei": "https://asia.nikkei.com/rss/feed/nar",
    "LATAM": "https://www.bbc.com/mundo/temas/america_latina/index.xml",
    "MEXICO": "https://www.jornada.com.mx/rss/ultimas.xml?v=1",
    "USA_NORTE": "https://www.theguardian.com/us-news/rss",
    "Australia": "https://www.abc.net.au/news/feed/51120/rss.xml",
    "Canada": "https://www.cbc.ca/cxml/rss/news/world",
    "Groenlandia": "https://www.arctictoday.com/feed/",
    "Africa_Sahel": "https://www.africanews.com/feed/"
}

COORDENADAS = {
    "Rusia_Eurasia": [60.0, 90.0],
    "Medio_Oriente": [25.0, 45.0],
    "Europa_DW": [50.0, 10.0],
    "Asia_Nikkei": [35.0, 135.0],
    "LATAM": [-15.0, -60.0],
    "MEXICO": [23.0, -102.0],
    "USA_NORTE": [40.0, -100.0],
    "Australia": [-25.0, 133.0],
    "Canada": [60.0, -110.0],
    "Groenlandia": [72.0, -40.0],
    "Africa_Sahel": [15.0, 15.0]
}

def ejecutar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(POSTS_OUTPUT, exist_ok=True)
    os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS news 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                   region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL)''')

    print("--- INICIANDO CAPTURA ---")
    for reg, url in FEEDS.items():
        print(f"📡 {reg}...", end=" ", flush=True)
        f = feedparser.parse(url, agent=USER_AGENT)
        c = 0
        if f.entries:
            for e in f.entries[:15]:
                pola = TextBlob(str(e.title)).sentiment.polarity
                cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?, ?, ?, ?)", 
                            (reg, e.title, e.link, pola))
                if cur.rowcount > 0: c += 1
            print(f"OK (+{c})")
        else:
            print("⚠️ ERROR")
    conn.commit()

    ahora = datetime.now()
    fecha_str = ahora.strftime("%Y-%m-%d")
    
    # --- GENERAR JSON (LISTA PURA PARA JAVASCRIPT) ---
    cur.execute("SELECT region, COUNT(*), AVG(sentimiento) FROM news WHERE timestamp > datetime('now', '-24 hours') GROUP BY region")
    resultados = cur.fetchall()
    
    hotspots = []
    for r, ct, s in resultados:
        if r in COORDENADAS:
            color = "#f1c40f"
            if s < -0.1: color = "#ff4b2b"
            elif s > 0.1: color = "#2ecc71"
            
            hotspots.append({
                "name": r,
                "lat": COORDENADAS[r][0],
                "lon": COORDENADAS[r][1],
                "intensity": ct,
                "color": color,
                "sentiment_index": round(s, 2)
            })

    # IMPORTANTE: Escribe la lista directamente (sin diccionario exterior)
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(hotspots, f, indent=4)

    # --- GENERAR INFORME HUGO ---
    filename = os.path.join(POSTS_OUTPUT, f"{fecha_str}-informe-inteligencia.md")
    cur.execute("SELECT region, title, link FROM news WHERE timestamp > datetime('now', '-24 hours') ORDER BY timestamp DESC LIMIT 60")
    records = cur.fetchall()

    with open(filename, 'w') as f:
        f.write(f"---\ntitle: \"Informe de Inteligencia - {fecha_str}\"\ndate: {ahora.strftime('%Y-%m-%dT%H:%M:%S')}\ntype: \"post\"\n---\n\n")
        f.write(f"### 🕒 Corte de datos: {ahora.strftime('%H:%M:%S')}\n\n")
        for reg, tit, link in records:
            f.write(f"- **[{reg}]**: {tit} ([Link]({link}))\n")

    conn.close()
    print(f"--- ÉXITO: Mapa y Post actualizados ---")

if __name__ == "__main__":
    ejecutar()
