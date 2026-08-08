# -*- coding: utf-8 -*-
"""Split full OCR into per-lab raw text files."""
import re
from pathlib import Path

RAW = Path(__file__).with_name("raw_all.txt")
OUT = Path(__file__).parent

# PDF page ranges (1-based, inclusive): (start, end, filename, title)
RANGES = [
    (1, 2, "raw_front.txt", "Front matter"),
    (3, 18, "raw_lab01.txt", "Lab 1 PrimeTime Flow"),
    (19, 32, "raw_lab02.txt", "Lab 2 Constraining Methodology"),
    (33, 50, "raw_lab03.txt", "Lab 3 Generating Reports"),
    (51, 70, "raw_lab04.txt", "Lab 4 Constraining Multiple Clocks"),
    (71, 82, "raw_lab05.txt", "Lab 5 Additional Constraints"),
    (83, 90, "raw_lab07.txt", "Lab 7 Path-Based Analysis"),
    (91, 102, "raw_lab08.txt", "Lab 8 SI Delay Analysis"),
    (103, 114, "raw_lab09.txt", "Lab 9 SI Noise Analysis"),
    (115, 124, "raw_job_aids.txt", "Job Aids"),
]

text = RAW.read_text(encoding="utf-8")
parts = re.split(r"={20} PAGE (\d+) ={20}\n", text)
pages = {}
for i in range(1, len(parts), 2):
    pages[int(parts[i])] = parts[i + 1]

for start, end, name, title in RANGES:
    chunks = []
    for p in range(start, end + 1):
        chunks.append(f"===== PAGE {p} =====\n{pages.get(p, '')}")
    out = OUT / name
    out.write_text(f"# {title}\n# PDF pages {start}-{end}\n\n" + "\n".join(chunks), encoding="utf-8")
    print(f"wrote {out.name} ({end - start + 1} pages)")
