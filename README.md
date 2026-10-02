# PolicyMosaic

防御用途、实际能力及本轮验证范围见 [DEFENSIVE_SCOPE.md](DEFENSIVE_SCOPE.md)。

An attributed derivative of **sandblaster_26**, retaining the upstream behavior while reorganizing Python modules and implementation bindings. See [ORIGIN.md](ORIGIN.md) for source, copyright and licensing.

PolicyMosaic reverses binary Apple sandbox profiles into SBPL and retains upstream C/Mach-O output modes. Profile layout parsing, operation graph traversal, filter catalogs, regex bytecode and string bytecode decoding are organized into separate package modules. Resource lookup follows installed package paths while user input and output paths keep their original current-directory meaning.

The optional firmware workflow is available through `python -m policymosaic.firmware_helper` and requires the upstream `ipsw` command, compatible firmware, and Unicorn. The installed helper launches the renamed decoder module. Firmware downloads, external services and actual device validation remain OPEN; offline parser and helper-output checks are independently measured.

## Install

```sh
python -m pip install .
policymosaic --help
```

## Development

```sh
python -m pip install '.[test]'
python -m pytest
python -m build
```

New implementation names are listed in `SYMBOL_MAP.json`, and module/file mappings in `FILE_MAP.json`. External data labels and public compatibility aliases are kept at an explicit adapter boundary. The `guides` directory contains clearly attributed historical upstream documentation; its original commands refer to the upstream project.

See [VALIDATION.md](VALIDATION.md) for measured checks and remaining environmental limits.

## Compare with upstream

```sh
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
```

The source checkout is supplied explicitly; no developer machine paths are embedded. The public CI pins the original upstream commit and repeats tests, comparison, build and installed consumption.
