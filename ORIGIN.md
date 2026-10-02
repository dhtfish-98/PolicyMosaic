# Origin and attribution

PolicyMosaic is a derived, reorganized version of sandblaster_26.

- Source: https://github.com/chensokolovsky/sandblaster_26.git
- Baseline commit: `3dc6582f7f7d137adaa115f635eb5fc8e8da91f5`
- Baseline tree: `1cac93e4419f6de08e6a094cfe2c530dea897696`
- License: BSD-3-Clause; the original license and copyright are retained.

The original algorithms and project history belong to their upstream authors. This derivative introduces renamed implementation bindings resolved by lexical scope, renamed modules, and explicit adapters separating public data labels from internal implementation names. It does not claim independent authorship of upstream code or approval by any verification program.

Public CLI flags, structured data keys, enum identifiers, Python framework hooks, legacy external API aliases, resource formats and compatibility labels are deliberate naming exceptions. The compatibility module provides separate wire/display labels; it is not a hidden copy of the old implementation.

## Maintenance release 1.0.3

The current derivative substantively replaces the profile input/report pipeline, string and regex record interpreters, scoped filter conversion and optional firmware execution workflow. Operation and regex graph reduction algorithms retain upstream lineage; this release adds resource guards and replaces selected reference/walk/state routines. It does not claim that every inherited graph or formatting algorithm has been independently rewritten.

The package also adds owned malformed-input/process fixtures, an isolated native-emulation worker and exact intentional-change comparison evidence. Original catalogs and license remain. Historical naming maps describe the earlier release and do not supersede current source or imply independent authorship.

Release 1.0.3 additionally pins the verified official Unicorn 2.1.4 dependency and makes native-child failure/timeouts explicit. This does not close the inherited graph-algorithm or real-firmware OPEN scope.
