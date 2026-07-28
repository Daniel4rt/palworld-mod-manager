import json
import os

from app.models import InstalledMod, ModInfo


def load_cache(path: str) -> dict:
    """
    Lee el archivo de cache JSON.

    Si el archivo no existe, devuelve un cache vacío sin lanzar excepción.

    Args:
        path: Ruta al archivo cache.json.

    Returns:
        Diccionario con el contenido del cache, o {"mods": []} si no existe.
    """
    if not os.path.exists(path):
        return {"mods": []}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_cache(path: str, mods: list[InstalledMod]) -> None:
    """
    Guarda la lista de mods instalados en el archivo de cache JSON.
    Siempre sobrescribe el archivo completo.

    Args:
        path: Ruta al archivo cache.json.
        mods: Lista de objetos InstalledMod a persistir.
    """
    data = {
        "mods": [
            {
                "id": mod.id,
                "package_name": mod.package_name,
                "content_hash": mod.content_hash,
            }
            for mod in mods
        ]
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def is_update_required(
    installed: InstalledMod | None,
    current: ModInfo,
) -> bool:
    """
    Determina si un mod necesita ser instalado o reinstalado.

    Compara PackageName y content_hash. No usa el campo Version.

    Returns:
        True si el mod no está en cache, cambió de PackageName o cambió de hash.
        False si no hay cambios detectados.
    """
    if installed is None:
        return True
    if installed.package_name != current.package_name:
        return True
    if installed.content_hash != current.content_hash:
        return True
    return False
