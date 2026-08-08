# -*- coding: utf-8 -*-
"""Supplemental translated content for chapter 22 (HyperScale / ETM / Budgeting depth)."""
from pt_tex_utils import cmd, fig, itemize, lst, note, opt, subsection, subsubsection


def hyperscale_supplement() -> str:
    p = []
    p.append(subsection("从 ETM 层次化流程迁移", "Moving From an ETM Hierarchical Flow"))
    p.append(
        "若当前使用传统 ETM/ILM 自底向上流程，迁移到 HyperScale 可获得更接近扁平分析的精度，"
        "同时保留层次化运行时间与内存优势。迁移步骤概览：\n"
    )
    p.append(
        itemize(
            [
                "在块级完成布局布线并关闭块内部时序。",
                "运行顶层 HyperScale 分析，characterize_context 并 write_context。",
                "块级读入 context 进行 signoff 级块分析。",
                "迭代顶层与块级直至收敛。",
                "逐步用 HyperScale 块模型替代 ETM 用于顶层 signoff。",
            ],
            env="enumerate",
        )
    )

    p.append(subsubsection("MIM 悲观度", "MIM Pessimism"))
    p.append(
        "多重实例化模块（MIM）中，各实例的时钟到达时间可能不同。"
        "HyperScale 在顶层分析时对 MIM 输出路径施加 mim_pessimism 修正，"
        "将实际时钟到达与最差到达实例之间的差值加回，消除不必要悲观。\n\n"
        "可查询时序路径对象的 mim_pessimism 属性。\n"
    )
    p.append(
        lst(
            "pt_shell> report_timing -path_type full_clock -delay_type max \\\n"
            "  -input_pins -max_paths 1 -sort_by slack\n"
            "# ... 报告中显示 clock reconvergence pessimism 与 MIM pessimism ..."
        )
    )

    p.append(subsubsection("时序降额（Derating）", "Timing Derating"))
    p.append(
        "层次化分析中 OCV/AOCV/POCV 降额在块边界传递须保持一致。"
        "HyperScale 在 write_context/read_context 时保留降额信息；"
        "块级与顶层须使用兼容的降额策略。\n\n"
    )

    p.append(subsubsection("CRPR 与块边界", "CRPR at Block Boundaries"))
    p.append(
        "时钟重汇悲观度移除（CRPR）在 HyperScale 顶层分析中跨块边界计算。"
        "块模型保留接口 CRPR 信息，使顶层 CRPR 信用与扁平分析一致。\n\n"
    )

    p.append(subsubsection("边界检查与违例报告", "Boundary Checks and Violation Reporting"))
    p.append(
        f"{cmd('report_hyperscale_constraints')} 报告块边界上的约束检查，"
        "包括 setup/hold/DRC 在块与顶层的对比、降额窗口类型、"
        "时钟映射引用等。用于调试块/顶层不一致。\n\n"
    )
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{HyperScale 边界检查违例类型}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"违例类型 & 边界检查名称 \\" + "\n"
        r"\midrule" + "\n"
        r"Setup & boundary\_setup\_check \\" + "\n"
        r"Hold & boundary\_hold\_check \\" + "\n"
        r"Max transition & boundary\_transition\_check \\" + "\n"
        r"Max capacitance & boundary\_capacitance\_check \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsubsection("约束提取器限制", "Constraint Extractor Limitations"))
    p.append(
        "约束提取器不支持：UPF 命令、set_ocvm_table_group -type pocvm、"
        "set_si_delay_disable_statistical；SDC 格式不支持 set_clock_sense"
        "（.pt 格式写为 set_sense -type clock）。\n\n"
        "常见错误：HCEXT-004（块内生成时钟定义问题）、UITE-461（生成时钟不可满足）、"
        "PTE-004（生成时钟 pin 在环中或在两个时钟源 fanout 中）。\n\n"
    )

    p.append(subsubsection("反相时钟提取", "Inverted Clock Extraction"))
    p.append(
        "约束提取器识别反相时钟关系并在块级约束中正确写出，"
        "确保块级时钟定义与顶层一致。\n\n"
    )

    p.append(subsubsection("生成块约束与块边界 Context 数据", "Generating Block Constraint and Block Boundary Context Data"))
    p.append(
        "characterize_context 与 write_context 组合可一次性生成块级 SDC 约束与边界 context，"
        "供 HyperScale 块级运行使用。\n\n"
    )

    p.append(subsubsection("在较少主机上并行运行 HyperScale", "Running HyperScale on Fewer Hosts"))
    p.append(
        "大型设计的顶层与多块分析可分布式运行；"
        "通过合理调度块级作业与共享 HyperScale 数据目录降低硬件需求。\n\n"
    )

    return "".join(p)


def etm_supplement() -> str:
    p = []
    p.append(subsection("ETM 分析流程详解", "ETM Analysis Flow in Detail"))
    p.append(fig("Figure 429", "提取时序模型分析", "fig:etm-analysis-flow"))

    p.append(subsubsection("False Path 与 ETM", "False Paths and ETM"))
    p.append(
        "接口逻辑上的 false path 在提取时被尊重；"
        "被例外命令标记的路径不生成对应弧。"
        "块内部 register-to-register false path 不影响 ETM（ETM 仅覆盖接口）。\n\n"
    )

    p.append(subsubsection("时钟门控检查", "Clock-Gating Checks"))
    p.append(
        "extract_model 将时钟门控 setup/hold 检查传播到提取模型的时钟 pin 属性上，"
        "供顶层分析使用。\n\n"
    )

    p.append(subsubsection("反标延迟", "Back-Annotated Delays"))
    p.append(
        "若内部 net 反标了延迟或电容，提取使用反标值而非计算值。"
        "这影响弧延迟精度，须确保块分析时寄生数据完整。\n\n"
    )

    p.append(subsubsection("噪声特性提取", "Noise Characteristics Extraction"))
    p.append(
        "ETM 可包含噪声裕量表，描述块输出在不同负载与转换时间下的噪声容限。\n\n"
    )

    p.append(subsection("ETM 表与变量控制", "ETM Table and Variable Control"))
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{控制 ETM 提取表大小的变量}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}p{0.45\textwidth} p{0.45\textwidth}@{}}" + "\n"
        r"\toprule" + "\n"
        r"变量 & 说明 \\" + "\n"
        r"\midrule" + "\n"
        r"extract\_model\_capacitance\_limit & 输出负载电容扫描上限 \\" + "\n"
        r"extract\_model\_transition\_limit & 输入转换时间扫描上限 \\" + "\n"
        r"extract\_model\_number\_of\_capacitance\_points & 电容索引点数 \\" + "\n"
        r"extract\_model\_number\_of\_transition\_points & 转换时间索引点数 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsection("ETM 裕量与角", "Margin for Block Analysis and Model"))
    p.append(
        "可在提取前对块分析应用裕量，使 ETM 内置保守度。"
        "不同工艺角与模式应分别分析与提取模型。\n\n"
    )

    p.append(subsection("工作条件与分析模式", "Operating Conditions and Analysis Modes"))
    p.append(
        note(
            "每个工艺角与模式须单独执行 update_timing 与 extract_model；"
            "顶层须读入对应角的 ETM 库。"
        )
    )

    p.append(subsection("包装设计与验证", "Wrapper Design Effects"))
    p.append(
        "extract_model -test_design 创建的包装设计中，"
        "须在全部 net 上反标零电阻与零电容以消除线负载延迟：\n"
    )
    p.append(lst("set_resistance 0 [get_nets *]\nset_load 0 [get_nets *]"))

    p.append(subsection("ETM 的 Derating 与 AOCV", "Derating and AOCV in ETM"))
    p.append(
        "若网表分析中应用了降额并纳入 ETM 时序弧，"
        "验证时包装设计与 ETM 不得再次应用相同降额，避免双重降额。\n\n"
        "启用 AOCV 时，验证流程须与提取时 AOCV 设置一致。\n\n"
    )

    p.append(subsection("层次化 Signoff 使用 ETM 的最佳实践", "Best Practices for Hierarchical Signoff With ETMs"))
    p.append(
        itemize(
            [
                "块内部时序必须在提取前关闭。",
                "IP 块周边布置缓冲环，控制端口转换时间范围。",
                "对输入使用 set_driving_cell 与适当 set_load 建模外部环境。",
                "对输出使用保守 load 范围。",
                "使用 write_interface_timing/compare_interface_timing 验证。",
                "最终 signoff 考虑迁移到 HyperScale 或扁平分析确认。",
            ]
        )
    )

    return "".join(p)


def budgeting_supplement() -> str:
    p = []
    p.append(subsection("Budgeting 流程示例", "Context Budgeting Flow Example"))
    p.append(
        "典型三块设计（BLK1—MID—BLK2）中，顶层负 slack 通过 update_budget "
        "按段延迟比例分配到各块接口，生成块级 input/output delay 预算。\n\n"
    )

    p.append(subsubsection("设置块段目标 Slack", "Setting the Target Slack of a Block Segment"))
    p.append(
        f"{cmd('set_timing_budget')} 支持为特定块段指定目标 slack，"
        "覆盖默认比例分配。\n\n"
    )

    p.append(subsubsection("设置块段精确延迟", "Setting the Exact Delay of a Block Segment"))
    p.append(
        "可为块接口指定固定预算延迟，用于已知延迟的互连或硬约束通道。\n\n"
    )

    p.append(subsubsection("设置时钟周期百分比", "Setting the Clock Period Percentage of a Block Segment"))
    p.append(
        "按时钟周期百分比分配段预算，适用于均匀分配时钟周期预算的场景。\n\n"
    )

    p.append(subsubsection("设置最小块段延迟", "Setting a Minimum Block Segment Delay"))
    p.append(
        "保证每段获得最小延迟预算，避免小段被分配过少预算。\n\n"
    )

    p.append(subsubsection("预算规范优先级", "Precedence of Context Budget Specifications"))
    p.append(
        "显式段规范优先于全局 slack_margin；"
        "pin_slack 模式为默认。多种规范同时存在时按文档优先级应用。\n\n"
    )

    p.append(subsection("Budgeting 与层次化块模型", "Hierarchical Analysis Using Block Models With Budgeting"))
    p.append(
        "预算后的 context 可与 ETM/QTM/HyperScale 块模型配合："
        "先 update_budget，再 write_context，块级读入后获得带预算的 I/O 约束。\n\n"
    )

    return "".join(p)


def qtm_supplement() -> str:
    p = []
    p.append(subsection("定义快速时序模型", "Defining a Quick Timing Model"))
    p.append(fig("Figure 451", "块的快速时序模型表示", "fig:qtm-repr"))
    p.append(fig("Figure 452", "快速时序模型分析", "fig:qtm-analysis"))

    p.append(
        "定义 QTM 步骤：\n"
        "1. create_qtm_model 创建模型。\n"
        "2. create_qtm_port 定义输入/输出/时钟端口。\n"
        "3. create_qtm_drive_type 与 set_qtm_port_drive 设置驱动。\n"
        "4. create_qtm_delay_arc 定义组合/时序延迟弧。\n"
        "5. create_qtm_constraint_arc 定义 setup/hold 约束弧。\n"
        "6. save_qtm_model 保存为 .lib 或 .db。\n\n"
    )

    p.append(subsection("在设计中实例化 QTM", "Instantiating a Quick Timing Model in a Design"))
    p.append(
        lst(
            "read_qtm_model my_block_qtm.lib\n"
            "set_link_library \"* my_block_qtm.lib\"\n"
            "link_design top"
        )
    )
    p.append(
        "链接后块实例使用 QTM 替代完整网表，顶层可快速评估接口时序。\n\n"
    )

    p.append(subsection("QTM 全局参数命令", "QTM Global Model Parameters"))
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{QTM 全局模型参数命令}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"命令 & 全局模型参数 \\" + "\n"
        r"\midrule" + "\n"
        r"set\_qtm\_global\_parameter & 设置工艺、温度、电压等 \\" + "\n"
        r"report\_qtm\_model & 报告已定义弧与端口 \\" + "\n"
        r"remove\_qtm\_model & 删除 QTM 定义 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    return "".join(p)


def context_char_supplement() -> str:
    p = []
    p.append(subsection("Context 特征化工作流详解", "Context Characterization Workflow Details"))
    p.append(
        "特征化在 update_timing 期间执行，将顶层时序环境映射到块边界：\n"
    )
    p.append(
        itemize(
            [
                "输入端口：到达时间、转换时间、case 值、串扰 delta",
                "输出端口：要求时间、转换时间、外部负载",
                "时钟端口：时钟定义映射、source latency、网络延迟",
                "侧输入/stub pin：关键路径到达/要求时间",
            ]
        )
    )

    p.append(subsection("Context 文件格式", "Context File Formats"))
    p.append(
        f"{cmd('write_context')} 支持 ptsh 与 sdc 格式。"
        "ptsh 格式保留完整 PrimeTime 语义；sdc 格式便于第三方工具读入。\n\n"
    )

    p.append(subsection("多块 Context 特征化", "Characterizing Multiple Blocks"))
    p.append(
        "一次顶层运行可对多个块 characterize_context；"
        "update_timing 后分别 write_context 到各块目录。\n\n"
    )

    return "".join(p)


def build_supplement() -> str:
    extra = (
        hyperscale_supplement()
        + context_char_supplement()
        + budgeting_supplement()
        + etm_supplement()
        + qtm_supplement()
    )
    # 附加：HyperScale ECO、路径标记、ETM 多电源域、QTM 约束类型
    extra += subsection("HyperScale ECO 流程细节", "HyperScale ECO Flow Details")
    extra += (
        "PrimeTime ECO 与 HyperScale 集成支持顶层 fix_eco_* 与块级 ECO 协同。"
        "顶层 ECO 后须 write_hier_data 更新块 context；块级 ECO 使用最新 context 独立修复。"
        "MIM 实例须一致应用 ECO 变更。可与 IC Compiler、StarRC 增量寄生接口做 signoff ECO。\n\n"
        "并行 ECO：多块可同时运行 ECO 脚本以缩短收敛时间；"
        "各块 write_hier_data 后顶层统一 link_design 与 update_timing。\n\n"
    )
    extra += subsection("HyperScale 路径类型标记", "HyperScale Path Type Markers")
    extra += (
        "report_timing 路径点标记：``@'' 表示顶层施加的约束；``\\&'' 表示块内计算延时；"
        "``I'' 表示 ideal network；``H'' 表示 HyperScale context override。"
        "块级报告跨边界路径时，input external delay 行后的 ``@'' 表示该延时来自顶层分析。\n\n"
    )
    extra += subsection("跨块内电源域合并 ETM", "Merging ETMs Across Block-Internal Power Supplies")
    extra += (
        "多电源域块可按域分别 extract_model 再合并，或单次提取合并模型；"
        "合并时须保证各域接口弧与电平转换器行为正确抽象。"
        "UPF 意图须在块分析中正确加载（load_upf）后再提取。\n\n"
    )
    extra += subsection("QTM 约束弧类型", "QTM Constraint Arc Types")
    extra += (
        "create_qtm_constraint_arc 支持 setup、hold、recovery、removal、"
        "min_pulse_width、minimum_period 等 path_type。"
        "时钟端口与数据端口组合定义寄存器接口约束；"
        "可与 create_qtm_delay_arc 的 max/min 路径类型配合建模建立/保持时间。\n\n"
    )
    extra += subsection("Context 预算模式", "Context Budget Modes")
    extra += (
        "set_timing_budget -mode 支持 pin_slack（默认，按 pin 段 slack 比例分配）、"
        "path_slack（整条路径 slack 分配）等模式。"
        "update_budget 在 update_timing 之后运行一次，根据顶层违例路径调整块边界 input/output delay。\n\n"
    )
    extra += subsection("ETM 与 CCS 数据提取", "Extracting Models With CCS Data")
    extra += (
        "extract_model 可生成含 CCS 时序表的 ETM，提高顶层使用 CCS 延时计算时的精度。"
        "须块分析启用 CCS 且库含 CCS 数据；格式仍可为 .db/.lib。"
        "与 NLDM-only ETM 相比，CCS ETM 文件更大但顶层 RC 分析更准确。\n\n"
    )
    extra += subsection("层次化分析选型指南", "Hierarchical Analysis Selection Guide")
    extra += (
        "流程选型参考：\n"
        r"\begin{itemize}" + "\n"
        r"  \item 早期 RTL/规划 — QTM 或预算约束 + ETM" + "\n"
        r"  \item 块布局后独立收敛 — Context 特征化 + 块级 signoff" + "\n"
        r"  \item 全芯片 signoff — HyperScale 自顶向下或扁平分析" + "\n"
        r"  \item IP 交付 — 保守 ETM + 接口验证脚本" + "\n"
        r"  \item 内存受限大芯片 — HyperScale 多块分治" + "\n"
        r"\end{itemize}" + "\n\n"
    )

    extra += subsection("HyperScale 块 Context 数据类型", "HyperScale Block Context Data Types")
    extra += (
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{Context 数据类型与合并策略（表 66 摘要）}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"数据类型 & MIM 合并取值 \\" + "\n"
        r"\midrule" + "\n"
        r"到达时间 & 各实例最早到达 \\" + "\n"
        r"要求时间 & 各实例最晚要求 \\" + "\n"
        r"转换时间 & 最坏转换 \\" + "\n"
        r"Case 值 & 一致则保留，否则 X \\" + "\n"
        r"串扰 delta & 各实例最坏 \\" + "\n"
        r"时钟映射 & 合并时钟定义 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
        "write_hier_data 写出全部 context 类型；read_context 在块级恢复。"
        "块级分析可禁用部分 context 调整：set_dont_override -include arc_delay/case_value/pin_transition。\n\n"
    )

    extra += subsection("时钟映射检查与修复", "Clock Mapping Check and Fixes")
    extra += (
        "report_constraint -boundary_check -all_violators 列出 clock_mapping、clock_attributes、"
        "clock_uncertainty 等可修复违例。常见修复：块级 create_clock 与顶层周期一致；"
        "set_propagated_clock 匹配 is_propagated 属性；添加 set_clock_uncertainty 匹配顶层。"
        "HyperScale 约束提取器可从扁平约束生成一致块级时钟定义，减少手工映射错误。\n\n"
    )

    extra += subsection("ETM 输入到寄存器与寄存器到输出路径", "ETM Input-to-Register and Register-to-Output Paths")
    extra += (
        "输入到寄存器：提取 setup 弧（最长数据路径+setup）与 hold 弧（最短数据路径+hold）。"
        "寄存器到输出：提取 max/min 两条延迟弧，延时为时钟到输出 pin 的延迟。"
        "输入到输出：组合路径提取 max/min 延迟弧，为输入转换与输出负载的函数。"
        "寄存器到寄存器路径不进入 ETM（仅遍历接口逻辑中的寄存器）。\n\n"
    )

    extra += subsection("ETM 透明锁存器与时间借用", "ETM Transparent Latches and Time Borrowing")
    extra += (
        "extract_model -latch_levels 0/1/2 控制接口透明锁存器级数（默认 2）。"
        "含锁存器接口时须用 write_interface_timing 与 compare_interface_timing 验证借用行为。"
        "顶层使用 ETM 时锁存器借用由模型内约束弧表达。\n\n"
    )

    extra += subsection("ETM 模型验证流程", "ETM Model Validation Flow")
    extra += (
        "推荐验证步骤：\n"
        r"\begin{enumerate}" + "\n"
        r"  \item 块网表 update\_timing 后 write\_interface\_timing 作黄金参考" + "\n"
        r"  \item extract\_model -test\_design 生成含 ETM 实例的包装器" + "\n"
        r"  \item 包装器应用与块分析相同工作条件与约束" + "\n"
        r"  \item compare\_interface\_timing 比较各接口 pin slack（容差约 20 ps）" + "\n"
        r"\end{enumerate}" + "\n\n"
        "不匹配排查：工作条件/分析模式不一致；接口 multicycle；set_max_delay 不支持提取；"
        "包装器未零反标边界 net；driving cell 与集总电容差异；双重 derating。\n\n"
    )

    extra += subsection("QTM 驱动类型与负载", "QTM Drive Types and Loads")
    extra += (
        "create_qtm_drive_type 定义输入驱动（-lib_cell）或输出负载模板；"
        "set_qtm_port_drive 将驱动类型关联到端口。"
        "create_qtm_port -type bidirectional 建模 inout；时钟端口用于约束弧 reference。"
        "save_qtm_model -format lib 生成 Liberty 供 link_design 使用。\n\n"
    )

    extra += subsection("Context 预算自定义示例", "Context Budget Customization Example")
    extra += (
        lst(
            "characterize_context -block block1 -instances BLK1\n"
            "characterize_context -block block2 -instances BLK2\n"
            "update_timing\n"
            "set_timing_budget -mode pin_slack -slack_margin 0.1\n"
            "set_timing_budget -through BLK1/Z -target_slack 0.5\n"
            "update_budget\n"
            "report_budget -through BLK1/Z\n"
            "write_context -format ptsh -output BLK1_budgeted"
        )
    )

    extra += subsection("HyperScale 与 SI 分析", "HyperScale and SI Analysis")
    extra += (
        "HyperScale 顶层与块级均支持 update_noise 与耦合延时分析。"
        "块 context 包含端口级串扰 aggressor 信息；块级读入 context 后 SI 分析与顶层一致。"
        "写 context 时保留无限窗口 aggressor 设置以确保保守 SI 边界。\n\n"
    )

    extra += subsection("report_hier_analysis 报告", "Reporting HyperScale Configuration")
    extra += (
        r"\cmd{report\_hier\_analysis} 默认报告块名、时间戳、HyperScale 路径。"
        "可报告额外信息：链接状态、MIM 配置、context 时间戳等。"
        "若路径或数据错误，须退出会话、修正 set_hier_config 后重新 link_design。\n\n"
    )

    extra += subsection("块边界自动调整机制", "Block Boundary Automatic Adjustment")
    extra += (
        "顶层 HyperScale 分析后，块级 read_context 可自动调整用户边界约束："
        "输入/输出 delay、set_case_analysis、端口转换时间、时钟不确定性等。"
        "不可解析的违例须用户修正块约束；set_dont_override 可抑制特定类型自动调整。"
        "该机制使块级在顶层真实环境下收敛，无需手工复制顶层到达/要求时间。\n\n"
    )

    extra += subsection("ETM 噪声与功耗选项", "ETM Noise and Power Options")
    extra += (
        r"\cmd{extract\_model -noise} 在模型中包含噪声特性；\cmd{-power} 包含功耗信息。"
        r"\cmd{-format db} 供 Synopsys 工具直接使用；\cmd{-format lib} 便于审阅与第三方兼容。"
        "提取前 check_timing 与 report_constraint 确保无违例；"
        "多模式设计按 mode 分别提取后合并或分角使用。\n\n"
    )

    extra += subsection("QTM 与 HyperScale/ETM 选型", "When to Use QTM Versus ETM Versus HyperScale")
    extra += (
        "QTM 适用于早期架构探索与接口预算估算，创建快但精度低。"
        "ETM 适用于 IP 交付与顶层集成，须完整实现网表与保守边界约束。"
        "HyperScale 适用于 signoff 级层次化分析，保留块内部网表精度并降低顶层容量。"
        "成熟流程通常：QTM（早期）→ ETM（中期）→ HyperScale（signoff）或扁平分析。\n\n"
        "无论采用何种块抽象，块内部时序必须在抽象前闭合；"
        "顶层仅对块接口施加环境约束，不能替代块内 signoff。"
        "层次化团队应约定 HyperScale 数据目录命名、时间戳检查与 context 版本管理规范。"
        "块级与顶层脚本应分离但共享 characterize_context 写出目录，避免时钟映射与约束漂移。"
        "signoff 前建议对关键跨块路径做扁平与 HyperScale 结果对比抽样验证，"
        "确认块模型与 context 未引入系统性悲观或乐观。"
        "对含多电源域与 DVFS 的设计，须在块与顶层使用一致的 SMVA 电压场景与二进制 context 格式。\n\n"
    )

    return extra
