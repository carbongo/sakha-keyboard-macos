# Design

## Why v2

macOS 27 ships `com.apple.keylayout.Yakut`, which puts ү ҥ ҕ ө һ in place of ц г ъ ф ж and shifts г/ш one key right. v2 never sacrifices a Russian letter. The v1 layouts (Sakha (Yakut), Latin and their PC variants) were replaced.

## Pipeline

`src/base/{us,russian}.json` (dumped from Apple's layouts by `tools/dump-layout.swift`) + overrides in `build.py` → `Sakha.bundle`.

- Cmd and Ctrl layers are always US QWERTY, so shortcuts don't change.
- Caps Lock = Shift for letter outputs.
- US Opt dead keys (e u i n `) only type their spacing accent.
- Icons: Apple-style template text badges (filled/outlined СА, SA) from `tools/make-icons.swift` → `src/icons`; no icon = generic keyboard glyph. macOS derives the input-source IDs itself (`com.carbongo.keyboardlayout.sakha.keylayout.SakhaWindows`, …).

## Decisions

| Layout | Decision |
|---|---|
| Sakha (Windows) | Clone of Windows KBDYAK (kbdlayout.info/kbdyak). ё stays on its Mac key. Windows has no digits, so they go on Opt+number. |
| Sakha (Russian) | Opt pairs by lookalike shape. дь on Opt+д; нь on Opt+ь, because Opt+н is ҥ. |
| Sakha (Latin) | Common Turkic: ҕ ğ, ҥ ñ, ө ö, ү ü, ы ı, ч ç, дь j, нь ń, й y. Turkic casing (i/İ, ı/I). Own keys plus Opt backups. |
| Sakha (Novgorodov) | Closest IPA letters: ɯ ɣ ɟ ŋ ɲ ø; c = ч. Diphthong keys type digraphs. Opt = vowel+ː or doubled consonant. Holding a key can't be detected by a keylayout, so Opt is used. |
| Sakha (Cyrillic) on US | Dropped as redundant. |
