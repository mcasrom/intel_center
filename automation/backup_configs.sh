#!/bash
# --- BACKUP INTEGRAL DEL NODO INTEL (OPTIMIZADO) ---
FECHA=$(date +'%Y%m%d')
BACKUP_NAME="backup_node_${FECHA}.tar.gz"
DESTINO="/home/dietpi/intel_center_odroid/blog/static/backups/"
DB_ORIGEN="/home/dietpi/intel_center_odroid/data/news.db"
DB_TEMP="/home/dietpi/intel_center_odroid/data/news_snapshot.db"

mkdir -p "$DESTINO"

echo "[*] Creando snapshot de la base de datos para evitar corrupción..."
# Usamos el comando .backup de sqlite para una copia en caliente segura
sqlite3 "$DB_ORIGEN" ".backup '$DB_TEMP'"

echo "[*] Comprimiendo scripts y datos..."
tar -czf "$DESTINO$BACKUP_NAME" \
    /home/dietpi/intel_center_odroid/automation/*.py \
    /home/dietpi/intel_center_odroid/automation/*.sh \
    "$DB_TEMP"

# Borrar el snapshot temporal
rm "$DB_TEMP"

# --- SEGURIDAD: Evitar listado de directorio si usas servidor web ---
touch "$DESTINO/index.html" # Un index vacío evita que se vean los archivos

# --- ROTACIÓN: Mantener solo los últimos 3 backups ---
ls -t "$DESTINO"backup_node_*.tar.gz 2>/dev/null | tail -n +4 | xargs -I {} rm {}

echo "[+] Backup integral creado con éxito: $DESTINO$BACKUP_NAME"
echo "[+] Estado de la carpeta de backups:"
ls -lh "$DESTINO"backup_node_*.tar.gz
