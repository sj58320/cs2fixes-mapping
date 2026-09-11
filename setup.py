"""Install pinned official Windows packages for local CS2Fixes mapping."""

import argparse
from datetime import datetime, timezone
import hashlib
import io
from pathlib import Path, PurePosixPath
import shutil
import zipfile

import psutil
import requests

from common import get_cs2_path

# Keep this pair explicit: CS2Fixes v1.20.1 requires Metamod build 1411 or earlier.
# Do not automatically upgrade Metamod to a KHook-based release.
PACKAGES = (
    (
        "https://github.com/alliedmodders/metamod-source/releases/download/"
        "2.0.0.1403/mmsource-2.0.0-git1403-windows.zip",
        "55aebd32a7811cfad682c8e133d01bba2d8d617654b07c4a14fb309e25f20b86",
        "addons/metamod/bin/win64/metamod.2.cs2.dll",
    ),
    (
        "https://github.com/Source2ZE/CS2Fixes/releases/download/"
        "v1.20.1/CS2Fixes-v1.20.1-windows.zip",
        "3ea9607b6a6713a10de67c7b7787eaf4915cf9362a2d76797e7dc340e6172ca2",
        "addons/cs2fixes/bin/win64/cs2fixes.dll",
    ),
)


def download_package(url, sha256, required_file):
    print(f"Downloading {url.rsplit('/', 1)[-1]}...")
    response = requests.get(url, timeout=(15, 120))
    response.raise_for_status()
    data = response.content
    if hashlib.sha256(data).hexdigest() != sha256:
        raise RuntimeError("Package SHA-256 mismatch; installation cancelled.")
    archive = zipfile.ZipFile(io.BytesIO(data))
    if required_file not in archive.namelist():
        raise RuntimeError(f"Package is missing {required_file}")
    # Validate all paths before writing any files.
    for item in archive.infolist():
        name = PurePosixPath(item.filename)
        if (name.is_absolute() or '..' in name.parts or '\\' in item.filename
                or ':' in item.filename or not name.parts
                or name.parts[0] not in ('addons', 'cfg', 'materials', 'particles',
                                        'soundevents', 'sounds')):
            raise RuntimeError(f"Unexpected archive path: {item.filename}")
    return archive


def preserve_config(relative):
    path = relative.as_posix()
    return (path.startswith('cfg/') or path.startswith('addons/cs2fixes/configs/')
            or path == 'addons/metamod/metaplugins.ini')


def install_packages(archives, csgo, backup):
    # Resolve paths first so an existing symlink cannot redirect writes outside CS2.
    files = []
    for archive in archives:
        for item in archive.infolist():
            if item.is_dir():
                continue
            relative = Path(*PurePosixPath(item.filename).parts)
            target = csgo / relative
            if not target.resolve().is_relative_to(csgo.resolve()):
                raise RuntimeError(f"Install path escapes game/csgo: {relative}")
            if target.exists() and preserve_config(relative):
                print(f"Keeping existing config: {relative.as_posix()}")
                continue
            files.append((archive, item, relative, target))

    for archive, item, relative, target in files:
        if target.exists():
            saved = backup / relative
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(target, saved)
        target.parent.mkdir(parents=True, exist_ok=True)
        with archive.open(item) as source, target.open('wb') as destination:
            shutil.copyfileobj(source, destination)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cs2-path', type=Path, help='CS2 installation root (otherwise detected from Steam)')
    args = parser.parse_args()
    detected = args.cs2_path or get_cs2_path()
    if not detected:
        raise RuntimeError('CS2 installation not found. Use --cs2-path.')
    root = Path(detected).resolve()
    if not (root / 'game/bin/win64/cs2.exe').is_file():
        raise RuntimeError('The selected directory is not a Windows CS2 installation.')
    if any((p.info.get('name') or '').lower() in ('cs2.exe', 'csgocfg.exe')
           for p in psutil.process_iter(['name'])):
        raise RuntimeError('Close CS2 and Workshop Tools before installation.')

    print('Installing Metamod 2.0.0-dev+1403 and official CS2Fixes v1.20.1.')
    print('No KZ FGD/assets or custom ConVar presets will be installed.')
    archives = []
    try:
        # Download and verify both packages before touching the game directory.
        archives = [download_package(*package) for package in PACKAGES]
        backup = Path(__file__).resolve().parent / 'backups' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        csgo = root / 'game/csgo'
        install_packages(archives, csgo, backup)
        asset = csgo / 'readonly_tools_asset_info.bin'
        if asset.is_file():
            target = csgo / 'addons/metamod/readonly_tools_asset_info.bin'
            if target.exists():
                saved = backup / 'addons/metamod/readonly_tools_asset_info.bin'
                saved.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, saved)
            shutil.copy2(asset, target)
        else:
            print('Warning: tools asset index missing. Install CS2 Workshop Tools before using Hammer.')
        (root / 'content/csgo/addons/metamod').mkdir(parents=True, exist_ok=True)
        if backup.exists():
            print('Replaced files were backed up under this tool\'s backups/ directory.')
    finally:
        for archive in archives:
            archive.close()
    print('Setup complete. Existing configs were preserved; new configs use upstream defaults.')
    print('No gameinfo.gi, FGD, particle editor or CSM settings were changed by setup.')


if __name__ == '__main__':
    main()
