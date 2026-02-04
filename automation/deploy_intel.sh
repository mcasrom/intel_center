#!/bin/bash
# 1. Limpieza y preparación
cd ~/intel_center_test

# 2. Ejecutar el cerebro (Python)
python3 automation/main_intel.py

# 3. Compilar el blog con Hugo
cd blog
hugo

# 4. Sincronizar con el mundo
git add .
git commit -m "Auto-intel: $(date +'%Y-%m-%d %H:%M') - Expansión América"
git push origin main
