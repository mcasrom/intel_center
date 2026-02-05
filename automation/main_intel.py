import sys, os, feedparser, sqlite3, json, socket, time
from datetime import datetime, timedelta
from textblob import TextBlob

# --- OPTIMIZACIÓN DE RECURSOS ---
TIMEOUT = 30 
socket.setdefaulttimeout(TIMEOUT)
BASE_DIR = "/home/miguelc/intel_center_test"
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")
USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0'

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

def analizar_sentimiento(texto):
    """Retorna polaridad (-1 a 1) y color hexadecimal."""
    blob = TextBlob(str(texto))
    pola = blob.sentiment.polarity
    if pola < -0.1: return pola, "#ff4b2b" # Rojo (Tensión)
    if pola > 0.1:  return pola, "#2ecc71" # Verde (Calma)
    return pola, "#f1c40f"                 # Amarillo (Neutral)

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), timeout=30)
    cur = conn.cursor()
    try: cur.execute('PRAGMA journal_mode=WAL;')
    except: pass
    # AÑADIDA COLUMNA 'sentimiento'
    cur.execute('''CREATE TABLE IF NOT EXISTS news 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                   region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL)''')
    conn.commit()
    return conn

def housekeeping(conn):
    print("🧹 Iniciando autolimpieza y rotación (30 días)...")
    cur = conn.cursor()
    cur.execute("DELETE FROM news WHERE timestamp < date('now', '-30 days')")
    conn.commit()
    now = time.time()
    for f in os.listdir(POSTS_OUTPUT):
        f_path = os.path.join(POSTS_OUTPUT, f)
        if f.endswith(".md") and f != "_index.md":
            if os.stat(f_path).st_mtime < now - (30 * 86400):
                os.remove(f_path)

def fetch_data(conn):
    cur = conn.cursor()
    for reg, url in FEEDS.items():
        print(f"📥 {reg}...", end=" ", flush=True)
        try:
            f = feedparser.parse(url, agent=USER_AGENT)
            c = 0
            for e in f.entries[:15]:
                pola, _ = analizar_sentimiento(e.title)
                cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?, ?, ?, ?)", 
                            (reg, e.title, e.link, pola))
                if cur.rowcount > 0: c += 1
            print(f"✅ {c}")
        except: print("❌")
    conn.commit()

def export_map_json(conn):
    cur = conn.cursor()
    # Promediamos sentimiento y contamos noticias
    cur.execute("""SELECT region, COUNT(*), AVG(sentimiento) FROM news 
                   WHERE timestamp > datetime('now', '-24 hours') GROUP BY region""")
    results = cur.fetchall()
    
    hs = []
    for r, ct, sent_avg in results:
        if r in COORDENADAS:
            # Asignar color según el promedio de la región
            color = "#f1c40f" # Default amarillo
            if sent_avg < -0.1: color = "#ff4b2b" # Rojo
            elif sent_avg > 0.1: color = "#2ecc71" # Verde
            
            hs.append({
                "name": r,
                "lat": COORDENADAS[r][0],
                "lon": COORDENADAS[r][1],
                "intensity": ct,
                "color": color,
                "sentiment_index": round(sent_avg, 2)
            })
    
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(hs, f, indent=4)
    print(f"📍 Mapa actualizado con {len(hs)} regiones y análisis de tensión.")

def create_hugo_post(conn):
    date_str = datetime.now().strftime("%Y-%m-%d")
    date_iso = datetime.now().strftime('%Y-%m-%d')    
    filename = os.path.join(POSTS_OUTPUT, f"{date_str}-informe-inteligencia.md")    
    cur = conn.cursor()
    
    # Obtenemos noticias de hoy
    cur.execute("SELECT region, title, sentimiento, link FROM news WHERE date(timestamp) = date('now') ORDER BY timestamp DESC")
    news_today = cur.fetchall()

    # --- WATCHLIST DE INTELIGENCIA ---
    watchlist = ["golpe", "coup", "nuclear", "ataque", "attack", "crisis", "misil", "missile", "dictator", "muertos", "dead", "emergencia"]
    alertas_criticas = []
    reporte_normal = []

    for reg, tit, sent, link in news_today:
        # Verificamos si el título contiene alguna palabra de la watchlist
        es_critica = any(word in tit.lower() for word in watchlist)
        
        linea = f"- **[{reg}]**: {tit} ([Link]({link}))"
        
        if es_critica or sent < -0.4:  # Si es crítica por palabra o por tensión extrema
            alertas_criticas.append(f"⚠️ **CRÍTICO**: {linea}")
        else:
            marca = "🔴" if sent < -0.1 else "🔹"
            reporte_normal.append(f"{marca} {linea}")

    # --- CONSTRUCCIÓN DEL DOCUMENTO MD ---
    content = f"---\ntitle: \"Informe de Inteligencia OSINT - {date_str}\"\ndate: \"{date_iso}\"\ntype: \"post\"\n# Imagen de cabecera automática para el post\nfeatured_image: \"images/header_intel.jpg\"\n---\n\n"
    
    if alertas_criticas:
        content += "## 🚨 ALERTAS DE ALTA PRIORIDAD\n"
        content += "> **Aviso**: El sistema ha detectado eventos de potencial inestabilidad global.\n\n"
        content += "\n".join(alertas_criticas) + "\n\n---\n\n"

    content += "### 📡 Monitorización Global Diaria\n"
    if reporte_normal:
        content += "\n".join(reporte_normal)
    else:
        content += "No se registraron eventos significativos adicionales."

    with open(filename, 'w') as f: 
        f.write(content)
    print(f"📄 Reporte generado con {len(alertas_criticas)} alertas críticas.")

