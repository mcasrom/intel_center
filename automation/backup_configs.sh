#!/bin/bash
# --- BACKUP INTEGRAL DEL NODO INTEL ---
BACKUP_NAME="backup_node_$(date +'%Y%m%d').tar.gz"
DESTINO="/home/dietpi/intel_center_odroid/blog/static/backups/"

mkdir -p "$DESTINO"

# Comprimir Scripts (.py, .sh) Y la Base de Datos (.db)
tar -czf "$DESTINO$BACKUP_NAME" \
    /home/dietpi/intel_center_odroid/automation/*.py \
    /home/dietpi/intel_center_odroid/automation/*.sh \
    /home/dietpi/intel_center_odroid/data/*.db

# Mantener solo los últimos 3 backups
ls -t "$DESTINO"backup_node_*.tar.gz 2>/dev/null | tail -n +4 | xargs -I {} rm {}

echo "[+] Backup integral creado en: $DESTINO$BACKUP_NAME"
