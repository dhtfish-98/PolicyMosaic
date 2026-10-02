# Current validation — 1.0.2

Date: 2026-10-02. Python 3.12.13, macOS ARM64.

## Evidence

- **150 tests passed**: 40 retained contracts plus 110 current boundary/process/format tests. Tests use owned finite binary fixtures; they do not query a device or download firmware.
- Fixed upstream archive: commit `3dc6582f7f7d137adaa115f635eb5fc8e8da91f5`, tree `1cac93e4419f6de08e6a094cfe2c530dea897696`. The archive's original files are checked separately from decoder outputs/logs.
- **956 deterministic observations**: 927 equal; 29 exact checked changes. Those changes are 20 incomplete/unknown header cases, 8 incomplete/malformed string cases, and one helper result missing its output path. Every other observation must match; the comparison does not blanket-ignore exceptions.
- **8 normal SBPL/C reports** independently compared byte for byte against fixed upstream: single profiles, terminal actions, a nonterminal graph and a normal bundle. Every compared report matches. These are finite examples, not coverage of all policy expressions.
- Current macOS clang successfully generated a **50,208-byte 64-bit Mach-O dynamic library** for the owned minimal profile. Header and file type were verified; the resulting binary was **not executed**.
- Actual child-process tests cover exit failure, bounded stdout, invalid UTF-8, deadlines and a parent exiting while a descendant holds its pipe open.
- CLI tests cover all 40 short-input boundaries of the owned profile, normal SBPL/C output, bundle stride, directory/FIFO/symlink rejection, output traversal and collisions, existing files, graph cycles/references, duplicate/injectable operation labels, and input immutability.
- Bytecode tests cover operands, malformed UTF-8, string variables/concat/reset, cyclic jump walks, independent regex state, output/work/depth limits and already-seen shared nodes. C literal tests cover control bytes, quotes and modifier payloads.

`CURRENT_VALIDATION.json` records this source's audit and test evidence. `SOURCE_AUDIT.json` identifies every current Python module and its scope. `DELIVERY_VALIDATION.json`, old name/file maps and v1.0.0/v1.0.1 assets are historical records of their own code, not current-package verification.

## Resource and compatibility changes

| Boundary | Current limit / behavior |
| --- | --- |
| Profile snapshot | 64 MiB; regular file, final symlink/FIFO/directory rejected |
| Operations catalog | 1 MiB; unique labels, exact count, bounded ASCII grammar |
| Node table / regex records | 4,096 per analysis graph; invalid references rejected |
| Bundle count | 1,024 |
| Graph / nested string depth | 128 |
| Graph work | 2,000,000 function/loop steps with a cooperative 20-second deadline |
| Graph expansion | 16 MiB text/bytes or 65,536 list/tuple items for guarded operations |
| Reports | 16 MiB per report, 64 MiB cumulatively per decoder CLI run; exclusive 0600 files; exit 2 on incomplete work |
| External helpers | No shell; concurrent pipe reads; 30–300-second mode deadlines and bounded captured output |
| Firmware profile dump | 64 MiB; exact returned byte count |
| Native emulation | Separate process in firmware flow, 2-second native timeout, 65,536 instructions, 1 MiB dynamically mapped memory |

The legacy string interpreter silently returned an empty result for the listed incomplete programs; these now fail explicitly. Unknown headers and regex opcodes, zero-length underflow, out-of-range references and graph cycles also fail. The current profile listing uses the computed row stride rather than the old hard-coded 376-byte stride. Fresh per-operation graph copies avoid mutation leaking into another operation. Conversion state uses a scoped context instead of incorrect/shared `base_addr` assignments.

The actual sandboxed local Unicorn probe terminated with SIGILL at `mem_map`. The identical NOP probe and full native boundary test passed on the authorized ordinary host. The test gate was run there; the native-firmware workflow now isolates failures in a child. This is an observed execution-environment limitation, not a firmware/device result. The pinned Unicorn dependency still emits its upstream `pkg_resources` deprecation warning; it is recorded, not hidden.

## Reproduce

```sh
python -m pip install -r requirements-test.lock
python -m pip install -e .
python -m pytest -q -p no:cacheprovider
python checks/compare_upstream.py --upstream-root /path/to/commit-3dc6582
python -m build
python -m venv .consumer
.consumer/bin/python -m pip install dist/*.whl
.consumer/bin/python -I checks/consume_installation.py
```

## OPEN

- Complete operation/regex graph semantic rewrite, every inherited formatting rule and real profile corpus coverage remain unfinished. Added limits do not prove policy equivalence for all inputs or comprehensively escape/redact every SBPL/XML presentation path.
- Retained graph helpers contain legacy module-level state. CLI work runs in one process with per-operation reset/copies; concurrent direct library graph calls are not established safe.
- The work deadline is cooperative. Byte limits do not impose a wall-clock timeout on an arbitrary caller-supplied library stream. The CLI uses finite snapshots; independent helper process deadlines are enforced separately.
- Actual `ipsw` download/disassembly, kernel layout correctness, full firmware extraction, generated-Mach-O behavior, signatures and real device/sandbox runtime results remain unverified.
- External helper executables and their downloads are not attested by this package. Native dependency compatibility remains host-specific.
- CVP applicant authorization, identity, organization and an actual legitimate task affected by safeguards remain separate evidence. Repository counts, renamed code, tests and publishing do not prove admission or bypass safety controls.
