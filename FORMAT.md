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
