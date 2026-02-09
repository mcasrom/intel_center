#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, feedparser, sqlite3, json, pytz
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = "/home/dietpi/intel_center_odroid"
# Apuntamos a la base de datos que comprobamos que tiene el "oro" (los sentimientos)
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
JSON_OUTPUT = os.path.join(BASE_DIR, "blog/data/hotspots.json")

# Generación dinámica del nombre del informe para que no siempre sea el mismo archivo
ahora_utc = datetime.now()
nombre_informe = ahora_utc.strftime("%Y-%m-%d") + "-informe.md"
INFORME_MD = os.path.join(BASE_DIR, f"blog/content/post/{nombre_informe}")

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

BUSQUEDA_LIDERES = {
    "Donald Trump": ["trump", "potus", "maga"],
    "Vladimir Putin": ["putin", "kremlin"],
    "Xi Jinping": ["xi jinping", "jinping", "beijing"],
    "Pedro Sánchez": ["sánchez", "moncloa"],
    "Javier Milei": ["milei", "casa rosada"]
}

def ejecutar():
    # Conectamos a la DB correcta
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Aseguramos que la tabla news tenga la columna 'sentimiento' (con 'o')
    cur.execute("""
        CREATE TABLE IF NOT EXISTS news 
        (region TEXT, title TEXT, link TEXT UNIQUE, sentimiento REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)
    """)

    alertas, electoral, resumen, lideres = [], [], [], []

    # 1. FETCH Y CLASIFICACIÓN
    for reg, url in FEEDS.items():
        feed = feedparser.parse(url)
        for e in feed.entries[:12]:
            title = e.title
            link = e.link
            low_title = title.lower()
            
            # A. Detección de Líderes
            encontrado_lider = False
            for nombre, claves in BUSQUEDA_LIDERES.items():
                if any(x in low_title for x in claves):
                    lideres.append(f"👤 **{nombre}**: {title} ([Link]({link}))")
                    encontrado_lider = True
                    break

            if not encontrado_lider:
                if any(x in low_title for x in ["war", "military", "conflict", "attack", "nuclear", "missile"]):
                    alertas.append(f"🚩 [ALERTA] {reg}: {title} ([Link]({link}))")
                elif any(x in low_title for x in ["election", "voto", "campaña", "electoral", "pp", "psoe"]):
                    electoral.append(f"🗳️ [ELECTORAL] {reg}: {title} ([Link]({link}))")
                else:
                    resumen.append(f"[{reg}]: {title} ([Link]({link}))")

            # IMPORTANTE: No insertamos 0.0 si el link ya existe para no borrar el sentimiento real calculado
            cur.execute("INSERT OR IGNORE INTO news (region, title, link, sentimiento) VALUES (?,?,?,?)", (reg, title, link, 0.0))

    conn.commit()

    # 2. SENTIMIENTOS DINÁMICOS (Usando la columna 'sentimiento' confirmada)
    def get_avg(region):
        # Filtramos para que no cuente los 0.0 que son noticias nuevas sin procesar aún
        cur.execute("SELECT AVG(sentimiento) FROM news WHERE region=? AND sentimiento != 0.0 AND timestamp > datetime('now','-48 hours')", (region,))
        res = cur.fetchone()[0]
        return round(res if res is not None else 0.0, 4)

    s_usa, s_esp = get_avg("USA_NORTE"), get_avg("ESPAÑA")
    
    # Guardar en CSV para la gráfica (solo si hay datos nuevos)
    for csv_path, val in [(USA_CSV, s_usa), (SPAIN_CSV, s_esp)]:
        with open(csv_path, "a") as f: f.write(f"{fecha_s},{val}\n")

    # 3. GENERAR HOTSPOTS (JSON)
    hotspots = []
    cur.execute("SELECT region, AVG(sentimiento), COUNT(*) FROM news WHERE sentimiento != 0.0 AND timestamp > datetime('now','-24 hours') GROUP BY region")
    
    for r, sent, count in cur.fetchall():
        if r in COORDS:
            color_nodo = "#f1c40f" # Neutro
            if sent < -0.05: color_nodo = "#e74c3c" # Rojo
            elif sent > 0.05: color_nodo = "#2ecc71" # Verde

            hotspots.append({
                "name": r, "lat": COORDS[r][0], "lon": COORDS[r][1],
                "intensity": min(count, 15), "color": color_nodo,
                "sentiment_index": round(sent, 4)
            })
    
    with open(JSON_OUTPUT, "w") as j:
        json.dump(hotspots, j, indent=4)

    # 4. GENERAR INFORME MD (Corrigiendo la ruta de la imagen para GitHub y Local)
    with open(INFORME_MD, "w") as f:
        f.write(f'---\ntitle: "Monitor Intel: {fecha_s}"\ndate: {ahora.isoformat()}\n---\n\n')
        f.write("🛡️ ESTADO DEL NODO\n\n| Indicador | Valor |\n| :--- | :--- |\n")
        f.write(f"| STATUS | 🟢 OPERATIVO |\n| ÚLTIMA SYNC | {fecha_s} |\n| HARDWARE | Odroid-C2-Madrid |\n\n")
        f.write("📊 RADARES DE TENDENCIA\n\n| Región | Sentimiento |\n| :--- | :--- |\n")
        f.write(f"| 🇺🇸 USA | {s_usa} |\n| 🇪🇸 ESPAÑA | {s_esp} |\n\n")
        f.write("📈 Evolución de Tendencia\n\n")
        f.write("![Gráfica de Tendencias](/images/trend.png)\n\n") # Ruta absoluta para Hugo

        f.write("👤 MOVIMIENTOS DE LÍDERES MUNDIALES\n\n")
        if lideres:
            for l in lideres[:10]: f.write(f"{l}  \n")
        else:
            f.write("No se detectan movimientos directos de mandatarios clave.  \n")

        f.write("\n⚡ ALERTAS CRÍTICAS\n\n")
        if alertas:
            for a in alertas[:6]: f.write(f"{a}  \n")
        else:
            f.write("No se han detectado eventos críticos.  \n")

        f.write("\n🌍 RESUMEN GLOBAL\n\n")
        for r in resumen[:12]: f.write(f"{r}  \n")

    # --- MANTENIMIENTO ---
    cur.execute("DELETE FROM news WHERE timestamp < datetime('now','-15 days')")
    conn.commit()
    conn.close()

if __name__ == "__main__":
    ejecutar()
