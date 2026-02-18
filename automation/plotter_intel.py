import pandas as pd
import matplotlib.pyplot as plt
import os
import sys
import datetime
import logging

# --- CONFIGURACIÓN DE LOGS ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- CONFIGURACIÓN DE RUTAS ---
BASE_DIR = "/home/dietpi/intel_center_odroid"
USA_CSV = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_CSV = os.path.join(BASE_DIR, "data/spain_trend.csv")
INDIA_CHINA_CSV = os.path.join(BASE_DIR, "data/india_china_core_trend.csv")

def generar_grafica():
    logging.info("Iniciando generación de gráficos de tendencia...")
    try:
        # Verificación de integridad de archivos consolidados
        if not os.path.exists(USA_CSV) or not os.path.exists(SPAIN_CSV):
            logging.error("Faltan archivos CSV críticos (USA o SPAIN). Abortando.")
            return

        # Carga de datos con nombres de columna para evitar errores de cabecera
        # Se toman los últimos 24 registros para la ventana de tiempo del informe
        df_usa = pd.read_csv(USA_CSV, names=['timestamp', 'val']).tail(24)
        df_spain = pd.read_csv(SPAIN_CSV, names=['timestamp', 'val']).tail(24)

        # Configuración del lienzo (Estilo oscuro OSINT)
        plt.figure(figsize=(12, 6))
        plt.style.use('dark_background')

        # --- RENDERIZADO DE LÍNEAS ---
        
        # 1. USA (Azul)
        plt.plot(df_usa['timestamp'], df_usa['val'], 
                 label='USA', color='#3498db', linewidth=2.5, 
                 marker='o', markersize=4, alpha=0.9)
        
        # 2. ESPAÑA (Rojo)
        plt.plot(df_spain['timestamp'], df_spain['val'], 
                 label='ESPAÑA', color='#e74c3c', linewidth=2.5, 
                 marker='o', markersize=4, alpha=0.9)

        # 3. INDIA-CHINA (Amarillo) - Nueva implementación
        if os.path.exists(INDIA_CHINA_CSV):
            try:
                df_ic = pd.read_csv(INDIA_CHINA_CSV, names=['timestamp', 'val']).tail(24)
                if not df_ic.empty:
                    plt.plot(df_ic['timestamp'], df_ic['val'], 
                             label='INDIA-CHINA', color='#f1c40f', linewidth=2.5, 
                             marker='o', markersize=4, alpha=0.9)
                    logging.info("Nodo INDIA-CHINA integrado en la gráfica.")
            except Exception as e_csv:
                logging.warning(f"Error al leer datos de India-China: {e_csv}")

        # --- FORMATEO ESTÉTICO ---
        plt.axhline(0, color='white', linestyle='--', alpha=0.3) # Línea de neutralidad
        plt.title('MONITORIZACIÓN GEOPOLÍTICA: SENTIMIENTO POR REGIÓN', 
                  color='#2ecc71', fontsize=14, fontweight='bold', pad=20)
        plt.xlabel('Ventana Temporal (Últimas 24 lecturas)', fontsize=10, color='#95a5a6')
        plt.ylabel('Índice de Sentimiento', fontsize=10, color='#95a5a6')
        
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.legend(loc='upper left', frameon=True, facecolor='#2c3e50', edgecolor='white')
        plt.grid(True, which='both', linestyle='--', alpha=0.1)
        plt.tight_layout()

        # --- GESTIÓN DE SALIDA DE ARCHIVOS ---
        
        # Determinación del nombre (por argumento o timestamp)
        if len(sys.argv) > 1:
            nombre_img = sys.argv[1]
        else:
            nombre_img = datetime.datetime.now().strftime("%y%m%d_%H%M_trend.png")

        # Rutas de exportación
        IMG_HISTORICA = os.path.join(BASE_DIR, "blog/static/images/", nombre_img)
        IMG_ESTATICA = os.path.join(BASE_DIR, "blog/static/images/trend.png")

        # Asegurar que el directorio existe
        os.makedirs(os.path.dirname(IMG_HISTORICA), exist_ok=True)

        # Guardado doble
        plt.savefig(IMG_HISTORICA, dpi=100)
        plt.savefig(IMG_ESTATICA, dpi=100)
        
        plt.close()
        logging.info(f"Gráfico exportado correctamente: {nombre_img}")

    except Exception as e:
        logging.critical(f"ERROR CRÍTICO EN EL PLOTTER: {e}")

if __name__ == "__main__":
    generar_grafica()
