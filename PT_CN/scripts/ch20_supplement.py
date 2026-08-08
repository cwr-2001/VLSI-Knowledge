# -*- coding: utf-8 -*-
"""Supplemental GUI chapter content."""
from pt_tex_utils import fig, itemize, lst, note, subsection, subsubsection


def build_supplement() -> str:
    p = []

    p.append(subsection("GUI 菜单结构概览", "GUI Menu Structure Overview"))
    p.append("PrimeTime GUI 主菜单包括：\n")
    p.append(
        itemize(
            [
                r"\textbf{File} — 打开/关闭 GUI、保存/恢复会话、退出",
                r"\textbf{Edit} — 撤销/重做、复制、首选项",
                r"\textbf{View} — 工具栏、视图窗口、布局图、密度图、缩放",
                r"\textbf{Select} — 按名称/类型/路径选择对象",
                r"\textbf{Timing} — Path Analyzer、Recalculated Path 比较、时序报告",
                r"\textbf{Clock} — Clock Analyzer、Abstract Clock Graph",
                r"\textbf{Schematic} — 原理图视图、展开/折叠、层次导航",
                r"\textbf{ECO} — 插入/删除缓冲器、调整单元尺寸（需布局视图）",
                r"\textbf{Window} — 窗口管理、Layout window",
                r"\textbf{Help} — 帮助与文档",
            ]
        )
    )

    p.append(subsection("路径分析器高级功能", "Advanced Path Analyzer Features"))
    p.append(
        "路径分析器支持多列排序、过滤表达式、导出 CSV、"
        "与 Path Inspector 联动、按 session 分组（IMSA）等。\n\n"
        "预定义分类规则包括：Startpoint、Endpoint、Start Clock、End Clock、"
        "Path Group、Logic Levels、Fanout、Net Length 等。\n\n"
    )

    p.append(subsubsection("过滤表达式语法", "Filter Expression Syntax"))
    p.append(
        "自定义过滤支持比较运算符（==、!=、>、<）与逻辑组合（\\texttt{\\&\\&}、\\texttt{||}）。"
        "属性名区分大小写，字符串值用引号括起。\n\n"
    )

    p.append(subsection("原理图视图工具", "Schematic View Tools"))
    p.append(
        itemize(
            [
                "Zoom In/Out/Fit — 缩放与适应窗口",
                "Pan — 平移视图",
                "Highlight — 高亮选中对象",
                "Query — 查询 pin/cell/net 属性",
                "Add Fanin/Fanout — 添加扇入/扇出逻辑",
                "Add Path — 添加时序路径到原理图",
            ]
        )
    )

    p.append(subsection("抽象时钟图高级操作", "Advanced Abstract Clock Graph Operations"))
    p.append(
        "支持按时钟域过滤、显示/隐藏 ICG、显示生成时钟关系、"
        "导出时钟树报告、与 Clock Analyzer 联动跳转。\n\n"
    )
    p.append(fig("Figure 322", "时钟矩阵符号图例", "fig:clk-matrix-legend"))

    p.append(subsection("波形与数据表视图", "Waveform and Data Table Views"))
    p.append(
        "GUI 支持将路径延迟数据以波形图与表格形式显示，"
        "便于分析路径上各段增量延迟贡献。\n\n"
    )

    p.append(subsection("GUI 会话保存与恢复", "GUI Session Save and Restore"))
    p.append(
        "save_session 可保存完整会话或仅路径集合；"
        "restore_session 恢复后可在 GUI 中继续分析。"
        "IMSA 模式依赖 save/restore 跨场景比较路径。\n\n"
    )
    p.append(
        lst(
            "save_session -only_timing_paths $paths /path/to/session\n"
            "restore_session /path/to/session"
        )
    )

    p.append(subsection("GUI 与 pt_shell 协同", "GUI and pt_shell Interaction"))
    p.append(
        note(
            "GUI 与 pt_shell 共享同一设计数据库；"
            "在任一处执行的命令会更新双方视图。"
            "耗时 update_timing 建议在 pt_shell 终端执行，完成后在 GUI 刷新视图。"
        )
    )

    p.append(subsection("GUI 相关环境变量", "GUI Environment Variables"))
    p.append(
        itemize(
            [
                "DISPLAY — X11 显示（必需）",
                "SYNOPSYS_PT_GUI_PREF — 首选项文件路径覆盖",
                "TCL_LIBRARY — Tcl 脚本库路径",
            ]
        )
    )

    p.append(subsection(r"gui\_* 命令完整列表（节选）", r"gui\_* Command Reference (Selected)"))
    p.append(
        r"\begin{longtable}{@{}p{0.38\textwidth} p{0.55\textwidth}@{}}" + "\n"
        r"\toprule" + "\n"
        r"命令 & 功能 \\" + "\n"
        r"\midrule" + "\n"
        r"\texttt{gui\_start} / \texttt{gui\_stop} & 打开/关闭 GUI \\" + "\n"
        r"\texttt{gui\_change\_highlight} & 操纵全局高亮对象集 \\" + "\n"
        r"\texttt{gui\_create\_attrgroup} & 创建属性组 \\" + "\n"
        r"\texttt{gui\_create\_pref\_category} & 创建首选项类别 \\" + "\n"
        r"\texttt{gui\_create\_pref\_key} & 创建首选项键值 \\" + "\n"
        r"\texttt{gui\_create\_vm} & 创建 Visual Mode \\" + "\n"
        r"\texttt{gui\_execute\_menu\_item} & 执行菜单项 \\" + "\n"
        r"\texttt{gui\_get\_current\_window} & 获取当前窗口 \\" + "\n"
        r"\texttt{gui\_set\_attrgroup\_value} & 设置属性组值 \\" + "\n"
        r"\texttt{gui\_set\_pref\_key\_value} & 设置首选项值 \\" + "\n"
        r"\texttt{gui\_show\_window} & 显示指定窗口 \\" + "\n"
        r"\texttt{gui\_update\_display} & 刷新显示 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{longtable}" + "\n\n"
    )

    return "".join(p)
