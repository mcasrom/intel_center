import sys, os, feedparser, sqlite3, json, socket, time
from datetime import datetime, timedelta

# --- OPTIMIZACIÓN DE RECURSOS ---
TIMEOUT = 30 
socket.setdefaulttimeout(TIMEOUT)
BASE_DIR = "/home/miguelc/intel_center_test"
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")



JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'

FEEDS = {
    "Rusia_Eurasia": "https://tass.com/rss/v2.xml",
    "Medio_Oriente": "https://www.aljazeera.com/xml/rss/all.xml",
    "Europa_DW": "https://rss.dw.com/rdf/rss-en-top",
    "Africa_Sahel": "https://www.africanews.com/feed/",
    "Asia_Nikkei": "https://asia.nikkei.com/rss/feed/nar",
    "LATAM": "https://www.bbc.com/mundo/temas/america_latina/index.xml",
    "MEXICO": "https://www.jornada.com.mx/rss/ultimas.xml?v=1",
    "USA_NORTE": "https://www.theguardian.com/us-news/rss"
}

COORDENADAS = {
    "Rusia_Eurasia": [60.0, 90.0], 
    "Medio_Oriente": [25.0, 45.0],
    "Europa_DW": [50.0, 10.0], 
    "Africa_Sahel": [15.0, 15.0], 
    "Asia_Nikkei": [35.0, 135.0],
    "LATAM": [-15.0, -60.0], 
    "MEXICO": [23.0, -102.0],
    "USA_NORTE": [40.0, -100.0]
}

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    cur = conn.cursor()
    # MODO WAL: Vital para resiliencia ante cortes de luz en Odroid
    try: cur.execute('PRAGMA journal_mode=WAL;')
    except: pass
    cur.execute('CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY AUTOINCREMENT, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, region TEXT, title TEXT, link TEXT UNIQUE)')
    conn.commit()
    return conn


def housekeeping(conn):
    print("🧹 Iniciando autolimpieza y rotación (30 días)...")
    # 1. Limpieza de Base de Datos (opcional, para no engordar el .db)
    cur = conn.cursor()
    cur.execute("DELETE FROM news WHERE timestamp < date('now', '-30 days')")
    conn.commit()

    # 2. Rotación de archivos Markdown en la carpeta posts
    import time
    now = time.time()
    for f in os.listdir(POSTS_OUTPUT):
        f_path = os.path.join(POSTS_OUTPUT, f)
        # Si el archivo es un .md y tiene más de 30 días (30 * 24 * 60 * 60 segundos)
        if f.endswith(".md") and f != "_index.md":
            if os.stat(f_path).st_mtime < now - (30 * 86400):
                os.remove(f_path)
                print(f"🗑️ Eliminado informe antiguo: {f}")


def fetch_data(conn):
    cur = conn.cursor()
    for reg, url in FEEDS.items():
        print(f"📥 {reg}...", end=" ", flush=True)
        try:
            f = feedparser.parse(url, agent=USER_AGENT)
            c = 0
            for e in f.entries[:15]:
                cur.execute("INSERT OR IGNORE INTO news (region, title, link) VALUES (?, ?, ?)", (reg, e.title, e.link))
                if cur.rowcount > 0: c += 1
            print(f"✅ {c}")
        except: print("❌")
    conn.commit()

def export_map_json(conn):
    cur = conn.cursor()
    # Solo contamos noticias de las últimas 24 horas para que el mapa sea real
    cur.execute("SELECT region, COUNT(*) FROM news WHERE timestamp > datetime('now', '-24 hours') GROUP BY region")
    results = cur.fetchall()
    
    # Creamos la lista desde cero
    hs = []
    for r, ct in results:
        if r in COORDENADAS:
            hs.append({
                "name": r,
                "lat": COORDENADAS[r][0],
                "lon": COORDENADAS[r][1],
                "intensity": ct
            })
    
    # Sobreescribimos el archivo JSON
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(hs, f, indent=4)
    print(f"📍 Mapa actualizado con {len(hs)} regiones activas.")



def create_hugo_post(conn):
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime('%Y-%m-%d')    
    filename = os.path.join(POSTS_OUTPUT, f"{date_str}-informe-inteligencia.md")    
    cur = conn.cursor()
    cur.execute("SELECT region, title FROM news WHERE date(timestamp) = date('now') ORDER BY timestamp DESC")
    news_today = cur.fetchall()

    content = f"---\ntitle: \"Resumen Inteligencia {date_str}\"\ndate: \"{date_iso}\"\ntype: \"post\"\ndraft: false\n---\n\n"
    for reg, tit in news_today:
        content += f"- **[{reg}]**: {tit}\n"

    with open(filename, 'w') as f: f.write(content)

if __name__ == "__main__":
    db = init_db()
    housekeeping(db) # Limpia antes de procesar
    fetch_data(db)
    export_map_json(db)
    create_hugo_post(db)
    db.close()
    print("🚀 Nodo Optimizado y Sincronizado.")
