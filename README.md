# Sakha (Yakut) Keyboard Layouts for macOS

Four Sakha layouts in one bundle. None of them moves or replaces a Russian or English letter.

| Layout | Base | Sakha letters |
|---|---|---|
| **Sakha (Russian)** | Mac Russian | Number row, as in the Windows "Sakha" layout |
| **Russian (Sakha)** | Mac Russian | Opt + the lookalike Russian letter |
| **Sakha (Latin)** | US | Common Turkic Latin; own keys + Opt shortcuts |
| **Sakha (Novgorodov)** | US | 1920s Novgorodov alphabet (IPA letters); Opt = long vowel / geminate |

## Install

```sh
git clone https://github.com/carbongo/sakha-keyboard-macos
cp -R sakha-keyboard-macos/Sakha.bundle ~/Library/Keyboard\ Layouts/
```

Log out and back in, then **System Settings → Keyboard → Text Input → Edit… → +** and search *Sakha*.

## Sakha (Russian)

Russian letters stay in place, including ё on its usual key. Only the number row and two punctuation keys change:

| Key | ` | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | / |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Base | " | ! | нь | дь | ҥ | ҕ | ө | һ | ү | ; | : | . |
| Shift | № | ? | Нь | Дь | Ҥ | Ҕ | Ө | Һ | Ү | ( | ) | , |
| Opt | ] | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 0 | / |
| Shift+Opt | [ | ! | @ | # | $ | % | ^ | & | * | ( | ) | \ |

## Russian (Sakha)

The standard Mac Russian layout, plus these on Opt (add Shift for capitals):

| Opt + | г | н | о | у | х | д | ь |
|---|---|---|---|---|---|---|---|
| types | ҕ | ҥ | ө | ү | һ | дь | нь |

## Sakha (Latin)

US QWERTY with the Common Turkic letters on their own keys: ҕ=ğ, ҥ=ñ, ө=ö, ү=ü, ы=ı, ч=ç, дь=j, нь=ń, й=y, х=x, һ=h.

| Key | ` | [ | ] | \ | ; | ' | Shift+i |
|---|---|---|---|---|---|---|---|
| types | ñ | ğ | ü | ç | ı (Shift: I) | ö | İ |

- The punctuation those keys used to type moves to Opt (Opt+[ = [, Shift+Opt+; = :, …).
- Opt shortcuts: Opt+o ö, Opt+u ü, Opt+g ğ, Opt+i ı, Opt+c ç, Opt+n ñ, Opt+m ń, Opt+s ş.

## Sakha (Novgorodov)

The 1920s Novgorodov alphabet, typed with IPA letters. The diphthongs have no single Unicode letter, so their keys type both letters at once:

| Key | w | v | f | q | z | [ | ; | ' | \ | ] |
|---|---|---|---|---|---|---|---|---|---|---|
| types | ɯ (ы) | ɣ (ҕ) | ɟ (дь) | ŋ (ҥ) | ɲ (нь) | ø (ө) | ie | uo | yø | ɯa |

- Other letters are plain Latin: c = ч, j = й, y = ү, x = х.
- **Opt + vowel** types a long vowel (Opt+a → aː). **Opt + consonant** doubles it (Opt+t → tt).
- Punctuation that lost its key: Shift+, = ;, Shift+. = :, ` = ', Shift+` = ". On Opt: < > [ ] \.

## Development

The layouts are generated; see [AGENTS.md](AGENTS.md).

*Originally inspired by [@sandaar/sakha-keylayout-osx](https://github.com/sandaar/sakha-keylayout-osx).*
