import json
import datetime
from config.settings import MAP_DATA_JSON, HUGO_DIR

def generate_daily_post():
    print("✍️ Generando reporte Markdown para el blog...")
    
    # 1. Cargar los datos frescos del análisis
    with open(MAP_DATA_JSON, 'r') as f:
        hotspots = json.load(f)
    
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    post_path = HUGO_DIR / "content" / "posts" / f"intel-{date_str}.md"
    
    # Asegurar que la carpeta de posts existe
    post_path.parent.mkdir(parents=True, exist_ok=True)
    
    # 2. Construir el contenido
    content = f"""---
title: "Informe Geopolítico Diario: {date_str}"
date: {datetime.datetime.now().isoformat()}
draft: false
tags: ["inteligencia", "automatizado", "odroid-c2"]
---

## Resumen de Actividad Global

El sistema de análisis de **El Mapa y El Código** ha procesado las últimas noticias de fuentes estratégicas (TASS, Al Jazeera, Nikkei).

### Análisis por Región
"""
    
    for h in hotspots:
        keywords_str = ", ".join([f"**{k[0]}** ({k[1]})" for k in h['keywords']])
        content += f"\n#### 📍 {h['region']}\n"
        content += f"- **Intensidad de noticias:** {h['intensity']}\n"
        content += f"- **Conceptos clave:** {keywords_str}\n"

    content += """
---
*Informe generado automáticamente por el núcleo de análisis en Odroid C2 (DietPi Linux).*
"""

    # 3. Escribir el archivo
    with open(post_path, 'w') as f:
        f.write(content)
    
    print(f"✅ Post creado en: {post_path}")

if __name__ == "__main__":
    generate_daily_post()
