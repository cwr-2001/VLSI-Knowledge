# -*- coding: utf-8 -*-
"""Build chapters 09, 10, 11 tex files via Path.write_text."""
from pathlib import Path
import re

BASE = Path(__file__).resolve().parent.parent / "chapters"

def write_ch(name, text):
    p = BASE / name
    p.write_text(text, encoding="utf-8")
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    print(f"{name}: {len(text)} bytes, {len(text.splitlines())} lines, CJK={cjk}")

# Import chunk modules
from gen_ch09_part1 import CHUNK1

CHUNK2 = r"""
% ============================================================
\section{最小与最大延时计算}
\subsection*{Minimum and Maximum Delay Calculations}

\cmd{set\_operating\_conditions} 定义时序分析的工作条件并指定分析类型（单一或片上变异）。工作条件必须在指定库或库对中定义。

默认情况下，PrimeTime 在单一工作条件集下分析（单一工作条件模式）。此模式下需多次分析运行以处理多种工作条件。通常至少需分析两种工作条件以确保无时序违例：最好情况（最小路径报告）用于 hold 检查，最坏情况（最大路径报告）用于 setup 检查。

在片上变异（OCV）模式下，PrimeTime 执行保守分析，允许最小与最大延时同时应用于不同路径。Setup 检查对 launch 时钟路径与数据路径用最大延时，对 capture 时钟路径用最小延时；Hold 检查相反。

OCV 模式下，当路径段被 launch 与 capture 时钟路径共享时，该段可能同时被视为具有两种不同延时。未考虑共享路径段会导致悲观分析。可通过修正获得更准确分析，见「时钟再汇聚悲观移除」。

最小-最大分析考虑下列设计参数的最小与最大值：
\begin{itemize}
  \item 输入与输出外部延时
  \item 自 SDF 反标的延时
  \item 端口连线负载模型
  \item 端口扇出数
  \item Net 电容与电阻
  \item Net 连线负载模型
  \item 时钟 latency 与转换时间
  \item 输入端口驱动单元
\end{itemize}

例如计算最大延时时，PrimeTime 使用最长路径、最坏工作条件、最晚到达时钟边沿、最大单元延时、最长转换时间等。

可用单库（指定最小与最大工作条件）或双库（一库最好、一库最坏）进行最小-最大分析，见「用两个库进行分析」。

启用最小-最大分析的方法：
\begin{itemize}
  \item 用 \cmd{set\_operating\_conditions} 设置最小与最大工作条件：
\begin{lstlisting}
pt_shell> set_operating_conditions -analysis_type on_chip_variation \
          -min BCCOM -max WCCOM
\end{lstlisting}
  \item 读入 SDF 并读取最小与最大延时值：
\begin{lstlisting}
pt_shell> read_sdf -analysis_type on_chip_variation my_design.sdf
\end{lstlisting}
\end{itemize}

\subsection{最小-最大单元与 Net 延时值}
\subsubsection*{Minimum-Maximum Cell and Net Delay Values}

每条时序弧可有最小与最大延时以反映工作条件变化。指定方式：
\begin{itemize}
  \item 从一个或两个 SDF 文件反标延时
  \item 由 PrimeTime 计算延时
\end{itemize}

从 SDF 反标：SDF 三元组的最小/最大、两个 SDF 文件、或上述方式加最大/最小乘数。

由 PrimeTime 计算：单一工作条件加时序降额、两种工作条件（最好/最坏）建模 OCV、上述加最小/最大降额、单元与 net 分别降额、不同时序检查分别降额。

\begin{table}[htbp]
\centering
\caption{表 17：来自 SDF 三元组数据的最小-最大延时}
\small
\begin{tabular}{@{}p{2.8cm}p{4.5cm}p{2cm}p{2cm}@{}}
\toprule
分析模式 & 基于工作条件的延时 & 一个 SDF & 两个 SDF \\
\midrule
单一工作条件 Setup & 工作条件下最大数据；工作条件下最小 capture 时钟 & \texttt{a:b:c} & --- \\
单一工作条件 Hold & 工作条件下最小数据；工作条件下最大 capture 时钟 & \texttt{a:b:c} & --- \\
OCV Setup & 最坏最大数据；最好最小 capture 时钟 & \texttt{a:b:c} & SDF1/SDF2 \\
OCV Hold & 最好最小数据；最坏最大 capture 时钟 & \texttt{a:b:c} & SDF1/SDF2 \\
\bottomrule
\end{tabular}
\end{table}

PrimeTime 使用粗斜体显示的三元组值。

\subsubsection{Setup 与 Hold 检查}
\paragraph*{Setup and Hold Checks}

单一工作条件与 OCV 下 setup/hold 检查示例见：
\begin{itemize}
  \item 路径延时追踪
  \item 最坏条件下 Setup 时序检查
  \item 最好条件下 Hold 时序检查
\end{itemize}

\paragraph{路径延时追踪}
\subparagraph*{Path Delay Tracing for Setup and Hold Checks}

下图示出 PrimeTime 如何执行 setup 与 hold 检查。

\figplaceholder{Figure 90: Design Example}{设计示例}{fig:oc-path-trace}

\begin{itemize}
  \item Setup 检查（DL2/ck 到 DL2/d）：clock\_path1 最大延时；数据路径（data\_path\_max）最大延时；clock\_path2 最小延时。
  \item Hold 检查：clock\_path1 最小延时；数据路径（data\_path\_min）最小延时；clock\_path2 最大延时。
\end{itemize}

data\_path\_min 与 data\_path\_max 可因组合逻辑中多条拓扑路径而不同。

\paragraph{最坏条件下 Setup 时序检查}
\subparagraph*{Setup Timing Check for Worst-Case Conditions}

\figplaceholder{Figure 91: Setup Check Using Worst-Case Conditions}{用最坏条件的 Setup 检查}{fig:oc-setup-wc}

PrimeTime 按下列方式检查 setup 违例：
\[
\text{clockpath1} + \text{datapathmax} - \text{clockpath2} + \text{setup} \leq \text{clockperiod}
\]
其中 clockpath1 $= 0.8 + 0.6 = 1.4$，datapathmax $= 3.8$，clockpath2 $= 0.8 + 0.65 = 1.45$，setup $= 0.2$。时钟周期至少为 $1.4 + 3.8 - 1.45 + 0.2 = 3.95$。

\paragraph{最好条件下 Hold 时序检查}
\subparagraph*{Hold Timing Check for Best-Case Conditions}

\figplaceholder{Figure 92: Hold Check Using Best-Case Conditions}{用最好条件的 Hold 检查}{fig:oc-hold-bc}

Hold 违例检查：
\[
\text{clockpath1} + \text{datapathmax} - \text{clockpath2} - \text{hold} \geq 0
\]
无 hold 违例，因 $0.8 + 1.6 - 0.85 - 0.1 = 1.45 > 0$。

\paragraph{存在延时变异时的路径追踪}
\subparagraph*{Path Tracing in the Presence of Delay Variation}

OCV 下每个单元或 net 延时存在不确定性。可指定最坏条件下 OCV 为标称延时的 80\%--100\%。

\figplaceholder{Figure 93: OCV for Worst-Case Conditions}{最坏条件的 OCV}{fig:oc-ocv-wc}

此模式下，给定路径的最大延时按最坏情况 100\% 计算，最小按 80\%。Setup 检查：
\[
\text{clockpath1} + \text{datapathmax} - \text{clockpath2} - \text{setup} \leq 0
\]
时钟周期至少为 $1.40 + 3.80 - 1.16 + 0.2 = 4.24$。

\begin{noteBox}
片上变异影响时钟 latency；因此仅在使用传播时钟 latency 时需要。若指定理想时钟 latency，可通过 \cmd{set\_clock\_uncertainty} 增大时钟不确定性以考虑 OCV。
\end{noteBox}

% ============================================================
\section{指定分析模式}
\subsection*{Specifying the Analysis Mode}

不同工作条件下时序分析示例见：
\begin{itemize}
  \item 单一工作条件分析
  \item 片上变异分析
\end{itemize}

\subsection{单一工作条件分析}
\subsubsection*{Single Operating Condition Analysis}

最好条件分析：
\begin{lstlisting}
pt_shell> set_operating_conditions BEST
pt_shell> report_timing -delay_type min
\end{lstlisting}

\figplaceholder{Figure 94: Timing path for one operating condition -- best case}{单一工作条件时序路径 -- 最好情况}{fig:oc-single-best}

最坏条件分析：
\begin{lstlisting}
pt_shell> set_operating_conditions WORST
pt_shell> report_timing -delay_type max
\end{lstlisting}

\figplaceholder{Figure 95: Timing path for one operating condition -- worst case}{单一工作条件时序路径 -- 最坏情况}{fig:oc-single-worst}

\subsection{片上变异分析}
\subsubsection*{On-Chip Variation Analysis}

执行 OCV 分析：
\begin{enumerate}
  \item 指定工作条件：
\begin{lstlisting}
pt_shell> set_operating_conditions \
            -analysis_type on_chip_variation \
            -min MIN -max MAX
\end{lstlisting}
  \item 报告 setup 与 hold：
\begin{lstlisting}
pt_shell> report_timing -delay_type min
pt_shell> report_timing -delay_type max
\end{lstlisting}
\end{enumerate}

\figplaceholder{Figure 96: Timing path reported during OCV analysis}{OCV 分析报告的时序路径}{fig:oc-ocv-path}

\figplaceholder{Figure 97: Early and late arrival time}{早到与晚到时间}{fig:oc-early-late}

\textbf{示例 1}：WCCOM 最坏商业条件下 OCV 20\% 以下：
\begin{lstlisting}
pt_shell> set_operating_conditions -analysis_type \
            on_chip_variation WCCOM
pt_shell> set_timing_derate -early 0.8
pt_shell> report_timing
\end{lstlisting}

\textbf{示例 2}：WCCOM\_scaled 与 WCCOM 之间 OCV：
\begin{lstlisting}
pt_shell> set_operating_conditions -analysis_type \
            on_chip_variation -min WCCOM_scaled -max WCCOM
pt_shell> report_timing
\end{lstlisting}

\textbf{示例 3}：单元延时 OCV 在 SDF 值上下 5\%/10\%；net 延时 2\%/4\%；单元时序检查 setup 上 10\%、hold 下 20\%：
\begin{lstlisting}
pt_shell> set_timing_derate -cell_delay -early 0.90
pt_shell> set_timing_derate -cell_delay -late 1.05
pt_shell> set_timing_derate -net_delay -early 0.96
pt_shell> set_timing_derate -net_delay -late 1.02
pt_shell> set_timing_derate -cell_check -early 0.80
pt_shell> set_timing_derate -cell_check -late 1.10
\end{lstlisting}

% ============================================================
\section{用两个库进行分析}
\subsection*{Using Two Libraries for Analysis}

\cmd{set\_min\_library} 指示 PrimeTime 同时使用两个逻辑库进行最小与最大延时分析，例如：
\begin{itemize}
  \item 最好与最坏工作条件
  \item 乐观与悲观连线负载模型
  \item 最小与最大时序延时
\end{itemize}

用 \cmd{set\_min\_library} 在两库间建立最小/最大关联：一库用于最大延时分析，另一用于最小延时分析。仅最大库应在 link path 中。

使用 \cmd{set\_min\_library} 时，PrimeTime 先查最大库中的库单元，再在最小库中查找匹配（同名、同 pin、同时序弧）。若存在则用于最小分析，否则使用最大库信息。

% ============================================================
\section{延时降额}
\subsection*{Derating Timing Delays}

可对计算延时降额以建模片上变异效应。降额将计算延时乘以指定因子，改变 \cmd{report\_timing} 等报告的延时与 slack。

\cmd{set\_timing\_derate} 指定早/晚延时调整因子及可选作用范围：
\begin{lstlisting}
pt_shell> set_timing_derate -early 0.9
pt_shell> set_timing_derate -late 1.2
\end{lstlisting}

第一条将所有早（最短路径）单元与 net 延时减少 10\%（如 hold 数据路径）；第二条将晚延时增加 20\%（如 setup 数据路径），使分析更保守。

\cmd{set\_timing\_derate} 会隐式切换到 OCV 模式（若尚未处于该模式），等效于：
\begin{lstlisting}
pt_shell> set_operating_conditions -analysis_type on_chip_variation
\end{lstlisting}

OCV 模式下同时对早、晚应用最坏情况调整。Setup 检查对 launch 时钟与数据路径用晚降额，对 capture 时钟路径用早降额；Hold 检查相反。

必须指定 \opt{-early} 或 \opt{-late}。早、晚降额需两条命令。降额因子为浮点数；更保守分析用早降额 $< 1.0$ 或晚降额 $> 1.0$。

报告已设降额用 \cmd{report\_timing\_derate}。在 \cmd{report\_timing} 中用 \opt{-derate} 报告每级增量延时的降额因子。

取消所有降额用 \cmd{reset\_timing\_derate}。

\subsection{降额选项}
\subsubsection*{Derating Options}

默认 \cmd{set\_timing\_derate} 将指定早/晚降额因子应用于全设计所有早/晚时序路径。可选缩小范围：
\begin{itemize}
  \item \opt{-clock}/\opt{-data}：仅时钟/数据路径
  \item \opt{-net\_delay}/\opt{-cell\_delay}：仅 net/单元延时
  \item \opt{-rise}/\opt{-fall}：仅上升/下降边延时
  \item 对象列表：特定 net、单元实例或库单元
  \item \opt{-net\_delay} 与 \opt{-static}/\opt{-dynamic}：仅静态或动态 net 延时分量
  \item \opt{-cell\_check}：单元时序检查约束（hold/removal 用早降额；setup/recovery 用晚降额）
  \item \opt{-aocvm\_guardband}、\opt{-pocvm\_guardband}、\opt{-pocvm\_coefficient\_scale\_factor}：影响 AOCV/POCV 分析
\end{itemize}

在 net 或叶级单元上设置降额时，命令隐式匹配对象类型。层次单元上必须显式指定 \opt{-net\_delay}、\opt{-cell\_delay} 或 \opt{-cell\_check}。

将 \cmd{timing\_use\_constraint\_derates\_for\_pulse\_checks} 设为 \texttt{true} 可使最小脉宽与最小周期约束参与降额。也可用 \cmd{set\_timing\_derate} 的 \opt{-min\_pulse\_width}、\opt{-min\_period} 选项（此时上述变量须为 \texttt{false}，默认）。

\begin{lstlisting}
set_timing_derate -min_pulse_width rise 1.2
set_timing_derate -min_period fall 1.1
report_timing_derate -min_pulse_width
report_timing_derate -min_period
reset_timing_derate -min_pulse_width
reset_timing_derate -min_period
\end{lstlisting}

此功能与 POCV 分析配合；在 \cmd{set\_timing\_derate} 中与 \opt{-pocvm\_guardband}、\opt{-pocvm\_coefficient\_scale\_factor} 联用。

\subsection{冲突的降额设置}
\subsubsection*{Conflicting Derating Settings}

新 \cmd{set\_timing\_derate} 覆盖同范围先前设置的降额值。范围重叠时，范围更窄的命令优先：
\begin{lstlisting}
set_timing_derate -late -cell_delay 1.4 [get_cells U2*]
set_timing_derate -late -cell_delay 1.3 [get_lib_cells libAZ/ND*]
set_timing_derate -late -cell_delay 1.2
set_timing_derate -late -1.1
\end{lstlisting}

\subsection{负延时降额}
\subsubsection*{Derating Negative Delays}

某些情况下延时可为负（如输入转换慢、输出转换快且延时极短时，输出可在输入到达 50\% 触发电平前到达）。串扰导致 net 延时变化也可能类似。

一般调整公式：
\[
\text{delay\_new} = \text{old\_delay} + ((\text{derating\_factor} - 1.0) \times |\text{old\_delay}|)
\]
正延时时简化为 $\text{delay\_new} = \text{old\_delay} \times \text{derating\_factor}$；负延时时为 $\text{delay\_new} = \text{old\_delay} \times (2.0 - \text{derating\_factor})$。

静态与动态 net 延时分量分别降额后再合并，使负 delta 延时在合并到正静态延时前正确降额。

% ============================================================
\section{时钟再汇聚悲观移除}
\subsection*{Clock Reconvergence Pessimism Removal}

时钟再汇聚悲观是：两条不同时钟路径部分共享物理路径段，共享段被假定对一路径为最小延时、对另一路径为最大延时。launch 与 capture 时钟路径使用不同延时时常出现，最常见于 OCV 分析。自动修正称为时钟再汇聚悲观移除（CRPR）。

CRPR 默认使能。可禁用以节省运行时间与内存（牺牲精度、增加悲观）。CRPR 仅减少悲观，故仅能增加报告 slack。若禁用 CRPR 时设计无违例，使能 CRPR 后仍无违例。

禁用 CRPR：在时序分析前将 \cmd{timing\_remove\_clock\_reconvergence\_pessimism} 设为 \texttt{false}。更改此变量会导致完整时序更新。

\subsection{片上变异示例}
\subsubsection*{On-Chip Variation Example}

\begin{lstlisting}
pt_shell> set_operating_conditions -analysis_type \
          on_chip_variation -min MIN -max MAX
pt_shell> set_timing_derate -net_delay -early 0.80
pt_shell> report_timing -delay_type min
pt_shell> report_timing -delay_type max
\end{lstlisting}

\figplaceholder{Figure 98: Clock reconvergence pessimism example}{时钟再汇聚悲观示例}{fig:crpr-ocv}

各延时有最小与最大值（最好/最坏工作条件）。LD2/CP 的 setup 检查将源锁存器时钟路径（CLK 到 LD1/CP）按 100\% 最坏，目标锁存器路径（CLK 到 LD2/CP）按 80\% 最坏。

虽为有效方法，但因 clock path1 与 path2 共享至 U1 输出的时钟树，分析悲观：共享段称为公共部分，最后单元输出为公共点（common point）。Setup 检查假定 U1 同时有 0.64 与 0.80 两种延时，悲观量为 0.16（公共点最晚与最早到达时间之差），即时钟再汇聚悲观。Hold 检查类似。

\subsection{再汇聚逻辑示例}
\subsubsection*{Reconvergent Logic Example}

\figplaceholder{Figure 99: Reconvergent logic in a clock network}{时钟网络中的再汇聚逻辑}{fig:crpr-reconv}

即使无 OCV，时钟网络中的再汇聚逻辑也可能产生时钟再汇聚：馈入多路选择器的两路时钟路径不能同时有效，但分析可能对同一次 setup/hold 同时考虑较短与较长路径。

\subsection{最小脉宽检查示例}
\subsubsection*{Minimum Pulse Width Checking Example}

\cmd{report\_constraint} 检查时钟网络（\cmd{set\_min\_pulse\_width}）与单元输入（逻辑库）的最小脉宽违例。CRPR 提高此检查精度。

\figplaceholder{Figure 100: Minimum pulse width analysis}{最小脉宽分析}{fig:crpr-mpw}

无 CRPR 时最坏脉宽可能极小并违例，因假设上升与下降边同时最坏延时。实际电路中两边延时至少部分相关。使能 CRPR 时，工具将一定 slack 加回最小脉宽计算：
\[
\text{crp} = \min[(M_r - m_r), (M_f - m_f)]
\]
$M_r/m_r$ 为累积最大/最小上升延时，$M_f/m_f$ 为下降。

\subsection{CRPR 报告}
\subsubsection*{CRPR Reporting}

\cmd{report\_timing}、\cmd{report\_constraint}、\cmd{report\_analysis\_coverage}、\cmd{report\_bottleneck} 详细报告会报告 CRPR 调整。示例 \cmd{report\_timing -delay_type max} 输出中含 \texttt{clock reconvergence pessimism} 行。

\subsection{公共点不同跳变的 CRPR 降额}
\subsubsection*{Derating CRPR for Different Transitions at the Common Point}

\cmd{timing\_clock\_reconvergence\_pessimism} 指定 launch 与 capture 时钟路径跳变不匹配时如何找最晚公共点。\texttt{normal}（默认）找最晚拓扑公共点（跳变可不同）；\texttt{same\_transition} 还要求跳变类型相同。

\figplaceholder{Figure 101: Common Point for Different timing\_clock\_reconvergence\_pessimism Settings}{不同 CRPR 变量设置下的公共点}{fig:crpr-common}

\texttt{normal} 适用于上升/下降到达时间高度相关；不高度相关时 \texttt{same\_transition} 保证保守（可能更悲观）分析。

可用 \texttt{normal} 公共点搜索并对公共点跳变不同时的 CRP 降额：
\begin{lstlisting}
set_app_var timing_crpr_different_transition_derate 0.90
\end{lstlisting}

跳变不同时 CRP 减至原值的 90\% 再加回 slack，比默认 100\% 更保守。

POCV 分析中可同时降额 CRP 变化：
\begin{lstlisting}
set_app_var timing_crpr_different_transition_derate 0.90
set_app_var timing_crpr_different_transition_variation_derate 0.90
\end{lstlisting}

公共点跳变相同时无效果；\texttt{timing\_clock\_reconvergence\_pessimism} 为 \texttt{same\_transition} 时也无效果。第一变量默认 1.0（标称不降额），第二默认 0.0（完全消除 CRP 变化）。

最小脉宽示例脚本：
\begin{lstlisting}
set_operating_conditions -analysis_type on_chip_variation
create_clock -period 8 CLK
set_propagated_clock [all_clocks]
set_clock_latency -source -early -1.3 CLK
set_clock_latency -source -late 1.4 CLK
set_annotated_delay -cell -from CT1/A -to CT1/Z 1
set_annotated_delay -cell -from CT2/A -to CT2/Z -min -rise 0.8
set_annotated_delay -cell -from CT2/A -to CT2/Z -max -rise 1.8
set_annotated_delay -cell -from CT2/A -to CT2/Z -min -fall 0.85
set_annotated_delay -cell -from CT2/A -to CT2/Z -max -fall 2.03
\end{lstlisting}

使能 CRPR 时 \cmd{report\_constraint} 路径报告含 \texttt{clock reconvergence pessimism 3.70} 等。

\subsection{CRPR 合并阈值}
\subsubsection*{CRPR Merging Threshold}

为计算效率，相邻点 CRP 差小于阈值时合并路径点。\cmd{timing\_crpr\_threshold\_ps} 以皮秒指定阈值，默认 5 ps。建议在性能与精度间取时钟网络典型门级延时（门延时+net 延时）的一半；设计阶段可用较大值，签核用较小值。

\subsection{CRPR 与串扰分析}
\subsubsection*{CRPR and Crosstalk Analysis}

用 PrimeTime SI 做串扰分析时，时钟路径公共段上因串扰的延时变化对零周期检查可能悲观（同一时钟边沿驱动 launch 与 capture）。其他路径类型不悲观，因不能假定 launch 与 capture 边沿的串扰变化相同。

因此 CRPR 仅在零周期检查时移除公共段上的串扰诱导延时。适用情形包括：标准 hold 检查、Q-bar 接 D 的寄存器、串扰反馈 hold、多周期路径为零的 hold、涉及透明锁存器的某些 setup 检查等。

\subsection{CRPR 与动态时钟到达}
\subsubsection*{CRPR With Dynamic Clock Arrivals}

动态反标（\cmd{set\_clock\_latency}、\cmd{set\_voltage} 设置的动态时钟 latency 与 rail 电压）可导致动态时钟到达。CRPR 与处理串扰延时相同：仅对零周期路径用动态时钟到达计算 CRP；其他路径仅用静态分量。

示例：早源 latency 2.5（静态 3.0 + 动态 $-0.5$）；晚源 latency 5.5（静态 5.0 + 动态 0.5）。静态 CRP $= 2$（5 减 3）；动态 CRP $= 3$（5.5 减 2.5）。

\subsection{透明锁存器边沿考虑}
\subsubsection*{Transparent Latch Edge Considerations}

路径终点为透明锁存器时，PrimeTime 计算两个 CRP 值：公共节点上升与下降各一。开/关时钟边沿各平移对应悲观量。

\figplaceholder{Figure 102: CRPR for latches}{锁存器的 CRPR}{fig:crpr-latch}

开边沿悲观影响非借用路径 slack 并减少借用路径借用时间；关边沿悲观增加最大借用时间并减少 setup 违例量。用 \cmd{report\_crpr} 报告锁存器 CRP 计算。

\subsection{报告 CRPR 计算}
\subsubsection*{Reporting CRPR Calculations}

\cmd{report\_crpr} 报告两寄存器时钟 pin 或端口间的 CRP 计算，含静态/动态条件及实际用于悲观移除的值。需指定 launch/capture pin、时钟与检查类型（setup/hold）：
\begin{lstlisting}
pt_shell> report_crpr -from [get_pins ffa/CP] \
            -to [get_pins ffd/CP] \
            -from_clock CLK -setup
\end{lstlisting}

\cmd{report\_crpr} 与 \cmd{report\_timing} 报告的 CRP 可能略有不同，因 \cmd{report\_timing} 为效率合并相邻点（\cmd{timing\_crpr\_threshold\_ps}，默认 5 ps）。不一致时 \cmd{report\_crpr} 更准确。

% ============================================================
\section{时钟片上变异悲观缩减}
\subsection*{Clock On-Chip Variation Pessimism Reduction}

\cmd{set\_timing\_derate} 可建模 OCV。launch 与 capture 时钟路径有公共段时，若使能 CRPR，会移除公共段延时降额导致的悲观，但默认仅在路径最终 slack 计算后移除，不在计算串扰到达窗口时移除。若通向 aggressor/victim 的时钟路径共享公共段，到达窗口可能过宽，导致边际重叠的串扰情形在准确 CRPR 下本不存在。

\figplaceholder{Figure 103: Clock reconvergence pessimism in crosstalk arrival windows}{串扰到达窗口中的时钟再汇聚悲观}{fig:ocv-xtalk}

无降额时到达窗口宽 1.0，不重叠；降额后公共点前长时钟路径早到 6.0、晚到 9.0，窗口扩至 3.0 并重叠，产生实际电路中不存在的串扰。

为在基于路径分析中获得最佳精度，可选在到达窗口重叠分析中应用 CRPR，移除公共点早/晚到达差异导致的悲观。设置：
\begin{lstlisting}
set_app_var pba_enable_xtalk_delay_ocv_pessimism_reduction true
\end{lstlisting}
默认 \texttt{false}。为 \texttt{true} 且 CRPR 使能时，PrimeTime SI 在计算 aggressor/victim 到达窗口时应用 CRPR，提高精度，代价是额外运行时间。基于路径分析在使用 \cmd{get\_timing\_paths} 或 \cmd{report\_timing} 的 \opt{-pba\_mode} 时发生。CRPR 在 \cmd{timing\_remove\_clock\_reconvergence\_pessimism} 为 \texttt{true} 时使能。
"""

write_ch("09_operating_conditions.tex", CHUNK1 + CHUNK2)
