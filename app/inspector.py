import json
from pathlib import Path

from app.models import ModInfo
from app.hashing import calculate_directory_hash


class InvalidModError(Exception):
    """Se lanza cuando el directorio del mod no tiene una estructura válida."""
    pass


def inspect_mod(mod_directory: Path, workshop_id: int) -> ModInfo:
    """
    Analiza el contenido de un mod descargado.

    Args:
        mod_directory: Directorio raíz donde se descargó el mod.
        workshop_id: ID del Workshop Item correspondiente.

    Returns:
        Objeto ModInfo con los datos extraídos de Info.json y el hash del contenido.

    Raises:
        InvalidModError: Si no se encuentra Info.json en el directorio.
    """
    matches = list(mod_directory.rglob("Info.json"))

    if not matches:
        raise InvalidModError("Info.json not found.")

    info_json_path = matches[0]

    with info_json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    content_hash = calculate_directory_hash(mod_directory)

    return ModInfo(
        workshop_id=workshop_id,
        package_name=data.get("PackageName", ""),
        content_hash=content_hash,
        info_json=info_json_path,
        root_directory=info_json_path.parent,
    )
