<p align="center">
  <img src="https://rmontor.com/images/e7d29dd1-3b55-4ef6-b2ee-958005d477be.png" alt="Palworld Mod Manager" width="900">
</p>

<p align="center">
  <a href="https://github.com/Daniel4rt/palworld-mod-manager/releases">
    <img src="https://img.shields.io/github/v/release/Daniel4rt/palworld-mod-manager?color=blue">
  </a>
  <img src="https://img.shields.io/github/stars/Daniel4rt/palworld-mod-manager?style=flat">
  <img src="https://img.shields.io/github/issues/Daniel4rt/palworld-mod-manager">
  <img src="https://img.shields.io/github/license/Daniel4rt/palworld-mod-manager">
  <img src="https://img.shields.io/badge/python-3.12-blue">
  <img src="https://img.shields.io/badge/docker-ready-blue?logo=docker">
</p>

A Docker-integrated mod manager for Palworld servers, designed to work directly
inside the
[`thijsvanloef/palworld-server-docker`](https://github.com/thijsvanloef/palworld-server-docker)
container.

The manager automatically synchronizes Steam Workshop mods before the server
starts, ensuring your installation is always up to date.

---

# Features

- Install Steam Workshop mods automatically
- Update existing mods
- Remove obsolete mods
- Enable or disable mods without deleting them
- Automatically regenerate `PalModSettings.ini`
- Runs automatically before every server startup
- Fully integrated into the original `thijsvanloef/palworld-server-docker` image

---

# Requirements

Before installing Palworld Mod Manager, make sure your server is already
working correctly using the official
[`thijsvanloef/palworld-server-docker`](https://github.com/thijsvanloef/palworld-server-docker)
repository.

The Mod Manager modifies the original Docker image, so it must be rebuilt once
the files have been added.

---

# Installation

## 1. Clone the original server

```bash
git clone https://github.com/thijsvanloef/palworld-server-docker.git
cd palworld-server-docker
```

---

## 2. Copy the Mod Manager files

Copy the following into the server project:

```text
app/
requirements.txt
mods.yml
Dockerfile
scripts/start.sh
```

The provided `Dockerfile` and `start.sh` already contain the required changes to
execute the Mod Manager automatically before starting Palworld.

---

## 3. Configure your mods

Edit:

```text
mods.yml
```

Example:

```yaml
mods:
  - id: 3812345678
    enabled: true

  - id: 3823456789
    enabled: true

  - id: 3834567890
    enabled: false
```

Use:

```yaml
enabled: false
```

to temporarily disable a mod without removing it from the configuration.

---

## 4. Rebuild the Docker image

Since the Mod Manager is integrated into the container, Docker must rebuild the
image.

```bash
docker compose build
```

If you want a completely clean rebuild:

```bash
docker compose build --no-cache
```

---

## 5. Start the server

```bash
docker compose up -d
```

The startup sequence is now:

```text
docker compose up -d
        │
        ▼
Palworld Container
        │
        ▼
Palworld Mod Manager
        │
        ▼
Install / Update / Remove Mods
        │
        ▼
Generate PalModSettings.ini
        │
        ▼
Palworld Server
```

The server will only start after the Mod Manager finishes successfully.

---

# Updating Mods

Whenever you want to add, remove or update Workshop mods:

1. Edit:

```text
mods.yml
```

2. Rebuild the image:

```bash
docker compose build
```

3. Restart the server:

```bash
docker compose up -d
```

During startup the Mod Manager will:

- Install new Workshop mods
- Update existing mods
- Remove deleted mods
- Regenerate `PalModSettings.ini`
- Launch the Palworld server

No additional commands are required.

---

# mods.yml format

```yaml
mods:
  - id: 3812345678
    enabled: true

  - id: 3823456789
    enabled: true

  - id: 3834567890
    enabled: false
```

---

# Directory Structure

```text
palworld-server-docker/
├── app/
├── mods.yml
├── requirements.txt
├── Dockerfile
├── scripts/
│   └── start.sh
├── cache/
├── downloads/
└── palworld/
```

---

# How it works

On every container startup the Mod Manager performs the following steps:

1. Read `mods.yml`
2. Compare the installed Workshop mods
3. Download new mods
4. Update outdated mods
5. Remove obsolete mods
6. Generate `PalModSettings.ini`
7. Start the Palworld dedicated server

This guarantees the server always starts with the exact mod configuration
defined in `mods.yml`.

---

# License

This project follows the license of this repository.

Palworld and all related assets belong to Pocketpair.