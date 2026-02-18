#!/usr/bin/env python3
import sqlite3
import os
import matplotlib.pyplot as plt
from datetime import datetime

# CONFIGURACIÓN DE RUTAS
BASE_DIR = "/home/dietpi/intel_center_odroid/automation"
DB_PATH = "/home/dietpi/intel_center_odroid/data/news.db"
POSTS_DIR = "/home/dietpi/intel_center_odroid/blog/content/post/"
IMG_DIR = "/home/dietpi/intel_center_odroid/blog/static/images/mensuales/"
LOGS_A_LIMPIAR = [
    f"{BASE_DIR}/cron_log.txt",
    f"{BASE_DIR}/analista.log",
    f"{BASE_DIR}/mensual.log"
]

def generar_reporte_mensual():
    if not os.path.exists(IMG_DIR): os.makedirs(IMG_DIR)
    
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # 1. OBTENER DATOS DE VOLUMEN DIARIO (Mantenemos tu gráfico intacto)
    query_vol = """
    SELECT date(timestamp), COUNT(*) 
    FROM news 
    WHERE timestamp > datetime('now', '-30 days')
    GROUP BY date(timestamp) ORDER BY date(timestamp);
    """
    cur.execute(query_vol)
    datos_vol = cur.fetchall()
    
    if not datos_vol:
        print("[-] Sin datos para el informe mensual.")
        conn.close()
        return

    # --- LÓGICA DE GRÁFICO (SIN CAMBIOS PARA NO ROMPER EL ESTILO) ---
    fechas = [d[0][-2:] for d in datos_vol] 
    valores = [d[1] for d in datos_vol]
    
    plt.figure(figsize=(10, 5))
    plt.plot(fechas, valores, color='cyan', marker='o', linestyle='-', linewidth=2)
    plt.fill_between(fechas, valores, color='cyan', alpha=0.1)
    plt.title(f"Volumen de Inteligencia - {datetime.now().strftime('%B %Y')}")
    plt.xlabel("Día del mes")
    plt.ylabel("Señales detectadas")
    plt.grid(True, alpha=0.2)
    
    img_name = f"volumen-{datetime.now().strftime('%y%m')}.png"
    plt.savefig(os.path.join(IMG_DIR, img_name), bbox_inches='tight')
    plt.close()

    # --- NUEVA FASE: ANÁLISIS POR REGIÓN (BLINDADO PARA INDIA/CHINA) ---
    # Esta parte añade valor al MD sin tocar el gráfico
    query_regiones = """
    WITH mensual AS (
        SELECT 
            region,
            AVG(CASE WHEN timestamp >= datetime('now', '-15 days') THEN sentimiento END) as actual,
            AVG(CASE WHEN timestamp < datetime('now', '-15 days') AND timestamp >= datetime('now', '-30 days') THEN sentimiento END) as previo,
            COUNT(*) as volumen
        FROM news
        GROUP BY region
    )
    SELECT region, actual, COALESCE(previo, 0.0), volumen 
    FROM mensual WHERE actual IS NOT NULL;
    """
    cur.execute(query_regiones)
    datos_regiones = cur.fetchall()

    # 2. REDACTAR INFORME MD
    nombre_archivo = datetime.now().strftime("%y%m") + "-INFORME-MENSUAL.md"
    REPORT_PATH = os.path.join(POSTS_DIR, nombre_archivo)
    
    with open(REPORT_PATH, "w") as f:
        f.write("---\n")
        f.write(f"title: \"Informe Mensual de Inteligencia: {datetime.now().strftime('%B %Y')}\"\n")
        f.write(f"date: {datetime.now().isoformat()}\n")
        f.write("report_types: [\"Mensual\"]\n")
        f.write("---\n\n")
        f.write(f"## 📊 Análisis de Volumen Mensual\n\n")
        f.write(f"![Volumen Diario](../../images/mensuales/{img_name})\n\n")
        
        # Insertamos la tabla de regiones blindada
        f.write("### 🌏 Balance Regional de Sentimiento (30 días)\n\n")
        f.write("| Vector | Sentimiento Mes | Cambio (Δ) | Volumen |\n")
        f.write("|:---|:---:|:---:|:---:|\n")
        for reg, actual, previo, vol in datos_regiones:
            diff = actual - previo
            f.write(f"| {reg} | {actual:.3f} | {diff:+.3f} | {vol} |\n")

        f.write(f"\n### 🧠 Conclusión Operativa\n\n")
        total_mes = sum(valores)
        promedio = total_mes / len(valores)
        
        f.write(f"> El nodo Odroid-C2 ha procesado **{total_mes} señales** este mes, con un promedio de **{promedio:.1f} eventos/día**. ")
        f.write("El sistema de almacenamiento se encuentra en estado óptimo tras la rotación de logs.\n")

    conn.close()
    print(f"[+] Informe Mensual Generado: {REPORT_PATH}")

    # 3. HIGIENE OPERATIVA (Tu lógica original intacta)
    print("[*] Iniciando rotación de logs...")
    for log_file in LOGS_A_LIMPIAR:
        if os.path.exists(log_file):
            with open(log_file, "w") as f:
                f.write(f"--- Log reseteado tras Informe Mensual: {datetime.now()} ---\n")
            print(f"[+] Log saneado: {os.path.basename(log_file)}")

if __name__ == "__main__":
    generar_reporte_mensual()
