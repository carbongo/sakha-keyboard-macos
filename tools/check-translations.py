#!/usr/bin/env python3
"""Fail if a translated README/CONTRIBUTING drifts structurally from the English one."""
import re, sys

def shape(path):
    lines = open(path, encoding="utf-8").read().splitlines()
    out, fence = [], False
    for l in lines:
        if l.startswith("```"):
            fence = not fence
            out.append("```")
        elif fence:
            if not l.startswith("#"):
                out.append("code:" + l)  # commands match verbatim; comments are translated
        elif m := re.match(r"(#+) ", l):
            out.append(m[1])
        elif l.startswith(("<details>", "</details>", "![", "> [!")):
            out.append(l.split("(")[0] if l.startswith("![") else l)
        elif l.startswith("|"):
            out.append("|")
        elif re.match(r"\d+\. ", l):
            out.append("1.")
    return out

bad = False
for base, langs in (("README", ("ru", "sah")), ("CONTRIBUTING", ("ru", "sah"))):
    ref = shape(f"{base}.md")
    for lang in langs:
        path = f"{base}.{lang}.md"
        if shape(path) != ref:
            print(f"::error file={path}::{path} is out of step with {base}.md (headings, lists, tables, code or images differ)")
            bad = True
sys.exit(bad)
