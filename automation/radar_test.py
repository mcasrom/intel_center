import sqlite3
import os
import json

# Rutas seguras (ajustadas a tu Odroid)
DB_PATH = "/home/dietpi/intel_center_odroid/data/news.db"
# Lo sacamos a una carpeta de TEST para no tocar la producción
TEST_JSON = "/home/dietpi/intel_center_odroid/blog/static/data/radar_test.json"

def test_radar():
    # Asegurar que la carpeta existe sin borrar nada
    os.makedirs(os.path.dirname(TEST_JSON), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # Solo leemos los últimos 7 días
    cur.execute("SELECT region, AVG(sentimiento) FROM news WHERE timestamp > datetime('now','-7 days') AND sentimiento != 0.0 GROUP BY region")
    rows = cur.fetchall()
    conn.close()

    data = {
        "labels": [r[0] for r in rows],
        "values": [round((1 - (r[1] or 0)) * 50) for r in rows]
    }

    with open(TEST_JSON, "w") as f:
        json.dump(data, f)
    print(f"Test JSON generado en: {TEST_JSON}")

if __name__ == "__main__":
    test_radar()
