# -*- coding: utf-8 -*-
from pathlib import Path

PART5 = r'''
\section{aplccs（CCS2APL）库表征}
\subsection*{aplccs (CCS2APL) Library Characterization}

\subsection{引言与语法}
\texttt{aplccs} 将 CCS 库数据转为 APL 开关电流格式。优势：对 RedHawk 透明；可在运行前生成 CCS2APL DI 库；APL 工具完全支持；转换极快；时序信息为硬值。

标准单元：支持对角稀疏 cload 表；同单元多 nom\_voltage 合并须 slew 归一化因子/温度/pg\_pins/states/samples 一致；C00/C11 _toggle aplccs 扩展样本（同 slew 波形相同）。

存储器/I/O/定制：C-load 无关状态用默认 1\,fF；支持多输出单元。

\begin{lstlisting}
aplccs [-o <output_file>] -mstate_cells <cell_list> -conf <aplccs_config> [-skip_ps]
\end{lstlisting}
默认输出 \texttt{ccs.current}；\texttt{-skip\_ps} 跳过生成 \texttt{.apache/apache.pslib}。

\subsection{APLCCS 配置文件}
\texttt{LIB\_FILES}/\texttt{LIBS\_DIRECTORY}/\texttt{LIBS\_FILE}；\texttt{RETRY\_VECTORLESS [0|1]}（默认向量失败时用随机向量）；\texttt{IGNORE\_CELLS \{ <cell> ... \}}。

\subsection{直接导入 CCS Lib}
GSR \texttt{LIB\_USE\_CCS 1} 可在 RedHawk 流程中透明转换；\texttt{CCS\_OVERRIDE\_APL 1} 在两者并存时 CCS 优先（须 \texttt{LIB\_USE\_CCS 1}）。\texttt{CONVERT\_CCS\_CAP [0|1]} 将 CCS intrinsic\_parasitic ESC/ESR/漏电流转 APL cdev（默认 0；用户须确认 CCS 与 APLCAP 中 ESC/ESR 含义一致）。

\section{I/O 单元表征}
\subsection*{I/O Cell Characterization}

I/O 可向内核注入显著噪声（尤其共享 VSS），应纳入动态分析。I/O 常有 core 与 I/O 多套 Vdd/Vss，须表征全部 pin 电流。须准备输入向量（见定制单元与下文流程）。

\subsection{I/O 单元表征流程}
\begin{enumerate}
  \item 定义 I/O Vdd pin 与电压（在 SPICE \texttt{.subckt} 行，非 .lib）：\texttt{dc <io\_vdd\_pin> <value>}
  \item 开路监测 pin：\texttt{openpin <open\_pins>}
  \item 电压源参数：\texttt{param vddo=1.5}、\texttt{dc VDDQ15 vddo} 等
  \item 输入激励：自动 \texttt{active\_input clk}（差分 I/O 勿用自动）；或 \texttt{VECTOR \{ VNAME ... TUNIT VIH SLOPE <time> <values> ... \}}
  \item 负载：\texttt{OUTPUT <out\_pin> <load\_subckt>}，子电路在 \texttt{.inpvec} 或 include 文件中定义板级/封装负载（示例 \texttt{pkg\_board\_load}、\texttt{board\_load}、\texttt{pkg\_load}）。
\end{enumerate}

\subsection{I/O 附加关键字（可选）}
\texttt{TSTEP}/\texttt{TSTOP} 瞬态步长与停止时间；\texttt{OP} decap dump 时间；\texttt{tranXX <time><unit>} 开关窗口起始（也可在 vector 行末，优先级更高）；\texttt{ioprobe <VDD> <+|-> <VSS> <-|+>} 探测极性（Spice 正电流流入电压源正 pin）。

\begin{noteBox}
I/O 单元仅考虑一个代表性样本。
\end{noteBox}

最精确 I/O 表征：\texttt{sim2iprof}（电流）+ ACE（电容）；更快但不那么精确：AVM 数据手册表征。

\section{存储器与 IP 表征}
\subsection*{Memory and IP Characterization}

存储器、定制 IP、I/O 的 APL 级数据有两种选择：
\begin{itemize}
  \item \textbf{精确：}\texttt{sim2iprof}（开关电流）+ ACE（ESR、电容、漏电流）
  \item \textbf{快速：}AVM 规则化数据手册表征（三角/梯形电流、ESR、电容、漏电流）
\end{itemize}

\subsection{Sim2iprof 开关电流表征}
见附录 E「sim2iprof」。

\subsection{ACE Decap 与 ESR 表征}
ACE 估计存储器与复杂 IP 的 P/G pin 固有与有意 decap，用追踪算法找 P/G 网络，调用 SPICE 表征代表 MOSFET 栅电容，生成 APL 格式电容、ESR、漏电流估计；可用 DSPF（\texttt{*|NET}、\texttt{*|I}）追踪 R 元件。可识别内嵌 header/footer 开关；大单元（约 50 万 MOSFET）Linux 上典型约 1 分钟。

\textbf{识别 tied-off 器件为 decap：}
\begin{itemize}
  \item NMOS：源/栅接地的漏接电源；或漏/栅接地、源接电源 $\Rightarrow$ decap
  \item PMOS：源/栅接电源的漏接地；或漏/栅接电源、源接地 $\Rightarrow$ decap
  \item 接信号而非电源/地：电流置零，不作 decap
\end{itemize}

\textbf{PWCap 特殊 pin：}从 Liberty 属性自动识别 retention 等 pin，用于 pwcap 条件（不影响电流/cap 表征）。

\textbf{ACE 配置文件必需：}\texttt{External\_power\_net}、\texttt{External\_ground\_net}、\texttt{Subckt}、\texttt{Modelfile}（或 \texttt{Include}）、\texttt{VddValue}。

主要可选关键字（名称不区分大小写）：\texttt{Ace\_HSpice}/\texttt{Ace\_Eldo}/\texttt{Ace\_Spectre}；\texttt{ACE\_OPTION}；\texttt{DECAP\_SUBCKT}（有意 decap 子电路及 port 类型 power/ground/na）；\texttt{Internal\_Power\_Net}/\texttt{Internal\_Ground\_Net} 与 \texttt{VP\_PAIRING}（开关）；\texttt{K\_GROUND\_CAP}/\texttt{K\_FLOAT\_CAP}（信号寄生电容分配，默认 0.5）；\texttt{Leakage\_i}（\texttt{-pwc} 必需）；\texttt{METAL\_RESISTOR}/\texttt{METAL\_RESISTOR\_FILE}；\texttt{MOS\_Report}；\texttt{NOMINAL\_VDD}；\texttt{NMOS/PMOS\_Model\_Name}；\texttt{Option}；\texttt{Preprocess\_Subckt\_File}；\texttt{Primary\_Power\_Net}/\texttt{Primary\_Ground\_Net}；\texttt{SIGCAP\_FACTOR}；\texttt{SIGNAL\_PARASITIC\_C}；\texttt{Simulator\_Command\_Option}；\texttt{SPICE\_SIMULATOR}；\texttt{SweepValue}（\texttt{-pwc}，默认 11 点 10\%--110\% Vdd）；\texttt{Switch\_Subckt}；\texttt{Temperature}；\texttt{TOGGLE\_RATE\_ASSIGNMENT}；\texttt{VP\_Mapping}（LEF-Spice pin 映射）；\texttt{VTH\_FACTOR}；\texttt{WRAPSUB}；\texttt{XMOS\_INST\_PARAM}；\texttt{XMOS\_PARAM\_MAPPING}；\texttt{FLIP\_WELL}（FDSOI）；\texttt{FINFET\_UNIT\_WIDTH}（16nm FinFET）等。

\textbf{运行 ACE：}
\begin{lstlisting}
ace [-d] [-o <output_file>] [-toggle_rate <On_fraction>] [-pwc] <cellname>.smin
\end{lstlisting}
\texttt{-toggle\_rate} 控制 MOSFET On 时间分数（影响 ESC）；\texttt{-pwc} 生成分段线性电容。

\textbf{输出：}\texttt{<cell>.mcap}（RedHawk 导入 CDEV）、\texttt{<cell>.ace.mmx}（MMX 详细数据）、\texttt{<cell>.ace.decap}（有意 decap 明细）。

\subsection{AVM 数据手册表征}
动态分析中若无存储器 APL 数据，RedHawk 可从设计/LIB/GSR 收集信息生成 \texttt{adsRpt/avm.conf}，内部用规则生成电流剖面、漏电流与 decap。GSR：
\begin{lstlisting}
LIB2AVM [ 0 | 1 | 2 | 3 | 4 ]
\end{lstlisting}
默认 1=双三角；2=梯形；3=负载相关三角；4=负载相关梯形；0=关闭。已有 APL 存储器数据覆盖 AVM。识别 \texttt{memory()} 或 \texttt{timing()\{mode...\}}；Cpd 优先级：active pin(VCD) $>$ 时钟 related pin $>$ 最高 Cpd 功耗表。

特性：可独立运行；仅动态流程；可指定 \texttt{Ipeak} 调整 base width；报告与指定 Ipeak/Cpd 的百分比差；尾部电流置 0；\texttt{CHARACTERIZATION\_MODE ACCURATE} 为精确模式；\texttt{MAX\_FREQ} 检查 base width $< 1/\mathrm{MAX\_FREQ}$；\texttt{LIB2AVM\_MSTATE 1} 多状态仅考虑 VCD 中状态。

\textbf{独立运行 LIB2AVM：}
\begin{lstlisting}
lib2avm <lib2avm_config_filename> -l <cell_list>
\end{lstlisting}

\textbf{AVM 配置语法（多标称 Vdd 示例结构）：}
\begin{lstlisting}
Cell1 {
    MEMORY_TYPE RegFile
    EQUIV_GATE_COUNT 6663
    Cload 2f
    VDD_PIN VDDPR VDDP
    GND_PIN VSS
    C_decap { VDDPR VSS 11.002f ... }
    VDD 1.08 1.08 { ck2q_delay 1537p; tr_q 30.194p; ... Cpd_read {...} }
    VDD 1.32 1.32 { ... }
}
\end{lstlisting}

关键字段：\texttt{CHARACTERIZATION\_MODE}（\texttt{accurate}=400 点，\texttt{ultra\_accurate}=1000 点，\texttt{PWL}/\texttt{PWL1}）；\texttt{PROCESS}（SS/TT/FF，必需）；\texttt{C\_decap}/\texttt{Cpd\_read|write|standby}；可选 \texttt{AVM\_VOLTAGES}、\texttt{WAVEFORM\_TYPE}、\texttt{leakage\_i}、\texttt{Peak\_I\_*}、\texttt{Peak\_T\_*}、\texttt{TMIN}、\texttt{Delay\_Derating}、\texttt{Gate\_cap}、\texttt{TEMPERATURE}、\texttt{Avg\_High/Low\_Power}、\texttt{Freq}、\texttt{Cknt\_Power\_Ratio}、\texttt{Seq\_Power\_Ratio}、\texttt{CHARGE\_RATIO}（默认 0.7）、\texttt{DATAVERSION [7v1|pre7v1]} 等。

\textbf{多状态模式：}仅存储器/IP；忽略 \texttt{Cpd\_write/read/standby} 等时用 \texttt{CUSTOM\_STATE\_FILE} 或 \texttt{STATE\_BOOLEAN} 与 \texttt{Cpd <state> \{...\}}；可选 \texttt{peak\_I}/\texttt{peak\_T}、\texttt{WAVEFORM\_TYPE\_PER\_STATE}。

\textbf{运行 AVM：}\texttt{avm <avm\_configuration\_file>}

\textbf{AVM 输出：}\texttt{vmemory.current}、\texttt{vmemory.cdev}；\texttt{avm.log}/\texttt{avm.warning}/\texttt{avm.error}；报告与指定 Ipeak/Cpd 的差异。

\section{APL 问题排查}
\subsection*{Troubleshooting APL Problems}

\subsection{检查配置文件}
\begin{itemize}
  \item 必需关键字是否正确？
  \item Vdd 与 GSR 一致？
  \item 温度与 \texttt{*.lib}/Tech 一致？
  \item Vdd/Gnd pin 名与 Spice 网表一致？
  \item Spice 中器件尺寸是否为 um？否则设 \texttt{SIZE\_SCALE}（如 \texttt{1e-6}）。
\end{itemize}

\subsection{常见问题}
\begin{itemize}
  \item \texttt{.apache/adsLib.out} 缺向量——LIB 缺失或 function/state table 缺失
  \item Spice 网表/模型缺失或参数/scale/不支持 card 错误
  \item 误表征 tie-off、天线二极管（电流表征）或 decap 未用 \texttt{-p}、复杂单元缺定制向量
  \item 向量未引起输出升降沿；磁盘不足（检查 \texttt{TMP\_DIR}）；监控与样本计数
\end{itemize}

\subsection{命令行 APL 错误调试}
单单元 \texttt{<cell>.list}；非 LSF 模式看 STDOUT；确认 \texttt{adsLib.output} 有向量；检查 SUBCKT；\texttt{DEBUG 1}、\texttt{-v}、\texttt{-d}；查 \texttt{.apache/APL/<cell>.sp} 与 SV 波形；小 deck 用 \texttt{nspice} 验证；分析失败共性（机器/队列/单元类型）；NSpice 孤立节点错误可加 \texttt{OPTION gshunt=1e-9}；样本缺失见 \texttt{adsRpt/apache.refCell.noAplSample}（Warning ITG-022）。

\section{APL 配置文件示例}
\subsection*{Sample APL Configuration File}

库 APL 配置示例（注释说明各条目）：
\begin{lstlisting}
# APL run mode
APL_RUN_MODE DI

LIB_FILES {
    /nfs/apl1/user_data/lib/IO.lib
    /nfs/apl1/user_data/lib/ANALOG.lib
}

DESIGN_CORNER {
    { TEMP 25  PROCESS TT  VDD 1.0  MODEL /nfs/apl1/model TT }
    { TEMP 125 PROCESS FF VDD 1.1  MODEL /nfs/apl1/model FF }
}

GRID_TYPE LSF
BATCH_QUEUING_COMMAND bsub
BATCH_QUEUING_OPTIONS -r -R select [type==any]
EXEC_PATH /appls/lsf/6.0/linux2.4-glibc2.3-x86/bin
LSF_SUBMIT_MODE 1
JOB_COUNT 20

SPICE_SUBCKT { /nfs/apl1/user_data/spice/subckt/spice.lib }
INCLUDE { /nfs/apl1/model/model.typ }

WORKING_DIR /nfs/apl1/apldi_test
SIZE_SCALE 1
VDD 1.5
VDD_NAME VDD
GND_NAME GND1
TMP_DIR /nfs/apl1/apldi_test/temp
\end{lstlisting}
'''

path = Path(r'd:\IC Design\VLSI\RH_CN\chapters\09_apl_char.tex')
text = path.read_text(encoding='utf-8')
path.write_text(text.replace('%%%CH09_PART5%%%', PART5), encoding='utf-8')
print('Part 5 written - chapter 9 complete')
