# -*- coding: utf-8 -*-
"""Restore paired \\$...\\$ back to $...$ (math mode), leave lone \\$ (env vars)."""
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "chapters"

# Paired escaped dollars on one line (non-greedy). Skip empty.
# Allow nested LaTeX macros inside.
pair = re.compile(r"\\\$((?:[^$\n]|\\\$)*?)\\\$")

def restore_line(line: str) -> str:
    # Don't touch lstlisting content handled at file level
    def repl(m: re.Match) -> str:
        inner = m.group(1)
        # Env-var-like single tokens: APACHEROOT, APACHEDA_..., LD_LIBRARY_PATH
        if re.fullmatch(r"[A-Z][A-Z0-9_\\]*", inner):
            # Keep escaped: \$APACHEROOT
            return m.group(0)
        return f"${inner}$"

    return pair.sub(repl, line)


def protect_listings(text: str):
    pattern = re.compile(
        r"(\\begin\{lstlisting\}.*?\\end\{lstlisting\}|"
        r"\\begin\{verbatim\}.*?\\end\{verbatim\})",
        re.S,
    )
    last = 0
    parts = []
    for m in pattern.finditer(text):
        parts.append(("txt", text[last : m.start()]))
        parts.append(("code", m.group(0)))
        last = m.end()
    parts.append(("txt", text[last:]))
    return parts


for p in sorted(root.glob("*.tex")):
    text = p.read_text(encoding="utf-8")
    out = []
    changed = False
    for kind, chunk in protect_listings(text):
        if kind == "code":
            out.append(chunk)
            continue
        lines = chunk.split("\n")
        new_lines = [restore_line(L) for L in lines]
        new_chunk = "\n".join(new_lines)
        if new_chunk != chunk:
            changed = True
        out.append(new_chunk)
    if changed:
        p.write_text("".join(out), encoding="utf-8")
        print("restored math pairs in", p.name)

# spot check
for fname in ["15_reliability_em.tex", "03_ui_data_prep.tex", "12_package_board.tex"]:
    t = (root / fname).read_text(encoding="utf-8")
    print("---", fname)
    for i, line in enumerate(t.splitlines(), 1):
        if "mathrm{peak}" in line or "APACHEDA_TEMPLATE" in line or "rightarrow" in line:
            print(i, line[:140])
            break
