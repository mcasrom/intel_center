#!/bin/bash

# --- CONFIGURACIÓN ---
IP_LOCAL="192.168.1.147"
PUERTO="1315"
SOURCE_DIR="/home/dietpi/intel_center_odroid/blog"

echo "🧹 Limpiando procesos previos en el puerto $PUERTO..."
# Intentamos matar el proceso que ocupa el puerto de forma silenciosa
fuser -k $PUERTO/tcp > /dev/null 2>&1

echo "🚀 Lanzando Hugo Server para Intel Center..."
echo "📍 Dirección: http://$IP_LOCAL:$PUERTO"

cd $SOURCE_DIR

hugo server \
  -s "$SOURCE_DIR" \
  --bind "$IP_LOCAL" \
  --port "$PUERTO" \
  --baseURL "http://$IP_LOCAL:$PUERTO/" \
  --appendPort=true \
  --disableFastRender \
  --buildDrafts
