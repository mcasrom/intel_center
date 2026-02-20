import sqlite3
import os
import sys
from datetime import datetime, timedelta

# --- CONFIGURACIÓN ---
BASE_DIR = "/home/dietpi/intel_center_odroid"
DB_PATH = os.path.join(BASE_DIR, "data/news.db")
POSTS_DIR = os.path.join(BASE_DIR, "blog/content/post")

sys.path.append(os.path.join(BASE_DIR, "automation"))
try:
    from enrich_report import GEO_CONTEXT
except ImportError:
    sys.exit(1)

def generar_barra(puntos):
    ancho = 10
    lleno = int(min(puntos / 100, 1.0) * ancho)
    return f"|{'█' * lleno}{'░' * (ancho - lleno)}|"

def ejecutar_final():
    os.makedirs(POSTS_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    tabla_iie = []
    tabla_actividad = []
    datos_analisis = []
    fecha_hoy = datetime.now().strftime('%Y-%m-%d')
    hace_24h = (datetime.now() - timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')

    for region, info in GEO_CONTEXT.items():
        cur.execute("SELECT link, COUNT(*) as c FROM news WHERE region = ? AND timestamp > ? GROUP BY link ORDER BY c DESC", (region, hace_24h))
        filas = cur.fetchall()
        n_noticias = sum(f[1] for f in filas)
        
        if n_noticias > 0:
            # Cálculo de Intensidad
            gdp = float(info['gdp'].replace('$', '').replace('T', ''))
            iie_hoy = round(n_noticias / gdp, 2)
            
            # Determinar estado
            estado = "🔴 CRÍTICO" if iie_hoy > 50 else "🟠 ELEVADO" if iie_hoy > 15 else "🟢 ESTABLE"
            barra = generar_barra(iie_hoy)
            
            tabla_iie.append(f"| **{region}** | {iie_hoy} | `{barra}` | {estado[0]} |")
            tabla_actividad.append(f"| {region} | {n_noticias} | {filas[0][0].split('//')[-1].split('/')[0]} |")
            datos_analisis.append({"region": region, "iie": iie_hoy, "noticias": n_noticias})

    # Narrativa Inteligente
    if datos_analisis:
        top_region = max(datos_analisis, key=lambda x: x['iie'])
        narrativa = f"El foco de atención principal se sitúa en **{top_region['region']}**, que presenta el índice de intensidad más alto ({top_region['iie']}). "
        narrativa += f"A pesar del volumen bruto de noticias, su relación con el peso económico de la región indica una saturación informativa crítica."

    ruta_final = os.path.join(POSTS_DIR, f"{fecha_hoy}-informe.md")
    with open(ruta_final, "w", encoding="utf-8") as f:
        f.write(f"---\ntitle: \"Análisis Estratégico: {fecha_hoy}\"\ndate: {datetime.now().isoformat()}\nreport_types: \"diario\"\n---\n\n")
        
        f.write(f"## 🧠 Resumen Ejecutivo\n\n{narrativa}\n\n")
        
        f.write(f"## 📊 1. Índice de Intensidad ($P_p$)\n\n| Región | $P_p$ | Visual | Est. |\n| :--- | :---: | :--- | :---: |\n")
        f.write("\n".join(tabla_iie) + "\n\n")
        
        f.write(f"## 🚨 2. Desglose de Actividad\n\n| Región | Noticias | Fuente Principal |\n| :--- | :---: | :--- |\n")
        f.write("\n".join(tabla_actividad) + "\n\n")
        
        f.write(f"## 🛠️ Metodología de Cálculo\n\n")
        f.write("El **Índice de Intensidad ($P_p$)** se calcula mediante la fórmula:\n\n")
        f.write("$$P_p = \\frac{\\text{Nº Noticias (24h)}}{\\text{PIB Regional (T$) * Coeficiente Contexto}}$$\n\n")
        f.write("* **Verde (<15)**: Ruido mediático estándar.\n* **Naranja (15-50)**: Actividad anómala, posible conflicto en gestación.\n* **Rojo (>50)**: Saturación informativa, evento de alto impacto en curso.\n")

    conn.close()
    print(f"✅ Informe con narrativa generado en: {ruta_final}")

if __name__ == "__main__":
    ejecutar_final()
