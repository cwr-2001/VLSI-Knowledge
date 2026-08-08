# -*- coding: utf-8 -*-
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent / "chapters"
pair = re.compile(r"\\\$([^$\n]+?)\\\$")
ENV_HINT = re.compile(
    r"APACHE|LD_LIBRARY|PATH|HOME|ROOT|TEMPLATE|LICENSE|USER|PWD",
    re.I,
)


def repl(m):
    inner = m.group(1)
    # Keep env-style: $APACHEROOT, $APACHEDA_TEMPLATE_GSR, $LD_LIBRARY_PATH
    raw = inner.replace("\\_", "_").replace("\\", "")
    if ENV_HINT.search(raw) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_/]*", raw):
        return m.group(0)
    return f"${inner}$"


for p in sorted(root.glob("*.tex")):
    text = p.read_text(encoding="utf-8")
    parts = re.split(
        r"(\\begin\{lstlisting\}.*?\\end\{lstlisting\}|"
        r"\\begin\{verbatim\}.*?\\end\{verbatim\})",
        text,
        flags=re.S,
    )
    out = []
    for part in parts:
        if part.startswith(r"\begin{lstlisting}") or part.startswith(r"\begin{verbatim}"):
            out.append(part)
        else:
            out.append(pair.sub(repl, part))
    new = "".join(out)
    if new != text:
        p.write_text(new, encoding="utf-8")
        print("fixed", p.name)

for fname in ["04_power_static_em.tex", "12_package_board.tex", "03_ui_data_prep.tex"]:
    t = (root / fname).read_text(encoding="utf-8")
    for i, line in enumerate(t.splitlines(), 1):
        if "P_K" in line or "Z_0" in line or "APACHEDA_TEMPLATE" in line:
            print(fname, i, line[:130])
            break
