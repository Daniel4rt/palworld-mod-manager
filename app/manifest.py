from pathlib import Path

from app.models import ModInfo


def generate_palmodsettings(mods: list[ModInfo], server_root: Path) -> Path:
    """
    Genera el archivo PalModSettings.ini con la lista de mods activos.

    Args:
        mods: Lista de ModInfo instalados correctamente, en orden de mods.yml.
        server_root: Ruta raíz del servidor de Palworld.

    Returns:
        Ruta al archivo PalModSettings.ini generado.
    """
    mods_dir = server_root / "Mods"
    mods_dir.mkdir(parents=True, exist_ok=True)

    output_path = mods_dir / "PalModSettings.ini"

    # Deduplicar manteniendo el orden original
    seen: set[str] = set()
    unique_package_names: list[str] = []
    for mod in mods:
        if mod.package_name not in seen:
            seen.add(mod.package_name)
            unique_package_names.append(mod.package_name)

    lines: list[str] = [
        "[PalModSettings]",
        "bGlobalEnableMod=True",
        "",
    ]
    for package_name in unique_package_names:
        lines.append(f"ActiveModList={package_name}")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    return output_path
