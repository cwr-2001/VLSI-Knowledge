# -*- coding: utf-8 -*-
"""Generate 22_hierarchical.tex — Chapter 22 Hierarchical Analysis."""
from pathlib import Path

from ch22_supplement import build_supplement as ch22_extra
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

OUT = Path(__file__).resolve().parent.parent / "chapters" / "22_hierarchical.tex"


def build() -> str:
    p: list[str] = []
    p.append(chapter_header(22, "层次化分析", "Hierarchical Analysis", "chap:hier"))

    p.append(
        "对于大型芯片设计，从顶层层次进行扁平时序分析可能消耗大量内存或运行时间。"
        "可采用层次化分析，使每次分析运行仅针对整片芯片的一部分。"
        "要学习层次化分析，请参阅：\n"
    )
    p.append(
        itemize(
            [
                "层次化分析概述",
                "HyperScale 分析",
                "Context 特征化",
                "Context 预算（Budgeting）",
                "提取时序模型（ETM）",
                "快速时序模型（QTM）",
            ]
        )
    )

    # ===== Overview =====
    p.append(section("层次化分析概述", "Overview of Hierarchical Analysis"))
    p.append(
        "大型设计的分析可能消耗大量内存或运行时间。"
        "层次化分析使每次运行仅针对芯片一部分。\n\n"
        "PrimeTime 提供以下层次化分析特性：\n"
    )
    p.append(
        itemize(
            [
                "HyperScale 分析 — 先进技术，分别分析块级与顶层部分，"
                "准确处理顶层与下级块之间的时序接口；"
                "在块级分析的缩减运行时间与内存占用下获得接近全扁平分析的精度。",
                "Context 特征化 — 写出块在顶层内的时序 context，"
                "使块可脱离顶层单独分析并仍获得在顶层 context 下工作的准确时序。",
                "提取时序模型（ETM） — 直接从下级块网表提取的块时序模型，"
                "由时钟、输入与输出 pin 之间的时序弧组成；可移植并导出到其他工具。",
                "快速时序模型（QTM） — 用一组 PrimeTime 命令指定输入、"
                "输出与约束以创建简化时序模型，用于早期层次化分析。",
            ]
        )
    )
    p.append(fig("Figure 381", "层次化分析流程", "fig:hier-flows"))

    p.append(subsection("何时使用扁平与层次化分析", "When to Use Flat vs Hierarchical Analysis"))
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{扁平全芯片分析与 HyperScale 层次化分析对比}" + "\n"
        r"\begin{tabularx}{\textwidth}{@{}X X@{}}" + "\n"
        r"\toprule" + "\n"
        r"扁平全芯片分析 & HyperScale 层次化分析 \\" + "\n"
        r"\midrule" + "\n"
        r"最终 signoff、最佳顶层性能 & 大型设计、内存/运行时间受限 \\" + "\n"
        r"整片同时分析 & 块级与顶层分别运行 \\" + "\n"
        r"无需块模型 & 使用 HyperScale 块模型与 context \\" + "\n"
        r"替代旧 ILM 流程 & 支持自底向上、自顶向下与混合流程 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabularx}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(
        "典型层次化流程包括：生成块级约束 → 块级分析 → 顶层 HyperScale 分析 → 时序收敛迭代。\n\n"
    )

    # ===== HyperScale =====
    p.append(section("HyperScale 分析", "HyperScale Analysis"))
    p.append(
        "HyperScale 技术分别对块级与顶层部分进行分析，"
        "准确处理块接口时序，在层次化运行时间与内存下接近扁平分析精度。\n\n"
        "PrimeTime HyperScale 层次化分析方法的主要优势：\n"
    )
    p.append(
        itemize(
            [
                "运行时间与容量 — 相比扁平全芯片分析，HyperScale 将分析拆分为多次较小运行，显著降低内存与运行时间。",
                "精度 — 与扁平分析执行相同延时计算、POCV/AOCV 与耦合/非耦合 SI 分析，在块接口保持完整精度。",
                "高效顶层分析 — 自动记录并缩减顶层需分析的块内部逻辑，仅保留接口时序信息。",
                "自动 context 更新 — 顶层与块级迭代时自动更新并传递块边界条件。",
                "ECO 指导 — HyperScale 信息指导时序 ECO，支持顶层与块级协同修复。",
                "约束管理 — 在块级收敛时序，顶层使用 HyperScale 块模型；支持约束提取保证块级与顶层一致。",
            ]
        )
    )
    p.append(
        "大型芯片可跨多个层次级。HyperScale 可在每一级分别分析下级块与当前级，"
        "“顶层”可指包含一个或多个下级块的任意分析级。\n\n"
    )
    p.append(fig("Figure 382", "扁平分析与 HyperScale 层次化分析对比", "fig:flat-vs-hs"))
    p.append(fig("Figure 383", "跨多层次的层次化分析", "fig:hs-multi-level"))

    p.append(subsection("HyperScale 关键技术特性", "Key HyperScale Technology Features"))
    p.append(
        itemize(
            [
                "HyperScale 建模 — 块以 HyperScale 模型表示，保留接口路径、约束与 CRPR 信息。",
                "HyperScale 块 Context — 顶层向块传递边界条件（到达/要求时间、转换时间、case 值、串扰数据等）。",
                "多重实例化模型（MIM） — 对多重实例化模块合并 context。",
                "上下文覆盖（Context Override） — 块级运行中根据顶层 context 调整边界。",
            ]
        )
    )
    p.append(
        "HyperScale 块模型包含以下逻辑类型：输入到寄存器、寄存器到输出、输入到输出、"
        "时钟路径、接口锁存器与时间借用、最小脉冲宽度/周期检查、噪声与 SI 相关逻辑。"
        "模型包含准确时序分析所需的全部接口逻辑。\n\n"
    )
    p.append(
        lst(
            "set_app_var hier_enable_analysis true\n"
            "read_verilog block.v\n"
            "link_design block\n"
            "read_parasitics block.spef\n"
            "source block.sdc\n"
            "update_timing -full\n"
            "write_hier_data $blkDir"
        )
    )
    p.append(fig("Figure 384", "HyperScale 块模型", "fig:hs-block-model"))
    p.append(fig("Figure 385", "HyperScale 块 Context", "fig:hs-block-context"))
    p.append(fig("Figure 386", "多重实例化模块的 Context 合并", "fig:mim-context-merge"))

    p.append(subsection("HyperScale 使用流程", "HyperScale Usage Flows"))
    p.append(
        "支持自顶向下、自底向上与混合流程：\n"
    )
    p.append(fig("Figure 387", "HyperScale 分析流程", "fig:hs-usage-flows"))
    p.append(fig("Figure 389", "HyperScale 自顶向下与自底向上流程", "fig:hs-td-bu"))
    p.append(fig("Figure 390", "HyperScale 自顶向下流程", "fig:hs-td-flow"))
    p.append(fig("Figure 391", "HyperScale 自底向上流程", "fig:hs-bu-flow"))

    p.append(subsubsection("无 Context 的块模型自底向上分析", "Bottom-Up Analysis Using Block Models Without Context"))
    p.append(
        "自底向上无 context 建模中，用预算约束分析块时序，生成 HyperScale 块模型供顶层使用。"
        "比 ETM 更准确（保留块内部网表与接口逻辑），顶层性能与容量优于带 context 的完整流程，"
        "但精度低于自顶向下带 context 流程。\n\n"
    )
    p.append(subsubsection("从 ETM 层次化流程迁移", "Moving From an ETM Hierarchical Flow"))
    p.append(
        "已有 ETM 层次化流程可少量修改脚本转为 HyperScale 以获得更高精度："
        "块级用 \cmd{write\_hier\_data} 替代 \cmd{extract\_model}；"
        "顶层用 HyperScale 块模型路径替代 ETM .lib/.db 路径；"
        "可用 \cmd{read\_context} 读入已有顶层 context（若可用）。\n\n"
    )

    p.append(subsubsection("使用块模型与 Context 的自顶向下分析", "Top-Down Analysis Using Block Models and Context"))
    p.append(
        "顶层先运行 HyperScale 分析并写出块 context；"
        "块级读入 context 进行独立分析，结果回注顶层。\n\n"
    )
    p.append(fig("Figure 388", "使用顶层与块级分析运行的 HyperScale 分析", "fig:hs-top-block-runs"))

    p.append(subsubsection("含 MIM 的自顶向下分析", "Top-Down Analysis With Multiply Instantiated Modules (MIMs)"))
    p.append(
        "对同一块的多实例，HyperScale 合并各实例 context 并处理 MIM 悲观度（mim_pessimism）。\n\n"
    )
    p.append(fig("Figure 392", "自底向上流程中的时钟匹配问题", "fig:clk-match-bu"))

    p.append(subsubsection("顶层与块之间的时钟映射", "Clock Mapping Between Top and Block"))
    p.append(
        "块级与顶层须建立时钟映射；\cmd{write\_context} 写出 clock\_map.pt，块级读入后映射顶层时钟名。"
        "自底向上流程中顶层与块时钟名/周期不匹配会导致接口时序错误。"
        "可用 \cmd{create\_clock -name CLKZ} 在块级创建虚拟时钟调试映射问题。\n\n"
        "HyperScale 按优先级映射：共享物理时钟源网络；周期与波形精确匹配；时钟名前缀匹配。"
        "失败时发出 HS-004 错误但 \cmd{update\_timing} 仍完成。"
        "用 \cmd{report\_clock -map} 检查映射；N/A 表示未找到对应时钟。\n\n"
        "SMVA/DVFS 设计中，\cmd{create\_clock -dvfs\_scenario} 定义的时钟在映射时选择周期匹配的顶层时钟；"
        "未映射时钟端口传播无时钟到达窗口以确保块级分析边界顶层分析。"
        "块 context 须用 \cmd{write\_context -format gbc} 二进制格式以包含 DVFS 信息。\n\n"
        r"\cmd{get\_hier\_clocks} 返回 \texttt{hier\_clock} 集合，可在块级查询顶层时钟定义，"
        "在顶层查询块级时钟定义；用 \cmd{report\_attributes -application [get\_hier\_clocks]} 查看属性。\n\n"
    )

    p.append(subsection("选择自顶向下或自底向上流程", "Choosing a Top-Down or Bottom-Up Flow"))
    p.append(
        "自顶向下为首选：时序收敛更快，块约束与顶层约束从一开始保证一致。"
        "若块可分析而顶层约束尚未就绪，可用自底向上流程从预算约束开始，"
        "顶层分析后须检查顶层与块级约束一致性。\n\n"
    )

    p.append(subsection("自顶向下 HyperScale 流程", "Top-Down HyperScale Flow"))
    p.append(fig("Figure 390", "HyperScale 自顶向下层次化分析流程", "fig:hs-td-flow-detail"))
    p.append(
        "自顶向下流程四步（各在独立 PrimeTime 会话）：\n"
        r"\begin{enumerate}" + "\n"
        r"  \item 全芯片提取块约束（\cmd{hier\_characterize\_context\_mode constraints\_only}，最小 update，不用寄生）" + "\n"
        r"  \item 块级分析（读入提取约束，\cmd{write\_hier\_data} 写初始块数据）" + "\n"
        r"  \item 顶层 HyperScale 分析（\cmd{set\_hier\_config}，\cmd{write\_hier\_data} 写块 context）" + "\n"
        r"  \item 块级分析（\cmd{read\_context} 读详细 context，迭代收敛）" + "\n"
        r"\end{enumerate}" + "\n\n"
        "步骤 3--4 可重复直至时序收敛。顶层可用 \cmd{report\_timing -path\_type full\_clock\_expanded -from IN1 -to BLKA/reg2} "
        "报告跨层次完整路径。块级报告中顶层施加的约束以 ``@'' 标记（如 input external delay 0.34 @）。\n\n"
    )

    p.append(subsection("自底向上 HyperScale 流程", "Bottom-Up HyperScale Flow"))
    p.append(fig("Figure 391", "HyperScale 自底向上层次化分析流程", "fig:hs-bu-flow-detail"))
    p.append(
        "自底向上三步：\n"
        r"\begin{enumerate}" + "\n"
        r"  \item 用预算约束做块级分析，\cmd{write\_hier\_data} 生成 HyperScale 块模型" + "\n"
        r"  \item 顶层 HyperScale 分析（可用 \cmd{set\_clock\_map} 映射时钟，\cmd{report\_clock -cells/-map} 检查）" + "\n"
        r"  \item 块级用准确 context 最终分析（\cmd{read\_context}）" + "\n"
        r"\end{enumerate}" + "\n\n"
        "可用约束一致性检查器比较预算块约束与顶层扁平约束："
        r"\cmd{set\_app\_var sh\_enable\_constraint\_consistency\_checker true}，"
        r"\cmd{report\_constraint\_analysis} 报告不一致。" + "\n\n"
    )

    p.append(subsection("HyperScale 脚本与块 Context 自动生成", "Automatic Generation of HyperScale Scripts and Block Context"))
    p.append(
        "若有全芯片扁平分析脚本，可启用 HyperScale 模板脚本生成："
        r"\cmd{set\_app\_var hier\_enable\_analysis true}、"
        r"\cmd{set\_app\_var hier\_create\_script\_mode true}。"
        r"\cmd{characterize\_context -block ...} 后为各块创建 partition0/..partitionN/ 目录及 RUN.ptsh 脚本。" + "\n\n"
    )

    p.append(subsection("HyperScale 配置", "HyperScale Configuration"))
    p.append(
        f"使用 {cmd('set_hier_config')}（或 {cmd('set_hyperscale_configuration')}）配置块数据路径、"
        "时间戳与 HyperScale 目录结构。\n\n"
        f"{opt('-block')} 指定块名，{opt('-path')} 指定块会话数据目录，"
        f"{opt('-instances')} 指定实例列表，{opt('-name')} 关联配置名。"
        "顶层分析在配置目录下执行；各块数据目录建议以 HS\_ 为前缀。\n\n"
    )
    p.append(subsubsection("顶层 HyperScale 配置示例", "Example of Top-Level HyperScale Configuration"))
    p.append(
        lst(
            "set_hyperscale_configuration -block_config_path ./hs_data/BLKA\n"
            "read_verilog top.v\n"
            "link_design top\n"
            "read_parasitics top.spef\n"
            "source top.sdc\n"
            "update_timing -full"
        )
    )

    p.append(subsection("HyperScale 会话数据", "HyperScale Session Data"))
    p.append(
        "HyperScale 流程须用 \cmd{write\_hier\_data} 保存、\cmd{read\_context} 恢复会话数据。"
        "数据目录含网表快照、约束、context、时钟映射、时间戳与变量设置。"
        "顶层 \cmd{link\_design} 在配置路径下查找块级会话数据；"
        "指定 \opt{-instances} 时按实例路径查找。\n\n"
    )

    p.append(subsection("HyperScale 使用细节", "HyperScale Usage Details"))
    p.append(
        "使用 HyperScale 的基本步骤：\n"
        r"\begin{enumerate}" + "\n"
        r"  \item 配置 HyperScale（\cmd{set\_hier\_config}）" + "\n"
        r"  \item 读入并链接设计" + "\n"
        r"  \item 读入寄生与约束" + "\n"
        r"  \item \cmd{update\_timing}（及 \cmd{update\_noise} 若适用）" + "\n"
        r"  \item \cmd{write\_hier\_data} 写出块数据或 context" + "\n"
        r"\end{enumerate}" + "\n\n"
        f"用 {cmd('report_hier_analysis')} 确认配置；"
        f"{cmd('set_app_var hier_enable_analysis true')} 使能层次化分析。\n\n"
    )

    p.append(subsection("模型与 Context 不匹配处理", "Model-Context Mismatch Handling"))
    p.append(
        "块网表与 HyperScale 模型/context 不一致时，工具检测端口 net 变更并尝试 context 覆盖。"
        "无法解析时钟时应用无时钟 context。"
        r"\cmd{report\_context -list\_context\_override} 列出覆盖信息；"
        "属性 \texttt{is\_netlist\_dont\_override}、\texttt{is\_clock\_dont\_override}、"
        r"\texttt{has\_model\_mismatch\_clock} 标识问题端口。"
        r"\cmd{report\_constraint -boundary\_check} 报告块边界约束违例（clock\_mapping、"
        "clock\_attributes、clock\_uncertainty 等），许多可通过修正块级约束或继续迭代 HyperScale 流程解决。\n\n"
    )
    p.append(subsection("块级分析", "Block-Level Analysis"))
    p.append(
        "块级运行读入网表、寄生、块约束与顶层写出的 context：\n"
    )
    p.append(
        lst(
            "read_verilog block.v\n"
            "link_design block\n"
            "read_parasitics block.spef\n"
            "read_context -path ./hs_data/BLKA\n"
            "source block.sdc\n"
            "update_timing -full"
        )
    )

    p.append(subsubsection("带调整后 Context 的块级分析", "Block-Level Analysis With Adjusted Context"))
    p.append(
        "顶层 context 在块边界自动调整到达/要求时间与转换时间，"
        "反映顶层实际时序环境。\n\n"
    )

    p.append(subsection("链接设计", "Linking the Design"))
    p.append(
        "层次化分析中 link_design 须正确解析块引用、"
        "HyperScale 模型与黑盒实例。\n\n"
    )

    p.append(subsection("控制裕量应用方式", "Controlling How Margins Are Applied"))
    p.append(
        "HyperScale 在块边界应用 OCV/AOCV/POCV 裕量；"
        f"{cmd('report_hyperscale_constraints')} 报告边界检查与裕量传递。\n\n"
    )

    p.append(subsection("层次化约束提取", "Hierarchical Constraint Extraction"))
    p.append(
        "可用 HyperScale 约束提取器从全芯片扁平约束中提取一致的块级时钟、"
        "case 值与例外，用于 context 准确的块级分析。\n\n"
    )
    p.append(subsubsection("配置与运行约束提取", "Configuring and Running Constraint Extraction"))
    p.append(
        lst(
            "set_app_var hier_characterize_context_mode constraints_only\n"
            "source full_chip_analysis_script.tcl\n"
            "characterize_context -block BlockA\n"
            "update_timing\n"
            "write_context -format ptsh -output $outDir"
        )
    )
    p.append(
        "输出目录包含 clock_map.pt、constraints.pt、variables.pt。\n\n"
    )

    p.append(subsection("Context 覆盖", "Context Override"))
    p.append(
        "HyperScale 提供 context 覆盖特性：\n"
    )
    p.append(
        itemize(
            [
                "检测端口 net 上的网表更改",
                "对每个差异尽力应用 context 覆盖",
                "无法解析时钟时应用无时钟 context 数据",
            ]
        )
    )
    p.append(
        f"查询覆盖信息：{cmd('report_context -list_context_override')}；"
        "属性 is_netlist_dont_override、is_clock_dont_override 标识问题端口。\n\n"
    )

    p.append(subsubsection("侧输入与 Stub Pin 的时钟映射", "Clock Mapping for Side-Input and Stub Pins"))
    p.append(
        "在侧输入或 stub pin 上标注到达/要求时间时，"
        "工具检测时钟映射错误；has_model_mismatch_clock 属性标识未映射时钟。\n\n"
    )

    p.append(subsection("控制块边界调整", "Controlling the Block Boundary Adjustment"))
    p.append(
        f"使用 {cmd('set_dont_override')} 忽略顶层 context 数据，回退到预算约束。\n"
        f"{opt('-include')} 可选择性忽略 arc_delay、case_value、pin_transition 等类型。\n\n"
    )
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{set\_dont\_override -include 关键字}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"-include & 忽略的顶层 context 数据 \\" + "\n"
        r"\midrule" + "\n"
        r"arc\_delay & 输入端口到叶负载 pin 的 net 延迟；叶驱动到输出端口的延迟 \\" + "\n"
        r"case\_value & 输入端口的 case analysis \\" + "\n"
        r"pin\_transition & 输入端口的 context 转换时间 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )
    p.append(fig("Figure 422", "HyperScale 块级分析（抑制不完整块 context）", "fig:hs-block-dont-override"))

    p.append(subsection("HyperScale 属性", "HyperScale Attributes"))
    p.append(
        "可用 get_attribute 查询 HyperScale 相关属性，包括：\n"
    )
    p.append(
        itemize(
            [
                "单元对象：block_config_name、block_config_path、block_timestamp、critical_path_max 等",
                "设计对象：is_hyperscale_block、hyperscale_mode 等",
                "pin 对象：context_arrival、context_required、has_model_mismatch_clock 等",
                "port 对象：context_capacitance、is_user_dont_override 等",
            ]
        )
    )

    p.append(subsection("HyperScale 数据目录结构", "HyperScale Data Directory Structure"))
    p.append(
        "HyperScale 块数据目录包含网表、约束、context、时钟映射与时间戳文件，"
        "供顶层与块级运行共享。\n\n"
    )

    p.append(subsection("为 HyperScale 块写出网表与约束", "Writing Netlists and Constraints for a HyperScale Block"))
    p.append(
        f"使用 {cmd('write_context')}、{cmd('write_script')} 等命令保存块数据。\n\n"
    )

    p.append(subsection("HyperScale ECO 收敛方法", "HyperScale ECO Closure Methods"))
    p.append(
        "PrimeTime ECO 流程与 HyperScale 集成：\n"
    )
    p.append(
        itemize(
            [
                "顶层 ECO 修复 — 在顶层运行 fix_eco_*，写出变更列表。",
                "块级 ECO 修复 — 在块级运行，使用更新后的块 context。",
                "使用更新块 context 进行块级 ECO。",
                "MIM 的 ECO — 跨实例一致应用更改。",
                "在 ECO 流程中解析块违例。",
                "并行运行 ECO 以改善运行时间与容量。",
            ]
        )
    )
    p.append(
        "HyperScale ECO 与 IC Compiler、StarRC 的接口支持 signoff 增量 ECO 流程。\n\n"
    )

    p.append(subsection("HyperScale 中的时序分析", "Timing Analysis in HyperScale"))
    p.append(
        "HyperScale 顶层分析使用块 HyperScale 模型替代内部网表，"
        "在接口保留完整时序信息。支持 CRPR、SI、POCV 等分析模式。\n\n"
    )
    p.append(
        "路径类型标记：I（ideal network）、H（HyperScale context override）等。\n\n"
    )

    p.append(subsection("路径特定例外建模", "Path-Specific Exception Modeling"))
    p.append(
        "HyperScale 在块边界建模路径特定例外（false path、multicycle path 等），"
        "确保顶层与块级约束一致。\n\n"
    )

    p.append(fig("Figure 393", "两级层次设计示例", "fig:two-level-hier"))

    # ===== Context Characterization =====
    p.append(section("Context 特征化", "Context Characterization"))
    p.append(
        "Context 特征化支持块级分析：写出块在顶层内的时序 context，"
        "块可单独分析并获得在顶层环境下工作的准确时序。\n\n"
    )
    p.append(fig("Figure 424", "Context 特征化示例", "fig:ctx-char-example"))

    p.append(subsection("将 Context 用于块级时序分析", "Using Context for Block-Level Timing Analysis"))
    p.append(
        f"使用 {cmd('characterize_context')} 标记待特征化块，"
        f"{cmd('update_timing')} 后执行特征化，"
        f"{cmd('write_context')} 写出 context 文件。\n\n"
    )
    p.append(
        lst(
            "characterize_context -block block1 -instances BLK1\n"
            "update_timing\n"
            "write_context -format ptsh -output BLK1_context [get_cells BLK1]"
        )
    )

    p.append(
        "读入块级分析：\n"
    )
    p.append(
        lst("read_context -path BLK1_context")
    )
    p.append(
        "context 包含输入端口到达时间、输出端口要求时间、"
        "转换时间、case 值、串扰信息与时钟映射。\n\n"
    )

    p.append(subsection("Context 特征化命令与选项", "Context Characterization Commands and Options"))
    p.append(
        itemize(
            [
                f"{cmd('characterize_context')} — 指定块与实例",
                f"{cmd('write_context')} — 写出 context（ptsh/sdc 格式）",
                f"{cmd('read_context')} — 读入 context",
                f"{cmd('report_context')} — 报告 context 信息",
                f"{cmd('remove_context')} — 移除已加载 context",
            ]
        )
    )

    # ===== Context Budgeting =====
    p.append(section("Context 预算", "Context Budgeting"))
    p.append(
        "Context Budgeting（PrimeTime-APX）在层次化流程中为块接口分配时序预算，"
        "从顶层 slack 按比例分配到各块段，生成块级 I/O 约束。\n\n"
    )
    p.append(fig("Figure 425", "Context Budgeting 概念", "fig:ctx-budget-concept"))

    p.append(subsection("Budgeting 期间如何调整 Context", "How Contexts are Adjusted During Budgeting"))
    p.append(
        f"使用 {cmd('set_timing_budget')} 配置预算模式，"
        f"{cmd('update_budget')} 在时序更新后计算预算，"
        "调整各块边界的 input/output delay。\n\n"
    )
    p.append(
        lst(
            "characterize_context -block block1 -instances BLK1\n"
            "characterize_context -block block2 -instances BLK2\n"
            "update_timing\n"
            "set_timing_budget -mode pin_slack\n"
            "update_budget\n"
            "report_budget -through BLK1/Z"
        )
    )

    p.append(subsection("报告 Context 预算", "Reporting the Context Budget"))
    p.append(
        f"{cmd('report_budget -through pin')} 报告通过指定层次 pin 的关键路径各段延迟、"
        "权重与分配预算。若 pin 有 context 调整，还显示调整计算细节。\n\n"
    )
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{report\_budget 输出列示例}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}l l r r r@{}}" + "\n"
        r"\toprule" + "\n"
        r"Point & Mode & Delay & Weight & Budget \\" + "\n"
        r"\midrule" + "\n"
        r"BLK1/Z & pin\_slack & 4.00 & 0.33 & 3.33 \\" + "\n"
        r"MID/A & pin\_slack & 1.00 & 0.08 & 0.83 \\" + "\n"
        r"MID/Z & pin\_slack & 2.00 & 0.17 & 1.67 \\" + "\n"
        r"BLK2/A & pin\_slack & 1.00 & 0.08 & 0.83 \\" + "\n"
        r"BLK2/FF/D & pin\_slack & 4.00 & 0.33 & 3.33 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsection("自定义 Context 预算", "Customizing the Context Budget"))
    p.append(
        "默认按路径段延迟比例分配 slack，可自定义：\n"
    )
    p.append(
        itemize(
            [
                "应用 Slack 裕量（-slack_margin、-positive_slack_margin）",
                "设置块段目标 slack",
                "设置块段精确延迟",
                "设置块段时钟周期百分比",
                "设置块段最小延迟",
                "预算规范的优先级",
            ]
        )
    )

    p.append(subsubsection("应用 Slack 裕量", "Applying Slack Margins"))
    p.append(
        f"{cmd('set_timing_budget -slack_margin')} 影响违例路径（从负 slack 减去裕量）；"
        f"{opt('-positive_slack_margin')} 影响通过路径（最多减至零 slack）。\n\n"
    )

    p.append(subsection("写出预算后的 Context", "Writing Out Budgeted Context"))
    p.append(
        f"预算计算后使用 {cmd('write_context')} 写出含预算约束的块 context，"
        "供块级独立分析使用。\n\n"
    )

    p.append(subsection("在 HyperScale 流程中使用 Context 预算", "Using Context Budgeting in a HyperScale Flow"))
    p.append(
        "HyperScale 顶层运行中使能 context budgeting 时："
        r"\cmd{set\_hier\_config -block} 自动选择块进行 context 特征化（非 HyperScale 全网表块仍须 \cmd{characterize\_context}）；"
        r"\cmd{write\_hier\_data} 自动包含预算调整（仍可用 \cmd{write\_context} 做独立测试）。"
        "块级默认使用预算 context；用 \cmd{read\_context -exclude\_budget} 读入非预算实际 context。\n\n"
        r"\begin{noteBox}" + "\n"
        r"Context Budgeting 限制：\cmd{set\_timing\_budget -target\_slack} 仅用于块 feedthrough 段；\cmd{update\_budget} 只能运行一次。" + "\n"
        r"\end{noteBox}" + "\n\n"
    )

    p.append(subsection("预算规范优先级", "Budget Specification Precedence"))
    p.append(
        "同一路径多段应用多个规范时顺序：\n"
        r"\begin{enumerate}" + "\n"
        r"  \item 应用 \opt{-slack\_margin}/\opt{-positive\_slack\_margin} 更新路径 slack" + "\n"
        r"  \item 应用 \texttt{timing\_budget\_segment\_delay\_threshold} 放大小段延迟" + "\n"
        r"  \item 应用 \opt{-target\_slack}/\opt{-delay\_value}/\opt{-percent\_value}" + "\n"
        r"  \item 其余段按延迟比例分配剩余 slack" + "\n"
        r"\end{enumerate}" + "\n\n"
    )

    # ===== ETM =====
    p.append(section("提取时序模型（ETM）", "Extracted Timing Model (ETM)"))
    p.append(
        "ETM 是由 \cmd{extract\_model} 生成的块抽象时序模型，可在更高层次替代块网表进行分析。"
        r"\figplaceholder{Figure 429: Extracted Timing Model Analysis}{ETM 分析}{fig:etm-analysis}"
        "优势：降低 PrimeTime/DC/ICC 全芯片分析运行时间与内存；保护 IP 网表。"
        "模型用组合与时序弧抽象接口行为，延时以 NLDM/CCS 查找表表示，"
        "随输入转换与输出负载变化，属 context-independent 模型。\n\n"
    )

    p.append(subsection("ETM 使用流程", "Usage Flow of ETM"))
    p.append(
        "块级：读入网表/寄生/约束，\cmd{update\_timing}，设置 \cmd{hier\_modeling\_version 2.0}，"
        r"\cmd{extract\_model ... -validate timing} 自动验证网表与包装器中模型实例的 slack 匹配。"
        "顶层：用 extract\_model 生成的 .db/.lib 替换块实例，读入顶层网表与约束分析。\n\n"
        r"\figplaceholder{Figure 430: Timing model extraction process}{时序模型提取过程}{fig:etm-extract-proc}"
        r"\figplaceholder{Figure 431--432: Gate-Level Netlist and Extracted Model}{门级网表与提取模型}{fig:etm-netlist-model}" + "\n\n"
    )

    p.append(subsection("ETM 流程概述", "ETM Flow Overview"))
    p.append(
        "典型 ETM 流程：\n"
        "1. 准备块设计（读入网表、寄生、约束）。\n"
        "2. check_timing 检查潜在问题。\n"
        "3. report_timing 验证时序。\n"
        "4. 设置模型提取变量。\n"
        "5. extract_model 生成 .db/.lib 模型。\n"
        "6. 在顶层实例化模型并分析。\n\n"
    )

    p.append(subsection("生成模型", "Generating the Model"))
    p.append(
        lst("pt_shell> extract_model -output example_model -format {db}")
    )
    p.append(
        "生成 .lib 模型时可能含 min_delay_flag、original_pin 等用户定义属性。\n\n"
    )

    p.append(subsection("时序模型提取细节", "Timing Model Extraction Details"))
    p.append(
        "extract_model 从原始设计时序路径提取简单时序弧，涵盖：\n"
    )
    p.append(
        itemize(
            [
                "边界 net 与内部 net",
                "输入到寄存器路径",
                "输入到输出路径",
                "寄存器到输出路径",
                "寄存器到寄存器路径（不提取，仅遍历接口逻辑）",
                "时钟路径",
                "透明锁存器与时间借用",
                "最小脉冲宽度与最小周期",
                "False path",
                "时钟门控检查",
                "反标延迟",
                "噪声特性",
            ]
        )
    )

    p.append(subsubsection("边界 net 与内部 net", "Boundary Nets and Internal Nets"))
    p.append(
        "提取模型不保留原始边界 net，而将边界 net 延迟分解到模型中。"
        "内部 net 无详细寄生时 PrimeTime 计算电容/电阻；"
        "有 SPEF/RSPF 反标时使用详细寄生值。\n\n"
    )

    p.append(subsubsection("输入到寄存器路径", "Paths From Inputs to Registers"))
    p.append(
        "提取为输入 pin 与寄存器时钟之间的 setup 弧与 hold 弧；"
        "setup 弧捕获最长路径延迟加寄存器 setup 时间，"
        "hold 弧捕获最短路径延迟加 hold 时间。\n\n"
    )

    p.append(subsubsection("输入到输出与寄存器到输出路径", "Paths From Inputs/Registers to Outputs"))
    p.append(
        "各提取两条延迟弧（最长与最短路径）。"
        "延迟为输入转换时间与输出负载电容的函数；"
        "弧与使用环境无关，在不同环境中延迟可能不同。\n\n"
    )

    p.append(subsubsection("时钟路径", "Clock Paths"))
    p.append(
        "时钟网络延迟与转换时间反映在模型中，但不含时钟 latency；"
        "使用模型时须指定 source latency 与 network latency。\n\n"
    )

    p.append(subsubsection("透明锁存器与时间借用", "Transparent Latches and Time Borrowing"))
    p.append(
        f"{cmd('extract_model')} 可提取接口逻辑中简单锁存器结构，"
        f"在指定条件下保留最多两级借用行为。"
        f"{opt('-latch_levels')}（0--2，默认 2）控制考虑的透明锁存器级数。\n\n"
    )
    p.append(
        "write_interface_timing 与 compare_interface_timing 用于验证模型与网表时序，"
        "对含锁存器接口尤为重要。\n\n"
    )

    p.append(subsubsection("最小脉冲宽度与最小周期", "Minimum Pulse Width and Minimum Period"))
    p.append(fig("Figure 433", "最小脉冲宽度与最小周期提取", "fig:mpw-mp-extract"))

    p.append(subsection("控制提取表大小", "Controlling the Extracted Table Sizes"))
    p.append(
        "应用变量控制查找表索引数量与范围，影响模型精度与文件大小。"
        r"\cmd{set\_extract\_model\_indexes} 显式指定电容/转换索引；"
        r"\cmd{reset\_extract\_model\_indexes} 移除用户指定索引。"
        r"\cmd{set\_extract\_model\_margin} 在提取时为延时/约束弧加固定裕量。" + "\n\n"
    )

    p.append(subsection("指定模型索引与裕量", "Specifying Model Indexes and Margins"))
    p.append(
        lst(
            "set_extract_model_indexes -type capacitance \\\n"
            "  {0.11 0.12 0.15 0.18 0.20} -ports [get_ports out[1]]\n"
            "set_extract_model_margin -max 10 -ports [get_ports *]"
        )
    )

    p.append(subsection("抽头输出端口", "Tapped Output Ports"))
    p.append(
        "抽头输出（同时连驱动与接收）是不良设计实践，工具发 MEXT-75 警告。"
        "NLDM 默认可建 3-D 弧（\texttt{related\_output\_load}）；"
        r"设 \cmd{extract\_model\_with\_3d\_arcs false} 得 2-D 弧。CCS 提取恒为 2-D。"
        "稳健层次建模应缓冲所有端口。\n\n"
    )

    p.append(subsection("时序例外与生成时钟", "Timing Exceptions and Generated Clocks"))
    p.append(
        "接口 false path 影响提取弧；multicycle path 调整 setup/hold/延时。"
        "建议在接口避免复杂例外，提取后在顶层对 ETM 实例施加端口/时钟特定约束。"
        "生成时钟命名：\texttt{instance\_name/generated\_clock\_name}；"
        "ETM 保留与接口寄存器相关的生成时钟及 feedthrough 时钟路径。"
        "级联生成时钟应逐级引用 master（div-by-2 再 div-by-4），勿均指原始 master。\n\n"
    )

    p.append(subsection("提取内部 Pin 与检查 Pin", "Extracting Internal Pins and Check Pins"))
    p.append(
        "内部 pin 时钟信息存为模型内部 pin；时钟网络含组合路径时创建 check pin 以允许时钟追踪继续到时钟输出，"
        "否则 setup/hold 弧会阻止时钟路径遍历。"
        r"\figplaceholder{Figure 441--442: Check pins in ETM}{ETM 中的检查 pin}{fig:etm-check-pin}" + "\n\n"
    )

    p.append(subsection("跨块内电源域合并模型", "Merging Models Across Block-Internal Power Supplies"))
    p.append(
        "多电源域块可合并为单一 ETM 或按域分别提取，取决于分析需求。\n\n"
    )

    p.append(subsection("保守块时序分析与模型提取", "Conservative Block Timing Analysis and Model Extraction"))
    p.append(
        "块分析（update_timing）质量直接决定 extract_model 模型质量。"
        "遵循保守块收敛方法以产生高质量 ETM。\n\n"
    )

    p.append(subsubsection("块 Context 的保守建模", "Conservative Modeling of the Block Context"))
    p.append(
        "建议采用 STA 最坏情况方法：\n"
    )
    p.append(
        itemize(
            [
                "穷尽保守评估块使用场景与 context（PVT、电压、温度、裕量、驱动/接收类型等）",
                "以值或条件范围指定 context，覆盖所有实例化场景",
                "对时序分析与模型提取应用相同约束",
            ]
        )
    )

    p.append(subsubsection("块输出约束", "Constraints for Block Outputs"))
    p.append(
        lst(
            "set_load -pin_load -min $min_cap [all_outputs]\n"
            "set_load -pin_load -max $max_cap [all_outputs]"
        )
    )
    p.append("通常 $min_cap=0.0；$max_cap 保守估计为强驱动器输入电容加典型线电容。\n\n")

    p.append(subsubsection("块输入约束", "Constraints for Block Inputs"))
    p.append(
        lst(
            "set_driving_cell -min -input_transition_rise/fall $min_slew \\\n"
            "  -lib_cell $strong_driver ...\n"
            "set_driving_cell -max -input_transition_rise/fall $max_slew \\\n"
            "  -lib_cell $weak_driver ..."
        )
    )
    p.append(
        "对长顶层连线可在输入端口加集总电容建模；"
        "IP 块周边缓冲环是层次 signoff 的最安全做法。\n\n"
    )
    p.append(fig("Figure 448", "在输入端口设置 driving cell", "fig:driving-cell-port"))

    p.append(subsubsection("转换时间传播效应", "Slew Propagation Effects"))
    p.append(
        "ETM .lib 文件用 NLDM 查找表表示延迟、转换与约束；"
        "顶层到达 ETM 的慢转换可能触发 max_transition DRC。\n\n"
    )

    p.append(subsection("ETM 的 SI 与串扰建模", "SI and Crosstalk Modeling in ETM"))
    p.append(
        "提取时使用当前分析的边界串扰延迟；"
        "si_filter_keep_all_port_aggressors 在 extract_model 时强制为 true，"
        "包含所有端口级 aggressor 以实现保守 SI 建模。\n\n"
    )

    p.append(subsection("模型验证", "Model Validation"))
    p.append(
        "验证流程：\n"
        "1. 对块网表 write_interface_timing 作为参考。\n"
        "2. extract_model -test_design 生成测试设计。\n"
        "3. 对测试设计应用约束并 update_timing。\n"
        "4. compare_interface_timing 比较 slack（典型绝对容差 20 ps）。\n\n"
    )

    p.append(subsubsection("排查模型验证不匹配", "Troubleshooting Model Validation Mismatches"))
    p.append(
        itemize(
            [
                "工作条件与分析模式须与块分析一致",
                "接口路径上不推荐 multicycle path；块内部 multicycle 不影响 ETM",
                "不支持 set_max_delay/set_min_delay 异步约束提取",
                "包装（wrapper）设计中须对测试网表 net 反标零电容/电阻",
                "输入 driving cell 与集总电容差异可导致验证误差",
                "ETM 中已含 derating 时验证约束避免双重 derating",
            ]
        )
    )
    p.append(fig("Figure 449", "含 ETM 实例的测试设计", "fig:etm-test-design"))
    p.append(fig("Figure 450", "反标边界 net", "fig:ba-boundary-nets"))

    p.append(subsection("ETM 的噪声特性", "Noise Characteristics in ETM"))
    p.append(
        "extract_model 可将噪声裕量信息纳入模型，供顶层 SI 分析使用。"
        r"\cmd{extract\_model -noise} 在模型中包含噪声数据；"
        "提取时 \cmd{si\_filter\_keep\_all\_port\_aggressors} 强制为 true 以保守包含所有端口 aggressor。\n\n"
    )

    p.append(subsection("块内部路径与接口路径", "Block-Internal and Interface Paths"))
    p.append(
        "ETM 替换块后内部寄存器到寄存器路径不可见，须在提取前闭合块内部时序。"
        "提取扫掠接口路径转换与负载索引，用当前分析边界串扰延时；"
        "对输入可用 \cmd{set\_si\_delay\_analysis -ignore\_arrival} 设无限到达窗口以保守建模未知到达对齐。\n\n"
    )

    # ===== QTM =====
    p.append(section("快速时序模型（QTM）", "Quick Timing Model (QTM)"))
    p.append(
        "QTM 通过 PrimeTime 命令指定输入、输出与约束创建简化时序模型，"
        "用于设计早期快速层次化分析，精度低于 ETM 但创建更快。\n\n"
    )

    p.append(subsection("创建 QTM", "Creating a Quick Timing Model"))
    p.append(
        "QTM 通过 PrimeTime 命令手动定义端口、弧与约束，无需完整块网表。"
        "常用命令：\cmd{create\_qtm\_model}、\cmd{create\_qtm\_port}、\cmd{create\_qtm\_delay\_arc}、"
        r"\cmd{create\_qtm\_constraint\_arc}、\cmd{create\_qtm\_drive\_type}、\cmd{set\_qtm\_port\_drive}、"
        r"\cmd{save\_qtm\_model}、\cmd{report\_qtm\_model}、\cmd{remove\_qtm\_model}。"
        "端口类型：input、output、clock、bidirectional。弧可指定 max/min（setup/hold/recovery/removal）。\n\n"
    )
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{常用 QTM 命令}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"命令 & 功能 \\" + "\n"
        r"\midrule" + "\n"
        r"create\_qtm\_model & 创建 QTM 模型 \\" + "\n"
        r"create\_qtm\_port & 定义端口 \\" + "\n"
        r"create\_qtm\_delay\_arc & 创建延迟弧 \\" + "\n"
        r"create\_qtm\_constraint\_arc & 创建约束弧 \\" + "\n"
        r"create\_qtm\_drive\_type & 定义驱动类型 \\" + "\n"
        r"save\_qtm\_model & 保存 QTM 模型 \\" + "\n"
        r"report\_qtm\_model & 报告 QTM 信息 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsection("创建 QTM 的脚本示例", "Script Example to Create a Quick Timing Model"))
    p.append(
        lst(
            "create_qtm_model -name my_block_qtm\n"
            "create_qtm_port -type input I1\n"
            "create_qtm_port -type output O1\n"
            "create_qtm_port -type clock CLK\n"
            "create_qtm_drive_type -type input_drive input_drv \\\n"
            "  -lib_cell BUF1\n"
            "set_qtm_port_drive -type input_drv I1\n"
            "create_qtm_delay_arc -from I1 -to O1 -path_type max \\\n"
            "  -value 0.5\n"
            "create_qtm_constraint_arc -from I1 -to CLK \\\n"
            "  -path_type setup -value 0.3\n"
            "save_qtm_model -format lib -output my_block_qtm.lib"
        )
    )

    p.append(subsection("在顶层使用 QTM", "Using a QTM at the Top Level"))
    p.append(
        "顶层读入 QTM .lib 文件，将块实例链接为 QTM 模型进行早期时序评估。"
        "随着设计成熟，应迁移到 ETM 或 HyperScale 流程以获得 signoff 精度。\n\n"
    )

    p.append(subsection("QTM 与 ETM 对比", "QTM vs ETM"))
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{QTM 与 ETM 对比}" + "\n"
        r"\begin{tabularx}{\textwidth}{@{}X X X@{}}" + "\n"
        r"\toprule" + "\n"
        r"特性 & QTM & ETM \\" + "\n"
        r"\midrule" + "\n"
        r"创建方式 & 手动指定弧与约束 & 从网表自动提取 \\" + "\n"
        r"精度 & 低（早期估算） & 高（基于实际实现） \\" + "\n"
        r"创建速度 & 快 & 较慢（需完整块分析） \\" + "\n"
        r"适用阶段 & RTL/早期 netlist & 布局后/ signoff 前 \\" + "\n"
        r"SI/串扰 & 不支持 & 支持保守 SI 建模 \\" + "\n"
        r"HyperScale 集成 & 有限 & 完整支持 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabularx}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(
        see_also(
            [
                "第~\\ref{chap:eco}~章 ECO 流程（HyperScale ECO）",
                "第~\\ref{chap:hier}~章 HyperScale 与 Context 特征化",
            ]
        )
    )

    p.append(ch22_extra())

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
