#!/bin/bash

# 1. Definir rutas
BASE_DIR="/home/dietpi/intel_center_odroid"
PYTHON_BIN="$BASE_DIR/venv/bin/python3"
SCRIPT_PY="$BASE_DIR/automation/main_intel.py"

echo "[+] [odroid-c2] Iniciando ciclo de inteligencia..."

# 2. Ejecutar directamente con el binario del venv
# Esto evita tener que hacer 'source activate'
$PYTHON_BIN $SCRIPT_PY

# 3. Subir a GitHub (solo si el script de python terminó bien)
if [ $? -eq 0 ]; then
    echo "[+] Captura exitosa. Sincronizando con GitHub..."
    cd $BASE_DIR
    git add .
    git commit -m "Intel Update: $(date +'%Y-%m-%d %H:%M')"
    git push origin main
else
    echo "[-] Error en Python. Abortando."
    exit 1
fi
