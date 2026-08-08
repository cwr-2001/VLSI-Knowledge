# -*- coding: utf-8 -*-
from pathlib import Path

PART4 = r'''
\section{APL 中的多作业管理}
\subsection*{Multi-Job Management in APL}

APL 在「9.x LSF」上使用 Job array 进行作业管理，数组内作业共享 job ID 与参数。

用法：
\begin{enumerate}
  \item 在 APL 配置中指定 LSF 提交模式：
\begin{lstlisting}
GRID_TYPE lsf
BATCH_QUEUING_COMMAND bsub
LSF_SUBMIT_MODE 3    // array submission
BATCH_QUEUING_OPTIONS -J shortjob
\end{lstlisting}
  \texttt{-J} 指定作业名；未指定时 APL 用 \texttt{aplchar} 作为 array 名。
  \item 须指定 \texttt{-j 1}；array 提交仅支持 bsub 模式。例：\texttt{\$APACHEROOT/bin/apldi2 -l list -j 1 apl.current.config}
  \item 从此版本起 APL 用自有机制监控作业，不再查询 LSF 守护进程。
\end{enumerate}

LSF 9.x 默认 array 大小为 1000；sample split 模式下须确保 array 大小大于 APL 作业数，否则提交失败。

\section{输出文件}
\subsection*{Output Files}

\subsection{整体流程文件}
\textbf{进程日志}（\texttt{adsRpt/Log/}）：\texttt{apl.current.log.<time>}、\texttt{apl.cap.log.<time>}、\texttt{apl.pwcap.log.<time>}。记录子程序消息、每单元成功/失败/待表征、条件、Spice 错误与统计摘要。

\textbf{错误/警告}（\texttt{adsRpt/Error/}、\texttt{Warn/}）：\texttt{apl.current.err|warn.<time>} 等。\texttt{adsRpt/} 顶层文件软链接到最新结果。

\textbf{状态日志：}\texttt{aplstat <apl\_config>} 屏幕输出并写 \texttt{aplstat.log}，汇总成功/失败/待处理单元及失败原因。

\subsection{结果文件}
\texttt{apldi -o <filename>} 可指定输出名。

\textbf{APL-DI：}\texttt{/<corner>.current}（开关波形）、\texttt{/<corner>.cdev}（decap/ESR/漏电流）、\texttt{/<corner>.pwcdev}（上电分段线性 decap）。

\textbf{APL-DD：}\texttt{/<cell>.spcurrent}（\texttt{*.spcurrent} 节点上限 10 亿）、\texttt{/<cell>.cdev}、\texttt{/<cell>.pwcdev}。

\subsection{单单元表征文件}
默认目录 \texttt{APLDI\_<time>/} 或 \texttt{APLDD\_<time>/}；\texttt{APL\_RESULT\_DIRECTORY} 可改。

DI：\texttt{corner*/CURRENT|CAP|PWCAP/<cell>.spiprof|cdev|pwcdev} 及对应 \texttt{.<time>.log}。

DD：\texttt{CURRENT|CAP|PWCAP/<cell>...} 结构相同。

\subsection{APL 结果检查与处理}
\texttt{aplchk} 检查 APL 结果数据范围、缺失信息、单元类型与转换（组合 0->1/1->0；时序须四种转换）一致性：
\begin{lstlisting}
aplchk <input_file/dir> ?-v? ?-l <list_file>? ?-w <output_file>?
    ?-c? ?-pwc <pwcdev_file>? ?-conf <APL_config>? ?-spice <apl config>?
\end{lstlisting}

失败单元列表在 \texttt{adsRpt/aplchk.log}。

\textbf{检查限值关键字（全局/按单元 \texttt{CELL\_CHECK\_LIMITS}）：}
\texttt{IMAX\_STDCELL\_WARN}（默认 100000\,uA）、\texttt{ITAIL\_STDCELL\_WARN}、\texttt{SLEWMAX\_STDCELL\_WARN}（默认 3e6\,ps）、\texttt{DELAYMAX\_STDCELL\_WARN}、\texttt{FIREMAX\_STDCELL\_WARN}、\texttt{CMAX\_STDCELL\_WARN}（默认 1000\,pF）、\texttt{RMAX\_STDCELL\_WARN}、\texttt{LEAKMAX\_STDCELL\_WARN/ERROR}、\texttt{PWC\_VDD\_MAX\_WARN}（默认 5\,V）；存储器对应 \texttt{*_MEMORY\_*} 系列（峰值电流默认 1e6\,uA 等）。

\textbf{电阻/电容/漏电流直方图：}\texttt{aplchk -c <cell>.cdev} 等为 c0/c1、r0/r1、leak0/leak1 分布。

\subsection{无 APL 数据或样本的单元报告}
无电流剖面：\texttt{adsRpt/apache.inst.libCurrent}；无 decap：\texttt{apache.refCell.noAplCap}；无电压相关 decap：\texttt{apache.refCell.noAplPwcap}。导入时 \texttt{apache.refcell.noAplSample} 列出有 APLDI 但无样本的单元。

\section{在 RedHawk 中导入与合并表征数据文件}
\subsection*{Importing and Merging Characterization Data Files in RedHawk}

\subsection{导入 APL 文件}
推荐 GSR \texttt{APL\_FILES}：
\begin{lstlisting}
APL_FILES {
    <APL_binary>    current
    <APL_binary>    cdev
    <Avm.conf>      avm
    <AVM_binary>    current_avm
    <AVM_binary>    cap_avm
    <APL binary>    pwcap
    ...
}
\end{lstlisting}

或 TCL \texttt{import apl <APL\_file>}；\texttt{import apl <current>} 与 \texttt{import apl -c <cdev>} 可累积合并。\texttt{APL\_FILES}  preferred（支持目录与多种类型）。若命令文件有 \texttt{import apl} 且 GSR 有 \texttt{APL\_FILES}，命令优先、\texttt{APL\_FILES} 被忽略。

导入错误控制：默认忽略模型/Vdd/温度差异；\texttt{gsr set ignore\_apl\_check 1} 忽略全部；修复数据重跑 APL；或 \texttt{import apl} 从 \texttt{APL\_FILES} 重导；或用 GUI \texttt{APL -> Import}。

\subsection{合并 APL 结果文件}
\texttt{aplmerge} 检查 corner（P,V,T）兼容性并合并 \texttt{<cell>.current}/\texttt{.cdev} 等：
\begin{lstlisting}
aplmerge [-c] [-pwc] [-rep] [-l <cell_list>] [-im] [-t] [-o <output>]
    [-avm] [-ilimit] [<file1> ...] [<directory>] [-fl <list_file>]
    [-multi_pvt_merge <file1> <file2>]
\end{lstlisting}

\texttt{-c} decap；\texttt{-pwc} 分段线性 decap；\texttt{-rep} 用 file2 替换 file1 同名单元；\texttt{-l} 单元列表（格式 \texttt{<path>/<cellname>}，不含文件名）；\texttt{-im} 忽略 model 检查；\texttt{-t} turbo；\texttt{-o} 默认 \texttt{cell.spcurrent.merge}；\texttt{-avm} 忽略 AVM 头差异；支持通配符 \texttt{aplmerge -o <cell>.current *.spiprof}。

%%%CH09_PART5%%%
'''

path = Path(r'd:\IC Design\VLSI\RH_CN\chapters\09_apl_char.tex')
text = path.read_text(encoding='utf-8')
path.write_text(text.replace('%%%CH09_PART4%%%', PART4), encoding='utf-8')
print('Part 4 written')
