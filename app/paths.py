from pathlib import Path

# Rutas estándar utilizadas dentro del contenedor.
# Todos los módulos deben importar desde aquí.

MODS_CONFIG_PATH = Path("/config/mods.yml")
CACHE_PATH = Path("/cache/cache.json")
DOWNLOAD_DIR = Path("/downloads")
SERVER_ROOT = Path("/palworld")
