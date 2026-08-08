# -*- coding: utf-8 -*-
"""Run all chapter generators (09-12) and print size/CJK summary."""
from pathlib import Path
import re
import subprocess
import sys

scripts = [
    "build_ch09_11.py",
    "build_ch10.py",
    "build_ch11.py",
    "gen_ch12.py",
]

base = Path(__file__).resolve().parent
for s in scripts:
  p = base / s
  print(f"=== {s} ===")
  r = subprocess.run([sys.executable, str(p)], capture_output=True, text=True, encoding="utf-8")
  print(r.stdout, end="")
  if r.stderr:
    print(r.stderr, file=sys.stderr)
  if r.returncode != 0:
    sys.exit(r.returncode)

chapters = [
    "09_operating_conditions.tex",
    "10_delay_calculation.tex",
    "11_back_annotation.tex",
    "12_case_mode.tex",
]
chap_dir = base.parent / "chapters"
print("\n=== Summary ===")
for c in chapters:
    p = chap_dir / c
    t = p.read_text(encoding="utf-8")
    cjk = len(re.findall(r"[\u4e00-\u9fff]", t))
    print(f"{c}: {p.stat().st_size} bytes, {len(t.splitlines())} lines, CJK={cjk}")
