# JSON patch format (version 1)

One file is one patch for one version of one game.

| Field | Meaning |
| --- | --- |
| `format` | `1` |
| `console` | `ps5` (others when their recompiler reads this format) |
| `title_id`, `version` | the game and the exact version the patch was made for (`contentVersion` of `sce_sys/param.json`) |
| `game`, `name`, `description`, `author` | texts shown to the player |
| `tested` | where it was run and the result |
| `writes` | list of writes, all applied or none |

A write:

| Field | Meaning |
| --- | --- |
| `module` | file name of the module that holds the data (`eboot.bin`, `something.prx`); its converted form `<module>.guest.prx` is accepted too |
| `find_u32` or `find` | what identifies the place: little-endian 32-bit numbers, or hex text. Must occur exactly once in the module. A data constant, never code |
| `write_u32` or `write` | the new numbers or bytes |
| `at` | optional byte offset from the start of the match where the write goes (default 0) |

A tool applies a write to the module file (keeping a `.orig` copy) or to the loaded module in memory; the result is
the same bytes.

A **memory write** is for a value the game computes into its own data after it starts (a render size, for instance),
so there is nothing to find in the file. It has `offset` instead of a pattern:

| Field | Meaning |
| --- | --- |
| `module` | `eboot.bin` (the main module; offsets are counted from its load address, as in GoldHEN/Kyty cheat files) |
| `offset` | hex text, where the value lives |
| `find_u32` or `find` | the value the game writes there (only these bytes are replaced) |
| `write_u32` or `write` | our value |
| `hold` | `true`: the value is written again whenever the game writes its own value there |

Only the KytyPS5 path (`recomp_patch.py kyty`, KytyPS5 `--game-patch`) applies memory writes; `apply` refuses a patch
that has them.
