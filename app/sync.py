import shutil
from pathlib import Path

from app.models import Mod, InstalledMod


def synchronize_installed_mods(
    requested_mods: list[Mod],
    server_root: Path,
    cache: list[InstalledMod],
) -> list[int]:
    """
    Elimina del servidor los mods que ya no están habilitados en mods.yml.

    Compara los IDs habilitados contra el cache y elimina la carpeta
    Mods/Workshop/<WorkshopID> de cada mod que ya no deba estar instalado.

    Args:
        requested_mods: Lista de mods definidos en mods.yml.
        server_root: Ruta raíz del servidor de Palworld.
        cache: Lista de mods actualmente registrados en cache.json.

    Returns:
        Lista de IDs eliminados.
    """
    requested_ids: set[int] = {mod.id for mod in requested_mods if mod.enabled}
    cached_ids: set[int] = {entry.id for entry in cache}

    to_remove: set[int] = cached_ids - requested_ids

    removed: list[int] = []

    for mod_id in to_remove:
        mod_dir = server_root / "Mods" / "Workshop" / str(mod_id)

        if mod_dir.exists():
            shutil.rmtree(mod_dir)

        removed.append(mod_id)

    return removed
