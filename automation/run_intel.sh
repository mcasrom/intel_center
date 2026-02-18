#!/bin/bash
# NODO ODROID: ORQUESTADOR TOTAL SANEADO

AUTO_DIR="/home/dietpi/intel_center_odroid/automation"
BLOG_DIR="/home/dietpi/intel_center_odroid/blog"
LOG="$AUTO_DIR/intel_final.log"

echo "--- INICIO CICLO $(date) ---" >> $LOG

# 0. Sincronización previa (Vital para redundancia)
cd /home/dietpi/intel_center_odroid && git pull origin main >> $LOG 2>&1

# 1. Ejecutar Ingesta de noticias
/usr/bin/python3 $AUTO_DIR/main_intel.py >> $LOG 2>&1

# 2. Ejecutar Gráficos
/usr/bin/python3 $AUTO_DIR/plotter_intel.py >> $LOG 2>&1

# 3. Ejecutar Informe de Varianza
/usr/bin/python3 $AUTO_DIR/analitica_varianza.py >> $LOG 2>&1

# 4. Construcción de Hugo
cd $BLOG_DIR
/usr/local/bin/hugo --gc --minify >> $LOG 2>&1

# 5. Despliegue Final (Usando el script correcto)
/bin/bash $AUTO_DIR/deploy_intel.sh >> $LOG 2>&1

echo "--- FIN CICLO EXITOSO ---" >> $LOG
