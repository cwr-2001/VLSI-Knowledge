# -*- coding: utf-8 -*-
"""Generate 19_reporting_debugging.tex with proper UTF-8 encoding."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "chapters" / "19_reporting_debugging.tex"
C = []

def S(*parts):
    C.append("".join(parts))

S(r"""% 第 19 章 Reporting and Debugging Analysis Results
\bichapter{报告与调试分析结果}{Reporting and Debugging Analysis Results}
\label{chap:report}

加载并约束设计、指定分析条件后，可执行完整静态时序分析并报告时序与设计规则违例。还可生成多种报告以检查与调试违例。常用报告包括：
\begin{itemize}
  \item 全局时序摘要报告
  \item 路径时序报告
  \item 结果质量（QoR）报告
  \item 约束报告
  \item 瓶颈报告
  \item 全局 slack 报告
  \item 分析覆盖率报告
  \item 时钟网络时序报告
  \item 时钟门控与 recovery/removal 检查
  \item 时序更新效率
  \item 基于路径的时序分析（PBA）
\end{itemize}

""")

S(r"""% ============================================================
\section{全局时序摘要报告}
\subsection*{Global Timing Summary Report}

\cmd{report\_global\_timing} 报告设计全局时序收敛状态，包括最差负 slack（WNS）、总负 slack（TNS）等端点级信息。与 PBA、DMSA、SMVA/DVFS 等特性配合使用。

特性：
\begin{itemize}
  \item 仅考虑违例时序路径，不收集/分析通过路径
  \item 按四种拓扑路径类别组织：\texttt{in->reg}、\texttt{reg->reg}、\texttt{reg->out}、\texttt{in->out}
  \item 分两阶段：路径收集（gathering）与报告输出（reporting），由不同选项独立配置
\end{itemize}

\subsubsection{控制路径收集}
\subsection*{Controlling report\_global\_timing Path Gathering}

默认：每个端点收集单条最差路径（不限拓扑类型或路径组）。表 51 选项：

\begin{table}[htbp]
\centering
\caption{控制 \cmd{report\_global\_timing} 路径收集（表 51）}
\small
\begin{tabular}{@{}p{5.5cm}p{6.5cm}@{}}
\toprule
目的 & 选项 \\
\midrule
仅 setup(max) 或 hold(min) & \cmd{-delay\_type min|max} \\
每端点每路径组最差路径 & \cmd{-group group\_list} \\
每端点每拓扑类别最差路径 & \cmd{-enable\_multiple\_categories\_per\_endpoint} \\
每端点每类别+路径组+发射/捕获时钟组合 & \cmd{-include \{per\_clock\_violations\}} \\
PBA 收集路径 & \cmd{-pba\_mode none|path|exhaustive|ml\_exhaustive} \\
限定 DVFS 场景 & \cmd{-dvfs\_scenarios dvfs\_scenarios} \\
\bottomrule
\end{tabular}
\end{table}

示例设计含 CLK1/CLK2/CLK3 与输入/输出延迟。默认行为仅每端点一条最差路径；\cmd{-group \{CLK1 CLK2\}} 为指定组各报告一条；\cmd{-enable\_multiple\_categories\_per\_endpoint} 为四拓扑类别各一条；\cmd{-include \{per\_clock\_violations\}} 为每组、每发射/捕获时钟组合各一条。

\subsubsection{控制报告输出}
\subsection*{Controlling report\_global\_timing Report Output}

默认生成摘要表：setup/hold 下四拓扑类别的 WNS、TNS、违例端点数（NUM）。表 52 选项：

\begin{table}[htbp]
\centering
\caption{控制 \cmd{report\_global\_timing} 报告（表 52）}
\small
\begin{tabular}{@{}p{5.5cm}p{6.5cm}@{}}
\toprule
目的 & 选项 \\
\midrule
摘要表或逐端点表 & \cmd{-path\_type summary|end}（默认 summary） \\
非标准路径组单独表 & \cmd{-separate\_non\_standard\_groups} \\
所有路径组单独表 & \cmd{-separate\_all\_groups} \\
发射/捕获时钟组合单独表 & \cmd{-include \{per\_clock\_violations inter\_clock\}} \\
包含空类别（零路径） & \cmd{-include \{non\_violated\}} \\
DMSA 场景详情 & \cmd{-include \{scenario\_details\}} \\
窄/宽表格式 & \cmd{-format narrow|wide} \\
CSV 输出 & \cmd{-format csv -output filename} \\
有效数字 & \cmd{-significant\_digits digits} \\
\bottomrule
\end{tabular}
\end{table}

非标准路径组为 \texttt{**default**}、\texttt{**async\_default**}、\texttt{**clock\_gating\_default**}。

\cmd{-path\_type end} 显示逐端点贡献。\cmd{-include \{per\_clock\_violations inter\_clock\}} 显示跨时钟（C2C）摘要表（如 \texttt{C2C * -> CLK1}）。\cmd{-format wide} 将 WNS/TNS/NUM 列式排列。

""")

S(r"""% ============================================================
\section{路径时序报告}
\subsection*{Path Timing Report}

路径时序报告用于聚焦特定违例并确定原因。默认 \cmd{report\_timing} 报告最差 setup slack 路径。可显示：逻辑级、各级增量延迟、路径总延迟、slack、源/目的时钟名/latency/uncertainty、去除 CRPR 的 OCV 等。

\subsubsection{使用 \cmd{report\_timing} 命令}
\subsection*{Using the report\_timing Command}

\cmd{-significant\_digits} 仅控制显示位数，不影响内部分析精度。

典型报告含：起点、终点、路径组、路径类型、各级 Point/Incr/Path、到达/要求时间与 slack。

\begin{lstlisting}
pt_shell> report_timing
pt_shell> report_timing -input_pins -max_paths 4
\end{lstlisting}

\cmd{-max\_paths} $>$ 1 时默认仅报告负 slack 路径；要包含正 slack 路径用 \cmd{-slack\_lesser\_than}：
\begin{lstlisting}
pt_shell> report_timing -slack_lesser_than 100 -max_paths 40
\end{lstlisting}

多个 \cmd{-through} 表示按序经过各点：
\begin{lstlisting}
pt_shell> report_timing -from A1 -through B1 -through C1 -to D1
pt_shell> report_timing -from A1 -through {B1 B2} -through {C1 C2} -to D1
pt_shell> report_timing -from A1 -through {B1 C1} -to D1
\end{lstlisting}

\cmd{-start\_end\_type} 过滤拓扑：\texttt{reg\_to\_reg}、\texttt{reg\_to\_out}、\texttt{in\_to\_reg}、\texttt{in\_to\_out}（与 \cmd{report\_global\_timing} 四类一致）。此处 “reg” 含非端口端点（如时钟门控检查端点）。

\cmd{-transition\_time -capacitance} 显示转换时间与电容。

其他常用选项：\cmd{-delay\_type min|max}、\cmd{-path full|short|full\_clock|full\_clock\_expanded}、\cmd{-from}/\cmd{-to}/\cmd{-through}、\cmd{-group}、\cmd{-nworst}、\cmd{-max\_paths}、\cmd{-sort\_by group|slack}、\cmd{-nets}、\cmd{-crosstalk\_delta}、\cmd{-variation}、\cmd{-attributes \{...\}}。

\cmd{-attributes} 在时序点行打印指定属性（经 timing\_point 对象的链式属性访问）。合并 DMSA 报告支持 master 可用属性。\cmd{-nosplit} 防止行拆分。\cmd{timing\_report\_fixed\_width\_columns\_on\_left true} 将点名移到属性列右侧。限制：\cmd{-nets} 时不报告网线对象属性。

\subsubsection{报告归一化 slack}
\subsection*{Reporting Normalized Slack}

路径最大频率取决于传播延迟与所需时钟周期数。归一化 slack：
\[
\text{归一化 slack} = \frac{\text{路径 slack}}{\text{路径允许传播延迟}}
\]
表 53：路径 B slack 更差但归一化 slack 更小，对频率限制更大。用 \cmd{report\_timing -normalized\_slack} 排序。高级锁存器分析中见第~\ref{chap:adv}~章。

""")

S(r"""% ============================================================
\section{结果质量报告}
\subsection*{Quality of Results Report}

\cmd{report\_qor} 提供设计时序概览：最差路径长度（Critical Path Length，即端点到达时间）、TNS、最小延迟/hold、详细设计规则约束摘要。

TNS 两种模式（\cmd{timing\_report\_union\_tns}）：
\begin{itemize}
  \item \textbf{Union 模式（默认 true）：}各端点取所有路径组/场景中最差 slack 一次计入 TNS
  \item \textbf{Every-group 模式（false）：}每个路径组分别计入，同一端点在多组违例则多次计入
\end{itemize}

DMSA 中每种模式均取各场景最差 slack 计入。示例：两路径组两违例端点，union TNS = $-(6+8)=-14$，every-group = $-(6+5+4+8)=-23$。

\cmd{report\_qor} 支持 \cmd{-pba\_mode} 与 DMSA/SMVA 场景选项。

""")

S(r"""% ============================================================
\section{约束报告}
\subsection*{Constraint Reports}

\cmd{report\_constraint} 汇总约束违例：违例/满足量及最差违例对象。可报告最大面积及多种时序约束，验证网表是否满足引脚限制。

\subsubsection{时序约束类型}
\subsection*{Timing Constraints}

最大路径延迟/setup；最小路径延迟/hold；recovery（异步控制撤销到下一有效时钟边沿的最小间隔）；removal（时钟边沿在异步控制有效期间到控制撤销的最小间隔）；时钟门控 setup/hold；最小时钟脉宽高/低；最小时钟周期；单元两时钟引脚间最大 skew。

\subsubsection{设计规则约束}
\subsection*{Design Rule Constraints}

检查 ASIC 厂商库定义的设计规则；亦可用 \cmd{set\_max\_capacitance} 等指定。检查项：网线总电容（min/max）、引脚转换时间（min/max）、扇出负载属性之和（min/max）。通常关注最大电容与最大转换；可对上升/下降、不同时钟域分别设置。

\subsubsection{生成默认约束报告}
\subsection*{Generating a Default Constraint Report}

\cmd{report\_constraint} 显示各约束在当前设计的最差评估与加权 Cost。示例输出含 \texttt{max\_delay/setup}、\texttt{min\_delay/hold} 分组 Cost 与总 Constraint Cost。

\subsubsection{报告违例}
\subsection*{Reporting Violations}

\cmd{report\_constraint -all\_violators} 列出所有违例实例。\cmd{-verbose} 显示详细路径报告（含完整点列）。

\subsubsection{最大 skew 检查}
\subsection*{Maximum Skew Checks}

多时钟顺序器件可能需要 skew 检查。Liberty 关键字：\texttt{skew\_rising}、\texttt{skew\_falling}；\texttt{timing\_type} 设为其中之一，\texttt{related\_pin} 指定参考时钟引脚。

\figplaceholder{Figure 296: Timing diagram for skew constraint}{Skew 约束时序图}{fig:rpt-skew}

\cmd{report\_constraint -max\_skew [-all\_violators] [-verbose]} 报告最大 skew。实际 skew = 参考与约束时钟边沿延迟差的绝对值；参考引脚用最小 latency、约束引脚用最大 latency；skew 检查不考虑 uncertainty。

\subsubsection{No-change 时序检查}
\subsection*{No-Change Timing Checks}

库中 no-change 检查确保信号在时钟有效间隔内不翻转。等价于对有效边沿做 setup、对无效边沿做 hold。高有效时钟：上升沿 setup、下降沿 hold。\cmd{report\_timing} 与 \cmd{report\_constraint} 报告为 library no-change setup/hold time。

\subsubsection{其他 \cmd{report\_constraint} 选项}
\subsection*{Other report\_constraint Options}

\cmd{-all\_violators}、\cmd{-verbose}、\cmd{-max\_delay}、\cmd{-min\_delay}、\cmd{-recovery}、\cmd{-removal}、\cmd{-max\_skew}、\cmd{-clock\_gating\_setup/hold}、\cmd{-min\_pulse\_width}、\cmd{-min\_period}、\cmd{-significant\_digits}、\cmd{-pba\_mode}。

""")

S(r"""% ============================================================
\section{瓶颈报告}
\subsection*{Bottleneck Report}

\textbf{瓶颈}是对多条违例有贡献的公共点。瓶颈分析识别最差瓶颈、评估改善可能性，并指导网表修改（综合、尺寸调整等）。PrimeTime 将瓶颈与叶单元关联。

报告方式：
\begin{itemize}
  \item GUI：Reports $>$ Histograms $>$ Timing Bottlenecks
  \item Shell：\cmd{report\_bottleneck}（使用前将 \cmd{timing\_save\_pin\_arrival\_and\_slack} 设为 \texttt{true}）
  \item Tcl：\texttt{install\_dir/auxx/pt/examples/tcl/bottleneck\_utils.tcl} 中的过程
\end{itemize}

用 \cmd{report\_timing} 或 \cmd{get\_timing\_paths} 验证瓶颈分析结果。

\cmd{report\_bottleneck} 默认基于 slack $<$ 0 的路径数报告最差瓶颈单元（Bottleneck Cost = 经该单元的违例路径数）。Example 87 显示前 20 个单元。

Example 88 Tcl 过程 \texttt{verify\_bottleneck\_cell} 可验证单元瓶颈代价是否与报告一致。

""")

S(r"""% ============================================================
\section{全局 slack 报告}
\subsection*{Global Slack Report}

\cmd{report\_global\_slack} 显示指定引脚或端口的 slack。默认报告所有引脚（层次单元引脚与设计端口除外）。

\begin{noteBox}
首次时序更新前将 \cmd{timing\_save\_pin\_arrival\_and\_slack} 设为 \texttt{true}；否则 \cmd{report\_global\_slack} 会将其设为 \texttt{true} 并触发另一次时序更新。
\end{noteBox}

\cmd{-max}/\cmd{-min} 与 \cmd{-rise}/\cmd{-fall} 互斥；\cmd{object\_list} 指定引脚/端口，省略则默认所有引脚。

获取 setup 违例端点列表：
\begin{lstlisting}
pt_shell> get_attribute [current_design] violating_endpoints_max
\end{lstlisting}

hold 违例：
\begin{lstlisting}
pt_shell> get_attribute [current_design] violating_endpoints_min
\end{lstlisting}

端点按 slack 递增顺序列出。

""")

S(r"""% ============================================================
\section{分析覆盖率报告}
\subsection*{Analysis Coverage Report}

\cmd{report\_analysis\_coverage} 报告当前设计/实例的时序检查覆盖情况，对新设计尤为关键。

推荐流程：
\begin{enumerate}
  \item \cmd{link\_design} 并解决链接错误
  \item \cmd{check\_timing} 并解决检查时序错误
  \item \cmd{report\_analysis\_coverage} 并解决未测试（untested）问题
  \item 执行其余分析
\end{enumerate}

汇总检查类型：setup、hold、no-change、min period、recovery、removal、min pulse width、clock separation、clock-gating setup/hold、output setup/hold、max skew。默认按类型汇总 met/violated/untested 数量与百分比；某类型无检查则不显示。

静态时序理论上检查所有路径，但若断言不完整或路径被禁用（false path、禁用弧、case analysis 等），部分检查为 untested。与 \cmd{check\_timing} 配合验证设计与断言。多 case analysis 配置下可查看各配置 untested 检查。

\cmd{-status\_details} 显示各检查详情；untested 项含原因（若可确定）。\cmd{-exclude\_untested} 可排序原因列表。\cmd{-check\_type}、\cmd{-sort\_by slack} 等过滤。

示例摘要：
\begin{verbatim}
Type of Check   Total        Met     Violated    Untested
setup               5    0 ( 0%)   3 (60%)     2 (40%)
hold                5    3 (60%)   0 ( 0%)     2 (40%)
\end{verbatim}

\cmd{-status\_details \{untested\} -check\_type \{setup\}} 列出 untested setup 检查及原因（如 \texttt{no\_clock}）。

""")

S(r"""% ============================================================
\section{时钟网络时序报告}
\subsection*{Clock Network Timing Report}

高性能设计中时钟网络时序特性至关重要。\cmd{report\_clock\_timing} 报告顺序器件指定时钟引脚上的 latency、转换时间与 skew。

指定报告类型（latency、transition、skew、interclock\_skew、summary）、分析范围及过滤/排序选项。PrimeTime 收集信息并按指定顺序报告。

\subsubsection{Latency 与转换时间报告}
\subsection*{Latency and Transition Time Reporting}

基于 PrimeTime 计算的时钟 latency 与转换时间，针对所有顺序器件（触发器、锁存器）时钟引脚维护。某引脚 latency 取决于：约束类型（setup/hold）、路径角色（launch/capture）、转换类型（rise/fall）。

示例：
\begin{lstlisting}
pt_shell> report_clock_timing -type latency -to U1/CP \
          -hold -capture -rise
\end{lstlisting}

\cmd{-to} 限制范围；非顺序器件时钟引脚时，默认替换为该引脚传递扇出中的时钟引脚集合。\cmd{-probe} 则直接报告指定引脚 latency，不追溯扇出。

\subsubsection{Skew 报告}
\subsection*{Skew Reporting}

\cmd{-type skew}：同一时钟下引脚对 skew。\cmd{-type interclock\_skew}：含不同时钟间 skew。

两顺序器件时钟引脚 skew = 两引脚 latency 之差（图 297）。考虑器件类型、setup/hold、launch/capture 角色。启用 CRPR 时计入 skew。可用 \cmd{-from}/\cmd{-to} 限制；仅 \cmd{-from} 或仅 \cmd{-to} 时对未指定侧使用与指定侧通信的所有时钟引脚。\cmd{-clock} 限制时钟；\cmd{-include\_uncertainty\_in\_skew} 将 uncertainty 计入。

仅当两器件在指定方向存在数据路径通信时才报告 skew（不检查路径是否 false）。对电平敏感锁存器，skew 基于 “to” 器件 opening 边沿计算（即使允许时间借用）。

\subsubsection{跨时钟 skew 报告}
\subsection*{Interclock Skew Reporting}

\cmd{-type interclock\_skew} 报告不同时钟间 skew，如 CLK1 与 CLK2 域间最差局部 skew、与某引脚通信的十个最差 skew 等。\cmd{-from\_clock}/\cmd{-to\_clock} 限制范围；\cmd{-show\_clocks} 显示发射/捕获时钟名。分析引脚可能很多，应尽量缩小范围。

\subsubsection{时钟时序报告选项}
\subsection*{Clock Timing Reporting Options}

报告类型层次（图 298）：Summary（每时钟 min/max latency、转换、skew）$\rightarrow$ List（skew/interclock\_skew/transition 引脚对或单引脚列表，\cmd{-nworst}）$\rightarrow$ Verbose（\cmd{-verbose} 完整时钟路径）。

摘要报告右列条件代码（图 299）：\texttt{-} 发射转换、\texttt{+} 捕获转换、\texttt{i} 相对源反相、\texttt{p} 传播网络、\texttt{r/f} 锁存器时钟引脚上升/下降。

\cmd{-from}/\cmd{-to} 可限制摘要报告范围。

""")

S(r"""% ============================================================
\section{时钟门控与 recovery/removal 检查}
\subsection*{Clock-Gating and Recovery/Removal Checks}

\cmd{report\_clock\_gating\_check} 报告时钟门控 setup/hold 违例。\cmd{report\_timing -exception\_groups clock\_gating\_default} 可报告相关路径。

Recovery/removal 检查由库或约束定义；\cmd{report\_constraint -recovery -removal -all\_violators} 汇总违例。\cmd{report\_timing} 在异步 preset/clear 路径上显示 recovery/removal 为库检查时间。

异步复位路径调试：确认 \cmd{set\_false\_path} 未错误覆盖 recovery/removal；检查 \cmd{set\_case\_analysis} 对复位网络的影响。

""")

S(r"""% ============================================================
\section{时序更新效率}
\subsection*{Timing Update Efficiency}

大规模设计中 \cmd{update\_timing} 运行时间显著。\cmd{report\_timing} 前通常需完整或增量更新。

\textbf{消息限制：}\cmd{read\_parasitics}、\cmd{report\_annotated\_parasitics -check}、\cmd{read\_sdf} 及隐式/显式 \cmd{update\_timing} 发出的部分消息每次调用有默认上限；超限后日志注明不再输出，会话结束打印抑制摘要。\cmd{sh\_message\_limit} 控制默认限制；\cmd{sh\_limited\_messages} 控制受影响消息集，可减小大违例数量时的日志体积。

\textbf{增量更新：}PrimeTime 在约束、寄生、延迟标注等局部变化后执行增量时序更新；避免不必要的全量 \cmd{update\_timing}。

\textbf{保存 pin arrival/slack：}\cmd{timing\_save\_pin\_arrival\_and\_slack} 在更新时保存引脚到达时间与 slack，供 \cmd{report\_global\_slack}、\cmd{report\_bottleneck} 等使用，但增加内存与更新开销。

""")

S(r"""% ============================================================
\section{基于路径的时序分析}
\subsection*{Path-Based Timing Analysis}

静态时序工具设计为悲观以确保检出所有违例。例如 PrimeTime 对路径同时考虑最差到达时间与最差 slew，即使二者来自不同侧弧。

\textbf{基于路径的时序分析（PBA）} 通过隔离分析关键路径降低悲观性：沿感兴趣路径传播边沿，忽略侧弧 slew，重新计算路径专用 slack，并重新计算 CRPR、串扰 delta 等。适用于违例较少、需判断违例是否由到达/slew 悲观引起的情形。

重要性质：重算后路径 slack \textbf{排序可能改变}；单条最差路径重算不能代表端点最差重算 slack，可能需要对同一端点多条路径重算。

支持 \cmd{-pba\_mode} 的命令：\cmd{get\_timing\_paths}、\cmd{report\_constraint}、\cmd{report\_global\_timing}、\cmd{report\_qor}、\cmd{report\_timing}。

\subsubsection{PBA 模式}
\subsection*{Path-Based Analysis Modes}

\cmd{-pba\_mode} 取值：
\begin{itemize}
  \item \texttt{path} — 不搜索确认是否为真正最差重算路径；快速估计改善幅度；结果与 exhaustive 相同或略乐观
  \item \texttt{exhaustive} — 穷尽重算路径搜索，确保返回满足选项的最差重算路径
  \item \texttt{ml\_exhaustive} — 机器学习加速的穷尽 PBA；signoff 安全；早期更激进预测、后期更保守（见下文）
\end{itemize}

推荐用法：\cmd{exhaustive} 配合 \cmd{-slack\_lesser\_than} 限定搜索；仅在 \cmd{path} 模式显示 slack 接近阈值时使用 exhaustive；报告尽量具体（路径组、起终点）；\cmd{timing\_report\_use\_worst\_parallel\_cell\_arc true} 启用最差并行弧报告。

\begin{lstlisting}
pt_shell> report_timing -pba_mode exhaustive -slack_lesser_than 0
\end{lstlisting}

\cmd{-pba\_mode path} 时 \cmd{-slack\_lesser\_than} 应用于原始 slack 筛选；报告的重算 slack 可能改善。\cmd{-max\_paths}/\cmd{-nworst} 与 \cmd{exhaustive} 联用时，限制为搜索完成后的路径数，搜索过程中可能分析更多路径。

\begin{lstlisting}
pt_shell> report_timing -pba_mode exhaustive -nworst 1 \
          -slack_lesser_than 0 -max_paths 1000
\end{lstlisting}

\cmd{report\_timing -pba\_mode exhaustive} 不支持 \cmd{-start\_end\_pair} 与 \cmd{-slack\_greater\_than}。

\cmd{get\_timing\_paths -pba\_mode path \$coll} 对路径集合重算；\cmd{report\_timing \$recalc\_paths} 报告重算值。重算值仅 \cmd{report\_timing}/\cmd{get\_attribute} 可见，非 \cmd{report\_constraint}（可用 \cmd{report\_attribute} 读路径集合内属性）。\texttt{is\_recalculated} 属性标识重算；报告头显示 \texttt{Path Type: max (recalculated)}。

\cmd{pba\_recalculate\_full\_path}（默认 \texttt{false}）：\texttt{false} 时不重算时钟路径与借用路径，仅数据段；\texttt{true} 时始终重算。注意 \cmd{-path full\_clock\_expanded} 仅控制报告是否展开时钟路径，不控制是否重算。启用全路径重算时，透明锁存器借用仅当指定 \cmd{-trace\_latch\_borrow} 时才重算。

\cmd{timing\_report\_recalculation\_status} 便于调试 exhaustive 搜索运行时间。\cmd{pba\_exhaustive\_endpoint\_path\_limit} 限制 exhaustive 搜索考虑的端点数。

\subsubsection{机器学习穷尽 PBA}
\subsection*{Exhaustive Path-Based Analysis With Machine Learning}

ML-PBA（\cmd{-pba\_mode ml\_exhaustive}）用机器学习在准确性与运行时间间折中；比 regular exhaustive 快且 signoff 安全；可在全流程代替 path/exhaustive 切换。\cmd{pba\_exhaustive\_endpoint\_path\_limit} 须为 infinity（默认）。

行为摘要：
\begin{itemize}
  \item regular exhaustive 无违例 $\Rightarrow$ ML-PBA 无违例
  \item regular 单违例 $\Rightarrow$ ML-PBA 单违例（可能非同一路径）
  \item regular 多端点违例 $\Rightarrow$ ML-PBA 报告其中部分端点违例（可能非最差路径）
\end{itemize}

ML-PBA 结果恒为 regular exhaustive 结果子集（在搜索范围内）。ML-PBA 无违例则设计无重算违例路径。

\subsubsection{设置重算限制}
\subsection*{Setting Recalculation Limits}

\cmd{-pba\_mode path} 每次重算命令上限 2{,}000{,}000 条路径。\cmd{exhaustive} 每端点路径数由 \cmd{pba\_exhaustive\_endpoint\_path\_limit} 限制。

达限时 \cmd{pba\_path\_recalculation\_limit\_compatibility}（默认 \texttt{true}）控制行为：\texttt{true} 停止获取/重算；\texttt{false} 超限后用基于图的原始时序填充，报告头仍标 recalculated 标志。

\subsubsection{Exhaustive PBA 设置}
\subsection*{Exhaustive Path-Based Analysis Settings}

\cmd{pba\_exhaustive\_endpoint\_path\_limit} 默认 \texttt{infinity}：将端点 fanin 锥划分子图迭代分析，保证覆盖所有路径并返回最差 PBA slack。设为整数（如 25000）则逐路径孤立分析，达限发出 UITE-480 警告并停止；当图基与 PBA slack 已接近时整数模式可能更快。

\subsubsection{HyperTrace 加速 PBA}
\subsection*{HyperTrace Accelerated Path-Based Analysis}

HyperTrace 通过计算精炼的基于图的时序数据加速 exhaustive PBA 搜索。需在首次 exhaustive PBA 前对关键区域（slack 违例引脚集）做图精炼（选择性信号合并）。精炼开销与后续 PBA 加速需权衡：当 exhaustive PBA 占全流程 $>$20\% 且违例引脚 $<$10\% 时推荐；接近 signoff、PBA 占 $>$50\% 运行时收益最大。需 PrimeTime-ADV-PLUS 许可证。

配置变量包括 \cmd{timing\_enable\_hypertrace} 等；不支持部分流（见原书 “Unsupported Flows”）。精炼图仅用于 exhaustive PBA，非 PBA 报告仍用原时序图。

关键区域阈值应设为 exhaustive 搜索使用的最大 \cmd{-slack\_lesser\_than}（显式或默认），确保搜索完全在关键区域内加速。

\begin{seeAlsoBox}
高级分析（并行弧、时间借用）见第~\ref{chap:adv}~章；约束一致性调试见第~\ref{chap:cc}~章；GUI 报告见第~\ref{chap:gui}~章。
\end{seeAlsoBox}

""")

OUT.write_text("".join(C), encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size:,} bytes, UTF-8)")
