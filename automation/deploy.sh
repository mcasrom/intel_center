#!/bin/bash
# Sincronización con GitHub - Nodo Intel

cd /home/dietpi/intel_center_odroid

# Añadimos todo (incluyendo la DB y los nuevos posts)
git add .
git commit -m "OSINT Update: $(date +'%Y-%m-%d %H:%M') [Host: $(hostname)]"
git push origin main

echo "🚀 Datos sincronizados en GitHub."
