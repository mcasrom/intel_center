import os, feedparser, sqlite3, json
from datetime import datetime, timedelta
from textblob import TextBlob

# --- CONFIGURACIÓN ---
BASE_DIR = os.path.expanduser("~/intel_center_test")
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT = os.path.join(BASE_DIR, "blog/content/post/")
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'

DATOS_INTEL = {
    "Rusia_Eurasia": {"url": "https://tass.com/rss/v2.xml", "coord": [60.0, 90.0]},
    "Medio_Oriente": {"url": "https://www.aljazeera.com/xml/rss/all.xml", "coord": [25.0, 45.0]},
    "Europa_DW": {"url": "https://rss.dw.com/rdf/rss-en-top", "coord": [50.0, 10.0]},
    "Asia_Nikkei": {"url": "https://asia.nikkei.com/rss/feed/nar", "coord": [35.0, 135.0]},
    "LATAM": {"url": "https://www.bbc.com/mundo/temas/america_latina/index.xml", "coord": [-15.0, -60.0]},
    "MEXICO": {"url": "https://www.jornada.com.mx/rss/ultimas.xml?v=1", "coord": [23.0, -102.0]},
    "USA_NORTE": {"url": "https://www.theguardian.com/us-news/rss", "coord": [40.0, -100.0]},
    "Australia": {"url": "https://www.abc.net.au/news/feed/51120/rss.xml", "coord": [-25.0, 133.0]},
    "Canada": {"url": "https://www.cbc.ca/cxml/rss/news/world", "coord": [60.0, -110.0]},
    "Groenlandia": {"url": "https://www.arctictoday.com/feed/", "coord": [72.0, -40.0]},
    "Africa_Sahel": {"url": "https://www.africanews.com/feed/", "coord": [15.0, 15.0]}
}

KEYWORDS_CRITICAS = [
    "nuclear", "misil", "missile", "atentado", "ataque", "attack", "guerra", "war",
    "golpe", "coup", "ciber", "cyber", "despliegue", "deployment", "frontera", "border",
    "cartel", "sicario", "sahel", "yihad", "jihad", "bombard", "militar", "military",
    "sancion", "sanction", "ultimatum", "amenaza", "threat"
]

def obtener_sentimiento(texto):
    """Analiza sentimiento intentando detectar idioma."""
    try:
        blob = TextBlob(texto)
        # Si el texto es lo suficientemente largo, intentamos ver si es inglés
        # TextBlob usa por defecto un analizador entrenado en inglés.
        return blob.sentiment.polarity
    except:
        return 0.0

def ejecutar():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(POSTS_OUTPUT, exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS news 
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                   timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
                   region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL)''')

    # --- 1. LIMPIEZA DE DATOS VIEJOS (Más de 7 días) ---
    cur.execute("DELETE FROM news WHERE timestamp < datetime('now', '-7 days')")
    print(f"🧹 Limpieza completada: {cur.rowcount} registros antiguos eliminados.")

    # --- 2. CAPTURA ---
    print("--- INICIANDO CAPTURA INTELIGENTE ---")
    for reg, info in DATOS_INTEL.items():
        f = feedparser.parse(info["url"], agent=USER_AGENT)
        if f.entries:
            for e in f.entries[:15]:
                pola = obtener_sentimiento(str(e.title))
                cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?, ?, ?, ?)", 
                            (reg, e.title, e.link, pola))
    conn.commit()

    ahora = datetime.now()
    fecha_str = ahora.strftime("%Y-%m-%d")
    
    # --- 3. GENERAR JSON PARA MAPA ---
    cur.execute("SELECT region, COUNT(*), AVG(sentimiento) FROM news WHERE timestamp > datetime('now', '-24 hours') GROUP BY region")
    hotspots = []
    for r, ct, s in cur.fetchall():
        if r in DATOS_INTEL:
            color = "#f1c40f"
            if s < -0.1: color = "#ff4b2b"
            elif s > 0.1: color = "#2ecc71"
            hotspots.append({
                "name": r, "lat": DATOS_INTEL[r]["coord"][0], "lon": DATOS_INTEL[r]["coord"][1],
                "intensity": ct, "color": color, "sentiment_index": round(s, 2)
            })
    with open(JSON_OUTPUT, 'w') as f:
        json.dump(hotspots, f, indent=4)

    # --- 4. GENERAR INFORME HUGO ---
    cur.execute("SELECT region, title, link FROM news WHERE timestamp > datetime('now', '-24 hours') ORDER BY timestamp DESC LIMIT 100")
    records = cur.fetchall()
    alertas, normales = [], []
    for reg, tit, link in records:
        if any(key in tit.lower() for key in KEYWORDS_CRITICAS):
            alertas.append(f"- 🚩 **[ALERTA] {reg}**: {tit} ([Link]({link}))")
        else:
            normales.append(f"- **[{reg}]**: {tit} ([Link]({link}))")

    with open(os.path.join(POSTS_OUTPUT, f"{fecha_str}-informe-inteligencia.md"), 'w') as f:
        f.write(f"---\ntitle: \"Monitor Global - {fecha_str}\"\ndate: {ahora.strftime('%Y-%m-%dT%H:%M:%S')}\ntype: \"post\"\n---\n\n")
        if alertas:
            f.write("## ⚡ ALERTAS DETECTADAS\n")
            f.write("\n".join(alertas) + "\n\n---\n\n")
        f.write("## 🌍 Actividad Reciente\n")
        f.write("\n".join(normales[:70]))

    conn.close()
    print(f"--- PROCESO FINALIZADO: {len(alertas)} alertas registradas ---")

if __name__ == "__main__":
    ejecutar()
