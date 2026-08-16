# -*- coding: utf-8 -*-
"""Replace ch1–ch2 figure placeholders with includegraphics."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LABEL_TO_FIG = {
    "fig:physyn-flow": "fig-physyn-flow.png",
    "fig:formality-flow": "fig-formality-flow.png",
    "fig:pnr-flow": "fig-pnr-flow.png",
    "fig:upf-flows": "fig-upf-flows.png",
    "fig:dp-example": "fig-dp-example.png",
    "fig:odd-cycle": "fig-odd-cycle.png",
    "fig:no-odd-cycle": "fig-no-odd-cycle.png",
    "fig:lib-config": "fig-lib-config.png",
    "fig:logic-hier": "fig-logic-hier.png",
    "fig:fc-lib-analysis-flow": "fig-fc-lib-analysis-flow.png",
    "fig:fc-lib-monotonic": "fig-fc-lib-monotonic.png",
    "fig:fc-lib-redundant": "fig-fc-lib-redundant.png",
    "fig:fc-lib-outlier": "fig-fc-lib-outlier.png",
    "fig:fc-lib-equivalent": "fig-fc-lib-equivalent.png",
    "fig:fc-lib-gap": "fig-fc-lib-gap.png",
    "fig:merge-va": "fig-merge-va.png",
    "fig:nested-va": "fig-nested-va.png",
    "fig:va-guard": "fig-va-guard.png",
    "fig:eff-bound": "fig-eff-bound.png",
    "fig:phys-ft": "fig-phys-ft.png",
    "fig:phys-ft-off": "fig-phys-ft-off.png",
    "fig:ft-buf-diff": "fig-ft-buf-diff.png",
    "fig:clk-lat-cg": "fig-clk-lat-cg.png",
    "fig:cg-stages": "fig-cg-stages.png",
    "fig:lat-fanout": "fig-lat-fanout.png",
    "fig:keepout": "fig-keepout.png",
    "fig:ch2b-ir-drop-categories": "fig-ch2b-ir-drop-categories.png",
    "fig:ch2b-equiv-pin-loc": "fig-ch2b-equiv-pin-loc.png",
    "fig:ch2b-equiv-pin-color": "fig-ch2b-equiv-pin-color.png",
    "fig:ch2b-drc-disabled": "fig-ch2b-drc-disabled.png",
    "fig:ch2b-port-isolation": "fig-ch2b-port-isolation.png",
    "fig:ch2b-multiport-nets": "fig-ch2b-multiport-nets.png",
    "fig:ch2b-clock-net-types": "fig-ch2b-clock-net-types.png",
    "fig:ch2b-root-fanout": "fig-ch2b-root-fanout.png",
    "fig:ch2b-level-ndr": "fig-ch2b-level-ndr.png",
}

WIDTH = {
    "fig:pnr-flow": "0.55",
    "fig:nested-va": "0.45",
    "fig:eff-bound": "0.45",
    "fig:ch2b-equiv-pin-loc": "0.45",
    "fig:ch2b-equiv-pin-color": "0.45",
    "fig:ch2b-level-ndr": "0.50",
    "fig:lat-fanout": "0.55",
    "fig:lib-config": "0.70",
    "fig:formality-flow": "0.85",
    "fig:physyn-flow": "0.85",
    "fig:ch2b-multiport-nets": "0.75",
    "fig:ch2b-port-isolation": "0.95",
    "fig:cg-stages": "0.70",
    "fig:ch2b-drc-disabled": "0.85",
}

FIG_RE = re.compile(
    r"\\begin\{figure\}\[[^\]]*\]\s*"
    r"\\centering\s*"
    r"\\fbox\{.*?\}"
    r"\s*\\caption\{(?P<cap>.*?)\}\s*"
    r"\\label\{(?P<label>[^}]+)\}\s*"
    r"\\end\{figure\}",
    re.S,
)

FILES = [
    ROOT / "chapters" / "01_working_with_fc.tex",
    ROOT / "chapters" / "02_preparing_design.tex",
    ROOT / "chapters" / "02_fc_extra_sections.tex",
]


def main() -> None:
    total = 0
    for path in FILES:
        text = path.read_text(encoding="utf-8")
        count = 0

        def repl(m: re.Match[str]) -> str:
            nonlocal count
            label = m.group("label")
            cap = m.group("cap")
            png = LABEL_TO_FIG.get(label)
            if not png or not (ROOT / "figures" / png).exists():
                return m.group(0)
            w = WIDTH.get(label, "0.92")
            count += 1
            return (
                "\\begin{figure}[htbp]\n"
                "\\centering\n"
                f"\\includegraphics[width={w}\\textwidth,keepaspectratio]{{figures/{png}}}\n"
                f"\\caption{{{cap}}}\n"
                f"\\label{{{label}}}\n"
                "\\end{figure}"
            )

        new = FIG_RE.sub(repl, text)
        path.write_text(new, encoding="utf-8")
        left = len(re.findall(r"\\fbox\{\\parbox", new))
        print(f"{path.name}: replaced {count}, remaining fbox {left}")
        total += count
    print("total replaced", total)


if __name__ == "__main__":
    main()
