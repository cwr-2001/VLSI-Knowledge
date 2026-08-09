# -*- coding: utf-8 -*-
"""Fix broken colspecs; normalize tables to Synopsys-like grids."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"d:\IC Design\VLSI\PT_CN\chapters")


def extract_braced(s: str, open_idx: int) -> tuple[str, int]:
    assert s[open_idx] == "{"
    depth = 0
    for i in range(open_idx, len(s)):
        if s[i] == "{":
            depth += 1
        elif s[i] == "}":
            depth -= 1
            if depth == 0:
                return s[open_idx + 1 : i], i + 1
    raise ValueError("unbalanced braces")


def convert_colspec(spec: str, *, step_c: bool = False) -> str:
    s = spec.strip()
    s = s.replace("|@{|", "").replace("|@{}", "")
    if s.startswith("@{}"):
        s = s[3:]
    if s.endswith("@{}"):
        s = s[:-3]
    s = s.strip().strip("|").strip()

    tokens: list[str] = []
    i = 0
    while i < len(s):
        if s[i].isspace() or s[i] == "|":
            i += 1
            continue
        if s.startswith(">{", i):
            _, j = extract_braced(s, i + 1)
            i = j
            continue
        if s[i] in "clr":
            tokens.append(s[i])
            i += 1
            continue
        if s[i] in "pLCmX":
            letter = s[i]
            i += 1
            if i < len(s) and s[i] == "{":
                inner, i = extract_braced(s, i)
                tokens.append(f"{letter}{{{inner}}}")
            else:
                tokens.append(letter)
            continue
        i += 1

    out: list[str] = []
    for idx, t in enumerate(tokens):
        if t == "c" and step_c and idx == 0:
            out.append("C{1.2em}")
        elif t == "c":
            out.append("c")
        elif t == "l":
            out.append("l")
        elif t == "r":
            out.append("r")
        elif t.startswith("p{"):
            out.append("L" + t[1:])
        elif t.startswith(("L{", "C{", "X")):
            out.append(t)
        else:
            out.append(t)
    return "|" + "|".join(out) + "|"


def fix_longtable(text: str) -> str:
    needle = "\\begin{longtable}{"
    out: list[str] = []
    i = 0
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        brace_at = j + len(needle) - 1
        spec, k = extract_braced(text, brace_at)
        # STA flow and similar: leading c for step numbers
        step_c = (" c " in f" {spec} ") or spec.strip().startswith("c ") or "|c " in spec or spec.startswith("c ")
        # also broken form |@{|c
        if "c p{" in spec or spec.lstrip("|@{").startswith("c "):
            step_c = True
        new_spec = convert_colspec(spec, step_c=step_c)
        out.append(f"\\begin{{longtable}}{{{new_spec}}}")
        i = k
    return "".join(out)


def fix_tabular(text: str) -> str:
    needle = "\\begin{tabular}{"
    out: list[str] = []
    i = 0
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        brace_at = j + len(needle) - 1
        spec, k = extract_braced(text, brace_at)
        new_spec = convert_colspec(spec, step_c=False)
        out.append(f"\\begin{{tabular}}{{{new_spec}}}")
        i = k
    return "".join(out)


def fix_tabularx(text: str) -> str:
    # \begin{tabularx}{\textwidth}{cols}
    needle = "\\begin{tabularx}{"
    out: list[str] = []
    i = 0
    while True:
        j = text.find(needle, i)
        if j < 0:
            out.append(text[i:])
            break
        out.append(text[i:j])
        width_brace = j + len(needle) - 1
        width, k = extract_braced(text, width_brace)
        # skip spaces
        while k < len(text) and text[k].isspace():
            k += 1
        if k >= len(text) or text[k] != "{":
            out.append(text[j:k])
            i = k
            continue
        spec, k2 = extract_braced(text, k)
        new_spec = convert_colspec(spec, step_c=False)
        out.append(f"\\begin{{tabularx}}{{{width}}}{{{new_spec}}}")
        i = k2
    return "".join(out)


def wrap_sta_topics(text: str) -> str:
    start = text.find("\\label{tab:pt-sta-flow}")
    if start < 0:
        return text
    end = text.find("\\end{longtable}", start)
    if end < 0:
        return text
    block = text[start:end]
    lines = block.splitlines(keepends=True)
    new_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if (
            stripped.endswith("\\\\")
            and "&" not in stripped
            and not stripped.startswith("\\")
            and "步骤" not in stripped
        ):
            cell = stripped[:-2].strip()
            if cell and not cell.startswith("\\topicref"):
                indent = line[: len(line) - len(line.lstrip())]
                line = f"{indent}\\topicref{{{cell}}} \\\\\n"
        new_lines.append(line)
    return text[:start] + "".join(new_lines) + text[end:]


def bold_simple_headers(text: str) -> str:
    """Bold header row of tabular/tabularx that still lack \\tblhead / \\textbf."""
    lines = text.splitlines()
    out: list[str] = []
    for i, line in enumerate(lines):
        prev = lines[i - 1].strip() if i else ""
        nxt = lines[i + 1].strip() if i + 1 < len(lines) else ""
        if (
            prev == "\\hline"
            and "&" in line
            and "\\cmd" not in line
            and "\\tblhead" not in line
            and "\\textbf" not in line
            and "\\multicolumn" not in line
            and not line.strip().startswith("%")
            and (nxt == "\\hline" or nxt.startswith("\\end"))
        ):
            indent = re.match(r"^(\s*)", line).group(1)
            raw = line.strip()
            suf = ""
            if raw.endswith("\\\\"):
                raw, suf = raw[:-2].rstrip(), " \\\\"
            cells = [c.strip() for c in raw.split("&")]
            if cells and all(
                c and "\\" not in c and len(c) < 40 for c in cells
            ):
                line = indent + " & ".join(f"\\tblhead{{{c}}}" for c in cells) + suf
        out.append(line)
    return "\n".join(out) + ("\n" if text.endswith("\n") else "")


def fix_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    orig = text
    text = fix_longtable(text)
    text = fix_tabular(text)
    text = fix_tabularx(text)
    if path.name == "02_getting_started.tex":
        text = wrap_sta_topics(text)
    text = bold_simple_headers(text)
    if text != orig:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = [p.name for p in sorted(ROOT.glob("*.tex")) if fix_file(p)]
    print("changed:", ", ".join(changed) if changed else "(none)")
    sample = (ROOT / "02_getting_started.tex").read_text(encoding="utf-8")
    idx = sample.find("\\begin{longtable}{")
    brace = idx + len("\\begin{longtable}")
    spec, _ = extract_braced(sample, brace)
    print("ch02 colspec:", spec)
    print("has topicref:", "\\topicref" in sample)


if __name__ == "__main__":
    main()
