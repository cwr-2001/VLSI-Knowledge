# -*- coding: utf-8 -*-
"""Verify RH_CN chapters 1-6 tex files exist and report line counts."""
from __future__ import annotations

from pathlib import Path

import rh_tex_utils as u

CHAPTERS = [
    ("01_introduction.tex", "第1章 引言"),
    ("02_redhawk_flow.tex", "第2章 RedHawk 流程"),
    ("03_ui_data_prep.tex", "第3章 用户界面与数据准备"),
    ("04_power_static_em.tex", "第4章 功耗/静态IR/EM"),
    ("05_dynamic_vd.tex", "第5章 动态压降"),
    ("06_reports.tex", "第6章 报告"),
]


def main() -> None:
    print("RH_CN chapters 1-6 status:")
    for fname, title in CHAPTERS:
        path = u.CHAPTERS / fname
        if not path.exists():
            print(f"  MISSING: {fname}")
            continue
        text = path.read_text(encoding="utf-8")
        sections = [
            ln.split("{")[1].split("}")[0]
            for ln in text.splitlines()
            if ln.startswith("\\section{")
        ]
        print(f"  {title}: {len(text.splitlines())} lines, {len(sections)} sections")
        for s in sections:
            print(f"    - {s}")


if __name__ == "__main__":
    main()
