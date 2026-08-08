# -*- coding: utf-8 -*-
"""Strip PDF page headers/footers from DCE raw chapter extracts."""
import re
from pathlib import Path

SKIP = re.compile(
    r"^(===== PAGE \d+ =====|Feedback|DC Explorer User Guide|S-2021\.06|"
    r"Chapter \d+: .+|\d{2,3})$"
)

def clean(path: Path) -> str:
    out = []
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        s = line.rstrip()
        t = s.strip().replace("\xa0", " ")
        if SKIP.match(t):
            continue
        out.append(s.replace("\xa0", " "))
    # collapse 3+ blank lines
    text = "\n".join(out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"

def main():
    base = Path(__file__).resolve().parent
    for name in ("raw_ch09.txt", "raw_ch10.txt", "raw_ch11.txt"):
        src = base / name
        dst = base / ("_clean_" + name)
        dst.write_text(clean(src), encoding="utf-8")
        print(f"{name} -> {dst.name}: {dst.stat().st_size} bytes")

if __name__ == "__main__":
    main()
