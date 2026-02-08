#!/bin/bash
# Limpieza de informes antiguos (más de 15 días)
find /home/dietpi/intel_center_odroid/blog/content/post/ -name "*-informe.md" -mtime +15 -exec rm {} \;

# Vaciar logs de cron si superan 1MB
LOGFILE="/home/dietpi/intel_center_odroid/cron_log.txt"
if [ -f "$LOGFILE" ]; then
    find "$LOGFILE" -size +1M -exec cp /dev/null {} \;
fi

echo "[+] Limpieza completada: $(date)"
