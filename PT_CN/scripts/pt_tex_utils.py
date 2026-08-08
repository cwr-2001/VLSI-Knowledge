# -*- coding: utf-8 -*-
"""Shared LaTeX helpers for PT_CN chapter generators."""
from __future__ import annotations

import re
from pathlib import Path


def esc(text: str) -> str:
    """Escape LaTeX special chars in plain text (not commands)."""
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = text
    for k, v in repl.items():
        out = out.replace(k, v)
    return out


def cmd(name: str) -> str:
    escaped = name.replace("_", r"\_")
    return rf"\cmd{{{escaped}}}"


def opt(name: str) -> str:
    escaped = name.replace("_", r"\_")
    return rf"\opt{{{escaped}}}"


def section(zh: str, en: str) -> str:
    return f"\\section{{{zh}}}\n\\subsection*{{{en}}}\n\n"


def subsection(zh: str, en: str) -> str:
    return f"\\subsection{{{zh}}}\n\\subsubsection*{{{en}}}\n\n"


def subsubsection(zh: str, en: str) -> str:
    return f"\\subsubsection{{{zh}}}\n\\paragraph*{{{en}}}\n\n"


def fig(fig_id: str, zh_cap: str, label: str) -> str:
    return f"\\figplaceholder{{{fig_id}}}{{{zh_cap}}}{{{label}}}\n\n"


def note(body: str) -> str:
    return f"\\begin{{noteBox}}\n{body}\n\\end{{noteBox}}\n\n"


def see_also(items: list[str]) -> str:
    if len(items) == 1:
        body = items[0]
    else:
        inner = "\n".join(f"  \\item {it}" for it in items)
        body = f"\\begin{{itemize}}\n{inner}\n\\end{{itemize}}"
    return f"\\begin{{seeAlsoBox}}\n{body}\n\\end{{seeAlsoBox}}\n\n"


def lst(code: str, caption: str = "") -> str:
    cap = f"\n\\caption{{{caption}}}" if caption else ""
    return f"\\begin{{lstlisting}}{cap}\n{code}\n\\end{{lstlisting}}\n\n"


def itemize(items: list[str], env: str = "itemize") -> str:
    lines = "\n".join(f"  \\item {it}" for it in items)
    return f"\\begin{{{env}}}\n{lines}\n\\end{{{env}}}\n\n"


def ident(name: str) -> str:
    """Inline English identifier in text mode."""
    return r"\texttt{" + name.replace("_", r"\_") + "}"


def write_tex(out_path: Path, parts: list[str]) -> int:
    text = "".join(parts)
    out_path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u4e00-\u9fff]", text))


def chapter_header(num: int, zh: str, en: str, label: str) -> str:
    return (
        f"% 第 {num} 章 {en}\n"
        f"\\bichapter{{{zh}}}{{{en}}}\n"
        f"\\label{{{label}}}\n\n"
    )
