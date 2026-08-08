# -*- coding: utf-8 -*-
import re
from pathlib import Path

p = Path(__file__).resolve().parent.parent / "chapters" / "C_file_defs.tex"
t = p.read_text(encoding="utf-8")
# WIRESEGMENT \$ \$STARTX \$STARTY ... -> readable field list
t2 = re.sub(
    r"WIRESEGMENT(?:\s*\\\$\s*)+(?:\\\$)?",
    "WIRESEGMENT fields: ",
    t,
)
# Remaining \$FIELDNAME -> \texttt{FIELDNAME}
t2 = re.sub(r"\\\$([A-Z][A-Z0-9_]*)", r"\\texttt{\1}", t2)
# Lone \$ leftover
t2 = t2.replace("\\$ ", "")
if t2 != t:
    p.write_text(t2, encoding="utf-8")
    print("updated C_file_defs.tex")
else:
    print("no change")

# show EM_WORST lines
for i, line in enumerate(t2.splitlines(), 1):
    if "EM_WORST" in line:
        print(i, line[:180])
