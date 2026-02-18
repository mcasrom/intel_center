#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import feedparser
import sqlite3
import json
import pytz
import glob
import logging
import sys
import time
from datetime import datetime

# --- VERIFICACIÓN DE DEPENDENCIAS ---
try:
    from sentiment_engine import analizar_sentimiento 
except ImportError:
    print("CRITICAL: El motor de sentimiento (sentiment_engine.py) no es accesible.")
    sys.exit(1)

# --- CONFIGURACIÓN DE LOGGING ---
LOG_FILE = "/home/dietpi/intel_center_odroid/data/intel_process.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(process)d] - %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)

# --- RUTAS ---
BASE_DIR = "/home/dietpi/intel_center_odroid"
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/data/hotspots.json")
POSTS_DIR = os.path.join(BASE_DIR, "blog/content/post/")
IMAGES_DIR = os.path.join(BASE_DIR, "blog/static/images/")

ahora_utc = datetime.now()
timestamp_img = ahora_utc.strftime("%y%m%d_%H%M") 
nombre_imagen_dinamica = f"{timestamp_img}_trend.png"

USA_CSV = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_CSV = os.path.join(BASE_DIR, "data/spain_trend.csv")
INDIA_CHINA_CSV = os.path.join(BASE_DIR, "data/india_china_core_trend.csv")

ZONA_LOCAL = pytz.timezone("Europe/Madrid")
ahora_local = datetime.now(ZONA_LOCAL)
fecha_s = ahora_local.strftime("%Y-%m-%d %H:%M")

FEEDS = {
    "USA_NORTE": "https://www.theguardian.com/us-news/rss",
    "ESPAÑA": "https://elpais.com/rss/politica/portada.xml",
    "ARGENTINA": "https://www.clarin.com/rss/politica/",
    "BRASIL": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml",
    "Europa_DW": "https://rss.dw.com/rdf/rss-en-top",
    "Rusia_Eurasia": "https://tass.com/rss/v2.xml",
    "Medio_Oriente": "https://www.aljazeera.com/xml/rss/all.xml",
    "Asia_Nikkei": "https://asia.nikkei.com/rss/feed/nar",
    "Africa_Sahel": "https://www.africanews.com/feed/",
    "INDIA_CORE": "https://www.thehindu.com/news/national/feeder/default.rss",
    "CHINA_CORE": "https://asia.nikkei.com/rss/feed/nar"
}

COORDS = {
    "USA_NORTE": [40.0, -100.0], "ESPAÑA": [40.4, -3.7], "ARGENTINA": [-34.0, -64.0],
    "BRASIL": [-10.0, -55.0], "Europa_DW": [50.0, 10.0], "Rusia_Eurasia": [60.0, 90.0],
    "Medio_Oriente": [25.0, 45.0], "Asia_Nikkei": [35.0, 135.0], "Africa_Sahel": [15.0, 15.0],
    "INDIA_CORE": [28.6, 77.2], "CHINA_CORE": [39.9, 116.4]
}

BUSQUEDA_LIDERES = {
    "Donald Trump": ["trump", "potus", "maga"],
    "Vladimir Putin": ["putin", "kremlin"],
    "Xi Jinping": ["xi jinping", "jinping", "beijing"],
    "Pedro Sánchez": ["sánchez", "moncloa"],
    "Javier Milei": ["milei", "casa rosada"],
    "Narendra Modi": ["modi", "delhi"]
}

def ejecutar():
    logging.info("--- INICIO DE CICLO OPERATIVO OSINT ---")
    start_time = time.time()
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS news (region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

        alertas, electoral, resumen, lideres = [], [], [], []

        for reg, url in FEEDS.items():
            logging.info(f"Escaneando vector: {reg}")
            try:
                feed = feedparser.parse(url)
                for e in feed.entries[:15]:
                    title = e.title
                    link = e.link
                    low_title = title.lower()
                    puntaje = analizar_sentimiento(title)
                    
                    cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?,?,?,?)", (reg, title, link, puntaje))

                    encontrado_lider = False
                    for nombre, claves in BUSQUEDA_LIDERES.items():
                        if any(x in low_title for x in claves):
                            lideres.append(f"👤 **{nombre}**: {title} — [Noticia]({link})")
                            encontrado_lider = True
                            break

                    if not encontrado_lider:
                        if any(x in low_title for x in ["war", "military", "conflict", "attack", "nuclear", "missile", "defense"]):
                            alertas.append(f"🚩 [MILITAR] **{reg}**: {title} — [Fuente]({link})")
                        elif any(x in low_title for x in ["election", "voto", "campaña", "electoral", "psoe", "pp", "vox"]):
                            electoral.append(f"🗳️ [ELECTORAL] **{reg}**: {title} — [Fuente]({link})")
                        else:
                            # FORMATO UNIFICADO Y ÚNICO
                            resumen.append(f"● **{reg}**: {title} — [Leer más]({link})")
            
            except Exception as e_feed:
                logging.error(f"Error en feed {reg}: {e_feed}")

        conn.commit()

        # --- FASE 2: PROCESAMIENTO TENDENCIAS ---
        def get_avg(region_list):
            placeholders = ','.join(['?'] * len(region_list))
            cur.execute(f"SELECT AVG(sentimiento) FROM news WHERE region IN ({placeholders}) AND sentimiento != 0.0 AND timestamp > datetime('now','-12 hours')", region_list)
            res = cur.fetchone()[0]
            return round(res if res is not None else 0.0, 4)

        s_usa, s_esp, s_ic = get_avg(["USA_NORTE"]), get_avg(["ESPAÑA"]), get_avg(["INDIA_CORE", "CHINA_CORE"])
        
        for csv_path, val in [(USA_CSV, s_usa), (SPAIN_CSV, s_esp), (INDIA_CHINA_CSV, s_ic)]:
            if not os.path.exists(csv_path):
                with open(csv_path, "w") as f: f.write("timestamp,val\n")
            with open(csv_path, "a") as f: f.write(f"{fecha_s},{val}\n")

        # --- FASE 3: HOTSPOTS ---
        hotspots_data = []
        cur.execute("SELECT region, AVG(sentimiento), COUNT(*) FROM news WHERE sentimiento != 0.0 AND timestamp > datetime('now','-72 hours') GROUP BY region")
        db_results = {r: (s, c) for r, s, c in cur.fetchall()}

        for r in COORDS:
            sent, count = db_results.get(r, (0.0, 2))
            color_node = "#f1c40f"
            if sent < -0.05: color_node = "#e74c3c"
            elif sent > 0.05: color_node = "#2ecc71"
            hotspots_data.append({"name": r, "lat": COORDS[r][0], "lon": COORDS[r][1], "intensity": min(max(count, 3), 15), "color": color_node, "sentiment_index": round(sent, 4)})
        
        with open(JSON_OUTPUT, "w") as j: json.dump(hotspots_data, j, indent=4)

        # --- FASE 4: INFORME MD ---
        nombre_diario = f"{timestamp_img}-noticias.md"
        DIARIO_PATH = os.path.join(POSTS_DIR, nombre_diario)

        resumen_balanceado = []
        for reg_key in FEEDS.keys():
            especificas = [linea for linea in resumen if f"**{reg_key}**" in linea]
            resumen_balanceado.extend(especificas[:3])

        ya_incluidas = set(resumen_balanceado)
        for linea in resumen:
            if linea not in ya_incluidas and len(resumen_balanceado) < 35:
                resumen_balanceado.append(linea)

        with open(DIARIO_PATH, "w") as f:
            f.write("---\ntitle: \"INTEL REPORT: " + ahora_local.strftime('%d/%m/%Y %H:%M') + "\"\ndate: " + ahora_utc.isoformat() + "\nreport_types: [\"Diario\"]\nstatus: \"Operational\"\n---\n\n")
            f.write("### ⚡ RESUMEN OPERATIVO\nAnálisis en Odroid-C2.\n\n")
            f.write("#### 📊 RADARES DE TENDENCIA\n| Región | Sentiment |\n| :--- | :--- |\n| 🇺🇸 USA | " + str(s_usa) + " |\n| 🇪🇸 ESPAÑA | " + str(s_esp) + " |\n| 🌏 INDIA-CHINA | " + str(s_ic) + " |\n\n")
            f.write(f"![Tendencias](/images/{nombre_imagen_dinamica})\n\n")
            f.write("#### 👤 LÍDERES\n" + "\n".join(lideres[:12]) + "\n\n")
            f.write("#### 🚩 MILITAR\n" + "\n".join(alertas[:10]) + "\n\n")
            f.write("#### 🌍 PANORAMA GLOBAL\n\n" + "\n".join(resumen_balanceado) + "\n")

        # --- FASE 5: HIGIENE ---
        archivos_viejos = sorted(glob.glob(os.path.join(POSTS_DIR, "*-noticias.md")), reverse=True)
        if len(archivos_viejos) > 20:
            for f_old in archivos_viejos[20:]: os.remove(f_old)

        cur.execute("DELETE FROM news WHERE timestamp < datetime('now','-15 days')")
        conn.commit()
        conn.close()
        logging.info(f"--- FIN (Duración: {round(time.time() - start_time, 2)}s) ---")

    except Exception as e_global:
        logging.critical(f"FALLO: {e_global}")

if __name__ == "__main__":
    ejecutar()
