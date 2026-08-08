# -*- coding: utf-8 -*-
from pathlib import Path
import re

p = Path(r"d:\IC Design\VLSI\ICV_CN\chapters\F_third_party.tex")
t = p.read_text(encoding="utf-8")


def escape_underscores(title: str) -> str:
    out = []
    i = 0
    while i < len(title):
        if title[i] == "\\" and i + 1 < len(title):
            out.append(title[i : i + 2])
            i += 2
            continue
        if title[i] == "_":
            out.append("\\_")
            i += 1
            continue
        out.append(title[i])
        i += 1
    return "".join(out)


def repl(m):
    return m.group(1) + "{" + escape_underscores(m.group(2)) + "}"


t2 = re.sub(r"(\\sub(?:sub)?section\*?)\s*\{([^}]*)\}", repl, t)
t2 = re.sub(
    r"(以下为 )([^\n]+)( 的许可)",
    lambda m: m.group(1) + escape_underscores(m.group(2)) + m.group(3),
    t2,
)
p.write_text(t2, encoding="utf-8")

for i, ln in enumerate(t2.splitlines(), 1):
    if "cx" in ln.lower() and ("subsection" in ln or "以下为" in ln):
        print(f"{i}:{ln}")
print("ok")
