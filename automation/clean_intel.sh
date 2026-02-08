#!/bin/bash
# --- MANTENIMIENTO DEL NODO INTEL ---

# 1. Definir rutas
POSTS_DIR="/home/dietpi/intel_center_odroid/blog/content/post/"
LOG_FILE="/home/dietpi/intel_center_odroid/cron_log.txt"

# 2. Borrar informes de más de 15 días (ahorramos inodos en la SD)
# Mantenemos los últimos 15 para tener histórico web, el resto fuera.
find "$POSTS_DIR" -name "*-informe.md" -mtime +15 -exec rm {} \;

# 3. Rotar el log del cron si es mayor a 500KB (evitamos archivos gigantes)
if [ -f "$LOG_FILE" ]; then
    SIZE=$(du -k "$LOG_FILE" | cut -f1)
    if [ $SIZE -gt 500 ]; then
        echo "[$(date)] Log rotado por tamaño excesivo" > "$LOG_FILE"
    fi
fi

echo "[+] Mantenimiento completado: $(date)"
