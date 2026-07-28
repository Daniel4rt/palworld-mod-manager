# palworld-mod-manager
<<<<<<< HEAD

A Docker-based mod manager for Palworld servers, designed to work alongside
[`thijsvanloef/palworld-server-docker`](https://github.com/thijsvanloef/palworld-server-docker)
without modifying it.

## Requirements

- Docker
- Docker Compose

## Usage

1. Edit `mods.yml` with the Workshop IDs you want to install.
2. Run:

```bash
docker compose up -d
```

3. To add, remove or update mods, edit `mods.yml` and run the same command again.

## Docker Compose

```
docker compose up -d
        │
        ▼
mod-manager
        │
        ▼
Instala / actualiza / elimina mods
        │
        ▼
Exit 0
        │
        ▼
Palworld Server
```

The `mod-manager` service runs first. Only if it exits with code 0 will the
`palworld` server container start. This guarantees the server always boots
with the correct mods already in place.

The only file you need to modify is:

```text
mods.yml
```

After editing it, apply the changes by running:

```bash
docker compose up -d
```

The manager will install new mods, update changed ones, remove mods that are
no longer listed, regenerate `PalModSettings.ini`, and then hand off to the
server automatically.

## mods.yml format

```yaml
mods:
  - id: 3812345678
    enabled: true

  - id: 3823456789
    enabled: true

  - id: 3834567890
    enabled: false
```

Set `enabled: false` to disable a mod without removing it from the list.
=======
A mod manager for docker compose palworld servers
>>>>>>> d4ab95657fc17cd9688b07921a608dc21c7a5b31
