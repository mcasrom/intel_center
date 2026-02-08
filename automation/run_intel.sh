#!/bin/bash
BASE_DIR="/home/dietpi/intel_center_odroid"
PYTHON_BIN="$BASE_DIR/venv/bin/python3"
BLOG_DIR="$BASE_DIR/blog"

echo "[+] Iniciando ciclo de inteligencia..."

# 1. Generar datos e Informe
$PYTHON_BIN $BASE_DIR/automation/main_intel.py

# 2. Generar la GRÁFICA (Ahora antes de subir nada)
$PYTHON_BIN $BASE_DIR/automation/plotter_intel.py

# 3. Construir la web estática
cd $BLOG_DIR
rm -rf public/
hugo --buildFuture

# 4. Sincronizar TODO a la vez con GitHub
echo "[+] Enviando informe + gráfica a GitHub..."
cd $BASE_DIR
git add .
git commit -m "Intel Update: Complete Report & Graphs $(date +'%H:%M')"
git push origin main

echo "[+] Proceso finalizado."
