# sakha-keyboard-macos

macOS keyboard layout bundle `Sakha.bundle` with 4 Sakha layouts, plus installers. README.md (+ README.ru.md) is the user-facing guide.

## Commands

- Build: `python3 build.py` regenerates `Sakha.bundle` + `docs/layouts/*.svg`. Commit the results; CI fails on drift.
- Install the local build: `./install.sh -y` (`-u` uninstalls). Lint: `shellcheck install.sh tools/package.sh packaging/*.command`.
- Release zip: `tools/package.sh` → `dist/Sakha-Keyboard.zip`.
- Menu bar badges: `swift tools/make-icons.swift` → `src/icons/*.icns` (Mac only; commit them).
- Release: bump `VERSION` in build.py and add a CHANGELOG section, rebuild, push tag `vX.Y.Z` (Actions publishes it).
- Re-dump a base layout: `swift tools/dump-layout.swift com.apple.keylayout.Russian > src/base/russian.json`.

## Constraints

- Never move or replace a Russian or English base letter: Sakha letters go on spare keys, the number row or Opt.
- `Sakha.bundle/` and `docs/layouts/` are generated: edit `build.py`.
- Layout IDs (-19001…-19004) are shared by `build.py` and `install.sh`; change both together.
- `xmllint` errors on `&#x0008;` etc. are expected (keylayouts are XML 1.1).

## Docs

- `docs/design.md`: why each layout is shaped the way it is; decisions and sources.
- `docs/installer.md`: how install.sh registers and enables layouts without a logout.
