#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import feedparser
import sqlite3
import json
from datetime import datetime
import pytz

# ===============================
# SENTIMIENTO (VADER) - NO SE TOCA
# ===============================
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    VADER_OK = True
except Exception:
    analyzer = None
    VADER_OK = False

def obtener_sentimiento(texto: str) -> float:
    if not VADER_OK: return 0.0
    try:
        return analyzer.polarity_scores(texto)["compound"]
    except Exception:
        return 0.0

# ===============================
# CONFIGURACIÓN Y RUTAS (MODO HIGH)
# ===============================
INTEL_MODE = "HIGH"
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)

DB_PATH        = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT    = os.path.join(BASE_DIR, "blog/data/hotspots.json")
INFORME_MD     = os.path.join(BASE_DIR, "blog/content/post/2026-02-08-informe.md")
USA_LOG_CSV    = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_LOG_CSV  = os.path.join(BASE_DIR, "data/spain_trend.csv")

USER_AGENT = "IntelCenterBot/1.0 (DietPi HighPerformance)"

DATOS_INTEL = {
    "USA_NORTE":      {"url": "https://www.theguardian.com/us-news/rss", "coord": [40.0, -100.0]},
    "Europa_DW":      {"url": "https://rss.dw.com/rdf/rss-en-top", "coord": [50.0, 10.0]},
    "Rusia_Eurasia":  {"url": "https://tass.com/rss/v2.xml", "coord": [60.0, 90.0]},
    "Medio_Oriente":  {"url": "https://www.aljazeera.com/xml/rss/all.xml", "coord": [25.0, 45.0]},
    "Asia_Nikkei":    {"url": "https://asia.nikkei.com/rss/feed/nar", "coord": [35.0, 135.0]},
    "Africa_Sahel":   {"url": "https://www.africanews.com/feed/", "coord": [15.0, 15.0]},
    "ESPAÑA":          {"url": "https://elpais.com/rss/politica/portada.xml", "coord": [40.4, -3.7]},
    "LATAM_GENERAL":  {"url": "https://www.bbc.com/mundo/temas/america_latina/index.xml", "coord": [-15.0, -60.0]},
    "BRASIL":          {"url": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml", "coord": [-10.0, -55.0]},
    "ARGENTINA":       {"url": "https://www.clarin.com/rss/politica/", "coord": [-34.0, -64.0]},
}

KEYWORDS_CRITICAS = ["nuclear","missile","misil","attack","ataque","war","coup","terror","militar","tension"]

def calcular_score(titulo: str, sentimiento: float) -> float:
    t = titulo.lower()
    score = 1.0
    if any(k in t for k in KEYWORDS_CRITICAS): score += 2.5
    if sentimiento < -0.3: score += 1.0
    return round(score, 2)

def registrar_tendencia(path: str, valor: float, fecha: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f: f.write("timestamp,avg_sentiment\n")
    with open(path, "a") as f: f.write(f"{fecha},{round(valor,4)}\n")

# ===============================
# PROCESAMIENTO
# ===============================
def ejecutar():
    ZONA_LOCAL = pytz.timezone("Europe/Madrid")
    ahora = datetime.now(ZONA_LOCAL)
    fecha_str = ahora.strftime("%Y-%m-%d %H:%M")
    
    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS news (id INTEGER PRIMARY KEY, region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL, score REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)")

    print(f"[*] Procesando feeds en modo {INTEL_MODE}...")
    
    for region, info in DATOS_INTEL.items():
        parsed = feedparser.parse(info["url"], agent=USER_AGENT)
        # Modo HIGH: 12 artículos
        for e in parsed.entries[:12]:
            title = getattr(e, "title", "")
            link = getattr(e, "link", "")
            sent = obtener_sentimiento(title)
            score = calcular_score(title, sent)
            cur.execute("INSERT OR IGNORE INTO news(region,title,link,sentimiento,score) VALUES (?,?,?,?,?)", 
                        (region, title, link, sent, score))
    conn.commit()

    # TENDENCIAS (PARA LOS GRÁFICOS)
    def avg_s(reg):
        cur.execute("SELECT AVG(sentimiento) FROM news WHERE region=? AND timestamp > datetime('now','-24 hours')", (reg,))
        return cur.fetchone()[0] or 0.0

    registrar_tendencia(USA_LOG_CSV, avg_s("USA_NORTE"), fecha_str)
    registrar_tendencia(SPAIN_LOG_CSV, avg_s("ESPAÑA"), fecha_str)

    # GENERAR JSON HOTSPOTS
    cur.execute("SELECT region, COUNT(*), AVG(sentimiento) FROM news WHERE timestamp > datetime('now','-24 hours') GROUP BY region")
    hotspots = []
    for r, ct, s in cur.fetchall():
        if r not in DATOS_INTEL: continue
        color = "#f1c40f" if s >= -0.1 else "#ff4b2b"
        hotspots.append({
            "name": r, "lat": DATOS_INTEL[r]["coord"][0], "lon": DATOS_INTEL[r]["coord"][1],
            "intensity": min(ct, 10), "color": color, "sentiment_index": round(s, 2)
        })

    with open(JSON_OUTPUT, "w") as f:
        json.dump(hotspots, f, indent=4)

    # ACTUALIZAR INFORME MD (MATA LAS 15:05)
    with open(INFORME_MD, "w") as f:
        f.write(f'---\ntitle: "Monitor Intel: {fecha_str}"\ndate: {ahora.isoformat()}\n---\n\n')
        f.write(f"| **ÚLTIMA SYNC** | `{fecha_str}` |\n")
        f.write("|---|---|\n")
        f.write(f"| **ESTADO** | `OPERATIVO` |\n")
        f.write(f"| **LATAM** | `ACTIVO (ARG/BRA)` |\n\n")
        f.write("## Análisis de Situación\n\nLos hotspots y gráficos de tendencia han sido actualizados con los últimos feeds.")

    conn.close()
    print(f"✅ Sincronización completa a las {fecha_str}")

if __name__ == "__main__":
    ejecutar()
