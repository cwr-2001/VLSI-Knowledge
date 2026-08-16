# -*- coding: utf-8 -*-
"""Patch table-like figure placeholders to includegraphics; reuse ch2 clock figs; drop DEF fake figure."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CH = ROOT / "chapters"

# label -> (png, width)
MAP = {
    "fig:cg-rpto-opts": ("fig-cg-rpto-opts.png", "0.95"),
    "fig:cg-rpto-no-obj": ("fig-cg-rpto-no-obj.png", "0.95"),
    "fig:cg-rpto-params": ("fig-cg-rpto-params.png", "0.95"),
    "fig:cg-rpto-same": ("fig-cg-rpto-same.png", "0.95"),
    "fig:cg-rpto-nosplit": ("fig-cg-rpto-nosplit.png", "0.95"),
    "fig:cg-rpt": ("fig-cg-rpt.png", "0.72"),
    "fig:cg-multibit-rpt": ("fig-cg-multibit-rpt.png", "0.55"),
    "fig:cg-eff-rpt": ("fig-cg-eff-rpt.png", "0.92"),
    "fig:cg-eff-ex": ("fig-cg-eff-by-cg.png", "0.92"),
    "fig:qorsum-report": ("fig-qorsum-report.png", "0.95"),
    "fig:cmp-report": ("fig-comparison-report.png", "0.95"),
    # ch4 duplicates of ch2 extractions
    "fig:cg-latency-design": ("fig-clk-lat-cg.png", "0.92"),
    "fig:cg-stage-latency": ("fig-cg-stages.png", "0.70"),
    "fig:cg-fanout-latency": ("fig-lat-fanout.png", "0.55"),
    "fig:select-op-verilog": ("fig-verilog-select-op.png", "0.85"),
}

FIG_RE = re.compile(
    r"\\begin\{figure\}\[[^\]]*\]\s*"
    r"\\centering\s*"
    r"(?:\\fbox\{.*?\}|\\includegraphics\[[^\]]*\]\{[^}]+\})"
    r"\s*\\caption\{(?P<cap>.*?)\}\s*"
    r"\\label\{(?P<label>[^}]+)\}\s*"
    r"\\end\{figure\}",
    re.S,
)

DEF_FIG_RE = re.compile(
    r"\\begin\{figure\}\[[^\]]*\]\s*"
    r"\\centering\s*"
    r"\\fbox\{.*?DEF Port Location Information.*?"
    r"\\caption\{DEF Port 位置信息（示例占位）\}\s*"
    r"\\label\{ex:def-port-loc\}\s*"
    r"\\end\{figure\}\s*",
    re.S,
)


def make_fig(cap: str, label: str, png: str, w: str) -> str:
    return (
        "\\begin{figure}[htbp]\n"
        "\\centering\n"
        f"\\includegraphics[width={w}\\textwidth,keepaspectratio]{{figures/{png}}}\n"
        f"\\caption{{{cap}}}\n"
        f"\\label{{{label}}}\n"
        "\\end{figure}"
    )


def patch_file(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8")
    n_fig = 0
    n_def = 0

    if path.name == "02_preparing_design.tex":
        new, n_def = DEF_FIG_RE.subn(
            "% DEF Port Location Information example follows as listing "
            "(原书 Example 1，非插图)\n\n",
            text,
            count=1,
        )
        text = new

    # resolve verilog label if present
    local_map = dict(MAP)

    def repl(m: re.Match[str]) -> str:
        nonlocal n_fig
        label = m.group("label")
        cap = m.group("cap")
        if label not in local_map:
            return m.group(0)
        png, w = local_map[label]
        if not (ROOT / "figures" / png).exists():
            return m.group(0)
        n_fig += 1
        return make_fig(cap, label, png, w)

    text2 = FIG_RE.sub(repl, text)
    if text2 != text or n_def:
        path.write_text(text2, encoding="utf-8")
    return n_fig, n_def


def main() -> None:
    files = [
        CH / "02_preparing_design.tex",
        CH / "03_physical_synthesis.tex",
        CH / "04_clock_gating.tex",
    ]
    for path in files:
        if not path.exists():
            print("skip missing", path.name)
            continue
        n_fig, n_def = patch_file(path)
        left = len(re.findall(r"\\fbox\{\\parbox", path.read_text(encoding="utf-8")))
        print(f"{path.name}: patched figs={n_fig}, def_removed={n_def}, remaining fbox={left}")


if __name__ == "__main__":
    main()
