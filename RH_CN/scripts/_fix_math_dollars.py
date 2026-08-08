# -*- coding: utf-8 -*-
"""Restore legitimate math-mode $...$ that were over-escaped to \$...\$."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "chapters"

# 1) Restore \$\command$ / \$\command{...}\$
pat_cmd = re.compile(r"\\\$(\\[a-zA-Z]+(?:\{[^{}]*\})?)\\\$")
# 2) Restore short simple math \$x\$, \$n\$, \$1\$
pat_short = re.compile(r"\\\$([A-Za-z0-9]{1,3})\\\$")

for p in sorted(root.glob("*.tex")):
    text = p.read_text(encoding="utf-8")
    n1 = len(pat_cmd.findall(text))
    text2 = pat_cmd.sub(r"$\1$", text)
    n2 = len(pat_short.findall(text2))
    text3 = pat_short.sub(r"$\1$", text2)
    if text3 != text:
        p.write_text(text3, encoding="utf-8")
        print(f"{p.name}: cmd_math={n1} short_math={n2}")

# verify ch3
t = (root / "03_ui_data_prep.tex").read_text(encoding="utf-8")
for i, line in enumerate(t.splitlines(), 1):
    if "rightarrow" in line or "Export GUI" in line:
        print(i, line[:160])
