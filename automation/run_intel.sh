#!/bin/bash
# INTEL CENTER - Script Maestro para Odroid C2 / Linux
# Detectar rutas relativas al script
SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
REPO_DIR=$(dirname "$SCRIPT_DIR")
BLOG_DIR="$REPO_DIR/blog"
PYTHON_EXE=$(which python3)

echo -e "\e[32m[+] [$(hostname)] Iniciando ciclo de inteligencia...\e[0m"

# 1. Ejecutar motor de análisis
$PYTHON_EXE "$SCRIPT_DIR/main_intel.py"
if [ $? -ne 0 ]; then echo -e "\e[31m[-] Error en Python. Abortando.\e[0m"; exit 1; fi

# 2. Compilar Hugo
echo -e "\e[32m[+] Compilando sitio estático...\e[0m"
cd "$BLOG_DIR" && rm -rf public && hugo --minify

# 3. Sincronizar GitHub
echo -e "\e[32m[+] Sincronizando con GitHub...\e[0m"
cd "$REPO_DIR"
git add .
git commit -m "Intel Update ($(hostname)): $(date +'%Y-%m-%d %H:%M')"
git push origin main

echo -e "\e[32m[+] Proceso completado con éxito.\e[0m"
