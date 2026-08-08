# -*- coding: utf-8 -*-
"""Part 1 of gen_ch09 - header and sections through OCV modes."""
CHUNK1 = r"""% 第 9 章 Operating Conditions
\bichapter{工作条件}{Operating Conditions}
\label{chap:opcond}

半导体器件参数随工艺、电压与温度（PVT）条件变化。ASIC 厂商通常在多种条件下表征器件参数，并在逻辑库中以不同工作条件集给出参数值。时序分析所用工作条件会影响分析结果。关于为时序分析指定工作条件，见：
\begin{itemize}
  \item 工作条件（Operating Conditions）
  \item 工作条件分析模式（Operating Condition Analysis Modes）
  \item 最小与最大延时计算（Minimum and Maximum Delay Calculations）
  \item 指定分析模式（Specifying the Analysis Mode）
  \item 用两个库进行分析（Using Two Libraries for Analysis）
  \item 延时降额（Derating Timing Delays）
  \item 时钟再汇聚悲观移除（Clock Reconvergence Pessimism Removal）
  \item 时钟片上变异悲观缩减（Clock On-Chip Variation Pessimism Reduction）
\end{itemize}

% ============================================================
\section{工作条件}
\subsection*{Operating Conditions}

集成电路在不同工作条件下呈现不同性能特征：制造工艺变化、电源电压与温度。逻辑库定义这些参数的标称值，并在该条件下给出延时信息。

一组工作条件包含下列值：

\begin{table}[htbp]
\centering
\caption{工作条件参数}
\begin{tabular}{@{}p{3.2cm}p{9.5cm}@{}}
\toprule
工作条件 & 说明 \\
\midrule
工艺降额因子（Process derating factor） & 与制造工艺变化导致的器件参数缩放相关。工艺数小于标称值通常导致更小延时。 \\
环境温度（Ambient temperature） & 芯片温度影响器件延时，取决于环境温度、功耗、封装类型与冷却方式等。 \\
电源电压（Supply voltage） & 较高电源电压通常导致更小延时。 \\
互连模型类型（Interconnect model type） & 定义 PrimeTime 在布局前分析中估计 net 电容与电阻所用的 RC 树拓扑。 \\
\bottomrule
\end{tabular}
\end{table}

每条时序弧的延时信息在标称工艺、温度与电压下指定。若实际工作条件不同，PrimeTime 应用缩放因子以反映这些变化。许多库对工艺、温度与电压使用线性缩放。

若逻辑库包含缩放单元信息，可包含特定工作条件的精确延时表或系数。对非线性缩放库单元，此方法可非常准确。更多信息见 Library Compiler 与 Design Compiler 文档。

可用单组工作条件进行分析（setup 与 hold），或指定最小与最大条件。若未在设计上设置工作条件，PrimeTime 使用主库中的默认工作条件集（若存在），或主库的标称值。

\subsection{互连模型类型}
\subsubsection*{Interconnect Model Types}

PrimeTime 在计算布局前设计的 net 延时时使用互连模型信息（当无反标 net 延时与寄生信息时）。总电阻与电容相同但 RC 树拓扑不同的两条 net，pin 到 pin 延时可能不同。

本主题提供互连模型类型的背景信息。无法在 PrimeTime 中修改这些类型。更多信息见 Library Compiler 文档。

互连模型由每个逻辑库工作条件集中的 \texttt{tree\_type} 规范定义。\texttt{tree\_type} 指示连线电阻与电容拓扑类型：\texttt{best\_case\_tree}、\texttt{worst\_case\_tree} 或 \texttt{balanced\_tree}。例如：
\begin{lstlisting}
operating_conditions(BEST) {
      process     : 1.1;
      temperature : 11.0;
      voltage     : 4.6;
      tree_type   : "best_case_tree";
 }
operating_conditions(TYPICAL) {
      process     : 1.3;
      temperature : 31.0;
      voltage     : 4.6;
      tree_type   : "balanced_tree";
}
operating_conditions(WORST) {
     process      : 1.7;
     temperature : 55.0;
     voltage      : 4.2;
     tree_type    : "worst_case_tree";
}
\end{lstlisting}

若逻辑库未定义树类型，PrimeTime 使用 \texttt{balanced\_tree} 模型。下图示出树类型模型网络。

\figplaceholder{Figure 89: RC interconnect topologies for fanout of N}{扇出为 N 的 RC 互连拓扑}{fig:oc-tree}

\subsection{设置工作条件}
\subsubsection*{Setting Operating Conditions}

要为时序分析指定工艺、温度与电压条件，使用 \cmd{set\_operating\_conditions} 命令。

所指定工作条件必须在指定库或 link path 中的库内定义。要为库创建自定义工作条件，使用 \cmd{create\_operating\_conditions}。使用 \cmd{report\_lib} 获取逻辑库中可用工作条件列表后再使用 \cmd{set\_operating\_conditions}。

将 tech\_lib 库中的 WCCOM 设为单一工作条件：
\begin{lstlisting}
pt_shell> set_operating_conditions WCCOM -library tech_lib
\end{lstlisting}

将 WCCOM 设为最大条件、BCCOM 设为最小条件以进行片上变异分析：
\begin{lstlisting}
pt_shell> set_operating_conditions -analysis_type on_chip_variation \
            -min BCCOM -max WCCOM
\end{lstlisting}

未指定库时，PrimeTime 搜索 link path 中所有库。设置工作条件后，可报告或移除工作条件。

\subsection{创建工作条件}
\subsubsection*{Creating Operating Conditions}

逻辑库包含固定的工作条件集。要在库中创建新工作条件，使用 \cmd{create\_operating\_conditions}。这些自定义工作条件可用于当前会话中的设计分析，但不能写入库 \texttt{.db} 文件。

查看库中定义的工作条件用 \cmd{report\_lib}；在当前设计上设置工作条件用 \cmd{set\_operating\_conditions}。

在 tech\_lib 库中创建名为 WC\_CUSTOM 的新工作条件：
\begin{lstlisting}
pt_shell> create_operating_conditions -name WC_CUSTOM \
            -library tech_lib -process 1.2 \
            -temperature 30.0 -voltage 2.8 \
            -tree_type worst_case_tree
\end{lstlisting}

\subsection{工作条件信息命令}
\subsubsection*{Operating Condition Information}

下列命令用于报告、移除或重置工作条件信息：

\begin{table}[htbp]
\centering
\caption{工作条件相关命令}
\begin{tabular}{@{}ll@{}}
\toprule
命令 & 操作 \\
\midrule
\cmd{report\_design} & 列出设计的工作条件设置 \\
\cmd{remove\_operating\_conditions} & 从当前设计移除工作条件 \\
\cmd{reset\_design} & 将工作条件重置为默认并移除所有用户指定数据（如时钟、输入/输出延时） \\
\bottomrule
\end{tabular}
\end{table}

% ============================================================
\section{工作条件分析模式}
\subsection*{Operating Condition Analysis Modes}

半导体器件参数可随制造工艺、工作温度与电源电压等条件变化。PrimeTime 中 \cmd{set\_operating\_conditions} 指定分析工作条件，使 PrimeTime 使用逻辑库中相应的参数值集。

PrimeTime 提供下列设置时序分析工作条件的方法：
\begin{itemize}
  \item \textbf{单一工作条件模式}：基于一组工艺、温度与电压条件，对整个设计使用单组延时参数。
  \item \textbf{片上变异（OCV）模式}：执行保守分析，允许最小与最大延时同时应用于不同路径。Setup 检查对 launch 时钟路径与数据路径用最大延时，对 capture 时钟路径用最小延时。Hold 检查相反。
  \item \textbf{高级片上变异（AOCV）模式}：根据路径逻辑深度与物理距离等指标确定降额因子。
  \item \textbf{参数化片上变异（POCV）模式}：将延时、要求时间与 slack 计算为统计分布。
\end{itemize}

下表示出各工作条件分析模式下 setup 与 hold 检查所用的时钟到达时间、延时、工作条件与延时降额。

\begin{table}[htbp]
\centering
\caption{表 16：Setup 与 Hold 检查所用的时序参数（续表见下文）}
\small
\begin{tabular}{@{}p{1.8cm}p{1.2cm}p{3.2cm}p{3.2cm}p{3.2cm}@{}}
\toprule
分析模式 & 时序检查 & Launch 时钟路径 & 数据路径 & Capture 时钟路径 \\
\midrule
单一工作条件 & Setup & 晚时钟，时钟路径最大延时，单一工作条件（无降额） & 最大延时，单一工作条件（无降额） & 早时钟，时钟路径最小延时，单一工作条件（无降额） \\
单一工作条件 & Hold & 早时钟，时钟路径最小延时，单一工作条件（无降额） & 最小延时，单一工作条件（无降额） & 晚时钟，时钟路径最大延时，单一工作条件（无降额） \\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[htbp]
\centering
\caption{表 16（续）：OCV 模式}
\small
\begin{tabular}{@{}p{1.8cm}p{1.2cm}p{3.2cm}p{3.2cm}p{3.2cm}@{}}
\toprule
分析模式 & 时序检查 & Launch 时钟路径 & 数据路径 & Capture 时钟路径 \\
\midrule
OCV & Setup & 晚时钟，时钟路径最大延时，晚降额，最坏工作条件 & 最大延时，晚降额，最坏工作条件 & 早时钟，时钟路径最小延时，早降额，最好工作条件 \\
OCV & Hold & 早时钟，时钟路径最小延时，早降额，最好工作条件 & 最小延时，早降额，最好工作条件 & 晚时钟，时钟路径最大延时，晚降额，最坏工作条件 \\
\bottomrule
\end{tabular}
\end{table}
"""
