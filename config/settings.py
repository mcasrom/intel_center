import os
from pathlib import Path

# 1. Encuentra la raíz del proyecto (la carpeta intel_center)
# __file__ es la ubicación de este script. .parent.parent sube dos niveles.
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. Definición de rutas internas (Relativas a la raíz)
CORE_DIR = BASE_DIR / "core"
SENSORS_DIR = BASE_DIR / "sensors"
CONFIG_DIR = BASE_DIR / "config"
HUGO_DIR = BASE_DIR / "blog"

# 3. Lógica del SSD (Detección automática)
# Si estamos en la Odroid, el SSD suele estar en /mnt/...
# Si estamos en el Laptop, usamos una carpeta local para no romper nada.
PROD_SSD_PATH = Path("/mnt/ssd_data/geopolitica")

if PROD_SSD_PATH.exists():
    DATA_DIR = PROD_SSD_PATH
else:
    # Si no existe (estamos en laptop), crea una carpeta 'data' en la raíz del proyecto
    DATA_DIR = BASE_DIR / "data_simulation"
    DATA_DIR.mkdir(parents=True, exist_ok=True)

# 4. Rutas finales para los scripts
DB_PATH = DATA_DIR / "db" / "geopolitica.db"
MAP_DATA_JSON = HUGO_DIR / "static" / "data" / "hotspots.json"

# Asegurar que las carpetas de datos existan
(DATA_DIR / "db").mkdir(parents=True, exist_ok=True)
(DATA_DIR / "exports").mkdir(parents=True, exist_ok=True)
