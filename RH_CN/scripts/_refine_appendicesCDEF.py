# -*- coding: utf-8 -*-
"""Generate refined Appendix C–F LaTeX (full-structure translation)."""
from __future__ import annotations

import re
from pathlib import Path

from rh_refine_utils import (
    CAT_ZH,
    CMD_ZH,
    LICENSE_OVERVIEW,
    UTIL_ZH,
    block_to_zh_summary,
    clean_block,
    cjk_ratio,
    fix_tex_escapes,
    format_keyword_subsection,
    format_prose_section,
    format_tcl_command_section,
    latex_escape,
    lst_escape,
    parse_config_keyword_sections,
    parse_keyword_section,
    parse_tcl_commands,
    translate_en,
    translate_prose,
    write_kw_table,
)

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).resolve().parent
CHAPTERS = ROOT / "chapters"


def read_raw(name: str) -> str:
    return (SCRIPTS / name).read_text(encoding="utf-8", errors="replace")


def extract_section(text: str, start: str, end: str) -> str:
    s = text.find(start)
    if s < 0:
        return ""
    e = text.find(end, s + len(start))
    if e < 0:
        e = len(text)
    return text[s:e]


def prose_section_from_raw(raw: str, start: str, end: str) -> list[str]:
    """Convert raw prose block to LaTeX paragraphs (Chinese where possible)."""
    block = extract_section(raw, start, end)
    block = clean_block(block)
    paras = []
    for para in re.split(r"\n\s*\n", block):
        p = para.strip()
        if len(p) < 20:
            continue
        if p.startswith(start):
            p = p[len(start):].strip()
        zh = translate_prose(p)
        if cjk_ratio_simple(zh) > 0.05:
            paras.append(zh)
        else:
            paras.append(p)
    return paras


def cjk_ratio_simple(s: str) -> float:
    cjk = sum(1 for c in s if "\u4e00" <= c <= "\u9fff")
    return cjk / max(len(s), 1)


# ---------------------------------------------------------------------------
# Appendix C
# ---------------------------------------------------------------------------

def gen_appendix_c() -> str:
    raw = read_raw("raw_C_file_defs.txt")

    tech_cats = parse_keyword_section(
        raw, "Technology File Keywords", "Global Switching Configuration"
    )
    gsr_cats = parse_keyword_section(
        raw, "GSR File Keywords", "\nPad, Power/Ground and I/O Definition Files\n"
    )

    parts: list[str] = [
        "% 附录 C — 文件定义（精译重写）",
        "\\biappendix{文件定义}{File Definitions}",
        "\\label{chap:files}",
        "",
        "\\section{引言}",
        "\\subsection*{Introduction}",
        "",
        "本附录描述 RedHawk 支持的内部输入/输出文件格式与内容。",
        "RedHawk 输入文件可在文件名前加设计名前缀；所有此类文件中，行首 \\texttt{\\#} 视为注释。",
        "",
        "\\begin{noteBox}",
        "RedHawk 可直接读取 gzip 压缩格式（\\texttt{*.gz}）的 LEF、DEF、STA、SPEF、VCD、FSDB 与 GDS 文件。",
        "\\end{noteBox}",
        "",
        "\\section{RedHawk 输入文件}",
        "\\subsection*{RedHawk Input Files}",
        "",
        "\\begin{enumerate}",
        "\\item 工艺文件（\\texttt{*.tech}）",
        "\\item 全局开关配置 GSC 文件（\\texttt{*.gsc}）",
        "\\item 全局系统需求 GSR 文件（\\texttt{*.gsr}）",
        "\\item 焊盘实例/单元/位置文件（\\texttt{*.pad}、\\texttt{*.pcell}、\\texttt{*.ploc}）",
        "\\item 库工艺文件（LEF 等，路径在 GSR 中引用）",
        "\\item 设计网表文件（DEF 等）",
        "\\item Synopsys 库文件（\\texttt{*.lib}）",
        "\\end{enumerate}",
        "",
        "下列文件信息须在 GSR 中引用路径。",
        "",
        "\\section{RedHawk 输出文件}",
        "\\subsection*{RedHawk Output Files}",
        "",
        "分析各阶段均会生成结果文件与图形显示。详细报告说明见第~6~章及各主题章节。",
        "",
        "\\section{关键字语法约定}",
        "\\subsection*{Keyword Syntax Conventions}",
        "",
        "RedHawk 命令、选项与关键字语法约定如下：",
        "\\begin{itemize}",
        "\\item \\texttt{<x>} — 需指定的变量或取值",
        "\\item \\texttt{[a|b|c]} — 必须选择 a、b、c 之一",
        "\\item \\texttt{?x?} — 可选参数 x",
        "\\item \\texttt{abcd} — 参数 a、b、c、d 均须指定",
        "\\item \\texttt{<x> ...} — 可追加多个与 x 同类型的元素",
        "\\item \\texttt{\\{ \\{a b c ...\\} \\{j k l ...\\} ...\\}} — 可追加多组相似元素集合",
        "\\item \\texttt{+-*/} — 加减乘除算术运算符",
        "\\end{itemize}",
        "",
        "\\section{Apache 工艺文件（\\texttt{*.tech}）}",
        "\\subsection*{Apache Technology File (*.tech)}",
        "",
        "RedHawk 工艺文件为每个 IC 工艺提供金属层、过孔、介质、衬底及 bump 等参数。",
        "需为每个工艺节点单独准备一份 \\texttt{.tech} 文件。主要内容包括：",
        "\\begin{itemize}",
        "\\item 各金属层名称（与 LEF 一致）、厚度、电阻率、温度系数与 EM 限值",
        "\\item 过孔名称、单孔电阻与 via EM 限值",
        "\\item wire-bond 或 flip-chip bump 的 R/L/C",
        "\\item 介质层厚度、高度与介电常数",
        "\\item 衬底层厚度与电阻率",
        "\\end{itemize}",
        "",
        "\\subsection{单位与前缀}",
        "\\subsubsection*{Unit Prefix Conventions}",
        "",
        "单位区分大小写。支持 t/g/M/k/m/u/n/p/f 等前缀（如 \\texttt{1.3p = 1.3e-12}，数字与单位间无空格）。",
        "长度换算：\\texttt{1 mil = 0.001 inch = 2.54e-5 m}；\\texttt{1 inch = 2.54e-2 m}；\\texttt{1 micron = 1e-6 m}。",
        "",
        "\\subsection{工艺文件加解密}",
        "\\subsubsection*{Encrypting and Decrypting a Tech File}",
        "",
        "\\textbf{全文件加密：}使用 \\texttt{bin} 目录下 \\texttt{techEncrypt}/\\texttt{techDecrypt}。",
        "\\begin{lstlisting}",
        "techEncrypt <tech_filename>    # 生成 <tech_filename>.enc.tech",
        "techDecrypt -i <encrypted_tech_file> -o <tech_file>",
        "\\end{lstlisting}",
        "",
        "\\textbf{部分加密：}在 \\texttt{\\#ENCRYPT\\_START} 与 \\texttt{\\#ENCRYPT\\_END} 注释行之间自动加密敏感 RC/高度/介电常数段。",
        "",
        "\\subsection{工艺文件关键字}",
        "\\subsubsection*{Technology File Keywords}",
        "",
        "\\begin{noteBox}",
        "关键字与选项名不区分大小写。",
        "\\end{noteBox}",
        "",
    ]

    # Tech keywords — full subsection per keyword
    tech_blocks: list = []
    for cat_blocks in tech_cats.values():
        tech_blocks.extend(cat_blocks)
    for block in tech_blocks:
        parts.append(format_keyword_subsection(block, use_gsr=False))

    # GSC
    parts += [
        "\\section{全局开关配置 GSC 文件}",
        "\\subsection*{Global Switching Configuration (GSC) File}",
        "",
        "GSC 文件定义设计中模块、实例与电压域的开关状态，用于功耗计算与仿真。",
        "可与 SIM2IPROF、AVM 或 APLMMX 的多状态定义配合，实现无向量（vectorless）多状态仿真。",
        "在 GSR 中通过 \\gsr{GSC\\_FILES} 指定路径；亦可用 TCL \\cmd{import gsc <file>} 动态读入。",
        "",
        "\\textbf{语法（GSR）：}",
        "\\begin{lstlisting}",
        "GSC_FILES <gsc_FilePathName>",
        "\\end{lstlisting}",
        "",
        "\\textbf{语法（GSC 文件）：}",
        "\\begin{lstlisting}",
        "[<blockName>|<instanceName>] ?<domain_name>?",
        "[UNDECIDED|TOGGLE|HIGH|LOW|POWERUP|POWERDOWN|STANDBY|ENABLE|DISABLE|OFF|<custom_state>]",
        "\\end{lstlisting}",
        "",
        "\\begin{itemize}",
        "\\item 若 GSC 仅含单周期状态，RedHawk 在整个仿真时间内重复该状态",
        "\\item 若含多状态序列，触发多周期 GSC 流程",
        "\\item 多 GSC 文件中重复实例：后读文件覆盖先读值（警告 GSC-028）",
        "\\item 默认启用 \\gsr{DYNAMIC\\_GSC\\_CHECK}，检查 GSC 中未覆盖的实例",
        "\\item 大文件可在首行加注释 \\texttt{\\#EXACT\\_INSTANCE\\_NAME\\_MATCH} 加速解析",
        "\\end{itemize}",
        "",
        "\\subsection{GSC 状态关键字说明}",
        "\\subsubsection*{GSC State Keywords}",
        "",
        "\\begin{itemize}",
        "\\item \\textbf{UNDECIDED}（默认）— 由 RedHawk 在仿真中决定实例/模块状态",
        "\\item \\textbf{TOGGLE} — 实例在仿真中翻转；不推荐用于真实分析",
        "\\item \\textbf{HIGH/LOW} — APL 表征顺序中的高/低翻转电荷条件（非必然对应功耗高低）",
        "\\item \\textbf{POWERUP/POWERDOWN} — 电源门控模块上电/断电",
        "\\item \\textbf{STANDBY} — 无输出翻转，时钟仍可能翻转",
        "\\item \\textbf{DISABLE/ENABLE/OFF} — 实例 inactive/active/关断（OFF 时漏电为零）",
        "\\item \\textbf{<custom\\_state>} — SIM2IPROF/APLMMX 定义的自定义状态",
        "\\end{itemize}",
        "",
        "\\section{全局系统需求 GSR 文件}",
        "\\subsection*{Global System Requirements File (*.gsr)}",
        "",
        "GSR 是 RedHawk 的\\textbf{主配置文件}，汇总输入设计文件路径、分析类型、仿真参数与流程控制关键字。",
        "可用 TCL \\cmd{gsr get}/\\cmd{gsr set} 查询或修改。关键字名不区分大小写。",
        "",
        f"本译本按原书 {len(gsr_cats)} 类列出全部 {sum(len(v) for v in gsr_cats.values())} 个 GSR 关键字；",
        "每类以长表给出中文用途说明，语法与默认值见原书或在线 \\cmd{help}。",
        "",
        "\\begin{noteBox}",
        "GSR 关键字名不区分大小写；\\gsr{DEFINE} 与 \\gsr{INCLUDE} 可组织多文件 GSR 结构。",
        "\\end{noteBox}",
        "",
    ]

    for cat_en, blocks in gsr_cats.items():
        if cat_en == "GSR File Keywords":
            continue
        cat_zh = CAT_ZH.get(cat_en, cat_en)
        parts += [
            f"\\subsection{{{cat_zh}}}",
            f"\\subsubsection*{{{cat_en}}}",
            "",
            f"本类共 {len(blocks)} 个 GSR 关键字。以下逐条给出中文用途、语法、默认值与示例。",
            "",
        ]
        for block in blocks:
            parts.append(format_keyword_subsection(block, use_gsr=True))

    # Pad files — full translation from raw
    pad_raw = extract_section(raw, "Unified Pad Input File Format", "Library Technology Files")
    parts += [
        "\\section{焊盘、电源/地与 I/O 定义文件}",
        "\\subsection*{Pad, Power/Ground and I/O Definition Files}",
        "",
        "\\subsection{统一焊盘输入格式}",
        "\\subsubsection*{Unified Pad Input File Format}",
        "",
    ]
    parts.extend(format_prose_section(pad_raw))

    pad_individual = extract_section(raw, "Individual Pad File Specification", "Library Technology Files")
    parts += [
        "\\subsection{分散焊盘文件}",
        "\\subsubsection*{Individual Pad File Specification}",
        "",
    ]
    parts.extend(format_prose_section(pad_individual))

    # LEF / DEF / LIB / STA — full sections from raw
    lef_raw = extract_section(raw, "Library Technology Files", "Design Netlist Files")
    def_raw = extract_section(raw, "Design Netlist Files", "Synopsys Library Files")
    lib_raw = extract_section(raw, "Synopsys Library Files", "Timing Data File")
    sta_raw = extract_section(raw, "Timing Data File", "Result Files")

    parts += [
        "\\section{库工艺与设计网表文件}",
        "\\subsection*{Library Technology and Design Netlist Files}",
        "",
        "\\subsection{库工艺文件（LEF）}",
        "\\subsubsection*{Library Technology Files}",
        "",
    ]
    parts.extend(format_prose_section(lef_raw))

    parts += [
        "\\subsection{设计网表文件（DEF）}",
        "\\subsubsection*{Design Netlist Files}",
        "",
    ]
    parts.extend(format_prose_section(def_raw))

    parts += [
        "\\subsection{Synopsys 库文件（LIB）}",
        "\\subsubsection*{Synopsys Library Files}",
        "",
    ]
    parts.extend(format_prose_section(lib_raw))

    parts += [
        "\\section{时序数据文件}",
        "\\subsection*{Timing Data File}",
        "",
    ]
    parts.extend(format_prose_section(sta_raw))

    parts += [
        "\\section{结果文件}",
        "\\subsection*{Result Files}",
        "",
        "RedHawk 在 \\texttt{adsRpt}、\\texttt{adsPower} 等目录下生成功耗摘要、IR/DvD 结果、",
        "EM 报告、电流波形与各类文本/图形报告。详见第~6~章「报告」。",
        "",
        "\\begin{seeAlsoBox}",
        "结果文件类型与命名约定见第~6~章及各分析主题章节。",
        "\\end{seeAlsoBox}",
        "",
    ]
    return "\n".join(parts)


# ---------------------------------------------------------------------------
# Appendix D
# ---------------------------------------------------------------------------

def gen_appendix_d() -> str:
    raw = read_raw("raw_D_cmd_gui.txt")
    tcl_cmds = parse_tcl_commands(raw)

    parts: list[str] = [
        "% 附录 D — 命令与 GUI 参考（精译重写）",
        "\\biappendix{命令与 GUI 参考}{Command and GUI Reference}",
        "\\label{chap:cmd}",
        "",
        "\\section{引言}",
        "\\subsection*{Introduction}",
        "",
        "本附录描述 RedHawk 的两种用户界面：TCL 命令行与图形用户界面（GUI）。",
        "",
        "\\section{启动 RedHawk}",
        "\\subsection*{Invoking RedHawk}",
        "",
        "在 UNIX 工作目录下执行：",
        "\\begin{lstlisting}",
        "redhawk [-b <cmnd_file>] [-c <cmnd_file>] [-f <cmnd_file>]",
        "        [-i ?<cmnd_file>?] [-h] [-tclsh] [-lmhold <cmdfile>]",
        "        [-lmwait <wait_sec>] [-iconify]",
        "        [-style [CDE|Motif|Plastique|Windows]]",
        "        [-stack [<stacksize_MB>|unlimited]]",
        "        [clampviewer <IV_FileName> [<IV_Name(s)>] [<options>]]",
        "\\end{lstlisting}",
        "",
        "\\begin{itemize}",
        "\\item \\texttt{-b} — 批处理运行 TCL 脚本，不显示 GUI，结束后退出",
        "\\item \\texttt{-c} — 预解析 TCL 脚本并报告语法警告/错误，不执行",
        "\\item \\texttt{-f} — 运行 TCL 脚本并显示 GUI",
        "\\item \\texttt{-i} — 交互 TCL 命令行，无 GUI；须显式退出命令才结束",
        "\\item \\texttt{-h} — 显示启动语法帮助",
        "\\item \\texttt{-tclsh} — 完整 TCL shell；检出许可证后可用 \\cmd{redhawk} 启动 GUI",
        "\\item \\texttt{-lmhold} — 退出后保持许可证占用并重新显示 shell",
        "\\item \\texttt{-lmwait} — 无可用许可证时等待（可指定秒数，超时则退出）",
        "\\item \\texttt{-iconify} — 启动时最小化 GUI（仍需 DISPLAY 环境）",
        "\\item \\texttt{-style} — 更改 GUI 窗口管理器风格（默认 Plastique）",
        "\\item \\texttt{-stack} — 指定栈大小（MB）或 unlimited",
        "\\end{itemize}",
        "",
        "\\section{终止进程}",
        "\\subsection*{Terminating Processes}",
        "",
        "\\texttt{Ctrl+C} 可终止当前操作及多数子进程；在 X-term 中可能直接杀死主进程。",
        "\\cmd{setup design} 与提取等少数流程在 GUI 中不响应 Ctrl+C。",
        "",
        "\\section{TCL 语法约定}",
        "\\subsection*{TCL Syntax Conventions}",
        "",
        "语法约定同附录 C「关键字语法约定」。",
        "",
        "\\section{TCL 命令概要}",
        "\\subsection*{TCL Command Summary}",
        "",
        "TCL 脚本可手动编写，也可通过 GUI Playback 录制。使用 \\cmd{help <命令名>} 查看完整语法。",
        "GUI 中支持 TAB 自动补全（按 TAB 可展开命令及下一级子选项）。",
        "",
        f"下表列出 {len(tcl_cmds)} 个一级 TCL 命令及中文说明。",
        "",
        "\\begin{longtable}{@{}p{0.22\\textwidth}p{0.72\\textwidth}@{}}",
        "\\toprule",
        "\\textbf{命令} & \\textbf{用途说明} \\\\",
        "\\midrule",
        "\\endhead",
    ]

    for cmd in sorted(tcl_cmds, key=lambda c: c.name):
        zh = CMD_ZH.get(cmd.name, translate_en(cmd.body[:400], cmd.name))
        cmd_tex = latex_escape(cmd.name).replace(" ", r"\_")
        parts.append(f"\\cmd{{{cmd_tex}}} & {latex_escape(zh)} \\\\")

    parts += [
        "\\bottomrule",
        "\\end{longtable}",
        "",
        "\\section{TCL 命令详解}",
        "\\subsection*{TCL Command Details}",
        "",
        "以下按原书结构逐条译出各 TCL 命令的语法、选项说明与示例。",
        "",
    ]

    for cmd in tcl_cmds:
        parts.append(format_tcl_command_section(cmd))

    # perform subcommands table
    perform_sub = [
        ("analysis", "执行指定类型分析（静态/动态 IR、EM 等）"),
        ("extraction", "执行 R/C 电源网格提取"),
        ("pwrcalc", "功耗计算"),
        ("powermodel", "生成功耗模型"),
        ("res_calc", "电阻/网格电阻计算"),
        ("gridcheck", "电源网格 DRC/连通性检查"),
        ("clampcheck", "ESD clamp 检查"),
        ("thermalmodel", "热分析建模"),
        ("jitter", "抖动分析"),
        ("min_res_path", "最小电阻路径分析"),
        ("esdcheck", "ESD 检查"),
        ("dvd", "动态电压跌落（DvD）分析"),
    ]
    parts += [
        "\\subsection{\\cmd{perform} 子命令概要}",
        "\\subsubsection*{perform Subcommand Summary}",
        "",
        "\\begin{longtable}{@{}p{0.26\\textwidth}p{0.68\\textwidth}@{}}",
        "\\toprule",
        "\\textbf{子命令} & \\textbf{说明} \\\\",
        "\\midrule",
        "\\endhead",
    ]
    for sub, zh in perform_sub:
        parts.append(f"\\cmd{{perform {sub}}} & {latex_escape(zh)} \\\\")
    parts += ["\\bottomrule", "\\end{longtable}", ""]

    # GUI section
    parts += gen_gui_section(raw)
    return "\n".join(parts)


def gen_gui_section(raw: str) -> list[str]:
    gui_start = raw.find("RedHawk Graphic User Interface Description")
    if gui_start < 0:
        gui_start = raw.find("GUI Menu")
    gui_raw = raw[gui_start:] if gui_start >= 0 else ""

    parts = [
        "\\section{RedHawk 图形用户界面}",
        "\\subsection*{RedHawk Graphic User Interface Description}",
        "",
        "\\figplaceholder{Figure D-3}{RedHawk 图形用户界面布局}",
        "",
        "GUI 主要区域包括菜单栏、主显示区、控制按钮、视图配置、结果查看、查询、TCL 命令行与日志区。",
        "",
    ]

    # Mouse and control buttons from raw (before GUI Menu)
    mouse_raw = extract_section(gui_raw, "Mouse Function", "GUI Menu")
    if mouse_raw:
        parts += [
            "\\subsection{鼠标操作}",
            "\\subsubsection*{Mouse Function}",
            "",
        ]
        parts.extend(format_prose_section(mouse_raw))

    ctrl_raw = extract_section(gui_raw, "GUI Control Buttons", "GUI Menu")
    if ctrl_raw:
        parts += [
            "\\subsection{GUI 控制按钮}",
            "\\subsubsection*{GUI Control Buttons}",
            "",
        ]
        parts.extend(format_prose_section(ctrl_raw))

    # Full menu translation
    menus = parse_gui_menus(raw)
    parts += [
        "\\subsection{GUI 菜单}",
        "\\subsubsection*{GUI Menu}",
        "",
    ]
    for menu_zh, menu_en, items in menus:
        parts += [
            f"\\subsection{{{menu_zh}}}",
            f"\\subsubsection*{{{menu_en}}}",
            "",
        ]
        for zh_desc, left, right in items:
            menu_path = f"\\textbf{{{latex_escape(left)} $\\rightarrow$ {latex_escape(right)}}}"
            parts.append(f"{menu_path} — {latex_escape(zh_desc)}")
            parts.append("")

    # Layer dialog and other GUI sections after menus
    layer_raw = extract_section(gui_raw, "Layer Dialog", "Playback Menu")
    if layer_raw:
        parts += [
            "\\subsection{层与色图对话框}",
            "\\subsubsection*{Layer and Colormap Dialogs}",
            "",
        ]
        parts.extend(format_prose_section(layer_raw))

    playback_raw = extract_section(gui_raw, "Playback Menu", "Query Menu")
    if not playback_raw:
        playback_raw = extract_section(gui_raw, "Playback", "APPENDIX")
    if playback_raw:
        parts += [
            "\\subsection{回放与其他 GUI 功能}",
            "\\subsubsection*{Playback and Other GUI Features}",
            "",
        ]
        parts.extend(format_prose_section(playback_raw[:8000]))

    parts += [
        "\\begin{seeAlsoBox}",
        "完整 GUI 控件说明见原书附录 D 及第~3~章 GUI 概述。",
        "\\end{seeAlsoBox}",
        "",
    ]
    return parts


def parse_gui_menus(raw: str) -> list[tuple[str, str, list[tuple[str, str]]]]:
    """Parse File/Edit/View/... menu items from raw Appendix D."""
    start = raw.find("GUI Menu")
    if start < 0:
        return []
    section = raw[start:]
    menus: list[tuple[str, str, list[tuple[str, str]]]] = []
    current_menu_en = ""
    current_menu_zh = ""
    items: list[tuple[str, str]] = []
    pending_left = ""
    pending_right = ""
    pending_desc: list[str] = []

    menu_map = {
        "File Menu": ("文件菜单", "File Menu"),
        "Edit Menu": ("编辑菜单", "Edit Menu"),
        "View Menu": ("视图菜单", "View Menu"),
        "Setup Menu": ("设置菜单", "Setup Menu"),
        "Analysis Menu": ("分析菜单", "Analysis Menu"),
        "Results Menu": ("结果菜单", "Results Menu"),
        "Dynamic Menu": ("动态分析菜单", "Dynamic Menu"),
        "Tools Menu": ("工具菜单", "Tools Menu"),
        "Query Menu": ("查询菜单", "Query Menu"),
        "Windows Menu": ("窗口菜单", "Windows Menu"),
        "Playback Menu": ("回放菜单", "Playback Menu"),
    }

    def flush_item(
        left: str, right: str, pd: list[str], it: list[tuple[str, str]]
    ) -> tuple[str, str, list[str]]:
        if left:
            desc_en = " ".join(pd)
            zh = translate_en(desc_en[:500], "")
            if cjk_ratio(zh) < 0.15 and desc_en:
                zh = translate_en(desc_en[:300], "")
            if not zh or cjk_ratio(zh) < 0.1:
                zh = "打开对应对话框或执行相应 GUI 操作。"
            it.append((zh, left, right))
        return "", "", []

    for line in section.splitlines():
        s = line.strip()
        if not s or "ANSYS" in s or "RedHawk User Manual" in s:
            continue
        if s.startswith("Figure"):
            pending_left, pending_right, pending_desc = flush_item(
                pending_left, pending_right, pending_desc, items
            )
            continue
        matched_menu = False
        for en, (zh, _) in menu_map.items():
            if s == en:
                pending_left, pending_right, pending_desc = flush_item(
                    pending_left, pending_right, pending_desc, items
                )
                if current_menu_en and items:
                    menus.append((current_menu_zh, current_menu_en, items))
                current_menu_en = en
                current_menu_zh = zh
                items = []
                pending_left = ""
                pending_right = ""
                pending_desc = []
                matched_menu = True
                break
        if not matched_menu:
            if "->" in s and not s.startswith("Figure") and "Menu" not in s:
                pending_left, pending_right, pending_desc = flush_item(
                    pending_left, pending_right, pending_desc, items
                )
                parts = s.split("->", 1)
                pending_left = parts[0].strip()
                pending_right = parts[1].strip()
                pending_desc = []
            elif pending_left and len(s) > 30 and not s.startswith(("•", "-", "Figure")):
                pending_desc.append(s)

    pending_left, pending_right, pending_desc = flush_item(
        pending_left, pending_right, pending_desc, items
    )
    if current_menu_en and items:
        menus.append((current_menu_zh, current_menu_en, items))
    return menus


# ---------------------------------------------------------------------------
# Appendix E
# ---------------------------------------------------------------------------

def gen_appendix_e() -> str:
    raw = read_raw("raw_E_utilities.txt")
    util_names = [
        "vcdtrans", "vcdscan", "fsdbtrans", "ircx2tech", "rhtech",
        "gds2rh/gds2def", "pt2timing", "sim2iprof", "aplreader",
        "aplcdev2pwc", "aplcopy", "aplchk", "clampviewer",
    ]

    parts: list[str] = [
        "% 附录 E — 实用程序（精译重写）",
        "\\biappendix{实用程序}{Utility Programs}",
        "\\label{chap:util}",
        "",
        "\\section{引言}",
        "\\subsection*{Introduction}",
        "",
        "本附录介绍 RedHawk 安装目录 \\texttt{bin} 下的关键命令行实用程序。",
        "",
        "\\begin{itemize}",
    ]
    for name in util_names:
        zh = UTIL_ZH.get(name, name)
        parts.append(f"\\item \\textbf{{{latex_escape(name)}}} — {latex_escape(zh)}")
    parts += ["\\end{itemize}", ""]

    for name in util_names:
        key = name.split("/")[0]
        block = extract_utility_block(raw, name, key)
        parts += [
            f"\\section{{{latex_escape(name)}}}",
            f"\\subsection*{{{name}}}",
            "",
            UTIL_ZH.get(name, ""),
            "",
        ]
        if block:
            parts.extend(format_prose_section(block[:12000]))

        # gds2rh/gds2def configuration keywords — full subsection per keyword
        if name == "gds2rh/gds2def":
            gds_cats = parse_config_keyword_sections(
                raw,
                "GDSII Files Keywords",
                ["gds2rh -m and gds2def -m", "sim2iprof", "APPENDIX F"],
            )
            top_cats = parse_config_keyword_sections(
                raw,
                "Top Cell Definition Keywords",
                ["Nets Definition Keywords", "gds2rh -m"],
            )
            net_cats = parse_config_keyword_sections(
                raw,
                "Nets Definition Keywords",
                ["Layer Map", "Geometry Extraction"],
            )
            all_gds_cats = {**gds_cats, **top_cats, **net_cats}
            # Additional keyword sections in gds2rh block
            for marker, enders in [
                ("Layer Map Definition Keywords", ["Geometry Extraction", "Input LEF"]),
                ("Geometry Extraction Keywords", ["Selective Cell", "Auto Pad"]),
                ("Selective Cell Hierarchy", ["Auto Pad", "DSPF"]),
                ("DSPF/SPEF-based", ["Switch Cell", "Other Keywords"]),
                ("Switch Cell Handling", ["Other Keywords", "VALIDATE_MODEL"]),
                ("Other Keywords", ["gds2rh -m"]),
            ]:
                extra = parse_config_keyword_sections(raw, marker, enders)
                all_gds_cats.update(extra)

            parts += [
                "\\subsection{GDS2RH/GDS2DEF 配置文件关键字}",
                "\\subsubsection*{GDS2RH/GDS2DEF Configuration File Keywords}",
                "",
                "以下逐条译出 gds2rh/gds2def 配置文件中的主要关键字（语法、默认值与示例）。",
                "",
            ]
            for cat_en, blocks in all_gds_cats.items():
                if not blocks:
                    continue
                cat_zh = cat_en.replace("Keywords", "关键字")
                parts += [
                    f"\\subsection{{{latex_escape(cat_zh)}}}",
                    f"\\subsubsection*{{{cat_en}}}",
                    "",
                ]
                for b in blocks:
                    parts.append(format_keyword_subsection(b, use_gsr=False))

        # sim2iprof / apl* config keywords
        if name == "sim2iprof":
            sim_cats = parse_config_keyword_sections(
                raw, "sim2iprof", ["aplreader", "aplcdev2pwc"]
            )
            for cat_en, blocks in sim_cats.items():
                if blocks and cat_en != "sim2iprof":
                    parts += [
                        f"\\subsection{{{latex_escape(cat_en)}}}",
                        "",
                    ]
                    for b in blocks:
                        parts.append(format_keyword_subsection(b, use_gsr=False))

        if name in ("aplreader", "aplcdev2pwc", "aplcopy", "aplchk"):
            apl_cats = parse_config_keyword_sections(
                raw, name, util_names
            )
            for cat_en, blocks in apl_cats.items():
                for b in blocks:
                    if b.name != name.upper() and len(b.description) > 20:
                        parts.append(format_keyword_subsection(b, use_gsr=False))

    parts += [
        "\\section{通用注意事项}",
        "\\subsection*{General Notes}",
        "",
        "\\begin{noteBox}",
        "vcdtrans/vcdscan/fsdbtrans 的 \\texttt{-s}/\\texttt{-e} 时间值若小于 0.1，RedHawk 假定单位为秒；否则为皮秒（ps）。",
        "\\end{noteBox}",
        "",
        "\\begin{tipBox}",
        "VCD 动态 IR 流程：先用 vcdscan 获取峰值功耗周期 \\texttt{<FROM>,<TO>}，",
        "再在 GUI Dynamic 菜单中启动 VCD-based Dynamic IR-drop Analysis。",
        "\\end{tipBox}",
        "",
    ]
    return "\n".join(parts)


def extract_utility_block(raw: str, name: str, key: str) -> str:
    lines = raw.splitlines()
    start_i = -1
    for i, line in enumerate(lines):
        s = line.strip()
        if s == name or s == key:
            start_i = i
            break
    if start_i < 0:
        return ""
    end_i = len(lines)
    util_headers = [
        "vcdtrans", "vcdscan", "fsdbtrans", "ircx2tech", "rhtech",
        "gds2rh/gds2def", "pt2timing", "sim2iprof", "aplreader",
        "aplcdev2pwc", "aplcopy", "aplchk", "clampviewer",
    ]
    for j in range(start_i + 1, len(lines)):
        s = lines[j].strip()
        if s in util_headers and s != name and s != key:
            end_i = j
            break
        if s.startswith("APPENDIX") and j > start_i + 5:
            end_i = j
            break
    return clean_block("\n".join(lines[start_i:end_i]))


def parse_where_options(block: str) -> list[tuple[str, str]]:
    opts: list[tuple[str, str]] = []
    in_where = False
    for line in block.splitlines():
        s = line.strip()
        if s.lower().startswith("where"):
            in_where = True
            continue
        if in_where and s.startswith("-") and ":" in s:
            opt, desc = s.split(":", 1)
            opts.append((opt.strip(), translate_en(desc.strip())))
        elif in_where and s.startswith("Example"):
            break
    return opts[:20]


# ---------------------------------------------------------------------------
# Appendix F
# ---------------------------------------------------------------------------

def gen_appendix_f() -> str:
    raw = read_raw("raw_F_licenses.txt")
    blocks = parse_license_blocks(raw)

    parts: list[str] = [
        "% 附录 F — 第三方软件许可（精译重写）",
        "\\biappendix{第三方软件许可}{Third-Party Software Licenses}",
        "\\label{chap:lic}",
        "",
        "\\section{引言}",
        "\\subsection*{Introduction}",
        "",
        "RedHawk 产品包含需保留下列版权声明与许可条款的第三方软件。",
        "本译本对各组件给出\\textbf{中文导读}（许可类型、使用义务、与专有代码组合注意点），",
        "长篇法律正文保留英文原文于 \\texttt{lstlisting} 环境中，便于对照查阅。",
        "",
        "\\section{第三方组件概览}",
        "\\subsection*{Third-Party Components Overview}",
        "",
        "\\begin{longtable}{@{}p{0.30\\textwidth}p{0.18\\textwidth}p{0.46\\textwidth}@{}}",
        "\\toprule",
        "\\textbf{组件/许可} & \\textbf{类型} & \\textbf{中文导读} \\\\",
        "\\midrule",
        "\\endhead",
    ]
    for title, lic_type, zh in LICENSE_OVERVIEW:
        parts.append(f"{latex_escape(title)} & {lic_type} & {latex_escape(zh)} \\\\")
    parts += [
        "\\bottomrule",
        "\\end{longtable}",
        "",
        "\\section{许可正文（英文原文）}",
        "\\subsection*{License Texts (English)}",
        "",
        "\\begin{noteBox}",
        "以下为原书附录 F 收录的第三方许可正文。完整法律文本以 ANSYS 官方发布包为准。",
        "\\end{noteBox}",
        "",
    ]

    for i, block in enumerate(blocks):
        title = block["title"][:100]
        body = block["body"]
        parts += [
            f"\\subsection{{{latex_escape(title)}}}",
            "",
            "\\begin{lstlisting}[basicstyle=\\ttfamily\\scriptsize,breaklines=true]",
            latex_escape(body),
            "\\end{lstlisting}",
            "",
        ]

    return "\n".join(parts)


def parse_license_blocks(text: str) -> list[dict[str, str]]:
    intro_end = text.find("THE ACCOMPANYING PROGRAM IS PROVIDED")
    body = text[intro_end:] if intro_end > 0 else text
    # Split on page headers / double blank with indent
    chunks = re.split(
        r"\n\n\n\s+|\n\nANSYS, Inc\.\n",
        body,
    )
    blocks: list[dict[str, str]] = []
    current_title = "Common Public License 1.0"
    current_lines: list[str] = []

    license_markers = [
        "THE ACCOMPANYING PROGRAM",
        "The MIT License",
        "Permission is hereby granted",
        "Copyright (C)",
        "Copyright (c)",
        "GAlib License",
        "Original SSLeay License",
        "Mozilla Public License",
        "Apache License",
    ]

    for chunk in chunks:
        chunk = chunk.strip()
        if len(chunk) < 60:
            continue
        lines = chunk.splitlines()
        title = lines[0].strip()[:120]
        for marker in license_markers:
            if marker in chunk[:200]:
                if current_lines:
                    blocks.append({
                        "title": current_title,
                        "body": "\n".join(current_lines).strip(),
                    })
                current_title = title
                current_lines = lines
                break
        else:
            current_lines.extend(lines)

    if current_lines:
        blocks.append({"title": current_title, "body": "\n".join(current_lines).strip()})

    if not blocks:
        blocks.append({"title": "Third-Party Licenses", "body": body.strip()})
    return blocks


def main() -> None:
    outputs = {
        "C_file_defs.tex": gen_appendix_c(),
        "D_cmd_gui.tex": gen_appendix_d(),
        "E_utilities.tex": gen_appendix_e(),
        "F_licenses.tex": gen_appendix_f(),
    }
    for fname, content in outputs.items():
        path = CHAPTERS / fname
        fixed = fix_tex_escapes(content)
        path.write_text(fixed, encoding="utf-8")
        lines = fixed.count("\n") + 1
        secs = len(re.findall(r"\\section\{", fixed))
        subs = len(re.findall(r"\\subsection\{", fixed))
        print(f"{fname}: {lines} lines, {secs} sections, {subs} subsections")


if __name__ == "__main__":
    main()
