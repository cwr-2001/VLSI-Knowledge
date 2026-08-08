# -*- coding: utf-8 -*-
"""Generate chapters/21_eco_flow.tex — PrimeTime UG Ch.21 ECO Flow."""
from pathlib import Path

from ch21_supplement import build_supplement as ch21_extra
from pt_tex_utils import (
    chapter_header,
    cmd,
    count_cjk,
    fig,
    itemize,
    lst,
    note,
    opt,
    section,
    see_also,
    subsubsection,
    subsection,
    write_tex,
)

OUT = Path(__file__).resolve().parent.parent / "chapters" / "21_eco_flow.tex"


def build() -> str:
    p: list[str] = []
    p.append(chapter_header(21, "ECO 流程", "ECO Flow", "chap:eco"))

    p.append(
        "若设计存在时序、设计规则或噪声违例，或需优化面积/功耗，"
        "可使用工程变更指令（ECO）流程修复违例、实现更改并重新运行时序分析。\n"
    )
    p.append(
        itemize(
            [
                "ECO 修复概述",
                "设置 ECO 选项",
                "物理感知 ECO",
                "ECO 修复方法",
                "报告不可修复违例与不可用单元",
                "HyperTrace ECO 修复",
                "写入变更列表",
                "在 Synopsys 布局工具中实现 ECO 更改",
                "使用 Synopsys 工具的增量 ECO 流程",
                "使用缩减资源的 ECO 流程",
                "Freeze Silicon ECO 流程",
                "在较少主机上运行 ECO 场景",
                "手动网表编辑",
            ]
        )
    )

    # --- Overview ---
    p.append(section("ECO 修复概述", "ECO Fixing Overview"))
    p.append(
        "在 PrimeTime 中，工程变更指令（ECO）是对芯片设计的增量更改，"
        "用于修复时序违例或设计规则约束（DRC）违例，或降低功耗。"
        "PrimeTime 发现这些问题并通过调整单元尺寸、替换单元或插入缓冲器进行纠正，"
        "并以脚本格式写出更改，以便在其他工具中实现。\n\n"
        "执行 ECO 修复的命令：\n"
    )
    p.append(
        itemize(
            [
                cmd("fix_eco_drc"),
                cmd("fix_eco_timing"),
                cmd("fix_eco_power"),
            ]
        )
    )
    p.append(
        f"ECO 修复完成后，使用 {cmd('write_changes')} 写出更改，"
        "在 IC Compiler II 等物理实现工具中运行脚本。"
        "实现更改后应重新进行寄生提取并在 PrimeTime 中再次分析。\n\n"
        "PrimeTime 可在有或没有物理布局数据的情况下执行 ECO 修复：\n"
    )
    p.append(
        itemize(
            [
                "仅逻辑模式 — 仅使用设计网表与详细寄生数据，不考虑物理布局。",
                "物理感知模式 — 使用网表、寄生数据与物理布局；"
                "仅在有余量处替换单元/插入缓冲器；"
                f"{cmd('write_changes')} 写出每个更改的位置以实现快速准确物理实现。",
            ]
        )
    )
    p.append(
        "ECO 修复流程兼容单核、多核与分布式多场景分析（DMSA）。"
        "为降低内存、运行时间与周转时间，可使用：\n"
    )
    p.append(
        itemize(
            [
                "缩减资源 ECO 流程 — 在全设计上做时序分析，但在较小“缩减”设计上做 ECO。",
                "Synopsys 增量 ECO 流程 — 用 Synopsys 工具实现更改，每步仅写出/分析变更部分。",
            ]
        )
    )
    p.append(
        note(
            "尝试 ECO 修复前，确保设计已完全布局布线并生成时钟树；"
            "使用物理感知 ECO 以获得最佳结果质量。"
        )
    )

    p.append(subsection("DRC、串扰与单元电迁移违例修复", "DRC, Crosstalk, and Cell Electromigration Violation Fixing"))
    p.append(
        f"修复 DRC、噪声、串扰延迟或单元电迁移违例，使用 {cmd('fix_eco_drc')}。"
        "它修复以下命令报告的违例：\n"
    )
    p.append(
        lst(
            "report_constraint -max_capacitance ...\n"
            "report_constraint -max_transition ...\n"
            "report_constraint -max_fanout ...\n"
            "report_noise ...\n"
            "report_cell_em_violation ..."
        )
    )
    p.append(
        "修复机制包括缓冲器插入、单元尺寸调整、负载屏蔽（load shielding）等。\n\n"
    )

    p.append(subsubsection("串扰 Delta 延迟修复", "Crosstalk Delta Delay Fixing"))
    p.append(
        f"{cmd('fix_eco_drc')} 可修复由串扰引起的 delta delay 违例，"
        "与 SI 分析结果协同工作。\n\n"
    )

    p.append(subsubsection("SI 瓶颈优化与报告", "SI Bottleneck Optimization and Reporting"))
    p.append(
        "可识别并优化导致串扰问题的瓶颈网络，"
        f"使用相关报告命令分析修复前后 SI 影响。\n\n"
    )

    p.append(subsection("时序违例修复", "Timing Violation Fixing"))
    p.append(
        f"使用 {cmd('fix_eco_timing')} 修复 setup 与 hold 违例。"
        "支持按违例类型（setup/hold）、目标（WNS/TNS）、"
        "修复方法（insert_buffer、size_cell、remove_buffer 等）配置。\n\n"
    )

    p.append(subsection("功耗回收修复", "Power Recovery Fixing"))
    p.append(
        f"使用 {cmd('fix_eco_power')} 在不引入新时序或 DRC 违例的前提下回收漏电功耗，"
        "通过单元尺寸调整、阈值电压交换等方式。\n\n"
        f"功耗回收后，用 {cmd('write_changes')} 写出设计更改。\n\n"
    )

    p.append(subsection("ECO 修复步骤顺序", "Order of ECO Fixing Steps"))
    p.append("推荐 ECO 修复顺序：\n")
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{ECO 修复步骤、命令与优先级}" + "\n"
        r"\small" + "\n"
        r"\begin{tabularx}{\textwidth}{@{}l l X X@{}}" + "\n"
        r"\toprule" + "\n"
        r"步骤 & 命令 & 修复机制 & 优先级规则 \\" + "\n"
        r"\midrule" + "\n"
        r"Step 1: 功耗回收 & \texttt{fix\_eco\_power} & 单元尺寸、缓冲器 & 不引入新时序/DRC \\" + "\n"
        r"Step 2: DRC 修复 & \texttt{fix\_eco\_drc} & 缓冲器插入、单元尺寸 & 会改变 setup/hold slack \\" + "\n"
        r"Step 3: 时序修复 & \texttt{fix\_eco\_timing} & 缓冲器插入、单元尺寸 & setup 修复遵守 DRC \\" + "\n"
        r"Step 4: 最终漏电 & \texttt{fix\_eco\_power} & 阈值电压 & 不引入新时序/DRC \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabularx}" + "\n"
        r"\end{table}" + "\n\n"
    )

    # --- ECO Options ---
    p.append(section("设置 ECO 选项", "Setting the ECO Options"))
    p.append(
        f"使用 {cmd('set_eco_options')} 配置 ECO 行为，包括物理数据路径、"
        "可用单元库、修复策略、并行度等。\n\n"
        f"使用 {cmd('report_eco_options')} 查看当前设置；"
        f"{cmd('reset_eco_options')} 恢复默认。\n\n"
    )

    p.append(subsection("多库配置", "Configuring the ECO for Multiple Libraries"))
    p.append(
        "若工具须区分多个逻辑等效库，可指定库优先级与排除规则。"
        f"用 {cmd('set_eco_options')} 的库相关选项配置。\n"
        f"用 {opt('-exclude')} 相关变量从设计特定部分排除库单元。\n\n"
    )

    p.append(subsection("电源管理单元尺寸调整", "Resizing Power Management Cells"))
    p.append(
        "默认 ECO 可能不调整电源管理单元；"
        f"可通过 {cmd('set_eco_options')} 允许在功耗回收期间考虑这些单元。\n\n"
    )

    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{常用 ECO 相关命令}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"命令 & 说明 \\" + "\n"
        r"\midrule" + "\n"
        rf"\texttt{{set\_eco\_options}} & 设置 ECO 选项（物理路径、单元列表等） \\" + "\n"
        rf"\texttt{{report\_eco\_options}} & 报告当前 ECO 选项 \\" + "\n"
        rf"\texttt{{check\_eco}} & 检查物理数据是否可用于 ECO \\" + "\n"
        rf"\texttt{{fix\_eco\_timing}} & 修复时序违例 \\" + "\n"
        rf"\texttt{{fix\_eco\_drc}} & 修复 DRC/SI/EM 违例 \\" + "\n"
        rf"\texttt{{fix\_eco\_power}} & 功耗回收 \\" + "\n"
        rf"\texttt{{write\_changes}} & 写出 ECO 变更列表 \\" + "\n"
        rf"\texttt{{estimate\_eco}} & 估算 ECO 更改的时序影响 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    # --- Physically Aware ECO ---
    p.append(section("物理感知 ECO", "Physically Aware ECO"))
    p.append(
        "物理感知 ECO 流程整合静态时序、SI 分析、ECO 变更列表、"
        "寄生数据与 StarRC 寄生提取，在考虑物理布局约束的情况下生成可实现的 ECO。\n\n"
    )
    p.append(fig("Figure 358", "Synopsys 物理感知 ECO 流程", "fig:phys-eco-flow"))

    p.append(subsection("执行物理感知 ECO", "Performing Physically Aware ECO"))
    p.append(
        "物理 ECO 所需设计数据文件：\n"
    )
    p.append(
        r"\begin{longtable}{@{}p{0.28\textwidth} p{0.65\textwidth}@{}}" + "\n"
        r"\toprule" + "\n"
        r"数据类型 & 说明 \\" + "\n"
        r"\midrule" + "\n"
        r"SPEF/GPD 寄生 & 须含位置信息；可用 StarRC 从 ICC II 生成 \\" + "\n"
        r"块级 LEF 库 & 来自 ICC II 数据库或 Milkyway \\" + "\n"
        r"DEF / ICC II 数据库 & 布局与布线信息 \\" + "\n"
        r"物理约束文件 & 含高级间距标签与规则 \\" + "\n"
        r"StarRC 寄生文件 & 与物理布局一致的寄生 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{longtable}" + "\n\n"
    )

    p.append(
        "配置示例：\n"
    )
    p.append(
        lst(
            "set_eco_options -physical_design_path design.def \\\n"
            "  -physical_tech_lib_path tech.lef \\\n"
            "  -physical_lib_path stdcells.lef"
        )
    )

    p.append(subsection("站点感知物理 ECO 修复", "Site-Aware Physical ECO Fixing"))
    p.append(
        "PrimeTime 物理感知 ECO 可识别单高度与双高度 site row，"
        "在合法 site 上放置 ECO 单元。\n\n"
    )
    p.append(fig("Figure 360", "常规单高度与双高度 site row", "fig:site-rows"))
    p.append(fig("Figure 361", "偏移单高度与双高度 site row", "fig:offset-site-rows"))

    p.append(subsection("多电压物理约束", "Multivoltage Physical Constraints"))
    p.append(
        "物理 ECO 可处理多电压域的电压岛、电平转换器与隔离单元约束。\n\n"
    )
    p.append(fig("Figure 359", "多电压物理约束示例", "fig:mv-phys-constraint"))

    # --- Fixing Methods ---
    p.append(section("ECO 修复方法", "ECO Fixing Methods"))
    p.append(subsection("负载缓冲与负载屏蔽", "Load Buffering and Load Shielding"))
    p.append(
        "负载缓冲（load buffering）在关键负载前插入缓冲器以加速网络；"
        "负载屏蔽在受害网络附近插入缓冲器隔离串扰 aggressor。\n\n"
    )
    p.append(fig("Figure 362", "负载缓冲示例", "fig:load-buffering"))
    p.append(fig("Figure 363", "负载屏蔽示例", "fig:load-shielding"))

    p.append(subsection("时钟网络 ECO 修复", "Clock Network ECO Fixing"))
    p.append(
        f"在时钟网络中插入缓冲器修复 hold 违例时，"
        f"{cmd('fix_eco_timing')} 支持 "
        f"{opt('-cell_type clock_network')} 与 "
        f"{opt('-methods {insert_buffer}')}。\n\n"
        "需注意 setup/hold 权衡：时钟网络缓冲可能改善部分路径 hold 但恶化其他路径 setup。\n\n"
    )

    p.append(subsection("TNS 驱动的时钟网络时序 ECO", "TNS-Driven Clock Network Timing ECO"))
    p.append(
        f"使用 {opt('-target_violation_type tns')} 以 TNS 为目标修复；"
        f"{opt('-wns_limit')} 限制 WNS 恶化程度。\n\n"
        "图 365--367 示例说明：默认不允许因修复而恶化其他路径 hold；"
        "TNS 模式可在 WNS 限制内权衡多条路径。\n\n"
    )
    p.append(fig("Figure 365", "负 hold slack 示例", "fig:hold-neg"))
    p.append(fig("Figure 366", "TNS 驱动 hold 修复（默认 WNS 限制）", "fig:tns-hold-default"))
    p.append(fig("Figure 367", "TNS 驱动 hold 修复（显式 WNS 限制）", "fig:tns-hold-explicit"))

    p.append(subsection("使用负载电容单元进行 Hold 修复", "ECO Hold Fixing Using Load Capacitance Cells"))
    p.append(
        f"{cmd('fix_eco_timing')} {opt('-type hold')} 可在数据路径插入负载电容单元。"
        "对小 hold 违例（约 5 ps 以内）比最小缓冲器更精确，避免 over-fix。\n\n"
        "专用负载单元属性：function_id=unknown、is_black_box=true、number_of_pins=1。\n\n"
    )
    p.append(fig("Figure 368", "缓冲器插入与负载单元插入进行 hold 修复", "fig:load-cell-hold"))

    p.append(subsection("基于库单元名的功耗回收", "Power Recovery Based on Library Cell Names"))
    p.append(
        "可指定高漏电与低漏电单元对进行阈值电压或尺寸交换。\n\n"
    )

    p.append(subsection("基于库单元字符串属性的功耗回收", "Power Recovery Based on a Library Cell String Attribute"))
    p.append(
        "通过用户定义属性标记可交换单元组，"
        f"{cmd('fix_eco_power')} 按属性匹配进行功耗优化。\n\n"
    )

    p.append(subsection("用户脚本 ECO 机器学习", "User-Scripted ECO Machine Learning"))
    p.append(
        "支持基于机器学习的功耗回收加速，"
        "训练单元替换模型以在保持时序前提下降低漏电。\n\n"
    )

    p.append(subsection("MIM 的 ECO", "ECOs With Multiply Instantiated Modules (MIMs)"))
    p.append(
        "对多重实例化模块，ECO 更改须在所有实例间一致应用；"
        f"使用 HyperScale MIM 流程与相应 {cmd('write_changes')} 选项。\n\n"
    )

    # --- Reporting ---
    p.append(section("报告不可修复违例与不可用单元", "Reporting Unfixable Violations and Unusable Cells"))
    p.append(
        f"ECO 完成后使用 {cmd('report_eco_summary')} 查看修复统计。"
        f"{cmd('report_eco_unfixed')} 列出无法修复的违例及原因代码：\n"
    )
    p.append(
        itemize(
            [
                "T — 时序裕量过紧无法修复",
                "U — UPF 限制修复",
                "W — 修复可能恶化 DRC",
                "X — 单元对 ECO 不可用",
                "Z — 单元已被调整尺寸",
            ]
        )
    )

    # --- HyperTrace ---
    p.append(section("HyperTrace ECO 修复", "HyperTrace ECO Fixing"))
    p.append(
        "HyperTrace 加速 ECO 路径分析，在大型设计上缩短 "
        f"{cmd('fix_eco_timing')} 与 {cmd('fix_eco_power')} 运行时间。\n\n"
        "配置 HyperTrace ECO 相关应用变量以启用路径追踪优化。\n\n"
    )

    # --- Change Lists ---
    p.append(section("写入变更列表", "Writing Change Lists"))
    p.append(
        f"使用 {cmd('write_changes')} 将 ECO 更改写出为脚本，供 ICC II 或其他 P\\&R 工具读入。\n\n"
        f"常用格式：{opt('-format icctcl')}、{opt('-format verilog')}、第三方格式等。\n\n"
    )

    p.append(subsubsection("在 PrimeTime 中回放 ECO 变更列表", "Replaying an ECO Change List in PrimeTime"))
    p.append(
        f"可用 {cmd('source')} 读入变更列表验证或增量更新时序。\n\n"
    )

    p.append(subsubsection("在顶层运行中回放块级 ECO 更改", "Replaying Block-Level ECO Changes in a Top-Level Run"))
    p.append(
        "HyperScale 流程中，块级 ECO 可在顶层会话中回放并验证接口时序。\n\n"
    )

    p.append(subsubsection("为第三方 P\\&R 工具写入 ECO 变更列表", "Writing ECO Change Lists for Third-Party Place-and-Route Tools"))
    p.append(
        "支持 pseudo-Tcl 语法描述 insert_buffer、size_cell、create_cell、connect_net 等操作。\n\n"
        "变更列表文件头含版本字符串（当前为 1.0），解析脚本应检查版本。\n\n"
    )
    p.append(
        lst(
            "insert_buffer -on_route BUFFD4 \\\n"
            "  -new_net_names {net1} -new_cell_names {BUF1} \\\n"
            "  -location {x1 y1} -route_cut_location {x1' y1'} \\\n"
            "  {sink1/I sink2/I sink3/I sink4/I}"
        )
    )

    # --- Implementing in Layout Tools ---
    p.append(section("在 Synopsys 布局工具中实现 ECO 更改", "Implementing ECO Changes in Synopsys Layout Tools"))
    p.append(
        note(
            "若有 PrimeECO 许可证，可在单 shell 环境中完成 ECO 物理实现、"
            "寄生提取与 signoff 时序分析。详见 PrimeECO User Guide。"
        )
    )
    p.append(
        "使用独立 Synopsys 工具的步骤：\n"
        "1. PrimeTime：\n"
    )
    p.append(lst("write_changes -format icctcl new_change_list_file"))
    p.append(
        "2. IC Compiler II：source 变更列表，"
        f"{cmd('place_eco_cells')}、{cmd('create_stdcell_fillers')}、{cmd('route_eco')}。\n"
        "3. StarRC：寄生提取。\n"
        "4. PrimeTime：读入更新网表与寄生，重新分析。\n"
        "5. 验证 QoR，按需迭代。\n\n"
    )

    # --- Incremental ECO ---
    p.append(section("使用 Synopsys 工具的增量 ECO 流程", "Incremental ECO Flow Using Synopsys Tools"))
    p.append(
        "与全网表/全寄生 ECO 流程相比，增量 ECO 流程中：\n"
    )
    p.append(
        itemize(
            [
                "IC Compiler II 实现 ECO 并仅写出增量更改。",
                "StarRC 仅提取增量物理更改并写出增量寄生文件。",
                "PrimeTime 将增量寄生应用于恢复的会话并验证修改后设计时序。",
            ]
        )
    )
    p.append(fig("Figure 372", "Synopsys 增量 ECO 流程", "fig:incr-eco-flow"))
    p.append(fig("Figure 373", "Synopsys 增量 ECO 流程步骤", "fig:incr-eco-steps"))

    p.append(subsection("初始化增量 ECO 流程", "Initialize the Incremental ECO Flow"))
    p.append(
        "1. ICC II：打开库、复制块、初始化 ECO 数据库：\n"
    )
    p.append(
        lst(
            "icc2_shell> open_lib Design.nlib\n"
            "icc2_shell> copy_block -from_block Block -to_block Block_pre_eco\n"
            "icc2_shell> open_block Block_pre_eco\n"
            "icc2_shell> record_signoff_eco_changes -init -def"
        )
    )
    p.append("2. StarRC：ECO 模式与增量网表模式寄生提取。\n")
    p.append("3. PrimeTime：全设计基线时序更新、save_session、执行初始 ECO。\n\n")

    p.append(subsection("增量 ECO 迭代", "Incremental ECO Iteration"))
    p.append(
        "初始化后每轮迭代：ICC II 实现 PrimeTime 写出的更改并跟踪增量；"
        "StarRC 增量提取；PrimeTime restore_session 并应用增量寄生。\n\n"
    )

    p.append(subsection("层次化增量 ECO 流程", "Hierarchical Incremental ECO Flow"))
    p.append(
        "HyperScale 块级与顶层可分别进行增量 ECO，"
        "通过 record_signoff_eco_changes 协调跨层次更改。\n\n"
    )

    # --- Reduced Resources ---
    p.append(section("使用缩减资源的 ECO 流程", "ECO Flow Using Reduced Resources"))
    p.append(
        "在全设计时序分析后，创建仅含违例相关逻辑的缩减设计进行 ECO，"
        "降低内存与运行时间。支持 DMSA 与非 DMSA 模式。\n\n"
    )
    p.append(subsection("缩减资源非 DMSA ECO 流程", "Reduced Resource Non-DMSA ECO Flow"))
    p.append(
        f"使用 {cmd('create_eco_scenario')} 与相关命令创建缩减场景，"
        "在缩减设计上执行 fix_eco_* 命令。\n\n"
    )

    # --- Freeze Silicon ---
    p.append(section("Freeze Silicon ECO 流程", "Freeze Silicon ECO Flow"))
    p.append(
        "Freeze silicon ECO 在已流片硅片上通过备用单元（spare cell）实现逻辑更改。"
        "需特殊物理规则、导出规则与技术约束。\n\n"
    )
    p.append(subsection("准备 Freeze Silicon ECO 流程", "Preparing for the Freeze Silicon ECO Flow"))
    p.append(
        "ICC II 中准备 spare cell、填充单元与 ECO 合法化规则；"
        "PrimeTime 中配置 freeze silicon 相关 ECO 选项。\n\n"
    )
    p.append(subsection("PrimeTime 中的 Freeze Silicon ECO", "Freeze Silicon ECO in PrimeTime"))
    p.append(
        f"使用专用 {cmd('fix_eco_*')} 选项与 {cmd('write_changes')} 格式，"
        "将逻辑映射到 spare cell 并实现金属层 ECO。\n\n"
    )

    # --- DMSA on fewer hosts ---
    p.append(section("在较少主机上运行 ECO 场景", "Running ECO Scenarios on Fewer Hosts"))
    p.append(
        "优化 DMSA ECO 脚本以在有限主机上更快完成："
        "合并场景、调整并行度、使用场景优先级。\n\n"
    )
    p.append(subsection("优化 DMSA ECO 脚本以加快周转", "Optimizing DMSA ECO Scripts for Faster Turnaround"))
    p.append(
        "减少场景镜像交换、批量 fix_eco 命令、复用物理数据路径等最佳实践。\n\n"
    )

    # --- Manual Netlist Editing ---
    p.append(section("手动网表编辑", "Manual Netlist Editing"))
    p.append(
        "除自动 ECO 外，可手动编辑网表：\n"
    )
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{手动网表编辑任务与命令}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"对象 & 任务 / 命令 \\" + "\n"
        r"\midrule" + "\n"
        rf"单元 & 尺寸调整：\texttt{{size\_cell}}；创建：\texttt{{create\_cell}} \\" + "\n"
        rf"网络 & 连接：\texttt{{connect\_pin}} / \texttt{{disconnect\_pin}} \\" + "\n"
        rf"缓冲器 & 插入：\texttt{{insert\_buffer}}；删除：\texttt{{remove\_buffer}} \\" + "\n"
        rf"负载 & 插入负载电容单元：\texttt{{create\_cell}} + \texttt{{connect\_net}} \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsection("GUI 中的单元尺寸调整与缓冲器插入", "Sizing Cells and Inserting Buffers in the GUI"))
    p.append(
        "在布局视图中可通过 ECO 菜单交互式 size cell 与 insert buffer，"
        "支持 on-route 放置引导与即时增量时序更新（见第~\\ref{chap:gui}~章）。\n\n"
    )

    p.append(ch21_extra())

    p.append(see_also(["第~\\ref{chap:gui}~章 Layout View 与 GUI ECO", "PrimeECO User Guide"]))

    return "".join(p)


def main() -> None:
    text = build()
    size = write_tex(OUT, [text])
    cjk = count_cjk(text)
    print(f"Wrote {OUT}")
    print(f"Size: {size:,} bytes")
    print(f"CJK characters: {cjk:,}")


if __name__ == "__main__":
    main()
