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
VERSION = "2.2.1"

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


# ── Sakha (Windows): Windows "Sakha" (KBDYAK) on Mac Russian; digits on Opt ──
sakha_windows = {
    K["`"]: ('"', "№", "]", "["),
    K["1"]: ("!", "?", "1", "!"),
    **{K[k]: (low, upper(low), k, US_SHIFT_DIGITS[k]) for k, low in
       zip("2345678", ["нь", "дь", "ҥ", "ҕ", "ө", "һ", "ү"])},
    K["9"]: (";", "(", "9", "("),
    K["0"]: (":", ")", "0", ")"),
    K["/"]: (".", ",", "/", "\\"),
}

# ── Sakha (Russian): Mac Russian untouched; Opt + lookalike letter = Sakha letter ──
sakha_russian = {
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

LAYOUTS = [  # (name, id, base, overrides)
    ("Sakha (Windows)", -19001, "russian", sakha_windows),
    ("Sakha (Russian)", -19002, "russian", sakha_russian),
    ("Sakha (Latin)", -19003, "us", sakha_latin),
    ("Sakha (Novgorodov)", -19004, "us", novgorodov),
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
		<true/>
		<key>TISIntendedLanguage</key>
		<string>{'sah-Latn' if base == 'us' else 'sah'}</string>
	</dict>
""" for name, _, base, _ in LAYOUTS)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>CFBundleIdentifier</key>
	<string>{BUNDLE_ID}</string>
	<key>CFBundleName</key>
	<string>Sakha</string>
	<key>CFBundleVersion</key>
	<string>{VERSION}</string>
{entries}</dict>
</plist>
"""


DIAGRAM_ROWS = [  # (label, width in key units); single characters are keys from K
    [*"`1234567890-=", ("delete", 1.5)],
    [("tab", 1.5), *"qwertyuiop[]\\"],
    [("caps", 1.75), *"asdfghjkl;'", ("return", 1.75)],
    [("shift", 2.25), *"zxcvbnm,./", ("shift", 2.25)],
]
DIAGRAM_CSS = """
.k{fill:#f6f8fa;stroke:#d0d7de}.c{fill:#ddf4ff;stroke:#54aeff}
text{font-family:-apple-system,"Segoe UI",Helvetica,Arial,sans-serif;fill:#1f2328}
.o{fill:#bf3989}.m{fill:#8c959f;font-size:11px}
@media (prefers-color-scheme:dark){.k{fill:#161b22;stroke:#30363d}.c{fill:#0c2d6b;stroke:#1f6feb}
text{fill:#e6edf3}.o{fill:#ff80c8}.m{fill:#6e7681}}
"""


def diagram(t, base_name):
    """SVG keyboard: Shift/base on the left, added Opt (Shift+Opt) on the right in accent; changed keys tinted."""
    base = json.loads((ROOT / "src/base" / f"{base_name}.json").read_text())
    unit, gap = 60, 5
    out = []
    for r, row in enumerate(DIAGRAM_ROWS):
        x, y = 0.0, r * (unit + gap)
        for key in row:
            label, width = (None, key[1]) if isinstance(key, tuple) else (key, 1)
            w = width * unit + (width - 1) * gap
            if label is None:
                out.append(f'<rect class="k" x="{x}" y="{y}" width="{w}" height="{unit}" rx="7"/>'
                           f'<text class="m" x="{x + 8}" y="{y + unit - 9}">{key[0]}</text>')
            else:
                code = str(K[label])
                vals = {layer: t[layer].get(code, "") for layer in ("base", "shift", "opt", "shiftopt")}
                was = {layer: base[layer].get(code, base["capsopt"].get(code, "")) for layer in vals}
                changed = {layer: vals[layer] != was[layer] for layer in vals}
                tint = "c" if changed["base"] or changed["shift"] else "k"
                out.append(f'<rect class="{tint}" x="{x}" y="{y}" width="{w}" height="{unit}" rx="7"/>')
                legends = [("base", "shift", "", x + 8, 20)]
                if changed["opt"] or changed["shiftopt"]:  # only show Opt where this project adds something
                    legends.append(("opt", "shiftopt", ' class="o"', x + unit / 2 + 4, 14))
                for low, high, cls, tx, size in legends:
                    lo, hi = vals[low], vals[high]
                    if not (lo.isprintable() and hi.isprintable()):
                        continue
                    if is_letter(lo) and hi == upper(lo):  # one legend for letter pairs: capital on base, small on Opt
                        text = hi if not cls else lo
                        out.append(f'<text{cls} x="{tx}" y="{y + unit - 12}" font-size="{size}">{xml_escape(text)}</text>')
                    else:
                        out.append(f'<text{cls} x="{tx}" y="{y + 22}" font-size="{size - 4}">{xml_escape(hi)}</text>'
                                   f'<text{cls} x="{tx}" y="{y + unit - 10}" font-size="{size - 4}">{xml_escape(lo)}</text>')
            x += w + gap
    width, height = 14.5 * unit + 13 * gap, 4 * unit + 3 * gap
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-2 -2 {width + 4} {height + 4}" width="{width + 4}">'
            f"<style>{DIAGRAM_CSS}</style>{''.join(out)}</svg>\n")


def slug(name):
    return name.lower().replace(" (", "-").rstrip(")")


def main():
    shutil.rmtree(BUNDLE, ignore_errors=True)
    res = BUNDLE / "Contents/Resources"
    res.mkdir(parents=True)
    (BUNDLE / "Contents/Info.plist").write_text(info_plist())
    (ROOT / "docs/layouts").mkdir(parents=True, exist_ok=True)
    for name, layout_id, base, overrides in LAYOUTS:
        t = tables(base, overrides)
        (res / f"{name}.keylayout").write_text(keylayout(name, layout_id, t))
        # Badge icons from tools/make-icons.swift; macOS ignores TISIconLabels for keyboard layouts.
        shutil.copy(ROOT / "src/icons" / f"{slug(name)}.icns", res / f"{name}.icns")
        (ROOT / "docs/layouts" / f"{slug(name)}.svg").write_text(diagram(t, base))
    print(f"built {BUNDLE.name} v{VERSION}: {', '.join(n for n, *_ in LAYOUTS)}")


if __name__ == "__main__":
    main()
