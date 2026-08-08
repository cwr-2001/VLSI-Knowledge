# -*- coding: utf-8 -*-
"""Generate 16_signal_integrity.tex — Chapter 16 Signal Integrity Analysis."""
from pathlib import Path

OUT = Path(r"d:\IC Design\VLSI\PT_CN\chapters\16_signal_integrity.tex")
PARTS = []

PARTS.append(r"""% 第 16 章 Signal Integrity Analysis
\bichapter{信号完整性分析}{Signal Integrity Analysis}
\label{chap:si}

PrimeTime SI 是为 PrimeTime 静态时序分析器增加串扰分析能力的选项。PrimeTime SI 计算网间交叉耦合电容的时序效应，并将由此产生的延时变化纳入 PrimeTime 分析报告；同时计算串扰噪声的逻辑效应，报告可能导致功能失效的条件。运行 PrimeTime SI 需要 PrimeTime SI 许可证。

关于串扰分析与 PrimeTime SI，参见：
\begin{itemize}
  \item 信号完整性与串扰概述
  \item Aggressor 与 Victim 网
  \item 串扰延时分析
  \item 静态噪声分析
\end{itemize}

% ============================================================
\section{信号完整性与串扰概述}
\subsection*{Overview of Signal Integrity and Crosstalk}

信号完整性（signal integrity）是电信号可靠承载信息并抵抗邻近信号高频电磁干扰的能力。串扰（crosstalk）是两个或多个物理相邻网之间因电容交叉耦合产生的不良电相互作用。随着集成电路工艺向更小几何尺寸发展，与单元延时和网线延时相比，串扰效应日益重要。

工艺尺寸缩小时，互连线间距更近、高度增加，网间交叉耦合电容增大；同时互连线变窄使对衬底寄生电容减小，晶体管变小使单元延时降低。

PrimeTime SI 可分析并报告两类主要串扰效应：延时与静态噪声。可选择仅计算串扰延时、仅计算串扰噪声，或两者皆算。

\subsection{串扰延时效应}
\subsubsection*{Crosstalk Delay Effects}

串扰通过改变信号跳变发生时刻影响信号延时。图~\ref{fig:si-crosstalk-waveform} 示交叉耦合网 A、B、C 上的信号波形。

\figplaceholder{Figure 148: Transition slowdown or speedup caused by crosstalk}{串扰引起的跳变减慢或加快}{fig:si-crosstalk-waveform}

由于电容交叉耦合，网 A 与网 C 上的跳变可影响网 B 上跳变发生的时刻。图中所示时刻网 A 的上升沿可使网 B 上的跳变推迟，可能加剧含 B 的路径的 setup 违例；网 C 的下降沿可使网 B 上的跳变提前，可能加剧 hold 违例。

PrimeTime SI 确定最坏情况的延时变化量，用该信息计算并报告总 slack；同时报告串扰延时位置与大小，以便修改设计或版图以降低关键点的串扰。

\subsection{Delta 延时与扇出级效应}
\subsubsection*{Delta Delay and Fanout Stage Effect}

串扰效应使开关波形畸变，从而给扇出级的传播波形增加延时（图~\ref{fig:si-delta-fanout}）。

\figplaceholder{Figure 149: Delta delay includes the fanout stage effect}{Delta 延时包含扇出级效应}{fig:si-delta-fanout}

PrimeTime SI 计算 delta 延时（串扰在开关网上引起的额外延时）。扇出级效应（fanout stage effect）表示传播到扇出级的延时；PrimeTime SI 将其作为 delta 延时的一部分。

\subsection{串扰噪声效应}
\subsubsection*{Crosstalk Noise Effects}

PrimeTime SI 还确定稳态网上串扰噪声的逻辑效应。图~\ref{fig:si-noise-bump} 示交叉耦合网 A 与 B 上的噪声凸起示例。

\figplaceholder{Figure 150: Noise bump due to crosstalk}{串扰引起的噪声凸起}{fig:si-noise-bump}

网 B 应恒为逻辑 0，但网 A 的上升沿在 B 上引起噪声凸起或毛刺（glitch），若足够大可能被下游逻辑错误采样。

PrimeTime SI 考虑这些效应，确定串扰噪声凸起在何处可能导致逻辑失效，并报告噪声 slack 与违例。

% ============================================================
\section{Aggressor 与 Victim 网}
\subsection*{Aggressor and Victim Nets}

在串扰分析中，\textbf{aggressor（侵扰网）}是对另一网产生串扰效应的网；\textbf{victim（受害网）}是受串扰影响的网。同一网在不同分析中可既是 aggressor 又是 victim。

aggressor 对 victim 的时序效应取决于多种因素：
\begin{itemize}
  \item 交叉耦合电容大小
  \item aggressor 与 victim 跳变的相对时间与方向
  \item aggressor 驱动强度与 victim 负载
  \item 逻辑相关性（多个 aggressor 是否可同时同向开关）
\end{itemize}

PrimeTime SI 计算串扰效应时考虑所有这些因素。

\figplaceholder{Figure 151: Effects of crosstalk at different arrival times}{不同到达时刻的串扰效应}{fig:si-aggr-window}

图~\ref{fig:si-aggr-window} 说明时序考虑对串扰计算的重要性。aggressor 信号 A 有从早到晚的可能到达时间范围。

若 A 的跳变与 B 的跳变大致同时，串扰对 B 的延时影响最大。若 A 跳变较早，在 B 上感应向上毛刺，可能不影响 B 的延时（若 B 尚未开关）。若 A 跳变较晚，在 B 跳变之后感应凸起，同样可能不影响 B 的延时。

\subsection{时序窗口与串扰延时分析}
\subsubsection*{Timing Windows and Crosstalk Delay Analysis}

PrimeTime 提供 single 与 on-chip variation 两种工作条件分析模式。使用 on-chip variation 模式时，PrimeTime SI 为 aggressor 与 victim 找到最早与最晚到达时间，形成到达窗口（arrival window）。

默认 PrimeTime SI 用两次迭代执行串扰分析。第一次迭代不考虑时序窗口（保守假设所有 aggressor 在最坏时刻最坏方向跳变）；第二次及以后迭代根据 aggressor 与 victim 跳变的时间分离与方向剔除不可能发生的串扰延时。

\subsection{交叉耦合模型}
\subsubsection*{Cross-Coupling Models}

\figplaceholder{Figure 152: Detailed model of cross-coupled nets}{交叉耦合网的详细模型}{fig:si-cc-model}

详细 SPICE 级模型可非常准确预测仿真中的串扰，但对实际集成电路元素过多。给定外部工具提供的足够准确且足够简单的交叉耦合电容网络，PrimeTime SI 可在合理时间内获得准确串扰分析结果。
""")

PARTS.append(r"""
% ============================================================
\section{串扰延时分析}
\subsection*{Crosstalk Delay Analysis}

使用 PrimeTime SI 进行串扰延时分析的基础，参见：
\begin{itemize}
  \item 执行串扰延时分析
  \item PrimeTime SI 如何工作
  \item 使用指南
  \item 时序报告
  \item 报告串扰设置
  \item 双开关检测
\end{itemize}

\subsection{执行串扰延时分析}
\subsubsection*{Performing Crosstalk Delay Analysis}

PrimeTime SI 串扰延时分析使用与普通 PrimeTime 相同的命令集、库与 Tcl 脚本。额外步骤：
\begin{enumerate}
  \item 启用 PrimeTime SI：\cmd{set\_app\_var si\_enable\_analysis true}
  \item 用 SPEF 或 GPD 回标交叉耦合电容：\cmd{read\_parasitics -keep\_capacitive\_coupling file\_name.spf}
  \item （可选）设置控制串扰分析速度与精度的变量（见「PrimeTime SI 变量」）
  \item 若时序报告显示明显串扰效应，调试或修正；GUI 可生成串扰延时与感应电压直方图
\end{enumerate}

示例脚本（串扰相关加粗）：
\begin{lstlisting}
set_operating_conditions -analysis_type on_chip_variation
set_app_var si_enable_analysis true
read_verilog ./test1.v
current_design test1
link_design
read_parasitics -keep_capacitive_coupling SPEF.spf
create_clock -period 5.0 clock
check_timing -include { no_driving_cell ideal_clocks \
  partial_input_delay unexpandable_clocks }
report_timing
report_si_bottleneck
report_delay_calculation -crosstalk -from pin -to pin
\end{lstlisting}

\cmd{set\_operating\_conditions} 将分析类型设为 \texttt{on\_chip\_variation}，使 PrimeTime SI 正确处理 min/max 时序窗口关系；未显式指定时 PrimeTime SI 自动切换。

读取 SPEF 时须确保耦合电容对称。先读入设计，再用 \cmd{read\_parasitics -syntax\_only -keep\_capacitive\_coupling}；若发现非对称耦合，PrimeTime 发出警告。

\subsection{PrimeTime SI 如何工作}
\subsubsection*{How PrimeTime SI Operates}

启用串扰分析后，\cmd{update\_timing} 或 \cmd{report\_timing} 时 PrimeTime SI 执行图~\ref{fig:si-flow} 所示步骤。

\figplaceholder{Figure 153: PrimeTime SI Crosstalk Analysis Flow}{PrimeTime SI 串扰分析流程}{fig:si-flow}

\textbf{电气滤波（electrical filtering）}：根据 victim 网上计算的凸起电压大小，移除影响过小的 aggressor。可指定阈值。

\textbf{初始网选择}：从未被滤除的网中选择初始串扰分析网集；可指定包含或排除特定网。

\textbf{延时计算}：对所选网执行含串扰考虑的延时计算。

\textbf{迭代}：串扰分析为迭代过程。初始迭代不考虑时序窗口（保守最坏假设）；后续迭代考虑 victim 跳变时间与方向，剔除不可能发生的串扰延时。默认第二次迭代后退出，通常可在合理时间内获得良好结果。

可按 Ctrl+C 中断当前迭代；PrimeTime SI 完成当前迭代后退出循环并报告诊断信息。

\subsection{PrimeTime SI 变量}
\subsubsection*{PrimeTime SI Variables}

表~\ref{tab:si-vars} 列出控制串扰分析的变量。启用串扰分析须 \cmd{si\_enable\_analysis true}。

\begin{table}[htbp]
\centering
\caption{PrimeTime SI 变量（表 33，节选）}
\label{tab:si-vars}
\footnotesize
\begin{tabularx}{\textwidth}{@{}lX@{}}
\toprule
变量 & 默认设置 \\
\midrule
\cmd{delay\_calc\_waveform\_analysis\_mode} & disabled \\
\cmd{si\_analysis\_logical\_correlation\_mode} & true \\
\cmd{si\_ccs\_aggressor\_alignment\_mode} & lookahead \\
\cmd{si\_enable\_analysis} & false \\
\cmd{si\_filter\_accum\_aggr\_noise\_peak\_ratio} & 0.03 \\
\cmd{si\_filter\_per\_aggr\_noise\_peak\_ratio} & 0.01 \\
\cmd{si\_noise\_composite\_aggr\_mode} & disabled \\
\cmd{si\_xtalk\_composite\_aggr\_mode} & disabled \\
\cmd{si\_xtalk\_delay\_analysis\_mode} & all\_paths \\
\cmd{si\_xtalk\_double\_switching\_mode} & disabled \\
\cmd{si\_xtalk\_exit\_on\_max\_iteration\_count} & 2 \\
\cmd{si\_xtalk\_max\_transition\_mode} & uncoupled \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{逻辑相关性}
\subsubsection*{Logical Correlation}

保守分析假设所有 aggressor 可同时同向开关，导致 victim 最坏减慢或加快。某些情况下因逻辑关系，aggressor 不能同向同时开关。

\figplaceholder{Figure 154: Logical Correlation}{逻辑相关性}{fig:si-logical-corr}

默认 PrimeTime SI 考虑经缓冲器与反相器的多 aggressor 逻辑关系，提供更准确（更少悲观）的多 aggressor 分析。将 \cmd{si\_analysis\_logical\_correlation\_mode} 设为 \texttt{false} 可禁用，分析更快但更悲观。

\subsection{电气滤波}
\subsubsection*{Electrical Filtering}

为在合理时间内获得准确结果，PrimeTime SI 滤除对 victim 凸起贡献过小的 aggressor。若单个 aggressor 在 victim 上的凸起高度贡献很小（低于每 aggressor 阈值），则滤除。

\figplaceholder{Figure 155: Voltage bumps from multiple aggressors}{多 aggressor 的电压凸起}{fig:si-multi-aggr}

多个较小 aggressor 的组合若低于另一较大累积阈值，也可能被滤除。可提高阈值以加快运行、降低精度，或降低阈值以提高精度、增加运行时间。

\subsection{使用指南}
\subsubsection*{Usage Guidelines}

多数 PrimeTime SI 变量在分析精度与执行时间之间权衡。

\subsubsection{准备运行串扰分析}
\paragraph*{Preparing to Run Crosstalk Analysis}

首先确保设计约束良好且通过常规静态时序检查。

\paragraph*{电容耦合数据}

用 \cmd{read\_parasitics -keep\_capacitive\_coupling} 读入 SPEF/GPD。若提取工具支持基于阈值滤除小电容，注意不要滤得过激导致 PrimeTime SI 遗漏重要耦合。PrimeTime SI 忽略网与自身的交叉耦合。

\paragraph*{工作条件}

PrimeTime SI 使用 on-chip variation 工作条件寻找 aggressor 与 victim 到达窗口。未显式设置 \texttt{on\_chip\_variation} 时自动切换，影响包括 min/max 条件分离等。

\paragraph*{使用 check\_timing}

\cmd{check\_timing} 可检查多种串扰相关条件：\texttt{no\_input\_delay}、\texttt{partial\_input\_delay}、\texttt{unexpandable\_clocks}、\texttt{no\_driving\_cell} 等。除 \texttt{ideal\_clocks} 外，串扰相关检查默认开启。

\subsection{包含或排除特定网的串扰分析}
\subsubsection*{Including or Excluding Specific Nets From Crosstalk Analysis}

\begin{itemize}
  \item \cmd{set\_si\_delay\_analysis -include/-exclude} — 串扰延时
  \item \cmd{set\_si\_noise\_analysis -include/-exclude} — 串扰噪声
  \item \cmd{set\_coupling\_separation} — 物理分离（不参与耦合）
  \item \cmd{set\_si\_aggressor\_exclusion} / \cmd{set\_si\_victim\_exclusion} — 排除 aggressor-victim 对
\end{itemize}

\cmd{set\_coupling\_separation}、\cmd{set\_si\_delay\_analysis} 等设置冲突时，排除设置优先。

可仅排除 victim 的上升或下降沿（\cmd{set\_si\_delay\_analysis -rise/-fall}），或排除 setup/hold 分析。

\subsubsection{排除时钟网}
\paragraph*{Excluding Clock Nets}

若时钟延时受串扰影响不显著，可用 \cmd{set\_si\_delay\_analysis -exclude [get\_nets CLK*]} 将时钟网排除为 victim。

\subsubsection{排除安静 aggressor}
\paragraph*{Excluding Quiet Aggressor Nets}

\cmd{set\_si\_aggressor\_exclude} 将特定网标为安静（不开关）aggressor。

\subsubsection{排除 aggressor-victim 对}
\paragraph*{Excluding Aggressor-Victim Pairs}

\cmd{set\_si\_aggressor\_exclusion -exclude} 与 \cmd{set\_si\_victim\_exclusion -exclude} 配合排除特定对，例如扫描时钟与功能时钟之间已知无同时开关的情况。

\subsubsection{Aggressor 互斥组}
\paragraph*{Exclusive Groups of Aggressors}

\figplaceholder{Figure 156: One-Hot Decoder Multiple Aggressor Example}{One-hot 译码器多 aggressor 示例}{fig:si-onehot}

\figplaceholder{Figure 157: Multiple aggressor arrival windows at decoder outputs}{译码器输出处多 aggressor 到达窗口}{fig:si-decoder-window}

默认多个 aggressor 到达窗口与 victim 跳变重叠时，假设所有 aggressor 同时活跃。可用 \cmd{set\_si\_exclusive\_groups} 指定互斥 aggressor 组以降低悲观度：

\begin{table}[htbp]
\centering
\caption{互斥组对 aggressor 活跃性的影响}
\small
\begin{tabular}{@{}llll@{}}
\toprule
 & Agg1 & Agg2 & Agg3 \\
\midrule
无互斥组 & Quiet & Active & Active \\
互斥组 \{agg1 agg2 agg3\} & Quiet & Active & Quiet \\
\bottomrule
\end{tabular}
\end{table}

移除排除：\cmd{reset\_si\_aggressor\_exclusion}、\cmd{reset\_si\_victim\_exclusion}、\cmd{reset\_si\_exclusive\_groups} 等。
""")

PARTS.append(r"""
\subsection{Victim-Aggressor 对齐与窗口模式}
\subsubsection*{Victim-Aggressor Switching Time Alignment}

\figplaceholder{Figure 158: Victim-aggressor switching time alignment}{Victim-aggressor 开关时间对齐}{fig:si-align}

\figplaceholder{Figure 159: Multiple aggressor alignment}{多 aggressor 对齐}{fig:si-multi-align}

PrimeTime SI 将 aggressor 到达窗口与 victim 跳变时间对齐以计算 delta 延时。异步时钟之间 aggressor 视为相对 victim 的无限窗口。

\subsection{「All Paths」与「All Path Edges」重叠模式}
\subsubsection*{``All Paths'' Window Versus ``All Path Edges'' Overlap Modes}

默认考虑 victim 网上所有路径的最早到最晚到达时间范围（\texttt{all\_paths}）。任一 aggressor 窗口与「所有路径」victim 窗口重叠即触发 delta 延时计算。

\figplaceholder{Figure 160: ``All Paths'' (Default) Window Overlap Mode}{「所有路径」（默认）窗口重叠模式}{fig:si-all-paths}

该模式简单快速但保守——实际 victim 跳变可能不与 aggressor 窗口重叠。对关键路径可：
\begin{itemize}
  \item 基于路径分析：\cmd{report\_timing -pba\_mode path} 或 \texttt{exhaustive}
  \item 「所有路径边」模式：\cmd{set\_app\_var si\_xtalk\_delay\_analysis\_mode all\_path\_edges}
\end{itemize}

\figplaceholder{Figure 161: ``All Path Edges'' Overlap Mode}{「所有路径边」重叠模式}{fig:si-all-edges}

\figplaceholder{Figure 162: ``All Path Edges'', Aggressor Between Edges}{「所有路径边」模式，aggressor 窗口位于边之间}{fig:si-between-edges}

\texttt{all\_path\_edges} 考虑实际早/晚到达边时刻，不合并为连续窗口；对最大延时分析，若晚边不与 aggressor 重叠则不施加 delta 延时。

\subsection{时钟组}
\subsubsection*{Clock Groups}

\cmd{set\_clock\_groups} 指定时钟间关系，使 PrimeTime SI 正确分析时钟间串扰。

\figplaceholder{Figure 163: Circuit with multiplexed clocks}{含复用时钟的电路}{fig:si-mux-clk}

时钟可定义为逻辑互斥（\texttt{-logically\_exclusive}）、物理互斥（\texttt{-physically\_exclusive}）或异步（\texttt{-asynchronous}）。逻辑互斥抑制逻辑时序检查但 SI 仍检查串扰；物理互斥假定无串扰交互；异步时钟使用无限到达窗口。

最准确做法是对每种时钟组合分别分析，或用 DMSA。时钟数量极大时，可用 \cmd{set\_clock\_groups} 在单次运行中指定关系，或用 case analysis 分多次分析。

\subsection{Delta 延时合并与多时钟}
\subsubsection*{Delta Delay Merging Across Clocks}

\cmd{si\_xtalk\_delay\_merge\_mode} 控制跨时钟域 delta 延时的合并方式：\texttt{all\_clocks}（默认，最保守）、\texttt{physically\_exclusive\_clocks}、\texttt{none} 等。对物理互斥时钟组可分别合并 delta 延时以降低悲观度与内存。

\subsection{时序报告}
\subsubsection*{Timing Reports}

\cmd{report\_timing} 在启用 SI 时显示 delta 延时列。\cmd{report\_si\_bottleneck} 报告串扰瓶颈网。\cmd{report\_delay\_calculation -crosstalk} 显示单条弧的详细串扰计算，包括各 aggressor 贡献、滤波状态与对齐信息。

串扰相关网属性包括：\texttt{delta\_delay}、\texttt{si\_aggressor\_nets}、\texttt{si\_victim\_nets}、\texttt{si\_double\_switching\_slack} 等。

\subsection{报告串扰设置}
\subsubsection*{Reporting Crosstalk Settings}

\cmd{report\_si\_options} 报告当前串扰分析设置与变量值。\cmd{report\_coupling\_capacitance} 报告耦合电容。\cmd{report\_si\_aggressor\_exclusion} 等报告排除设置。

\subsection{双开关检测}
\subsubsection*{Double-Switching Detection}

双开关（double-switching）指 victim 在预期稳定期间因 aggressor 耦合发生额外跳变，可能导致时钟网络上功能错误。

将 \cmd{si\_xtalk\_double\_switching\_mode} 设为 \texttt{clock\_network} 或 \texttt{full\_design} 启用检测。工具计算双开关错误并报告为双开关 slack；风险越高 slack 越负。slack 存于 \texttt{si\_double\_switching\_slack} 网属性。

\subsubsection{报告双开关违例}
\paragraph*{Reporting Double-Switching Violations}

\cmd{report\_si\_double\_switching} 报告所有检测到双开关的 victim 网。\opt{-clock\_network} 仅报告时钟网。\opt{-rise}/\opt{-fall} 过滤上升/下降 victim。

示例输出：
\begin{lstlisting}
pt_shell> report_si_double_switching -nosplit
Victim  Switching  Actual      Required    Double Switching
Net     Direction  Bump Height Bump Height Slack
I2      max_rise   0.69        0.42        -0.26 (Violating)
I1      max_fall   0.50        0.30        -0.20 (Violating)
\end{lstlisting}

\cmd{report\_delay\_calculation -crosstalk} 在启用双开关模式时显示 victim 上是否存在双开关违例。

\subsubsection{修复双开关违例}
\paragraph*{Fixing Double-Switching Violations}

可通过增大线间距、屏蔽相邻线降低交叉电容，或加大 victim 驱动降低 transition time。时序违例可用 \cmd{fix\_eco\_timing} 修复。
""")

PARTS.append(r"""
% ============================================================
\section{静态噪声分析}
\subsection*{Static Noise Analysis}

PrimeTime SI 可分析稳态网上串扰噪声导致的逻辑失效。参见：
\begin{itemize}
  \item 静态噪声分析概述
  \item PrimeTime SI 噪声分析流程
  \item 噪声分析命令
  \item 使用 CCS 噪声数据的噪声建模
  \item 使用非线性延时模型的噪声建模
\end{itemize}

\subsection{静态噪声分析概述}
\subsubsection*{Static Noise Analysis Overview}

静态噪声分析用于找出设计中最坏的噪声效应以便降低或消除，从而最大化成品可靠性。与静态时序分析一样，不依赖测试向量或电路仿真，而考虑 aggressor 与 victim 间交叉耦合电容、aggressor 跳变到达窗口、aggressor 驱动特性、victim 驱动器稳态负载特性及噪声穿过单元的传播。

\figplaceholder{Figure 175: Crosstalk effects on timing and steady-state voltage}{串扰对时序与稳态电压的效应}{fig:si-sta-vs-sna}

静态时序分析确定串扰引起的 victim 最坏延时变化；静态噪声分析确定稳态 victim 网上最坏噪声凸起或毛刺（稳态指网恒为逻辑 1 或 0）。稳态网上的噪声凸起可沿时序路径传播，在端点被错误捕获为数据。

主要噪声命令：\cmd{check\_noise}、\cmd{update\_noise}、\cmd{report\_noise}，分别类似于 \cmd{check\_timing}、\cmd{update\_timing}、\cmd{report\_timing}。

\figplaceholder{Figure 176: Combined effects of crosstalk and propagated noise}{串扰与传播噪声的 combined 效应}{fig:si-noise-combined}

\cmd{check\_noise} 检查驱动器与负载引脚处噪声模型的存在与有效性。\cmd{update\_noise} 执行噪声分析并用噪声凸起信息更新设计。\cmd{report\_noise} 报告最坏噪声效应，包括宽度、高度与噪声 slack。

\subsection{噪声凸起特性}
\subsubsection*{Noise Bump Characteristics}

电子设计中的「噪声」通常指应保持恒定电压的网上任何不良电压偏差。深亚微米 CMOS 中主导效应是物理相邻逻辑网之间的串扰噪声及由此产生的串扰凸起在单元输入到输出的传播。

噪声效应（电压-时间曲线）可有多种形态：凸起、振铃、阻尼振荡等。PrimeTime SI 将噪声凸起参数化为高度（height）、宽度（width）与 time-to-peak（或 time-peak-ratio）。

\subsection{PrimeTime SI 噪声分析流程}
\subsubsection*{PrimeTime SI Noise Analysis Flow}

噪声分析流程：
\begin{enumerate}
  \item 启用：\cmd{si\_enable\_analysis true}（与延时分析共用）
  \item 读入含耦合电容的寄生参数
  \item \cmd{check\_noise} 验证噪声模型
  \item \cmd{update\_noise} 更新噪声分析
  \item \cmd{report\_noise} 报告违例与 slack
\end{enumerate}

噪声分析可与串扰延时分析迭代协同，或独立运行。

\subsection{噪声分析命令}
\subsubsection*{Noise Analysis Commands}

\begin{table}[htbp]
\centering
\caption{主要噪声分析命令}
\label{tab:si-noise-cmds}
\small
\begin{tabularx}{\textwidth}{@{}lX@{}}
\toprule
命令 & 说明 \\
\midrule
\cmd{check\_noise} & 检查噪声模型与网表完整性 \\
\cmd{update\_noise} & 执行噪声分析并更新数据库 \\
\cmd{report\_noise} & 报告最坏噪声凸起与 slack \\
\cmd{report\_noise\_calculation} & 详细噪声计算报告 \\
\cmd{set\_si\_noise\_analysis} & 包含/排除网的噪声分析 \\
\cmd{reset\_si\_noise\_analysis} & 重置噪声分析设置 \\
\bottomrule
\end{tabularx}
\end{table}

\cmd{report\_noise} 常用选项：\opt{-all}、\opt{-violators}、\opt{-nosplit}、\opt{-significant\_digits}、\opt{-height\_threshold}、\opt{-slack\_lesser\_than}。

\subsection{使用 CCS 噪声数据的噪声建模}
\subsubsection*{Noise Modeling With CCS Noise Data}

Composite Current Source（CCS）噪声模型提供更准确的驱动器与接收器噪声特性。库中含 \texttt{output\_current\_*} 与噪声相关表格时，PrimeTime SI 使用 CCS 噪声分析。

CCS 噪声分析考虑：
\begin{itemize}
  \item 非线性 I-V 特性
  \item 多 aggressor 叠加
  \item 噪声传播与衰减
  \item 噪声免疫曲线（noise immunity curve）
\end{itemize}

推荐对先进工艺节点使用含 CCS 噪声数据的库。

\subsection{使用非线性延时模型（NLDM）的噪声建模}
\subsubsection*{Noise Modeling With Nonlinear Delay Models}

对仅有 NLDM 时序数据的库，PrimeTime SI 使用简化的噪声分析模型，精度低于 CCS。噪声免疫可用曲线、表或多项式指定。

\subsection{噪声免疫与 Slack 计算}
\subsubsection*{Noise Immunity and Slack Calculation}

噪声免疫（noise immunity）定义输入引脚可容忍而不导致逻辑失效的噪声凸起。可用 \texttt{noise\_immunity\_*} 库组（曲线、表或多项式）指定。

\cmd{si\_noise\_slack\_method} 控制 slack 计算方法：
\begin{itemize}
  \item \texttt{height} — 给定凸起高度的电压裕量（库电压单位）
  \item \texttt{area} — 电压裕量乘以凸起宽度
  \item \texttt{area\_percent} — 面积 slack 除以约束面积
\end{itemize}

\figplaceholder{Figure 197: Area slack calculation}{面积 slack 计算}{fig:si-area-slack}

\figplaceholder{Figure 198: Area percent slack calculation}{面积百分比 slack 计算}{fig:si-area-pct-slack}

对低于失效阈值的凸起 slack 为正，高于则为负。

\subsection{传播噪声特性}
\subsubsection*{Propagated Noise Characteristics}

足够大的输入噪声凸起会在单元输出引起输出噪声凸起，称为噪声传播（noise propagation）。

\figplaceholder{Figure 199: Noise propagation characterization}{噪声传播表征}{fig:si-noise-prop}

噪声传播通过在输入施加不同高度与宽度的凸起并测量输出凸起来表征。输出特性取决于输入凸起宽高、输出负载及 time-peak-ratio。

库语法支持两种指定传播效应的方式：
\begin{itemize}
  \item \textbf{多项式}：输出凸起高度、宽度、time-peak-ratio 为输入凸起参数与负载的函数；每时序弧 12 个多项式（四种输出凸起类型 $\times$ 三种函数）
  \item \textbf{查找表}：输出高度与宽度为输入高度、输入宽度与负载的函数；每弧八个表（四种类型 $\times$ 高度/宽度）
\end{itemize}

time-peak-ratio 为 time-to-peak 除以凸起宽度，取值 0.0--1.0；对称凸起为 0.5。

\begin{table}[htbp]
\centering
\caption{库中传播噪声的指定方法（表 40）}
\label{tab:si-noise-lib}
\small
\begin{tabularx}{\textwidth}{@{}llX@{}}
\toprule
指定方法 & 库类型 & 库中如何指定 \\
\midrule
查找表 & NLDM & 每时序弧四对查找表（八种），按输入凸起高度、宽度与输出负载给出输出高度与宽度；分别对应 above low、below low、above high、below high \\
多项式 & CCS/NLDM & 输出高度、宽度、time-peak-ratio 的多项式函数 \\
\bottomrule
\end{tabularx}
\end{table}

\subsection{多 Aggressor 噪声合成}
\subsubsection*{Composite Aggressor Noise}

\cmd{si\_noise\_composite\_aggr\_mode} 控制多 aggressor 噪声合成方式。\texttt{disabled}（默认）采用保守叠加；启用 composite 模式可用统计或峰值比方法合成多 aggressor 效应。

\cmd{si\_xtalk\_composite\_aggr\_mode} 类似地控制串扰延时分析中的多 aggressor 合成。

\subsection{噪声端点过滤与传播限制}
\subsubsection*{Noise Endpoint Filtering and Propagation Limits}

\cmd{si\_noise\_endpoint\_height\_threshold\_ratio} 设置端点高度阈值比例，低于阈值的传播噪声可能被忽略。\cmd{si\_noise\_limit\_propagation\_ratio} 限制噪声沿路径传播的程度。

\cmd{si\_noise\_slack\_skip\_disabled\_arcs} 控制是否跳过 disabled 弧上的噪声 slack 计算。

\subsection{报告与调试噪声}
\subsubsection*{Reporting and Debugging Noise}

\cmd{report\_noise -violators} 仅报告违例。\cmd{report\_noise\_calculation -from pin -to pin} 显示详细计算，包括各 aggressor 贡献、免疫曲线交点与传播阶段。

噪声相关属性：\texttt{noise\_slack}、\texttt{noise\_peak}、\texttt{actual\_noise\_height}、\texttt{allowed\_noise\_height} 等。

\subsection{修复噪声违例}
\subsubsection*{Fixing Noise Violations}

常见修复方法：
\begin{itemize}
  \item 增大 aggressor 与 victim 间距或插入屏蔽线
  \item 加大 victim 驱动或 victim 网负载电容（降低噪声敏感度）
  \item 插入缓冲器隔离长 victim 网
  \item 调整布线层或 via 策略
  \item 使用 \cmd{fix\_eco\_timing} 或物理 ECO 工具
\end{itemize}

\begin{seeAlsoBox}
Library Compiler 文档中的噪声库语法；SolvNetPlus 上 PrimeTime SI 应用笔记；第~\ref{chap:mv}~章多电压分析（aggressor/victim 电源轨电压）；第~\ref{chap:var}~章片上师变异。
\end{seeAlsoBox}

\begin{noteBox}
PrimeTime SI 需要含耦合电容的 SPEF/GPD 寄生文件及支持噪声分析的库（推荐 CCS 噪声模型）。无 CCS 噪声模型时，部分分析（如双开关 slack）可能不受约束（\texttt{INFINITY}）。
\end{noteBox}
""")

text = "\n".join(PARTS)
OUT.write_text(text, encoding="utf-8")
cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
print(f"Wrote {OUT} bytes={OUT.stat().st_size} lines={text.count(chr(10))+1} CJK={cjk}")
