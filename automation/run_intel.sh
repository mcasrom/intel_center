#!/bin/bash
# 1. Generar datos y actualizar CSVs
/usr/bin/python3 /home/dietpi/intel_center_odroid/automation/main_intel.py

# 2. Generar la gráfica Matplotlib (ESTO DEBE IR ANTES DEL COMMIT)
/usr/bin/python3 /home/dietpi/intel_center_odroid/automation/plotter_intel.py

# 3. Construir la web con Hugo
cd /home/dietpi/intel_center_odroid/blog
rm -rf public/
/usr/local/bin/hugo --buildFuture

# 4. Sincronizar todo el paquete con GitHub
cd /home/dietpi/intel_center_odroid/
git add .
git commit -m "Intel Update: Informe completo con Gráficas y Separadores"
git push origin main
