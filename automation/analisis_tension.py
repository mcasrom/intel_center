import sqlite3
import os
import datetime

# --- CONFIGURACIÓN DE RUTAS ---
DB_PATH = "/home/dietpi/intel_center_odroid/data/news.db"
REPORT_DIR = "/home/dietpi/intel_center_odroid/blog/content/reports/"

def calcular_tension():
    hoy = datetime.datetime.now().strftime("%y%m%d") + "_total_analysis.md"
    path = os.path.join(REPORT_DIR, hoy)
    
    if not os.path.exists(path):
        print(f"Error: No se encuentra el reporte {path}")
        return

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # 1. Obtener regiones activas en la última semana
    cur.execute("SELECT DISTINCT region FROM news WHERE timestamp > datetime('now','-7 days')")
    regiones = [r[0] for r in cur.fetchall()]

    alertas = []

    for reg in regiones:
        # Media diaria de los últimos 7 días (base de comparación)
        cur.execute(f"SELECT COUNT(*)/7.0 FROM news WHERE region='{reg}' AND timestamp > datetime('now','-7 days')")
        media = cur.fetchone()[0] or 1
        
        # Volumen de las últimas 24 horas
        cur.execute(f"SELECT COUNT(*) FROM news WHERE region='{reg}' AND timestamp > datetime('now','-24 hours')")
        actual = cur.fetchone()[0]

        # Evitar alertas si el volumen actual es insignificante (menos de 5 noticias)
        if actual < 5:
            continue

        varianza = ((actual - media) / media) * 100

        # Umbral de Alerta: +20% de incremento sobre lo habitual
        if varianza > 20:
            color = "red" if varianza > 50 else "orange"
            alertas.append(f"<b style='color:{color}'>⚠️ {reg}</b>: Incremento del {varianza:.1f}% sobre la media semanal.")

    conn.close()

    # 2. INYECCIÓN MODULAR EN EL REPORTE
    if alertas:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Construir el bloque de alertas con estilo Markdown/HTML
            aviso = "### 🚨 ALERTAS DE TENSIÓN DETECTADAS\n"
            aviso += "\n".join([f"- {a}" for a in alertas])
            aviso += "\n\n---\n"
            
            # Dividimos por el delimitador de Hugo (---)
            # partes[0] = vacío (antes del primer ---)
            # partes[1] = metadatos (título, fecha, tags)
            # partes[2] = contenido del reporte
            partes = content.split("---", 2)
            
            if len(partes) >= 3:
                # Reconstruimos: Frontmatter + Alertas + Resto del Dashboard
                new_content = f"---{partes[1]}---\n\n{aviso}{partes[2]}"
                
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("✅ Inteligencia: Alertas de tensión inyectadas correctamente.")
            else:
                print("⚠️ Aviso: No se pudo inyectar alertas (formato de Frontmatter no detectado).")
                
        except Exception as e:
            print(f"❌ Error al procesar el reporte: {e}")

if __name__ == "__main__":
    calcular_tension()
