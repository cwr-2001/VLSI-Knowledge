# -*- coding: utf-8 -*-
"""Shared LaTeX helpers for RH_CN chapter generators."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHAPTERS = ROOT / "chapters"
SCRIPTS = Path(__file__).resolve().parent


def esc(text: str) -> str:
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


def gsr(name: str) -> str:
    return rf"\gsr{{{name}}}"


def cmd(name: str) -> str:
    return rf"\cmd{{{name.replace('_', r'\_')}}}"


def section(zh: str, en: str) -> str:
    return f"\\section{{{zh}}}\n\\subsection*{{{en}}}\n\n"


def subsection(zh: str, en: str) -> str:
    return f"\\subsection{{{zh}}}\n\\subsubsection*{{{en}}}\n\n"


def subsubsection(zh: str, en: str) -> str:
    return f"\\subsubsection{{{zh}}}\n\\paragraph*{{{en}}}\n\n"


def fig(fig_id: str, zh_cap: str, label: str = "") -> str:
    lbl = f"\n\\label{{{label}}}" if label else ""
    return f"\\figplaceholder{{{fig_id}}}{{{zh_cap}}}{lbl}\n\n"


def note(body: str) -> str:
    return f"\\begin{{noteBox}}\n{body}\n\\end{{noteBox}}\n\n"


def see_also(body: str) -> str:
    return f"\\begin{{seeAlsoBox}}\n{body}\n\\end{{seeAlsoBox}}\n\n"


def lst(code: str) -> str:
    return f"\\begin{{lstlisting}}\n{code}\n\\end{{lstlisting}}\n\n"


def read_raw(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8", errors="replace")


def write_chapter(filename: str, content: str) -> int:
    path = CHAPTERS / filename
    path.write_text(content, encoding="utf-8")
    return len(content.splitlines())
