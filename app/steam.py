import shutil
import subprocess
from pathlib import Path


# App ID de Palworld en Steam
PALWORLD_APP_ID = "2394010"


def check_steamcmd() -> bool:
    """
    Comprueba que steamcmd esté disponible en el PATH.

    Returns:
        True si steamcmd está instalado, False si no se encuentra.
    """
    return shutil.which("steamcmd") is not None


def download_mod(mod_id: int, download_dir: Path) -> bool:
    """
    Descarga un Workshop Item de Palworld usando SteamCMD.

    Args:
        mod_id: ID del mod en Steam Workshop.
        download_dir: Directorio base donde SteamCMD depositará los archivos.

    Returns:
        True si SteamCMD terminó con código de salida 0, False si falló.
    """
    download_dir.mkdir(parents=True, exist_ok=True)

    command = [
        "steamcmd",
        "+force_install_dir", str(download_dir),
        "+login", "anonymous",
        "+workshop_download_item", PALWORLD_APP_ID, str(mod_id),
        "+quit",
    ]

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    return result.returncode == 0
