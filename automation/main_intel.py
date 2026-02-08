#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import feedparser
import sqlite3
import json
from datetime import datetime, timezone

# ===============================
# SENTIMIENTO (robusto)
# ===============================
try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()
    VADER_OK = True
except Exception:
    analyzer = None
    VADER_OK = False

def obtener_sentimiento(texto: str) -> float:
    if not VADER_OK:
        return 0.0
    try:
        return analyzer.polarity_scores(texto)["compound"]
    except Exception:
        return 0.0

# ===============================
# MODOS OPERATIVOS
# ===============================
INTEL_MODE = os.getenv("INTEL_MODE", "LOW").upper()
TEST_MODE  = os.getenv("INTEL_TEST", "0") == "1"

LOW_POWER = {
    "entries": 5,
    "latam_extended": False,
}

HIGH_INTEL = {
    "entries": 12,
    "latam_extended": True,
}

CFG = HIGH_INTEL if INTEL_MODE == "HIGH" else LOW_POWER

# ===============================
# RUTAS
# ===============================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(SCRIPT_DIR)

DB_PATH        = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT    = os.path.join(BASE_DIR, "blog/static/data/hotspots.json")
POSTS_OUTPUT   = os.path.join(BASE_DIR, "blog/content/post")
USA_LOG_CSV    = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_LOG_CSV  = os.path.join(BASE_DIR, "data/spain_trend.csv")

USER_AGENT = "IntelCenterBot/1.0 (DietPi LowPower)"

# ===============================
# FEEDS
# ===============================
FEEDS_SPAIN = [
    "https://elpais.com/rss/politica/portada.xml",
    "https://www.elmundo.es/e/rss/espana.xml",
]

DATOS_INTEL = {
    "USA_NORTE":      {"url": "https://www.theguardian.com/us-news/rss", "coord": [40.0, -100.0]},
    "Europa_DW":      {"url": "https://rss.dw.com/rdf/rss-en-top", "coord": [50.0, 10.0]},
    "Rusia_Eurasia":  {"url": "https://tass.com/rss/v2.xml", "coord": [60.0, 90.0]},
    "Medio_Oriente":  {"url": "https://www.aljazeera.com/xml/rss/all.xml", "coord": [25.0, 45.0]},
    "Asia_Nikkei":    {"url": "https://asia.nikkei.com/rss/feed/nar", "coord": [35.0, 135.0]},
    "Africa_Sahel":   {"url": "https://www.africanews.com/feed/", "coord": [15.0, 15.0]},
    "ESPAÑA":         {"url": "COMBO", "coord": [40.4, -3.7]},
    "LATAM_GENERAL":  {"url": "https://www.bbc.com/mundo/temas/america_latina/index.xml", "coord": [-15.0, -60.0]},
    "BRASIL":         {"url": "https://agenciabrasil.ebc.com.br/rss/ultimasnoticias/feed.xml", "coord": [-10.0, -55.0]},
    "ARGENTINA":      {"url": "https://www.telam.com.ar/rss2/politica.xml", "coord": [-34.0, -64.0]},
}

# FILTRO LATAM según CFG
if not CFG["latam_extended"]:
    if "ARGENTINA" in DATOS_INTEL:
        DATOS_INTEL.pop("ARGENTINA")
    if "BRASIL" in DATOS_INTEL:
        DATOS_INTEL.pop("BRASIL")

# ===============================
# KEYWORDS
# ===============================
KEYWORDS_CRITICAS = [
    "nuclear","missile","misil","attack","ataque","war","coup",
    "terror","military","militar","threat","sanción","tensión"
]

KEYWORDS_ELECTORALES = [
    "election","vote","ballot","voters",
    "elecciones","comicios","votación","campaña"
]

def calcular_score(titulo: str, sentimiento: float) -> float:
    t = titulo.lower()
    score = 1.0
    if any(k in t for k in KEYWORDS_CRITICAS):
        score += 2.5
    if any(k in t for k in KEYWORDS_ELECTORALES):
        score += 1.5
    if sentimiento < -0.3:
        score += 1.0
    return round(score, 2)

# ===============================
# LOG CSV
# ===============================
def registrar_tendencia(path: str, valor: float, fecha: str):
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("timestamp,avg_sentiment\n")
    with open(path, "a") as f:
        f.write(f"{fecha},{round(valor,4)}\n")

# ===============================
# MAIN
# ===============================
def ejecutar():
    print("=" * 60)
    print(f"INTEL CENTER | MODE={INTEL_MODE} | TEST={TEST_MODE}")
    print(f"Sentiment engine: {'VADER' if VADER_OK else 'NEUTRAL'}")
    print("=" * 60)

    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    os.makedirs(POSTS_OUTPUT, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur  = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            region TEXT,
            title TEXT,
            link TEXT UNIQUE,
            sentimiento REAL,
            score REAL
        )
    """)

    if TEST_MODE:
        print("[TEST] No limpieza de histórico")
    else:
        cur.execute("DELETE FROM news WHERE timestamp < datetime('now','-7 days')")

    ahora = datetime.now(timezone.utc)
    fecha_str = ahora.strftime("%Y-%m-%d %H:%M")
    total = 0

    for region, info in DATOS_INTEL.items():
        feeds = FEEDS_SPAIN if info["url"] == "COMBO" else [info["url"]]
        for url in feeds:
            parsed = feedparser.parse(url, agent=USER_AGENT)
            entries = parsed.entries[:CFG["entries"]]
            for e in entries:
                title = getattr(e, "title", "").strip()
                link  = getattr(e, "link", "")
                if not title or not link:
                    continue
                sent = obtener_sentimiento(title)
                score = calcular_score(title, sent)
                cur.execute("""
                    INSERT OR IGNORE INTO news(region,title,link,sentimiento,score)
                    VALUES (?,?,?,?,?)
                """, (region, title, link, sent, score))
                total += 1

    conn.commit()

    # ===============================
    # RADARES
    # ===============================
    def avg(region):
        cur.execute("""
            SELECT AVG(sentimiento)
            FROM news
            WHERE region=? AND timestamp > datetime('now','-24 hours')
        """, (region,))
        return cur.fetchone()[0] or 0.0

    registrar_tendencia(USA_LOG_CSV, avg("USA_NORTE"), fecha_str)
    registrar_tendencia(SPAIN_LOG_CSV, avg("ESPAÑA"), fecha_str)

    # ===============================
    # MAPA
    # ===============================
    cur.execute("""
        SELECT region, COUNT(*) as ct, AVG(sentimiento) as s
        FROM news
        WHERE timestamp > datetime('now','-24 hours')
        GROUP BY region
    """)

    hotspots = []
    for r, ct, s in cur.fetchall():
        if r not in DATOS_INTEL:
            continue
        color = "#f1c40f"  # neutro
        if s < -0.05:
            color = "#ff4b2b"
        intensity = min(round(ct * (1 + abs(s))), 10)
        hotspots.append({
            "name": r,
            "lat": DATOS_INTEL[r]["coord"][0],
            "lon": DATOS_INTEL[r]["coord"][1],
            "intensity": intensity,
            "color": color,
            "sentiment_index": round(s, 2)
        })

    with open(JSON_OUTPUT, "w") as f:
        json.dump(hotspots, f, indent=4)

    print(f"[OK] JSON hotspots generado con {len(hotspots)} regiones")
    print(f"[OK] Artículos procesados: {total}")

if __name__ == "__main__":
    ejecutar()
