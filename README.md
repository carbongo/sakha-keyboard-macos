<div align="center">

# ⌨️ Sakha Keyboard for macOS

**Type in Sakha (Yakut) on a Mac — without losing a single Russian or English letter.**

[![Release](https://img.shields.io/github/v/release/carbongo/sakha-keyboard-macos?label=release)](https://github.com/carbongo/sakha-keyboard-macos/releases/latest)
[![CI](https://github.com/carbongo/sakha-keyboard-macos/actions/workflows/ci.yml/badge.svg)](https://github.com/carbongo/sakha-keyboard-macos/actions/workflows/ci.yml)
![macOS](https://img.shields.io/badge/macOS-12%2B-black?logo=apple)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

**English** · [Русский](README.ru.md) · [Сахалыы](README.sah.md)

</div>

Four layouts, one install, no restart:

| Layout | Built on | Where the Sakha letters are |
|---|---|---|
| [**Sakha (Windows)**](#sakha-windows) | Mac Russian | Number row, same as the Windows "Sakha" layout |
| [**Sakha (Russian)**](#sakha-russian) | Mac Russian | **Opt** + the Russian letter that looks like it |
| [**Sakha (Latin)**](#sakha-latin) | US | Common Turkic Latin alphabet |
| [**Sakha (Novgorodov)**](#sakha-novgorodov) | US | 1920s Novgorodov alphabet |

> macOS 27 ships its own *Yakut* layout, which replaces ц, г, ъ, ф and ж. These layouts don't.

## 🚀 Install

### Option 1: Terminal (recommended, no security warning)

```sh
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash
```

It asks which layouts to add to your input menu; just press Return for **Sakha (Windows)**. Then switch with **Ctrl+Space** or **🌐 Globe**. On macOS 27, log out and back in once to see them in the input menu; older macOS shows them right away. No restart needed.

<details>
<summary>Options</summary>

```sh
# pick layouts without prompts
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash -s -- -l sakha-windows,sakha-latin

# all four layouts, no questions
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash -s -- -l all

# uninstall
curl -fsSL https://raw.githubusercontent.com/carbongo/sakha-keyboard-macos/main/install.sh | bash -s -- -u
```

| Flag | |
|---|---|
| `-l, --layouts` | `sakha-windows`, `sakha-russian`, `sakha-latin`, `sakha-novgorodov` or `all` |
| `-y, --yes` | Don't ask; add Sakha (Windows) only |
| `--no-enable` | Only install; add layouts in System Settings yourself |
| `-v, --version` | A specific release, e.g. `v2.0.0` |
| `-u, --uninstall` | Remove everything |

</details>

### Option 2: Download and double-click

> [!WARNING]
> **macOS blocks this installer the first time.** The first double-click shows *"Apple could not verify 'Install Sakha Keyboard.command' is free of malware…"*. That's expected. macOS shows this for any downloaded script that isn't notarised by Apple, and notarisation needs a paid Apple Developer account. The script is [`install.sh`](install.sh), so you can read exactly what it does. If you'd rather not see the warning at all, use [Option 1](#option-1-terminal-recommended-no-security-warning).

1. Download **[Sakha-Keyboard.zip](https://github.com/carbongo/sakha-keyboard-macos/releases/latest/download/Sakha-Keyboard.zip)** and open it.
2. Double-click **Install Sakha Keyboard.command**. macOS shows the warning, so click **Done**.
3. Open **System Settings → Privacy & Security**, scroll down to *"Install Sakha Keyboard.command" was blocked…* and click **Open Anyway**. Confirm with your password or Touch ID.
4. Double-click **Install Sakha Keyboard.command** again, click **Open**, and tick the layouts you want.

To remove the layouts, double-click **Uninstall Sakha Keyboard.command**. It's a separate file, so it needs the same **Open Anyway** step once.

> Right-click → **Open** no longer gets past this warning on macOS 15 and later. Use **Open Anyway** in Privacy & Security instead.

<details>
<summary>Manual install</summary>

Copy `Sakha.bundle` into `~/Library/Keyboard Layouts`. Log out and back in, then add the layouts in **System Settings → Keyboard → Text Input → Edit → +** (search for *Sakha*).

</details>

## 🗺️ Layouts

The large legend is what a key types on its own (Shift for capitals). The small pink legend is **Opt**, and **Shift+Opt** for the upper one. Blue keys differ from the layout it's built on.

### Sakha (Windows)

The Windows Sakha layout (KBDYAK), on Mac Russian. ё stays on its key, and digits are on **Opt+1…0**.

![Sakha (Windows)](docs/layouts/sakha-windows.svg)

### Sakha (Russian)

Plain Mac Russian. Hold **Opt** for the Sakha letter that looks like it: г→ҕ, н→ҥ, о→ө, у→ү, х→һ, д→дь, ь→нь.

![Sakha (Russian)](docs/layouts/sakha-russian.svg)

### Sakha (Latin)

Common Turkic Latin: ҕ ğ · ҥ ñ · ө ö · ү ü · ы ı · ч ç · дь j · нь ń · й y. The letters have their own keys, as on German or Turkish keyboards. **Opt+letter** also works (Opt+o → ö). The punctuation those keys used to type moves to Opt.

![Sakha (Latin)](docs/layouts/sakha-latin.svg)

### Sakha (Novgorodov)

The 1920s Novgorodov alphabet, typed with the closest IPA letters: ɯ ɣ ɟ ŋ ɲ ø, and c for ч. The diphthong keys type **ie uo yø ɯa**. **Opt+vowel** types a long vowel (aː), and **Opt+consonant** doubles it (tt).

![Sakha (Novgorodov)](docs/layouts/sakha-novgorodov.svg)

## ❓ FAQ

<details>
<summary><b>Do I need to log out?</b></summary>

On macOS 27, yes, once: it shows new layouts in the input menu only after a login. On older macOS, no: the installer registers them through the Text Input Sources API, so they appear right away. No restart either way.

</details>

<details>
<summary><b>Why does macOS say it "could not verify" the installer? Is it safe?</b></summary>

macOS shows that message for every downloaded script or app that Apple hasn't notarised. It doesn't mean malware was found. Notarising requires a paid Apple Developer membership, and this free project doesn't have one. The `.command` files only run [`install.sh`](install.sh), which copies `Sakha.bundle` to `~/Library/Keyboard Layouts` and adds the layouts to your input menu. The terminal one-liner shows no warning, because files fetched with `curl` aren't flagged as downloads.

</details>

<details>
<summary><b>Will Cmd+C / Cmd+V still work?</b></summary>

Yes. Cmd and Ctrl shortcuts always use the US QWERTY positions in every layout.

</details>

<details>
<summary><b>System Settings says "The developer can access anything you type". Do you collect anything?</b></summary>

**No. Nothing is collected, sent or stored.**

macOS 27 shows that label on every keyboard layout that doesn't come from Apple, whatever it contains. These layouts contain no code at all: `Sakha.bundle` is an `Info.plist`, four `.keylayout` files (plain XML tables like "this key types ҕ") and four icons. Nothing runs while you type. The installer runs once, copies those files and exits. It doesn't stay running, has no network access after the download, and has no telemetry.

The warning is written for input *methods*, which are real programs that do see your keystrokes. Apple uses the same wording for plain layouts. You can check every file in this repository.

</details>

<details>
<summary><b>What do the menu bar badges mean?</b></summary>

Like Apple's **РУ** and **A**, each layout shows short letters: **СА** for Sakha (Windows), **СР** for Sakha (Russian), **SA** for Sakha (Latin) and **NV** for Sakha (Novgorodov). They're boxed badges like Apple's and turn dark or white to match the menu bar and menus. If you still see old flag icons, log out and back in once so macOS refreshes its cache.

</details>

## 🤝 Contributing

New letters, better key positions and bug reports are all welcome. See [CONTRIBUTING.md](CONTRIBUTING.md). The layouts are generated by [`build.py`](build.py), so a change is usually a single line.

## License

[MIT](LICENSE). Originally inspired by [@sandaar/sakha-keylayout-osx](https://github.com/sandaar/sakha-keylayout-osx).
