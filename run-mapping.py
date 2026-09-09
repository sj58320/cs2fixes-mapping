"""Launch CS2 Workshop Tools with Metamod and CS2Fixes enabled temporarily."""

import argparse
import os
from pathlib import Path
import shutil
import subprocess
import time

import psutil

from common import get_cs2_path, modify_gameinfo


def cs2_processes():
    return [p for p in psutil.process_iter(['name'])
            if (p.info.get('name') or '').lower() == 'cs2.exe']


def wait_until_dll_loaded(timeout):
    print('Waiting for cs2fixes.dll. This checks module presence, not plugin initialization.')
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        processes = cs2_processes()
        if not processes:
            return False
        for process in processes:
            try:
                if any(Path(module.path).name.lower() == 'cs2fixes.dll'
                       for module in process.memory_maps()):
                    return True
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                continue
        time.sleep(0.2)
    return False


def gameinfo_paths(root):
    return [(root / f'game/{directory}/gameinfo.gi',
             root / f'game/{directory}/gameinfo_cs2fixes_original.gi',
             root / f'game/{directory}/gameinfo_cs2fixes_temp.gi')
            for directory in ('csgo', 'csgo_core')]


def recover_gameinfo(paths):
    for original, backup, temp in paths:
        if original.is_symlink():
            if (original.resolve() != temp.resolve() or not backup.is_file()):
                raise RuntimeError('Unrecognized gameinfo symlink or missing backup; restore it manually.')
            original.unlink()
            shutil.move(backup, original)
        elif not original.exists() and backup.is_file():
            shutil.move(backup, original)
        if not original.is_file():
            raise RuntimeError('gameinfo.gi is missing. Verify game files in Steam before continuing.')
        if backup.exists():
            # Do not overwrite an ambiguous backup after an interrupted previous run.
            raise RuntimeError('A gameinfo_cs2fixes_original.gi backup remains; inspect it before retrying.')
        if temp.exists():
            temp.unlink()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cs2-path', type=Path, help='CS2 installation root (otherwise detected from Steam)')
    parser.add_argument('--timeout', type=float, default=120, help='Seconds to wait for CS2Fixes DLL (default: 120)')
    args = parser.parse_args()
    if args.timeout <= 0:
        parser.error('--timeout must be positive')
    detected = args.cs2_path or get_cs2_path()
    if not detected:
        raise RuntimeError('CS2 installation not found. Use --cs2-path.')
    root = Path(detected).resolve()
    tools = root / 'game/bin/win64'
    for required in (tools / 'csgocfg.exe',
                     root / 'game/csgo/addons/metamod/bin/win64/metamod.2.cs2.dll',
                     root / 'game/csgo/addons/cs2fixes/bin/win64/cs2fixes.dll'):
        if not required.is_file():
            raise RuntimeError(f'Missing {required.name}. Install Workshop Tools and run setup.py first.')
    if any((p.info.get('name') or '').lower() in ('cs2.exe', 'csgocfg.exe')
           for p in psutil.process_iter(['name'])):
        raise RuntimeError('Close CS2 and Workshop Tools before starting this launcher.')

    paths = gameinfo_paths(root)
    recover_gameinfo(paths)
    changed = []
    try:
        for original, backup, temp in paths:
            shutil.move(original, backup)
            changed.append((original, backup, temp))
            shutil.copy2(backup, temp)
            try:
                original.symlink_to(temp)
            except OSError as error:
                raise RuntimeError('Cannot create gameinfo symlinks. Enable Windows Developer Mode '
                                   'or run this launcher as Administrator.') from error
        modify_gameinfo(str(paths[0][0]), str(paths[1][0]))
        print('Opening Workshop Tools with -insecure -gpuraytracing...')
        subprocess.run([str(tools / 'csgocfg.exe'), '-insecure', '-gpuraytracing'],
                       cwd=tools, check=True)
        deadline = time.monotonic() + 10
        while not cs2_processes() and time.monotonic() < deadline:
            time.sleep(0.2)
        if not cs2_processes():
            raise RuntimeError('No CS2 process detected after closing the tools launcher.')
        if not wait_until_dll_loaded(args.timeout):
            raise RuntimeError('CS2Fixes DLL was not detected (timeout, exit, or access denied). '
                               'Check the game console and plugin errors.')
        print('CS2Fixes DLL detected. Confirm successful initialization with: meta list')
        time.sleep(3)
    finally:
        # Restore the original names even if launch or DLL detection fails.
        # The game may still hold temp files open; leave locked ones for next run.
        for original, backup, temp in reversed(changed):
            if os.path.lexists(original):
                original.unlink()
            shutil.move(backup, original)
            try:
                temp.unlink(missing_ok=True)
            except OSError:
                pass
        if changed:
            print('Original gameinfo files restored.')


if __name__ == '__main__':
    main()
