# Design

## Why v2

macOS 27 ships `com.apple.keylayout.Yakut`, which puts ү ҥ ҕ ө һ in place of ц г ъ ф ж and shifts г/ш one key right. v2 never sacrifices a Russian letter. The v1 layouts (Sakha (Yakut), Latin and their PC variants) were replaced.

## Pipeline

`src/base/{us,russian}.json` (dumped from Apple's layouts by `tools/dump-layout.swift`) + overrides in `build.py` → `Sakha.bundle`.

- Cmd and Ctrl layers are always US QWERTY, so shortcuts don't change.
- Caps Lock = Shift for letter outputs.
- US Opt dead keys (e u i n `) only type their spacing accent.
- `TISIntendedLanguage`: `sah` for Cyrillic (Apple's convention for a language's default script), so System Settings lists them under Apple's **Sakha** next to its Yakut layout; `sah-Latn` for Latin → **Sakha (Latin)**. `sah-Cyrl` made a second "Sakha" row.
- Icons: filled badges with knocked-out letters (СА, СР, SA, NV; 16 pt, SF semibold 8 pt caps) like Apple's **A**/**Ca**, **template** (`TISIconIsTemplate`), from `tools/make-icons.swift`: they adapt in the menu bar and input menu. Native labels are system-drawn from `TISIconLabels`, which works only for input methods; a layout gets one square .icns for every context (TIFF/PDF ignored). The switcher draws templates dark even on its blue selection, so they must be filled: bare letters or outlines (v2.2.0) vanish there; always-white (v2.2.1) vanishes on a light menu bar. No icon = generic keyboard glyph. macOS derives the input-source IDs itself (`com.carbongo.keyboardlayout.sakha.keylayout.SakhaWindows`, …).

## Decisions

| Layout | Decision |
|---|---|
| Sakha (Windows) | Clone of Windows KBDYAK (kbdlayout.info/kbdyak). ё stays on its Mac key. Windows has no digits, so they go on Opt+number. |
| Sakha (Russian) | Opt pairs by lookalike shape. дь on Opt+д; нь on Opt+ь, because Opt+н is ҥ. |
| Sakha (Latin) | Common Turkic: ҕ ğ, ҥ ñ, ө ö, ү ü, ы ı, ч ç, дь j, нь ń, й y. Turkic casing (i/İ, ı/I). Own keys plus Opt backups. |
| Sakha (Novgorodov) | Closest IPA letters: ɯ ɣ ɟ ŋ ɲ ø; c = ч. Diphthong keys type digraphs. Opt = vowel+ː or doubled consonant. Holding a key can't be detected by a keylayout, so Opt is used. |
| Sakha (Cyrillic) on US | Dropped as redundant. |
