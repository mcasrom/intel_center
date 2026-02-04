import feedparser
import sqlite3
import os
from config.settings import DB_PATH

# Identidad de navegador para evitar bloqueos
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'

FEEDS = {
    "Rusia_Eurasia": "https://tass.com/rss/v2.xml",
    "Global_Reuters": "https://www.reutersagency.com/feed/",
    "Medio_Oriente": "https://www.aljazeera.com/xml/rss/all.xml",
    "Europa_DW": "https://www.dw.com/en/top-stories/s-9097/rss",
    "Asia_Nikkei": "https://asia.nikkei.com/rss/feed/nar"
}

def init_and_fetch():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            region TEXT, title TEXT, link TEXT UNIQUE
        )
    ''')

    for region, url in FEEDS.items():
        print(f"📥 Intentando capturar {region}...")
        try:
            # Aquí pasamos el User-Agent para "engañar" al servidor
            feed = feedparser.parse(url, agent=USER_AGENT)
            
            if not feed.entries:
                print(f"⚠️ {region}: No se recibieron entradas (posible bloqueo o feed vacío).")
                continue

            count = 0
            for entry in feed.entries:
                cursor.execute("INSERT OR IGNORE INTO news (region, title, link) VALUES (?, ?, ?)",
                               (region, entry.title, entry.link))
                if cursor.rowcount > 0:
                    count += 1
            print(f"✅ {region}: {count} nuevas entradas.")
        except Exception as e:
            print(f"❌ Error en {region}: {e}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_and_fetch()
