"""recomp_patch.py: applies the JSON patches of this repository (FORMAT.md) without the launcher.

  python tools/recomp_patch.py apply  <patch.json> <game folder>   patch the module files in place (a .orig copy
                                                                   of each changed file is kept beside it)
  python tools/recomp_patch.py revert <game folder>                put every .orig copy back
  python tools/recomp_patch.py kyty   <patch.json> <output.json>   write the patch as a cheat file for
                                                                   kyty_emulator --game-patch (the game is not needed)

<game folder> is where the converted modules are, e.g. an AnyPS5 port's build/out/app0. Never point it at your
only copy of a dump: the files are changed in place.
"""
import json
import shutil
import struct
import sys
from pathlib import Path


def pattern(write, key):
    """The bytes of "<key>" (hex text) or "<key>_u32" (little-endian 32-bit numbers)."""
    if key in write:
        return bytes.fromhex(write[key])
    return struct.pack(f'<{len(write[key + "_u32"])}I', *write[key + '_u32'])


def module_files(folder, module):
    """The module itself or its converted form (<module>.guest.prx), anywhere under the folder."""
    names = {module.lower(), module.lower() + '.guest.prx'}
    return [p for p in Path(folder).rglob('*') if p.name.lower() in names and p.is_file()]


def apply(patch, folder, log=print):
    """Applies every write of the patch; raises ValueError (nothing changed) when one does not fit."""
    plan = []
    for write in patch['writes']:
        find, new = pattern(write, 'find'), pattern(write, 'write')
        at = int(write.get('at', 0))
        files = module_files(folder, write['module'])
        if len(files) != 1:
            raise ValueError(f'{write["module"]}: {len(files)} files with that name under {folder}')
        original = Path(str(files[0]) + '.orig')
        data = (original if original.is_file() else files[0]).read_bytes()
        if data.count(find) != 1:
            raise ValueError(f'{write["module"]}: the pattern occurs {data.count(find)} times (another game version?)')
        plan.append((files[0], data.find(find) + at, new))
    for path, offset, new in plan:
        original = Path(str(path) + '.orig')
        if not original.is_file():
            shutil.copy2(path, original)
        data = bytearray(path.read_bytes())
        data[offset:offset + len(new)] = new
        path.write_bytes(data)
        log(f'{patch["name"]}: {path.name} +0x{offset:x}, {len(new)} bytes')


def revert(folder, log=print):
    for original in Path(folder).rglob('*.orig'):
        shutil.copy2(original, str(original)[:-5])
        original.unlink()
        log(f'restored {original.name[:-5]}')


def kyty(patch):
    """The same patch as a GoldHEN-style cheat file; the emulator finds the module by the pattern."""
    memory = []
    for index, write in enumerate(patch['writes']):
        find, new = pattern(write, 'find'), pattern(write, 'write')
        at = int(write.get('at', 0))
        on = find[:at] + new + find[at + len(new):]
        memory.append({'offset': hex(0x20000000 + index * 0x1000), 'off': find.hex(), 'on': on.hex()})
    return {'name': patch['game'], 'id': patch['title_id'], 'version': patch['version'], 'process': 'eboot.bin',
            'mods': [{'name': patch['name'], 'enabled': True, 'memory': memory}]}


def main():
    args = sys.argv[1:]
    if len(args) == 3 and args[0] == 'apply':
        apply(json.loads(Path(args[1]).read_text(encoding='utf-8')), args[2])
    elif len(args) == 2 and args[0] == 'revert':
        revert(args[1])
    elif len(args) == 3 and args[0] == 'kyty':
        Path(args[2]).write_text(json.dumps(kyty(json.loads(Path(args[1]).read_text(encoding='utf-8'))), indent=2), encoding='utf-8')
    else:
        raise SystemExit(__doc__)


if __name__ == '__main__':
    try:
        main()
    except ValueError as error:
        raise SystemExit(f'not applied: {error}')
