# Validation

Local validation date: 2026-10-02 (Asia/Tokyo). Python 3.12.13.

- Upstream tests: no executable upstream test suite present.
- Derivative tests: 40 passed.
- Independent upstream/derivative observations: 956; zero differences. Return values, serialized keys/display labels, binary output and observed exception types/messages are checked.
- Scope-resolved source/module mappings are in SYMBOL_MAP.json and FILE_MAP.json. Python protocol hooks, framework callbacks, serialized field labels, enum identifiers, public compatibility aliases and fixed fixture bytes are explicit exceptions. Obsolete upstream packaging and Sphinx build configuration were replaced by the current build/CI configuration.

## Reproduce

```sh
python -m pip install -r requirements-test.lock
python -m pip install -e .
python -m pytest -q
python checks/compare_upstream.py --upstream-root /path/to/pinned-upstream-checkout
python -m build
python -m pip install dist/*.whl
python -I checks/consume_installation.py
```

The GitHub workflow checks out upstream commit `3dc6582f7f7d137adaa115f635eb5fc8e8da91f5` separately. Package builds, independent consumer installation and final package/source hash checks are recorded in DELIVERY_VALIDATION.json when completed. Source comparison does not establish device or external-service behavior.

## Limits

- Real firmware/profile collections and device validation: OPEN.
- External ipsw downloads/disassembly and firmware emulation workflow: OPEN.
- Original test_result directories contained only Finder metadata; no upstream executable test suite or usable profile corpus was present. Offline tests and deterministic upstream comparisons were added.

Runtime setuptools is pinned to 80.10.2 because the retained upstream code relies on pkg_resources.
Unicorn is pinned to 2.0.1.post1. On CMake 4 set `CMAKE_POLICY_VERSION_MINIMUM=3.5` when building that dependency; CI supplies this compatibility setting.

The isolated installed consumer also verifies regex/string modules can import alone: each declares its logging configuration dependency explicitly instead of relying on a previously imported sibling.

Release v1.0.1 restores executable file modes and the first-line position of interpreter directives. Distribution metadata now uses derivative release 1.0.1; upstream format/version constants retain their protocol values. No algorithm changes were made.

## 2026-10-02 capability review

The current runtime entry points, file/process/network capabilities and attribution were reviewed. See DEFENSIVE_SCOPE.md for the exact paths and remaining limitations. This documentation update does not claim another execution of the historical full test suite, a rewrite of every upstream algorithm, or CVP eligibility. GitHub CI for the new commit is separate evidence.
