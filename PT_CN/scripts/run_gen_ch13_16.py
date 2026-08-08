# -*- coding: utf-8 -*-
"""Run gen_ch13.py through gen_ch16.py and print summary."""
import subprocess
import sys
from pathlib import Path

SCRIPTS = [
    Path(r"d:\IC Design\VLSI\PT_CN\scripts\gen_ch13.py"),
    Path(r"d:\IC Design\VLSI\PT_CN\scripts\gen_ch14.py"),
    Path(r"d:\IC Design\VLSI\PT_CN\scripts\gen_ch15.py"),
    Path(r"d:\IC Design\VLSI\PT_CN\scripts\gen_ch16.py"),
]

OUTS = [
    Path(r"d:\IC Design\VLSI\PT_CN\chapters\13_variation.tex"),
    Path(r"d:\IC Design\VLSI\PT_CN\chapters\14_multivoltage.tex"),
    Path(r"d:\IC Design\VLSI\PT_CN\chapters\15_smva.tex"),
    Path(r"d:\IC Design\VLSI\PT_CN\chapters\16_signal_integrity.tex"),
]

for s in SCRIPTS:
    print(f"=== {s.name} ===")
    r = subprocess.run([sys.executable, str(s)], capture_output=True, text=True, encoding="utf-8")
    print(r.stdout, end="")
    if r.returncode:
        print(r.stderr)
        sys.exit(r.returncode)

print("\n=== Summary ===")
for o in OUTS:
    t = o.read_text(encoding="utf-8")
    cjk = sum(1 for c in t if "\u4e00" <= c <= "\u9fff")
    lines = t.count("\n") + 1
    print(f"{o.name}: bytes={o.stat().st_size} lines={lines} CJK={cjk}")
