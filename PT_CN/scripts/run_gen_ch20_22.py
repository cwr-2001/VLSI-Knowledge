# -*- coding: utf-8 -*-
"""Run generators for PT_CN chapters 20-22."""
from pathlib import Path
import subprocess
import sys

SCRIPTS = Path(__file__).resolve().parent
GENS = ["gen_ch20_gui.py", "gen_ch21_eco_flow.py", "gen_ch22.py"]


def main() -> int:
    for name in GENS:
        print(f"=== {name} ===")
        r = subprocess.run([sys.executable, str(SCRIPTS / name)], check=False)
        if r.returncode != 0:
            return r.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
