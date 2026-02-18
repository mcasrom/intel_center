#!/usr/bin/env python3
import sqlite3
import os
import glob
from datetime import datetime

# CONFIGURACIÓN DE RUTAS
DB_PATH = "/home/dietpi/intel_center_odroid/data/news.db"
POSTS_DIR = "/home/dietpi/intel_center_odroid/blog/content/post/"

def obtener_varianza():
    """Extrae la comparativa de sentimiento de las últimas 24h vs 48h."""
    if not os.path.exists(DB_PATH):
        print("[-] Error: Base de datos no encontrada.")
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # SQL blindada para incluir regiones nuevas (India/China) con COALESCE
        query = """
        WITH datos AS (
            SELECT 
                region, 
                AVG(CASE WHEN timestamp >= datetime('now', '-1 day') THEN sentimiento END) as t_hoy,
                AVG(CASE WHEN timestamp < datetime('now', '-1 day') AND timestamp >= datetime('now', '-2 days') THEN sentimiento END) as t_ayer
            FROM news
            GROUP BY region
        )
        SELECT region, t_hoy, COALESCE(t_ayer, 0.0) as t_ayer 
        FROM datos 
        WHERE t_hoy IS NOT NULL
        UNION ALL
        SELECT 
            'GLOBAL (Media)', 
            AVG(CASE WHEN timestamp >= datetime('now', '-1 day') THEN sentimiento END),
            AVG(CASE WHEN timestamp < datetime('now', '-1 day') AND timestamp >= datetime('now', '-2 days') THEN sentimiento END)
        FROM news
        WHERE timestamp >= datetime('now', '-2 days');
        """
        cursor.execute(query)
        resumen = cursor.fetchall()
        conn.close()
        return resumen
    except Exception as e:
        print(f"[-] Error SQL: {e}")
        return None

def inyectar_en_reporte_diario(datos):
    """Inyecta la tabla de varianza en el post diario evitando duplicaciones."""
    if not datos:
        return

    ahora_dt = datetime.now()
    titulo_tabla = "### 📊 Evolución de Sentimiento (Varianza 24h)"
    
    # 1. Construcción de la tabla Markdown
    tabla = f"{titulo_tabla}\n"
    tabla += f"Comparativa de tensión narrativa: {ahora_dt.strftime('%d/%m/%Y')}\n\n"
    tabla += "| Región | Hoy | Ayer | Delta (Δ) | Estado |\n"
    tabla += "|:---|:---:|:---:|:---:|:---:|\n"

    for reg, hoy, ayer in datos:
        h_val = hoy if hoy is not None else 0.0
        a_val = ayer if ayer is not None else 0.0
        delta = h_val - a_val
        
        # Resaltado para la media global
        b = "**" if "GLOBAL" in reg else ""
        
        # Lógica de estados por Delta
        if delta > 0.05: status = "🔴 Escalada"
        elif delta < -0.05: status = "🟢 Distensión"
        else: status = "⚪ Estable"
        
        tabla += f"| {b}{reg}{b} | {h_val:.4f} | {a_val:.4f} | {delta:+.4f} | {status} |\n"
    
    tabla += "\n---\n"

    # 2. Localización del archivo objetivo (Post de hoy)
    prefijo_hoy = ahora_dt.strftime("%y%m%d")
    candidatos = glob.glob(os.path.join(POSTS_DIR, f"{prefijo_hoy}*.md"))
    reportes = [f for f in candidatos if "varianza" not in f and "balance" not in f]

    if not reportes:
        print(f"[-] No se encontró reporte diario ({prefijo_hoy}) para inyectar.")
        return

    target = reportes[0]

    # 3. Lectura y validación de duplicados
    with open(target, 'r', encoding='utf-8') as f:
        lineas = f.readlines()

    # Si el título de la tabla ya está en el archivo, abortamos para no duplicar
    if any(titulo_tabla in l for l in lineas):
        print(f"[!] Abortado: La tabla de varianza ya existe en {os.path.basename(target)}.")
        return

    # 4. Búsqueda del punto de inserción (tras el segundo '---')
    dashes = 0
    posicion_insercion = 0
    for i, linea in enumerate(lineas):
        if linea.strip() == "---":
            dashes += 1
        if dashes == 2:
            posicion_insercion = i + 1
            break

    # 5. Inserción y escritura final
    lineas.insert(posicion_insercion, "\n" + tabla + "\n")

    with open(target, 'w', encoding='utf-8') as f:
        f.writelines(lineas)

    print(f"✅ Varianza inyectada con éxito en: {os.path.basename(target)}")

if __name__ == "__main__":
    datos_varianza = obtener_varianza()
    inyectar_en_reporte_diario(datos_varianza)
