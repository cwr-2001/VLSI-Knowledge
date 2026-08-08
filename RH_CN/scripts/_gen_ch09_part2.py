# -*- coding: utf-8 -*-
"""Append part 2+ of chapter 9 translation to 09_apl_char.tex"""
from pathlib import Path

PART2 = r'''
\section{单元表征数据准备}
\subsection*{Cell Characterization Data Preparation}

\subsection{数据要求}
\subsubsection*{Data Requirements}

标准单元 APL 表征所需数据见本节。表征用向量由 APL 自动生成。运行 APL 前需要：
\begin{itemize}
  \item \texttt{*.lib} 文件——单元库数据（功能、pin 定义、状态表）。库 APL 表征必需。
  \item P/G arc 定义——多 Vdd/Vss pin 单元须定义 P/G arc 以进行基于 arc 的 decap 表征。APL-DI 若 .lib 含 \texttt{related\_power/ground\_pin} 可自动解释；否则须在定制 .lib 中定义：
\begin{lstlisting}
pin(D) {
    direction : input;
    related_power_pin : VDD;
    related_ground_pin : VSS;
}
\end{lstlisting}
  APLDI 读取 \texttt{related\_power\_pin} 与 \texttt{related\_ground\_pin} 得到 VDD 到 VSS 的 P/G arc。定制 lib 与 .lib 间 P/G arc 重叠时优先级：a) 定制 lib 单元级；b) LIB 单元级；c) 定制 lib 文件级。DD 表征需要 RedHawk 生成的 \texttt{.apache/apache.pgarc}，APL 自动搜索。
  \item Spice 子电路文件——每单元 HSpice 兼容网表；可多文件；pin 顺序可不同；VDD/GND 常未在库中定义，APL 自动匹配缺失 P/G pin。
  \item Spice 器件模型文件——HSpice 兼容；可多文件/条目；各 corner 模型。
  \item Spice 到 LEF pin 映射——处理 SPICE 与 LEF 中 P/G pin 不同名。APL 输出 LEF P/G pin，内部用 Spice pin。关键字 \texttt{SPICE2LEF\_PIN\_MAPPING} 适用于开关电流、CDEV、PWCAP。仅允许：1 LEF pin $\leftrightarrow$ 1 Spice pin；或多个 LEF pin $\leftrightarrow$ 1 Spice pin。未给映射时 LEF 与 Spice 中 P/G pin 名须相同。
\begin{lstlisting}
SPICE2LEF_PIN_MAPPING {
    Vdd_spice   Vdd_lef
    Vss_spice   gnd_lef
}
\end{lstlisting}
  \item APL 配置文件——通常 \texttt{apldi.config} 或 \texttt{apl.config}，指定上述文件及温度、理想电源电压、P/G 节点名、缩放因子等。
  \item 单元列表文件——DD 表征（未做库 APL）或定制单元表征时需要。
  \item 输入向量文件——定制单元表征专用（见「定制单元表征数据准备」）。
\end{itemize}

\begin{noteBox}
单元表征用的负载电容来自 GSR 中定义的 SPEF/DSPF；否则使用 Steiner 树近似。slew 来自 GSR 中 PrimeTime 数据；否则使用 GSR 默认 slew。
\end{noteBox}

\subsection{APL 配置文件说明}
\subsubsection*{APL Configuration File Description}

配置文件包含表征所需信息，关键字分为：所有 APL 运行必需；仅库 APL（DI）必需；可选。

\subsubsection{必需的 APL 配置文件关键字}
以下关键字为单元表征必需（节选主要项，语法与示例保留英文关键字）：

\textbf{APL\_RUN\_MODE}——DD 或 DI，默认 DI。若无 \texttt{DESIGN\_CORNER} 定义，即使指定 DI 也为 DD。
\begin{lstlisting}
APL_RUN_MODE [ DD | DI ]
APL_RUN_MODE DI
\end{lstlisting}

\textbf{DC}——表征期间为特定 pin 指定 DC 电压。
\begin{lstlisting}
DC <pinName> <voltage_value>
DC VSSV 0
\end{lstlisting}

\textbf{DEVICE\_MODEL\_LIBRARY}——SPICE 器件模型库，须全路径，可多次定义，corner 如 TT/FF/SS。
\begin{lstlisting}
DEVICE_MODEL_LIBRARY <SPICE_model_lib_path> <process_corner>
DEVICE_MODEL_LIBRARY /home/design/13um.lib TT
\end{lstlisting}

\textbf{INCLUDE}——模型或其他参数文件，直接传给 NSPICE INCLUDE。
\begin{lstlisting}
INCLUDE <SPICE_device_model_filePath> ...
INCLUDE /home/design/spice.models
\end{lstlisting}

\textbf{PROCESS}——MSDF 流程要求 \texttt{<cell>.current} 提供 corner 名。WC=SS=slow，BC=FF=fast，TC=TT=typical。若指定 \texttt{DESIGN\_CORNER}，\texttt{PROCESS} 应为其子关键字。
\begin{lstlisting}
PROCESS [ FF | TT | SS | BC | TC | WC ]
PROCESS FF
\end{lstlisting}

\textbf{REDHAWK\_WORKING\_DIRECTORY}、\textbf{SIZE\_SCALE}（MOSFET L/W 缩放，um 为 1）、\textbf{SPICE\_NETLIST}、\textbf{SWEEP\_TEMPERATURE}（热漏电流表征温度列表）、\textbf{TEMP}、\textbf{VDD}、\textbf{VDD\_VALUES}（多 Vdd）、\textbf{VDD\_PIN\_NAME}/\textbf{GND\_PIN\_NAME}——见原书语法示例。

\subsubsection{仅库 APL（DI）必需关键字}
\textbf{APL\_RUN\_PASS}/\textbf{APL\_RUN\_FAIL}——电流表征时转储 spice 网表与输出波形：\texttt{[ NONE | DECK | ALL ]}。

\textbf{CUSTOM\_LIBS\_FILE}——无 LEF 时用手工定制 LIB 定义 Vdd/Vss pin。

\textbf{DESIGN\_CORNER}——每个设计 corner（温度+电压）生成一套单元特性；可含多个 \texttt{LIB\_ENTRY}、\texttt{SUBCKT}、\texttt{LIB\_FILES/DIR}。示例：
\begin{lstlisting}
DESIGN_CORNER {
    TT_25 {
        TEMP 25
        PROCESS TT
        VDD 1.0
        MODEL /nfs/apl1/model TT
    }
    FF_125 {
        TEMP 125
        PROCESS FF
        VDD 1.1
        MODEL /nfs/apl1/model FF
        LIB_FILES lib_dir1
    }
}
\end{lstlisting}

\textbf{LEF\_FILES}——多 P/G pin 的 LEF 定义。无 LEF 时在定制 LIB 中按 \texttt{pin <name> \{ type vdd|gnd \}} 定义。

\textbf{LIB\_FILES}——Synopsys \texttt{*.lib} 或定制 P/G arc 文件；目录则选全部文件；\texttt{CUSTOM} 标记 P/G arc 文件。

\textbf{大 cdev 值处理：}特殊单元 cdev 上限放宽后，\texttt{aplchk}/\texttt{aplreader}/\texttt{aplmerge} 须加 \texttt{-icheck}；APL 运行勿用 \texttt{-o <outfile>} 且配置勿设 \texttt{MERGE\_RESULT 1}；导入 RedHawk 时设 GSR \texttt{IGNORE\_APL\_CHECK 1}。

\subsubsection{可选 APL 配置文件关键字}
以下列出主要可选关键字（命令名保持英文）：

\begin{description}[leftmargin=2.5cm,style=nextline]
\item[\texttt{APL\_AFS}] AFS 仿真器路径。
\item[\texttt{APL\_ELDO}/\texttt{APL\_ELDO\_WDB}] 使用 ELDO 代替默认 NSPICE；\texttt{APL\_ELDO\_WDB} 控制 WDB-only 模式（默认 0）。
\item[\texttt{APL\_FORMAT\_CORRECTION}] 设为 1 时 \texttt{aplcopy} 根据翻转率自动修正单元类型（默认 0）。
\item[\texttt{APL\_HSPICE}/\texttt{APL\_HSPICE\_ENCRYPT}/\texttt{APL\_SPECTRE}] 外部仿真器路径或 metaencryptor 路径。
\item[\texttt{APL\_RESULT\_DIRECTORY}] 指定结果目录结构 \texttt{<corner>/CURRENT|CAP|PWC/<cell>.spiprof|cdev|pwcdev} 及对应 log。
\item[\texttt{APL\_SAMPLE\_MODE}] \texttt{FAST\_CHECK}（单样本完整性检查）或 \texttt{DEFAULT}（多样本，默认）。
\item[\texttt{APL\_TAIL\_REDUCTION}] 波形尾部削减：\texttt{0|1|moderate}，与 \texttt{EXTRACTION\_METHOD pwl} 配合。
\item[\texttt{APL\_TECH\_LEVEL}] PWL 输入波形表征，加速并减小文件（仅 NSpice/HSpice）。
\item[\texttt{APL\_VOLTAGES}] DI 库电压分数列表，默认 \texttt{4 1.15 1.0 0.9 0.75}。
\item[\texttt{CDEV\_AC\_OPEN\_INPUT}] cdev 表征排除输入 pin 电容（默认 0）。
\item[\texttt{CELL\_PROPERTY\_FILE}] 按 pin 指定输出负载。
\item[\texttt{CONVERT\_CCS\_CAP}] CCS 转 APL cdev（默认 0）。
\item[\texttt{DC\_TABLE\_THRESHOLD}] LDO dc 表细步长时减少数据点。
\item[\texttt{DEBUG}] 保存中间/错误文件（0/1）。
\item[\texttt{ELDO\_VECTOR\_MODE}] ELDO 数字向量时间语义（0=HSpice 兼容，1=ELDO 原生）。
\item[\texttt{EXTRACTION\_METHOD}] \texttt{pwl} 分段线性波形提取（默认等时间步）。
\item[\texttt{FAST\_CHECKING}] 等同 \texttt{apldi -fc}。
\item[\texttt{GZIP\_RESULT}] 压缩 current 输出。
\item[\texttt{IGNORE\_DC\_CHECK}/\texttt{IGNORE\_NETLIST\_CHECK}/\texttt{IGNORE\_RESET\_PIN}/\texttt{IGNORE\_UPF\_PGARC}] 各类检查放宽。
\item[\texttt{INCREMENTAL\_APL}] 增量表征失败/新增单元（须 \texttt{APL\_RESULT\_DIRECTORY}）。
\item[\texttt{INPUT\_TYPE}] 输入激励波形类型 0--4（4=50 段 PWL，推荐精度）。
\item[\texttt{LEAKAGE\_DEVICE\_MODEL\_LIBRARY}] 漏电流单独模型库。
\item[\texttt{LEAK\_HIGH\_TO\_MID\_RATIO\_LIMIT}/\texttt{LEAK\_HIGH\_TO\_LOW\_RATIO\_LIMIT}] pwcap 漏电流比检查。
\item[\texttt{LSF\_JOBID\_QUERY}] LSF 作业 ID 查询方式（默认 0）。
\item[\texttt{MIN/MAX\_LOAD\_SAMPLE}]、\texttt{MIN/MAX\_SLEW\_SAMPLE}] 表征 Cload/slew 范围。
\item[\texttt{MEMORYFILE}/\texttt{INPVECFILE}] 存储器/定制单元向量文件路径。
\item[\texttt{MERGE\_RESULT}] 合并结果为单文件（DD 或单 corner DI）。
\item[\texttt{MULTI\_CORE}] 本地多 CPU 并行（默认 1）。
\item[\texttt{MULTI\_NOMINAL}/\texttt{MULTI\_NOMINAL\_VOLTAGES\_METHOD}] 多标称电压漏电流/cdev。
\item[\texttt{MULTI\_SPICE}] 分层网表按 Vdd 拆分 Spice 运行。
\item[\texttt{OPENPIN}] 开路 pin 用大电阻接地。
\item[\texttt{OPTION}] Spice 仿真选项。
\item[\texttt{OUTPUT\_STATE\_CHECK}] 改进 cdev 的 HIGH/LOW 状态识别。
\item[\texttt{PIN\_LIST}] pin 与 tie pin 连接。
\item[\texttt{PRIMARY\_GND\_PIN}/\texttt{PRIMARY\_VDD\_PIN}] 多 rail 时主 GND/VDD（输出负载连接）。
\item[\texttt{PWCAP\_MULTI\_SPICE}] pwcap 多 Vdd Spice 并行数。
\item[\texttt{RUN\_TIME\_LIMIT}] LSF/SGE 进程时间上限（小时）。
\item[\texttt{SAMPLE\_SPLIT}] 按样本分发作业（0/1；多 corner 不支持）。
\item[\texttt{SCANMODE}/\texttt{SCAN\_OUTPUT\_LOAD}] 扫描链表征与 scan pin 负载。
\item[\texttt{SIM\_TIME\_SCALE}] 缩放脉冲宽度/周期/tstop 加速 cdev/漏电流仿真。
\item[\texttt{SIMULATION\_COMMAND}/\texttt{SIMULATOR\_COMMAND\_OPTION}] 自定义 LSF 提交包装与仿真器命令行附加选项。
\item[\texttt{SMOOTH\_PWC\_LEAK}] 平滑 pwcap 低电压样本漏电流毛刺。
\item[\texttt{SPICE\_SUBCKT\_DIR}] 每单元独立子电路文件目录（与 \texttt{SPICE\_NETLIST} 互斥，先指定者生效）。
\item[\texttt{SPICE2LEF\_PIN\_MAPPING}] 见上文。
\item[\texttt{SUPPRESS\_INTERNAL\_OPTION}] 不自动加收敛相关 Spice 选项。
\item[\texttt{SWEEPSOURCE}/\texttt{SWEEPVALUE}] 低功耗 header/footer 扫电压 pin 与电压列表；输出用 GSR \texttt{PIECEWISE\_CAP\_FILE}。
\item[\texttt{SWITCH\_PRE\_DRIVER}] 开关预驱动器 ESR/ESC（配合 APLSW）。
\item[\texttt{TAIL\_CUT\_OPTION}] 按时间截断尾部电流（\texttt{-p -tl <ps>} 保峰值）。
\item[\texttt{TMP\_DIR}] 临时文件目录。
\item[\texttt{WARN/ERROR\_CLOAD\_CHECK}]、\texttt{WARN/ERROR\_SLEW\_CHECK}]、\texttt{WARN/ERROR/MIN\_VDD\_CHECK}]——预检查 .lib 中 Cload/slew/Vdd 限值（S/M/I=标准/存储器/I/O 单元）。
\end{description}

\subsubsection{并行运行关键字}
Platform LSF 或 Sun Grid 可选十个关键字：\texttt{BATCH\_QUEUING\_COMMAND}（LSF 默认 \texttt{bsub}，Sun Grid 默认 \texttt{qsub}）、\texttt{BATCH\_QUEUING\_OPTIONS}（仅一行）、\texttt{EXEC\_PATH}、\texttt{GRID\_TYPE}（\texttt{LSF|SUN\_GRID}）、\texttt{JOB\_COUNT}/\texttt{LSF\_JOB\_COUNT}（默认 10，Sun Grid 最大 100）、\texttt{LSF\_ARRAY\_SUBMIT\_LIMIT}（默认 1000）、\texttt{LSF\_JOB\_TIME\_OUT}（挂起后杀死并重提交，默认 1 小时；程序/数据问题最长 12 小时）、\texttt{LSF\_SUBMIT\_MODE}（1=bsub，2=LSF API，默认 1）、\texttt{QUEUE}、\texttt{TIMER}（作业状态检查间隔，默认 60 秒）。

运行 \texttt{apldi} 或 \texttt{avm} 前在 csh 中：\texttt{setenv APACHEROOT <path\_to\_redhawk\_release\_directory>}。

%%%CH09_PART3%%%
'''

path = Path(r'd:\IC Design\VLSI\RH_CN\chapters\09_apl_char.tex')
text = path.read_text(encoding='utf-8')
if '%%%CH09_PART2%%%' not in text:
    raise SystemExit('marker not found')
path.write_text(text.replace('%%%CH09_PART2%%%', PART2), encoding='utf-8')
print('Part 2 written')
