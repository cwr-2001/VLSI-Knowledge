# -*- coding: utf-8 -*-
"""Supplemental ECO chapter content."""
from pt_tex_utils import cmd, fig, itemize, lst, note, opt, subsection, subsubsection


def build_supplement() -> str:
    p = []

    p.append(subsection("fix_eco_timing 选项详解", "fix_eco_timing Option Details"))
    p.append(
        f"{cmd('fix_eco_timing')} 主要选项：\n"
    )
    p.append(
        r"\begin{longtable}{@{}p{0.32\textwidth} p{0.6\textwidth}@{}}" + "\n"
        r"\toprule" + "\n"
        r"选项 & 说明 \\" + "\n"
        r"\midrule" + "\n"
        r"-type setup\textbar hold & 修复类型 \\" + "\n"
        r"-methods \{insert\_buffer size\_cell remove\_buffer\} & 修复方法 \\" + "\n"
        r"-cell\_type data\_path\textbar clock\_network & 目标单元类型 \\" + "\n"
        r"-buffer\_list \{...\} & 可用缓冲器列表 \\" + "\n"
        r"-target\_violation\_type wns\textbar tns & 优化目标 \\" + "\n"
        r"-wns\_limit value & WNS 恶化限制 \\" + "\n"
        r"-max\_cells\_per\_path N & 每条路径最大 ECO 单元数 \\" + "\n"
        r"-effort low\textbar medium\textbar high & 修复力度 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{longtable}" + "\n\n"
    )

    p.append(subsection("fix_eco_drc 选项详解", "fix_eco_drc Option Details"))
    p.append(
        "修复 max_transition、max_capacitance、max_fanout、噪声与电迁移违例。"
        "支持 load shielding、buffer insertion、cell sizing 等方法。\n\n"
    )

    p.append(subsection("fix_eco_power 选项详解", "fix_eco_power Option Details"))
    p.append(
        "功耗回收在不恶化时序/DRC 前提下降低漏电。"
        "支持按库单元名、用户属性、机器学习模型选择替换单元。\n\n"
    )

    p.append(subsection("set_eco_options 物理选项", "set_eco_options Physical Options"))
    p.append(
        lst(
            "set_eco_options \\\n"
            "  -physical_design_path design.def \\\n"
            "  -physical_tech_lib_path tech.lef \\\n"
            "  -physical_lib_path stdcells.lef \\\n"
            "  -physical_constraint_file phys_constraints.tcl \\\n"
            "  -target_directories {./eco_cells}"
        )
    )

    p.append(subsection("物理 ECO 条件变量", "Physical ECO Condition Variables"))
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{物理 ECO 相关条件与变量}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}p{0.4\textwidth} p{0.5\textwidth}@{}}" + "\n"
        r"\toprule" + "\n"
        r"条件 & 相关变量 \\" + "\n"
        r"\midrule" + "\n"
        r"单元可用性 & eco\_allow\_footprint\_change \\" + "\n"
        r"缓冲器选择 & eco\_buffer\_list\_for\_reference \\" + "\n"
        r"最大扇出 & eco\_max\_fanout \\" + "\n"
        r"物理合法化 & eco\_physical\_mode \\" + "\n"
        r"Site 规则 & eco\_respect\_sites \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsection("DEF 到 LEF Site 名称转换", "DEF to LEF Site Name Conversion"))
    p.append(
        "当 DEF 中 SITE 名称与 LEF 不一致时，"
        "PrimeTime 提供映射规则（如 SITE CORE2T 映射到 LEF SITE）。\n\n"
    )
    p.append(lst("SITE CORE2T\nEND CORE2T"))

    p.append(subsection("层次块缺失 LEF 文件", "Missing LEF Files for Hierarchical Blocks"))
    p.append(
        "即使层次块 DEF 组件缺少完整 LEF，仍可读入 LEF/DEF 格式物理数据；"
        "工具对黑盒块使用占位物理信息。\n\n"
    )

    p.append(subsection("高级间距标签与规则", "Advanced Spacing Labels and Rules"))
    p.append(
        "物理感知 ECO 可考虑先进间距规则（advanced spacing rules），"
        "通过物理约束文件指定。\n\n"
    )

    p.append(subsection("StarRC 寄生数据文件", "Parasitic Data Files From StarRC"))
    p.append(
        "物理 ECO 需要带位置信息的 SPEF/GPD 寄生；"
        "StarRC 从 ICC II 数据库提取时须启用相应选项以保留位置。\n\n"
    )

    p.append(subsection("单场景与多场景功耗回收示例", "Single and Multi-Scenario Power Recovery Examples"))
    p.append(
        "单场景：fix_eco_power 后直接 write_changes。"
        "多场景 DMSA：对各场景分别 fix_eco_power 或合并违例后统一修复。\n\n"
    )

    p.append(subsection("功耗回收操作统计", "Power Recovery Operation Statistics"))
    p.append(
        "report_eco_summary 显示可参与功耗回收的单元数、"
        "已训练/已调整/未训练单元数及面积变化。\n\n"
    )

    p.append(subsection("estimate_eco 命令", "The estimate_eco Command"))
    p.append(
        f"{cmd('estimate_eco')} 在不实际修改网表的情况下估算 ECO 更改的时序影响，"
        "用于 GUI 手动 ECO 或脚本预评估。\n\n"
    )

    p.append(subsection("write_changes 格式选项", "write_changes Format Options"))
    p.append(
        itemize(
            [
                f"{opt('-format icctcl')} — IC Compiler II Tcl 脚本",
                f"{opt('-format verilog')} — Verilog 网表增量",
                f"{opt('-format ptsh')} — PrimeTime Tcl 脚本",
                "第三方 P\\&R 伪 Tcl 格式",
            ]
        )
    )

    p.append(subsection("ECO 变更列表版本与解析", "Change List Version and Parsing"))
    p.append(
        note("变更列表头版本字符串当前为 1.0；解析脚本应检查版本以避免未来格式升级导致意外行为。")
    )

    p.append(subsection("层次化增量 ECO", "Hierarchical Incremental ECO Flow Details"))
    p.append(
        "HyperScale 块级与顶层分别 record_signoff_eco_changes；"
        "增量寄生与增量网表在各自层次应用后验证接口时序。\n\n"
    )

    p.append(subsection("缩减资源 DMSA ECO", "Reduced Resource DMSA ECO"))
    p.append(
        "DMSA 模式下可为各场景创建缩减 ECO 设计，"
        "在场景子集上并行 fix_eco_* 以降低总内存。\n\n"
    )

    p.append(fig("Figure 374", "缩减资源 ECO 流程", "fig:reduced-eco-flow"))

    p.append(subsection("Freeze Silicon 技术规则", "Freeze Silicon Technology Rules"))
    p.append(
        "Freeze silicon 须遵守金属层 ECO 设计规则、"
        "spare cell 映射规则与导出规则（export rules）。\n\n"
    )

    p.append(subsection("ICC II Freeze Silicon 准备", "IC Compiler II ECO Preparation for Freeze Silicon"))
    p.append(
        "在 ICC II 中标记 spare cell、定义 filler 与 ECO 合法化约束，"
        "导出供 PrimeTime freeze silicon ECO 使用。\n\n"
    )

    p.append(subsection("手动插入缓冲器示例", "Manual Buffer Insertion Example"))
    p.append(
        lst(
            "insert_buffer -new_cell_names {eco_buf1} -new_net_names {eco_net1} \\\n"
            "  {driver_pin load_pin1 load_pin2}\n"
            "size_cell cell_instance new_lib_cell\n"
            "remove_buffer buffer_instance"
        )
    )

    p.append(subsection("ECO 与 UPF", "ECO and UPF"))
    p.append(
        "多电压设计中 ECO 须遵守电源域与电平转换规则；"
        "不可修复原因 U 表示 UPF 限制阻止修复。\n\n"
    )

    return "".join(p)
