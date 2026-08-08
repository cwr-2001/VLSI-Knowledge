# -*- coding: utf-8 -*-
"""Expand RH_CN chapters 07, 08, 13, 14 to full faithful translation depth."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "chapters"


def insert_after(text: str, marker: str, block: str) -> str:
    if marker not in text:
        raise ValueError(f"Marker not found: {marker!r}")
    return text.replace(marker, marker + block, 1)


# ---------------------------------------------------------------------------
# Chapter 07 expansions
# ---------------------------------------------------------------------------

CH07_AFTER_DECAP_PREP = r"""
\paragraph{DECAP\_CELL 与 LEF 物理定义示例}
\gsr{DECAP_CELL} 通常仅需列出 decap 单元名，其余信息在 LEF 中定义。LEF 中 decap 宏须含完整 P/G pin 定义，例如：
\begin{lstlisting}
MACRO cell_name
    CLASS <class_type> ;
    ORIGIN <value> ;
    SIZE <value> BY <value> ;
    PIN GND
        USE GROUND ;
        PORT
            LAYER <layer_name> ;
            RECT <x1> <y1> <x2> <y2> ;
        END
    END GND
    PIN VDD
        USE POWER ;
        PORT
            LAYER <layer_name> ;
            RECT <x1> <y1> <x2> <y2> ;
        END
    END VDD
END cell_name
\end{lstlisting}
"""

CH07_AFTER_CELL_SWAP = r"""
\paragraph{\cmd{cell swap} 选项详述}
\begin{itemize}
  \item \opt{-eco <file\_name>}：写出描述设计变更的 ECO 文件名
  \item \opt{-decap\_cells \{cell1 ...\}}：可与热点 instance 交换的 decap master 单元；默认任意无逻辑连接单元可交换。\opt{-glob} 允许通配符；\opt{-regexp} 允许正则；\opt{-exact} 精确单元名
  \item \opt{-fixed\_cells \{...\}}：禁止参与交换的 master 单元
  \item \opt{-fixed\_insts \{...\}}：禁止参与交换的 instance
  \item \opt{-removable\_cells \{...\}}：必要时可从设计中移除的 decap 单元（默认不可移除）；同样支持 \opt{-glob/-regexp/-exact}
  \item \opt{-include\_clock}：允许交换时钟单元
  \item \opt{-inst\_list \{...\}} / \opt{-inst\_file <file>}：仅对列出的 instance 执行交换
  \item \opt{-search\_only}：仅生成候选 instance 列表（默认 \texttt{cell\_swap\_<time>.list}），不执行交换；可用 \opt{-inst\_file} 改名
  \item DvD 准则：\opt{-eff\_vdd\_tw}（TW 上平均有效电压，默认）、\opt{-max\_vdd\_tw}、\opt{-min\_vdd\_tw}、\opt{-min\_vdd\_all}（整周期最小有效电压）
  \item \opt{-report}：生成 \texttt{adsRpt/cell\_swap.rpt} 文本表；\opt{-plot}：生成 \texttt{adsRpt/cell\_swap.hist} 直方图
\end{itemize}

\paragraph{Cell Swapping 报告日志示例}
\begin{lstlisting}
*******************************************************************************
**** FAO Cell Swapping Report
*******************************************************************************
Cell Swapping Result Summary
   Total swapping instance number : 2182
   Actually Moved instance number : 436
   Actually Deleted instance number: 0
   maximum voltage change (mv)                      : 171
   minimum voltage change (mv)                      : -18
**** Please see adsRpt/cell_swap.rpt for detail DvD change.
**** To view histogram of DvD change, please execute xgraph
adsRpt/cell_swap.hist.
MEMORY USAGE: 2265 MBytes
TOTAL CPU TIME: 1 hrs 17 mins 52 secs
WALLTIME: 1 hrs 27 mins 56 secs.
*******************************************************************************
\end{lstlisting}

\paragraph{控制 \cmd{cell swap} 的 GSR 关键字}
\begin{itemize}
  \item \gsr{fao\_region}：含高功耗 instance 的目标分析区域
  \item \gsr{fao\_nets}：多 VDD 设计时指定热点 instance 关联的 VDD 网
  \item \gsr{noise\_limit}：对最差热点列表，低于该压降百分比阈值的热点不参与交换（例：5\% 表示压降 $<$5\% 的热点忽略）
  \item \gsr{num\_hotinst}：区域内交换的最差热点 instance 数
  \item \gsr{fix\_window}：以各热点为中心的可移动/交换区域尺寸（默认 40$\times$40\,$\mu$m）
  \item \gsr{fao\_verbose}（0/1）：控制输出消息量（默认 0）
\end{itemize}
"""

CH07_EXPAND_EX_GH = r"""
\paragraph{示例 G 详细步骤与日志}
\begin{enumerate}
  \setcounter{enumi}{2}
  \item FAO 评估期间报告目标 DvD，例如：
\begin{lstlisting}
|Target Worst Average DvD percent over TW: 24.1895%(0.27576)(v.s. Vdd=1.14)
\end{lstlisting}
  表示目标 276\,mV 对应 Vdd 的 24.2\%；测量值为 TW 上最差平均 DvD（STA 给出的门可能开关时间窗）。
  \item FAO 自动迭代放置 decap 并报告，例如首轮：
\begin{lstlisting}
Placed decap cells for 29 hot instances.
Added decap 5.092 pF
\end{lstlisting}
  第二轮累计：
\begin{lstlisting}
Placed decap cells for 29 hot instances.
Added decap 204.718 pF
\end{lstlisting}
  \item 重跑提取与动态分析验证：
\begin{lstlisting}
perform extraction -power -ground -c
setup pad -power -r 0.005 -ground -r 0.005
setup wirebond -power -r 0.001 -l 1000 -ground -r 0.001 -l 1000
setup package -r 0.001 -l 250 -c 5
perform analysis -vectorless
\end{lstlisting}
  本例 DvD 改善至 284\,mV（目标 276\,mV）。
  \item \cmd{decap report} 完整报告示例：
\begin{lstlisting}
*************************************************************
****   FAO Decap Report on top Hot Instances
*************************************************************
Inserted Decap Inst Num : 3579
Inserted Decap Total      : 209.81 pF
V0/V1 : Average (VDD - GND) over TW before/after decap placement.
DvD0/DvD1 : Dynamic Voltage Drop (VDD - V0/V1) before/after decap
placement. Improvement % : (DvD0 - DvD1)/DvD0 %.
inst    V0    V1     DvD0     DvD1    Improvement%
-------------------------------------------------
INFO(FAO-75): inst194510 : 0.8343 0.8568 0.3057 0.2832 7.36017%
INFO(FAO-75): inst117100 : 0.8346 0.8574 0.3054 0.2826 7.46563%
INFO(FAO-75): inst76925 : 0.8395 0.8607 0.3005 0.2793 7.05491%
--------------------------------------
New Top Hot Instances:
inst    &   avgVoltage_TW
--------------------------------------
inst194510 0.8568
inst117100 0.8574
inst76925 0.8607
--------------------------------------
Overall DvD improvement = 7.3601 % v.s. initial DvD
\end{lstlisting}
  \item 在 ECO 中高亮新增 decap：\cmd{select add "decap*" -glob -linewidth 3}
  \item 将剩余改善量（本例 2.64\%）赋给网格修复：\cmd{gsr set noise\_reduction 2.64}，再运行 \cmd{mesh optimize} 或 \cmd{mesh fix}
\end{enumerate}

\paragraph{示例 H 完整 decap 重叠报告}
\begin{lstlisting}
**********************************************************
****      FAO Decap Report on top Hot Instances
**********************************************************
Inserted Decap Inst Num : 305
Inserted Decap Total             : 229.938 pf
V0/V1 : Average (VDD - GND) over TW before/after decap fix.
DvD0/DvD1:Dynamic Voltage Drop (VDD - V0/V1) before/after decap fix.
Improvement % : (DvD0 - DvD1)/DvD0 %.
     inst                       V0     V1 DvD0 DvD1 Improvement%
--------------------------------------------------------
INFO(FAO-75): inst117100 : 0.8346 0.8573 0.3054 0.2827 7.43288%
INFO(FAO-75): inst194510 : 0.8344 0.8609 0.3056 0.2791 8.67146%
INFO(FAO-75): inst76925 : 0.8396 0.8623 0.3004 0.2777 7.55658%
-------------------------------------------------------
New Top Hot Instances:
inst       &    avgVoltage_TW
-------------------------------
inst117100 0.8573
inst194510 0.8609
inst76925 0.8623
-------------------------------
Overall DvD improvement = 7.73499 % v.s. initial DvD
\end{lstlisting}
"""

CH07_GSR_EXPAND = r"""
\subsection{FAO GSR 关键字详述}
\subsubsection*{Detailed FAO GSR Keywords}

\paragraph{\gsr{FAO\_DYNAMIC\_MODE}}
选择静态 IR 或动态 DvD 分析作为 FAO 优化依据。\texttt{[0|1]}，默认 0（静态）。

\paragraph{\gsr{FAO\_TURBO\_MODE}}
选择 accurate 或 turbo 搜索模式。默认 on（turbo）；设为 0 使用 accurate 模式，精度更高但更慢。

\paragraph{\gsr{FAO\_RANGE}}
指定各金属层允许的新导线宽度范围（$\mu$m）：
\begin{lstlisting}
FAO_RANGE { {metal6 8 29.4} {metal5 4 12} }
\end{lstlisting}
放宽压降（负 \gsr{noise\_reduction}）时范围须小于现有宽度；收紧压降时须增大上限。

\paragraph{\gsr{FAO\_LAYERS}}
指定参与优化的层与方向约束：
\begin{lstlisting}
FAO_LAYERS { {metal6 hor <= 29.4} {metal5 ver} }
\end{lstlisting}
支持 \texttt{hor/ver}、宽度比较运算符（\texttt{<=}、\texttt{>=} 等）。

\paragraph{\gsr{MESH\_SEARCH}}
指定各层压降降低百分比分配（默认各选定层均分）：
\begin{lstlisting}
MESH_SEARCH { {metal6 60} {metal5 40} }
\end{lstlisting}

\paragraph{\gsr{FAO\_WIDTH\_CNSTR}}
定义层间宽度关系约束（可选）。

\paragraph{\gsr{FAO\_SUB\_GRID\_NETS} / \gsr{FAO\_SUB\_GRID\_SPEC}}
\cmd{mesh sub\_grid} 所用：子网格电源网列表及物理特性（pitch、方向等）。

\paragraph{\gsr{FAO\_DRC} / \gsr{FAO\_DRC\_OBS} / \gsr{FAO\_DRC\_PL\_OBS}}
控制 FAO 是否执行 DRC 检查：\gsr{FAO\_DRC} 总开关；\gsr{FAO\_DRC\_OBS} 为 1 时 decap 与 metal1 信号布线做 DRC；\gsr{FAO\_DRC\_PL\_OBS} 为 1 时遵守 DEF placement blockage。

\paragraph{\gsr{DECAP\_FILL}}
与 \cmd{decap qor} 配合，指定 decap 填充策略关键字（见附录 C）。
"""

# ---------------------------------------------------------------------------
# Chapter 08 expansions
# ---------------------------------------------------------------------------

CH08_PJX_EXPAND = r"""
\subsection{PJX Fullchip 与 Sign-Off 方案对比}
\subsubsection*{Comparison of Fullchip and Sign-Off Jitter Solutions}

RedHawk 提供两种互补的时钟抖动分析路径：
\begin{itemize}
  \item \textbf{PJX Fullchip（ATE 级）}——基于 STA 与 RedHawk 多周期有效电压的快速全芯片筛查；适合早期识别电压诱导抖动热点与网格薄弱区域；\textbf{不能}替代含 PI、SI 与其他抖动源的 SPICE 级 sign-off。
  \item \textbf{PJX Sign-Off（NX 级）}——多周期 Spice 仿真，并发考虑 P/G 噪声波形、耦合电容与单元级精度；用于 tape-out 前最终抖动 sign-off。
\end{itemize}

集成工作流：
\begin{center}
Setup Design $\rightarrow$ Power Calculation $\rightarrow$ Extraction $\rightarrow$ DvD Analysis $\rightarrow$ Fullchip Jitter Analysis $\rightarrow$ Sign-Off Analysis
\end{center}

\subsection{PJX Fullchip 长期抖动报告详解}
\subsubsection*{Long Term and Cycle-to-Cycle Jitter Reports}

\textbf{Long Term Jitter Report} 按各时钟域最坏长期抖动（占时钟周期百分比）排序。长期抖动定义为：对端点 pin 记录的所有到达时间，最早与最晚到达时间之差。

对选中时钟可执行：
\begin{itemize}
  \item \textbf{Show Summary}——最差 1000 个端点摘要；Show Browser 显示自源到端点的 schematic；Highlight 显示 flyline；Show Trace 显示路径详情（最早/最晚周期、路径 instance 周期电压、绝对抖动与占周期百分比）
  \item \textbf{Show Detail}——整个网络的 per-pin 抖动表，可搜索、浏览、高亮与缩放
  \item \textbf{Show Browser}——整个时钟网络的 schematic 连通，Highlight 在 GUI 显示全网 flyline
\end{itemize}

\textbf{Long Term Cycle-2-Cycle Jitter Report} 格式类似，但抖动量为相邻周期到达时间差的最大值。

\subsection{抖动配置关键字补充详述}
\subsubsection*{Additional Jitter Configuration Keyword Details}

\paragraph{\gsr{EXTEND\_CYCLE\_SELECTION}}
管理非连续周期集合，语法 \texttt{[-1 | 0 | 1]}：
\begin{itemize}
  \item \texttt{-1}：丢弃非连续周期（例：指定 10 15 16 17 时丢弃 10）
  \item \texttt{0}：保留原样（10 15 16 17）
  \item \texttt{1}：补充周期使序列连续（按 worst-best-worst/best-worst-best 排序添加 9--11 或 10--12 等）
\end{itemize}

\paragraph{\gsr{DEFINE\_CASE\_ANALYSIS}}
降低串扰悲观度，可选 \texttt{pgvolt}、\texttt{clock\_jitter\_worst}、\texttt{clock\_jitter\_best}（默认 \texttt{PGVOLT}）。

\paragraph{\gsr{JITTER\_FAST\_MODE}}
快速抖动仿真：\texttt{1} = 有效 DvD PWL；\texttt{2} = 多周期有效 VDD；\texttt{0} = 完整波形（默认）。

\paragraph{\gsr{CLK\_INST\_FILE} 文件格式}
\begin{lstlisting}
#| Clock Tree Instance Summary
# Root=CK1 Period=2000(ps) Freq=500.000(Mhz)
# InstName CellName (InstType) Freq EffVdd
T_buf1 zbfp (C_COMB) 500.000MHz
T_buf3 zbfp (C_COMB) 500.000MHz
...
# Buffer/Gate=29 Sequential(Total) Leafs=2(2)
\end{lstlisting}

\paragraph{\gsr{DYNAMIC\_SIMULATION\_CYCLES}}
列出或范围指定抖动仿真周期：
\begin{lstlisting}
DYNAMIC_SIMULATION_CYCLES { 10 15 16 17 }
DYNAMIC_SIMULATION_CYCLES { 10 : 20 }
\end{lstlisting}

\paragraph{\gsr{COUPLING\_CAP\_RATIO\_THRESHOLD}}
攻击者耦合电容占受害者总电容比例阈值，低于阈值不纳入耦合分析（默认 0.05）。

\paragraph{\gsr{COUPLING\_WINDOW\_MARGIN}}
以受害者 rise time 倍数扩展 TW 检查重叠（默认 1.0）。

\paragraph{\gsr{GROUP\_CLUSTERING} / \gsr{GROUP\_CLUSTERING\_DEPTH}}
聚类抖动仿真以加速：\texttt{ENABLE|DISABLE}（默认 DISABLE）；\gsr{GROUP\_CLUSTERING\_DEPTH} 为每簇最大逻辑层数（默认 3）。

\paragraph{\gsr{SIMULATION\_REDO\_MAX}}
PWL 对齐最大迭代次数（默认 10）。

\paragraph{边到边 DDR 抖动报告格式}
Report 1（\texttt{adsRpt/Jitter/edge\_to\_edge.jitter}）表头示例：
\begin{lstlisting}
# CLOCK : <clock pin name>
# DATA_1 : <data pin name>
# Ideal Bit Period : <ideal bit period>
CLOCK                    DATA_1
Rise Edge No   Setup Time (ps)   Hold Time (ps)   ...
Min tDS/tDH(ps)  <min setup>      <min hold>       ...
Edge-to-edge jitter (ps)           <jitter>
\end{lstlisting}

Report 2（\texttt{tree\_*\_pi/peak\_to\_peak.jitter}）按逻辑路径顺序列出各 instance pin 的周期与 C2C 抖动摘要。
"""

CH08_SKEW_EXPAND = r"""
\paragraph{Clock Tree Skew 文本报告目录结构}
Sign-off skew 分析输出至 \texttt{adsRpt/Clkskw}：
\begin{lstlisting}
|___adsRpt/Clkskw
        |___ skew.log / skew.err / skew.warn
        |___ tree_id_map
        |___ tree_<id>_<suffix>   # suffix: basic, pi, si, pisi
                 |___ tree.sdf
                 |___ tree.skw
                 |___ tree.leaf
                 |___ DomainRpt/subtree_*
\end{lstlisting}
临时文件在 \texttt{.apache/clkskw}。关闭 \texttt{DomainRpt}：\gsr{CLOCKTREE\_DOMAIN\_SPLIT\_REPORT 0}。

\paragraph{Skew 分析模式与配置文件覆盖关系}
\begin{itemize}
  \item \textbf{Basic}：\cmd{perform clockskew -config <f> -mode basic} 覆盖配置文件中 \gsr{POWER\_INTEGRITY 1}
  \item \textbf{仅 SI}：\gsr{SIGNAL\_INTEGRITY 1} + SPEF 含耦合电容 + \texttt{-mode basic}，同样覆盖 \gsr{POWER\_INTEGRITY 1}
  \item \textbf{仅 PI}：\texttt{-mode dynamic}（默认）或 \texttt{-mode static}，覆盖 \gsr{POWER\_INTEGRITY 0}
  \item \textbf{并发 PI+SI}：\texttt{-mode [static|dynamic]} 且 \gsr{SIGNAL\_INTEGRITY 1}，覆盖 \gsr{POWER\_INTEGRITY 0}
\end{itemize}

\paragraph{\gsr{PWL\_WAVEFORM}}
波形测量点（相对 Vdd 分数，升序），最多 10 点；延迟在 M 点，slew 在 L 与 H 之间。默认：0.1、L:0.3、M:0.5、H:0.7、0.9。
"""

# ---------------------------------------------------------------------------
# Chapter 13 expansions
# ---------------------------------------------------------------------------

CH13_MULTI_VDD = r"""
\subsection{多 Vdd 结果查看与报告}
\subsubsection*{Viewing and Reporting Multi-Vdd Results}

点击网表节点可查看该位置信息，消息窗口示例：
\begin{lstlisting}
Net: VDD
Wire: M2
LowerLeft = (3710.510, 4388.160)
Length: 101 um
Width: 1.46 um
Resistance: 6.95 Ohm
Voltage at query position: 1.595129 V
Current at query position: 0.000168779 A
\end{lstlisting}

点击 instance 示例：
\begin{lstlisting}
Instance: Test/U594
Cell: test1
LowerLeft = (3713.860, 4482.880), Width/Height = 5.220 / 4.639
Total Load Cap: 0.131 pF
Intrinsic Cap 0: 0 pF
Intrinsic Cap 1: 0 pF
Static Vdd-Vss: 1.592 V (domain vdd: 1.6000)
Average Pwr: 6.72e-10 W
\end{lstlisting}

\paragraph{P/G Arc 与 I/O 非对称电流}
单 instance 接多 VDD 时，须在自定义 LIB 或 APL 流程中定义 P/G arc 功率分配（见第~3~章与第~9~章）。I/O 单元同时接 I/O VDD、core VDD、I/O VSS 时，动态分析支持非对称电流轮廓，以正确反映 I/O 对 core 电源的影响。

\paragraph{最坏实例报告字段}
Results $\rightarrow$ List of Worst IR/DvD Instance 报告字段：
\begin{enumerate}
  \item 排名（全芯片最高压降 Top 1000）
  \item 最低 VDD-VSS 差
  \item 理想 VDD
  \item 坐标 (x, y)
  \item Instance 名
\end{enumerate}
在 Vdd Domain 组合框选择特定网表后点击 Apply 可过滤域。
"""

CH13_PG_EXPAND = r"""
\subsection{电源门控四态电气模型详解}
\subsubsection*{Detailed Four-State Switch Electrical Models}

每个开关区域须完整表征四种工作模式：

\paragraph{ON 态}
开关为低阻通路。静态/动态分析报告开关自身压降与电流。\texttt{aplsw} 生成含 ON/OFF/PowerUp/PowerDown 的模型文件。Header ON 态等效为 EXT\_PIN 与 INT\_PIN 间低 $R_{\mathrm{on}}$ 与 IDSAT 限制。

\paragraph{OFF 态}
由 instance 漏电与开关漏电决定内部节点平衡电压。OFF 分析为 ramp-up 提供初始条件。Footer OFF 态在 INT\_PIN 与 GND 间呈现高阻与寄生电容。

\paragraph{POWERUP 态}
上电动态：控制 pin 按 \texttt{POWER\_UP} 电压序列变化，开关电阻随栅压变化；\texttt{aplsw} 输出分段 PWL 电流（\texttt{PWL\_CURRENT}）描述浪涌。

\paragraph{POWERDOWN 态}
下电序列：\texttt{POWER\_DOWN} 定义控制 pin 波形，内部节点放电至 OFF 平衡态。

\paragraph{充电开关（Charge Switch）}
大电流开关，确保功能开关开启前内部电源达阈值。GSR：
\begin{lstlisting}
CHARGE_SWITCH {
    <charge_switch_inst> <threshold_voltage_V>
    ...
}
\end{lstlisting}

\paragraph{\texttt{charge\_switch.rpt} 报告格式}
\begin{lstlisting}
#Initial Function Switch Rampup Time (IFSRT): 10000
***** Charge Switch Report *****
[instance_name] [threshold] [voltage@IFSRT] [time_reach_SRT] [violation]
inst_CSW_VDD  0.7  0.293019  12970  Y
***** Functional Switch Report *****
#Time of last charge switch reaching SRT: 12970
[instance_name] [rampup_time] [violation]
fsw_inst_VDD-1  15000  N
\end{lstlisting}
字段：IFSRT 为功能开关规定的开启时间（ps）；\texttt{voltage@IFSRT} 为 ramp-up 时刻内部节点电压；\texttt{time\_reach\_SRT} 为达到阈值电压的时间；\texttt{violation Y} 表示超时。

\paragraph{双控制 pin 时序}
\texttt{POWER\_UP} 中一 pin 电压须与 \texttt{OFF\_STATE} 相同以确定触发顺序；\texttt{POWER\_DOWN} 同理。慢/非线性使能建议 \texttt{MD\_PWL 1}；\texttt{SPLIT\_MD\_PWL 1} 可并行加速表征。

\paragraph{GSC 块开关示例}
\begin{lstlisting}
sw_inst_A POWERUP
gated_block_B POWERUP
* domain_level POWERUP
sw_* POWERUP
\end{lstlisting}
"""

CH13_IP_EXPAND = r"""
\subsection{IP 开关宏模型关键字详述}
\subsubsection*{Switch Macro Model Keywords}

创建 IP 开关 LEF 时在 gds2def 配置中增加：
\begin{lstlisting}
LEF_FILES {
    <IP LEF file>
    <switch_cell_1>_adsgds.lef
    ...
}
USE_LEF_PINS_FOR_TRACING 1
SWITCH_CELLS {
    <sw1 cellname> <VDD1_INT>_ADS <VDD1_EXT>_ADS
    <sw2 cellname> <VDD2_INT>_ADS <VDD2_EXT>_ADS
}
VP_PAIRS {
    <vdd1_int> <vdd1_ext> <vdd2_int> <vdd2_ext>
}
\end{lstlisting}

\paragraph{\texttt{qswitch} 示例子电路输出}
\begin{lstlisting}
*-- extracted switch subckt for cell 'sw1'
.SUBCKT sw1 VDD1_EXT_ADS VDD1_INT_ADS PWRUP_ADS PWRON_ADS M0
+ VDD1_EXT_ADS POWERUP_ADS VDD1_INT_ADS ...
\end{lstlisting}

\paragraph{aplsw IP 开关模型片段}
\begin{lstlisting}
SWITCH_CELL sw1 {
    SWITCH_TYPE: HEADER
    EXT_PIN: VDD_EXT_ADS
    INT_PIN: VDD_INT_ADS
    CTRL_PIN: PWRUP_ADS F -
    ON:  R 30.1234  I 6.08777e-10  C 5.02222e-14  IDSAT 0.011111
    OFF: C 2.121212e-18
    PWL_CURRENT: 3
}
\end{lstlisting}

\paragraph{运行 RedHawk 的 GSR 设置}
\begin{lstlisting}
GDS_FILE <gds2def modeled IP>
EXTRACT_INTERNAL_NET 1
VP_CONTROL {
    <control_filename>
}
SWITCH_MODEL_FILE {
    <switch_model_file>
}
\end{lstlisting}
"""

CH13_RAM_LDO = r"""
\subsection{开关 RAM Case 2--4 配置补充}
\subsubsection*{Additional Case 2--4 GDS2DEF Configurations}

\textbf{Case 2}（多对外/内 P/G 对，各用独立开关）：
\begin{lstlisting}
VDD_NETS { Ext_VDD1 Int_VDD1 Ext_VDD2 Int_VDD2 }
EXTRACT_SWITCH_CELLS {
    sw1 HEADER EXT_VDD1 INT_VDD1
    sw2 HEADER EXT_VDD2 INT_VDD2
}
DEFINE_SWITCH_CELLS {
    sw1 HEADER VDD_EXT1 VDD_INT1 EN1
    sw2 HEADER VDD_EXT2 VDD_INT2 EN2
}
\end{lstlisting}

\textbf{Case 3}（单外网经同一开关接多内网）——\texttt{EXTRACT\_SWITCH\_CELLS} 对同一 \texttt{sw1} 多次声明不同内部网。

\textbf{Case 4}（单外网经不同开关接多内网）——为 \texttt{sw1}、\texttt{sw2} 分别定义。

\paragraph{Ramp-up GSC 与 VP\_CONTROL 示例}
\begin{lstlisting}
# GSC
mem_inst1 vdd_int POWERUP
# VP_CONTROL
Mem1 {
    POWERUP ctrl vdd_int 1e-9
    SWITCH_RAMPUP_TIMING adsU2 1e-9
}
\end{lstlisting}
未在 \texttt{SWITCH\_RAMPUP\_TIMING} 中列出的开关使用 \texttt{POWERUP} 时间；$\Delta=0$ 时所有开关在 TW 同时开启。

\subsection{LDO 负载/线调整动态模型配置}
\subsubsection*{Load and Line Regulation Dynamic Model Configuration}

负载调整（Load Regulation）动态模型 APLDO 配置除 DC 关键字外，还须指定 CPM 与封装接口：
\begin{lstlisting}
CPM_LDO_MODEL adsPowerModel
CPM_LDO_FILE ./power_model_CPM-LDO
CPM_LDO_PORT *:VCC 3.0
CPM_LDO_PORT *:VSS 0
CPM_OPEN_PORT VBB:*
CPM_LDO_TRANSIENT_TIME 120ns
PACKAGE_MODEL REDHAWK_PKG
PACKAGE_FILE redhawk_pkg_0.spi
\end{lstlisting}

线调整（Line Regulation）模型类似，激励加在输入 pin 而非负载电流阶跃。

\paragraph{LDO 与 CPM 协同}
含 LDO 的芯片可直接 \cmd{perform powermodel}；检测到 LDO 时自动启用 \texttt{-plocname} 并在 LDO pin 生成内部端口。系统级仿真须含 LDO 子电路（晶体管级或 APLDO 行为级）；推荐 \texttt{-pincurrent -global\_gnd}。
"""

# ---------------------------------------------------------------------------
# Chapter 14 expansions
# ---------------------------------------------------------------------------

CH14_POWMODEL_EXPAND = r"""
\subsection{\cmd{perform powermodel} 全选项说明}
\subsubsection*{Complete perform powermodel Option Reference}

完整命令语法：
\begin{lstlisting}
perform powermodel [ -wirebond | -nx <x> -ny <y> | -cdie | -static
| -lowpower | -esd ] ? -esd_clamp <file> ? ? -parasitic ? ? -vcd ?
? -pincurrent ? ? -rleak ? ? -rleak_par ? ? -solver mor ? ? -plocname ?
? -ind ? ? -no_afs ? ? -passive ? ? [ -noglobal_gnd | -global_gnd ] ?
? -high_capacity [0|1] ? ? -repeat_current [ <t> | presim | best ] ?
? -probe ? ? -internal_node -cell_file <file> ? ? -reportcap ?
? -o <output> ? ? -reuse ? ? -io ? ? -port_grouping <cfg> ?
? -esd_spice ? ? -cecm_subckt ? ? -user_config -group_file <file> ?
? -couple_gridc ?
\end{lstlisting}

\paragraph{模式与分区选项}
\begin{itemize}
  \item \texttt{-wirebond}：线键封装，每 P/G 连接一个端口
  \item \texttt{-nx/-ny}：倒装 X/Y 分区；\texttt{-nx 1 -ny 1} 生成 \texttt{adsRpt/CPM/apache.Cdie}
  \item \texttt{-cdie}：等价于 \texttt{-nx 1 -ny 1} 但跳过电流波形计算，仅 $C_{\mathrm{die}}/R_{\mathrm{die}}$
  \item \texttt{-static}：DC 静态 CPM（电阻网 + 平均电流）
  \item \texttt{-lowpower}：支持 ramp-up 分析的 CPM
  \item \texttt{-esd}：含 clamp 端口与子电路的 ESD-aware CPM；GSR 已有 \texttt{ESD\_CLAMP\_FILE} 时可省略 \texttt{-esd\_clamp}
  \item \texttt{-parasitic}：仅无源部分，适用于 DC/AC，不可用于瞬态
  \item \texttt{-vcd}：基于 VCD 的最坏开关场景
\end{itemize}

\paragraph{电流与求解器选项}
\begin{itemize}
  \item \texttt{-pincurrent}：不强制 Vdd/Vss 电流守恒，改善与 RedHawk 动态相关（RedHawk 电流不平衡时推荐）
  \item \texttt{-rleak}：在 VDD 端口与参考 VSS 端口间加泄漏电阻
  \item \texttt{-rleak\_par}：在各分区定义的 POWER/GROUND 端口对间加泄漏电阻（须 \texttt{partition.txt}）
  \item \texttt{-solver mor}：关闭默认 AC 求解器（\texttt{solver ac}），改用 MOR
  \item \texttt{-passive}：MOR 被动 enforced 模型（收敛问题时，可能略降精度）
  \item \texttt{-no\_afs}：关闭自适应频率扫描（$>50$ 端口推荐）；默认 AFS 选 7--9 个频率点
  \item \texttt{-high\_capacity 1}：ASIM3D 求解器（默认开）；\texttt{0} 切换为 asim\_mixed
\end{itemize}

\paragraph{端口与探测选项}
\begin{itemize}
  \item \texttt{-plocname}：CPM 端口用 pad/分组名；倒装分区名为 \texttt{PAR\_0\_0\_VDD1} 等形式
  \item \texttt{-ind}：含片上电感（须 extraction 使用 \texttt{-l}）；仅 \texttt{-l} 无 \texttt{-ind} 则忽略电感
  \item \texttt{-probe}：iCPM 内部节点探测（须 \texttt{PROBE\_NODE\_FILE}）
  \item \texttt{-internal\_node -cell\_file}：暴露实例内部 P/G pin 为端口（命名 \texttt{<inst>\_<net>}）；须配合 \texttt{-pincurrent}
  \item \texttt{-port\_grouping <cfg>}：bump 分组，格式 \texttt{CPM\_Port\_Grouping \{ \#region layer nx ny llx lly urx ury \}}
  \item \texttt{-io}：I/O 单元纳入 CPM
  \item \texttt{-reuse}：复用已生成电流波形以尝试不同分区
  \item \texttt{-reportcap}：写出电容分量日志（intentional/intrinsic/load/grid/well decap）
  \item \texttt{-repeat\_current}：从指定时刻（ns）、\texttt{presim} 或 \texttt{best} 重复电流 PWL；非零值取 PWL 最近时间点
  \item \texttt{-esd\_spice} / \texttt{-cecm\_subckt}：ESD 电路 spice 文件名与子电路名
  \item \texttt{-user\_config -group\_file}：用户可配置多组电流源（见下文）
  \item \texttt{-couple\_gridc}：EMI 建模时耦合网格电容（须 \texttt{COUPLEC 1}）
\end{itemize}

\paragraph{倒装/线键/无源生成示例}
\begin{lstlisting}
perform powermodel -nx 4 -ny 4 -o flipchip_cpm.sp
perform powermodel -wirebond -solver mor -o wirebond_cpm.sp
perform powermodel -nx 2 -ny 3 -parasitic -o cpm_passive.sp
perform powermodel -nx 1 -ny 1 -vcd -pincurrent -global_gnd -o cpm_vcd.sp
\end{lstlisting}

AC 模式默认线程数 $\le \min(\text{CPU 数}, 8)$；环境变量 \texttt{MAX\_CPU} 可调整上限。
"""

CH14_MODES_EXPAND = r"""
\subsection{VectorLess 与谐振频率感知模式}
\subsubsection*{VectorLess and Resonance Frequency-Aware Modes}

\paragraph{VectorLess 时钟门控开关模式}
CPM 除无向量与 VCD 外，支持 VectorLess™ 时钟门控开关模式：生成模拟时钟门控模式切换的多周期瞬态，捕获模式切换电流跃迁，有助于理解封装/板级 $L\,di/dt$ 效应。

\paragraph{谐振频率感知激励}
流程：
\begin{enumerate}
  \item 用常规 CPM 无源部分接封装做 AC 分析，得到系统谐振频率 $f_{\mathrm{res}}$
  \item 第二次 CPM 运行设 GSR：
\begin{lstlisting}
DYNAMIC_FREQUENCY_AWARE 40e6
\end{lstlisting}
  （例：40\,MHz）VectorLess 引擎生成在谐振附近引入大部分能量的多周期电流特征，同时保持逻辑与时序属性。
\end{enumerate}

\figplaceholder{Figure 14-8}{频率感知 CPM 模式}

\subsection{功率瞬态模式配置详解}
\subsubsection*{Power Transient Mode Configuration Details}

GSR：
\begin{lstlisting}
POWER_TRANSIENT_ANALYSIS {
    <duration_frame_1_sec> <config_file_1>
    <duration_frame_2_sec> <config_file_2>
    ...
}
\end{lstlisting}

各帧配置文件可含：\texttt{GSC\_FILE}、\texttt{INSTANCE\_POWER\_FILE}、\texttt{GSC\_OVERRIDE\_IPF}、\texttt{BLOCK\_POWER\_FOR\_SCALING}、\texttt{STATE\_PROPAGATION}（含 \texttt{PROPAGATION\_MODE}、\texttt{GATED\_ON\_PERCENTAGE} 等）、\texttt{TOGGLE\_RATE}、\texttt{INSTANCE/BLOCK\_TOGGLE\_RATE} 等。配置关键字覆盖 GSR（\texttt{GSC\_FILE}、\texttt{STATE\_PROPAGATION} 除外）。

\begin{noteBox}
功率瞬态分析\textbf{仅}支持无向量模式；不支持 \texttt{VCD\_FILE}、\texttt{STA\_FILE}、\texttt{BLOCK\_POWER\_ASSIGNMENT}、\texttt{PAR} 等。仿真以第一帧电荷为参考，首帧配置影响动态结果。
\end{noteBox}

\subsection{用户可配置模式详解}
\subsubsection*{User-Configurable Mode Details}

分组文件示例：
\begin{lstlisting}
GROUP GS1
INSTANCE Bl_1
Bl_2/Inst1
Inst2
Bl_3/MEM*;
GROUP GS2
INSTANCE Bl_4/*;
\end{lstlisting}

未分组 instance 归入 ``others''。无 \texttt{-pincurrent} 时每组 $(P-1)$ 个 PWL 源；有 \texttt{-pincurrent} 时 $P \times N_g$ 个源。PWL 名以组名前缀（如 \texttt{Icsg1\_1}）便于在 SPICE 中注释启用/禁用组。

示例多组分析结果（峰值电流 / 峰峰 DvD）：
\begin{center}
\small
\begin{tabular}{cccccc}
\toprule
Block 1 & Block 2 & Rest & Peak $I$ & Peak-to-Peak DvD \\
\midrule
ON & ON & ON & 192\,A & 95\,mV \\
OFF & ON & ON & 139\,A & 72\,mV \\
ON & OFF & ON & 130\,A & 66\,mV \\
ON & ON & OFF & 116\,A & 53\,mV \\
OFF & OFF & ON & 76\,A & 42\,mV \\
\bottomrule
\end{tabular}
\end{center}
"""

CH14_VALIDATE_EXPAND = r"""
\subsection{CPM 验证流程详述}
\subsubsection*{Detailed CPM Validation Procedure}

\begin{enumerate}
  \item \textbf{生成 CPM}：无封装模型运行 RedHawk；推荐 \texttt{DYNAMIC\_TIME\_STEP 10e-12}；\texttt{DYNAMIC\_PRESIM\_TIME} 步长与主仿真一致
  \item \textbf{接封装 SPICE}：将 CPM \texttt{.sp} + \texttt{.sp.inc} 与封装/板网表级联
  \item \textbf{Pad 点测量}：在 bump/pad 连接点探针电流与电压
  \item \textbf{RedHawk 对照 DvD}：相同封装模型、相同 presim；RedHawk 波形须\textbf{平移} presim 时间后与 CPM 对齐
  \item \textbf{比较}：所有 bump 的 VDD/GND 电流与电压波形应一致（图~\ref{fig:cpm-validate}）
\end{enumerate}

\paragraph{AC 分析注意事项}
\begin{itemize}
  \item AC 仅连接无源部分（\texttt{.inc}），勿将 CPM 端口接全局地
  \item 默认 Norton 电流模型：选一 VSS 端口作为各 PWL 负端，端口电流和为零
  \item \texttt{-pincurrent} 时各 PWL 参考节点 0，部分第三方工具不支持
  \item \texttt{get\_cdie.sp} 默认 50\,MHz 计算 $R_{\mathrm{die}}/C_{\mathrm{die}}$；多 P/G 网生成 \texttt{get\_cdie\_<pwr>\_<gnd>.sp}
\end{itemize}

\paragraph{CPM 输出格式}
\begin{itemize}
  \item 标准 SPICE（默认）：\texttt{PowerModel.sp} + \texttt{PowerModel.sp.inc}
  \item HSPICE 优化：\texttt{<design>\_hspice.sp}（100+ 端口时 Foster VCCS）
  \item Sentinel-PI 二进制：\texttt{<design>\_snpi.sp}
  \item \texttt{-nx 1 -ny 1}：\texttt{adsRpt/CPM/apache.Cdie} 各频率精确 $C_{\mathrm{die}}$、$R_{\mathrm{die}}$
\end{itemize}

\paragraph{系统级应用}
将 CPM 接封装/PCB 后 NSPICE 仿真，用于：全局 PDN 阻抗与 IC-封装谐振（AC）；封装/板级动态噪声预算；片外去耦优化。差分电压测量：
\begin{lstlisting}
plot voltage -pad_pair {VDD1 VSS2} -sv -o vdrop.txt
\end{lstlisting}

CPM 头含 presimulation 时间，用于与 RedHawk 波形时间对齐。
"""

CH14_REFINE_PROMPT = """# RH_CN 精译规范

对照 `scripts/raw_*.txt` **逐段精译**，覆盖现有 `chapters/*.tex`（整文件重写覆盖）。

## 必须做到
1. **不写摘要版**：原文每个 section/subsection、步骤枚举、GSR/TCL 选项说明、示例、表格、注意事项均译出。
2. 体例同现有第 1–2 章：`\bichapter`/`\biappendix`、`\section{中文}`+`\subsection*{English}`、深层 `\subsection`/`\subsubsection*`。
3. `\label{chap:...}` 保持与 `main.tex` 一致；交叉引用用 `\ref{chap:...}`。
4. 命令/关键字/文件名英文：`\cmd{}` `\gsr{}` `\texttt{}`；Tcl 用 `lstlisting`。
5. 注意框 `noteBox` / 参见 `seeAlsoBox`；图用 `\figplaceholder{Figure X-Y}{中文}`。
6. 中文流畅准确，术语中英夹注（如「去耦电容（decap）」）。
7. **LaTeX 安全**：`# $ % _ &` 在正文妥善转义；`\texttt`/`\gsr`/`\cmd` 内可用裸下划线（已 detokenize）；菜单箭头用 `$\rightarrow$`；环境变量写 `\texttt{\$APACHEROOT}`。
8. 无 `\documentclass`；文件须可直接 `\input`。
9. 禁止留下 `\chapterstub` 或「待译」占位。

## 目标行数（对照 raw 大幅扩写）
| 章节文件 | raw 源 | `\label` | 目标行数 |
|----------|--------|----------|----------|
| `07_grid_opt.tex` | `raw_07_grid_opt.txt` | `chap:grid` | >1100 |
| `08_dvd_noise_timing.tex` | `raw_08_dvd_noise_timing.txt` | `chap:noise` | >900 |
| `13_low_power.tex` | `raw_13_low_power.txt` | `chap:lp` | >1100 |
| `14_cpm.tex` | `raw_14_cpm.txt` | `chap:cpm` | >700 |

## 各章扩写要点
- **第 7 章**：示例 A–F 完整日志、FAO DvD 示例 G–H decap 报告、cell swap 选项、mesh/decap 命令表与 GSR 关键字全译。
- **第 8 章**：PJX fullchip/sign-off 对比、skew 模式、时序配置关键字全译（含 EXTEND\_CYCLE\_SELECTION、耦合阈值等）。
- **第 13 章**：多 Vdd 查看/报告、电源门控四态与 charge\_switch.rpt、IP 开关流程、开关 RAM Case 1–4、LDO/APLDO 全流程。
- **第 14 章**：`perform powermodel` 全选项、VectorLess/谐振感知/功率瞬态/用户可配置模式、验证步骤。

## 超长附录策略
- 附录 C：tech/GSC/GSR **按原书分类完整翻译**每个关键字的用途、语法、默认值与示例（可 longtable）。
- 附录 D：TCL 命令摘要表全译 + 各主要命令语法与选项详译；GUI 菜单/按钮按原文结构译。
- 附录 E：每个实用程序全文精译（语法、选项、示例）。
- 附录 F：各第三方组件中文导读 + 许可正文可保留英文 `lstlisting`。
"""


CH07_MESH_EXTRA = r"""
\subsection{Mesh 命令选项补充（表 7-1 扩展）}
\subsubsection*{Extended Mesh Command Options (Table 7-1)}

\paragraph{\cmd{mesh add} 完整选项}
\begin{itemize}
  \item \opt{-vertical|-horizontal}：添加垂直或水平 mesh
  \item \opt{-window \{x1 y1 x2 y2\}}：矩形区域
  \item \opt{-layer <name>}：金属层
  \item \opt{-offset <um>}：自窗口左/底边偏移
  \item \opt{-space <um>}：\opt{-net} 中各电源网间距
  \item \opt{-pitch <um>}：pitch
  \item \opt{-width <um>}：线宽
  \item \opt{-novia} 或 \opt{-viatop/-viabottom}：无 via 或叠层至指定层
  \item \opt{-net \{net1 ...\}}：关联网
  \item \opt{-clip_cell \{macro...\}}：宏边界内禁布金属防短路
  \item \opt{-exclude_regions \{\{x1 y1 x2 y2\}...\}}：排除区域
\end{itemize}

\paragraph{\cmd{mesh delete} 宽度/长度过滤}
\opt{-width \{?<Oper>? <w> ...\}}、\opt{-length \{?<Oper>? ...\}}，Oper 为 \texttt{=}, \texttt{>}, \texttt{<}, \texttt{$\geq$}, \texttt{$\leq$}。\opt{-out_of_ratio \{n m\}}：每 m 条线删 n 条。\opt{-all}：删除所有匹配段。

\paragraph{\cmd{mesh vias} 报告缺失 via}
\opt{-report_missing} 配合 \opt{-threshold}（默认 1\,mV，\texttt{-1} 禁用）、\opt{-sort_by_hot_inst}、\opt{-gds} 输出 GDS marker、\opt{-pitch}、\opt{-x/y_pitch}、\opt{-x/y_offset}、\opt{-adjust_offset}、\opt{-ignore_inter_met} 等控制阵列尺寸与排序。

\paragraph{\cmd{ring add}}
\opt{-name}、\opt{-window}；\texttt{\{-top|bottom|left|right -layer -offset -width -space -net \{...\}\}} 定义 ring 各边。

\paragraph{FAO 流程子步骤（时序感知）}
时序相关 FAO 在 DvD 热点基础上按 delta slack/delay 排序，可选子网格（sub-gridding）、重定线宽、via 插入、cell swapping、decap 插入等组合策略（图~\ref{fig:rh-fao-flow}）。
"""

CH07_EXAMPLE_B_DETAIL = r"""
\paragraph{示例 B 结果说明}
收紧 \gsr{noise_reduction} 为正值 10 时，\gsr{fao_range} 须允许更宽导线（本例 metal6 水平线 10--35\,$\mu$m，相对示例 A 的 8--29.4\,$\mu$m 放宽上限）。FAO 在 accurate 模式下搜索全芯片 METAL6 水平导线，将最坏静态 IR 降低约 10\%。优化成功后 metal 用量增加，最坏压降降至约 16.2\,mV（相对初始 18\,mV）。
"""

CH07_MORE = r"""
\subsection{Decap 命令选项扩展说明}
\subsubsection*{Extended Decap Command Reference}

\paragraph{\cmd{decap advise} 完整流程}
\begin{enumerate}
  \item 设置 \gsr{noise_reduction}、\gsr{fao_region}、\gsr{num_hotinst} 等
  \item \cmd{decap advise} 快速估算可放置总量
  \item \cmd{decap advise -place} 生成 \texttt{*.dpf} 放置文件
  \item \cmd{decap place -dpf <file>} 或 \cmd{decap fill} 执行放置
  \item \cmd{decap report} 查看改善；\cmd{export eco} 导出变更
\end{enumerate}

\paragraph{\cmd{decap fill} 模式详解}
\begin{itemize}
  \item \textbf{targeted}：每个热点 instance 周围矩形区域内放置
  \item \textbf{hot instance area}： encompass 一组热点的矩形区域
  \item \textbf{region}：用户指定 \gsr{fao_region}
  \item \textbf{prefill}：在热点旁腾出行空间后相邻放置
  \item \textbf{uniform}：\opt{-uniform <pct>} 在所有标准单元行均匀填充指定行百分比
\end{itemize}

\paragraph{\cmd{decap remove}}
默认移除峰值电流 $\le 30\,\mu$A 的无效 decap。\opt{-imax_less_than}、\opt{-dvmax_less_than} 自定义阈值。\opt{-user_decap} 仅移除用户放置 decap。\opt{-all} 移除区域内全部 decap。

\paragraph{\cmd{decap qor}}
评估 FAO 插入 decap 的 QoR：\opt{-i} 输入 instance 列表；\opt{-o} 输出目录。关联 \gsr{decap_fill}。

\paragraph{\cmd{decap drc}}
DRC 报告；\opt{-fix} 修复用户 decap 的 pin 与信号/屏蔽布线 DRC；\opt{-o <file>} 写出报告。

\subsection{示例 A--F 关键日志字段说明}
\subsubsection*{Log Field Reference for Examples A--F}

公共日志字段：
\begin{itemize}
  \item \texttt{ECO File}：输出 ECO 路径
  \item \texttt{Region}：\gsr{fao_region} 或全芯片边界
  \item \texttt{FAO Mode}：accurate / turbo
  \item \texttt{Simulation Mode}：static / dynamic
  \item \texttt{Noise Reduction}：目标压降变化百分比（负值表示放宽）
  \item \texttt{Initial Worst Static Noise}：优化前最坏静态噪声（mV）
  \item \texttt{Voltage Noise Constraints}：目标约束（mV）
  \item \texttt{Metal Usage Change Report}：各层金属面积变化百分比
  \item \texttt{DEF file for new via models}：匹配导线变更的新 via DEF
\end{itemize}

示例 C/D 另含 \texttt{Hot-spots Number}、\texttt{Fix-Window Size}、\texttt{Identified N hot-spots: (x,y)}、\texttt{Fixing Window} 坐标。示例 E/F 使用 \opt{-taper} 时修改仅限 \gsr{fao_region} 或各热点 \gsr{fix_window} 内，不横跨整片宽/高。
"""

CH08_MORE = r"""
\subsection{PJX Sign-Off 批处理完整示例}
\subsubsection*{Complete Batch Sign-Off Example}

\begin{lstlisting}
import gsr design_dynamic.gsr
setup design
import apl cell.current
import apl -c cell.cdev
perform pwrcalc
perform extraction -power -ground -c
setup pad -power -r 0.01 -c 0.5
setup pad -ground -r 0.01 -c 0.5
setup wirebond -power -r 0.245 -l 1420 -c 5
setup wirebond -ground -r 0.245 -l 1420 -c 5
setup package -r 0.002 -l 100 -c 5
perform jitter_cycle_select -type WORST_JITTER_CYCLE -vcd
perform analysis -vcd
perform jitter -config psi.jitter_config -mode waveform_pg
show jitter period rise
show jitter c2c fall
export db post_jitter.db
\end{lstlisting}

\paragraph{Jitter Bottleneck 参数与按钮}
排序列：No、Max/Min Delay、Delay Diff、DS Leaf Jitter、P/C-C Jitter (R/F)、Level、Leaf \#、Pin Name。按钮：Reset to Default Order、Go To Location、Up/Down、Previous/Next 1000。

\paragraph{抖动色阶图 TCL}
\begin{lstlisting}
show jitter period rise
show jitter period fall
show jitter c2c rise
show jitter c2c fall
\end{lstlisting}
通过 View $\rightarrow$ Clock Jitter Map 亦可选择 Rise/Fall Period 或 C-to-C Jitter；Set Color Range 显示颜色与最大抖动百分比关系。

\subsection{Skew 摘要报告列说明}
Clock Root、Leaf Num、Inst Num、Skew R/F（最长与最短上升/下降插入延迟差，ps）、Max/Min Delay R/F（根到叶最大/最小延迟，ps）。
"""

CH13_MORE = r"""
\subsection{低功耗技术引言补充}
\subsubsection*{Additional Low-Power Technique Context}

亚微米设计面临更大漏电、NBTI 阈值漂移、更强驱动与更高密度。省电技术虽在系统/架构层影响最大，设计层常见手段包括：时钟门控控制触发器时钟；电压岛降低动态功耗；多 $V_{\mathrm{th}}$ 单元风格在关键路径外使用高阈值降低漏电；有源体偏置动态调节 $V_{\mathrm{th}}$；保持触发器在掉电期间保持状态。

RedHawk 支持全芯片/块级瞬态 DvD 与平均静态 IR，含文本报告、图形及影片模式显示动态压降演化。

\subsection{开关配置文件关键字逐项说明}
\begin{itemize}
  \item \texttt{SWITCH\_TYPE [HEADER|FOOTER]}：header 控制 VDD，footer 控制 VSS
  \item \texttt{EXT\_PIN / INT\_PIN}：外部/内部 P/G 子电路端口
  \item \texttt{ON\_STATE / OFF\_STATE}：\{控制pin 电压...\}
  \item \texttt{POWER\_UP / POWER\_DOWN}：上电/下电控制电压序列
  \item \texttt{CONTROL\_PIN <pin> [R|F|-] [R|F|-]}：边沿触发方向
  \item \texttt{DC\_BIAS}：各端口 DC 偏置
  \item \texttt{OPENPIN}：开路 pin（高阻）
  \item \texttt{SPICE2LEF\_PIN\_MAPPING}：Spice 与 LEF pin 名映射
  \item \texttt{SWITCH\_TIMING\_CHAR [0|1]}：是否表征开关时序
  \item \texttt{EXTERNAL/INTERNAL\_CONTROL\_PIN}：外/内控制 pin 声明
  \item \texttt{CONTROL\_SLEW}：控制 pin 转换时间
  \item \texttt{INT\_TIMING\_ON2OFF / INT\_TIMING\_OFF2ON}：内部时序
  \item \texttt{SIM\_ON\_STATE\_ONLY}：仅仿真 ON 态加速
  \item \texttt{DYNAMIC\_ADAPTIVE\_RON}：自适应 ON 电阻
  \item \texttt{PIECEWISE\_SWITCH\_INPUT}：分段线性控制波形文件
\end{itemize}

\subsection{IP 块无文本标签流程步骤}
\begin{enumerate}
  \item 对各唯一开关 master 运行 gds2def 提取 \texttt{<cell>\_adsgds.lef}
  \item 建宏模型：\texttt{LEF\_FILES}、\texttt{SWITCH\_CELLS}、\texttt{VP\_PAIRS}、\texttt{USE\_LEF\_PINS\_FOR\_TRACING 1}
  \item \texttt{qswitch} 提取开关子电路
  \item \texttt{aplsw} 表征四态模型
  \item \texttt{ACE} 生成等效 R/C/漏电
  \item RedHawk 导入 \texttt{GDS\_FILE}、\texttt{SWITCH\_MODEL\_FILE}、\texttt{VP\_CONTROL}
\end{enumerate}
"""

CH14_MORE = r"""
\subsection{CPM 建模速度与精度选择回顾}
\subsubsection*{Modeling Speed vs Accuracy Review}

\begin{itemize}
  \item \textbf{MOR（高速）}：以 DC/零频为中心模型阶次缩减；高频开关时精度下降但省时；通常假设 P/G 对称；\texttt{DYNAMIC\_SOLVER\_MODE 1} 取消对称假设
  \item \textbf{AC 建模（默认高精度）}：分电流特征与无源缩减；对含非开关 RC 支路及开关电流源做 grid RC 缩减，频响匹配容差 $<0.2\%$；被动性保证
  \item \textbf{S 参数}：\cmd{perform powermodel -grid [RC|RLC] -options <cfg>}；\texttt{sParam=true}、\texttt{portFileName}、\texttt{broadbandSpice=true}
\end{itemize}

\subsection{泄漏电阻 partition.txt 完整示例}
\begin{lstlisting}
# partition.txt
bump_vcc1 part1
bump_vcc2 part2
ref1 part1
ref2 part2
\end{lstlisting}
命令：\cmd{perform powermodel -rleak_par -wirebond}。输出 CPM 中形如 \texttt{R0\_A320 GROUP44\_GROUND GROUP44\_POWER 99660.43}。

\subsection{iCPM 与 internal\_node 对比}
\begin{itemize}
  \item \textbf{-probe + PROBE\_NODE\_FILE}：按坐标/层定义探测端口
  \item \textbf{-internal\_node -cell\_file}：暴露列表中 instance 的内部 P/G pin，命名 \texttt{inst\_net}；GSC 可用 \texttt{<inst> EXCLUDE} 排除其电流与电容
  \item 不可与 LDO 的 \texttt{-internal\_node} 同用；LDO 可与 \texttt{-probe} 配合
\end{itemize}

\subsection{验证清单}
\begin{enumerate}
  \item CPM 与 RedHawk 使用相同 presim 与 \texttt{DYNAMIC\_TIME\_STEP}
  \item 所有 bump 电流波形对比（\texttt{-pincurrent} 时注意参考节点差异）
  \item 所有 VDD/GND 电压波形对比（平移 presim 时间）
  \item AC：仅连接 \texttt{.inc}，不测全局地
  \item 差分 pad 对：\cmd{plot voltage -pad_pair \{VDD1 VSS2\} -sv}
\end{enumerate}
"""

def refine_ch07() -> int:
    p = CH / "07_grid_opt.tex"
    text = p.read_text(encoding="utf-8")
    if "DECAP\\_CELL 与 LEF" not in text:
        text = insert_after(text, "  \\item 确保 LEF 中物理信息与 P/G pin 定义完整。\n\\end{enumerate}", CH07_AFTER_DECAP_PREP)
        text = insert_after(text, "\\figplaceholder{Figure 7-12}{Cell Swapping 报告示例}", CH07_AFTER_CELL_SWAP)
        text = insert_after(text, "设置 \\gsr{fao_decap_overlap 1} 允许在无合法空间处也插入 decap，示例总体 DvD 改善约 7.73\\%。", CH07_EXPAND_EX_GH)
        text = insert_after(text, "\\begin{seeAlsoBox}", CH07_GSR_EXPAND)
    if "Mesh 命令选项补充" not in text:
        text = insert_after(text, "\\label{tab:route-fix}", CH07_MESH_EXTRA)
    if "示例 B 结果说明" not in text:
        text = insert_after(text, "  \\item 查看结果。", CH07_EXAMPLE_B_DETAIL)
    if "Decap 命令选项扩展说明" not in text:
        text = text.rstrip() + "\n\n" + CH07_MORE + "\n"
    p.write_text(text, encoding="utf-8")
    return len(text.splitlines())


CH08_CONFIG_FULL = r"""
\subsection{配置关键字语法全集补充}
\subsubsection*{Supplemental Configuration Keyword Syntax}

\paragraph{\gsr{CYCLE\_SELECTION}（GSR 与配置文件）}
\begin{lstlisting}
CYCLE_SELECTION [ DISABLE | WORST_C2C_JITTER_CYCLE |
    WORST_PERIOD_JITTER_CYCLE | WORST_MIN_PERIOD_JITTER_CYCLE |
    WORST_MAX_PERIOD_JITTER_CYCLE | WORST_JITTER_CYCLE ]
\end{lstlisting}
\gsr{WORST\_JITTER\_CYCLE}：同时选取最差周期抖动与 cycle-to-cycle 分析周期。\gsr{IGNORE\_JITTER\_FASTSIM 1}：用功耗 histogram 替代纯仿真周期选择（默认 0）。

\paragraph{\gsr{JITTER\_CUTOFF\_FREQ}}
最低仿真时钟频率（MHz），默认 4\,MHz，用于剔除低频域加速。

\paragraph{\gsr{JITTER\_FAST\_MODE}}
\texttt{[0 | 1 | 2]}：0 关闭；1 有效 DvD PWL 快速模式；2 多周期有效 VDD。

\paragraph{\gsr{FALL\_SLEW} / \gsr{RISE\_SLEW} / \gsr{*_SLEW\_AGRS}}
转换时间（ns），须 $>0$ 且 $\le 1.0$\,ns；默认 0.05\,ns。超出范围报错退出。

\paragraph{\gsr{SPICE\_SIMULATOR}}
\texttt{[ NSpice | HSpice | Eldo ]}；可执行文件须在 PATH 中。

\paragraph{\gsr{SPICE\_TIME\_STEP}}
瞬态步进（ns），默认 0.01。

\paragraph{\gsr{SPICE\_PROBE\_USE} / \gsr{SPICE\_FILE\_BACKUP}}
\texttt{SPICE\_PROBE\_USE 1} 写出 \texttt{.probe} 与 \texttt{*.ta0}；\texttt{SPICE\_FILE\_BACKUP 1} 保留各次 Spice deck。

\paragraph{\gsr{CAP\_MULTIPLIER} / \gsr{RES\_MULTIPLIER} / \gsr{COUPLE\_CAP\_MULTIPLIER}}
全局电容/电阻/耦合电容倍乘，默认 1。

\paragraph{\gsr{NUM\_TASKS} / \gsr{MAX\_TASKS} / \gsr{LSF\_JOB\_COUNT}}
并行任务控制；\gsr{TIMER} 为作业状态检查间隔（秒，默认 60）。

\paragraph{\gsr{JITTER\_REPORT\_FORMAT} / \gsr{SKEW\_REPORT\_FORMAT}}
控制抖动/skew 报告详细程度。

\paragraph{\gsr{WAVEFORM\_OUTPUT}}
配合 \gsr{SPICE\_PROBE\_USE} 写出波形文件。

\paragraph{分析模式总结}
\begin{table}[htbp]
\centering
\caption{时钟树分析四种模式}
\begin{tabular}{@{}lll@{}}
\toprule
模式 & 配置 & 说明 \\
\midrule
Basic & 理想电压，无耦合 & 与 PrimeTime 比对；多 Vdd 支持 \\
仅 SI & \gsr{SIGNAL\_INTEGRITY 1}，SPEF 含 $C_c$ & 无 DvD \\
仅 PI & \gsr{POWER\_INTEGRITY 1}，DvD 波形 & 无 $C_c$ \\
PI+SI & 两者均为 1 & 并发分析 \\
\bottomrule
\end{tabular}
\end{table}
"""

def refine_ch08() -> int:
    p = CH / "08_dvd_noise_timing.tex"
    text = p.read_text(encoding="utf-8")
    if "PJX Fullchip 与 Sign-Off" not in text:
        text = insert_after(text, "\\section{PJX 时钟树抖动 Sign-Off 分析}", CH08_PJX_EXPAND)
        text = insert_after(text, "\\figplaceholder{Figure 8-23}{时序分析目录结构——skew}", CH08_SKEW_EXPAND)
    if "配置关键字语法全集补充" not in text:
        text = insert_after(text, "\\gsr{DOMAIN_RPT_ENABLE}——等效于 \\gsr{CLOCKTREE_DOMAIN_SPLIT_REPORT} 的遗留别名。", CH08_CONFIG_FULL)
    if "PJX Sign-Off 批处理完整示例" not in text:
        text = text.rstrip() + "\n\n" + CH08_MORE + "\n"
    p.write_text(text, encoding="utf-8")
    return len(text.splitlines())


CH13_RAM_CASES = r"""
\subsubsection{Case 2 GDS2DEF 完整示例}
\begin{lstlisting}
TOP_CELL <design_name>
GDS_FILE <gds_pointer>
GDS_MAP_FILE <layer_map_pointer>
VDD_NETS {
    Ext_VDD1
    Ext_VDD2
    INT_VDD1
    INT_VDD2
}
GND_NETS { VSS }
EXTRACT_SWITCH_CELLS {
    sw1 HEADER EXT_VDD1 INT_VDD1
    sw2 HEADER EXT_VDD2 INT_VDD2
}
DEFINE_SWITCH_CELLS {
    sw1 HEADER VDD_EXT VDD_INT EN
    sw2 HEADER VDD_EXT VDD_INT EN
}
LEF_FILE { <design LEF file pointer> }
USE_LEF_PINS_FOR_TRACING 1
SWITCH_MODEL_MODE [RAMPUP|ONSTATE]
\end{lstlisting}
Case 2 的 EXT/INT 网在 ONSTATE 下可选，RAMPUP 下必需。

\subsubsection{Case 3 GDS2DEF 完整示例}
同一 \texttt{sw1} 多次出现在 \texttt{EXTRACT\_SWITCH\_CELLS}：
\begin{lstlisting}
EXTRACT_SWITCH_CELLS {
    sw1 HEADER EXT_VDD1 INT_VDD1
    sw1 HEADER EXT_VDD1 INT_VDD2
}
\end{lstlisting}

\subsubsection{开关 RAM 动态与 Ramp-up 命令}
On-state DvD：
\begin{lstlisting}
perform analysis -vectorless
# 或 -vcd / -mcycle 等
\end{lstlisting}
Ramp-up：
\begin{lstlisting}
setup analysis_mode lowpower
perform analysis -lowpower
perform analysis -lowpower -alp3d   # 约 3x 加速，精度影响 10-15%
\end{lstlisting}
时间步须 $\le 150$\,ps（\texttt{-alp3d}）。

\subsection{电源门控运行示例与混合模式}
\subsubsection*{Power Gating Run Examples}

\textbf{纯 ON 态分析}：
\begin{lstlisting}
import gsr design.gsr
setup design
perform pwrcalc
perform extraction -power -ground -c
setup pad / wirebond / package
perform analysis -static
perform analysis -dynamic
\end{lstlisting}

\textbf{Ramp-up} 另须 GSC（\texttt{POWERUP}）、\texttt{PIECEWISE\_CAP\_FILE} 或 \texttt{RAMPUP\_OFFSTATE\_VOLTAGE}、STA 控制 pin TW。

\textbf{混合低功耗 + VCD}：
\begin{lstlisting}
setup design GENERIC.gsr
perform pwrcalc
setup analysis_mode lowpower
perform extraction -power -ground -c
setup package / wirebond / pad
perform analysis -dynamic
\end{lstlisting}

\subsection{switch\_static/dynamic 报告字段}
\texttt{switch\_static.rpt}：内部节点电压、开关压降、平均电流。\texttt{switch\_dynamic.rpt}：活动开关峰值电流（上电分析）。\texttt{adsRpt/apache.memsw.info} 列出设计中所有开关 instance。
"""

CH13_LDO_MORE = r"""
\subsection{APLDO 线调整与瞬态模型}
\subsubsection*{Line Regulation and Transient APLDO Models}

线调整动态模型在输入电压阶跃下表征输出电压响应；负载调整在负载电流阶跃下表征。两者均须完整 \texttt{POWER\_ARC}、\texttt{DC\_BIAS} 与封装/CPM 接口定义。

\paragraph{测试台与调试}
\begin{lstlisting}
apldo apldo.config          # 生成加密模型
aplreader -ldo <LDO model>  # 绘制 I-V 曲线
\end{lstlisting}
调试设 \texttt{DEBUG 1} 保留 \texttt{.apache/APLDO/ldo\_dc\_vdd.cir} 与 \texttt{ldo\_ac\_vdd.cir}。对 \texttt{<>_LOAD_REGULATION_TEST_BENCH.sp} 运行 Spice 做健全性检查。

\paragraph{GSC 动态 LDO 切换示例}
\begin{lstlisting}
# LDO_INST_CONFIG
ldo_inst_1 enable 100 disable 5000 enable 8000
# END_LDO_INST_CONFIG
\end{lstlisting}
不支持通配符。检查：\cmd{plot current -ldo -name <LDO instance>}；输出 \texttt{adsRpt/Dynamic/ldo.current}、\texttt{ldo.voltage}、\texttt{ldo\_dynamic.rpt}（最小/最大负载电流、输入/输出电压、$di/dt$）。
"""

def refine_ch13() -> int:
    p = CH / "13_low_power.tex"
    text = p.read_text(encoding="utf-8")
    if "多 Vdd 结果查看" not in text:
        text = insert_after(text, "Results $\\rightarrow$ List of Worst IR/DvD Instance 列出最高压降实例（最多 1000）；可在 Vdd Domain 组合框选择特定网表。报告字段：排名、最低 VDD-VSS、理想 VDD、坐标、实例名。", CH13_MULTI_VDD)
        text = insert_after(text, "每开关区域需 ON、OFF、POWERUP、POWERDOWN 四种模式。", CH13_PG_EXPAND)
        text = insert_after(text, "\\texttt{VP\\_CONTROL} 描述开关 IP 宏控制 pin（见附录 C）。", CH13_IP_EXPAND)
        text = insert_after(text, "\\figplaceholder{Figure 13-32}{正常与半驱动强度 LDO 输出电压}", CH13_RAM_LDO)
    if "Case 2 GDS2DEF 完整示例" not in text:
        text = insert_after(text, "各 Case 的 EXT/INT 网在 ONSTATE 下可选、RAMPUP 下必需。", CH13_RAM_CASES)
        text = insert_after(text, "\\figplaceholder{Figure 13-32}{正常与半驱动强度 LDO 输出电压}", CH13_LDO_MORE)
    if "低功耗技术引言补充" not in text:
        text = text.rstrip() + "\n\n" + CH13_MORE + "\n"
    p.write_text(text, encoding="utf-8")
    return len(text.splitlines())


CH14_LDO_OUTPUT = r"""
\subsection{CPM LDO 实例化与系统级仿真}
\subsubsection*{CPM LDO Instantiation and System Simulation}

CPM 头注释示例：
\begin{lstlisting}
* ****** CPM-LDO ***
* LDO cell | SPICE subcircuit name
* VDD_REG_FC_ISO_580173    VDD_REG_FC_ISO
\end{lstlisting}

顶层 \texttt{adsPowerModel} 实例化各 LDO：
\begin{lstlisting}
X_VDD_REG_FC_ISO_580173 VDD_REG_FC_ISO_580173__vddhv
+ VDD_REG_FC_ISO_580173__vddcore0 ... VDD_REG_FC_ISO
\end{lstlisting}

系统级仿真须含封装/PCB 与 LDO 子电路（晶体管级或 APLDO 行为级）。晶体管级模型可能有偏置 pin，须 ``包装'' 偏置源后供 CPM 调用。推荐 \texttt{-pincurrent -global\_gnd}。

\paragraph{*.cdie 文件示例}
\begin{lstlisting}
Cdie and Rdie between nets VDD and VSS
4.700000e+08 Hz, Cdie=2.662143e-11 F, Rdie=2.902836e+00 Ohm
6.250000e+08 Hz, Cdie=2.635451e-11 F, Rdie=2.874828e+00 Ohm
...
\end{lstlisting}
频率点为精确 Y 矩阵计算结果，无等效电路近似。

\paragraph{HSPICE 与 Sentinel-PI 输出}
100+ 端口时 HSPICE 优化格式使用 Foster VCCS 消除内部节点；\texttt{<design>\_snpi.sp} 为二进制 Sentinel-PI 格式（不含 LDO 实例子电路）。

\subsection{3DIC 与 ESD CPM 命令回顾}
\subsubsection*{3DIC and ESD CPM Command Review}

3DIC 组合 CPM：
\begin{lstlisting}
import gsr mem.gsr -die mem
import gsr logic.gsr -die logic
setup design
perform pwrcalc
perform extraction -power -ground -r -c
perform powermodel -nx 1 -ny 1 -o 3dic_cpm.sp
\end{lstlisting}

ESD-aware CPM：
\begin{lstlisting}
setup analysis_mode esd
setup design <GSR_file>
perform extraction -power -ground
perform powermodel -esd ?-esd_clamp <file>? ...
\end{lstlisting}
"""

def refine_ch14() -> int:
    p = CH / "14_cpm.tex"
    text = p.read_text(encoding="utf-8")
    if "perform powermodel} 全选项说明" not in text:
        text = insert_after(text, "AC 模式可用多线程；默认处理器数 $\\le \\min(\\text{可用数}, 8)$；环境变量 \\texttt{MAX\\_CPU} 可调整。", CH14_POWMODEL_EXPAND)
        text = insert_after(text, "\\figplaceholder{Figure 14-12}{CPM 分析结果示例}", CH14_MODES_EXPAND)
        text = insert_after(text, "\\figplaceholder{Figure 14-15}{CPM 与全芯片 RedHawk 仿真比较}", CH14_VALIDATE_EXPAND)
    if "CPM LDO 实例化" not in text:
        text = insert_after(text, "CPM 头含 presimulation 时间，用于与 RedHawk 波形时间对齐。", CH14_LDO_OUTPUT)
    if "CPM 建模速度与精度选择回顾" not in text:
        text = text.rstrip() + "\n\n" + CH14_MORE + "\n"
    p.write_text(text, encoding="utf-8")
    return len(text.splitlines())


def main() -> None:
    (ROOT / "scripts" / "_refine_prompt.md").write_text(CH14_REFINE_PROMPT, encoding="utf-8")
    counts = {
        "07_grid_opt.tex": refine_ch07(),
        "08_dvd_noise_timing.tex": refine_ch08(),
        "13_low_power.tex": refine_ch13(),
        "14_cpm.tex": refine_ch14(),
    }
    for name, n in counts.items():
        print(f"{name}: {n} lines")


if __name__ == "__main__":
    main()
