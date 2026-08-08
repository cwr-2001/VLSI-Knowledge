# -*- coding: utf-8 -*-
from pathlib import Path

PART3 = r'''
\section{定制单元表征数据准备}
\subsection*{Custom Cell Characterization Data Preparation}

APL 可表征组合逻辑与时序等定制单元，须用户指定表征向量，步骤较多。除标准单元数据外，还需输入向量文件；每个待表征单元须有一个向量文件。配置文件中须含 \texttt{VECTOR\_DIR} 指定向量目录（全路径）。

\subsection{输入向量文件}
\subsubsection*{Input Vector Files}

APL-DI 模式由 \texttt{libreader} 创建向量；APL-DD 由 RedHawk 调用 \texttt{libreader}。定制单元须手工创建向量文件，文件名 \texttt{<cell\_name>.inv}。

向量文件指定：所用输入向量；决定单元延迟的时序 arc 相关 pin；固有 decap 与漏电流估计的输入偏置。

主要关键字：
\begin{itemize}
  \item \textbf{DC 偏置：}\texttt{param <bias> <value>} 与 \texttt{dc <pin> <bias>}，偏置名与配置中 Vdd/Vss pin 名一致。
  \item \textbf{主输入输出：}\texttt{active\_input <pins...>}、\texttt{active\_output <pin>}。
  \item \textbf{向量：}
\begin{lstlisting}
vector {
    vname <input1> <input2> ...
    tunit ps
    vih [ <Vdd_name> | <VIH_value> ]
    <time_step> <state_pin1><state_pin2>... ?<state_name>?
}
\end{lstlisting}
  \texttt{time\_step} 为 APL 单位时间步倍数（非实际 ns）；0 步必需用于初始化。向量状态值之间无空格。
\end{itemize}

五输入组合门多向量示例、时序单元 \texttt{tran01}/\texttt{tran10}/\texttt{tran00}/\texttt{tran11} 示例及图~\ref{fig:apl-comb}、图~\ref{fig:apl-seq} 见原书。图~\ref{fig:apl-seq-prof} 为时序单元信号剖面；\texttt{0->0} 为非触发时钟沿，\texttt{1->1} 为触发沿且输出不翻转。

\figplaceholder{Figure 9-2}{两输入组合门的信号剖面}
\figplaceholder{Figure 9-3}{时序单元的信号剖面}

\begin{noteBox}
所有输入向量文件 \texttt{<cell\_name-n>.inv} 须位于配置 \texttt{VECTOR\_DIR} 指定目录。
\end{noteBox}

\section{运行单元表征}
\subsection*{Running Cell Characterization}

\subsection{库（DI）APL 运行设置}
\begin{enumerate}
  \item 按「APL 配置文件说明」准备配置文件。
  \item 运行 APL-DI 获开关电流剖面、高/低态器件电容与电阻、全库漏电流。
\end{enumerate}

\subsection{设计相关（DD）APL 运行设置}
\begin{enumerate}
  \item 准备 RedHawk GSR（附录 C）。
  \item GUI \texttt{APL -> Setup} 或 TCL \texttt{setup apl -dir <dir\_name>}，生成 \texttt{apache.apl}、\texttt{adsLib.output}（在 \texttt{<dir>/.apache}），并在 \texttt{<dir>} 创建模板：\texttt{apl.custom.config}、\texttt{apl.io.config}、\texttt{apl.memory.config}、\texttt{apl.std.config} 及对应单元列表。
  \item 准备配置文件。
  \item 运行 APL-DD。
  \item 低功耗设计上电周期：额外运行 header/footer 与 decap（pwcap），见「低功耗设计表征」。
\end{enumerate}

\subsection{增强型设计无关表征}
GSR \texttt{APL\_DID 1} 可在 RedHawk 运行中自动为 APL-DI 覆盖不足的实例生成额外设计相关样本。APL-DI 阶段在 \texttt{APLDI\_[yyyymmdd]/corner[n]/CURRENT/PACKAGE} 打包 Spice 与配置。已生成 DI 库可用 \texttt{aplgenpkg -d APLDI\_[yyyymmdd] -c <apldi\_config>} 无需重跑 APL-DI。须以目录格式导入（非单一 \texttt{*.current}）：\texttt{import apl APLDI/APLDI\_20070310/corner1/CURRENT}。

\subsection{从 UNIX Shell 运行 APL 表征}
\begin{lstlisting}
% apldi [-c] [-w] [-sw] [ -l <cell_file> | -p <decap_file> ]
      ? -o <output_file>? ? -s [1|2]? ?-j [1|2]? ?-v? ?-fc ? <apl_config_file>
\end{lstlisting}

选项：\texttt{-c} decap；\texttt{-w} pwcap；\texttt{-sw} 开关 decap；\texttt{-l} 单元列表；\texttt{-o} 输出（勿用保留扩展名 \texttt{.spiprof/.spcurrent/.cdev/.pwcdev}）；\texttt{-p} 有意 decap 列表（不与 \texttt{-c} 同用）；\texttt{-s 1|2}（仅 DI：1=仅生成样本，2=不生成样本直接表征）；\texttt{-j 1|2} 多机（1=LSF bsub，2=LSF API；SunGrid 亦用 \texttt{-j}）；\texttt{-v} 详细；\texttt{-fc} 快速库检查。

默认设计无关；\texttt{APL\_RUN\_MODE} 可设为 DD。许可证等待：\texttt{setenv APACHEDA\_LICENSE\_WAIT <xxx:unit sec>}。

\subsection{多 Vdd/Vss Decap 单元}
有意 decap 不在 LIB 中，表征方式不同。\texttt{DECAP\_VDD\_PIN} 指定各 Vdd 电压；\texttt{CUSTOM\_LIBS\_FILE} 提供 pin 类型；多 Vdd/Vss decap 的 P/G arc 须在 \texttt{pgarc.lib} 手工定义 \texttt{pgarc \{ <vdd> <vss> ... \}}。

\subsection{APL 调用示例}
DD 示例：
\begin{lstlisting}
% apldi -s 2 -l cell_list2 apl.config          # 本地电流表征 -> ./cell.spcurrent
% apldi -j 2 -s 2 -l cell_list2 apl.config     # 农场并行
% apldi -l cell_list1 -c apldi.config          # decap -> ./<cell>.cdev
% apldi -p decap_cell_list6 apl.config         # 有意 decap 列表
\end{lstlisting}

Decap 列表语法：每行 \texttt{<cell\_name>}。

DI 示例：
\begin{lstlisting}
% apldi -j 2 apldi.config                      # 电流 -> corner*.current
% apldi -j 2 -c -l cell_list_dc apldi.config   # decap -> corner*.cdev
% apldi -j 2 -w cell_list_pw apldi.config      # 低功耗 -> corner*.pwcdev
\end{lstlisting}

\subsection{低功耗设计表征}
Header/footer 上电仿真需分段线性模型（固有电容、漏电流、ESR 随电压变化）。多 Vdd/Vss 低功耗 pwlcap 为 arc 型，用 \texttt{PRIMARY\_VDD\_PIN}/\texttt{PRIMARY\_GND\_PIN}。

\begin{lstlisting}
% apldi -w [ -l <cell_list> | -p <decap_list> ] [-o <output>] <apl_config>
\end{lstlisting}

Header 设计扫 Vdd 从近零到 Vdd；footer 设计扫 Vss 从近 Vdd 到零。\texttt{SWEEPSOURCE [<power\_pin>|<gnd\_pin>]}。默认 11 个电压点（0.1--1.1$\times V_{eff}$）可用 \texttt{SWEEPVALUE} 替换。结果用 GSR \texttt{PIECEWISE\_CAP\_FILE <PWL\_cap\_file>} 导入。

\textbf{aplsw 开关表征：}
\begin{lstlisting}
aplsw [-c] [-d] [-o <output_file>] <sw_config_list.conf>
\end{lstlisting}
详见第~\ref{chap:lowpower}~章低功耗开关建模。

%%%CH09_PART4%%%
'''

path = Path(r'd:\IC Design\VLSI\RH_CN\chapters\09_apl_char.tex')
text = path.read_text(encoding='utf-8')
path.write_text(text.replace('%%%CH09_PART3%%%', PART3), encoding='utf-8')
print('Part 3 written')
