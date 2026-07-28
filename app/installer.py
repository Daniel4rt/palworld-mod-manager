import shutil
from pathlib import Path

from app.models import ModInfo


def remove_previous_install(destination: Path) -> None:
    """
    Elimina una instalación anterior de forma segura.

    Args:
        destination: Carpeta del mod a eliminar.
    """
    if destination.exists():
        shutil.rmtree(destination)


def install_mod(mod: ModInfo, server_root: Path) -> Path:
    """
    Copia el mod descargado a la carpeta Mods/Workshop del servidor.

    Args:
        mod: Objeto ModInfo con los datos del mod descargado.
        server_root: Ruta raíz del servidor de Palworld.

    Returns:
        Ruta de destino donde quedó instalado el mod.
    """
    workshop_dir = server_root / "Mods" / "Workshop"
    workshop_dir.mkdir(parents=True, exist_ok=True)

    destination = workshop_dir / str(mod.workshop_id)

    remove_previous_install(destination)

    shutil.copytree(mod.root_directory, destination)

    return destination
