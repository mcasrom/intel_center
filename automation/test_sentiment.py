import sqlite3
import os

DB_PATH = "/home/dietpi/intel_center_odroid/data/news.db"
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

for pais in ['ARGENTINA', 'BRASIL']:
    cur.execute("SELECT AVG(sentimiento), COUNT(*) FROM news WHERE region=? AND timestamp > datetime('now', '-24 hours')", (pais,))
    res = cur.fetchone()
    print(f"--- {pais} ---")
    print(f"Promedio: {res[0] if res[0] else 0:.4f}")
    print(f"Artículos analizados: {res[1]}")

conn.close()
