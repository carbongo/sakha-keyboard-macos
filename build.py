#!/usr/bin/env python3
"""Generates Sakha.bundle from src/base/*.json (dumped Apple layouts) + the overrides below.

Each override is {keycode: (base, shift, opt, shiftopt)}; None keeps the base layout's output.
Caps Lock = shift for letters, base for everything else.
"""
import json
import shutil
import unicodedata
from pathlib import Path

ROOT = Path(__file__).parent
BUNDLE = ROOT / "Sakha.bundle"
BUNDLE_ID = "com.carbongo.keyboardlayout.sakha"

# Mac virtual keycodes, by the US keycap label
K = {
    "`": 50, "1": 18, "2": 19, "3": 20, "4": 21, "5": 23, "6": 22, "7": 26, "8": 28, "9": 25, "0": 29, "-": 27, "=": 24,
    "q": 12, "w": 13, "e": 14, "r": 15, "t": 17, "y": 16, "u": 32, "i": 34, "o": 31, "p": 35, "[": 33, "]": 30, "\\": 42,
    "a": 0, "s": 1, "d": 2, "f": 3, "g": 5, "h": 4, "j": 38, "k": 40, "l": 37, ";": 41, "'": 39,
    "z": 6, "x": 7, "c": 8, "v": 9, "b": 11, "n": 45, "m": 46, ",": 43, ".": 47, "/": 44, "§": 10,
}
US_SHIFT_DIGITS = dict(zip("1234567890", "!@#$%^&*()"))


def is_letter(s):
    return any(unicodedata.category(c).startswith("L") for c in s)


def upper(s):
    """Capitalise the first letter (нь→Нь, uo→Uo)."""
    return s[:1].upper() + s[1:] if s else s


# ── Sakha (Russian): Windows "Sakha" (KBDYAK) on Mac Russian; digits on Opt ──
sakha_russian = {
    K["`"]: ('"', "№", "]", "["),
    K["1"]: ("!", "?", "1", "!"),
    **{K[k]: (low, upper(low), k, US_SHIFT_DIGITS[k]) for k, low in
       zip("2345678", ["нь", "дь", "ҥ", "ҕ", "ө", "һ", "ү"])},
    K["9"]: (";", "(", "9", "("),
    K["0"]: (":", ")", "0", ")"),
    K["/"]: (".", ",", "/", "\\"),
}

# ── Russian (Sakha): Mac Russian untouched; Opt + lookalike letter = Sakha letter ──
russian_sakha = {
    K[k]: (None, None, low, upper(low)) for k, low in [
        ("u", "ҕ"),   # г
        ("y", "ҥ"),   # н
        ("j", "ө"),   # о
        ("e", "ү"),   # у
        ("[", "һ"),   # х
        ("l", "дь"),  # д
        ("m", "нь"),  # ь
    ]
}

# ── Sakha (Latin): Common Turkic on US; own keys like German/Turkish-Q, plus Opt+letter ──
sakha_latin = {
    K["["]: ("ğ", "Ğ", "[", "{"),
    K["]"]: ("ü", "Ü", "]", "}"),
    K[";"]: ("ı", "I", ";", ":"),
    K["'"]: ("ö", "Ö", "'", '"'),
    K["\\"]: ("ç", "Ç", "\\", "|"),
    K["`"]: ("ñ", "Ñ", "`", "~"),
    K["i"]: ("i", "İ", "ı", "I"),
    K["o"]: (None, None, "ö", "Ö"),
    K["u"]: (None, None, "ü", "Ü"),
    K["g"]: (None, None, "ğ", "Ğ"),
    K["c"]: (None, None, "ç", "Ç"),
    K["s"]: (None, None, "ş", "Ş"),
    K["n"]: (None, None, "ñ", "Ñ"),
    K["m"]: (None, None, "ń", "Ń"),
}

# ── Sakha (Novgorodov): 1920s IPA-based alphabet on US; Opt = long vowel (aː) / geminate (tt) ──
NOVGORODOV_LETTERS = {  # key: (letter, capital)
    **{k: (k, k.upper()) for k in "abcdeghijklmnoprstuxy"},
    "w": ("ɯ", "Ɯ"),  # ы
    "v": ("ɣ", "Ɣ"),  # ҕ
    "f": ("ɟ", "ɟ"),  # дь (no capital in Unicode)
    "q": ("ŋ", "Ŋ"),  # ҥ
    "z": ("ɲ", "Ɲ"),  # нь
    "[": ("ø", "Ø"),  # ө
}
NOVGORODOV_VOWELS = set("aeiouyɯø")
novgorodov = {}
for key, (low, cap) in NOVGORODOV_LETTERS.items():
    if low in NOVGORODOV_VOWELS:
        novgorodov[K[key]] = (low, cap, low + "ː", cap + "ː")
    else:
        novgorodov[K[key]] = (low, cap, low * 2, cap + low)
novgorodov.update({
    K[k]: (d, upper(d), d, upper(d)) for k, d in [(";", "ie"), ("'", "uo"), ("\\", "yø"), ("]", "ɯa")]
})
novgorodov.update({  # punctuation pushed off [ ] ; ' \
    K["`"]: ("'", '"', "`", "~"),
    K[","]: (",", ";", "<", "<"),
    K["."]: (".", ":", ">", ">"),
    K["9"]: (None, None, "[", "{"),
    K["0"]: (None, None, "]", "}"),
    K["/"]: (None, None, "\\", "|"),
})

LAYOUTS = [  # (name, id, base, overrides, icon)
    ("Sakha (Russian)", -19001, "russian", sakha_russian, "sakha-pc.icns"),
    ("Russian (Sakha)", -19002, "russian", russian_sakha, "sakha.icns"),
    ("Sakha (Latin)", -19003, "us", sakha_latin, "sakha-latin.icns"),
    ("Sakha (Novgorodov)", -19004, "us", novgorodov, "sakha-novgorodov.icns"),
]

MODIFIERS = [  # keyMap index → modifier combos (Apple keylayout syntax)
    ("base", ['']),
    ("shift", ["anyShift caps?"]),
    ("caps", ["caps"]),
    ("opt", ["anyOption"]),
    ("shiftopt", ["anyShift caps? anyOption"]),
    ("capsopt", ["caps anyOption"]),
    ("cmd", ["command caps? anyOption?"]),
    ("cmdshift", ["command anyShift caps? anyOption?"]),
    ("ctrl", ["anyControl anyShift? caps? anyOption? command?"]),
]


def tables(base_name, overrides):
    base = json.loads((ROOT / "src/base" / f"{base_name}.json").read_text())
    us = json.loads((ROOT / "src/base/us.json").read_text())
    t = {layer: dict(base[layer]) for layer in ("base", "shift", "caps", "opt", "shiftopt", "capsopt")}
    for code, char in base["capsopt"].items():  # US Opt dead keys (e, u, i, n, `) dump empty: use their terminators
        t["opt"].setdefault(code, char)
    t["cmd"], t["cmdshift"], t["ctrl"] = us["base"], us["shift"], us["ctrl"]  # shortcuts stay QWERTY
    for code, outs in overrides.items():
        code = str(code)
        for layer, out in zip(("base", "shift", "opt", "shiftopt"), outs):
            if out is not None:
                t[layer][code] = out
        b, s, o, so = (t[layer].get(code) for layer in ("base", "shift", "opt", "shiftopt"))
        t["caps"][code] = (s.upper() if is_letter(b or "") else b)
        t["capsopt"][code] = (so.upper() if is_letter(o or "") else o)
    return t


def xml_escape(s):
    return "".join(c if c.isprintable() and c not in "&<>\"'" else f"&#x{ord(c):04X};" for c in s)


def keylayout(name, layout_id, t):
    maxout = max(len(v) for layer in t.values() for v in layer.values())
    lines = [
        '<?xml version="1.1" encoding="UTF-8"?>',
        '<!DOCTYPE keyboard SYSTEM "file://localhost/System/Library/DTDs/KeyboardLayout.dtd">',
        "<!-- Generated by build.py — edit that, not this file. -->",
        f'<keyboard group="126" id="{layout_id}" name="{name}" maxout="{maxout}">',
        "    <layouts>",
        '        <layout first="0" last="0" mapSet="ANSI" modifiers="mods"/>',
        "    </layouts>",
        '    <modifierMap id="mods" defaultIndex="0">',
    ]
    for i, (_, combos) in enumerate(MODIFIERS):
        lines.append(f'        <keyMapSelect mapIndex="{i}">')
        lines += [f'            <modifier keys="{c}"/>' for c in combos]
        lines.append("        </keyMapSelect>")
    lines += ["    </modifierMap>", '    <keyMapSet id="ANSI">']
    for i, (layer, _) in enumerate(MODIFIERS):
        lines.append(f'        <keyMap index="{i}">')
        for code in sorted(t[layer], key=int):
            lines.append(f'            <key code="{code}" output="{xml_escape(t[layer][code])}"/>')
        lines.append("        </keyMap>")
    lines += ["    </keyMapSet>", "</keyboard>", ""]
    return "\n".join(lines)


def info_plist():
    entries = "".join(f"""	<key>KLInfo_{name}</key>
	<dict>
		<key>TICapsLockLanguageSwitchCapable</key>
		<false/>
		<key>TISIconIsTemplate</key>
		<false/>
		<key>TISIntendedLanguage</key>
		<string>{'sah-Latn' if base == 'us' else 'sah-Cyrl'}</string>
	</dict>
""" for name, _, base, _, _ in LAYOUTS)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>{BUNDLE_ID}</string>
	<key>CFBundleName</key>
	<string>Sakha</string>
	<key>CFBundleVersion</key>
	<string>2.0</string>
{entries}</dict>
</plist>
"""


def main():
    shutil.rmtree(BUNDLE, ignore_errors=True)
    res = BUNDLE / "Contents/Resources"
    res.mkdir(parents=True)
    (BUNDLE / "Contents/Info.plist").write_text(info_plist())
    for name, layout_id, base, overrides, icon in LAYOUTS:
        (res / f"{name}.keylayout").write_text(keylayout(name, layout_id, tables(base, overrides)))
        shutil.copy(ROOT / "src/icons" / icon, res / f"{name}.icns")
    print(f"built {BUNDLE.name}: {', '.join(n for n, *_ in LAYOUTS)}")


if __name__ == "__main__":
    main()
