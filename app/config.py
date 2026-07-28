import sys

import yaml


def load_config(path: str) -> dict:
    """
    Lee el archivo YAML y devuelve el diccionario sin validar.

    Args:
        path: Ruta al archivo mods.yml.

    Returns:
        Diccionario con el contenido del archivo.
        Termina con código de salida 1 si el archivo no existe o el YAML es inválido.
    """
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: configuration file not found: '{path}'")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: invalid YAML in '{path}': {e}")
        sys.exit(1)
