"""
Prueba de integración temporal con Steam Workshop.

Ejecutar directamente:
    python test_steam_integration.py

No forma parte del flujo principal del gestor.
No modifica el servidor, el cache ni PalModSettings.ini.
"""

import json
import subprocess
import time
from pathlib import Path

PALWORLD_APP_ID: str = "2394010"
DOWNLOAD_DIR: Path = Path(__file__).parent / "downloads"


def print_section(title: str) -> None:
    print(f"\n{'─' * 60}")
    print(f"  {title}")
    print(f"{'─' * 60}\n")


def print_directory_tree(root: Path, prefix: str = "", depth: int = 8) -> None:
    """Imprime el árbol de directorios hasta la profundidad indicada."""
    if depth == 0:
        return

    entries = sorted(root.iterdir()) if root.exists() else []

    for i, entry in enumerate(entries):
        connector = "└── " if i == len(entries) - 1 else "├── "
        suffix = "/" if entry.is_dir() else ""
        print(f"{prefix}{connector}{entry.name}{suffix}")

        if entry.is_dir():
            extension = "    " if i == len(entries) - 1 else "│   "
            print_directory_tree(entry, prefix + extension, depth - 1)


def format_size(total_bytes: int) -> str:
    """Devuelve el tamaño en formato legible."""
    if total_bytes >= 1_048_576:
        return f"{total_bytes / 1_048_576:.1f} MB"
    if total_bytes >= 1_024:
        return f"{total_bytes / 1_024:.1f} KB"
    return f"{total_bytes} bytes"


def run_download(workshop_id: str) -> bool:
    """Ejecuta SteamCMD y descarga el Workshop Item. Devuelve True si tuvo éxito."""
    DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

    command = [
        "steamcmd",
        "+force_install_dir", str(DOWNLOAD_DIR),
        "+login", "anonymous",
        "+workshop_download_item", PALWORLD_APP_ID, workshop_id,
        "+quit",
    ]

    print_section("Ejecutando SteamCMD")
    print(f"Comando:\n  {' '.join(command)}\n")

    inicio = time.perf_counter()

    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    elapsed = time.perf_counter() - inicio

    print(f"Código de salida : {result.returncode}")
    print(f"Tiempo           : {elapsed:.2f} segundos\n")

    if result.stdout.strip():
        print("stdout:\n")
        print(result.stdout)

    if result.stderr.strip():
        print("stderr:\n")
        print(result.stderr)

    return result.returncode == 0


def inspect_download(workshop_id: str) -> None:
    """Muestra el árbol, estadísticas y todos los Info.json encontrados."""

    # Verificar que SteamCMD realmente descargó algo
    all_files = [p for p in DOWNLOAD_DIR.rglob("*") if p.is_file()]

    print_section("Archivos descargados")

    if not all_files:
        print("⚠ SteamCMD terminó correctamente pero no descargó ningún archivo.")
        return

    total_bytes = sum(p.stat().st_size for p in all_files)
    print(f"Archivos encontrados : {len(all_files)}")
    print(f"Peso total           : {format_size(total_bytes)}\n")

    print(f"{DOWNLOAD_DIR.name}/")
    print_directory_tree(DOWNLOAD_DIR)

    # Buscar Info.json desde la raíz de descargas (sin asumir ruta)
    print_section("Buscando Info.json")

    matches = list(DOWNLOAD_DIR.rglob("Info.json"))

    if not matches:
        print("✗ No se encontró ningún Info.json.")
        return

    print(f"Se encontraron {len(matches)} Info.json\n")

    for index, info_json_path in enumerate(matches, start=1):
        size_bytes = info_json_path.stat().st_size
        rel_path = info_json_path.relative_to(DOWNLOAD_DIR)

        print(f"{index}) {rel_path}")
        print(f"   Tamaño: {format_size(size_bytes)}")

        try:
            with info_json_path.open("r", encoding="utf-8") as f:
                data = json.load(f)

            print(f"   PackageName: {data.get('PackageName', '(no encontrado)')}")
            print(f"\n   Contenido completo:\n")
            print(json.dumps(data, indent=4, ensure_ascii=False))
        except (json.JSONDecodeError, OSError) as e:
            print(f"   ✗ Error al leer el archivo: {e}")

        if index < len(matches):
            print()

    # Indicar dónde quedó el mod
    print_section("Ruta de descarga del mod")
    print(f"SteamCMD descargó el mod en:\n")
    for match in matches:
        print(f"  {match.parent}")


def main() -> None:
    workshop_id = input("Workshop ID: ").strip()

    if not workshop_id.isdigit():
        print("Error: el Workshop ID debe ser un número entero.")
        return

    print(f"\nPrueba de integración — Workshop ID: {workshop_id}")
    print(f"App ID de Palworld  : {PALWORLD_APP_ID}")
    print(f"Directorio de descarga: {DOWNLOAD_DIR.resolve()}")

    success = run_download(workshop_id)

    if not success:
        print_section("Resultado")
        print("✗ SteamCMD falló. Revisa el stdout/stderr arriba.")
        return

    inspect_download(workshop_id)

    print_section("Resultado")
    print("✓ Prueba completada. No se modificó el servidor ni el cache.")


if __name__ == "__main__":
    main()
