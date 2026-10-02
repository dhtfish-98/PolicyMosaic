# PolicyMosaic

PolicyMosaic inspects authorized local Apple sandbox profile bytes and produces an attributed SBPL or C representation for defensive policy review. It is derived from [sandblaster_26](https://github.com/chensokolovsky/sandblaster_26) at the pinned commit in [ORIGIN.md](ORIGIN.md); upstream authorship and the BSD-3 license are retained.

## Current maintenance release: 1.0.2

This release rewrites profile input/layout handling, string and regex bytecode records, filter conversion context, report publication, compiler invocation and optional firmware-helper execution. The inherited operation/regex graph reducers receive explicit work and expansion guards, independent regex state and finite graph walks. Their complete semantic rewrite and real firmware/device validation remain **OPEN**.

- Default decoding uses local files and does not make network requests. Package imports no longer create `reverse.log` in the caller's directory.
- Profile files are copied from a checked regular file into a finite local snapshot (64 MiB). Final symlinks, directories and FIFOs are rejected. Observed changes during reading are rejected; this is not proof of a coherent acquisition from a live device.
- Reports are limited to 16 MiB each and 64 MiB cumulatively across a decoder CLI run, created with mode 0600, and never overwrite existing files. Derived bundle names stay one filename component; collisions and invalid names fail explicitly.
- Malformed, unsupported, truncated or over-limit CLI work exits **2**. Reports from a partially completed multi-profile run may remain; exit 2 must not be treated as a complete analysis.

## Install and use

```sh
python -m pip install .
policymosaic --help
policymosaic --release 17 --operations_file operations.txt --directory reports profile.bin
```

The output directory must already exist and the operations file must contain the unique labels matching the selected binary layout. Release selectors 17–26 use the inherited layouts; that does not establish coverage for every firmware with those release names. Reports are analysis representations, not proven sandbox policy effects.

`--c_output` produces a C report. `--macho` invokes local clang in a private temporary directory to produce a 64-bit Mach-O **dynamic library report**, plus its C source. The historical executable-link command lacked `main` and failed on the current host; this release uses `-dynamiclib` and verifies the output header. Generated output is never run by PolicyMosaic. Suitable macOS clang is required; a compiler failure is explicit and leaves existing files untouched.

## Optional firmware helper

```sh
python -m policymosaic.firmware_helper --kernel authorized-kernel --version 17.6.1
python -m policymosaic.firmware_helper --device iPhone16,1 --version 17.6.1
```

The second command explicitly requests an `ipsw` firmware download. Helper outputs use a fresh private workspace. The helper invokes `ipsw`, `strings`, the decoder and Unicorn; it does not connect to or change a device. Native emulation in the firmware workflow runs in a separate Python process, so a native fault becomes an incomplete helper error. The legacy library `Emulator` API remains an explicit in-process native API and needs a compatible host.

The external tools can perform their own network and disk activity. Process deadlines, captured-output limits and checked local output paths do not establish a network allowlist or bound every disk write performed by `ipsw`. No real firmware collection was downloaded or tested for this release.

See [DEFENSIVE_SCOPE.md](DEFENSIVE_SCOPE.md), [VALIDATION.md](VALIDATION.md) and [SOURCE_AUDIT.json](SOURCE_AUDIT.json) for evidence and remaining work. Historical module/name maps describe the earlier attributed refactoring, not an independent authorship claim.

## Development and source comparison

```sh
python -m pip install -r requirements-test.lock
python -m pytest -q -p no:cacheprovider
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream
python -m build
```

The comparison checks 927 unchanged observations and 29 exact, documented input/error differences in `checks/BOUNDARY_CHANGES.json`. CI repeats tests, pinned-source comparison, package build and an independently installed consumer. Tests involving Unicorn require a host permitting its native executable mappings.
