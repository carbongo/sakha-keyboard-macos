# Contributing

Native speakers' feedback is the most valuable contribution. If a letter is in an awkward place, [open an issue](https://github.com/carbongo/sakha-keyboard-macos/issues/new/choose).

## Changing a layout

1. Edit the layout's override table in [`build.py`](build.py). Each key is `(base, shift, opt, shift+opt)`, and `None` keeps the original.
2. Run `python3 build.py`. It regenerates `Sakha.bundle` and the diagrams in `docs/layouts/`.
3. Try it: `./install.sh -y` installs your local build.
4. Commit everything, generated files included. CI checks they match `build.py`.

**The one rule:** never move or replace a Russian or English letter. Sakha letters go on spare keys, the number row or Opt.

## Releasing

Add a section to `CHANGELOG.md`, bump `VERSION` in `build.py`, rebuild, and push a tag `vX.Y.Z`. GitHub Actions publishes the release with `Sakha-Keyboard.zip`.
