#!/usr/bin/env python3
import feedparser
import requests

# Diccionario de Test para Zonas de Alto Interés (M3.4)
TEST_FEEDS = {
    "TURQUÍA_SABAH": "https://www.dailysabah.com/rss/main.xml",
    "IRÁN_P_TV": "https://www.presstv.ir/rss", 
    "COREA_NORTE_KCNA": "https://kcnawatch.org/feed/", # Mirror estable de KCNA
    "MAR_CHINA_SCMP": "https://www.scmp.com/rss/91/feed", # South China Morning Post (Seguridad Asia)
    "UCRANIA_UKRINFORM": "https://www.ukrinform.net/rss/block-lastnews"
}

def test_source(name, url):
    print(f"\n--- Probando Vector: {name} ---")
    try:
        # Simulamos un navegador moderno para evitar bloqueos regionales
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"❌ FALLO DE RED: Código HTTP {response.status_code}")
            return

        feed = feedparser.parse(response.content)
        
        if len(feed.entries) == 0:
            print(f"⚠️  CONEXIÓN OK pero 0 NOTICIAS. Es posible que el XML sea incompatible.")
        else:
            print(f"✅ ÉXITO: {len(feed.entries)} noticias detectadas.")
            entry = feed.entries[0]
            print(f"   Último Titular: {entry.get('title', 'Sin título')[:60]}...")
            print(f"   Fecha: {entry.get('published', 'Sin fecha')}")
            
    except Exception as e:
        print(f"🚫 ERROR CRÍTICO: {str(e)}")

if __name__ == "__main__":
    print("=== LABORATORIO DE VECTORES GEOPOLÍTICOS (SIN RIESGO) ===")
    for name, url in TEST_FEEDS.items():
        test_source(name, url)
