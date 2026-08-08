# -*- coding: utf-8 -*-
"""Generate Appendix C–F LaTeX from raw text extracts (structured study translation)."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
CHAPTERS = ROOT / "chapters"

# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------

def read_raw(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8", errors="replace")


def parse_gsr_keywords(text: str) -> dict[str, list[tuple[str, str]]]:
    lines = text.splitlines()
    in_gsr = False
    cat = "GSR File Keywords"
    cats: dict[str, list[tuple[str, str]]] = {}
    current_kw: str | None = None
    desc_lines: list[str] = []
    cat_pat = re.compile(r"^[A-Z][A-Za-z /]+Keywords$")
    kw_pat = re.compile(r"^[A-Z][A-Z0-9_]+$")

    for line in lines:
        s = line.strip()
        if "GSR File Keywords" in s:
            in_gsr = True
            continue
        if not in_gsr:
            continue
        if s == "Pad, Power/Ground and I/O Definition Files":
            break
        if cat_pat.match(s) and "GSR File Keywords" not in s:
            if current_kw:
                cats.setdefault(cat, []).append((current_kw, " ".join(desc_lines)))
            cat = s
            current_kw = None
            desc_lines = []
            continue
        if kw_pat.match(s) and len(s) > 2:
            if current_kw:
                cats.setdefault(cat, []).append((current_kw, " ".join(desc_lines)))
            current_kw = s
            desc_lines = []
            continue
        if current_kw and s:
            if s.startswith(("Syntax", "where", "Example", "NOTE", "DMP compatible")):
                continue
            if kw_pat.match(s):
                continue
            if line.startswith(" ") and not s.startswith(("{", "}")):
                desc_lines.append(s)
    if current_kw:
        cats.setdefault(cat, []).append((current_kw, " ".join(desc_lines)))
    return cats


def parse_tech_keywords(text: str) -> dict[str, str]:
    start = text.find("Technology File Keywords")
    end = text.find("Global Switching Configuration")
    if start < 0 or end < 0:
        return {}
    section = text[start:end]
    kws: dict[str, str] = {}
    current: str | None = None
    desc: list[str] = []
    kw_pat = re.compile(r"^[A-Z][A-Z0-9_]+$")
    for line in section.splitlines():
        s = line.strip()
        if s in ("Technology File Keywords",) or s.startswith("NOTE:"):
            continue
        if kw_pat.match(s) and len(s) > 2:
            if current:
                kws[current] = " ".join(desc)[:500]
            current = s
            desc = []
        elif current and s and not s.startswith(("Syntax", "where", "Example")):
            if line.startswith(" "):
                desc.append(s)
    if current:
        kws[current] = " ".join(desc)[:500]
    return kws


def parse_tcl_commands(text: str) -> dict[str, dict[str, str]]:
    lines = text.splitlines()
    cmds: dict[str, dict[str, str]] = {}
    skip = {
        "where", "help", "then", "file", "group", "gui", "analysis", "resistance",
        "computation", "settings", "message list", "help get", "absolute voltage values",
    }
    i = 120
    while i < 3680:
        s = lines[i].strip()
        if re.match(r"^[a-z][a-z ]*$", s) and s and len(s) <= 25 and s not in skip:
            j = i + 1
            while j < len(lines) and not lines[j].strip():
                j += 1
            if j < len(lines):
                nxt = lines[j].strip()
                if nxt.startswith(s + " ") or nxt == s:
                    desc: list[str] = []
                    k = j + 1
                    while k < min(j + 40, len(lines)):
                        ds = lines[k].strip()
                        if not ds:
                            k += 1
                            continue
                        if re.match(r"^[a-z][a-z ]*$", ds) and len(ds) < 25:
                            nj = k + 1
                            while nj < len(lines) and not lines[nj].strip():
                                nj += 1
                            if nj < len(lines) and lines[nj].strip().startswith(ds):
                                break
                        if ds.startswith("ANSYS") or "RedHawk User Manual" in ds:
                            break
                        desc.append(ds)
                        k += 1
                    cmds[s] = {"syntax": nxt, "desc": " ".join(desc)[:600]}
        i += 1
    # Manual additions missed by heuristic
    extras = {
        "help": {
            "syntax": "help ?<TCL_command_name>?",
            "desc": "Lists available RedHawk TCL commands or shows syntax for a specific command.",
        },
        "history": {
            "syntax": "history ?<options>?",
            "desc": "Displays or manages TCL command history for the current session.",
        },
        "query": {
            "syntax": "query ?<options>?",
            "desc": "Queries design objects and returns property information.",
        },
        "report": {
            "syntax": "report ?<options>?",
            "desc": "Generates text-based analysis reports for power, EM, IR drop, and related results.",
        },
        "ring": {
            "syntax": "ring ?<options>?",
            "desc": "Creates or modifies power/ground ring structures around blocks or the chip.",
        },
        "window": {
            "syntax": "window ?<options>?",
            "desc": "Controls GUI window layout, views, and display configuration.",
        },
        "zoom": {
            "syntax": "zoom ?<options>?",
            "desc": "Zooms the layout view to a region, object, or full design extent.",
        },
    }
    cmds.update(extras)
    return cmds


def parse_utilities(text: str) -> list[dict[str, str]]:
    util_names = [
        "vcdtrans", "vcdscan", "fsdbtrans", "ircx2tech", "rhtech", "gds2rh/gds2def",
        "pt2timing", "sim2iprof", "aplreader", "aplcdev2pwc", "aplcopy", "aplchk", "clampviewer",
    ]
    utils: list[dict[str, str]] = []
    lines = text.splitlines()
    for name in util_names:
        key = name.split("/")[0]
        for i, line in enumerate(lines):
            s = line.strip()
            if s == name or s == key:
                desc: list[str] = []
                syntax = ""
                j = i + 1
                while j < min(i + 80, len(lines)):
                    ds = lines[j].strip()
                    if ds == name or (ds in util_names and ds != name):
                        break
                    if ds.startswith("ANSYS") or "RedHawk User Manual" in ds:
                        break
                    if not syntax and (key in ds or ds.startswith(key)):
                        if "<" in ds or "-i" in ds or "-o" in ds:
                            syntax = ds
                    if ds and not ds.startswith("where") and len(ds) > 20:
                        desc.append(ds)
                    j += 1
                utils.append({
                    "name": name,
                    "syntax": syntax[:200],
                    "desc": " ".join(desc[:6])[:500],
                })
                break
    return utils


def parse_license_blocks(text: str) -> list[dict[str, str]]:
    """Split Appendix F into license blocks by blank-line separators."""
    # Normalize: find blocks starting after intro
    intro_end = text.find("THE ACCOMPANYING PROGRAM IS PROVIDED")
    body = text[intro_end:] if intro_end > 0 else text
    chunks = re.split(r"\n\n\n              ", body)
    blocks: list[dict[str, str]] = []
    for chunk in chunks:
        chunk = chunk.strip()
        if len(chunk) < 80:
            continue
        lines = chunk.splitlines()
        title = lines[0].strip()[:120]
        blocks.append({"title": title, "body": chunk})
    return blocks


# ---------------------------------------------------------------------------
# Chinese summarization (learning-oriented; not word-for-word for 600+ entries)
# ---------------------------------------------------------------------------

GLOSSARY = [
    (r"\bWhen set to 1\b", "设为 1 时"),
    (r"\bWhen set to 0\b", "设为 0 时"),
    (r"\bWhen set\b", "启用时"),
    (r"\bWhen turned on\b", "开启时"),
    (r"\bWhen turned Off\b", "关闭时"),
    (r"\bOptional\b", "可选"),
    (r"\bDefault:\s*", "默认："),
    (r"\bDMP compatible\b", "兼容 DMP 分布式流程"),
    (r"\bSpecifies\b", "指定"),
    (r"\bAllows\b", "允许"),
    (r"\bDefines\b", "定义"),
    (r"\bEnables\b", "启用"),
    (r"\bDisables\b", "禁用"),
    (r"\bIgnores\b", "忽略"),
    (r"\bLEF\b", "LEF"),
    (r"\bDEF\b", "DEF"),
    (r"\bSPEF\b", "SPEF"),
    (r"\bSTA\b", "STA"),
    (r"\bVCD\b", "VCD"),
    (r"\bFSDB\b", "FSDB"),
    (r"\bAPL\b", "APL"),
    (r"\bGSC\b", "GSC"),
    (r"\bGSR\b", "GSR"),
    (r"\bEM\b", "EM"),
    (r"\bDvD\b", "DvD"),
    (r"\bIR drop\b", "IR 压降"),
    (r"\bvoltage drop\b", "电压跌落"),
    (r"\bpower grid\b", "电源网格"),
    (r"\bdecap\b", "去耦电容"),
    (r"\btoggle rate\b", "翻转率"),
    (r"\binstance\b", "实例"),
    (r"\bnet\b", "网络"),
    (r"\bcell\b", "单元"),
    (r"\blayer\b", "层"),
    (r"\bpin\b", "引脚"),
    (r"\bpad\b", "焊盘/PAD"),
    (r"\bextraction\b", "提取"),
    (r"\bsimulation\b", "仿真"),
    (r"\banalysis\b", "分析"),
]

CAT_ZH = {
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

CMD_ZH = {
    "help": "列出可用 TCL 命令或显示指定命令的完整语法。",
    "cell swap": "将高功耗单元替换为低功耗单元，以改善高 IR 压降区域。",
    "characterize": "运行 APL 表征，生成动态 Vdd 电流波形并表征去耦单元。",
    "condition": "设置、查看或清除 DvD 后处理分析条件（用于 plot/print 等）。",
    "config": "配置 GUI 显示与分析选项。",
    "decap": "对电源网格上的去耦电容执行添加、删除或优化操作。",
    "dump": "将 RedHawk 内部数据库或网络信息导出为指定格式文件。",
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
    "select": "在 GUI 中选择并高亮设计对象。",
    "setup": "设置设计数据与运行条件（design、package、pad 等）。",
    "show": "在 GUI 中显示指定结果的色阶图。",
    "window": "控制 GUI 窗口布局与视图配置。",
    "zoom": "缩放版图视图至区域、对象或全芯片。",
}

UTIL_ZH = {
    "vcdtrans": "从 VCD 文件生成各网络的翻转（toggle）统计文件，供功耗与动态分析使用。",
    "vcdscan": "从 VCD 计算每周期峰值/平均功耗，确定最坏功耗时间窗口。",
    "fsdbtrans": "从 FSDB 文件生成各网络的 toggle 文件（功能同 vcdtrans）。",
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

TECH_ZH = {
    "DIELECTRIC": "定义介质层参数（厚度、介电常数、高度等），电容/电感提取时必需。",
    "EM_PEAK_EQUATION_SOURCE_TECHFILE": "允许代工厂在 Peak EM 限值方程中内置自定义 Duty Ratio 因子。",
    "EM_RULE_SET": "在同一 tech 文件中定义多套 EM 规则集，供 EM_MODE 按角或分析模式选用。",
    "EM_TECH_FILE": "引用外部 EM 规则 tech 文件。",
    "HALF_NODE_SCALE_FACTOR": "半节点缩放因子，用于工艺尺寸缩放。",
    "METAL": "定义金属层电阻率、厚度、EM 限值等参数。",
    "RESISTIVE_ONLY": "仅提取电阻网络（忽略电容）。",
    "CAPACITIVE_ONLY": "仅提取电容（忽略电阻）。",
    "POLYNOMIAL_BASED_THICKNESS_VARIATION": "基于多项式的金属厚度变化建模。",
    "SUBSTRATE": "定义衬底层厚度与电阻率。",
    "UNITS": "声明 tech 文件中使用的单位制。",
    "VIAMODEL": "定义过孔电阻、EM 限值及 via 模型参数。",
}

LICENSE_OVERVIEW = [
    ("Common Public License (CPL) 1.0", "IBM 发起的开源许可证，允许使用、修改与再分发，但需保留版权声明与许可条款；商业分发者有额外担保义务。", "CPL"),
    ("MIT License — ZHU Kaidi (2017)", "宽松 MIT 许可：可自由使用、修改、合并与再分发，需保留版权与许可声明；软件按“原样”提供。", "MIT"),
    ("Boost Software License / 类似宽松许可", "允许自由使用与再分发，需保留版权声明；免责声明排除担保责任。", "Boost-like"),
    ("Jorn Lind-Nielsen 组件", "1996–2002 版权；按作者许可条款使用与再分发。", "Custom"),
    ("GAlib — Matthew Wall / MIT", "遗传算法库；非公有领域，按作者/MI T 条款使用；作者与 MIT 不承担使用责任。", "Custom"),
    ("GIFLIB — Eric S. Raymond", "GIF 图像库；MIT 风格宽松许可。", "MIT-like"),
    ("LAPACK / BLAS / 数值库", "田纳西大学、伯克利等机构的数值线性代数库；BSD 风格许可，需保留版权声明。", "BSD"),
    ("libarchive — Tim Kientzle", "归档/压缩文件读写库；BSD 风格许可。", "BSD"),
    ("EFL / Evas — Carsten Haitzler 等", "嵌入式图形库；BSD 风格许可。", "BSD"),
    ("Tcl/Tk — AT&T / Lucent / Bellcore", "脚本语言与 GUI 工具包；BSD 风格许可，需保留版权声明。", "BSD"),
    ("METIS — University of Minnesota", "图划分库；Apache License 2.0。", "Apache-2.0"),
    ("Independent JPEG Group (IJG)", "JPEG 编解码参考实现；宽松使用条款，需遵守 IJG 许可声明。", "IJG"),
    ("Mozilla Public License 2.0 (MPL-2.0)", "用于部分 GUI/库组件；修改文件需以 MPL 发布，可与专有代码以文件级隔离方式组合。", "MPL-2.0"),
    ("OpenSSL / SSLeay", "加密与 SSL/TLS 库；OpenSSL 与 SSLeay 双重许可条款，需保留版权声明与免责。", "OpenSSL"),
    ("Mersenne Twister — Makoto Matsumoto", "伪随机数生成器；BSD 风格许可。", "BSD"),
    ("UMFPACK / SuiteSparse — Timothy Davis", "稀疏矩阵求解；部分组件为 LGPL，需遵守 GNU 库许可要求。", "LGPL"),
    ("Open MPI 等 HPC 组件", "多机构版权的 MPI 实现；BSD 风格再分发条款。", "BSD"),
    ("CSPARSE — Timothy Davis", "稀疏矩阵库；GNU LGPL 许可。", "LGPL"),
    ("SuperLU / 其他科学计算库", "UC Berkeley 等机构的数值库；BSD 风格许可。", "BSD"),
    ("zlib / compression", "数据压缩库；zlib 宽松许可。", "zlib"),
]


TOKEN_ZH = {
    "IMPORT": "导入", "IGNORE": "忽略", "ENABLE": "启用", "DISABLE": "禁用",
    "FILES": "文件", "FILE": "文件", "NET": "网络", "NETS": "网络",
    "LEF": "LEF", "DEF": "DEF", "SPEF": "SPEF", "STA": "STA", "VCD": "VCD",
    "GSC": "GSC", "GSR": "GSR", "APL": "APL", "EM": "电迁移", "DVD": "DvD",
    "PAD": "焊盘", "PLOC": "焊盘位置", "POWER": "电源", "GND": "地",
    "VDD": "VDD", "BLOCK": "模块", "CELL": "单元", "LAYER": "层",
    "SCALE": "缩放", "FACTOR": "因子", "TEMPERATURE": "温度",
    "SIMULATION": "仿真", "EXTRACTION": "提取", "ANALYSIS": "分析",
    "TOGGLE": "翻转", "RATE": "率", "FREQUENCY": "频率",
    "DECAP": "去耦电容", "BPA": "模块功耗分配", "DMP": "DMP",
    "FAST": "快速", "READ": "读取", "WRITE": "写入", "MERGE": "合并",
    "OVERRIDE": "覆盖", "CHECK": "检查", "WARNING": "警告", "ERROR": "错误",
    "REGION": "区域", "MACRO": "宏", "HOOK": "关联", "INTERNAL": "内部",
    "EXTERNAL": "外部", "PIN": "引脚", "VIA": "过孔", "WIRE": "导线",
}


def keyword_name_hint(kw: str) -> str:
    parts = [p for p in kw.split("_") if p]
    zh_parts = [TOKEN_ZH.get(p, p) for p in parts]
    return "控制/配置：" + "·".join(zh_parts)


def en_to_zh_brief(desc: str, kw: str = "") -> str:
    if not desc:
        return f"{keyword_name_hint(kw)}；详见原书语法与示例。"
    d = re.sub(r"\s+", " ", desc).strip()
    parts = re.split(r"(?<=[.!?])\s+", d)
    d = " ".join(parts[:2])[:320]
    zh = d
    for pat, rep in GLOSSARY:
        zh = re.sub(pat, rep, zh, flags=re.I)
    cjk = sum(1 for c in zh if "\u4e00" <= c <= "\u9fff")
    if cjk < 12:
        hint = keyword_name_hint(kw)
        # Keep a short bilingual tail for learning
        tail = re.sub(r"[^\x00-\x7F]+", "", zh)
        tail = re.sub(r"\s+", " ", tail).strip()[:100]
        if tail:
            return f"{hint}。{tail}"
        return hint
    return zh[:220]


def dedupe_keywords(rows: list[tuple[str, str]]) -> list[tuple[str, str]]:
    best: dict[str, str] = {}
    order: list[str] = []
    for kw, desc in rows:
        if kw not in best:
            order.append(kw)
            best[kw] = desc
        elif len(desc) > len(best[kw]):
            best[kw] = desc
    return [(k, best[k]) for k in order]


def fix_tex_escapes(content: str) -> str:
    """Repair \\t swallowed as tab in non-raw Python string literals."""
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
# Generators
# ---------------------------------------------------------------------------

def gen_appendix_c() -> str:
    raw = read_raw("raw_C_file_defs.txt")
    gsr_cats = parse_gsr_keywords(raw)
    tech_kws = parse_tech_keywords(raw)

    parts = [
        r"% 附录 C — 文件定义（结构化学习译本）",
        r"\biappendix{文件定义}{File Definitions}",
        r"\label{chap:files}",
        "",
        r"\section{引言}",
        r"\subsection*{Introduction}",
        "",
        "本附录描述 RedHawk 支持的内部输入/输出文件格式与内容。",
        "RedHawk 输入文件可在文件名前加设计名前缀；所有此类文件中，行首 \texttt{\\#} 视为注释。",
        "",
        r"\begin{noteBox}",
        "RedHawk 可直接读取 gzip 压缩格式（\texttt{*.gz}）的 LEF、DEF、STA、SPEF、VCD、FSDB 与 GDS 文件。",
        r"\end{noteBox}",
        "",
        r"\section{RedHawk 输入文件}",
        r"\subsection*{RedHawk Input Files}",
        "",
        r"\begin{enumerate}",
        r"\item 工艺文件（\texttt{*.tech}）",
        r"\item 全局开关配置 GSC 文件（\texttt{*.gsc}）",
        r"\item 全局系统需求 GSR 文件（\texttt{*.gsr}）",
        r"\item 焊盘实例/单元/位置文件（\texttt{*.pad}、\texttt{*.pcell}、\texttt{*.ploc}）",
        r"\item 库工艺文件（LEF 等，路径在 GSR 中引用）",
        r"\item 设计网表文件（DEF 等）",
        r"\item Synopsys 库文件（\texttt{*.lib}）",
        r"\end{enumerate}",
        "",
        r"\section{RedHawk 输出文件}",
        r"\subsection*{RedHawk Output Files}",
        "",
        "分析各阶段均会生成结果文件与图形显示。详细报告说明见第~6~章及各主题章节。",
        "",
        r"\section{关键字语法约定}",
        r"\subsection*{Keyword Syntax Conventions}",
        "",
        "RedHawk 命令、选项与关键字语法约定如下：",
        r"\begin{itemize}",
        r"\item \texttt{<x>} — 需指定的变量或取值",
        r"\item \texttt{[a|b|c]} — 必须选择 a、b、c 之一",
        r"\item \texttt{?x?} — 可选参数 x",
        r"\item \texttt{abcd} — 参数 a、b、c、d 均须指定",
        r"\item \texttt{<x> ...} — 可追加多个与 x 同类型的元素",
        r"\item \texttt{\{ \{a b c ...\} \{j k l ...\} ...\}} — 可追加多组相似元素集合",
        r"\item \texttt{+-*/} — 加减乘除算术运算符",
        r"\end{itemize}",
        "",
        r"\section{Apache 工艺文件（\texttt{*.tech}）}",
        r"\subsection*{Apache Technology File (*.tech)}",
        "",
        "RedHawk 工艺文件为每个 IC 工艺提供金属层、过孔、介质、衬底及 bump 等参数。",
        "需为每个工艺节点单独准备一份 \texttt{.tech} 文件。主要内容包括：",
        r"\begin{itemize}",
        r"\item 各金属层名称（与 LEF 一致）、厚度、电阻率、温度系数与 EM 限值",
        r"\item 过孔名称、单孔电阻与 via EM 限值",
        r"\item wire-bond 或 flip-chip bump 的 R/L/C",
        r"\item 介质层厚度、高度与介电常数",
        r"\item 衬底层厚度与电阻率",
        r"\end{itemize}",
        "",
        r"\subsection{单位与前缀}",
        r"\subsubsection*{Unit Prefix Conventions}",
        "",
        "单位区分大小写。支持 t/g/M/k/m/u/n/p/f 等前缀（如 \texttt{1.3p = 1.3e-12}，数字与单位间无空格）。",
        "长度换算：\texttt{1 mil = 0.001 inch = 2.54e-5 m}；\texttt{1 inch = 2.54e-2 m}；\texttt{1 micron = 1e-6 m}。",
        "",
        r"\subsection{工艺文件加解密}",
        r"\subsubsection*{Encrypting and Decrypting a Tech File}",
        "",
        r"\textbf{全文件加密：}使用 \texttt{bin} 目录下 \texttt{techEncrypt}/\texttt{techDecrypt}。",
        r"\begin{lstlisting}",
        r"techEncrypt <tech_filename>    # 生成 <tech_filename>.enc.tech",
        r"techDecrypt -i <encrypted_tech_file> -o <tech_file>",
        r"\end{lstlisting}",
        "",
        r"\textbf{部分加密：}在 \texttt{\#ENCRYPT_START} 与 \texttt{\#ENCRYPT_END} 注释行之间自动加密敏感 RC/高度/介电常数段。",
        "",
        r"\subsection{工艺文件关键字}",
        r"\subsubsection*{Technology File Keywords}",
        "",
        r"\begin{noteBox}",
        "关键字与选项名不区分大小写。",
        r"\end{noteBox}",
    ]

    tech_rows = []
    for kw, desc in tech_kws.items():
        zh = TECH_ZH.get(kw, en_to_zh_brief(desc, kw))
        tech_rows.append((kw, zh))
    if not tech_rows:
        tech_rows = list(TECH_ZH.items())
    parts.append(write_kw_table(tech_rows))

    parts += [
        r"\section{全局开关配置 GSC 文件}",
        r"\subsection*{Global Switching Configuration (GSC) File}",
        "",
        "GSC 文件定义设计中实例/模块的开关状态，用于无向量（vectorless）或配合 SIM2IPROF/AVM/APLMMX 的多状态功耗建模。",
        "在 GSR 中通过 \gsr{GSC_FILES} 指定路径；亦可用 TCL \cmd{import gsc <file>} 动态读入。",
        "",
        r"\textbf{语法（GSR）：}",
        r"\begin{lstlisting}",
        r"GSC_FILES <gsc_FilePathName>",
        r"\end{lstlisting}",
        "",
        r"\textbf{语法（GSC 文件）：}",
        r"\begin{lstlisting}",
        r"[<blockName>|<instanceName>] ?<domain_name>?",
        r"[UNDECIDED|TOGGLE|HIGH|LOW|POWERUP|POWERDOWN|STANDBY|ENABLE|DISABLE|OFF|<custom_state>]",
        r"\end{lstlisting}",
        "",
        r"\begin{itemize}",
        r"\item 若 GSC 仅含单周期状态，RedHawk 在整个仿真时间内重复该状态",
        r"\item 若含多状态序列，触发多周期 GSC 流程",
        r"\item 多 GSC 文件中重复实例：后读文件覆盖先读值（警告 GSC-028）",
        r"\item 默认启用 \gsr{DYNAMIC_GSC_CHECK}，检查 GSC 中未覆盖的实例",
        r"\item 大文件可在首行加注释 \texttt{\#EXACT\_INSTANCE\_NAME\_MATCH} 加速解析",
        r"\end{itemize}",
        "",
        r"\section{全局系统需求 GSR 文件}",
        r"\subsection*{Global System Requirements File (*.gsr)}",
        "",
        "GSR 是 RedHawk 的\textbf{主配置文件}，汇总输入设计文件路径、分析类型、仿真参数与流程控制关键字。",
        "可用 TCL \cmd{gsr get}/\cmd{gsr set} 查询或修改。关键字名不区分大小写。",
        "",
        f"本译本按原书分类列出全部 {sum(len(v) for v in gsr_cats.values())} 个 GSR 关键字（共 {len(gsr_cats)} 类），",
        "每类以长表给出中文用途说明；极冷门项保留关键字名并附一句摘要。",
        "",
    ]

    for cat_en, kws in gsr_cats.items():
        cat_zh = CAT_ZH.get(cat_en, cat_en)
        parts += [
            f"\\subsection{{{cat_zh}}}",
            f"\\subsubsection*{{{cat_en}}}",
            "",
            f"本类共 {len(kws)} 个关键字，控制 {cat_zh} 相关 RedHawk 行为。",
            "",
        ]
        rows = [(kw, en_to_zh_brief(desc, kw)) for kw, desc in dedupe_keywords(kws)]
        parts.append(write_kw_table(rows))

    parts += [
        r"\section{焊盘、电源/地与 I/O 定义文件}",
        r"\subsection*{Pad, Power/Ground and I/O Definition Files}",
        "",
        r"\subsection{统一焊盘输入格式}",
        r"\subsubsection*{Unified Pad Input File Format}",
        "",
        "统一格式可在单文件中定义焊盘实例、单元类型、位置与 P/G 连接，替代分散的 \texttt{.pad}/\texttt{.pcell}/\texttt{.ploc}。",
        "",
        r"\subsection{分散焊盘文件}",
        r"\subsubsection*{Individual Pad File Specification}",
        r"\begin{itemize}",
        r"\item \texttt{*.pcell} — 焊盘单元名列表",
        r"\item \texttt{*.pad} — 焊盘实例名列表",
        r"\item \texttt{*.ploc} — 焊盘物理位置与层信息",
        r"\end{itemize}",
        "",
        r"\section{库工艺与设计网表文件}",
        r"\subsection*{Library Technology and Design Netlist Files}",
        "",
        r"\begin{itemize}",
        r"\item \textbf{LEF/库工艺：}在 GSR 的 \gsr{LEF_FILES}/\gsr{TECH_LEFS} 中指定；含 MACRO、PIN、OBS 等",
        r"\item \textbf{DEF 网表：}在 \gsr{DEF_FILES} 中指定；含布局布线、SPECIALNETS、PINS 等",
        r"\item \textbf{Synopsys LIB：}在 \gsr{LIB_FILES} 中指定；功耗/时序/漏电模型",
        r"\item \textbf{STA 时序：}紧凑格式或传统格式；见下文 STA 文件语法",
        r"\item \textbf{自定义 LIB 语法：}支持扩展功耗/电流模型字段",
        r"\end{itemize}",
        "",
        r"\section{时序数据文件}",
        r"\subsection*{Timing Data File}",
        "",
        r"\subsection{STA 紧凑格式}",
        r"\subsubsection*{STA Compact Format Timing File}",
        "",
        "推荐格式：每行包含实例、引脚、到达/转换时间等字段，便于大规模设计解析。",
        "",
        r"\subsection{传统 STA 格式}",
        r"\subsubsection*{Legacy Format Timing File}",
        "",
        "旧版 RedHawk 兼容格式；新设计建议使用紧凑格式。",
        "",
        r"\section{结果文件}",
        r"\subsection*{Result Files}",
        "",
        "RedHawk 在 \texttt{adsRpt}、\texttt{adsPower} 等目录下生成功耗摘要、IR/DvD 结果、EM 报告、电流文件等。",
        "详见第~6~章「报告」。",
        "",
    ]
    return "\n".join(parts)


def gen_appendix_d() -> str:
    raw = read_raw("raw_D_cmd_gui.txt")
    cmds = parse_tcl_commands(raw)

    parts = [
        r"% 附录 D — 命令与 GUI 参考",
        r"\biappendix{命令与 GUI 参考}{Command and GUI Reference}",
        r"\label{chap:cmd}",
        "",
        r"\section{引言}",
        r"\subsection*{Introduction}",
        "",
        "本附录描述 RedHawk 的两种用户界面：TCL 命令行与图形用户界面（GUI）。",
        "",
        r"\section{启动 RedHawk}",
        r"\subsection*{Invoking RedHawk}",
        "",
        "在 UNIX 工作目录下执行：",
        r"\begin{lstlisting}",
        r"redhawk [-b <cmnd_file>] [-c <cmnd_file>] [-f <cmnd_file>]",
        r"        [-i ?<cmnd_file>?] [-h] [-tclsh] [-lmhold <cmdfile>]",
        r"        [-lmwait <wait_sec>] [-iconify]",
        r"        [-style [CDE|Motif|Plastique|Windows]]",
        r"        [-stack [<stacksize_MB>|unlimited]]",
        r"        [clampviewer <IV_FileName> [<IV_Name(s)>] [<options>]]",
        r"\end{lstlisting}",
        r"\begin{itemize}",
        r"\item \texttt{-b} — 批处理运行 TCL 脚本，不显示 GUI，结束后退出",
        r"\item \texttt{-c} — 预解析 TCL 脚本并报告语法警告/错误，不执行",
        r"\item \texttt{-f} — 运行 TCL 脚本并显示 GUI",
        r"\item \texttt{-i} — 交互 TCL 命令行，无 GUI",
        r"\item \texttt{-tclsh} — 完整 TCL shell；检出许可证后可用 \cmd{redhawk} 启动",
        r"\item \texttt{-lmhold} — 退出后保持许可证占用",
        r"\item \texttt{-lmwait} — 无可用许可证时等待（可指定秒数）",
        r"\item \texttt{-iconify} — 启动时最小化 GUI（仍需 DISPLAY）",
        r"\item \texttt{-stack} — 指定栈大小（MB）或 unlimited",
        r"\end{itemize}",
        "",
        r"\section{终止进程}",
        r"\subsection*{Terminating Processes}",
        "",
        r"\texttt{Ctrl+C} 可终止当前操作及多数子进程；在 X-term 中可能直接杀死主进程。",
        r"\cmd{setup design} 与提取等少数流程在 GUI 中不响应 Ctrl+C。",
        "",
        r"\section{TCL 语法约定}",
        r"\subsection*{TCL Syntax Conventions}",
        "",
        "语法约定同附录 C「关键字语法约定」。",
        "",
        r"\section{TCL 命令概要}",
        r"\subsection*{TCL Command Summary}",
        "",
        "TCL 脚本可手动编写，也可通过 GUI Playback 录制。使用 \cmd{help <命令名>} 查看完整语法。",
        "GUI 中支持 TAB 自动补全。",
        "",
        f"下表列出全部 {len(cmds)} 个一级 TCL 命令及中文说明；各命令子选项详见原书或在线 help。",
        "",
        r"\begin{longtable}{@{}p{0.22\textwidth}p{0.72\textwidth}@{}}",
        r"\toprule",
        r"\textbf{命令} & \textbf{用途说明} \\",
        r"\midrule",
        r"\endhead",
    ]
    for name in sorted(cmds.keys()):
        zh = CMD_ZH.get(name, en_to_zh_brief(cmds[name]["desc"], name))
        cmd_tex = latex_escape(name).replace(" ", r"\_")
        parts.append(f"\\cmd{{{cmd_tex}}} & {latex_escape(zh)} \\\\")
    parts += [
        r"\bottomrule",
        r"\end{longtable}",
        "",
        r"\section{代表性 TCL 命令详解}",
        r"\subsection*{Representative TCL Commands}",
        "",
    ]

    perform_sub = [
        ("analysis", "执行指定类型的分析（静态/动态 IR、EM 等）"),
        ("extraction", "执行 R/C 网络提取"),
        ("pwrcalc", "功耗计算"),
        ("powermodel", "生成功耗模型"),
        ("res_calc", "电阻/网格电阻计算"),
        ("gridcheck", "电源网格 DRC/连通性检查"),
        ("clampcheck", "ESD clamp 检查"),
        ("thermalmodel", "热分析建模"),
        ("jitter", "抖动分析"),
        ("min_res_path", "最小电阻路径分析"),
    ]
    parts += [
        r"\subsection{\cmd{perform} 子命令}",
        r"\subsubsection*{perform Subcommands}",
        "",
        r"\begin{longtable}{@{}p{0.26\textwidth}p{0.68\textwidth}@{}}",
        r"\toprule",
        r"\textbf{子命令} & \textbf{说明} \\",
        r"\midrule",
        r"\endhead",
    ]
    for sub, zh in perform_sub:
        parts.append(f"\\cmd{{perform {sub}}} & {latex_escape(zh)} \\\\")
    parts += [r"\bottomrule", r"\end{longtable}", ""]

    detail_cmds = [
        "setup", "perform", "gsr", "import", "report", "show", "eco", "mesh", "fao", "pfs",
        "plot", "print", "probe", "query", "characterize", "decap", "condition", "config",
    ]
    for name in detail_cmds:
        if name not in cmds:
            continue
        info = cmds[name]
        cmd_tex = latex_escape(name).replace(" ", r"\_")
        zh = CMD_ZH.get(name, "")
        parts += [
            f"\\subsection{{\\cmd{{{cmd_tex}}}}}",
            f"\\subsubsection*{{{name}}}",
            "",
            zh,
            "",
            r"\textbf{语法：}",
            r"\begin{lstlisting}",
            latex_escape(info["syntax"]),
            r"\end{lstlisting}",
            "",
        ]

    parts += [
        r"\section{RedHawk 图形用户界面}",
        r"\subsection*{RedHawk Graphic User Interface Description}",
        "",
        "GUI 主要区域：菜单栏、主显示区、控制按钮、视图配置、结果查看、查询、TCL 命令行与日志区。",
        "详见原书 Figure D-3 及第~3~章 GUI 概述。",
        "",
        r"\subsection{鼠标操作}",
        r"\subsubsection*{Mouse Function}",
        r"\begin{itemize}",
        r"\item \textbf{左键：}选择/高亮对象并在日志区显示属性（需开启对应层显示）",
        r"\item \textbf{右键：}上下文菜单与快捷操作",
        r"\item 连续点击同一点可在更低金属层间循环选择",
        r"\item 动态分析后点击导线可显示网络、层、宽长、坐标及电压/电流",
        r"\end{itemize}",
        "",
        r"\subsection{菜单与对话框概要}",
        r"\subsubsection*{Menus and Dialogs Overview}",
        "",
        r"\begin{itemize}",
        r"\item \textbf{File} — 打开/保存设计、导入导出、退出",
        r"\item \textbf{Setup} — Setup Design、Package、Pad、GSR 编辑",
        r"\item \textbf{Analysis} — 提取、功耗计算、静态/动态 IR、EM、热、ESD",
        r"\item \textbf{Results} — 色阶图、报告、Log Viewer、Explorer",
        r"\item \textbf{Dynamic} — VCD/FSDB 动态分析、Movie",
        r"\item \textbf{Tools} — Grid Fix、Decap、FAO、DMP 等",
        r"\item \textbf{View/Query} — 层显示、缩放、对象查询、连通性",
        r"\item \textbf{Playback} — TCL 脚本录制与回放",
        r"\end{itemize}",
        "",
        r"\begin{seeAlsoBox}",
        "完整 GUI 控件说明（Layer 对话框、Colormap 配置、Probe 设置等）见原书附录 D 后半部分及第~3~章。",
        r"\end{seeAlsoBox}",
        "",
    ]
    return "\n".join(parts)


def gen_appendix_e() -> str:
    raw = read_raw("raw_E_utilities.txt")
    utils = parse_utilities(raw)

    parts = [
        r"% 附录 E — 实用程序",
        r"\biappendix{实用程序}{Utility Programs}",
        r"\label{chap:util}",
        "",
        r"\section{引言}",
        r"\subsection*{Introduction}",
        "",
        "本附录介绍 RedHawk 安装目录 \texttt{bin} 下的关键命令行实用程序，用于 VCD/FSDB 处理、",
        "工艺转换、GDS 导入、APL 数据校验与 ESD 预览等前处理/后处理任务。",
        "",
        r"\begin{itemize}",
    ]
    for u in utils:
        name = u["name"]
        zh = UTIL_ZH.get(name, u["desc"][:120])
        parts.append(f"\\item \\textbf{{{latex_escape(name)}}} — {latex_escape(zh)}")
    parts += [r"\end{itemize}", ""]

    util_options = {
        "vcdtrans": [("-o", "输出 toggle 文件名"), ("-c", "大小写不敏感"), ("-s/-e", "起止时间（ps 或秒）"), ("-w", "逻辑/物理模块名映射")],
        "vcdscan": [("-f", "帧长/周期（ps）"), ("-o", "输出功耗文件"), ("-d", "adsPower 输入目录"), ("-tt", "使用 VCD 真实 timing")],
        "fsdbtrans": [("-o", "输出 toggle 文件"), ("-s/-e", "扫描时间范围"), ("-w", "模块名映射")],
        "ircx2tech": [("-i", "输入 iRCX"), ("-o", "输出 tech"), ("-v", "RC 角 min/typ/max"), ("-m", "层映射"), ("-pe", "EM 规则文件")],
        "rhtech": [("-i", "nxtgrd/ITF 输入"), ("-f/-n", "代工厂/节点（必填注释）"), ("-o", "输出 tech"), ("-m", "层映射"), ("-e/-pe", "EM 限值文件")],
        "gds2rh/gds2def": [("-m", "存储器详细视图"), ("gds 配置文件", "层映射与单元定义")],
        "pt2timing": [("PrimeTime TCL", "生成 slew 与 timing window")],
        "sim2iprof": [("config", "仿真输出转电流轮廓"), ("read/write/standby", "基于 lib 公式提取波形")],
        "aplreader": [("输入电流轮廓", "转标准 APL 输出")],
        "aplcdev2pwc": [("校验 cdev", "并转 pwcdev")],
        "aplcopy": [("*spiprof/*cdev", "复制编辑 APL 数据")],
        "aplchk": [("cap/pwc", "APL 数据有效性验证")],
        "clampviewer": [("IV 文件", "预览 ESD clamp I-V 曲线")],
    }
    for u in utils:
        name = u["name"]
        zh = UTIL_ZH.get(name, "")
        parts += [
            f"\\section{{{latex_escape(name)}}}",
            f"\\subsection*{{{name}}}",
            "",
            zh,
            "",
        ]
        if u["syntax"]:
            parts += [
                r"\textbf{语法：}",
                r"\begin{lstlisting}",
                latex_escape(u["syntax"]),
                r"\end{lstlisting}",
                "",
            ]
        opts = util_options.get(name, [])
        if opts:
            parts += [
                r"\textbf{主要选项：}",
                r"\begin{itemize}",
            ]
            for opt, desc in opts:
                parts.append(f"\\item \\texttt{{{latex_escape(opt)}}} — {latex_escape(desc)}")
            parts += [r"\end{itemize}", ""]
        parts.append("")

    parts += [
        r"\section{通用注意事项}",
        r"\subsection*{General Notes}",
        "",
        r"\begin{noteBox}",
        r"vcdtrans/vcdscan/fsdbtrans 的 \texttt{-s}/\texttt{-e} 时间值若小于 0.1，RedHawk 假定单位为秒；否则为皮秒（ps）。",
        r"\end{noteBox}",
        "",
        r"\begin{tipBox}",
        "VCD 动态 IR 流程：先用 vcdscan 获取峰值功耗周期 \texttt{<FROM>,<TO>}，再在 GUI Dynamic 菜单中启动 VCD-based Dynamic IR-drop Analysis。",
        r"\end{tipBox}",
        "",
    ]
    return "\n".join(parts)


def gen_appendix_f() -> str:
    raw = read_raw("raw_F_licenses.txt")
    blocks = parse_license_blocks(raw)

    parts = [
        r"% 附录 F — 第三方软件许可",
        r"\biappendix{第三方软件许可}{Third-Party Software Licenses}",
        r"\label{chap:lic}",
        "",
        r"\section{引言}",
        r"\subsection*{Introduction}",
        "",
        "RedHawk 产品包含需保留下列版权声明与许可条款的第三方软件。",
        "本译本对各组件给出\textbf{中文导读}（许可类型、使用义务、与专有代码组合注意点），",
        "长篇法律正文保留英文原文于 \texttt{lstlisting} 环境中，便于对照查阅。",
        "",
        r"\section{第三方组件概览}",
        r"\subsection*{Third-Party Components Overview}",
        "",
        r"\begin{longtable}{@{}p{0.30\textwidth}p{0.18\textwidth}p{0.46\textwidth}@{}}",
        r"\toprule",
        r"\textbf{组件/许可} & \textbf{类型} & \textbf{中文导读} \\",
        r"\midrule",
        r"\endhead",
    ]
    for title, zh, lic_type in LICENSE_OVERVIEW:
        parts.append(f"{latex_escape(title)} & {lic_type} & {latex_escape(zh)} \\\\")
    parts += [
        r"\bottomrule",
        r"\end{longtable}",
        "",
        r"\section{许可正文（英文原文）}",
        r"\subsection*{License Texts (English)}",
        "",
        r"\begin{noteBox}",
        "以下为原书附录 F 收录的第三方许可正文摘录。完整法律文本以 ANSYS 官方发布包为准。",
        r"\end{noteBox}",
        "",
    ]

    # Include first block (CPL) and sample others - truncate very long blocks
    shown_titles = set()
    for i, block in enumerate(blocks[:25]):
        title = block["title"][:80]
        if title in shown_titles:
            continue
        shown_titles.add(title)
        body = block["body"]
        if len(body) > 3500:
            body = body[:3500] + "\n\n... [truncated for study translation; see original manual PDF] ..."
        parts += [
            f"\\subsection{{{latex_escape(title)}}}",
            "",
            r"\begin{lstlisting}[basicstyle=\ttfamily\scriptsize,breaklines=true]",
            latex_escape(body),
            r"\end{lstlisting}",
            "",
        ]

    if len(blocks) > 25:
        parts += [
            f"\\subsection{{其余 {len(blocks)-25} 项许可}}",
            "",
            "原书另含 LAPACK、OpenSSL、Open MPI、zlib、METIS、MPL 等组件的完整许可正文。",
            "学习用途请对照 \texttt{RedHawk\_UG\_2021.pdf} 附录 F 原文。",
            "",
        ]

    return "\n".join(parts)


def main() -> None:
    outputs = {
        "C_file_defs.tex": gen_appendix_c(),
        "D_cmd_gui.tex": gen_appendix_d(),
        "E_utilities.tex": gen_appendix_e(),
        "F_licenses.tex": gen_appendix_f(),
    }
    for fname, content in outputs.items():
        path = CHAPTERS / fname
        path.write_text(fix_tex_escapes(content), encoding="utf-8")
        lines = content.count("\n") + 1
        secs = len(re.findall(r"\\section\{", content))
        print(f"Wrote {path.name}: {lines} lines, {secs} sections")


if __name__ == "__main__":
    main()
