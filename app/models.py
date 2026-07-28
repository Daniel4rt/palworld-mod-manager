from dataclasses import dataclass
from pathlib import Path


@dataclass
class Mod:
    id: int
    enabled: bool


@dataclass
class InstalledMod:
    id: int
    package_name: str
    content_hash: str


@dataclass
class ModInfo:
    workshop_id: int
    package_name: str
    content_hash: str
    info_json: Path
    root_directory: Path
