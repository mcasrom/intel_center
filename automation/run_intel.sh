#!/bin/bash

# 1. Definir rutas
BASE_DIR="/home/dietpi/intel_center_odroid"
PYTHON_BIN="$BASE_DIR/venv/bin/python3"
SCRIPT_PY="$BASE_DIR/automation/main_intel.py"
BLOG_DIR="$BASE_DIR/blog"

echo "[+] [odroid-c2] Iniciando ciclo de inteligencia..."

# 2. Ejecutar captura de datos
$PYTHON_BIN $SCRIPT_PY

# 3. CONSTRUIR LA WEB CON HUGO (Paso crítico que faltaba)
if [ $? -eq 0 ]; then
    echo "[+] Generando HTML con Hugo..."
    cd $BLOG_DIR
    # Borramos la web vieja y generamos la nueva forzando posts futuros
    rm -rf public/
    hugo --buildFuture
    
    # 4. Sincronizar con GitHub
    echo "[+] Sincronizando con GitHub..."
    cd $BASE_DIR
    git add .
    git commit -m "Intel Update: $(date +'%Y-%m-%d %H:%M')"
    git push origin main
else
    echo "[-] Error en Python. Abortando."
    exit 1
fi

# ... (después de ejecutar main_intel.py) ...
$PYTHON_BIN $SCRIPT_PY

# NUEVA LÍNEA: Generar la gráfica
$PYTHON_BIN $BASE_DIR/automation/plotter_intel.py

# ... (luego sigue el bloque de Hugo que ya teníamos) ...
cd $BLOG_DIR
hugo --buildFuture
# ...
