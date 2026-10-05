# sakha-keyboard-macos

macOS keyboard layout bundle `Sakha.bundle` with 4 Sakha layouts. README.md = user-facing key reference.

## Commands

- Build: `python3 build.py` (regenerates `Sakha.bundle`; commit the result — users install it straight from the repo)
- Install locally: `rm -rf ~/Library/Keyboard\ Layouts/Sakha.bundle && cp -R Sakha.bundle ~/Library/Keyboard\ Layouts/`, then log out/in (or `TISRegisterInputSource` on the bundle URL)
- Re-dump a base layout: `swift tools/dump-layout.swift com.apple.keylayout.Russian > src/base/russian.json`

## Constraints

- Never move or replace a Russian or English base letter — Sakha letters go on spare keys, the number row or Opt.
- `Sakha.bundle/` is generated: edit `build.py`, never the `.keylayout` files.
- `xmllint` errors on `&#x0008;` etc. are expected (keylayouts are XML 1.1).

## Docs

- `docs/design.md` — why each layout is shaped the way it is; decisions and sources.
