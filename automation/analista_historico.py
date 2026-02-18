#!/usr/bin/env python3
import sqlite3
import os
import glob
from datetime import datetime

# CONFIGURACIÓN DE RUTAS
DB_PATH = "/home/dietpi/intel_center_odroid/data/news.db"
POSTS_DIR = "/home/dietpi/intel_center_odroid/blog/content/post/"

def obtener_analisis_historico():
    if not os.path.exists(DB_PATH):
        print("Error: No se encuentra la base de datos.")
        return None
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # SQL CORREGIDA: COALESCE evita que las regiones nuevas desaparezcan
        query = """
        WITH periodos AS (
            SELECT 
                region,
                AVG(CASE WHEN timestamp >= datetime('now', '-7 days') THEN sentimiento END) as actual,
                AVG(CASE WHEN timestamp < datetime('now', '-7 days') AND timestamp >= datetime('now', '-14 days') THEN sentimiento END) as previo,
                COUNT(*) as volumen
            FROM news
            GROUP BY region
        )
        SELECT 
            region, 
            actual, 
            COALESCE(previo, 0.0) as previo, 
            volumen 
        FROM periodos 
        WHERE actual IS NOT NULL;
        """
        cursor.execute(query)
        datos = cursor.fetchall()
        conn.close()
        return datos
    except Exception as e:
        print(f"Error en extracción SQL: {e}")
        return None

def rotar_informes_semanales(max_archivos=12):
    """Mantiene los últimos 3 meses de informes semanales."""
    archivos = sorted(glob.glob(os.path.join(POSTS_DIR, "*_balance-semanal.md")))
    if len(archivos) > max_archivos:
        for f in archivos[:-max_archivos]:
            try:
                os.remove(f)
            except:
                pass

def generar_reporte_semanal(datos):
    if not datos:
        print("Sin datos para generar el reporte semanal.")
        return
    
    ahora = datetime.now()
    nombre_archivo = f"{ahora.strftime('%y%m%d')}_balance-semanal.md"
    FULL_PATH = os.path.join(POSTS_DIR, nombre_archivo)
    
    with open(FULL_PATH, 'w', encoding='utf-8') as f:
        f.write("---\n")
        f.write(f"title: \"Balance Estratégico Semanal: {ahora.strftime('%d/%m/%Y')}\"\n")
        f.write(f"date: {ahora.strftime('%Y-%m-%dT%H:%M:%S+01:00')}\n")
        f.write("report_types: [\"Semanal\"]\n")
        f.write("status: \"Processed\"\n")
        f.write("---\n\n")
        
        f.write("### 📉 Comparativa de Sentimiento Regional (7d vs 14d)\n\n")
        f.write("| Región | Actual (7d) | Previo (14d) | Tendencia | Volumen | Estado |\n")
        f.write("|:---|:---:|:---:|:---:|:---:|:---:|\n")
        
        for reg, actual, previo, vol in datos:
            # Aseguramos que los valores sean floats para el cálculo
            val_actual = actual if actual is not None else 0.0
            val_previo = previo if previo is not None else 0.0
            diff = val_actual - val_previo
            
            # Lógica de Tendencia
            if diff > 0.02: tendencia = "📈 Mejorando"
            elif diff < -0.02: tendencia = "📉 Deterioro"
            else: tendencia = "➡️ Estable"
            
            # Lógica de Estado
            if val_actual > 0.1: estado = "🟢 Positivo"
            elif val_actual < -0.1: estado = "🔴 Tensión"
            else: estado = "🟡 Neutral"
            
            f.write(f"| {reg} | {val_actual:.3f} | {val_previo:.3f} | {tendencia} | {vol} | {estado} |\n")
            
        f.write(f"\n\n*Análisis de tendencia generado por el nodo Odroid-C2. Datos comparativos basados en histórico de 14 días.*")

    print(f"✅ Reporte semanal generado: {nombre_archivo}")
    rotar_informes_semanales()

if __name__ == "__main__":
    datos = obtener_analisis_historico()
    generar_reporte_semanal(datos)
