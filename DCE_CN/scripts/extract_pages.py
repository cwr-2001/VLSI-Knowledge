# -*- coding: utf-8 -*-
"""Extract text from DC Explorer UG PDF by page range (1-based inclusive)."""
import sys
import fitz

start = int(sys.argv[1])
end = int(sys.argv[2])
out = sys.argv[3]
pdf = sys.argv[4] if len(sys.argv) > 4 else (
    r"d:\IC Design\VLSI\DC Explorer User Guide, version S-2021.06.pdf"
)

doc = fitz.open(pdf)
parts = []
for i in range(start - 1, min(end, doc.page_count)):
    parts.append(f"\n===== PAGE {i+1} =====\n")
    parts.append(doc[i].get_text("text"))

text = "".join(parts)
with open(out, "w", encoding="utf-8") as f:
    f.write(text)
print(f"Wrote pages {start}-{end} -> {out} ({len(text)} chars, {doc.page_count} total pages)")
