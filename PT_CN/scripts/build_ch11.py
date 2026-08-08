# -*- coding: utf-8 -*-
"""Build 11_back_annotation.tex via Path.write_text."""
from pathlib import Path
import re

text = r"""% 第 11 章 Back-Annotation
\bichapter{反标}{Back-Annotation}
\label{chap:backann}

反标是将外部文件中的延时或寄生电阻、电容值读入工具用于时序分析的过程。通过反标可在物理设计各阶段后准确分析电路时序。关于反标，见：
\begin{itemize}
  \item SDF 反标
  \item 反标延时、时序检查与转换时间
  \item 写出 SDF 文件
  \item 设置集总寄生电阻与电容
  \item 详细寄生
  \item 读取寄生文件
  \item 不完整反标寄生
  \item 反标优先级
  \item 报告反标寄生
  \item 移除反标数据
  \item GPD 寄生浏览器
\end{itemize}

% ============================================================
\section{SDF 反标}
\subsection*{SDF Back-Annotation}

初始静态时序分析中，PrimeTime 基于连线负载模型估计 net 延时。实际延时取决于单元与 net 的物理布局布线。布局规划器或布线器可提供更详细准确的延时信息供 PrimeTime 使用，此过程称为延时反标。反标信息常来自 SDF 文件。

读取 SDF 反标延时的方式：
\begin{itemize}
  \item 从 SDF 文件读取延时与时序检查
  \item 不用 SDF 格式反标延时、时序检查与转换时间
\end{itemize}

PrimeTime 支持 SDF v1.0 至 2.1 及 v3.0 子集。一般支持除下列外的所有 SDF 构造：PATHPULSE、GLOBALPATHPULSE、NETDELAY、CORRELATION、PATHCONSTRAINT、SUM、DIFF、SKEWCONSTRAINT。另支持 v3.0 子集：RETAIN、RECREM、REMOVAL、CONDELSE。

若无 SDF 文件，可在分析脚本中用电容与电阻寄生反标命令指定延时。

\subsection{读取 SDF 文件}
\subsubsection*{Reading SDF Files}

\cmd{read\_sdf} 从 SDF 1.0/1.1/2.0/2.1/3.0 文件读取实例级 pin 到 pin 的叶单元与 net 时序信息并反标到当前设计。设计中实例名须与时序文件匹配（如 VHDL 命名约定）。

读取 SDF 后 PrimeTime 报告：读文件错误数、已反标延时与时序检查数、不支持的 SDF 构造及出现次数、SDF 中的 P/T/V 值、设计反标状态（\cmd{report\_annotated\_delay}、\cmd{report\_annotated\_check}）。

示例：
\begin{lstlisting}
pt_shell> read_sdf -load_delay cell adder.sdf
pt_shell> current_design MY_DESIGN
pt_shell> read_sdf -load_delay net -path u1 mult16_u1.sdf
pt_shell> read_sdf -cond_use max boo.sdf
pt_shell> read_sdf -analysis_type on_chip_variation boo.sdf
pt_shell> read_sdf -analysis_type on_chip_variation \
            -min_file boo_bc.sdf -max_file boo_wc.sdf
\end{lstlisting}

\subsubsection{从子设计时序文件反标}
\paragraph*{Annotating Timing From a Subdesign Timing File}

指定 \opt{-path} 时，\cmd{read\_sdf} 用子设计时序文件反标当前设计。指定子设计时，不能用子设计端口 net 延时反标当前设计。

\subsubsection{反标负载延时}
\paragraph*{Annotating Load Delay}

负载延时（extra source gate delay）是驱动 net 电容负载引起的单元延时部分。部分延时计算器将其算作 net 延时，部分算作单元延时。默认 \cmd{read\_sdf} 假定时序文件中负载延时包含在单元延时中；若在 net 延时中，使用 \opt{-load\_delay} 选项。

\subsubsection{从 SDF 反标条件延时}
\paragraph*{Annotating Conditional Delays From SDF}

SDF 中的延时与时序检查可为条件式，条件通常为被反标单元某些输入值的表达式。反标方式取决于 Synopsys 库是否指定条件延时：
\begin{itemize}
  \item 库含条件弧：反标 SDF 中所有条件延时；库中 \texttt{sdf\_cond} 字符串须与 SDF 完全匹配。
  \item 库无条件弧：反标 SDF 中所有条件延时的最大或最小值；用 \opt{-cond\_use max/min} 选择。
\end{itemize}

库含状态相关延时时，含条件弧的 Synopsys 库可实现更准确的 SDF 反标。PrimeTime 仅用 SDF 条件将延时反标到库中相应时序弧；可用 case 分析使能所需条件弧。

\figplaceholder{Figure 112: Example of state-dependent timing arcs}{状态相关时序弧示例}{fig:ba-state-arc}

XOR 门 A 到 Z 的 SDF 示例：
\begin{lstlisting}
(COND B (IOPATH A Z (0.21) (0.54) ) )
(COND ~B (IOPATH A Z (0.27) (0.34) ) )
\end{lstlisting}

库无条件时，A 到 Z 所有弧使用最坏情况延时（图 113）。库有条件时，可识别 SDF 条件对应弧（图 114）。

\figplaceholder{Figure 113: Annotated delays when the Synopsys library contains no conditions}{Synopsys 库无条件时的反标延时}{fig:ba-no-cond}
\figplaceholder{Figure 114: Annotated delays when the Synopsys Library contains conditions}{Synopsys 库有条件时的反标延时}{fig:ba-cond}

\begin{noteBox}
SDF 中 IOPATH 语句反标两 pin 间所有弧。即使 IOPATH 跟在 COND IOPATH 之后，COND IOPATH 优先于 IOPATH。
\end{noteBox}

选择 B=0 延时：\cmd{set\_case\_analysis 0 [get\_pins U1/B]}。常量也可经 tie-high/low 或从其他 pin 传播的 case 分析到达选择条件弧的 pin。

\subsubsection{反标时序检查}
\paragraph*{Annotating Timing Checks}

SDF 含表 19 构造时用于反标当前设计：

\begin{table}[htbp]
\centering
\caption{表 19：时序检查的 SDF 构造}
\begin{tabular}{@{}ll@{}}
\toprule
检查类型 & SDF 构造 \\
\midrule
Setup 与 Hold & SETUP, HOLD, SETUPHOLD \\
Recovery & RECOVERY \\
Removal & REMOVAL \\
最小脉宽 & WIDTH \\
最小周期 & PERIOD \\
最大 skew & SKEW \\
No change & NOCHANGE \\
\bottomrule
\end{tabular}
\end{table}

\subsubsection{报告延时反标状态}
\paragraph*{Reporting Delay Back-Annotation Status}

SDF 文件通常很大（$\geq$100 MB），建议验证所有 net 均已反标延时（及适用时的时序检查）。

\cmd{report\_annotated\_delay} 报告已反标与未反标延时弧数，分别统计单元延时与 net 延时。Net 分三类：主输入端口连接、主输出端口连接、非主端口内部 net（按 SDF 标准仅内部 net 在 SDF 中反标）。

\cmd{report\_annotated\_check} 报告已反标时序检查数量。

\subsubsection{SDF 流中更快的时序更新}
\paragraph*{Faster Timing Updates in SDF Flows}

\cmd{timing\_use\_zero\_slew\_for\_annotated\_arcs} 对 SDF 反标弧使用零 slew，在全设计或近全设计（如 $\geq$95\%）SDF 反标时减少运行时间。默认 \texttt{auto}：对已用 \cmd{read\_sdf} 或 \cmd{set\_annotated\_delay} 完全反标的弧跳过延时/slew 计算，负载 pin slew 置零。未反标弧仍用最佳可用输入 slew 估计；未反标块内传播最坏 slew。建议将 \cmd{timing\_prelayout\_scaling} 设为 \texttt{false}。

% ============================================================
\section{反标延时、时序检查与转换时间}
\subsection*{Annotating Delays, Timing Checks, and Transition Times}

可反标延时、时序检查与转换时间以进行有限调试修改。见：
\begin{itemize}
  \item 反标延时
  \item 反标时序检查
  \item 反标转换时间
\end{itemize}

\subsection{反标延时}
\subsubsection*{Annotating Delays}

\cmd{set\_annotated\_delay} 设置单元或 net 延时。单元延时指定同单元输入到输出；net 延时指定单元输出到另一单元输入。

示例：
\begin{lstlisting}
pt_shell> set_annotated_delay -cell -load_delay cell 20 \
            -from U1/U2/U3/A -to U1/U2/U3/Z
pt_shell> set_annotated_delay -net -rise 1.4 -load_delay \
            cell -from U1/Z -to U2/A
pt_shell> set_annotated_delay -net -rise 12.3 -load_delay \
            net -from U1/Z -to U2/A
pt_shell> set_annotated_delay -cell -fall -of_objects \
          [get_timing_arcs -from U8/EN -to U8/Z \
          -filter sense==enable_low] 21.2
\end{lstlisting}

列出反标延时用 \cmd{report\_annotated\_delay}；移除用 \cmd{remove\_annotated\_delay} 或 \cmd{reset\_design}。

\subsection{反标时序检查}
\subsubsection*{Annotating Timing Checks}

\cmd{set\_annotated\_check} 设置两 pin 间 setup、hold、recovery、removal 或 no-change 检查值。

示例：u1/ff12 的 CP 到 D setup 为 2.1：
\begin{lstlisting}
pt_shell> set_annotated_check -setup 2.1 -from u1/ff12/CP \
            -to u1/ff12/D
\end{lstlisting}

列出用 \cmd{report\_annotated\_check}；查看特定实例效果用 \cmd{report\_timing}；移除用 \cmd{remove\_annotated\_check} 或 \cmd{reset\_design}。

\subsection{反标转换时间}
\subsubsection*{Annotating Transition Times}

\cmd{set\_annotated\_transition} 在设计任意 pin 上设置转换时间（slew）：
\begin{lstlisting}
pt_shell> set_annotated_transition -rise 0.5 [get_pins U1/U2/U3/A]
pt_shell> set_annotated_transition -fall 0.7 [get_pins U1/U2/U3/A]
\end{lstlisting}

% ============================================================
\section{写出 SDF 文件}
\subsection*{Writing an SDF File}

可将反标延时信息写出用于门级仿真等。\cmd{write\_sdf} 写出 SDF 1.0/2.1/3.0 格式，默认 2.1：
\begin{lstlisting}
pt_shell> write_sdf -version 2.1 -input_port_nets mydesign.sdf
\end{lstlisting}

\begin{noteBox}
若用 \cmd{write\_sdf} 以外工具写 SDF，须确保在 SDF 版本允许处显式指定反标。
\end{noteBox}

主题包括：SDF 构造、SDF 延时三元组、SDF 条件与边沿标识符、缩减时钟 Mesh/Spine 网络的 SDF、写出 VITAL 兼容 SDF、写出映射 SDF、写出压缩 SDF、写出无 setup/hold 违例的 SDF。

\subsection{SDF 构造}
\subsubsection*{SDF Constructs}

PrimeTime 写出的 SDF 使用：DELAYFILE、SDFVERSION、DESIGN、DATE、VENDOR、PROGRAM、VERSION、DIVIDER、VOLTAGE、PROCESS、TEMPERATURE、TIMESCALE；CELL、CELLTYPE、INSTANCE；ABSOLUTE、COND、CONDELSE、COSETUP、DELAY、HOLD、INTERCONNECT、IOPATH、NOCHANGE、PERIOD、RECOVERY、RECREM、RETAIN、SETUP、SETUPHOLD、SKEW、TIMINGCHECK、WIDTH 等（CONDELSE、RETAIN、RECREM、REMOVAL 仅 v3.0）；上升/下降沿标识符。

\cmd{write\_sdf} 不使用：INCREMENT、CORRELATION、PATHPULSE、GLOBALPATHPULSE、PORT（除非使能 PORT 缩减特性）、DEVICE、SUM、DIFF、SKEWCONSTRAINT、PATHCONSTRAINT。

\subsection{SDF 延时三元组}
\subsubsection*{SDF Delay Triplets}

单一工作条件下三元组三值相同，如 \texttt{(1.0:1.0:1.0)}。最小/最大工作条件下仅含最小与最大两延时，如 \texttt{(1.0::2.0)}，典型值不使用。PrimeTime 写出 0$\to$1、1$\to$0、0$\to$Z、Z$\to$1、1$\to$Z、Z$\to$0 跳变。

\subsection{SDF 条件与边沿标识符}
\subsubsection*{SDF Conditions and Edge Identifiers}

若库用 \texttt{sdf\_cond} 指定边沿标识符，PrimeTime 利用边沿标识符与条件，用于时序检查与单元延时。

当组合逻辑弧正/负边延时不同且输入 net 上升/下降转换不同时，\cmd{write\_sdf} 为组合单元延时弧写 POSEDGE/NEGEDGE 标识符，同一时序弧可生成两条 IOPATH（常见于 MUX、XOR）。部分仿真器不支持组合/时序弧上的边沿标识符，期望仅一条弧；用 \opt{-no\_edge} 兼容：
\begin{lstlisting}
pt_shell> write_sdf -no_edge mydesign.sdf
\end{lstlisting}
仅生成一条弧，取正/负跳变最坏三元组，仿真延时可能更悲观。

\subsection{缩减时钟 Mesh/Spine 网络的 SDF}
\subsubsection*{Reducing SDF for Clock Mesh/Spine Networks}

大时钟 mesh/spine 网络因 net 数量极大可产生过大 SDF。可合并差异可忽略的 SDF 值，用 SDF 3.0 PORT 构造表示合并 net。四个控制变量：
\begin{itemize}
  \item \cmd{sdf\_enable\_port\_construct}（默认 \texttt{false}）：使能 PORT 构造
  \item \cmd{sdf\_enable\_port\_construct\_threshold}（默认 1 ps）：低于此绝对延时差用 PORT
  \item \cmd{sdf\_align\_multi\_drive\_cell\_arcs}（默认 \texttt{false}）：统一 mesh/spine 驱动器输出小差异
  \item \cmd{sdf\_align\_multi\_drive\_cell\_arcs\_threshold}（默认 1 ps）：多驱动弧对齐阈值
\end{itemize}

\figplaceholder{Figure 115: Parallel buffers driving parallel buffers}{并行缓冲器驱动并行缓冲器}{fig:ba-port}
\figplaceholder{Figure 116: Cell delays in a parallel driver network}{并行驱动器网络中的单元延时}{fig:ba-multidrive}

PORT 构造：在阈值内将多条 INTERCONNECT 合并为 PORT 语句（三态缓冲器驱动的并行 net 除外）。多驱动弧归一化：在阈值内用单一最坏弧值代表多驱动器，防止仿真错误；同时可调整 net 与单元延时使完整路径延时一致。生成仿真用 SDF 时可将 \cmd{sdf\_align\_multi\_drive\_cell\_arcs} 设为 \texttt{true}；勿将此类悲观 SDF 读回 PrimeTime 做时序分析。

\begin{seeAlsoBox}
快速多驱动延时分析、并行驱动器缩减（第~\ref{chap:delay}~章）。
\end{seeAlsoBox}

\subsection{写出 VITAL 兼容 SDF}
\subsubsection*{Writing VITAL Compliant SDF Files}

\begin{lstlisting}
pt_shell> write_sdf -no_edge_merging -exclude {"no_condelse"} file.sdf
\end{lstlisting}

仿真器不能处理负延时时，用 \opt{-no\_negative\_values} 配合 \texttt{timing\_checks}、\texttt{cell\_delays}、\texttt{net\_delays} 将对应负值置零。

\subsection{写出映射 SDF}
\subsubsection*{Writing a Mapped SDF File}

SDF 映射功能允许指定 SDF 输出格式。创建 SDF map 文件定义库单元在 SDF 中的语法与时序弧，用 \cmd{write\_sdf -map} 应用。

\textbf{在库中指定时序标签}：在 timing 组用 \texttt{timing\_label} 标记弧，供 IOPATH、SETUP、HOLD、SETUPHOLD、RECOVERY、REMOVAL、RECREM、NOCHANGE、WIDTH 等构造引用。

\textbf{指定 min\_pulse\_width 约束}：可用两种方式在库中标记最小脉宽弧（Style 1/2）。

\textbf{使用 SDF 映射}：\cmd{write\_sdf -map mapfile}。

\textbf{支持的映射函数}：包括 \texttt{pin}、\texttt{bus}、\texttt{min/max\_rise/fall\_delay}、\texttt{min/max\_rise/fall\_delay\_bus}、\texttt{min/max\_rise/fall\_retain\_delay}、\texttt{min\_period} 等（见表 20--21）。

\textbf{SDF 映射文件语法}：含 \texttt{\$SDF\_CELL}、\texttt{\$SDF\_MAP}、格式字符串与变量映射表达式（示例 12 完整 BNF）。

\textbf{SDF 映射假设}：假定 map 文件中格式字符串替换占位符后 SDF 语法/语义正确；用 \cmd{read\_sdf -syntax\_only} 验证生成文件。

\textbf{总线命名约定}：\texttt{bus(string)} 函数按 \texttt{\$SDF\_BUSBIT} 与 \opt{-context verilog/vhdl} 转换总线分隔符。

\textbf{标记总线弧}：对总线 pin 的 timing 组，用 \texttt{*\_delay\_bus} 函数引用各位弧，如 \texttt{max\_rise\_delay\_bus(tas, CK, A[5])}。

\textbf{SDF 映射限制}：不能用通配符；不能指定实例级映射格式；未提供格式的单元用 \cmd{write\_sdf} 默认格式。

\subsection{写出压缩 SDF}
\subsubsection*{Writing Compressed SDF Files}

\begin{lstlisting}
pt_shell> write_sdf -compress gzip 1.sdf.gz
\end{lstlisting}

\subsection{写出无 Setup 或 Hold 违例的 SDF}
\subsubsection*{Writing SDF Files Without Setup or Hold Violations}

设计中期仍有违例但需门级仿真时，用 \opt{-mask\_violations}（\texttt{setup}、\texttt{hold}、\texttt{both}）：
\begin{lstlisting}
pt_shell> write_sdf -significant_digits 5 -mask_violations both masked.sdf
\end{lstlisting}

通过调整驱动违例端点的最后一条时序弧延时掩盖违例：hold 加延时，setup 减延时。可能需要更高 \opt{-significant\_digits} 避免舍入导致轻微违例。

% ============================================================
\section{设置集总寄生电阻与电容}
\subsection*{Setting Lumped Parasitic Resistance and Capacitance}

可在 net 上反标电阻与电容（图 117）。即使已用 SDF 反标全部延时，仍可能需反标寄生以进行最大转换时间或最大电容等设计规则检查。

\figplaceholder{Figure 117: Lumped RC}{集总 RC}{fig:ba-lumped}

\cmd{set\_resistance} 或 \cmd{set\_load} 设置的集总 R/C 临时覆盖 net 的连线负载模型或详细寄生。\cmd{remove\_resistance}/\cmd{remove\_capacitance} 后 net 恢复先前寄生形式。可分别设置 R 与 C；例如读入详细寄生后仅用 \cmd{set\_load} 覆盖电容，PrimeTime 仍用详细寄生计算电阻。

\subsection{设置 Net 电容}
\subsubsection*{Setting Net Capacitance}

\cmd{set\_load} 在端口与 net 上设置电容。层次设计须先 \cmd{link\_design}。默认 net 总电容为所有 pin、端口与连线电容之和；指定值覆盖内部估计。对低层次 net 指定为 \texttt{BLOCK1/BLOCK2/NET\_NAME}。\opt{-wire\_load} 将值设为端口连线电容并计入总连线电容。查看：\cmd{report\_port}、\cmd{report\_net}。

\subsection{设置 Net 电阻}
\subsubsection*{Setting Net Resistance}

\cmd{set\_resistance} 设置 net 电阻，覆盖内部估计。可指定层次 net 名。查看用 \cmd{report\_net}；移除用 \cmd{remove\_resistance} 或 \cmd{reset\_design}。

% ============================================================
\section{详细寄生}
\subsection*{Detailed Parasitics}

可将详细寄生反标到 PrimeTime，以电阻电容形式标注布线网表各物理段（图 118）。比集总寄生更准确但更耗时；RC 网络复杂时 pin 到 pin 延时计算更慢。此 RC 网络用于计算各子节点有效电容（$C_{\mathrm{eff}}$）、slew 与延时。PrimeTime 可读 SPEF 格式详细 RC。

\figplaceholder{Figure 118: Detailed RC}{详细 RC}{fig:ba-detailed}
\figplaceholder{Figure 119: Meshed RC}{Mesh RC}{fig:ba-mesh}

对有关键时序延时的网表（如时钟树）使用此模型，在深亚微米设计中 net 延时相对单元延时更显著时结果更准确。详细 RC 网络支持 mesh。

% ============================================================
\section{读取寄生文件}
\subsection*{Reading Parasitic Files}

\cmd{read\_parasitics} 可读：
\begin{itemize}
  \item Galaxy Parasitic Database（GPD）
  \item SPEF
  \item DSPF
  \item RSPF（IEEE 1481-1999）
  \item Milkyway（PARA）
\end{itemize}

SPEF/RSPF 可为 gzip 压缩 ASCII。格式可自动识别。net 与实例 pin 名须与设计匹配。默认假定 SPEF 电容不含 pin 电容，使用 Synopsys 库 pin 电容，忽略 SPEF 中 pin 电容；须保证 SPEF 耦合电容对称。用 \opt{-syntax\_only} 与 \opt{-keep\_capacitive\_coupling} 检查非对称耦合。

SPEF 中降阶与详细 RC 网络在延时计算时动态用于有效电容。多数报告命令（如 \cmd{report\_timing}、\cmd{report\_net}）的电容为集总电容 $C_{\mathrm{total}}$（SPEF 中所有电容之和加 pin 电容）。

大文件读入耗时：放本地盘、足够内存、gzip 压缩 SPEF 可缩短总处理时间。

\subsection{读取多个寄生文件}
\subsubsection*{Reading Multiple Parasitic Files}

可增量读取多块与顶层寄生并拼接。推荐流：
\begin{lstlisting}
read_parasitics A.spef -path [all_instances -hierarchy BLKA]
read_parasitics B.spef
read_parasitics C.spef
read_parasitics D.spef
read_parasitics chip_file_name
report_annotated_parasitics -check
\end{lstlisting}

后续反标仅可出现在非终端节点；终端节点上的第二次反标无效（PARA-114）。

\figplaceholder{Figure 120: Second annotation is valid}{第二次反标有效}{fig:ba-para-valid}
\figplaceholder{Figure 121: Second annotation is invalid}{第二次反标无效}{fig:ba-para-invalid}

\subsection{对寄生数据应用位置变换}
\subsubsection*{Applying Location Transformations to Parasitic Data}

默认从 GPD/SPEF 获取宏位置与方向（若可用）。可用 \opt{-x\_offset}、\opt{-y\_offset}、\opt{-rotation}、\opt{-axis\_flip} 应用偏移、旋转与翻转（图 122）。

\figplaceholder{Figure 122: Transformations specified by axis\_flip options}{axis\_flip 选项指定的变换}{fig:ba-transform}

\subsection{读取带多物理 Pin 的寄生}
\subsubsection*{Reading Parasitics With Multiple Physical Pins}

（当库单元 pin 对应多个物理 pin 时，\cmd{read\_parasitics} 按物理 pin 映射反标；须保证 SPEF/GPD 与网表 pin 映射一致。）

\subsection{从多 Corner 寄生数据读取单 Corner}
\subsubsection*{Reading a Single Corner From Multicorner Parasitic Data}

GPD 等多 corner 数据可用 \cmd{set\_gpd\_config} 选择读取的寄生 corner。

\subsection{检查已反标 Net}
\subsubsection*{Checking the Annotated Nets}

\cmd{report\_annotated\_parasitics -check} 验证 RC 网络完整性。

\subsection{缩放寄生值}
\subsubsection*{Scaling Parasitic Values}

可用变量或命令缩放反标寄生（如温度/工艺 corner 差异）。

\subsection{为增量时序分析读取寄生}
\subsubsection*{Reading Parasitics for Incremental Timing Analysis}

支持 ECO 后增量读入部分寄生更新。

\subsection{寄生文件限制}
\subsubsection*{Limitations of Parasitic Files}

须注意 SPEF 版本、耦合电容对称性、与网表命名一致性等限制。

% ============================================================
\section{不完整反标寄生}
\subsection*{Incomplete Annotated Parasitics}

布局布线过程中寄生可能仅覆盖 net 部分段。\cmd{read\_parasitics} 的 \opt{-complete\_with} 选项可补全不完整 net：\texttt{zero} 将未标注段 RES/CAP 置零；\texttt{wlm} 用连线负载模型估计。连接负载的电阻为 0 $\Omega$（图 125）。

\figplaceholder{Figure 125: Multidrive segments}{多驱动段}{fig:ba-complete}

可用 \texttt{rc\_network} 属性比较补全前后不完整 net。补全后不可撤销；多次 \cmd{read\_parasitics} 时仅在最后一次使用 \opt{-complete\_with}。取消所有寄生读入用 \cmd{remove\_annotated\_parasitics}。

有错误的寄生不要用 \cmd{complete\_net\_parasitics}；可修 SPEF 后重读。\cmd{complete\_net\_parasitics} 仅当 net 相关部分已有详细寄生、希望用零或 WLM 补全其余较不重要部分时适用。

% ============================================================
\section{反标优先级}
\subsection*{Back-Annotation Order of Precedence}

不同类型反标信息冲突时，每条 net 按下列优先级（高到低）：
\begin{enumerate}
  \item SDF 或 \cmd{set\_annotated\_delay} 反标的延时
  \item \cmd{set\_resistance}、\cmd{set\_load} 反标的集总 R/C
  \item \cmd{read\_parasitics} 反标的详细寄生
  \item 逻辑库或 \cmd{set\_wire\_load\_model} 的连线负载模型
\end{enumerate}

% ============================================================
\section{报告反标寄生}
\subsection*{Reporting Annotated Parasitics}

寄生文件可很大。用 \cmd{report\_annotated\_parasitics} 验证所有单元驱动器已反标；\opt{-check} 验证 RC 网络完整性。示例报告列出 internal net drive、design input port 等类型的 Total/RC pi/RC network/Not Annotated 统计。

% ============================================================
\section{移除反标数据}
\subsection*{Removing Annotated Data}

\begin{table}[htbp]
\centering
\caption{表 22：移除反标的命令}
\begin{tabular}{@{}ll@{}}
\toprule
反标类型 & 命令 \\
\midrule
延时 & \cmd{remove\_annotated\_delay} \\
检查 & \cmd{remove\_annotated\_check} \\
转换时间 & \cmd{remove\_annotated\_transition} \\
寄生 & \cmd{remove\_annotated\_parasitics} \\
全部 & \cmd{reset\_design} \\
\bottomrule
\end{tabular}
\end{table}

保留寄生仅移除时序约束与反标：\cmd{reset\_design -keep\_parasitics}。

% ============================================================
\section{GPD 寄生浏览器}
\subsection*{GPD Parasitic Explorer}

Parasitic Explorer 选项允许查询 \cmd{read\_parasitics} 反标到设计上的 GPD 格式寄生电阻与电容，支持：
\begin{itemize}
  \item \cmd{get\_resistors}：从一或多个 net 创建寄生电阻集合
  \item \cmd{get\_ground\_capacitors}：地电容集合
  \item \cmd{get\_coupling\_capacitors}：耦合电容集合
  \item 查询电阻、电容、子节点名、层名、层号、物理位置等属性
\end{itemize}

另提供查询 GPD 目录及控制读入/反标的命令：\cmd{report\_gpd\_properties}、\cmd{set\_gpd\_config}、\cmd{report\_gpd\_config}、\cmd{reset\_gpd\_config}、\cmd{get\_gpd\_corners}、\cmd{get\_gpd\_layers}。

\subsection{使能 Parasitic Explorer 功能}
\subsubsection*{Enabling the Parasitic Explorer Feature}

\begin{lstlisting}
pt_shell> set_app_var parasitic_explorer_enable_analysis true
pt_shell> read_parasitics \
 -format gpd my_design_dir.gpd -keep_capacitive_coupling ...
\end{lstlisting}

默认 \texttt{false}。读 GPD 前设为 \texttt{true} 则读入所有寄生 corner 并可查询；读入后设为 \texttt{true} 仅可查询当前寄生 corner。

\subsection{寄生电阻与电容集合}
\subsubsection*{Parasitic Resistor and Capacitor Collections}

\cmd{get\_resistors}、\cmd{get\_ground\_capacitors}、\cmd{get\_coupling\_capacitors} 可指定 net、路径节点、寄生 corner、属性过滤等：
\begin{lstlisting}
get_resistors -of_objects [get_nets {net_rx*}] -parasitic_corners vhi85c
get_ground_capacitors -from_node U235/z -to_node n121:4
get_coupling_capacitors -of_objects n2 -filter "capacitance_max > 0.5e-3"
\end{lstlisting}

须用 \opt{-of\_objects} 或 \opt{-from\_node}/\opt{-to\_node} 指定范围。默认最多显示 100 个对象（\cmd{collection\_result\_display\_limit}）。\cmd{get\_attribute} 查询属性；\cmd{list\_attributes -application -class resistor} 列出可用属性。

\subsection{查询磁盘上的 GPD 数据}
\subsubsection*{Querying GPD Data Stored on Disk}

可查询尚未读入设计的 GPD 数据：\cmd{report\_gpd\_properties}、\cmd{set\_gpd\_config}、\cmd{report\_gpd\_config}、\cmd{reset\_gpd\_config}、\cmd{get\_gpd\_corners}、\cmd{get\_gpd\_layers}。

\cmd{report\_gpd\_properties -gpd MyDesignA.gpd} 报告设计名、工具版本、net/单元数量等；\opt{-layers}、\opt{-parasitic\_corners} 报告层与 corner 信息。

\cmd{set\_gpd\_config} 覆盖 GPD 读入参数（默认来自 StarXtract 生成的 GPD 配置文件），如耦合电容绝对/相对阈值：
\begin{lstlisting}
pt_shell> set_gpd_config -gpd my_design1.gpd \
 -absolute_coupling_threshold 3.0e-3 \
 -relative_coupling_threshold 0.03
\end{lstlisting}

\cmd{report\_gpd\_config -include\_starrc\_options} 可对比 StarRC 提取时设置的选项。\cmd{reset\_gpd\_config} 重置。

\cmd{get\_gpd\_corners}、\cmd{get\_gpd\_layers} 报告 corner 名与层名列表。

\subsection{无网表的 Parasitic Explorer}
\subsubsection*{Parasitic Explorer Without a Netlist}

支持无 Verilog 网表或逻辑库读取 GPD 寄生，从 GPD 数据库本身推导网络连接：
\begin{lstlisting}
set_app_var parasitic_explorer_enable_analysis true
read_parasitics -format gpd my_gpd
current_design TOP
\end{lstlisting}

\cmd{read\_parasitics} 准备读入；\cmd{current\_design TOP} 链接设计并实际读入 GPD 数据，之后可查询寄生。
"""

out = Path(__file__).resolve().parent.parent / "chapters" / "11_back_annotation.tex"
out.write_text(text, encoding="utf-8")
cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
print(f"11_back_annotation.tex: {len(text)} bytes, {len(text.splitlines())} lines, CJK={cjk}")
