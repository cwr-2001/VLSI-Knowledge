# -*- coding: utf-8 -*-
"""Fix literal \\n and markdown headers in PT_CN chapter tex files."""
from pathlib import Path
import re

chapters = Path(r"d:\IC Design\VLSI\PT_CN\chapters")

def fix_literal_n(text: str) -> str:
    # Replace literal backslash-n with real newlines (but keep \\n in rare intentional cases)
    # Pattern: \n that appears as escaped newline from bad Python string joining
    return text.replace("\\n", "\n")

def fix_md_headers(text: str) -> str:
    lines = text.splitlines()
    out = []
    for line in lines:
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            # If title looks like English-only subsection marker after Chinese section, keep as subsection*
            if level == 1:
                out.append(f"\\section{{{title}}}")
            elif level == 2:
                out.append(f"\\subsection{{{title}}}")
            elif level == 3:
                out.append(f"\\subsubsection{{{title}}}")
            else:
                out.append(f"\\paragraph{{{title}}}")
        else:
            out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")

for p in sorted(chapters.glob("*.tex")):
    if p.name.startswith("_"):
        continue
    raw = p.read_text(encoding="utf-8")
    new = raw
    if "\\n" in new and p.name == "11_back_annotation.tex":
        new = fix_literal_n(new)
    if re.search(r"(?m)^#{1,4} ", new):
        new = fix_md_headers(new)
    if new != raw:
        p.write_text(new, encoding="utf-8")
        print(f"fixed {p.name}: {len(raw)} -> {len(new)}")
    else:
        # still report md/n status
        pass

print("done")
