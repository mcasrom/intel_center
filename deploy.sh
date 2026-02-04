#!/bin/bash
# Script de despliegue para El Mapa y El Código

echo -e "\e[32m[+] Iniciando despliegue en GitHub...\e[0m"

# 1. Generar los posts y el JSON con el motor de Python
python3 ~/intel_center_test/automation/main_intel.py

# 2. Compilar el sitio con Hugo (limpiando el directorio public previo)
cd ~/intel_center_test/blog
rm -rf public
hugo

# 3. Empujar a GitHub
git add .
git commit -m "Intel Update: $(date +'%Y-%m-%d %H:%M')"
git push origin main

echo -e "\e[32m[+] Proyecto actualizado en https://mcasrom.github.io/intel_center/\e[0m"
