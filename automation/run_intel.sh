#!/bin/bash

# ================================
# RUN INTEL - Minimal para GitHub
# ================================

BASE_DIR="/home/dietpi/intel_center_odroid"
PYTHON_BIN="$BASE_DIR/venv/bin/python3"
SCRIPT_PY="$BASE_DIR/automation/main_intel.py"
PLOTTER="$BASE_DIR/automation/plotter_intel.py"

echo "[+] [odroid-c2] Iniciando ciclo de inteligencia..."

# 1. Ejecutar main_intel.py
$PYTHON_BIN $SCRIPT_PY
if [ $? -ne 0 ]; then
    echo "[-] Error ejecutando main_intel.py"
    exit 1
fi

# 2. Ejecutar plotter
$PYTHON_BIN $PLOTTER
if [ $? -ne 0 ]; then
    echo "[-] Error ejecutando plotter_intel.py"
    exit 1
fi

# 3. Subir resultados a GitHub
cd $BASE_DIR
git add .
git commit -m "Intel Update: $(date +'%Y-%m-%d %H:%M')"
git push origin main

echo "[+] Ciclo completo. JSON, posts y gráficas subidos a GitHub."
