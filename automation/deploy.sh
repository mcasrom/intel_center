#!/bin/bash

# 1. Ejecutar el motor de inteligencia
echo "🤖 Iniciando captura de inteligencia..."
python3 ~/intel_center_test/automation/main_intel.py

# 2. Construir el sitio con Hugo
echo "🏗️ Generando sitio estático..."
cd ~/intel_center_test/blog
hugo --minify

# 3. Subir a GitHub
echo "🚀 Sincronizando con GitHub Pages..."
git add .
git commit -m "Update Intel: $(date +'%Y-%m-%d %H:%M')"
git push origin main

echo "✅ Ciclo completado. Web actualizada."
