# -*- coding: utf-8 -*-
from pathlib import Path
d = Path(r"d:\IC Design\VLSI\PT_CN\chapters")
stubs = []
total_cjk = 0
for p in sorted(d.glob("*.tex")):
    if p.name.startswith("_"):
        continue
    t = p.read_text(encoding="utf-8", errors="replace")
    stub = "chapterstub" in t
    cjk = sum(1 for c in t if "\u4e00" <= c <= "\u9fff")
    total_cjk += cjk
    flag = "STUB" if stub else "OK"
    if stub:
        stubs.append(p.name)
    print(f"{flag:4} {p.name:35} {p.stat().st_size:8} CJK={cjk}")
print("TOTAL_CJK", total_cjk)
print("STUBS", stubs)
