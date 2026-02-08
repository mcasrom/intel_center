#!/bin/bash
# Usamos el binario que acabas de localizar
PYTHON_INTEL="/home/dietpi/intel_center_odroid/venv/bin/python3"

echo "[+] Iniciando ciclo de inteligencia..."

# 1. Generar datos
$PYTHON_INTEL /home/dietpi/intel_center_odroid/automation/main_intel.py

# 2. Generar la gráfica (Ahora sí funcionará con pandas)
$PYTHON_INTEL /home/dietpi/intel_center_odroid/automation/plotter_intel.py

# 3. Hugo
cd /home/dietpi/intel_center_odroid/blog
rm -rf public/
/usr/local/bin/hugo --buildFuture

# 4. GitHub
cd /home/dietpi/intel_center_odroid/
git add .
git commit -m "Intel Update: Informe, Gráficas y Separadores Restaurados"
git push origin main
