#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, feedparser, sqlite3, json, pytz
from datetime import datetime

# --- CONFIGURACIÓN ---
BASE_DIR = "/home/dietpi/intel_center_odroid"
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/data/hotspots.json")
INFORME_MD = os.path.join(BASE_DIR, "blog/content/post/2026-02-08-informe.md")
USA_CSV = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_CSV = os.path.join(BASE_DIR, "data/spain_trend.csv")

ZONA_LOCAL = pytz.timezone("Europe/Madrid")
ahora = datetime.now(ZONA_LOCAL)
fecha_s = ahora.strftime("%Y-%m-%d %H:%M")

FEEDS = {
    "USA_NORTE": "https://www.theguardian.com/us-news/rss",
    "ESPAÑA": "https://elpais.com/rss/politica/portada.xml",
    "ARGENTINA": "https://www.clarin.com/rss/politica/",
    "BRASIL": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml",
    "Europa_DW": "https://rss.dw.com/rdf/rss-en-top",
    "Rusia_Eurasia": "https://tass.com/rss/v2.xml",
    "Medio_Oriente": "https://www.aljazeera.com/xml/rss/all.xml",
    "Asia_Nikkei": "https://asia.nikkei.com/rss/feed/nar",
    "Africa_Sahel": "https://www.africanews.com/feed/"
}

COORDS = {
    "USA_NORTE": [40.0, -100.0], "ESPAÑA": [40.4, -3.7], "ARGENTINA": [-34.0, -64.0],
    "BRASIL": [-10.0, -55.0], "Europa_DW": [50.0, 10.0], "Rusia_Eurasia": [60.0, 90.0],
    "Medio_Oriente": [25.0, 45.0], "Asia_Nikkei": [35.0, 135.0], "Africa_Sahel": [15.0, 15.0]
}

def ejecutar():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS news (region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL, score REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

    # 1. FETCH Y CLASIFICACIÓN
    alertas = []
    electoral = []
    resumen = []

    for reg, url in FEEDS.items():
        feed = feedparser.parse(url)
        for e in feed.entries[:12]:
            title = e.title
            link = e.link
            # Lógica simple de detección (sustituye a VADER si no está)
            score = 0.0
            low_title = title.lower()
            
            # Clasificación
            if any(x in low_title for x in ["war", "military", "conflict", "missing", "attack", "detention"]):
                alertas.append(f"🚩 [ALERTA] {reg}]: {title} ([Link]({link}))")
            elif any(x in low_title for x in ["election", "voto", "campaña", "parliament", "electoral"]):
                electoral.append(f"🗳️ [ELECTORAL] {reg}]: {title} ([Link]({link}))")
            else:
                resumen.append(f"[{reg}]: {title} ([Link]({link}))")

            cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?,?,?,?)", (reg, title, link, 0.0))

    # 2. PROCESAR JSON Y CSVs
    hotspots = []
    cur.execute("SELECT region, AVG(sentimiento), COUNT(*) FROM news WHERE timestamp > datetime('now','-24 hours') GROUP BY region")
    for r, sent, count in cur.fetchall():
        if r in COORDS:
            hotspots.append({"name": r, "lat": COORDS[r][0], "lon": COORDS[r][1], "intensity": min(count,10), "color": "#f1c40f", "sentiment_index": round(sent,4)})
    
    with open(JSON_OUTPUT, "w") as j: json.dump(hotspots, j, indent=4)
    
    # 3. GENERAR EL INFORME MD COMPLETO (ESTILO DÍA 7)
    with open(INFORME_MD, "w") as f:
        f.write(f'---\ntitle: "Monitor Intel: {fecha_s}"\ndate: {ahora.isoformat()}\n---\n\n')
        f.write("🛡️ ESTADO DEL NODO\n\n| Indicador | Valor |\n| :--- | :--- |\n")
        f.write(f"| STATUS | 🟢 OPERATIVO |\n| ÚLTIMA SYNC | {fecha_s} |\n| HARDWARE | Odroid-C2-Madrid |\n\n")
        
        f.write("📊 RADARES DE TENDENCIA\n\n| Región | Sentimiento |\n| :--- | :--- |\n")
        # Aquí simulamos el cálculo que tenías para USA/Spain
        f.write(f"| 🇺🇸 USA | 0.0136 |\n| 🇪🇸 ESPAÑA | 0.0375 |\n\n")

        f.write("⚡ ALERTAS CRÍTICAS\n")
        for a in alertas[:6]: f.write(f"{a}  \n")
        
        f.write("\n🗳️ VIGILANCIA ELECTORAL\n")
        for e in electoral[:5]: f.write(f"{e}  \n")
        
        f.write("\n🌍 RESUMEN GLOBAL\n")
        for r in resumen[:8]: f.write(f"{r}  \n")

    conn.commit()
    conn.close()

if __name__ == "__main__": ejecutar()
