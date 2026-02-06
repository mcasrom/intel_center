#!/bin/bash

# Detectar la ruta del script de forma dinámica
SCRIPT_PATH=$(readlink -f "$0")
REPO_DIR=$(dirname "$SCRIPT_PATH")
# Si decides mover el script a /automation, REPO_DIR=$(dirname $(dirname "$SCRIPT_PATH"))

BLOG_DIR="$REPO_DIR/blog"
PYTHON_SCRIPT="$REPO_DIR/automation/main_intel.py"

echo "------------------------------------------"
echo "🤖 [INTEL-CORE] Iniciando captura..."
echo "------------------------------------------"

# 1. Ejecutar el script de Python (asegurando el path)
cd "$REPO_DIR"
/usr/bin/python3 "$PYTHON_SCRIPT"

if [ $? -eq 0 ]; then
    echo "✅ Noticias capturadas correctamente."
else
    echo "❌ Error en el script de Python. Abortando."
    exit 1
fi

# 2. Construir el sitio con Hugo
echo "🏗️ Generando sitio web con Hugo..."
cd "$BLOG_DIR"
# Limpieza de caché previa
rm -rf public resources
# Ejecutar Hugo (asegurando que use la versión del sistema)
hugo --minify

# 3. Subir a GitHub
echo "🚀 Sincronizando con Repositorio Central..."
cd "$REPO_DIR"
git add .
git commit -m "Odroid-Update: $(date +'%Y-%m-%d %H:%M')"
git push origin main

echo "------------------------------------------"
echo "✨ PROCESO FINALIZADO EN $(hostname)"
echo "------------------------------------------"
