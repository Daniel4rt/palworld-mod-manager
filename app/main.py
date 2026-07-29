# palworld-mod-manager
# Entry point of the application

import sys
import traceback
from pathlib import Path

from app.paths import MODS_CONFIG_PATH, CACHE_PATH, DOWNLOAD_DIR, SERVER_ROOT
from app.config import load_config
from app.validator import validate_config
from app.cache import load_cache, save_cache, is_update_required
from app.models import Mod, InstalledMod, ModInfo
from app.steam import check_steamcmd, download_mod, PALWORLD_APP_ID
from app.inspector import inspect_mod, InvalidModError
from app.installer import install_mod
from app.manifest import generate_palmodsettings
from app.sync import synchronize_installed_mods
from app.preflight import (
    check_server_directory,
    check_required_directories,
    check_steamcmd_installation,
    PreflightError,
)

# Activa el modo de prueba: descarga e inspecciona mods pero no modifica el servidor.
DRY_RUN: bool = False


def _print_mod_list(mod_ids: list[int]) -> None:
    """Imprime una lista de IDs, o '(none)' si está vacía."""
    if mod_ids:
        for mod_id in mod_ids:
            print(f"- {mod_id}")
    else:
        print("(none)")


def _run_preflight() -> None:
    """
    Ejecuta todas las comprobaciones previas al inicio.

    Termina con código 1 si alguna falla.
    """
    print("Running preflight checks...\n")

    try:
        check_steamcmd_installation()
        print("✓ SteamCMD detected")
    except PreflightError as e:
        print(f"✗ SteamCMD check failed: {e}")
        sys.exit(1)

    try:
        check_server_directory(SERVER_ROOT)
        print("✓ Palworld server detected")
    except PreflightError as e:
        print(f"✗ Server check failed: {e}")
        sys.exit(1)

    check_required_directories(SERVER_ROOT)
    print("✓ Mods directory ready\n")


def main() -> None:
    """Lee la configuración, compara contra el cache y gestiona la instalación de mods."""
    if DRY_RUN:
        print("*** DRY RUN ENABLED ***\n")

    _run_preflight()

    # Leer y validar configuración
    config = load_config(str(MODS_CONFIG_PATH))
    mods: list[Mod] = validate_config(config)

    # IDs solicitados (solo habilitados)
    requested_ids: list[int] = [mod.id for mod in mods if mod.enabled]

    # Leer cache e indexar por ID
    cache = load_cache(str(CACHE_PATH))
    cache_index: dict[int, InstalledMod] = {
        entry["id"]: InstalledMod(
            id=entry["id"],
            package_name=entry["package_name"],
            content_hash=entry["content_hash"],
        )
        for entry in cache.get("mods", [])
    }

    # Mostrar mods solicitados
    print("Mods requested:\n")
    _print_mod_list(requested_ids)

    if not requested_ids:
        return

    # Contadores para el resumen final
    count_downloaded = 0
    count_installed = 0
    count_updated = 0
    count_skipped = 0
    count_failed = 0

    # Lista de ModInfo de todos los mods habilitados procesados correctamente
    final_infos: list[ModInfo] = []

    print()
    for mod_id in requested_ids:
        print(f"Downloading {mod_id}... ", end="", flush=True)
        success = download_mod(mod_id, DOWNLOAD_DIR)
        print("OK" if success else "FAILED")

        if not success:
            count_failed += 1
            continue

        count_downloaded += 1

        mod_directory = DOWNLOAD_DIR / "steamapps" / "workshop" / "content" / PALWORLD_APP_ID / str(mod_id)

        try:
            info = inspect_mod(mod_directory, mod_id)
        except InvalidModError as e:
            print(f"\n  Invalid Workshop mod:\n  {e}\n")
            count_failed += 1
            continue

        cached_entry: InstalledMod | None = cache_index.get(mod_id)

        if not is_update_required(cached_entry, info):
            print(f"  Already up to date: {info.package_name}\n")
            count_skipped += 1
            final_infos.append(info)
            continue

        is_update = cached_entry is not None

        print(f"\n  PackageName  : {info.package_name}")
        print(f"  ContentHash  : {info.content_hash}\n")

        if DRY_RUN:
            print("  [DRY RUN] Skipping install.\n")
            count_installed += 1
            continue

        print("  Installing...")
        destination = install_mod(info, SERVER_ROOT)
        print(f"\n  Destination  : {destination}")
        print("  Installed successfully.\n")

        if is_update:
            count_updated += 1
        else:
            count_installed += 1

        final_infos.append(info)

    if DRY_RUN:
        print("*** DRY RUN: server files were not modified. ***\n")
    else:
        # Regenerar PalModSettings.ini si hay mods válidos
        if final_infos:
            print("Generating PalModSettings.ini...")
            ini_path = generate_palmodsettings(final_infos, SERVER_ROOT)
            print(f"\nGenerated:\n{ini_path}\n")

        # Sincronizar: eliminar mods que ya no están en mods.yml
        current_cache: list[InstalledMod] = list(cache_index.values())
        removed_ids = synchronize_installed_mods(mods, SERVER_ROOT, current_cache)

        if removed_ids:
            print("Removed:\n")
            for mod_id in removed_ids:
                print(f"- {mod_id}")
            print()

        # Guardar cache completo (solo mods habilitados inspeccionados correctamente)
        new_cache = [
            InstalledMod(
                id=info.workshop_id,
                package_name=info.package_name,
                content_hash=info.content_hash,
            )
            for info in final_infos
        ]
        save_cache(str(CACHE_PATH), new_cache)

    # Resumen final
    print("Summary\n")
    print(f"  Downloaded : {count_downloaded}")
    print(f"  Installed  : {count_installed}")
    print(f"  Updated    : {count_updated}")
    if not DRY_RUN:
        removed_count = len(removed_ids) if "removed_ids" in dir() else 0
        print(f"  Removed    : {removed_count}")
    print(f"  Skipped    : {count_skipped}")
    print(f"  Failed     : {count_failed}")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        print("\n========== UNHANDLED EXCEPTION ==========\n")
        traceback.print_exc(file=sys.stdout)
        print("\n=========================================\n")
        sys.exit(1)

