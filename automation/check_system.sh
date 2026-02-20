#!/bin/bash

# ====================================================
# SISTEMA DE MONITOREO OSINT - NODO ODROID-C2
# Genera reportes Markdown para visualización remota
# ====================================================

# Configuración de rutas
BASE_DIR="/home/dietpi/intel_center_odroid"
REPORT_DIR="$BASE_DIR/blog/content/reports"
DATE_STR=$(date +%y%m%d)
FILE_NAME="${DATE_STR}_total_analysis.md"
REPORT_PATH="$REPORT_DIR/$FILE_NAME"

mkdir -p "$REPORT_DIR"

# 1. CABECERA MARKDOWN (Frontmatter para Hugo)
{
    echo "---"
    echo "title: \"Análisis de Estado - $(date '+%Y-%m-%d %H:%M')\""
    echo "date: $(date '+%Y-%m-%dT%H:%M:%S')"
    echo "layout: \"post\""
    echo "tags: [\"monitor\", \"sistema\"]"
    echo "---"
    echo ""
    echo "# 🛡️ Dashboard Operativo: Nodo $(hostname)"
    echo "Actualización: $(date '+%d/%m/%Y %H:%M:%S')"
    echo ""
    echo "## 🌡️ Telemetría de Hardware"
} > "$REPORT_PATH"

# 2. MÉTRICAS DE HARDWARE
TEMP=$(cat /sys/class/thermal/thermal_zone0/temp | sed 's/\(..\).*/\1/')
LOAD=$(uptime | awk -F'load average:' '{ print $2 }')

{
    echo "- **Temperatura CPU**: ${TEMP}°C"
    if [ "$TEMP" -gt 65 ]; then
        echo "  - ⚠️ **ALERTA**: Temperatura elevada. Revisar flujo de aire."
    fi
    echo "- **Carga Sistema**: ${LOAD}"
    echo "- **Uptime**: $(uptime -p)"
} >> "$REPORT_PATH"

# 3. VERIFICACIÓN DE SCRIPTS (PRESENCIA)
echo -e "\n## 📜 Verificación de Scripts Críticos" >> "$REPORT_PATH"
scripts=(
    "$BASE_DIR/automation/run_intel.sh"
    "$BASE_DIR/automation/radar_intel.py"
    "$BASE_DIR/automation/analitica_varianza.py"
    "$BASE_DIR/automation/analista_historico.py"
    "$BASE_DIR/automation/analista_mensual.py"
    "/home/dietpi/scripts/monitor_hw.sh"
    "/home/dietpi/scripts/archive_data.py"
)

for script in "${scripts[@]}"; do
    if [ -f "$script" ]; then
        echo "- ✅ **OK**: $script" >> "$REPORT_PATH"
    else
        echo "- ❌ **ERROR**: $script (No encontrado)" >> "$REPORT_PATH"
    fi
done

# 4. CALIDAD DE LA INGESTA (Top Regiones Activas en 24h)
echo -e "\n## 📊 Calidad de Ingesta (Últimas 24h)" >> "$REPORT_PATH"
{
    echo "| Región | Noticias Ingeridas |"
    echo "| :--- | :--- |"
    sqlite3 "$BASE_DIR/data/news.db" "SELECT region, COUNT(*) as c FROM news WHERE timestamp >= datetime('now', '-24 hours') GROUP BY region ORDER BY c DESC LIMIT 5;" | while read -r line; do
        REGION=$(echo $line | cut -d'|' -f1)
        COUNT=$(echo $line | cut -d'|' -f2)
        echo "| $REGION | $COUNT |"
    done
} >> "$REPORT_PATH"

# 5. ANÁLISIS DE ERRORES EN LOGS
echo -e "\n## 🕵️ Análisis de Errores (Últimas 12h)" >> "$REPORT_PATH"
ERRORS=$(grep -Ei "error|exception|critical" $BASE_DIR/automation/intel_final.log | tail -n 5)
if [ -z "$ERRORS" ]; then
    echo "- ✅ Logs limpios. No se detectan anomalías críticas." >> "$REPORT_PATH"
else
    echo "- ⚠️ **Alertas en logs detectadas**:" >> "$REPORT_PATH"
    echo '```text' >> "$REPORT_PATH"
    echo "$ERRORS" >> "$REPORT_PATH"
    echo '```' >> "$REPORT_PATH"
fi

# 6. REDUNDANCIA (ODROID SECUNDARIA .149)
echo -e "\n## 🔄 Redundancia (Espejo .149)" >> "$REPORT_PATH"
if ping -c 1 192.168.1.149 &> /dev/null; then
    SSH_STATUS=$(ssh -o ConnectTimeout=2 dietpi@192.168.1.149 "echo 'OK'" 2>/dev/null)
    if [ "$SSH_STATUS" == "OK" ]; then
        echo "- 🔑 Enlace SSH: **VERIFICADO** (Backup garantizado)" >> "$REPORT_PATH"
    else
        echo "- ⚠️ Enlace SSH: **FALLIDO** (Ping OK pero sin acceso SSH)" >> "$REPORT_PATH"
    fi
else
    echo "- ❌ Estado: **OFFLINE** (Revisar conexión de la Odroid secundaria)" >> "$REPORT_PATH"
fi

# 7. ESPACIO EN DISCO
echo -e "\n## 💾 Almacenamiento" >> "$REPORT_PATH"
SPACE=$(df -h / | awk 'NR==2 {print $5}')
echo "- **Uso de Disco**: $SPACE" >> "$REPORT_PATH"

# ====================================================
# MODULARIDAD: LLAMADA A SCRIPTS DE ENRIQUECIMIENTO
# ====================================================

# A. Inyecta datos de Población, PIB y Religión
python3 "$BASE_DIR/automation/enrich_report.py"

# B. Analiza anomalías de varianza y lanza alertas visuales
python3 "$BASE_DIR/automation/analisis_tension.py"

# C. Cierre del archivo y Firma
{
    echo -e "\n---"
    echo "*Auto-reporte generado por el Nodo de Inteligencia $(hostname).*"
} >> "$REPORT_PATH"

# D. Rotación automática: mantiene solo los últimos 15 reportes
find "$REPORT_DIR" -name "*_total_analysis.md" -mtime +15 -delete

exit 0
