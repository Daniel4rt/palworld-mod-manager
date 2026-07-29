"""
Funciones relacionadas con SteamCMD.
"""

import subprocess
from pathlib import Path
from unittest import result

# App ID de Palworld en Steam
PALWORLD_APP_ID = "2394010"

# Ruta de SteamCMD dentro del contenedor thijsvanloef/palworld-server-docker
STEAMCMD = "/home/steam/steamcmd/steamcmd.sh"


def check_steamcmd() -> bool:
    """
    Comprueba que SteamCMD exista.

    Returns:
        True si SteamCMD está presente.
    """
    return Path(STEAMCMD).is_file()


def download_mod(mod_id: int, download_dir: Path) -> bool:
    """
    Descarga un Workshop Item de Palworld usando SteamCMD.

    Args:
        mod_id: ID del mod en Steam Workshop.
        download_dir: Directorio base donde SteamCMD depositará los archivos.

    Returns:
        True si SteamCMD terminó correctamente, False en caso contrario.
    """
    download_dir.mkdir(parents=True, exist_ok=True)

    command = [
        STEAMCMD,
        "+force_install_dir", str(download_dir),
        "+login", "anonymous",
        "+workshop_download_item", PALWORLD_APP_ID, str(mod_id),
        "+quit",
    ]

    print("Executing SteamCMD:")
    print(command)

    result = subprocess.run(
        command,
        cwd="/home/steam/steamcmd",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    print("SteamCMD finished")
    print(result.returncode)

    if result.returncode != 0:
        print("SteamCMD failed.")
        print("----- STDOUT -----")
        print(result.stdout)
        print("----- STDERR -----")
        print(result.stderr)

    return result.returncode == 0