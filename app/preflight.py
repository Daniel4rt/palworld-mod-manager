"""
Comprobaciones previas al inicio del gestor de mods.

Verifica que el entorno esté correctamente configurado antes de
ejecutar cualquier operación sobre el servidor o los mods.
"""

import subprocess
from pathlib import Path


# Archivos/directorios que identifican un servidor de Palworld válido
_PALWORLD_MARKERS: list[str] = [
    "PalServer.sh",
    "PalServer",
    "Pal",
]


class PreflightError(Exception):
    """Se lanza cuando una comprobación previa falla."""
    pass


def check_server_directory(server_root: Path) -> None:
    """
    Verifica que el directorio del servidor exista y sea un servidor de Palworld válido.

    Detecta la presencia del servidor buscando marcadores conocidos de la
    instalación oficial de Palworld.

    Args:
        server_root: Ruta raíz del servidor.

    Raises:
        PreflightError: Si el directorio no existe o no parece un servidor de Palworld.
    """
    if not server_root.exists():
        raise PreflightError(
            f"Palworld server volume not found: '{server_root}'\n"
            "Make sure the volume is mounted correctly."
        )

    for marker in _PALWORLD_MARKERS:
        if (server_root / marker).exists():
            return

    raise PreflightError(
        f"Directory '{server_root}' exists but does not appear to be a valid "
        "Palworld server installation. Expected to find one of: "
        + ", ".join(_PALWORLD_MARKERS)
    )


def check_required_directories(server_root: Path) -> None:
    """
    Crea las carpetas oficiales de mods si no existen.

    Solo crea:
        <server_root>/Mods/
        <server_root>/Mods/Workshop/

    Args:
        server_root: Ruta raíz del servidor.
    """
    (server_root / "Mods").mkdir(exist_ok=True)
    (server_root / "Mods" / "Workshop").mkdir(exist_ok=True)


def check_steamcmd_installation() -> None:
    """
    Verifica que SteamCMD esté instalado y sea ejecutable.

    Ejecuta 'steamcmd +quit' para confirmar que responde correctamente.

    Raises:
        PreflightError: Si steamcmd no se encuentra o no responde.
    """
    result = subprocess.run(
        ["steamcmd", "+quit"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if result.returncode != 0:
        raise PreflightError(
            f"SteamCMD was found but exited with code {result.returncode}.\n"
            f"stderr: {result.stderr.strip()}"
        )
