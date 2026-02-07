import pandas as pd
import matplotlib.pyplot as plt
import os

# Configuración de rutas
BASE_DIR = "/home/dietpi/intel_center_odroid"
USA_CSV = os.path.join(BASE_DIR, "data/usa_trend.csv")
SPAIN_CSV = os.path.join(BASE_DIR, "data/spain_trend.csv")
# La imagen se guarda en static para que Hugo la encuentre
OUTPUT_IMG = os.path.join(BASE_DIR, "blog/static/images/trend.png")

def generar_grafica():
    try:
        if not os.path.exists(USA_CSV) or not os.path.exists(SPAIN_CSV):
            print("[-] Faltan archivos CSV para graficar.")
            return

        # Cargar últimos 24 registros (aprox las últimas 72h si es cada 3h)
        df_usa = pd.read_csv(USA_CSV).tail(24)
        df_spain = pd.read_csv(SPAIN_CSV).tail(24)

        plt.figure(figsize=(10, 5))
        plt.style.use('dark_background') # Estética hacker/terminal

        # Dibujar líneas
        plt.plot(df_usa['timestamp'], df_usa['avg_sentiment'], label='USA', color='#3498db', linewidth=2, marker='o', markersize=4)
        plt.plot(df_spain['timestamp'], df_spain['avg_sentiment'], label='ESPAÑA', color='#e74c3c', linewidth=2, marker='o', markersize=4)

        # Formateo técnico
        plt.axhline(0, color='white', linestyle='--', alpha=0.3) # Eje neutral
        plt.title('EVOLUCIÓN DEL SENTIMIENTO GEOPOLÍTICO', color='#2ecc71', fontsize=14)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.legend(loc='upper left')
        plt.grid(alpha=0.1)
        plt.tight_layout()

        # Asegurar que el directorio existe y guardar
        os.makedirs(os.path.dirname(OUTPUT_IMG), exist_ok=True)
        plt.savefig(OUTPUT_IMG)
        print(f"[+] Gráfica generada en: {OUTPUT_IMG}")

    except Exception as e:
        print(f"[-] Error en el plotter: {e}")

if __name__ == "__main__":
    generar_grafica()
