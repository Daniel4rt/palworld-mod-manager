import hashlib
from pathlib import Path


def calculate_directory_hash(directory: Path) -> str:
    """
    Calcula un hash SHA-256 único representando el contenido completo de un directorio.

    Recorre recursivamente todos los archivos, los ordena por ruta relativa
    para garantizar determinismo, y combina su contenido en un único digest.

    Args:
        directory: Directorio raíz del mod.

    Returns:
        Hash SHA-256 en formato hexadecimal.
    """
    hasher = hashlib.sha256()

    files = sorted(
        (p for p in directory.rglob("*") if p.is_file()),
        key=lambda p: p.relative_to(directory).as_posix(),
    )

    for file_path in files:
        hasher.update(file_path.read_bytes())

    return hasher.hexdigest()
