# -*- coding: utf-8 -*-
"""Parsing and translation helpers for RH_CN appendix refinement."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional


# ---------------------------------------------------------------------------
# LaTeX helpers
# ---------------------------------------------------------------------------

def fix_tex_escapes(content: str) -> str:
    tab = "\t"
    for cmd in (
        "texttt", "textbf", "textwidth", "textasciitilde",
        "textasciicircum", "textbackslash",
    ):
        content = content.replace(tab + cmd, "\\" + cmd)
    return content


def latex_escape(s: str) -> str:
    repl = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = s
    for a, b in repl.items():
        out = out.replace(a, b)
    return out


def lst_escape(s: str) -> str:
    """Escape for lstlisting — keep command syntax readable."""
    return s.replace("\\", "\\\\")


def cjk_ratio(s: str) -> float:
    if not s:
        return 0.0
    cjk = sum(1 for c in s if "\u4e00" <= c <= "\u9fff")
    return cjk / len(s)


# ---------------------------------------------------------------------------
# Raw text cleaning
# ---------------------------------------------------------------------------

HEADER_PAT = re.compile(
    r"(?:ANSYS[^\n]*|RedHawk User Manual[^\n]*|APPENDIX [A-F][^\n]*|"
    r"Global System Requirements[^\n]*|Apache Technology File[^\n]*|"
    r"TCL / Script Commands[^\n]*|RedHawk Graphic User Interface[^\n]*|"
    r"Utility Programs[^\n]*|Third-Party Software Licenses[^\n]*)",
    re.I,
)


def clean_raw_line(line: str) -> str:
    s = line.rstrip()
    if HEADER_PAT.match(s.strip()):
        return ""
    if re.match(r"^\s*\d+\s*$", s):
        return ""
    return s


def clean_block(text: str) -> str:
    lines = [clean_raw_line(l) for l in text.splitlines()]
    return "\n".join(l for l in lines if l is not None).strip()


# ---------------------------------------------------------------------------
# Keyword block parser
# ---------------------------------------------------------------------------

@dataclass
class KeywordBlock:
    name: str
    description: str = ""
    syntax: str = ""
    where_text: str = ""
    example: str = ""
    notes: List[str] = field(default_factory=list)


CAT_LINE = re.compile(r"^[ \t]*([A-Z][A-Za-z /]+Keywords)\s*$")
KW_LINE = re.compile(r"^[ \t]*([A-Z][A-Z0-9_]{2,})\s*$")


def parse_keyword_section(text: str, start_marker: str, end_marker: str) -> dict[str, list[KeywordBlock]]:
    start = text.find(start_marker)
    if start < 0:
        return {}
    end = text.find(end_marker, start + len(start_marker))
    if end < 0:
        end = len(text)
    section = text[start:end]

    categories: dict[str, list[KeywordBlock]] = {}
    current_cat = start_marker
    current_kw: Optional[KeywordBlock] = None
    mode = "desc"

    STOP_LINE = re.compile(
        r"^(ANSYS|APPENDIX |RedHawk User Manual|Figure \d)",
        re.I,
    )

    for line in section.splitlines():
        s = line.strip()
        if not s:
            continue
        if STOP_LINE.match(s) or "ANSYS, Inc." in s:
            if current_kw and mode in ("syntax", "example", "where"):
                mode = "desc"
            continue
        if CAT_LINE.match(line) and "Keywords" in s:
            if current_kw:
                categories.setdefault(current_cat, []).append(current_kw)
            current_cat = s
            current_kw = None
            mode = "desc"
            continue
        if KW_LINE.match(line) and "Keywords" not in s and s not in ("ANSYS", "INC"):
            if current_kw:
                categories.setdefault(current_cat, []).append(current_kw)
            current_kw = KeywordBlock(name=s)
            mode = "desc"
            continue
        if current_kw is None:
            continue
        low = s.lower()
        if low.startswith("syntax"):
            mode = "syntax"
            rest = s.split(":", 1)[-1].strip()
            if rest:
                current_kw.syntax += rest + "\n"
            continue
        if low.startswith("where"):
            mode = "where"
            continue
        if low.startswith("example"):
            mode = "example"
            rest = s.split(":", 1)[-1].strip()
            if rest:
                current_kw.example += rest + "\n"
            continue
        if s.startswith("NOTE:") or s.startswith("Note:"):
            current_kw.notes.append(s.split(":", 1)[-1].strip())
            continue
        if mode == "syntax":
            if len(current_kw.syntax.splitlines()) < 25:
                current_kw.syntax += line.strip() + "\n"
        elif mode == "where":
            if len(current_kw.where_text) < 4000:
                current_kw.where_text += s + " "
        elif mode == "example":
            if len(current_kw.example.splitlines()) < 40:
                current_kw.example += line.strip() + "\n"
        else:
            if not s.startswith(("•", "-", "a.", "b.", "c.", "d.", "i)", "ii)")):
                current_kw.description += s + " "

    if current_kw:
        categories.setdefault(current_cat, []).append(current_kw)
    return categories


# ---------------------------------------------------------------------------
# Translation engine (rule-based, no external API)
# ---------------------------------------------------------------------------

PHRASE_RULES: list[tuple[str, str]] = [
    (r"When set to 1", "设为 1 时"),
    (r"When set to 0", "设为 0 时"),
    (r"When turned on", "开启时"),
    (r"When turned Off", "关闭时"),
    (r"When this keyword is turned on", "开启本关键字时"),
    (r"If set to true", "设为 true 时"),
    (r"If set to 1", "设为 1 时"),
    (r"If set to 0", "设为 0 时"),
    (r"Optional;\s*default:\s*0\s*\(no", "可选；默认：0（不"),
    (r"Optional;\s*default:\s*0", "可选；默认：0"),
    (r"Optional;\s*default:\s*1", "可选；默认：1"),
    (r"Optional\.\s*Default:\s*none\.?", "可选。默认：无。"),
    (r"Optional\.\s*Default:\s*0", "可选。默认：0"),
    (r"Optional\.\s*Default:\s*1", "可选。默认：1"),
    (r"Required for", "下列情形必需："),
    (r"Required\.", "必需。"),
    (r"DMP compatible\.?", "兼容 DMP 分布式流程。"),
    (r"By default", "默认情况下"),
    (r"Note that", "请注意："),
    (r"Allows you to", "允许您"),
    (r"Allows specifying", "允许指定"),
    (r"Allows foundries to", "允许代工厂"),
    (r"Allows EM_MODE to", "允许 EM_MODE"),
    (r"Allows", "允许"),
    (r"Specifies whether", "指定是否"),
    (r"Specifies the", "指定"),
    (r"Specifies a", "指定"),
    (r"Specifies", "指定"),
    (r"Defines the", "定义"),
    (r"Defines", "定义"),
    (r"Enables", "启用"),
    (r"Disables", "禁用"),
    (r"Creates", "创建"),
    (r"Controls", "控制"),
    (r"Eliminates", "消除"),
    (r"Ignores", "忽略"),
    (r"Identifies", "标识"),
    (r"Generates", "生成"),
    (r"Imports", "导入"),
    (r"Exports", "导出"),
    (r"Performs", "执行"),
    (r"Computes", "计算"),
    (r"Converts", "转换"),
    (r"Checks", "检查"),
    (r"Validates", "校验"),
    (r"Displays", "显示"),
    (r"Removes", "移除"),
    (r"Adds", "添加"),
    (r"Deletes", "删除"),
    (r"Overwrites", "覆盖"),
    (r"power grid", "电源网格"),
    (r"IR drop", "IR 压降"),
    (r"voltage drop", "电压跌落"),
    (r"decap", "去耦电容"),
    (r"decoupling capacitors?", "去耦电容"),
    (r"toggle rate", "翻转率"),
    (r"simulation time", "仿真时间"),
    (r"extraction", "提取"),
    (r"simulation", "仿真"),
    (r"analysis", "分析"),
    (r"instances?", "实例"),
    (r"blocks?", "模块"),
    (r"cells?", "单元"),
    (r"nets?", "网络"),
    (r"pins?", "引脚"),
    (r"layers?", "层"),
    (r"vias?", "过孔"),
    (r"pads?", "焊盘"),
    (r"design", "设计"),
    (r"file", "文件"),
    (r"default", "默认"),
    (r"optional", "可选"),
]

TOKEN_ZH: dict[str, str] = {
    "ADD": "添加", "PLOC": "焊盘位置", "PAD": "焊盘", "FROM": "从", "TOP": "顶层",
    "DEF": "DEF", "BLOCK": "模块", "POWER": "电源", "IGNORE": "忽略", "CELL": "单元",
    "CELLS": "单元", "FILES": "文件", "FILE": "文件", "AUTO": "自动", "CONNECTION": "连接",
    "LAYERS": "金属层", "ASSIGNMENT": "分配", "MASTER": "主", "INSTANCE": "实例",
    "INSTANCES": "实例", "NET": "网络", "NETS": "网络", "LEF": "LEF", "LIB": "LIB",
    "TECH": "工艺", "ERROR": "错误", "WARNING": "警告", "COUNT": "计数", "COUNTS": "计数",
    "LOG": "日志", "SIMULATION": "仿真", "DYNAMIC": "动态", "STATIC": "静态",
    "EXTRACT": "提取", "EXTRACTION": "提取", "EM": "电迁移", "DVD": "DvD",
    "VCD": "VCD", "FSDB": "FSDB", "STA": "STA", "SPEF": "SPEF", "APL": "APL",
    "DECAP": "去耦电容", "FAO": "FAO", "DMP": "DMP", "ESD": "ESD", "GSC": "GSC",
    "GSR": "GSR", "ENABLE": "启用", "DISABLE": "禁用", "CHECK": "检查",
    "FLOATING": "悬空", "UNPLACED": "未放置", "UNDEFINED": "未定义", "LAYER": "层",
    "PIN": "引脚", "PINS": "引脚", "VIA": "过孔", "ROUTE": "布线", "SHORT": "短路",
    "POPUP": "弹窗", "MESSAGE": "消息", "REGION": "区域", "MACRO": "宏",
    "DEFINE": "定义", "INCLUDE": "包含", "IMPORT": "导入", "EXPORT": "导出",
    "OVERWRITE": "覆盖", "TEMPERATURE": "温度", "FREQUENCY": "频率", "TOGGLE": "翻转",
    "RATE": "率", "SCALE": "缩放", "FACTOR": "因子", "MODE": "模式",
    "PEAK": "峰值", "RMS": "RMS", "AVG": "平均", "RULE": "规则", "SET": "集",
    "METAL": "金属", "DIELECTRIC": "介质", "SUBSTRATE": "衬底", "VIAMODEL": "过孔模型",
    "UNITS": "单位", "RESISTIVE": "电阻", "CAPACITIVE": "电容", "ONLY": "仅",
    "POLYNOMIAL": "多项式", "THICKNESS": "厚度", "VARIATION": "变化",
    "HALF": "半", "NODE": "节点", "SOURCE": "源", "EQUATION": "方程",
}

KW_SEMANTIC: dict[str, str] = {
    "ADD_PLOC_FROM_DEF": "允许指定额外的 DEF 文件以定义 PLOC；RedHawk 仅读取其中 PIN 信息。",
    "ADD_PLOC_FROM_TOP_DEF": "设为 1 时，使用顶层 DEF 的 PINS 段作为电源/地焊盘位置。",
    "AUTO_PAD_CONNECTION_LAYERS": "按指定金属层与捕捉范围自动为焊盘单元生成 P/G 连接 ploc。",
    "BLOCK_POWER_ASSIGNMENT": "在早期设计中为未完成模块/区域分配功耗，用于评估电网响应。",
    "IGNORE_CELLS": "导入 DEF 时忽略列表中的单元（不写入设计数据库）。",
    "IGNORE_INSTANCES": "数据输入阶段忽略指定实例列表。",
    "WARNING_COUNTS": "限制每类 Warning 写入 stdout 与 apache.log 的最大条数。",
    "WARNING_LOG_COUNTS": "限制写入 adsRpt/redhawk.warn 的每类 Warning 最大条数。",
    "ERROR_COUNTS": "限制每类 Error 写入 stdout 的最大条数。",
    "ERROR_LOG_COUNTS": "限制写入 adsRpt/redhawk.err 的每类 Error 最大条数。",
    "DEFINE": "定义可在多次运行间复用的变量或完整文件路径。",
    "INCLUDE": "将其他 GSR 文件内容嵌入当前 GSR，等效于直接写入。",
    "DIELECTRIC": "定义介质层厚度、介电常数及高度等参数；电容/电感提取时各层均须定义。",
    "EM_PEAK_EQUATION_SOURCE_TECHFILE": "允许代工厂在 Peak EM 限值方程中内置自定义 Duty Ratio 因子。",
    "EM_RULE_SET": "在同一 tech 文件中定义多套 EM 规则集，供 EM_MODE 按角或分析模式选用。",
    "EM_TECH_FILE": "引用外部 EM 规则 tech 文件。",
    "HALF_NODE_SCALE_FACTOR": "半节点缩放因子，用于工艺尺寸缩放。",
    "METAL": "定义金属层电阻率、厚度、温度系数及 EM 限值等。",
    "VIAMODEL": "定义过孔电阻、EM 限值及 via 模型参数。",
    "SUBSTRATE": "定义衬底层厚度与电阻率。",
    "UNITS": "声明 tech 文件中使用的单位制。",
    "RESISTIVE_ONLY": "仅提取电阻网络（忽略电容）。",
    "CAPACITIVE_ONLY": "仅提取电容（忽略电阻）。",
    "POLYNOMIAL_BASED_THICKNESS_VARIATION": "基于多项式的金属厚度变化建模。",
}


def semantic_from_keyword(kw: str) -> str:
    """Build readable Chinese purpose phrase from keyword name (fallback only)."""
    if kw in KW_SEMANTIC:
        return KW_SEMANTIC[kw]
    parts = kw.split("_")
    zh_parts = [TOKEN_ZH.get(p, p) for p in parts]
    if parts[0] == "IGNORE":
        tail = "、".join(zh_parts[1:]) if len(zh_parts) > 1 else kw
        return f"在数据输入或分析流程中忽略与 {tail} 相关的对象或检查。"
    if parts[0] == "ADD":
        tail = "、".join(zh_parts[1:]) if len(zh_parts) > 1 else kw
        return f"向当前设计或 GSR 配置追加 {tail} 相关输入数据。"
    if parts[0] in ("ENABLE", "DISABLE"):
        tail = "、".join(zh_parts[1:]) if len(zh_parts) > 1 else kw
        action = "启用" if parts[0] == "ENABLE" else "禁用"
        return f"{action} {tail} 相关功能或检查。"
    if parts[0] in ("WARNING", "ERROR"):
        return f"限制或控制 {kw} 类消息在日志中的输出条数或行为。"
    tail = "、".join(zh_parts)
    return f"GSR 关键字 {kw}：用于设置与 {tail} 相关的 RedHawk 运行参数。"


def extract_meta_flags(en: str) -> str:
    flags: list[str] = []
    if re.search(r"\boptional\b", en, re.I):
        flags.append("可选")
    dm = re.search(r"default[:\s]*([^.;]{1,40})", en, re.I)
    if dm:
        flags.append(f"默认：{dm.group(1).strip()}")
    if re.search(r"\bdmp compatible\b", en, re.I):
        flags.append("兼容 DMP")
    if re.search(r"\brequired\b", en, re.I):
        flags.append("必需")
    return "；".join(flags)

CAT_ZH = {
    "GSR File Keywords": "GSR 文件关键字",
    "Input Data Keywords": "输入数据关键字",
    "Parameter Keywords": "参数关键字",
    "Custom Cell Modeling Keywords": "自定义单元建模（CMM）关键字",
    "Electromigration Keywords": "电迁移（EM）关键字",
    "Extraction and Netlisting Keywords": "提取与网表关键字",
    "Characterization Keywords": "表征关键字",
    "Timing Keywords": "时序关键字",
    "Simulation Keywords": "仿真关键字",
    "DMP Keywords": "DMP 分布式关键字",
    "FAO General Keywords": "FAO 通用关键字",
    "Grid Fixing and Optimization Keywords": "网格修复与优化关键字",
    "Decap Optimization Keywords": "去耦电容优化关键字",
    "Low Power Design Keywords": "低功耗设计关键字",
    "ESD Keywords": "ESD 关键字",
    "Name Mapping Keywords": "名称映射关键字",
    "Warning and Error Message Keywords": "警告与错误消息关键字",
    "Ignore Function Keywords": "忽略功能关键字",
    "GSR Macro Keywords": "GSR 宏关键字",
}


def translate_en(text: str, kw: str = "") -> str:
    if not text or not text.strip():
        return semantic_from_keyword(kw) if kw else ""
    t = re.sub(r"\s+", " ", text.strip())
    for pat, rep in PHRASE_RULES:
        t = re.sub(pat, rep, t, flags=re.I)
    parts = re.split(r"(?<=[.!?])\s+", t)
    t = " ".join(parts[:3])
    if len(t) > 480:
        t = t[:477] + "…"
    meta = extract_meta_flags(text)
    if cjk_ratio(t) < 0.22:
        base = semantic_from_keyword(kw)
        if meta:
            return f"{base}（{meta}）"
        return base
    if meta and meta not in t:
        t = f"{t}（{meta}）"
    return t


def translate_prose(text: str) -> str:
    """Translate longer prose blocks (intros, GUI descriptions)."""
    lines_out: list[str] = []
    for para in re.split(r"\n\s*\n", text):
        p = para.strip()
        if not p:
            continue
        if p.startswith(("Syntax", "where", "Example", "NOTE", "Figure", "•", "-")):
            lines_out.append(p)
            continue
        zh = translate_en(p)
        if cjk_ratio(zh) < 0.1:
            zh = p  # keep English if translation failed
        lines_out.append(zh)
    return "\n\n".join(lines_out)


def block_to_zh_summary(block: KeywordBlock) -> str:
    desc_zh = translate_en(block.description, block.name)
    parts = [desc_zh]
    if block.notes:
        parts.append("注意：" + translate_en(" ".join(block.notes), block.name))
    return " ".join(parts)


def format_keyword_subsection(block: KeywordBlock, use_gsr: bool = True) -> str:
    """Full keyword entry with syntax/example."""
    tag = "\\gsr" if use_gsr else "\\texttt"
    name_tex = f"{tag}{{{block.name}}}"
    lines = [
        f"\\subsubsection{{{name_tex}}}",
        f"\\paragraph*{{{block.name}}}",
        "",
        block_to_zh_summary(block),
        "",
    ]
    if block.syntax.strip():
        lines += [
            "\\textbf{语法：}",
            "\\begin{lstlisting}",
            lst_escape(block.syntax.strip()),
            "\\end{lstlisting}",
            "",
        ]
    if block.where_text.strip():
        where_opts = parse_option_lines(block.where_text)
        if where_opts:
            lines += ["\\textbf{参数说明：}", "\\begin{itemize}"]
            for opt, desc in where_opts:
                lines.append(
                    f"\\item \\texttt{{{latex_escape(opt)}}} — "
                    f"{latex_escape(translate_en(desc, block.name))}"
                )
            lines += ["\\end{itemize}", ""]
        else:
            lines += [
                "\\textbf{参数说明：}",
                latex_escape(translate_en(block.where_text.strip(), block.name)),
                "",
            ]
    if block.example.strip():
        lines += [
            "\\textbf{示例：}",
            "\\begin{lstlisting}",
            lst_escape(block.example.strip()),
            "\\end{lstlisting}",
            "",
        ]
    for note in block.notes:
        note_zh = translate_en(note, block.name)
        if note_zh in [block_to_zh_summary(block)]:
            continue
        lines += [
            "\\begin{noteBox}",
            latex_escape(note_zh),
            "\\end{noteBox}",
            "",
        ]
    return "\n".join(lines)


def parse_option_lines(text: str, strict: bool = False) -> list[tuple[str, str]]:
    """Parse 'where' blocks: lines like '-opt : desc' or '<x> : desc'."""
    opts: list[tuple[str, str]] = []
    for line in text.splitlines():
        s = line.strip()
        if not s or ":" not in s:
            continue
        if strict:
            if not (s.startswith("-") or s.startswith("<") or re.match(r"^[a-z]\.", s)):
                continue
        left, right = s.split(":", 1)
        left = left.strip()
        right = right.strip()
        if left and right and len(left) < 80 and len(right) > 3:
            opts.append((left, right))
    return opts


def format_prose_section(raw_block: str, skip_patterns: list[str] = None) -> list[str]:
    """Convert raw prose to LaTeX paragraphs + lstlisting for code-like blocks."""
    skip_patterns = skip_patterns or []
    block = clean_block(raw_block)
    parts: list[str] = []
    code_buf: list[str] = []
    prose_buf: list[str] = []

    def flush_code():
        nonlocal code_buf, parts
        if code_buf:
            parts += [
                "\\begin{lstlisting}",
                lst_escape("\n".join(code_buf)),
                "\\end{lstlisting}",
                "",
            ]
            code_buf = []

    def flush_prose():
        nonlocal prose_buf, parts
        if prose_buf:
            text = " ".join(prose_buf)
            zh = translate_prose(text)
            if cjk_ratio(zh) < 0.08:
                zh = translate_en(text[:2000])
            parts.append(zh)
            parts.append("")
            prose_buf = []

    for line in block.splitlines():
        s = line.strip()
        if not s:
            flush_prose()
            flush_code()
            continue
        if any(p in s for p in skip_patterns):
            continue
        if HEADER_PAT.match(s) or s.startswith("Figure"):
            flush_prose()
            flush_code()
            continue
        # Code-like lines: syntax examples, config samples
        is_code = (
            s.startswith(("*", "#", "GDS_", "TOP_", "VDD_", "import ", "setup "))
            or re.match(r"^[A-Z][A-Z0-9_]+\s*[{<]", s)
            or (line.startswith(" ") and re.search(r"[{}<>]", s))
            or s.startswith(("-", "OR:", "Syntax", "where"))
        )
        if is_code and not s.startswith(("Syntax", "where")):
            flush_prose()
            code_buf.append(line.rstrip())
        elif s.startswith(("Syntax", "where")):
            flush_prose()
            flush_code()
            prose_buf.append(s)
        else:
            flush_code()
            prose_buf.append(s)

    flush_prose()
    flush_code()
    return parts


def format_tcl_command_section(cmd: TclCommand) -> str:
    """Full TCL command entry with syntax, options, examples."""
    cmd_tex = latex_escape(cmd.name).replace(" ", r"\_")
    zh = CMD_ZH.get(cmd.name, "")
    lines = [
        f"\\subsection{{\\cmd{{{cmd_tex}}}}}",
        f"\\subsubsection*{{{cmd.name}}}",
        "",
    ]
    if zh:
        lines.append(zh)
        lines.append("")

    # intro from body before 'where'
    body = cmd.body.strip()
    intro = body
    where_idx = re.search(r"\bwhere\b", body, re.I)
    if where_idx:
        intro = body[:where_idx.start()].strip()
    # Remove duplicate syntax line from intro
    intro_lines = []
    for ln in intro.splitlines():
        ls = ln.strip()
        if ls.startswith(cmd.name) and ("<" in ls or "[" in ls or "?" in ls):
            continue
        if ls.startswith(("a.", "b.", "c.", "d.", "e.", "f.", "g.", "h.", "i.", "j.")):
            intro_lines.append(ln)
        elif len(ls) > 25 and not ls.startswith("The '"):
            intro_lines.append(ln)
        elif ls.startswith("The '") or ls.startswith("See "):
            intro_lines.append(ln)
    intro_text = "\n".join(intro_lines).strip()
    if intro_text:
        zh_intro = translate_prose(intro_text[:3000])
        if cjk_ratio(zh_intro) < 0.1:
            zh_intro = translate_en(intro_text[:1500], cmd.name)
        lines.append(zh_intro)
        lines.append("")

    if cmd.syntax.strip():
        lines += [
            "\\textbf{语法：}",
            "\\begin{lstlisting}",
            lst_escape(cmd.syntax.strip()),
            "\\end{lstlisting}",
            "",
        ]

    where_opts = parse_option_lines(body, strict=True)
    if where_opts:
        lines += ["\\textbf{选项说明：}", "\\begin{itemize}"]
        for opt, desc in where_opts:
            d_zh = translate_en(desc, "") if desc else ""
            if not d_zh or cjk_ratio(d_zh) < 0.15:
                d_zh = translate_en(desc, opt) if desc else ""
            lines.append(
                f"\\item \\texttt{{{latex_escape(opt)}}} — {latex_escape(d_zh)}"
            )
        lines += ["\\end{itemize}", ""]

    # Examples from body
    ex_lines = []
    in_ex = False
    for ln in body.splitlines():
        s = ln.strip()
        if s.lower().startswith("example") or s.startswith("For example"):
            in_ex = True
            continue
        if in_ex:
            if s.startswith(("a.", "b.", "c.", "d.", "e.", "f.", "g.", "h.", "i.", "j.")):
                in_ex = False
                continue
            if HEADER_PAT.match(s):
                break
            if s and (s.startswith(cmd.name) or "<" in s or s.startswith("gsr ") or s.startswith("import ")):
                ex_lines.append(ln.strip())
            elif ex_lines and not s:
                break
    if ex_lines:
        lines += [
            "\\textbf{示例：}",
            "\\begin{lstlisting}",
            lst_escape("\n".join(ex_lines[:25])),
            "\\end{lstlisting}",
            "",
        ]

    return "\n".join(lines)


def parse_config_keyword_sections(
    text: str, start_marker: str, end_markers: list[str]
) -> dict[str, list[KeywordBlock]]:
    """Parse configuration-file keyword sections (e.g. gds2rh config)."""
    start = text.find(start_marker)
    if start < 0:
        return {}
    end = len(text)
    for em in end_markers:
        pos = text.find(em, start + len(start_marker))
        if pos > 0:
            end = min(end, pos)
    section = text[start:end]
    categories: dict[str, list[KeywordBlock]] = {}
    current_cat = "Configuration Keywords"
    current_kw: Optional[KeywordBlock] = None
    mode = "desc"

    for line in section.splitlines():
        s = line.strip()
        if not s or HEADER_PAT.match(s) or s.startswith("Figure"):
            continue
        if s.endswith("Keywords") and "ANSYS" not in s:
            if current_kw:
                categories.setdefault(current_cat, []).append(current_kw)
            current_cat = s
            current_kw = None
            mode = "desc"
            continue
        # Config keyword: uppercase at line start (may be indented)
        m = re.match(r"^[ \t]*([A-Z][A-Z0-9_]{2,})\s*$", line)
        if m and s not in ("OR", "INC"):
            if current_kw:
                categories.setdefault(current_cat, []).append(current_kw)
            current_kw = KeywordBlock(name=m.group(1))
            mode = "desc"
            continue
        if current_kw is None:
            continue
        low = s.lower()
        if low.startswith("syntax"):
            mode = "syntax"
            rest = s.split(":", 1)[-1].strip()
            if rest:
                current_kw.syntax += rest + "\n"
            continue
        if low.startswith("where"):
            mode = "where"
            continue
        if low.startswith("example"):
            mode = "example"
            rest = s.split(":", 1)[-1].strip()
            if rest:
                current_kw.example += rest + "\n"
            continue
        if s.startswith("NOTE") or s.startswith("Note"):
            current_kw.notes.append(s.split(":", 1)[-1].strip())
            continue
        if mode == "syntax":
            if len(current_kw.syntax.splitlines()) < 25:
                current_kw.syntax += line.strip() + "\n"
        elif mode == "where":
            if len(current_kw.where_text) < 4000:
                current_kw.where_text += s + " "
        elif mode == "example":
            if len(current_kw.example.splitlines()) < 40:
                current_kw.example += line.strip() + "\n"
        else:
            if len(s) > 10:
                current_kw.description += s + " "

    if current_kw:
        categories.setdefault(current_cat, []).append(current_kw)
    return categories


def write_kw_table(rows: list[tuple[str, str]], cols: str = "p{0.28\\textwidth}p{0.66\\textwidth}") -> str:
    if not rows:
        return ""
    lines = [
        r"\begin{longtable}{@{}%s@{}}" % cols,
        r"\toprule",
        r"\textbf{关键字} & \textbf{用途说明} \\",
        r"\midrule",
        r"\endhead",
    ]
    for kw, zh in rows:
        lines.append(f"\\gsr{{{latex_escape(kw)}}} & {latex_escape(zh)} \\\\")
    lines += [r"\bottomrule", r"\end{longtable}", ""]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# TCL command parser (Appendix D)
# ---------------------------------------------------------------------------

@dataclass
class TclCommand:
    name: str
    syntax: str = ""
    body: str = ""


TCL_SKIP = {
    "where", "help", "then", "file", "group", "gui", "analysis",
    "resistance", "computation", "settings", "message list",
}


def _normalize_quotes(s: str) -> str:
    return s.replace("\u2018", "'").replace("\u2019", "'").replace("\u201c", '"').replace("\u201d", '"')


def parse_tcl_commands(text: str) -> list[TclCommand]:
    """Parse TCL command sections from Appendix D raw text."""
    start = text.find("help\n\n help")
    if start < 0:
        start = text.find("cell swap\n\n cell swap")
    if start < 0:
        start = text.find("TCL Command Summary")
    end = text.find("RedHawk Graphic User Interface Description")
    if end < 0:
        end = text.find("GUI Menu")
    if end < 0:
        end = len(text)
    section = text[start:end]

    known_cmds = [
        "help", "cell swap", "characterize", "condition", "config", "decap",
        "dump", "eco", "export", "fao", "generate", "get", "gsr", "history",
        "import", "license get", "marker", "mesh", "message", "movie",
        "perform", "pfs", "plot", "print", "probe", "query", "report",
        "ring", "route fix", "save", "select", "setup", "show", "window", "zoom",
    ]

    lines = section.splitlines()
    cmd_positions: list[tuple[int, str]] = []
    for i, line in enumerate(lines):
        s = line.strip()
        if s not in known_cmds:
            continue
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        if j >= len(lines):
            continue
        nxt = _normalize_quotes(lines[j].strip())
        if (
            nxt.startswith(s)
            or nxt.startswith("The '")
            or (nxt.startswith("The ") and f"'{s}'" in nxt or f"'{s} " in nxt)
        ):
            cmd_positions.append((i, s))

    cmds: list[TclCommand] = []
    for idx, (pos, name) in enumerate(cmd_positions):
        end_pos = cmd_positions[idx + 1][0] if idx + 1 < len(cmd_positions) else len(lines)
        block_lines = lines[pos:end_pos]
        cmd = TclCommand(name=name)
        for bl in block_lines[1:]:
            bs = bl.strip()
            if not bs or HEADER_PAT.match(bs):
                continue
            bs_norm = _normalize_quotes(bs)
            if not cmd.syntax and (
                bs_norm.startswith(name) or bs_norm.startswith("The '" + name)
            ):
                if "<" in bs or "[" in bs or "?" in bs:
                    cmd.syntax = bs
            cmd.body += bl.strip() + "\n"
        cmds.append(cmd)

    return cmds


CMD_ZH = {
    "help": "列出可用 TCL 命令，或显示指定命令的完整语法。",
    "cell swap": "将高功耗单元替换为低功耗单元，改善高 IR 压降区域。",
    "characterize": "运行 APL 表征，生成动态 Vdd 电流波形并表征去耦单元。",
    "condition": "设置、查看或清除 DvD 后处理分析条件（plot/print 等）。",
    "config": "配置 GUI 显示选项（色图、按键绑定、层/网络视图等）。",
    "decap": "对电源网格上的去耦电容执行添加、删除或优化。",
    "dump": "将 RedHawk 内部数据库或网络信息导出为指定格式。",
    "eco": "工程变更（ECO）：添加/删除焊盘、绑带、开关、过孔等。",
    "export": "以第三方工具可读格式导出 RedHawk 数据。",
    "fao": "焊盘阵列优化（FAO）：在网格上添加/优化 P/G 焊盘布局。",
    "generate": "生成供复查或后续流程使用的指定文件。",
    "get": "查询并获取设计对象属性（单元、网络、焊盘、开关等）。",
    "gsr": "读取、设置或转储 GSR 关键字值。",
    "history": "显示或管理当前会话的 TCL 命令历史。",
    "import": "导入 GSR、LEF、DEF、SPEF、STA、工艺、VCD/FSDB 等输入文件。",
    "license get": "选择并持有特定类型的 RedHawk 许可证。",
    "marker": "在版图中添加或删除十字准线标记。",
    "mesh": "修改电源网格（绑带、过孔、电阻等）。",
    "message": "显示 Error、Info、Warning 消息信息。",
    "movie": "设置或播放基于实例/晶体管引脚的动态波形动画。",
    "perform": "执行核心分析：功耗计算、提取、DvD、EM、热、ESD 等。",
    "pfs": "PathFinder 静电放电（ESD）检查相关功能。",
    "plot": "生成图形化波形或结果曲线文件。",
    "print": "打印基于文本的分析报告。",
    "probe": "在仿真前选择/取消选择探测节点。",
    "query": "查询设计对象并返回属性信息。",
    "report": "生成功耗、EM、IR 压降等文本报告。",
    "ring": "创建或修改模块/芯片周围的电源/地环。",
    "route fix": "在指定层上添加修复布线以改善 IR。",
    "save": "保存 RedHawk 会话或数据库快照。",
    "select": "在 GUI 中选择并高亮设计对象。",
    "setup": "设置设计数据与运行条件（design、package、pad 等）。",
    "show": "在 GUI 中显示指定结果的色阶图。",
    "window": "控制 GUI 窗口布局与视图配置。",
    "zoom": "缩放版图视图至区域、对象或全芯片。",
}


UTIL_ZH = {
    "vcdtrans": "从 VCD 文件统计各网络翻转次数，生成 toggle 文件供功耗与动态分析使用。",
    "vcdscan": "从 VCD 计算每周期峰值/平均功耗，确定最坏功耗时间窗口。",
    "fsdbtrans": "从 FSDB 文件生成各网络 toggle 文件（功能同 vcdtrans）。",
    "ircx2tech": "将 iRCX 工艺文件转换为 RedHawk .tech 工艺文件。",
    "rhtech": "从代工厂 nxtgrd/ITF 等标准工艺文件生成 RedHawk .tech 文件。",
    "gds2rh/gds2def": "从 GDSII 数据生成 DEF/LEF，用于 RedHawk 数据库集成。",
    "pt2timing": "PrimeTime TCL 接口：生成各实例的转换时间与 timing window。",
    "sim2iprof": "从仿真输出生成电流轮廓（read/write/standby 波形）。",
    "aplreader": "将电流轮廓数据转换为标准 APL 输出格式。",
    "aplcdev2pwc": "校验 cdev 数据有效性并转换为 pwcdev 格式。",
    "aplcopy": "复制并编辑 *spiprof、*cdev、*pwcdev 文件中的数据。",
    "aplchk": "对 APL 电容与 PWC 数据进行有效性检查。",
    "clampviewer": "Linux 可执行工具，预览 ESD clamp 的 I-V 曲线数据。",
}

LICENSE_OVERVIEW = [
    ("Common Public License (CPL) 1.0", "CPL", "IBM 发起的开源许可证；允许使用、修改与再分发，但须保留版权声明与许可条款；商业分发者对最终用户承担额外担保义务。"),
    ("MIT License — ZHU Kaidi (2017)", "MIT", "宽松 MIT 许可：可自由使用、修改、合并与再分发，须保留版权与许可声明；软件按“原样”提供，不附带担保。"),
    ("Boost Software License", "Boost", "允许自由使用与再分发，须保留版权声明；免责声明排除担保责任。"),
    ("Jorn Lind-Nielsen 组件", "Custom", "1996–2002 版权；按作者许可条款使用与再分发。"),
    ("GAlib — Matthew Wall", "Custom", "遗传算法库；非公有领域，按作者/MIT 条款使用。"),
    ("GIFLIB — Eric S. Raymond", "MIT-like", "GIF 图像库；MIT 风格宽松许可。"),
    ("LAPACK / BLAS", "BSD", "田纳西大学、伯克利等机构数值线性代数库；BSD 风格许可。"),
    ("libarchive — Tim Kientzle", "BSD", "归档/压缩文件读写库；BSD 风格许可。"),
    ("EFL / Evas", "BSD", "嵌入式图形库；BSD 风格许可。"),
    ("Tcl/Tk", "BSD", "脚本语言与 GUI 工具包；BSD 风格许可。"),
    ("METIS", "Apache-2.0", "图划分库；Apache License 2.0。"),
    ("Independent JPEG Group (IJG)", "IJG", "JPEG 编解码参考实现；须遵守 IJG 许可声明。"),
    ("Mozilla Public License 2.0", "MPL-2.0", "部分 GUI/库组件；修改文件须以 MPL 发布，可与专有代码文件级隔离组合。"),
    ("OpenSSL / SSLeay", "OpenSSL", "加密与 SSL/TLS 库；双重许可，须保留版权与免责。"),
    ("Mersenne Twister", "BSD", "伪随机数生成器；BSD 风格许可。"),
    ("UMFPACK / SuiteSparse", "LGPL", "稀疏矩阵求解；部分组件为 LGPL。"),
    ("Open MPI", "BSD", "MPI 实现；BSD 风格再分发条款。"),
    ("CSPARSE", "LGPL", "稀疏矩阵库；GNU LGPL。"),
    ("SuperLU", "BSD", "UC Berkeley 等机构数值库；BSD 风格许可。"),
    ("zlib", "zlib", "数据压缩库；zlib 宽松许可。"),
]
