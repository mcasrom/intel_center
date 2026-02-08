#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, feedparser, sqlite3, json, pytz
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
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
    cur.execute("CREATE TABLE IF NOT EXISTS news (region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

    alertas, electoral, resumen = [], [], []

    # 1. FETCH Y CLASIFICACIÓN
    for reg, url in FEEDS.items():
        feed = feedparser.parse(url)
        for e in feed.entries[:12]:
            title = e.title
            link = e.link
            low_title = title.lower()
            
            # Clasificación por palabras clave
            if any(x in low_title for x in ["war", "military", "conflict", "missing", "attack", "detention", "nuclear", "bomb", "missile"]):
                alertas.append(f"🚩 [ALERTA] {reg}]: {title} ([Link]({link}))")
            elif any(x in low_title for x in ["election", "voto", "campaña", "parliament", "electoral", "voter", "sanchez", "trump", "pp", "psoe"]):
                electoral.append(f"🗳️ [ELECTORAL] {reg}]: {title} ([Link]({link}))")
            else:
                resumen.append(f"[{reg}]: {title} ([Link]({link}))")

            cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?,?,?,?)", (reg, title, link, 0.0))

    conn.commit()

    # 2. SENTIMIENTOS DINÁMICOS
    def get_avg(region):
        cur.execute("SELECT AVG(sentimiento) FROM news WHERE region=? AND timestamp > datetime('now','-24 hours')", (region,))
        return round(cur.fetchone()[0] or 0.0, 4)

    s_usa, s_esp = get_avg("USA_NORTE"), get_avg("ESPAÑA")
    for csv_path, val in [(USA_CSV, s_usa), (SPAIN_CSV, s_esp)]:
        with open(csv_path, "a") as f: f.write(f"{fecha_s},{val}\n")

    # 3. GENERAR INFORME MD (CON TODOS LOS SEPARADORES)
    with open(INFORME_MD, "w") as f:
        f.write(f'---\ntitle: "Monitor Intel: {fecha_s}"\ndate: {ahora.isoformat()}\n---\n\n')
        
        f.write("🛡️ ESTADO DEL NODO\n\n| Indicador | Valor |\n| :--- | :--- |\n")
        f.write(f"| STATUS | 🟢 OPERATIVO |\n| ÚLTIMA SYNC | {fecha_s} |\n| HARDWARE | Odroid-C2-Madrid |\n\n")
        
        f.write("📊 RADARES DE TENDENCIA\n\n| Región | Sentimiento |\n| :--- | :--- |\n")
        f.write(f"| 🇺🇸 USA | {s_usa} |\n| 🇪🇸 ESPAÑA | {s_esp} |\n\n")

        f.write("📈 Evolución de Tendencia\n\n")
        f.write("![Gráfica de Tendencias](/images/trend.png)\n\n")

        f.write("⚡ ALERTAS CRÍTICAS\n\n")
        if alertas:
            for a in alertas[:6]: f.write(f"{a}  \n")
        else:
            f.write("No se han detectado eventos críticos en las últimas horas.  \n")
        
        f.write("\n🗳️ VIGILANCIA ELECTORAL\n\n")
        if electoral:
            for e in electoral[:5]: f.write(f"{e}  \n")
        else:
            f.write("Sin novedades electorales en el radar actual.  \n")
        
        f.write("\n🌍 RESUMEN GLOBAL\n\n")
        for r in resumen[:12]: f.write(f"{r}  \n")

    conn.close()

if __name__ == "__main__": ejecutar()
