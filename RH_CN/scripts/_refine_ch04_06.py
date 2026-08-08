# -*- coding: utf-8 -*-
"""Expand RH_CN chapters 04-06 to full faithful translation (no compression)."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "chapters"

# ---------------------------------------------------------------------------
# Chapter 4 expansions (inserted via markers in base file)
# ---------------------------------------------------------------------------

CH04_INSERT_AFTER_GSC = r"""
GSC 文件语法与用法详见附录 C「Global Switching Configuration (GSC) File」。通过 \gsr{GSC_FILE} 可为功耗计算建立实例与块的开关状态。
"""

CH04_INSERT_AFTER_TOGGLE_PRIO = r"""
\paragraph{\gsr{NET_TOGGLE_RATE} / \gsr{NET_TOGGLE_RATE_FILE} / \gsr{SAIF_FILE}}
为设计中未另行指定的网络指定翻转率。\gsr{NET_TOGGLE_RATE_FILE} 指向含网络翻转率列表的文件；\gsr{SAIF_FILE} 可导入 SAIF 格式开关活动。可选。默认：无。

\paragraph{\gsr{CELL_TOGGLE_RATE}}
按单元类型（cell type）为未另行指定的实例定义默认翻转率。可选。默认：无。

\paragraph{\gsr{CLOCK_DOMAIN_TOGGLE_RATE} / \gsr{POWER_DOMAIN_TOGGLE_RATE}}
分别为各时钟域或电源域指定默认翻转率，用于未在更高优先级关键字中覆盖的实例/网络。可选。

\paragraph{\gsr{TOGGLE_RATE_RATIO_COMB_FF}}
指定组合逻辑相对触发器/锁存器翻转率的比值，用于 vectorless 状态传播中推导组合网活动。可选。
"""

CH04_EXPAND_BPA = r"""
\subsection{BLOCK\_POWER\_ASSIGNMENT 语法详解}
\subsubsection*{Block Power and Current Assignment Syntax}

\gsr{BLOCK_POWER_ASSIGNMENT}（BPA）因应用类型众多，语法按用途分类如下。

\paragraph{为已有 LEF/DEF 实例分配功耗}
\begin{lstlisting}
<instName> [BLOCK|PIN] <layerSpec> <netName> [<powerW>|<currentA>|-1]
\end{lstlisting}
其中 \texttt{<layerSpec>} 为层名、\texttt{ALL}、\texttt{TOP}、\texttt{BOTTOM} 或与 BPA 实例重叠的最高/最低掩模层，或 via 名。\texttt{[<powerW>|<currentA>]} 为电源网功耗（W）或地网电流（A）；\texttt{-1} 表示由功耗引擎根据翻转率、BPFS、APL 等决定。

\paragraph{创建新区域实例并分配功耗}
\begin{lstlisting}
<BPA_instName> REGION <layerSpec> <netName> [<powerW>|<currentA>]
    <llx> <lly> <urx> <ury>
\end{lstlisting}

\paragraph{用 DECAP\_CELL 或 BLOCK\_POWER\_MASTER\_CELL 声明的单元创建实例}
\begin{lstlisting}
<BPA_instName> <cellName> <layerSpec> <netName>
    [<powerW>|<currentA>] <llx> <lly> <orientation>
\end{lstlisting}

\paragraph{全芯片区域}
\begin{lstlisting}
<BPA_instName> FULLCHIP <layerSpec> <netName> [<powerW>|<currentA>]
\end{lstlisting}
注意：\texttt{FULLCHIP} 功率须在 BPFS 而非 BPA 中定义。

\paragraph{在已有 BPA 实例内定义子区域（可多次声明）}
\begin{lstlisting}
<BPA_instName> BLOCK AREA <llx> <lly> <urx> <ury>
<BPA_instName> BLOCK RECTILINEAR <x1 y1 x2 y2 x3 y3 ...>
\end{lstlisting}

\paragraph{排除区域或实例}
\begin{itemize}
  \item \texttt{<regionName> REGION EXCLUDE <llx> <lly> <urx> <ury>}：从 BPA 功耗分配中排除矩形区域
  \item \texttt{<instName> BLOCK EXCLUDE}：排除与 BPA 重叠的设计实例
  \item \texttt{<regionName> REGION INCLUDE <llx> <lly> <urx> <ury>}：在 EXCLUDE 区域内加回矩形
  \item \texttt{<instName> BLOCK INCLUDE}：用已有实例边界框执行与 INCLUDE 相同操作
  \item \texttt{<BPA_instName> BLOCK EXCLUDE_MACRO}：排除与 BPA 重叠的宏实例
  \item \texttt{<instName> BLOCK EXCLUDE_BPFS}：排除 BPFS 中定义且与 BPA 重叠的实例
  \item \texttt{<BPA_instName> BLOCK OVERLAP_OK}：排除与 BPA 重叠的所有实例所占区域
\end{itemize}

\paragraph{多域与 \texttt{-1} 功耗}
每个 block 的每个域（net）须单独一行，例如：
\begin{lstlisting}
regionA REGION met3 vdd1 -1 100 200 300 400
regionA REGION met4 vdd2 -1 100 200 300 400
regionA REGION met3 vss -1 100 200 300 400
\end{lstlisting}
若 block 中某一网在 BPA 中设为 \texttt{-1}，则该 block 所有域的功耗/电流均由功耗计算引擎决定。

\paragraph{BLOCK\_POWER\_MASTER\_CELL 与不规则区域}
可在 \gsr{BLOCK_POWER_MASTER_CELL} 中定义共享主单元格及矩形子区域，再在 BPA 中引用：
\begin{lstlisting}
BLOCK_POWER_MASTER_CELL {
    <master_cell_name1> <BB_llx> <BB_lly> <BB_urx> <BB_ury>
    ?<master_cell_name2> <bbox> {
        <sub-area bbox>
        ...
    }?
}
BLOCK_POWER_ASSIGNMENT {
    <region> <master_cell_name> <layer> <net_name>
    [<power_W>|<gnd_I>] <BB_llx> <BB_lly> <orientation_code>
    ...
}
\end{lstlisting}
多个 REGION 可共享同一 \texttt{master_cell_name}。

\paragraph{BPA 典型示例}
\begin{lstlisting}
RegionABC FULLCHIP via7 VDD 2.0
RegionABC FULLCHIP via5 VDDC 0.4
BlckA BLOCK MET6 GND 1.0
BlckB PIN MET6 VDD 0.2
BlckC BLOCK via2 VDD 0.4
Region1 REGION via3 VDDC 0.3 30.0 65.0 60.0 95.0
IOL REGION MET5 VDD_L 0.005 100 1050 1000 9900
regionA REGION ALL VSS 0.1 10.0 20.0 30.0 40.0
\end{lstlisting}

MMX 内子区域可用前缀 \texttt{adsU1/}，例如 \texttt{adsU1/regionA}，以便 RedHawk 正确解析层次。

\paragraph{交互式 BPA 合并规则}
\cmd{gsr set BLOCK_POWER_ASSIGNMENT_FILE <file>} 可在 \cmd{setup design} 前后初始化或重设 BPA。\cmd{gsr get BLOCK_POWER_ASSIGNMENT} 显示当前设置。\cmd{gsr get BLOCK_POWER_MASTER_CELL} 显示主单元格定义。新文件与已有 BPA 比较时：语法错误则不改该项；仅在新文件中存在则添加；仅在旧文件中存在则删除；双方都有则用新参数。

\paragraph{REGION 重叠与 inactive 实例}
两个不同 REGION 坐标重叠会警告（子区域除外）。BPA REGION 与常规实例重叠时，该实例视为 inactive 并被忽略。每个 BPA REGION 可作为实例名引用；层次名中 \texttt{/} 在 cell 名中替换为 \texttt{\_}（如 \texttt{U10/I5} $\rightarrow$ \texttt{U10\_I5}）。
"""

CH04_EXPAND_DECAP = r"""
\subsection{创建去耦单元（DECAP\_CELL + BPA）}
\subsubsection*{Creating Decap Cells During BPA}

可用 \gsr{DECAP_CELL} 与 BPA 创建/实例化 decap 块，\cmd{print decap} 亦会考虑这些块。Decap 可来自 LEF 或在流程中创建：
\begin{lstlisting}
APL_FILES {
    mydecap.cdev cap
    ...
}
BLOCK_POWER_ASSIGNMENT {
    DecapABC_10 DecapABC METAL1 VDD 0.0 3800 4200 N
    DecapABC_10 DecapABC METAL1 VSS 0.0 3800 4200 N
    DecapABC_20 LEF_decap1 METAL1 VDD 0.0 3900 4300 N
}
DECAP_CELL {
    LEF_decap1
    ...
    DecapABC 100 100 0.1 10 METAL1 0.001
}
\end{lstlisting}
语法 \texttt{<decap\_cell> <width> <height> <C\_pF> <R\_ohm> <layer> <leakage\_A>}。本例 RedHawk 为 \texttt{DecapABC} 创建 decap 单元，\texttt{DecapABC\_10/20} 为实例；GUI 选中 decap 实例时，日志显示实例名、单元名与分配的 decap 值。

\subsection{早期 decap 估计流程}
\subsubsection*{Early Stage Decap Estimation}

为帮助满足全局 DvD 目标，可按以下步骤估计早期 decap：
\begin{enumerate}
  \item 在粗略 placement/CTS 完成后运行动态分析，查看 DvD
  \item \cmd{decap fill -uniform <percent> -pattern \{<decap masters>\}} 在标准单元行上均匀填充指定比例 decap（可能与已有单元重叠）
  \item 重跑 DvD；若未达全局目标则删除所加 decap（可忽略局部热点）
  \item 调整覆盖率与 decap master 组合，重复 2--3 直至满足全局 DvD
  \item 将所需 decap 量（可选含 placement 信息）反馈给 P\&R 工具
  \item 继续常规定点与布线
\end{enumerate}
报告示例：
\begin{lstlisting}
DECAP_MASTER_NAME Number_of_Instance Amount_of_Decap_Added
cell_698               333548              457.397700 pF
cell_200               333548               93.843726 pF
-------------------------------------------------------
Total_Amount           667096              551.241426 pF
\end{lstlisting}

\subsection{早期分析报告}
\subsubsection*{Reports Created from Early Analysis}

早期分析与标准静态分析类似，生成：
\begin{itemize}
  \item 线基压降（wire-based voltage drops）
  \item pad 电流（pad currents）
  \item 潜在 EM 问题区域（potential EM problem areas）
\end{itemize}
"""

CH04_EXPAND_CASES = r"""
\paragraph{Case 1：仅 P/G 布线、无块布局}
条件：仅有 P/G 布线，无块放置；有全芯片或分区功耗。可指定 FULLCHIP 与 REGION 功耗，并为各区域/全芯片指定电流 sink 所在金属层或 via 层。

语法框架：
\begin{lstlisting}
BLOCK_POWER_ASSIGNMENT {
    [<DEF_inst_name> [BLOCK|PIN] | <regionName> [FULLCHIP|REGION]]
    [<layer_name>|ALL|TOP|BOTTOM|<via_name>] <pwr_domain_name>
    [<domain_power-W>|<gnd_net_current-A>|-1]
    ?<x1 y1 x2 y2 - REGION 必需>?
}
\end{lstlisting}
示例：顶层 metal6 上 VDD\_X 域消耗 1.0\,W：
\begin{lstlisting}
RegionXYZ FULLCHIP metal6 VDD_X 1.0
\end{lstlisting}
via4 上区域 (100,100)--(200,200) 内 GND\_X 总电流 0.35\,A：
\begin{lstlisting}
RegionA REGION via4 GND_X 0.35 100.0 100.0 200.0 200.0
\end{lstlisting}
RedHawk 在 RegionA 内所有 via4 形状上插入 current sink，合计 0.35\,A。指定金属层时，区域内该层所有 top/bottom via 为 sink；指定 via 层时，该类型 via 为 sink。

\paragraph{Case 2：P/G + 宏布局，宏无 LEF pin/详细视图}
可指定 FULLCHIP 与块级功耗及每层 sink 定义。示例：
\begin{lstlisting}
RegionMNOP FULLCHIP metal6 VDD_X 1.0
BlockA BLOCK via4 GND_X 0.35
BlockA BLOCK via4 VDD_X 0.42
BlockB BLOCK metal3 VDD_X 0.72
\end{lstlisting}
顶层 BlockA、BlockB 外 via5/via6 分配 1.0\,W（两 block 均覆盖 VDD\_X）；FULLCHIP 功率应仅针对顶层 sink。BlockA 内 via4 合计 0.35\,A（GND\_X）；BlockB 内 metal3 几何上 sink 合计 0.72\,W（VDD\_X）。

\paragraph{Case 3：P/G + 宏布局，宏有 LEF pin}
与 Case 2 类似，但对已有 LEF pin 的块使用 \texttt{PIN} 而非 \texttt{BLOCK}，current sink 须与 LEF 中 PIN 几何相交：
\begin{lstlisting}
RegionCDEF FULLCHIP metal6 VDD_X 1.0
BlockA PIN via4 GND_X 0.35
BlockA PIN via4 VDD_X 0.42
BlockB PIN metal3 VDD_X 0.72
\end{lstlisting}
BlockA 内与 LEF PIN 相交的 via4 合计 0.35\,A；BlockB 内与 PIN 相交的 metal3/via2/via3 合计 0.72\,W。
"""

CH04_EXPAND_IR_FIX = r"""
\paragraph{示例 IR 案例}
图~\ref{fig:ir-original} 为原始 IR 图。最差 Vdd--Vss 差 1.1073\,V，位于芯片左上高功耗区。日志示例：
\begin{lstlisting}
The worst IR drop of the top cover cell
voltage = 1.1073 at node (2679.182500,2737.390000)
\end{lstlisting}
自顶部延伸的 metal4 strap 与左侧 metal6 strap 对高功耗实例供电不足。

\paragraph{修改 pad 步骤}
\begin{enumerate}
  \item \textbf{Edit $\rightarrow$ Add Pad} 在两条 metal4 strap 上各加一个 pad（图~\ref{fig:add-pads}）
  \item 在 metal6 strap 上再加一个 pad
\end{enumerate}

\paragraph{加 metal6 strap 详细步骤}
\textbf{Edit $\rightarrow$ Add Power Strap}：
\begin{itemize}
  \item 取消「Add strap by text input」，使用绘制输入
  \item 选择竖向（Vertical）电源 strap
  \item 宽度 20\,\textmu m
  \item Stack via top：metal6；bottom：metal4
  \item Strap metal layer：metal6
  \item 在 metal4 上绘制后 Commit
\end{itemize}
重跑提取与静态分析后，最差差仅降至 1.1076\,V，改善很小。

\paragraph{金属电阻率敏感性}
将 tech 中 metal6 电阻率从 0.027 改为 0.014，重跑提取、\textbf{Power$\rightarrow$Import} 与静态分析，最差 1.109\,V，略有改善。说明可考虑更高金属层或 flip-chip 封装。
"""

# ---------------------------------------------------------------------------
# Chapter 5 expansion blocks
# ---------------------------------------------------------------------------

CH05_INSERT_AD = r"""
\subsubsection{Accelerated Dynamic（AD）分析}
\paragraph*{Accelerated Dynamic (AD) Analysis}

\textbf{Accelerated Dynamic（AD）} 适用于设计早期、信息尚不完整时的快速原型，\textbf{不能}替代签核用标准 vectorless 分析：
\begin{itemize}
  \item 仿真加速约 5--6 倍
  \item DvD 精度平均降低约 10--15\%
  \item 热点位置与趋势不变
\end{itemize}
AD 与标准 vectorless 的输入数据与 GSR 设置相同。
"""

CH05_INSERT_EVA = r"""
\paragraph{\gsr{EVA_PG_AWARE}}
设 \gsr{EVA_PG_AWARE 1} 且 \gsr{TOGGLE_RATE 0} 时，可分析 P/G 薄弱区域内实例的预期开关行为（见附录 C「\gsr{EVA_PG_AWARE}」）。
"""

CH05_EXPAND_CLOCK_GATE = r"""
\paragraph{推断时钟门与级联模式}
\gsr{CLOCK_GATE_ENABLE_RATIO} 默认同时影响实例化时钟门（lib 定义）与推断时钟门（如用作时钟门的 AND 门）。若不希望推断门影响时钟翻转率，可单独设置：
\begin{lstlisting}
STATE_PROPAGATION {
    PROPAGATION_MODE probability
    CLOCK_GATE_ENABLE_RATIO <ratio>
    INFERRED_CLOCK_GATE_ENABLE_RATIO <ratio>
}
\end{lstlisting}
设 \gsr{INFERRED_CLOCK_GATE_ENABLE_RATIO 1} 表示推断门不影响时钟翻转率。

\textbf{级联与非级联：}默认非级联（与传统 GOP 一致）——各门使用统一 enable ratio。级联模式下，任一门处的 gating ratio 取决于上游门及其开关概率，更贴近实际。启用级联：
\begin{lstlisting}
STATE_PROPAGATION {
    PROPAGATION_MODE probability
    CLOCK_GATE_ENABLE_RATIO <ratio>
    ENABLE_CASCADED_CLOCK_GATING 1
}
\end{lstlisting}

可用 \gsr{CLOCK_GATE_ENABLE_RATIO_FILE} 为指定时钟门指定自定义 enable ratio；文件格式：
\begin{lstlisting}
#<clock_gate_name> <enable_ratio>
...
\end{lstlisting}

\paragraph{ON/OFF 方法详解}
\gsr{FLOP_ON_PERCENTAGE <FOP>}（原 GOP 更名）控制\textbf{触发器开启比例}，而非时钟门数量。FOP=0.5 表示约 50\% 的 flop 处于 ON，由 PowerStream 根据各时钟门控制的 flop 数量决定哪些门必须 ON。\gsr{FOP_CONTROL_FILE} 格式：
\begin{lstlisting}
#<clock_gate_name> <ON/OFF>
...
\end{lstlisting}
若同时使用 GOP（已过时）与上述设置，将显示警告。
"""

CH05_EXPAND_RTL_VCD = r"""
\paragraph{约束文件补充说明}
最大翻转率为 2.0（每周期 0$\rightarrow$1 与 1$\rightarrow$0 各一次）；满活动时钟为 2。\gsr{SP_CLKMUX_AUTO 1} 可向 MUX 传播翻转率 2 而无需单独设置 Select pin。

无 VCD 时，\gsr{STATE_PROPAGATION} 仍可根据约束文件或默认翻转率传播；约束文件可指定时钟根、主输入与寄存器输出的翻转率。存储器须同时包含输入与输出翻转计数。设置完成后，静/动态分析无需额外命令。

\paragraph{RTL VCD 报告文件说明}
\begin{itemize}
  \item \texttt{adsRpt/vcd\_uncovered\_syms}：VCD 中存在但设计中不存在的符号
  \item \texttt{adsRpt/vcd\_uncovered\_mems}：VCD 未覆盖的存储器实例
  \item \texttt{adsRpt/vcd\_uncovered\_ffs}：未覆盖且不在时钟网中的 FF/latch
  \item \texttt{adsRpt/vcd\_uncovered\_clk\_ffs}：未覆盖且在时钟网中的 FF/latch
\end{itemize}
\gsr{PS_RTL_EP_REPORT} 开启时还生成：
\begin{itemize}
  \item \texttt{vcd\_covered\_ffs}：VCD/FSDB 中至少一个输出被覆盖的 FF/latch
  \item \texttt{vcd\_covered\_nets}：被覆盖的网络
  \item \texttt{propagated\_insts} / \texttt{propagated\_nets}：经传播得到活动的实例/网络
\end{itemize}
"""

CH05_EXPAND_GATE_VCD = r"""
\paragraph{BLOCK\_VCD\_FILE 参数说明}
\begin{itemize}
  \item \texttt{<Hierarch\_path/DEF\_instance\_name> <VCD file>}：与 DEF 一致的层次块名及 VCD/FSDB 路径
  \item \texttt{FILE_TYPE}：\texttt{VCD|FSDB|RTL\_VCD|RTL\_FSDB}
  \item \texttt{FRONT_PATH} / \texttt{SUBSTITUTE_PATH}：路径替换以匹配 DEF 层次
  \item \texttt{FRAME_SIZE}：逐周期功耗每帧时长（ps），默认 5000\,ps（$1/\text{FREQ}$）
  \item \texttt{START_TIME}：分析起始时间（ps）；默认 0，结束默认为 VCD/FSDB 末尾
  \item \texttt{TRUE_TIME}：0 用 STA、无 glitch；1 用 VCD 开关与时序
  \item \texttt{MAPPING}：RTL VCD 实例名到 DEF 名的映射文件
\end{itemize}
"""

CH05_EXPAND_VCD_DYN = r"""
\paragraph{VCD 关键周期选择}
RedHawk 逐周期计算功耗并找出最高功耗周期；时间跨度由 \gsr{DYNAMIC_SIMULATION_TIME} 决定；以小步长滑动窗口扫描。关键周期有序列表写入 \texttt{adsRpt/worst\_power\_cycle.rpt}。支持 True-time 与非 True-time 的门级/RTL VCD 功耗计算。

\paragraph{PRUNE 特性（RTL VCD）}
在 \gsr{VCD_FILE} 中设 \texttt{PRUNE 1} 可加速 RTL\_VCD 周期选择：
\begin{itemize}
  \item 无事件传播——直接从设计提取网权重，翻转网决定周期功耗
  \item 无延时计算——假定网翻转立即引起下游翻转
  \item 仅 VCD 覆盖网——适合 RTL-VCD 覆盖率常 $<$10\% 的情形
  \item 分块 pruning（多块 RTL-VCD 时按块分别处理）
  \item RTL-VCD 文件复用（重复块复用 pruning 结果）
  \item 支持 \gsr{WORST_DPDT_CYCLE}、\gsr{STA_VCD_FREQ_RATIO}、\gsr{POWER_VCD_NUM_PROCESS}
\end{itemize}
最有效条件：VCD 数据量大、功耗渐进变化、偶发脉冲式高峰。示例：
\begin{lstlisting}
VCD_FILE {
    core_top top.vcd
    FILE_TYPE RTL_VCD
    PRUNE 1
    SELECT_RANGE 10000 100000
}
\end{lstlisting}

\paragraph{混合模式时间示例说明}
上节 GSR 示例中 \texttt{ABCD10\_SEL}：presim 90--100\,ns，仿真 100--120\,ns；\texttt{ABCD20\_TEG}：presim 590--600\,ns，仿真 600--620\,ns；其余设计按 vectorless 处理。
"""

CH05_EXPAND_GATED = r"""
\paragraph{门控比自动推导与 \gsr{PS\_SP\_GATED\_CLOCK\_LOGIC}}
状态传播可根据各 enable 网 duty cycle 自动推导每级时钟门的 gating ratio；RTL\_VCD 流有利于时序逻辑功耗精度，vectorless 流有利于芯片总功耗估计。\gsr{PS_SP_GATED_CLOCK_LOGIC 0} 可禁用该自动 duty cycle 传播。

\gsr{SP_CLOCK_GATING_RATIO <ratio>}（0--1）可为全设计时钟门设全局 gating ratio。\gsr{GATED_ON_PERCENTAGE} 在叶级统计 flop/latch/存储器（含常开叶单元）；例如 0.5 表示随机约 50\% 门控控制单元为 ON，但动态分析中时钟网功耗未必精确缩至 50\%，取决于门控粒度。\gsr{GATED_CONTROL_FILE} 可逐实例覆盖全局 ON 设置。

\gsr{POWER_TRANSIENT_ANALYSIS} 可为各时间帧定义不同门控活动；多时间帧表示不同周期组上的时钟活动。\gsr{GATED_CLOCK_COVERAGE 1} 在使用 \gsr{GATED_ON_PERCENTAGE} 时提高覆盖率，并为每帧选择不同开门场景；须同时开启 \gsr{POWER_TRANSIENT_ANALYSIS}。

\paragraph{GCControls 文件字段}
\texttt{adsRpt/state\_propagation.GCControls} 每行：
\texttt{<gc\_instance\_name> <cell\_type> [On|Off] <user\_setting> <On\_fraction>}。其中 \texttt{user\_setting}：0=无用户设置，1=用户设为 On，2=用户设为 Off；\texttt{On\_fraction} 为静态分析时该门的 On 百分比/100，动态分析为到该门为止的累积 On 百分比（升序）。
"""

CH05_EXPAND_SCAN = r"""
\paragraph{Scan 模式关键特性（早期 vectorless）}
\begin{itemize}
  \item Scan FF 翻转由输入 pattern 推导并传播到组合逻辑
  \item Pattern 可简单（如 ``1010'' 压力 pattern）或由 ATPG 生成
  \item 全网活动确定性（非随机）
  \item 非 true-time：开关顺序由 PowerStream 决定，时刻由 STA 标注
  \item 按 scan 输出驱动数据 pin，行为来自 LIB
  \item \gsr{DYNAMIC_SIMULATION_TIME}、\gsr{PRESIM_TIME} 有效
\end{itemize}

\paragraph{Pattern 与链长}
Pattern 短于链长则重复；未指定 pattern 默认 ``0101…''。Pattern 文件可为每行一位：
\begin{lstlisting}
0
1
1
0
...
\end{lstlisting}
或单行：\texttt{0110...}。

\paragraph{Pattern 移位示例}
10 级 scan 链、pattern ``1001'' 重复为 ``1001100110''。仿真初态与各时钟沿后寄存器值示例：
\begin{verbatim}
0 1 1 0 0 1 1 0 0 1  - 仿真开始
0 0 1 1 0 0 1 1 0 0  - 第一时钟沿后
1 0 0 1 1 0 0 1 1 0  - 第二时钟沿后
\end{verbatim}

\paragraph{门级 VCD scan 模式}
与功能模式门级 VCD 动态分析相同（见「VCD 动态分析」）；可选最差功耗或最差 DvD 周期；活动来自所选周期的 VCD，动态分析复现 VCD 场景。
"""

CH05_EXPAND_DVD_EVAL = r"""
\paragraph{最差 DvD 实例列表排序}
\textbf{Results $\rightarrow$ List of Worst DVD Instances for Dynamic Simulation} 可按以下任一判据排序：
\begin{itemize}
  \item Ave DV / Max DV / Min DV / Min DV WC
  \item Max VDD-VSS、Min VDD-VSS（整周期）
  \item Min VDD-VSS over timing window、Avg VDD-VSS over timing window
\end{itemize}

\paragraph{动态实例结果视图}
\textbf{View $\rightarrow$ Dynamic Instance Result} 可选：线基压降图、实例基压降图、decap（DD）、动态功耗密度（PD）。注意各视图差异。

\paragraph{plot current 命令}
\begin{lstlisting}
plot current [-vdd|-gnd|-pwr|-net ?-name <nets>?|
     -pad ?-name <pads>?] ?-o <output>? ?-sv? ?-xgr?
\end{lstlisting}
\texttt{-vdd|-gnd|-pwr|-pad} 绘制对应电流波形；\texttt{-net}/\texttt{-pad} 未给名单时显示全部网或 pad。默认 Ansys \texttt{sv} 格式；\texttt{-xgr} 使用 Xgraph。

\paragraph{\gsr{DVD_GLITCH_FILTER}}
可按电压电平与 glitch 宽度 \texttt{WminW} 过滤 timing window 内 minTW（见图~\ref{fig:glitch-filter}）。报告 \texttt{adsRpt/Dynamic/<design>.minTW\_filtered}。详见附录 C「\gsr{DVD_GLITCH_FILTER}」。
"""

CH05_EXPAND_TCL = r"""
\begin{table}[htbp]
\centering
\caption{动态 DvD 分析 TCL 命令（详）}
\small
\begin{tabularx}{\textwidth}{@{}lX@{}}
\toprule
TCL & 用途 \\
\midrule
\cmd{setup vcd} \texttt{?<vcd\_cycle\_time>? ?-a <start>?<end>? ?-w <logical\_path> <physical\_path>? ?-d <adsPower>? ?-o <out>? ?-msg ?-cmd ?-tt <presim\_ps>?} &
当 GSR 含 \gsr{VCD_FILE} 时配置全 VCD 动态 DvD：周期时间、起止仿真时间、逻辑/物理路径映射、adsPower 目录、输出/消息/命令文件、presim 时间（ps）等 \\
\cmd{perform analysis [-lowpower | -vcd | -vectorless]} &
运行动态 DvD；\texttt{-vcd} 用于 VCD/scan 场景；\texttt{-vectorless} 用于 vectorless；\texttt{-lowpower} 用于低功耗流（见第 13 章） \\
\bottomrule
\end{tabularx}
\end{table}
"""

# ---------------------------------------------------------------------------
# Chapter 6 expansion blocks
# ---------------------------------------------------------------------------

CH06_EXPAND_POWER = r"""
\paragraph{power\_summary.rpt 字段说明}
\begin{itemize}
  \item \texttt{Recommended dynamic simulation time}：建议的 \gsr{DYNAMIC_SIMULATION_TIME}，以覆盖大部分功耗事件
  \item 按频率域、Vdd 域、单元类型列出 \texttt{total\_pwr}、\texttt{leakage\_pwr}、\texttt{internal\_pwr}、\texttt{switching\_pwr} 及占总功耗百分比
  \item \texttt{clocked\_inst}：有 clock pin 但无法归类为 latch\_and\_FF、memory 或 I/O 的实例
  \item \texttt{Total chip power}：含核与其它域的总功耗
  \item \texttt{Total clock network only power} / \texttt{Total clock power}：仅时钟网络 / 含 FF-latch clock pin 的时钟功耗
\end{itemize}
"""

CH06_EXPAND_IVDD = r"""
\paragraph{\texttt{<design>.ivdd} 示例}
无封装时测量设计 pad 电流（含片上寄生、decap 等）；有封装时测量封装外电压源电流（另含封装寄生）：
\begin{lstlisting}
Time                 i(vdd)
0.000000           0.0
-3490.0000         0.00265285
-3480.0000         0.0036665
-3470.0000         0.00341904
...
\end{lstlisting}
"""

CH06_EXPAND_SWITCH_DYN = r"""
\paragraph{\texttt{switch\_dynamic.rpt} 示例（vectorless）}
每行：实例名、开关类型、最差 Vdd-Vss、最大开关电压与电流：
\begin{lstlisting}
#<inst_name> <type> <worst_int_Vdd-Vss_Volt> <max_Vsw_Volt> <max_Isw_Amp>
QNP_1_BOTTOM_HS_CELL_083 H 1.051716 0.024256 0.004053
QNP_1_BOTTOM_HS_CELL_082 H 1.051716 0.025019 0.004180
...
\end{lstlisting}
"""

CH06_EXPAND_PAD = r"""
\paragraph{静态 \texttt{pad.current} 示例}
\begin{lstlisting}
#current      #pad_center_location                  #pad_name
2.4745        ( 65.282, 0.082)                  Vdd_130564_1645
2.1274        ( 163.329, 0.082)                 Vdd_326658_1645
...
\end{lstlisting}

\paragraph{动态 \texttt{pad.current} 示例}
\begin{lstlisting}
Vss1
-1750 -1.13646e-05
-1740 -0.00240712
...
0   -0.0506185
Vdd1
-1750 1.13646e-05
...
\end{lstlisting}
"""

CH06_EXPAND_CMM = r"""
\paragraph{动态 CMM 违例报告示例}
\begin{lstlisting}
# Top connection min voltage constraint violation:
ABC_CORE/ram64/adsU1 ram32x8x2 (1759.3600,783.0350, METAL2) VDD 1.7820 1.7309
# Top connection max voltage constraint violation:
ABC_CORE/ram64/adsU1 ram32x8x2 (1763.9600,778.4350, METAL2) VSS 0.0010 0.0528
# Pin min voltage constraint violation:
ABC_CORE/ram64/adsU1:VDD ram32x8x2 (1792.3700,727.8150) 1.7460 1.7294
\end{lstlisting}

\paragraph{静态 CMM 违例报告示例}
\begin{lstlisting}
# Top connection IR constraint violation:
ABC_CORE/ram64/adsU1 ram32x8x2 (1759.3600,783.0350, METAL2) VDD 1.7960 1.7909
# Pin IR constraint violation:
ABC_CORE/ram64/adsU1:VDD ram32x8x2 (1792.3700,727.8150) 1.7910 1.7909
\end{lstlisting}
"""

CH06_EXPAND_DEBUG = r"""
\paragraph{\texttt{apache.slew0} 说明}
列出时序文件中缺 slew 的实例：时序单元报告 CLK/OUT pin；组合单元报告 IN/OUT pin。
"""


def insert_after(text: str, marker: str, insertion: str) -> str:
    if marker not in text:
        print(f"  WARN: marker not found: {marker[:60]}...")
        return text + "\n" + insertion
    return text.replace(marker, marker + insertion, 1)


def replace_section(text: str, start_marker: str, end_marker: str, new_content: str) -> str:
    i = text.find(start_marker)
    if i < 0:
        print(f"  WARN: start not found: {start_marker[:50]}")
        return text
    j = text.find(end_marker, i + len(start_marker))
    if j < 0:
        print(f"  WARN: end not found after: {start_marker[:50]}")
        return text
    return text[:i] + new_content + text[j:]


def refine_ch04() -> int:
    path = CH / "04_power_static_em.tex"
    text = path.read_text(encoding="utf-8")

    text = insert_after(
        text,
        "设 \\gsr{GSC_OVERRIDE_IPF 1} 可让 GSC 覆盖 IPF（默认 0）。",
        CH04_INSERT_AFTER_GSC,
    )
    text = insert_after(
        text,
        "（见下文 VCD 功耗计算设置）。",
        CH04_INSERT_AFTER_TOGGLE_PRIO,
    )
    # Expand BPA section
    text = replace_section(
        text,
        "\\subsection{BLOCK\\_POWER\\_ASSIGNMENT}",
        "\\subsection{MMX Pin 区域与 OBS、Decap}",
        CH04_EXPAND_BPA,
    )
    text = insert_after(
        text,
        "\\textbf{DECAP\\_CELL + BPA}：可创建/实例化 decap 块；",
        CH04_EXPAND_DECAP.split("### 创建去耦单元")[1] if False else "",
    )
    # Replace abbreviated decap/early sections
    old_decap = "\\subsection{早期 decap 估计与报告}\n\\subsubsection*{Early Stage Decap Estimation and Reports}"
    if old_decap in text:
        text = text.replace(
            old_decap,
            CH04_EXPAND_DECAP + "\n\\subsection{早期 decap 估计与报告（摘要）}\n\\subsubsection*{Early Stage Decap Estimation and Reports}",
            1,
        )
    text = replace_section(
        text,
        "\\subsection{示例分析案例}",
        "\\section{评估静态 IR 结果}",
        "\\subsection{示例分析案例}\n\\subsubsection*{Example Analyses}\n\n"
        + CH04_EXPAND_CASES
        + "\n",
    )
    text = insert_after(
        text,
        "说明可加更高金属层或改用 flip-chip。",
        CH04_EXPAND_IR_FIX,
    )

    path.write_text(text, encoding="utf-8")
    return len(text.splitlines())


def refine_ch05() -> int:
    path = CH / "05_dynamic_vd.tex"
    text = path.read_text(encoding="utf-8")

    text = insert_after(
        text,
        "两者输入与设置相同。",
        CH05_INSERT_AD,
    )
    text = insert_after(
        text,
        "  \\item GSC 中可定义布尔多状态（见附录 C GSC）",
        CH05_INSERT_EVA,
    )
    text = insert_after(
        text,
        "与 \\cmd{setup analysis_mode static} + GOP 等效但 GOP 已过时。",
        CH05_EXPAND_CLOCK_GATE,
    )
    text = insert_after(
        text,
        "\\gsr{SP_CLKMUX_AUTO 1} 可向 MUX 传播翻转率 2 而无需单独设置 Select pin。",
        CH05_EXPAND_RTL_VCD,
    )
    text = insert_after(
        text,
        "\\subsection{VCD 动态分析}",
        CH05_EXPAND_GATE_VCD,
    )
    text = insert_after(
        text,
        "\\textbf{RTL VCD PRUNE：}",
        CH05_EXPAND_VCD_DYN,
    )
    text = insert_after(
        text,
        "检查：时钟树 \\texttt{.lib}/LEF 完整；",
        CH05_EXPAND_GATED,
    )
    text = insert_after(
        text,
        "\\textbf{门级 VCD scan：}",
        CH05_EXPAND_SCAN,
    )
    text = insert_after(
        text,
        "默认 Ansys \\texttt{sv} 格式；\\texttt{-xgr} 用 Xgraph。",
        CH05_EXPAND_DVD_EVAL,
    )
    text = replace_section(
        text,
        "\\section{运行动态压降的 TCL 命令}",
        "",
        "\\section{运行动态压降的 TCL 命令}\n\\subsection*{TCL Commands to Run Dynamic Voltage Drop Analysis}\n\n"
        + CH05_EXPAND_TCL,
    )

    path.write_text(text, encoding="utf-8")
    return len(text.splitlines())


def refine_ch06() -> int:
    path = CH / "06_reports.tex"
    text = path.read_text(encoding="utf-8")

    text = insert_after(
        text,
        "clock network and FF/latch clock pin power, 0.005992 Watt.",
        CH06_EXPAND_POWER,
    )
    text = insert_after(
        text,
        "有封装时，ivdd 测量封装外电压源处电流，另含封装寄生。",
        CH06_EXPAND_IVDD,
    )
    text = insert_after(
        text,
        "可快速查看哪些开关已 ON 及其效率。",
        CH06_EXPAND_SWITCH_DYN,
    )
    text = insert_after(
        text,
        "\\subsection{Pad 电流文件}",
        CH06_EXPAND_PAD,
    )
    text = insert_after(
        text,
        "pin IR constraint violation",
        CH06_EXPAND_CMM,
    )
    text = insert_after(
        text,
        "\\texttt{apache.slew0} & 时序文件中缺 slew 的 instance \\\\",
        CH06_EXPAND_DEBUG,
    )

    path.write_text(text, encoding="utf-8")
    return len(text.splitlines())


def count_sections(path: Path) -> list[str]:
    return [
        ln.split("{")[1].split("}")[0]
        for ln in path.read_text(encoding="utf-8").splitlines()
        if ln.startswith("\\section{")
    ]


def main() -> None:
    print("Refining RH_CN chapters 04-06...")
    n4 = refine_ch04()
    n5 = refine_ch05()
    n6 = refine_ch06()
    for fname, n in [
        ("04_power_static_em.tex", n4),
        ("05_dynamic_vd.tex", n5),
        ("06_reports.tex", n6),
    ]:
        secs = count_sections(CH / fname)
        print(f"  {fname}: {n} lines, {len(secs)} sections")
        for s in secs:
            print(f"    - {s}")


if __name__ == "__main__":
    main()
