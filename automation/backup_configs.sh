#!/bin/bash
# --- BACKUP DEL NODO INTEL ---
BACKUP_NAME="backup_node_$(date +'%Y%m%d').tar.gz"
DESTINO="/home/dietpi/intel_center_odroid/blog/static/backups/"

mkdir -p "$DESTINO"

# Comprimir scripts y configuración
# Incluimos todos los .py y .sh de la carpeta automation
tar -czf "$DESTINO$BACKUP_NAME" \
    /home/dietpi/intel_center_odroid/automation/*.py \
    /home/dietpi/intel_center_odroid/automation/*.sh

# Mantener solo los últimos 3 backups para no llenar la SD
ls -t "$DESTINO"backup_node_*.tar.gz 2>/dev/null | tail -n +4 | xargs -I {} rm {}

echo "[+] Backup creado con éxito en: $DESTINO$BACKUP_NAME"
