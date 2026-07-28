import sys

from app.models import Mod


def validate_config(config: dict) -> list[Mod]:
    """
    Valida la estructura del diccionario de configuración y convierte
    cada entrada en un objeto Mod.

    Args:
        config: Diccionario leído desde mods.yml.

    Returns:
        Lista de objetos Mod válidos.
        Termina con código de salida 1 si la estructura es incorrecta.
    """
    if not isinstance(config, dict) or "mods" not in config:
        print("Error: 'mods.yml' must contain a root key 'mods'.")
        sys.exit(1)

    if not isinstance(config["mods"], list):
        print("Error: 'mods' must be a list.")
        sys.exit(1)

    mods: list[Mod] = []

    for index, entry in enumerate(config["mods"]):
        if not isinstance(entry, dict):
            print(f"Error: item at index {index} is not a valid object.")
            sys.exit(1)

        if "id" not in entry or not isinstance(entry["id"], int):
            print(f"Error: item at index {index} is missing or has invalid 'id' (expected int).")
            sys.exit(1)

        if "enabled" not in entry or not isinstance(entry["enabled"], bool):
            print(f"Error: item at index {index} is missing or has invalid 'enabled' (expected bool).")
            sys.exit(1)

        mods.append(Mod(id=entry["id"], enabled=entry["enabled"]))

    return mods
