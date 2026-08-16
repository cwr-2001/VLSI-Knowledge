# -*- coding: utf-8 -*-
"""Extract table-like report/command-output figures from EN FC UG."""
from __future__ import annotations

import importlib.util
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "scripts" / "extract_figures_ch01_02.py"

spec = importlib.util.spec_from_file_location("fc_extract", BASE)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

# (stem, page, caption_or_phrase, mode)
FIGURES = [
    ("fig-cg-rpto-opts", 300, "Figure 50 Output of the report_clock_gating_options Command", "figure"),
    ("fig-cg-rpto-no-obj", 300, "Figure 51 Command Output With no Options set to Specific Objects", "figure"),
    ("fig-cg-rpto-params", 301, "Figure 52 Command Output With no Specific Object Options but Passed as Parameters", "figure"),
    ("fig-cg-rpto-same", 301, "Figure 53 Command Output With the Same Option set to Multiple Objects", "figure"),
    ("fig-cg-rpto-nosplit", 301, "Figure 54", "figure"),
    ("fig-cg-rpt", 321, "Figure 64 Example of a report_clock_gating Report", "figure"),
    ("fig-cg-multibit-rpt", 322, "Figure 65 Example of a Multibit Composition Report", "figure"),
    ("fig-cg-eff-rpt", 324, "The following figure shows the report_clock_gating_efficiency", "phrase"),
    ("fig-cg-eff-by-reg", 325, "report_clock_gating_efficiency -by_register", "phrase"),
    ("fig-cg-eff-by-cg", 326, "report_clock_gating_efficiency -by_clock_gate", "phrase"),
    ("fig-qorsum-report", 271, "Figure 38 QORsum Report", "figure"),
    ("fig-comparison-report", 277, "Figure 41 Comparison Report", "figure"),
    ("fig-verilog-select-op", 228, "Figure 32 Verilog Output—SELECT_OP and Selection Logic", "figure"),
]


def extract_phrase_below(doc, stem: str, page_no: int, key: str) -> Path:
    """Art below a phrase (used when caption is missing)."""
    page = doc[page_no - 1]
    out = mod.OUT_DIR / f"{stem}.png"
    r = mod.find_block_containing(page, key)
    if r is None:
        raise RuntimeError(f"phrase not found: {key}")
    y0 = r.y1 + 2
    y1 = mod.stop_y(page, y0)
    # if little room left on page, art may be above
    if y1 - y0 < 40:
        y1 = r.y0 - 2
        y0 = 90
        mod.render_clip(page, mod.figure_clip(page, y0, y1), out)
    else:
        mod.render_clip(page, mod.figure_clip(page, y0, y1), out)
    return out


def main() -> int:
    from PIL import Image

    doc = mod.fitz.open(mod.PDF)
    mod.OUT_DIR.mkdir(parents=True, exist_ok=True)
    ok = fail = 0
    for stem, page_no, key, mode in FIGURES:
        try:
            if mode == "phrase_below":
                path = extract_phrase_below(doc, stem, page_no, key)
            else:
                path = mod.extract_one(doc, stem, page_no, key, mode)
            im = Image.open(path)
            print(
                f"OK  {stem:28s} p{page_no:<4d} "
                f"{im.size[0]:4d}x{im.size[1]:<4d} {path.stat().st_size:7d}B"
            )
            ok += 1
        except Exception as e:
            print(f"FAIL {stem:28s} p{page_no:<4d} {e}")
            fail += 1
    print(f"Done: {ok} ok, {fail} fail")
    return 0 if fail == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
