# -*- coding: utf-8 -*-
"""Fix env-var style \$VAR that should remain as \\$VAR inside texttt."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "chapters"
# Patterns like \texttt{\$APACHEDA\_TEMPLATE\_GSR} are OK
# Broken: \texttt{$APACHEDA...} or bare $APACHEDA after restore short math
# Also: \texttt{\$APACHEDA\_TEMPLATE\_GSR} from dollar escape is fine

# Fix cases where short-math restore made $AP$ACHE... — unlikely
# Fix: texttt containing unescaped $ 
pat = re.compile(r"\\texttt\{([^}]*)\}")

def fix_inner(m):
    inner = m.group(1)
    # ensure $ is escaped inside texttt
    inner2 = re.sub(r"(?<!\\)\$", r"\\$", inner)
    return "\\texttt{" + inner2 + "}"

for p in sorted(root.glob("*.tex")):
    text = p.read_text(encoding="utf-8")
    new = pat.sub(fix_inner, text)
    if new != text:
        p.write_text(new, encoding="utf-8")
        print("fixed texttt dollars in", p.name)
