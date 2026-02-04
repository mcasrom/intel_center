import sqlite3
import json
import re
from collections import Counter
from nltk.corpus import stopwords
from config.settings import DB_PATH, MAP_DATA_JSON

# Coordenadas estratégicas para el mapa
GEO_COORDS = {
    "Rusia_Eurasia": [55.75, 37.61],
    "Medio_Oriente": [25.27, 51.53],
    "Asia_Nikkei": [35.68, 139.76]
}

def process_trends():
    print("🧠 Analizando titulares geopolíticos...")
    
    # Asegurar que la carpeta de salida para Hugo existe
    MAP_DATA_JSON.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        
        # Consultar noticias del último día
        cursor.execute("SELECT region, title FROM news WHERE timestamp > datetime('now', '-1 day')")
        rows = cursor.fetchall()
        
        stop_words = set(stopwords.words('english'))
        stop_words.update(['says', 'agency', 'discuss', 'talks', 'year', 'could', 'would', 'also'])

        results = []
        
        for region, coords in GEO_COORDS.items():
            # Filtrar títulos de esta región
            titles = [row[1].lower() for row in rows if row[0] == region]
            
            if not titles:
                continue
                
            # Limpieza y conteo de palabras
            all_text = " ".join(titles)
            words = re.findall(r'\b[a-z]{4,}\b', all_text)
            filtered = [w for w in words if w not in stop_words]
            
            top_keywords = Counter(filtered).most_common(5)
            
            results.append({
                "region": region,
                "lat": coords[0],
                "lon": coords[1],
                "intensity": len(titles),
                "keywords": top_keywords
            })
            print(f"📊 {region}: {len(titles)} noticias procesadas.")

        # Guardar el JSON para Leaflet
        with open(MAP_DATA_JSON, 'w') as f:
            json.dump(results, f, indent=2)
            
        conn.close()
        print(f"✅ JSON generado en: {MAP_DATA_JSON}")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    process_trends()
