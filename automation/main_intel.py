import os, feedparser, sqlite3, json, socket
from datetime import datetime
from textblob import TextBlob

# --- CONFIGURACIÓN ---
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
    "Africa_Sahel": "https://www.africanews.com/feed/"
}

def ejecutar():
    # 1. Preparar entorno
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(POSTS_OUTPUT, exist_ok=True)
    os.makedirs(os.path.dirname(JSON_OUTPUT), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS news 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                   region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL)''')

    # 2. Captura de datos
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

    # 3. Generar Informe Hugo
    ahora = datetime.now()
    fecha_str = ahora.strftime("%Y-%m-%d")
    filename = os.path.join(POSTS_OUTPUT, f"{fecha_str}-informe-inteligencia.md")
    
    cur.execute("SELECT region, title, link FROM news WHERE timestamp > datetime('now', '-24 hours') ORDER BY timestamp DESC LIMIT 60")
    records = cur.fetchall()

    with open(filename, 'w') as f:
        f.write(f"---\ntitle: \"Informe de Inteligencia - {fecha_str}\"\ndate: {ahora.strftime('%Y-%m-%dT%H:%M:%S')}\ntype: \"post\"\n---\n\n")
        f.write(f"### 🕒 Corte de datos: {ahora.strftime('%H:%M:%S')}\n\n")
        for reg, tit, link in records:
            f.write(f"- **[{reg}]**: {tit} ([Link]({link}))\n")

    # 4. Generar JSON para el Mapa
    cur.execute("SELECT region, COUNT(*), AVG(sentimiento) FROM news WHERE timestamp > datetime('now', '-24 hours') GROUP BY region")
    hs = [{"name": r, "count": ct, "sent": round(s, 2)} for r, ct, s in cur.fetchall()]
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(hs, f, indent=4)

    conn.close()
    print(f"--- ÉXITO: {filename} generado ---")

if __name__ == "__main__":
    ejecutar()
