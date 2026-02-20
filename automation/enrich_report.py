import os
import sys

# Datos Maestros (Modifica aquí cuando quieras cambiar población, PIB, etc.)
GEO_CONTEXT = {
    "INDIA_CORE":    {"pop": "1,428M", "gdp": "$3.7T",  "rel": "Hinduismo", "risk": "Alto"},
    "Rusia_Eurasia": {"pop": "144M",   "gdp": "$2.2T",  "rel": "Ortodoxia", "risk": "Extremo"},
    "Medio_Oriente": {"pop": "450M",   "gdp": "$4.5T",  "rel": "Islam",     "risk": "Crítico"},
    "USA_NORTE":     {"pop": "335M",   "gdp": "$26.9T", "rel": "Cristian.", "risk": "Moderado"},
    "Europa_DW":     {"pop": "448M",   "gdp": "$19.3T", "rel": "Cristian.", "risk": "Bajo/Medio"},
    "TURQUIA_SABAH": {"pop": "85M", "gdp": "$1.1T", "rel": "Islam", "risk": "Alto"}
}

def enrich():
    # Buscamos el reporte de hoy
    report_dir = "/home/dietpi/intel_center_odroid/blog/content/reports/"
    import datetime
    today_file = datetime.datetime.now().strftime("%y%m%d") + "_total_analysis.md"
    path = os.path.join(report_dir, today_file)

    if not os.path.exists(path):
        print(f"No se encontró el reporte: {path}")
        return

    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Si ya está enriquecido, no hacemos nada para no duplicar
    if "### 📊 Perfil Geo-Estratégico" in content:
        return

    # Construimos la sección nueva
    extra_info = "\n## 📊 Perfil Geo-Estratégico de las Áreas en Observación\n"
    extra_info += "| Región | Población | PIB | Religión | Riesgo |\n"
    extra_info += "| :--- | :--- | :--- | :--- | :--- |\n"

    for region, data in GEO_CONTEXT.items():
        # Solo añadimos las regiones que se mencionan en el reporte actual
        if region in content:
            extra_info += f"| **{region}** | {data['pop']} | {data['gdp']} | {data['rel']} | {data['risk']} |\n"

    # Insertamos la información antes de la sección de errores
    new_content = content.replace("## 🕵️ Análisis de Errores", extra_info + "\n## 🕵️ Análisis de Errores")

    with open(path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Reporte enriquecido con éxito.")

if __name__ == "__main__":
    enrich()
