# recomp-patches

Patches and cheats we wrote for games running through our recompilers and emulator forks
([PS2Recomp](https://github.com/batatinhafcbatatinha-pixel/PS2Recomp),
[AnyPS5](https://github.com/batatinhafcbatatinha-pixel/AnyPS5),
[KytyPS5](https://github.com/batatinhafcbatatinha-pixel/KytyPS5) and the others the
[port launcher](https://github.com/batatinhafcbatatinha-pixel/port-installer) knows). Only our own work goes here:
the community repositories (PCSX2 patches, CWCheat, Xenia game patches, GoldHEN) stay where they are and the
launcher already lists them.

Nothing in this repository is game code or game data. A patch holds where to write and the values we write.

## What is here

| Console | Game | Patch | File |
| --- | --- | --- | --- |
| PS2 | The Sopranos: Road to Respect (SLUS-21388) | 60 fps (menus 60; 3D scenes stay near 30 for now) | `ps2/SLUS-21388_sopranos-road-to-respect.pnach` |
| PS5 | Control Ultimate Edition (PPSA01949, 01.000.004) | Output and render 854x480 (not tested) | `ps5/PPSA01949/render-480p-output-480p.json` |
| PS5 | Control Ultimate Edition (PPSA01949, 01.000.004) | Output and render 1280x720 (tested: 59.6 fps in the KytyPS5 fork on an RTX 3050 laptop GPU) | `ps5/PPSA01949/render-720p-output-720p.json` |
| PS5 | Control Ultimate Edition (PPSA01949, 01.000.004) | Output and render 1920x1080 (not tested with these values) | `ps5/PPSA01949/render-1080p-output-1080p.json` |
| PS5 | Grand Theft Auto V (PPSA04264, 01.011.001) | Output and render 1280x720, Performance mode (tested: 60 fps in the KytyPS5 fork on an RTX 3050 laptop GPU; 40.7 fps in AnyPS5) | `ps5/PPSA04264/render-720p-output-720p.json` |
| PS5 | Grand Theft Auto V (PPSA04264, 01.011.001) | Output and render 1920x1080, Performance mode (tested: about 47 fps in AnyPS5 on an RTX 3050 laptop GPU) | `ps5/PPSA04264/render-1080p-output-1080p.json` |

## Using it

**Port launcher.** Select the game, open **Patches** (Game menu), choose **Add repository** and paste
`batatinhafcbatatinha-pixel/recomp-patches/ps2` (PS2 games) or `batatinhafcbatatinha-pixel/recomp-patches/ps5`
(PS5 games). PS2 entries are applied by **Apply** (`tools/ps2port hotpatch`). PS5 entries are listed; applying them
from the launcher needs a launcher and AnyPS5 `tools/ps5port` with support for this repository's JSON format, which
is not released yet. Until then use the tool below.

**AnyPS5 `tools/ps5port`** (memory writes included): put the JSON file in the port's `patches` folder
(`.local/ports/<TITLE ID>/patches/`); it is applied at every PLAY and removing the file undoes it.

**By hand, AnyPS5 port** (the converted modules in `build/out/app0`; a rebuild of the port undoes it):

    python tools/recomp_patch.py apply ps5/PPSA01949/render-720p-output-720p.json <port>/build/out/app0
    python tools/recomp_patch.py revert <port>/build/out/app0

**By hand, KytyPS5** (nothing on disk changes, the emulator patches the loaded module):

    python tools/recomp_patch.py kyty ps5/PPSA01949/render-720p-output-720p.json control-720p.json
    kyty_emulator --game <dump> --game-patch control-720p.json

## Layout and formats

- `ps2/<SERIAL>_<name>.pnach`: PCSX2's pnach text (`patch=1,EE,<address>,extended,<value>`), one `[Title]` section
  per patch with `author=` and `description=`.
- `ps5/<TITLE ID>/<name>.json`: see [FORMAT.md](FORMAT.md).
- Other consoles get a folder in the format their recompiler reads when we have a patch for them.

Each patch is for the exact game version it names. A pattern that is not found exactly once means another version:
the tools refuse to write.

## Rules for contributions

- Your own work only, with what it does, the game version and where it was tested.
- No game code, no disassembly, no dumps. Search patterns must be data constants (numbers such as a resolution or
  a frame-rate flag), short, never instructions.
