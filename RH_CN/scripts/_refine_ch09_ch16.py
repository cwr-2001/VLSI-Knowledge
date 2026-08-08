# -*- coding: utf-8 -*-
"""Expand chapters 09 and 16 with full keyword-level translations."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CH09 = ROOT / "chapters" / "09_apl_char.tex"
CH16 = ROOT / "chapters" / "16_pathfinder_esd.tex"


def kw_block(name: str, zh: str, syntax: str = "", example: str = "", note: str = "") -> str:
    lines = [
        f"\\subsubsection{{\\gsr{{{name}}}}}",
        f"\\paragraph*{{{name}}}",
        "",
        zh,
        "",
    ]
    if syntax.strip():
        lines += ["\\textbf{语法：}", "\\begin{lstlisting}", syntax.strip(), "\\end{lstlisting}", ""]
    if example.strip():
        lines += ["\\textbf{示例：}", "\\begin{lstlisting}", example.strip(), "\\end{lstlisting}", ""]
    if note.strip():
        lines += ["\\begin{noteBox}", note, "\\end{noteBox}", ""]
    return "\n".join(lines)


def gen_ch09_optional_keywords() -> str:
    keywords = [
        ("APL_AFS", "指定 apldi 表征使用的 AFS 仿真器路径。", "APL_AFS <path_to_afs_simulator>"),
        ("APL_ELDO", "使用 ELDO 代替默认 NSPICE 进行开关电流及 cdev/pwcdev/switch 表征；须给出 ELDO 可执行文件全路径。", "APL_ELDO <full_path_to_binary>", "APL_ELDO abc/sim/eldo"),
        ("APL_ELDO_WDB", "APL 原生支持 ELDO 语法；设为 1 时启用 WDB-only 接口模式（默认 0）。", "APL_ELDO_WDB [ 0 | 1 ]"),
        ("APL_FORMAT_CORRECTION", "设为 1 时，aplcop 根据翻转率自动识别并修正错误单元类型（默认类型为翻转率为 2 的 Gate）。默认 0。", "APL_FORMAT_CORRECTION [0|1]"),
        ("APL_HSPICE", "使用 HSPICE 代替默认 NSPICE；须指定二进制路径。", "APL_HSPICE <path_to_binary>", "APL_HSPICE abc/sim/hspice"),
        ("APL_HSPICE_ENCRYPT", "指定内部 HSpice deck 加密用的 metaencryptor 路径。", "APL_HSPICE_ENCRYPT <path_to_metaencryptor>"),
        ("APL_SPECTRE", "使用 Spectre 代替默认 NSPICE；须指定二进制路径。", "APL_SPECTRE <path_to_binary>"),
        ("APL_RESULT_DIRECTORY", "为单单元结果指定目录结构：电流 \\texttt{<corner>/CURRENT/<cell>.spiprof}，decap \\texttt{<corner>/CAP/<cell>.cdev}，pwcap \\texttt{<corner>/PWC/<cell>.pwcdev}，及对应带时间戳的 log。默认 \\texttt{APLDD\\_<time>/} 或 \\texttt{APLDI\\_<time>/}。", "APL_RESULT_DIRECTORY <APL_dir_name>", "APL_RESULT_DIRECTORY Apl-out-ABC"),
        ("APL_SAMPLE_MODE", "按所需精度选择表征类型；样本数由库中电压/负载/slew 范围自动决定。默认 DEFAULT（原 APLDI\\_SAMPLE）。", "APL_SAMPLE_MODE [ FAST_CHECK | DEFAULT ]", "APL_SAMPLE_MODE FAST_CHECK", "FAST\\_CHECK：每单元单样本完整性检查；DEFAULT：多样本全表征。"),
        ("APL_TAIL_REDUCTION", "等时间步波形尾部削减：0 关闭；1 原始算法；\\texttt{moderate} 改进算法（配合 \\texttt{EXTRACTION\\_METHOD pwl}）。", "APL_TAIL_REDUCTION [ 0 | 1 | moderate ]"),
        ("APL_TECH_LEVEL", "设为 1 时用 PWL 输入波形表征，加速并约减半磁盘占用；支持定制向量流程。仅 NSpice/HSpice。", "APL_TECH_LEVEL [ 0 | 1 ]"),
        ("APL_VOLTAGES", "DI 库中以标称电压分数指定表征电压点；须升序或降序。若未指定 $\\ge 1.15\\times$ 标称的点，APL 自动补充。默认：\\texttt{4 1.15 1.0 0.9 0.75}。", "APL_VOLTAGES <Num> <fraction1> ...", "APL_VOLTAGES 4 0.8 0.9 1.0 1.2"),
        ("CDEV_AC_OPEN_INPUT", "设为 1 时 cdev 表征排除所有输入 pin 电容（默认 0）。", "CDEV_AC_OPEN_INPUT [ 0 | 1 ]"),
        ("CELL_PROPERTY_FILE", "按 pin 指定输出负载的文件。", "cell <name> { pin <pin> { load <F> } ... }", "CELL_PROPERTY_FILE <filename>"),
        ("CONVERT_CCS_CAP", "将含 intrinsic\\_parasitic ESC/ESR/漏电流的 CCS 库转为 APL cdev（默认 0）。用户须确认 CCS 与 APLCAP 中 ESC/ESR 含义一致。", "CONVERT_CCS_CAP [0 |1]"),
        ("DC_TABLE_THRESHOLD", "LDO dc 表在细步长 Spice dc 仿真时减少数据点。", "DC_TABLE_THRESHOLD <slope_threshold>", "DC_TABLE_THRESHOLD 0.08"),
        ("DEBUG", "调试标志：保存中间与错误文件。", "DEBUG [ 0 | 1 ]"),
        ("ELDO_VECTOR_MODE", "0：ELDO 向量按 HSpice 语义（时间点为初值，默认）；1：ELDO 原生（时间点为终值）。", "ELDO_VECTOR_MODE [0 | 1]"),
        ("EXTRACTION_METHOD", "波形提取：\\texttt{pwl} 分段线性，文件更小且精度接近 Spice；默认等时间步。", "EXTRACTION_METHOD [ 0 | pwl ]"),
        ("FAST_CHECKING", "设为 1 时每单元单样本数据检查，等同 \\texttt{apldi -fc} 或 GSR \\texttt{APLDI\\_SAMPLE\\_MODE fast\\_check}。", "FAST_CHECKING [ 1 | 0 ]"),
        ("GZIP_RESULT", "压缩电流输出文件。", "GZIP_RESULT [ 0 | 1 ]"),
        ("IGNORE_DC_CHECK", "忽略用户 DC 偏置的输入 pin 检查，允许同一配置覆盖有/无 DC pin 的单元。", "IGNORE_DC_CHECK [ 0 | 1 ]"),
        ("IGNORE_NETLIST_CHECK", "P/G pin 预检查：0 检查配置与网表 pin 名一致；默认 1 跳过。", "IGNORE_NETLIST_CHECK [ 1 | 0 ]"),
        ("IGNORE_RESET_PIN", "Set/Reset pin 在网表中缺失时 Warning 继续（默认 Error）。", "IGNORE_RESET_PIN [ 0 | 1 ]"),
        ("IGNORE_UPF_PGARC", "UPF lib 无 P/G pin 时用定制 lib 定义 pg arc。", "IGNORE_UPF_PGARC [ 0 | 1 ]"),
        ("INCREMENTAL_APL", "增量表征：仅重跑失败或新增单元（须设 \\texttt{APL\\_RESULT\\_DIRECTORY}）。", "INCREMENTAL_APL [ 0 | 1 ]"),
        ("INPUT_TYPE", "输入激励波形：0 单段 ramp（默认）；2 ramp+RC；3 5 段 PWL+RC；4 50 段 PWL（推荐）。", "INPUT_TYPE [ 0 | 2 | 3 | 4 ]"),
        ("LEAKAGE_DEVICE_MODEL_LIBRARY", "漏电流表征单独器件模型库。", "LEAKAGE_DEVICE_MODEL_LIBRARY <file> ?<corner>?"),
        ("LEAK_HIGH_TO_MID_RATIO_LIMIT", "pwcap 漏电流比：最高 Vdd(1.1x) 与中点(0.5x) 之比低于阈值则不记入 log。", "LEAK_HIGH_TO_MID_RATIO_LIMIT <ratio>"),
        ("LEAK_HIGH_TO_LOW_RATIO_LIMIT", "pwcap 漏电流比：最高 Vdd 与最低(0.1x) 之比。", "LEAK_HIGH_TO_LOW_RATIO_LIMIT <ratio>"),
        ("LSF_JOBID_QUERY", "1：从作业提交返回消息取 LSF job ID；0：从 LSF 主机查询（默认，网络负担更大）。", "LSF_JOBID_QUERY [0 | 1]"),
        ("MIN_LOAD_SAMPLE", "表征 Cload 下限（F），可覆盖 WARN/ERROR\\_CLOAD\\_CHECK。", "MIN_LOAD_SAMPLE <load_Farads>", "MIN_LOAD_SAMPLE 10e-15"),
        ("MAX_LOAD_SAMPLE", "表征 Cload 上限（F）。", "MAX_LOAD_SAMPLE <load_Farads>", "MAX_LOAD_SAMPLE 500e-15"),
        ("MIN_SLEW_SAMPLE", "表征 transition time 下限（s）。", "MIN_SLEW_SAMPLE <trans_time-sec>", "MIN_SLEW_SAMPLE 10e-12"),
        ("MAX_SLEW_SAMPLE", "表征 transition time 上限（s）。", "MAX_SLEW_SAMPLE <trans_time-sec>", "MAX_SLEW_SAMPLE 500e-12"),
        ("MEMORYFILE", "存储器或定制单元输入向量文件路径（同 INPVECFILE）。", "[ MEMORYFILE | INPVECFILE ] </path>", "MEMORYFILE /nfs/apl1/memfile"),
        ("MERGE_RESULT", "设为 1 将结果合并为运行目录单文件；亦在 \\texttt{apldi -o} 时合并。仅建议 DD 或单 corner DI。", "MERGE_RESULT [ 0 | 1 ]"),
        ("MULTI_CORE", "本地多 CPU 并行提交作业数（默认 1，即开启）。", "MULTI_CORE [ 0 | 1 ]"),
        ("MULTI_NOMINAL", "多标称电压 cdev/漏电流：在每个电压点捕获漏电流。", "MULTI_NOMINAL [ 0 | 1 ]"),
        ("MULTI_NOMINAL_VOLTAGES_METHOD", "0：仅用 .LIB 第一个标称电压做 derating；1：使用全部标称电压及其 derating 组合。", "MULTI_NOMINAL_VOLTAGES_METHOD [ 0 | 1 ]"),
        ("MULTI_SPICE", "分层网表按 Vdd 拆分 Spice deck 与向量 VIH（默认关以缩短单机时间）。", "MULTI_SPICE [ 0 | 1 ]"),
        ("OPENPIN", "为未连接 pin 接大电阻到地以便表征。", "OPENPIN <pinA> <pinB> ...", "OPENPIN ABCpin3A MNOpin14BC"),
        ("OPTION", "Spice 仿真选项，可多次或块形式。", "OPTION <Spice option>", "OPTION mode=turbo"),
        ("OUTPUT_STATE_CHECK", "改进基于 STATE\\_TABLE 的 cdev HIGH/LOW 状态识别。", "OUTPUT_STATE_CHECK [ 0 | 1 ]"),
        ("PIN_LIST", "pin 与 tie pin 连接关系。", "PIN_LIST { <pin> <tie_pin> ... }", "PIN_LIST { A1 VDD1 }"),
        ("PRIMARY_GND_PIN", "多 rail 时输出负载所接主地 pin（可为 Spice 地网名）。", "PRIMARY_GND_PIN <name>", "PRIMARY_GND_PIN VSS0"),
        ("PRIMARY_VDD_PIN", "多 rail 时输出负载所接主电源 pin。", "PRIMARY_VDD_PIN <name>"),
        ("PWCAP_MULTI_SPICE", "pwcap 多 Vdd Spice 并行数（仅多核，非 LSF）。", "PWCAP_MULTI_SPICE <parallel run count>"),
        ("RUN_TIME_LIMIT", "LSF/SGE 进程时间上限（小时），到期后继续处理。", "RUN_TIME_LIMIT <limit_hrs>"),
        ("SAMPLE_SPLIT", "按样本分发作业：0 全不用；1 全用；未设则按网表大小自动。多 corner 不支持。", "SAMPLE_SPLIT [ 0 | 1 ]"),
        ("SCANMODE", "扫描链单元表征开关（默认 0）。", "SCANMODE [ 0 | 1 ]"),
        ("SCAN_OUTPUT_LOAD", "为 scan pin 附加恒定负载。", "SCAN_OUTPUT_LOAD <load>"),
        ("SIM_TIME_SCALE", "缩放 cdev/漏电流瞬态脉冲宽度与 tstop 以加速（cdev 默认 1.0；热漏电流默认 0.1）。", "SIM_TIME_SCALE <value>"),
        ("SIMULATION_COMMAND", "自定义 LSF 作业提交包装；\\$input\\_file 必需，\\$output\\_file 可选。", "SIMULATION_COMMAND <sim_command>"),
        ("SIMULATOR_COMMAND_OPTION", "附加到 Spice 命令行的用户选项。", "SIMULATOR_COMMAND_OPTION <option>"),
        ("SMOOTH_PWC_LEAK", "平滑 pwcap 低电压样本漏电流毛刺。", "SMOOTH_PWC_LEAK [ 1 | 0 ]"),
        ("SPICE_SUBCKT_DIR", "每单元独立子电路文件目录（与 SPICE\\_NETLIST 互斥，先指定者生效）。文件名 \\texttt{<cell>.<ext>}。", "SPICE_SUBCKT_DIR <directory>", "SPICE_SUBCKT_DIR ./spice_netlists"),
        ("SPICE2LEF_PIN_MAPPING", "Spice 与 LEF P/G pin 名映射；支持开关电流、CDEV、PWCAP。", "SPICE2LEF_PIN_MAPPING { <spice> <lef> ... }"),
        ("SUPPRESS_INTERNAL_OPTION", "不自动添加收敛相关 Spice 选项（如 method=gear）。", "SUPPRESS_INTERNAL_OPTION [ 0 | 1 ]"),
        ("SWEEPSOURCE", "低功耗 header/footer 扫电压的电源或地 pin 名；默认可由 PRIMARY\\_VDD/GND\\_PIN 或 Vdd 决定。", "SWEEPSOURCE [<power_pin> | <gnd_pin>]", "SWEEPSOURCE vdd1"),
        ("SWEEPVALUE", "替代默认 11 点有效电压（0.1--1.1$\\times V_{eff}$）的自定义列表。", "SWEEPVALUE <v1> <v2> ...", "SWEEPSOURCE vdd\nSWEEPVALUE 1.0 0.9 0.8 0.7"),
        ("SWITCH_PRE_DRIVER", "用 APLSW 表征开关预驱动器 ESR/ESC；DC 须使 header 输出 1、footer 输出 0。", "SWITCH_PRE_DRIVER { VDD_PIN_NAME ... DC <pin> <V> }"),
        ("TAIL_CUT_OPTION", "按时间截断尾部电流，\\texttt{-p} 保峰值。", "TAIL_CUT_OPTION -p -tl <ps>", "TAIL_CUT_OPTION -p -tl 500"),
        ("TMP_DIR", "临时文件目录。", "TMP_DIR <path>", "TMP_DIR /home/tmp"),
        ("WARN_CLOAD_CHECK", "预检查 .lib Cload（pF）：S/M/I=标准/存储器/I/O，默认 Warning 5/50/50。", "WARN_CLOAD_CHECK { S <val> M <val> I <val> }"),
        ("ERROR_CLOAD_CHECK", "Cload 错误阈值，默认 S/M/I=50/500/500。", "ERROR_CLOAD_CHECK { S <val> M <val> I <val> }"),
        ("WARN_SLEW_CHECK", "预检查 .lib slew（ns），默认 S/M/I=5/10/10。", "WARN_SLEW_CHECK { S <val> M <val> I <val> }"),
        ("ERROR_SLEW_CHECK", "slew 错误阈值。", "ERROR_SLEW_CHECK { S <val> M <val> I <val> }"),
        ("WARN_VDD_CHECK", "标称 Vdd Warning 阈值（默认 >5V）。", "WARN_VDD_CHECK <Vdd_warn_val>"),
        ("ERROR_VDD_CHECK", "标称 Vdd 过高错误（默认 >10V）。", "ERROR_VDD_CHECK <Vdd_high_error_val>"),
        ("MIN_VDD_CHECK", "标称 Vdd 过低错误（默认 <0.5V）。", "MIN_VDD_CHECK <Vdd_low_error_val>"),
    ]
    parts = ["\\subsubsection{可选 APL 配置文件关键字}", "以下逐项说明主要可选关键字（命令名保持英文）：", ""]
    for item in keywords:
        parts.append(kw_block(*item))
    return "\n".join(parts)


def gen_ch09_parallel_keywords() -> str:
    parallel = [
        ("BATCH_QUEUING_COMMAND", "批队列命令；LSF 默认 \\texttt{bsub}，Sun Grid 默认 \\texttt{qsub}。", "BATCH_QUEUING_COMMAND <command>", "BATCH_QUEUING_COMMAND qsub"),
        ("BATCH_QUEUING_OPTIONS", "LSF/SGE 特有选项；文件中仅允许一行且选项须连续。", "BATCH_QUEUING_OPTIONS <options>", "BATCH_QUEUING_OPTIONS -P mary -cwd -b y"),
        ("EXEC_PATH", "LSF 或 Sun Grid 二进制路径。", "EXEC_PATH <path>"),
        ("GRID_TYPE", "并行平台：\\texttt{LSF}（默认）或 \\texttt{SUN\\_GRID}。", "GRID_TYPE <LSF | SUN_GRID>"),
        ("JOB_COUNT", "并行作业数（LSF 默认 10；Sun Grid 最大 100）。", "JOB_COUNT <n>"),
        ("LSF_JOB_COUNT", "同 JOB\\_COUNT（LSF 专用别名）。", "LSF_JOB_COUNT <n>"),
        ("LSF_ARRAY_SUBMIT_LIMIT", "LSF job array 提交上限（默认 1000）。", "LSF_ARRAY_SUBMIT_LIMIT <n>"),
        ("LSF_JOB_TIME_OUT", "挂起作业杀死并重提交前等待时间（默认 1 小时）。", "LSF_JOB_TIME_OUT <hours>"),
        ("LSF_SUBMIT_MODE", "1=bsub；2=LSF API；3=array 提交（须 \\texttt{-j 1}）。", "LSF_SUBMIT_MODE [ 1 | 2 | 3 ]"),
        ("QUEUE", "指定队列名。", "QUEUE <queue name> ...", "QUEUE short"),
        ("TIMER", "作业状态轮询间隔（秒，默认 60）。", "TIMER <seconds>", "TIMER 10"),
    ]
    parts = ["\\subsubsection{并行运行关键字}", "Platform LSF 或 Sun Grid 可选下列关键字：", ""]
    for item in parallel:
        parts.append(kw_block(*item))
    parts.append(
        "运行 \\texttt{apldi} 或 \\texttt{avm} 前在 csh 中："
        "\\texttt{setenv APACHEROOT <path\\_to\\_redhawk\\_release\\_directory>}。"
    )
    return "\n".join(parts)


def gen_ch09_di_required_expand() -> str:
    return r"""
\subsubsection{仅库 APL（DI）必需关键字——详述}

\kw{APL_RUN_PASS} / \kw{APL_RUN_FAIL}：电流表征时转储 Spice 网表与输出波形。
\begin{lstlisting}
APL_RUN_PASS [ NONE | DECK | ALL ]
APL_RUN_FAIL [ NONE | DECK | ALL ]
\end{lstlisting}

\kw{CUSTOM_LIBS_FILE}：无 LEF 时用手工定制 LIB 定义 Vdd/Vss pin；APL-DI 将 pin 写入 \texttt{adsLib.output}。
\begin{lstlisting}
CUSTOM_LIBS_FILE { <.lib_file> }
\end{lstlisting}

\kw{DESIGN_CORNER}：每个工艺 corner（温度+电压+模型）生成一套特性；可含 \texttt{LIB_ENTRY}、\texttt{SUBCKT}、\texttt{LIB_FILES}、\texttt{CUSTOM_LIBS_FILE}、\texttt{LIBS_DIRECTORY} 等。
\begin{lstlisting}
DESIGN_CORNER {
    TT_25 { TEMP 25 PROCESS TT VDD 1.0 MODEL /nfs/apl1/model TT }
    FF_125 { TEMP 125 PROCESS FF VDD 1.1 MODEL /nfs/apl1/model FF
             LIB_FILES lib_dir1 lib_dir2/clkGen_fast.lib }
}
\end{lstlisting}

\kw{LEF_FILES}：多 P/G pin 的 LEF 定义；APL 分别捕获各电源/地 pin 的电流与电容剖面。
\begin{lstlisting}
LEF_FILES { design_data/lef/cella.lef design_data/lef/cellb.lef }
\end{lstlisting}
无 LEF 时在定制 LIB 中定义：
\begin{lstlisting}
cell CELLA {
    pin VDDIN { type vdd }
    pin VDD   { type vdd }
    pin VSS   { type gnd }
}
\end{lstlisting}

\kw{LIB_FILES}：Synopsys \texttt{*.lib} 或定制 P/G arc；目录则纳入全部文件；\texttt{CUSTOM} 标记 P/G arc 文件。
\begin{lstlisting}
LIB_FILES {
    libs/special/custom.lib CUSTOM
    libs/typical
    libs/memory/mem.lib
}
\end{lstlisting}
P/G arc 文件格式：\texttt{pgarc \{ <vdd> <vss> ... \}}。

\paragraph{大 cdev 值处理}
APLDI 对特殊单元放宽 cdev 上限会改变 ESC。导入与工具链须：
\begin{enumerate}
  \item \texttt{aplchk}/\texttt{aplreader}/\texttt{aplmerge} 加 \texttt{-icheck}
  \item APL 运行勿用 \texttt{-o <outfile>}，配置勿设 \texttt{MERGE_RESULT 1}
  \item RedHawk 导入设 GSR \texttt{IGNORE_APL_CHECK 1}
\end{enumerate}
"""


def gen_ch09_vectors() -> str:
    return r"""
\section{定制单元表征数据准备}
\subsection*{Custom Cell Characterization Data Preparation}

APL 可表征组合逻辑与时序等定制单元，须用户指定表征向量。除标准单元数据外，每个待表征单元须有一个向量文件；配置中须含 \kw{VECTOR_DIR}（全路径）。

\kw{VECTOR_DIR} 指定输入向量目录：
\begin{lstlisting}
VECTOR_DIR /home/design/input_vectors
\end{lstlisting}

\subsection{输入向量文件}
\subsubsection*{Input Vector Files}

APL-DI 由 \texttt{libreader} 创建向量；APL-DD 由 RedHawk 调用 \texttt{libreader}。定制单元须手工创建 \texttt{<cell_name>.inv}。

向量文件指定：输入向量；决定延迟的时序 arc 相关 pin；固有 decap 与漏电流的输入偏置。

\paragraph{DC 偏置}
\begin{lstlisting}
param <bias_level> <value>
dc <pin1> <bias_level>
\end{lstlisting}
偏置名须与配置中 Vdd/Vss pin 名一致；注意与 APL 配置电压一致。

\paragraph{主输入输出}
\begin{lstlisting}
active_input <input_pin1> <input_pin2> ...
active_output <output_pin>
\end{lstlisting}

\paragraph{向量块}
\begin{lstlisting}
vector {
    vname <input1> <input2> ...
    tunit ps
    vih [ <Vdd_name> | <VIH_value> ]
    <time_step> <state_pin1><state_pin2>... ?<state_name>?
}
\end{lstlisting}
\texttt{time\_step} 为 APL 单位时间步倍数（非实际 ns）；0 步用于初始化。向量状态值之间\textbf{无空格}。\texttt{MULTI\_SPICE 1} 时 \texttt{vih} 可为标称 Vdd 名，VIH 按电压百分比缩放。

\subsubsection{组合逻辑多向量示例}
五输入组合门示例（\texttt{a,b} 与 \texttt{e} 不同电源域）：
\begin{lstlisting}
dc c vdd
dc d 0
active_input a
active_output y
vector {
    vname a b
    tunit ps
    vih Vdd1
    0 10
    1 01
    5 10
}
vector {
    vname e
    tunit ps
    vih Vdd2
    0 1
    1 0
    5 1
}
\end{lstlisting}
时间步含义：步 0 时 A=1,B=0；步 1 时 A=0,B=1；步 5 时 A=1,B=0——确保输出 0$\rightarrow$1 与 1$\rightarrow$0 均被捕获。

\figplaceholder{Figure 9-2}{两输入组合门的信号剖面}

\subsubsection{时序单元向量示例}
须捕获 TRAN01、TRAN10、TRAN11（触发沿输出不翻转）、TRAN00（非触发沿）：
\begin{lstlisting}
dc scen 0
dc scin 0
active_input clock
active_output nq
vector {
    vname clock d
    tunit ns
    vih 1.2
    0 00
    2 10
    4 01
    6 11 tran10
    8 01
    10 11
    12 01
    14 10 tran01
    16 00 tran00
    18 10 tran11
    20 00
}
\end{lstlisting}

\figplaceholder{Figure 9-3}{时序单元的信号剖面}

图~\ref{fig:apl-seq-prof} 中 \texttt{0->0} 为非触发时钟沿，\texttt{1->1} 为触发沿且输出保持。

\begin{noteBox}
所有 \texttt{<cell\_name-n>.inv} 须位于 \kw{VECTOR_DIR} 指定目录。
\end{noteBox}
"""


def gen_ch09_rest() -> str:
    return r"""
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
  \item GUI \texttt{APL -> Setup} 或 TCL \texttt{setup apl -dir <dir\_name>}，生成 \texttt{apache.apl}、\texttt{adsLib.output}（在 \texttt{<dir>/.apache}），并创建模板：\texttt{apl.custom.config}、\texttt{apl.io.config}、\texttt{apl.memory.config}、\texttt{apl.std.config} 及单元列表。
  \item 准备配置文件。
  \item 运行 APL-DD。
  \item 低功耗设计：额外运行 header/footer 与 decap（pwcap），见「低功耗设计表征」。
\end{enumerate}

\subsection{增强型设计无关表征}
GSR \kw{APL_DID} 设为 1 时，RedHawk 自动为 APL-DI 覆盖不足的实例生成额外设计相关样本。APL-DI 在 \texttt{APLDI\_[yyyymmdd]/corner[n]/CURRENT/PACKAGE} 打包 Spice 与配置。已生成 DI 库可用：
\begin{lstlisting}
aplgenpkg -d APLDI_[yyyymmdd] -c <apldi_config>
\end{lstlisting}
导入须用目录格式：\texttt{import apl APLDI/APLDI\_20070310/corner1/CURRENT}（非单一 \texttt{*.current}）。

\subsection{从 UNIX Shell 运行 APL 表征}
\begin{lstlisting}
% apldi [-c] [-w] [-sw] [ -l <cell_file> | -p <decap_file> ]
      ? -o <output_file>? ? -s [1|2]? ?-j [1|2]? ?-v? ?-fc ? <apl_config_file>
\end{lstlisting}

\begin{itemize}
  \item \texttt{-c}：decap 表征；\texttt{-w}：pwcap；\texttt{-sw}：开关 decap
  \item \texttt{-l}：单元列表；\texttt{-o}：输出（勿用 \texttt{.spiprof/.spcurrent/.cdev/.pwcdev} 作扩展名）
  \item \texttt{-p}：有意 decap 列表（不与 \texttt{-c} 同用）
  \item \texttt{-s 1|2}（仅 DI）：1=仅生成样本；2=不生成样本直接表征（DD 常用）
  \item \texttt{-j 1|2}：多机（1=bsub，2=LSF API；SunGrid 亦用 \texttt{-j}）
  \item \texttt{-v}：详细；\texttt{-fc}：快速库检查
\end{itemize}

许可证等待：\texttt{setenv APACHEDA\_LICENSE\_WAIT <xxx:unit sec>}。

\subsection{多 Vdd/Vss Decap 单元}
\begin{lstlisting}
DECAP_VDD_PIN { VDD 1.2 VDDPST 3.3 }
CUSTOM_LIBS_FILE { <custom.lib> }
\end{lstlisting}
多 Vdd/Vss decap 的 P/G arc 须在 \texttt{pgarc.lib} 手工定义：
\begin{lstlisting}
cell decap234 {
    pgarc { VDD VSS  VDDPST VSSPST }
}
\end{lstlisting}

\subsection{APL 调用示例}
DD：
\begin{lstlisting}
% apldi -s 2 -l cell_list2 apl.config
% apldi -j 2 -s 2 -l cell_list2 apl.config
% apldi -l cell_list1 -c apldi.config
% apldi -p decap_cell_list6 apl.config
\end{lstlisting}
Decap 列表每行 \texttt{<cell\_name>}。

DI：
\begin{lstlisting}
% apldi -j 2 apldi.config
% apldi -j 2 -c -l cell_list_dc apldi.config
% apldi -j 2 -w cell_list_pw apldi.config
\end{lstlisting}

\subsection{低功耗设计表征}
Header 扫 Vdd 从近零到 Vdd；Footer 扫 Vss 从近 Vdd 到零。\kw{SWEEPSOURCE}、\kw{SWEEPVALUE}、\kw{PRIMARY_VDD_PIN}/\kw{PRIMARY_GND_PIN}。
\begin{lstlisting}
% apldi -w [ -l <cell_list> | -p <decap_list> ] [-o <output>] <apl_config>
aplsw [-c] [-d] [-o <output_file>] <sw_config_list.conf>
\end{lstlisting}
结果用 GSR \kw{PIECEWISE_CAP_FILE} 导入。详见第~\ref{chap:lp}~章。

\section{APL 中的多作业管理}
\subsection*{Multi-Job Management in APL}

APL 在 LSF 9.x 使用 Job array，数组内作业共享 job ID。
\begin{enumerate}
  \item 配置：
\begin{lstlisting}
GRID_TYPE lsf
BATCH_QUEUING_COMMAND bsub
LSF_SUBMIT_MODE 3
BATCH_QUEUING_OPTIONS -J shortjob
\end{lstlisting}
  \item 须 \texttt{-j 1}；例：\texttt{\$APACHEROOT/bin/apldi2 -l list -j 1 apl.current.config}
  \item APL 用自有机制监控作业，不再查询 LSF 守护进程。
\end{enumerate}
LSF 9.x 默认 array 大小 1000；\kw{SAMPLE_SPLIT} 模式下 array 须大于作业数。

\section{输出文件}
\subsection*{Output Files}

\subsection{整体流程文件}
\textbf{进程日志}（\texttt{adsRpt/Log/}）：\texttt{apl.current.log.<time>}、\texttt{apl.cap.log.<time>}、\texttt{apl.pwcap.log.<time>}。

\textbf{错误/警告}（\texttt{adsRpt/Error/}、\texttt{Warn/}）：\texttt{apl.current.err|warn.<time>} 等；\texttt{adsRpt/} 顶层软链接到最新结果。

\textbf{状态：}\texttt{aplstat <apl\_config>} 写 \texttt{aplstat.log}，汇总成功/失败/待处理及原因。

\subsection{结果文件}
\textbf{APL-DI：}\texttt{/<corner>.current}、\texttt{/<corner>.cdev}、\texttt{/<corner>.pwcdev}。

\textbf{APL-DD：}\texttt{/<cell>.spcurrent}（节点上限 10 亿）、\texttt{/<cell>.cdev}、\texttt{/<cell>.pwcdev}。

\subsection{单单元表征文件}
默认 \texttt{APLDI\_<time>/} 或 \texttt{APLDD\_<time>/}；\kw{APL_RESULT_DIRECTORY} 可改。结构：\texttt{corner*/CURRENT|CAP|PWCAP/<cell>.spiprof|cdev|pwcdev} 及 \texttt{.<time>.log}。

\subsection{APL 结果检查与处理}
\begin{lstlisting}
aplchk <input_file/dir> ?-v? ?-l <list_file>? ?-w <output_file>?
    ?-c? ?-pwc <pwcdev_file>? ?-conf <APL_config>? ?-spice <apl config>?
\end{lstlisting}
失败列表：\texttt{adsRpt/aplchk.log}。

\paragraph{检查限值（全局或 \kw{CELL_CHECK_LIMITS} 按单元）}
\begin{longtable}{@{}p{0.35\textwidth}p{0.58\textwidth}@{}}
\toprule
\textbf{关键字} & \textbf{说明（默认）} \\
\midrule
\endhead
\kw{IMAX_STDCELL_WARN} & 峰值电流 Warning（100000\,uA） \\
\kw{ITAIL_STDCELL_WARN} & 尾部电流 Warning \\
\kw{SLEWMAX_STDCELL_WARN} & 最大 slew（3e6\,ps） \\
\kw{DELAYMAX_STDCELL_WARN} & 最大延迟 \\
\kw{FIREMAX_STDCELL_WARN} & FIRE 指标 \\
\kw{CMAX_STDCELL_WARN} & 最大电容（1000\,pF） \\
\kw{RMAX_STDCELL_WARN} & 最大电阻 \\
\kw{LEAKMAX_STDCELL_WARN/ERROR} & 漏电流 \\
\kw{PWC_VDD_MAX_WARN} & pwcap 最大 Vdd（5\,V） \\
\kw{*_MEMORY_*} 系列 & 存储器对应限值（峰值默认 1e6\,uA） \\
\bottomrule
\end{longtable}

\texttt{aplchk -c <cell>.cdev} 输出 c0/c1、r0/r1、leak0/leak1 直方图。

\subsection{无 APL 数据或样本的单元报告}
\begin{itemize}
  \item 无电流：\texttt{adsRpt/apache.inst.libCurrent}
  \item 无 decap：\texttt{apache.refCell.noAplCap}
  \item 无电压相关 decap：\texttt{apache.refCell.noAplPwcap}
  \item 有 APLDI 无样本：\texttt{apache.refcell.noAplSample}（Warning ITG-022）
\end{itemize}

\section{在 RedHawk 中导入与合并表征数据文件}
\subsection*{Importing and Merging Characterization Data Files in RedHawk}

\subsection{导入 APL 文件}
推荐 GSR \kw{APL_FILES}：
\begin{lstlisting}
APL_FILES {
    <APL_binary>    current
    <APL_binary>    cdev
    <Avm.conf>      avm
    <AVM_binary>    current_avm
    <APL binary>    pwcap
}
\end{lstlisting}
或 \texttt{import apl <file>}；\texttt{import apl} 与 \texttt{import apl -c} 可累积。\texttt{APL\_FILES} 优先支持目录与多类型。命令文件有 \texttt{import apl} 时 GSR \texttt{APL\_FILES} 被忽略。

导入错误：默认忽略 model/Vdd/温度差异；\texttt{gsr set ignore\_apl\_check 1} 忽略全部；或 GUI \texttt{APL -> Import}。

\subsection{合并 APL 结果文件}
\begin{lstlisting}
aplmerge [-c] [-pwc] [-rep] [-l <cell_list>] [-im] [-t] [-o <output>]
    [-avm] [-ilimit] [<file1> ...] [<directory>] [-fl <list_file>]
    [-multi_pvt_merge <file1> <file2>]
\end{lstlisting}
\texttt{-rep}：用 file2 同名单元替换 file1；\texttt{-l} 列表格式 \texttt{<path>/<cellname>}；\texttt{-avm} 忽略 AVM 头差异；\texttt{aplmerge -o <cell>.current *.spiprof} 支持通配符。

\section{aplccs（CCS2APL）库表征}
\subsection*{aplccs (CCS2APL) Library Characterization}

\texttt{aplccs} 将 CCS 库转为 APL 开关电流格式。优势：对 RedHawk 透明；运行前可生成 DI 库；转换极快；时序为硬值。

标准单元：支持对角稀疏 cload 表；多 \texttt{nom\_voltage} 合并须 slew 归一化/温度/pg\_pins/states/samples 一致；C00/C11 \texttt{\_toggle} 扩展样本（同 slew 波形相同）。存储器/I/O/定制：C-load 无关状态默认 1\,fF；支持多输出。

\begin{lstlisting}
aplccs [-o <output_file>] -mstate_cells <cell_list> -conf <aplccs_config> [-skip_ps]
\end{lstlisting}
默认 \texttt{ccs.current}；\texttt{-skip\_ps} 跳过 \texttt{.apache/apache.pslib}。

\subsection{APLCCS 配置文件}
\begin{itemize}
  \item \kw{LIB_FILES}/\kw{LIBS_DIRECTORY}/\kw{LIBS_FILE}
  \item \kw{RETRY_VECTORLESS [0|1]}：向量失败时用随机向量（默认向量同 APL）
  \item \kw{IGNORE_CELLS \{ <cell> ... \}}：跳过格式异常单元
\end{itemize}

\subsection{直接导入 CCS Lib}
\kw{LIB_USE_CCS} 1：RedHawk 流程透明转换。\kw{CCS_OVERRIDE_APL} 1：CCS 优先于 APL（须 \kw{LIB_USE_CCS} 1）。\kw{CONVERT_CCS_CAP}：CCS intrinsic 转 cdev。

\section{I/O 单元表征}
\subsection*{I/O Cell Characterization}

I/O 可向内核注入显著噪声（尤其共享 VSS），应纳入动态分析。须表征 core 与 I/O 全部 Vdd/Vss pin 电流。

\subsection{I/O 单元表征流程}
\begin{enumerate}
  \item I/O Vdd（在 SPICE \texttt{.subckt}，非 .lib）：\texttt{dc <io\_vdd\_pin> <value>}
  \item 开路监测：\texttt{openpin <open\_pins>}
  \item 参数：\texttt{param vddo=1.5}、\texttt{dc VDDQ15 vddo}
  \item 激励：\texttt{active\_input clk}（差分 I/O 勿用自动）；或 \texttt{VECTOR \{ VNAME ... TUNIT VIH SLOPE ... \}}
  \item 负载：\texttt{OUTPUT <out\_pin> <load\_subckt>}，子电路在 \texttt{.inpvec} 或 include 中定义。
\end{enumerate}

板级负载示例子电路：
\begin{lstlisting}
.subckt pkg_board_load chip_node
X1 chip_node bga_node pkg_load
X2 bga_node far_end_node board_load
.ends
\end{lstlisting}

\subsection{I/O 附加关键字（可选）}
\kw{TSTEP}/\kw{TSTOP} 瞬态步长与停止时间；\kw{OP} decap dump 时间；\kw{tranXX} 开关窗口（向量行末优先级更高）；\kw{ioprobe <VDD> <+|-> <VSS> <-|+>} 探测极性。

\begin{noteBox}
I/O 单元仅考虑一个代表性样本。最精确：\texttt{sim2iprof}+ACE；更快：AVM。
\end{noteBox}

\section{存储器与 IP 表征}
\subsection*{Memory and IP Characterization}

\begin{itemize}
  \item \textbf{精确：}\texttt{sim2iprof}（开关电流）+ ACE（ESR、电容、漏电流）
  \item \textbf{快速：}AVM 数据手册表征（三角/梯形电流、ESR、电容、漏电流）
\end{itemize}

\subsection{Sim2iprof 开关电流表征}
见附录 E「sim2iprof」。

\subsection{ACE Decap 与 ESR 表征}
ACE 用追踪算法找 P/G 网络，Spice 表征 MOSFET 栅电容，输出 APL 格式电容、ESR、漏电流；可用 DSPF（\texttt{*|NET}、\texttt{*|I}）追踪 R。大单元（约 50 万 MOSFET）Linux 上约 1 分钟。

\paragraph{Tied-off 器件识别为 decap}
\begin{itemize}
  \item NMOS：源/栅接地、漏接电源；或漏/栅接地、源接电源
  \item PMOS：源/栅接电源、漏接地；或漏/栅接电源、源接地
  \item 接信号：电流置零，不作 decap
\end{itemize}

\paragraph{ACE 配置文件}
\textbf{必需：}\kw{External_power_net}、\kw{External_ground_net}、\kw{Subckt}、\kw{Modelfile}（或 \kw{Include}）、\kw{VddValue}。

\textbf{主要可选：}\kw{Ace_HSpice}/\kw{Ace_Eldo}/\kw{Ace_Spectre}；\kw{ACE_OPTION}；\kw{DECAP_SUBCKT}；\kw{Internal_Power_Net}/\kw{VP_PAIRING}；\kw{K_GROUND_CAP}/\kw{K_FLOAT_CAP}（默认 0.5）；\kw{Leakage_i}（\texttt{-pwc} 必需）；\kw{METAL_RESISTOR}/\kw{METAL_RESISTOR_FILE}；\kw{MOS_Report}；\kw{NOMINAL_VDD}；\kw{NMOS/PMOS_Model_Name}；\kw{Primary_Power_Net}/\kw{Primary_Ground_Net}；\kw{SIGCAP_FACTOR}；\kw{SIGNAL_PARASITIC_C}；\kw{SweepValue}（\texttt{-pwc}，默认 11 点 10\%--110\% Vdd）；\kw{Switch_Subckt}；\kw{Temperature}；\kw{TOGGLE_RATE_ASSIGNMENT}；\kw{VP_Mapping}；\kw{VTH_FACTOR}；\kw{WRAPSUB}；\kw{XMOS_INST_PARAM}；\kw{FLIP_WELL}；\kw{FINFET_UNIT_WIDTH} 等。

\begin{lstlisting}
ace [-d] [-o <output_file>] [-toggle_rate <On_fraction>] [-pwc] <cellname>.smin
\end{lstlisting}
输出：\texttt{<cell>.mcap}、\texttt{<cell>.ace.mmx}、\texttt{<cell>.ace.decap}。

\subsection{AVM 数据手册表征}
无存储器 APL 时 RedHawk 可生成 \texttt{adsRpt/avm.conf}。\kw{LIB2AVM}：0 关；1 双三角；2 梯形；3/4 负载相关三角/梯形。

\begin{lstlisting}
lib2avm <lib2avm_config_filename> -l <cell_list>
avm <avm_configuration_file>
\end{lstlisting}

配置示例：
\begin{lstlisting}
Cell1 {
    MEMORY_TYPE RegFile
    EQUIV_GATE_COUNT 6663
    Cload 2f
    VDD_PIN VDDPR VDDP
    GND_PIN VSS
    C_decap { VDDPR VSS 11.002f ... }
    VDD 1.08 1.08 { ck2q_delay 1537p; tr_q 30.194p; Cpd_read {...} }
}
\end{lstlisting}

关键字段：\kw{CHARACTERIZATION_MODE}（\texttt{accurate}/\texttt{ultra\_accurate}/\texttt{PWL}）；\kw{PROCESS}；\kw{C_decap}/\kw{Cpd_read|write|standby}；\kw{Peak_I_*}、\kw{CHARGE_RATIO}（默认 0.7）；\kw{DATAVERSION}；多状态 \kw{CUSTOM_STATE_FILE}、\kw{STATE_BOOLEAN}。

输出：\texttt{vmemory.current}、\texttt{vmemory.cdev}；\texttt{avm.log}/\texttt{avm.warning}/\texttt{avm.error}。

\section{APL 问题排查}
\subsection*{Troubleshooting APL Problems}

\subsection{检查配置文件}
\begin{itemize}
  \item 必需关键字、Vdd 与 GSR、温度与 .lib/Tech 一致？
  \item Vdd/Gnd pin 名与 Spice 一致？尺寸单位：非 $\mu$m 时设 \kw{SIZE_SCALE}（如 \texttt{1e-6}）。
\end{itemize}

\subsection{常见问题}
\begin{itemize}
  \item \texttt{.apache/adsLib.output} 缺向量——LIB 缺 function/state table
  \item Spice 网表/模型缺失、参数/scale/不支持 card
  \item tie-off、天线二极管误表征；decap 未用 \texttt{-p}；复杂单元缺向量
  \item 向量未引起输出边沿；\kw{TMP_DIR} 磁盘不足；\texttt{DEBUG 1}、\texttt{-v}、\texttt{-d} 查 \texttt{.apache/APL/<cell>.sp}
  \item NSpice 孤立节点：\kw{OPTION} \texttt{gshunt=1e-9}
\end{itemize}

\section{APL 配置文件示例}
\subsection*{Sample APL Configuration File}

\begin{lstlisting}
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
VDD_PIN_NAME VDD
GND_PIN_NAME GND1
TMP_DIR /nfs/apl1/apldi_test/temp
\end{lstlisting}
"""


def build_ch09() -> str:
    head = CH09.read_text(encoding="utf-8")
    cut_markers = [
        "\\subsubsection{仅库 APL（DI）必需关键字}",
        "\\subsubsection{仅库 APL（DI）必需关键字——详述}",
    ]
    idx = -1
    for m in cut_markers:
        i = head.find(m)
        if i >= 0:
            idx = i if idx < 0 else min(idx, i)
    if idx < 0:
        raise SystemExit("ch09 anchor not found")
    prefix = head[:idx].rstrip()
    body = (
        gen_ch09_di_required_expand()
        + "\n"
        + gen_ch09_optional_keywords()
        + "\n"
        + gen_ch09_parallel_keywords()
        + "\n"
        + gen_ch09_vectors()
        + "\n"
        + gen_ch09_rest()
    )
    return prefix + body


def gen_ch16_clamp_expand() -> str:
    return r"""
\subsubsection{Clamp 文件示例}
IO 单元 clamp 示例：
\begin{lstlisting}
BEGIN_CLAMP_CELL
    NAME IO_cell
    PIN PAD 7.29 362.14 METAL1 pad_1
    PIN VSS 7.39 362.04 METAL2 vss_1
    PIN VDD 7.29 363.66 METAL1 vdd_1
    RON 0.01
    ESD_PIN_PAIR pad_1 vss_1 0.001 0.05
    ESD_PIN_PAIR vdd_1 vss_1 0.02 OFF
END_CLAMP_CELL
\end{lstlisting}

MMX 晶体管级 clamp：
\begin{lstlisting}
BEGIN_CLAMP_CELL
NAME IO
XTOR mos1__2:VDD 2.24 328.14 BOTTOM
XTOR mos1__2:VSS 2.34 328.14 BOTTOM
ESD_PIN_PAIR mos1__2:VDD mos1__2:VSS diode
END_CLAMP_CELL

BEGIN_CLAMP_IV
  NAME diode
  RON 0.1 100K
  VT1 0.4
  ROFF 100K
END_CLAMP_IV

BEGIN_CLAMP_IV
  NAME sback
  RON 0.3 0.2
  VT1 1.2 1.5
  VH 0.1 0.15
END_CLAMP_IV
\end{lstlisting}

默认：\texttt{VH = VT1}；未指定 \texttt{RON-} 等则取正向默认值。TLP 文件逗号/空格/制表符分隔；\texttt{\#} 为注释。

\paragraph{CLAMP\_CELL 关键字详述}
\begin{description}[leftmargin=2.8cm,style=nextline]
\item[\kw{NAME}] 单元或 I-V 设备标识字符串。
\item[\kw{TYPE}] 用户定义的 clamp 类型名，供 \kw{FROM_CLAMP_TYPE}/\kw{TO_CLAMP_TYPE} 筛选。
\item[\kw{PIN}] 以 pin 名、坐标 \texttt{<x> <y>}、\kw{BOTTOM}/\kw{TOP}/层名、\kw{locID} 指定连接点。占位符仅用 ``\texttt{-}''，勿用 ``\texttt{NA}''。仅 pin 名时默认选近最小电阻到 pad 的节点；未指定时每域自动选一个近最小电阻 pin。
\item[\kw{XTOR}] MMX 块晶体管连接，语法同 \kw{PIN}，另加 \texttt{:<net>} 表示晶体管所接网络。
\item[\kw{RON}] 导通电阻（默认 0.0001\,$\Omega$）；\kw{RON+}/\kw{RON-} 为正/反向电流电阻。
\item[\kw{OFF}] 该 zapping 极性方向开路；pin 对两向均为 \kw{OFF} 为语法错误。
\item[\kw{ESD_PIN_PAIR}] 合法 B2B 放电路径及双向电阻；可写对称 \kw{RON}、非对称 \kw{RON+}/\kw{RON-}、\kw{OFF} 或引用 \kw{BEGIN_CLAMP_IV} 名称。
\item[\kw{IMAX}/\kw{VMAX}] 击穿检查电流/电压阈值；优先级：clamp I-V 规则 $>$ clamp cell 规则 $>$ ESD 规则。
\end{description}

\paragraph{CLAMP\_IV 参数说明}
\begin{itemize}
  \item \kw{ROFF}：关断电阻（默认 1e6\,$\Omega$）；\kw{ROFF+}/\kw{ROFF-} 正/反向
  \item \kw{VT1}：导通阈值（默认 0，即线性 RON 模型）
  \item \kw{VH}：保持电压（默认 VH=VT1；范围 $0 \le \mathrm{VH} \le \mathrm{VT1}$）
  \item \kw{ION2}/\kw{RON2}/\kw{IT2}/\kw{RT2}/\kw{VT2}：高导通区与击穿区建模
  \item \kw{TLP_FILE}、\kw{TLP_I_RESOLUTION}：TLP 曲线（典型分辨率 0--0.001）
\end{itemize}

加密后 \texttt{adsRpt/ESD/ClampInfo.rpt} 显示 \texttt{\# Encrypted}。

\begin{seeAlsoBox}
Clamp 连接与建模详见 GSR \kw{ESD_CLAMP_PIN_FILE}（附录 C）与 Tcl \kw{pfs}（附录 D）。
\end{seeAlsoBox}
"""


def gen_ch16_resistance_rules() -> str:
    return r"""
\subsection{B2B 电阻检查详述}
\subsubsection*{Bump-to-Bump (B2B) Details}

对每个 bump 对，PF-S 计算每条 bump$\rightarrow$clamp$\rightarrow$bump 路径的 \kw{LOOP_R}。超过阈值的环路中 clamp 视为无效，不参与后续 \kw{PARALLEL_R} 并行等效电阻计算。支持多级 bump 路径（\kw{ESD_STAGE}、\kw{B2B_LOOP_LENGTH}）。

\subsection{电阻规则文件关键字}
\begin{longtable}{@{}p{0.32\textwidth}p{0.63\textwidth}@{}}
\toprule
\textbf{关键字} & \textbf{说明} \\
\midrule
\endhead
\kw{TYPE} & \texttt{BUMP2BUMP|BUMP2CLAMP|CLAMP2CLAMP|PIN2CLAMP|PIN2PIN|BUMP2INSTANCE|CLAMP2INST|CLAMP2MACRO} \\
\kw{NAME} & 用户规则名 \\
\kw{ARC_R} & B2C/C2C/C2I/C2M 弧电阻阈值（$\Omega$） \\
\kw{LOOP_R} & B2B 单路径环路电阻阈值 \\
\kw{PARALLEL_R} & B2B 并行等效电阻；未指定时以最小 LOOP\_R 为通过准则 \\
\kw{ESD_STAGE} & 多级 B2B 级数范围（max $\le 5$，\kw{MAX_ESD_STAGE} 可覆盖） \\
\kw{PACKAGE [0|1]} & 是否含封装电阻 \\
\kw{PACKAGE_PIN [0|1]} & P2C/P2P 以封装 pin 为端点 \\
\kw{PAD_FILE} & PLOC/pcell bump 列表 \\
\kw{BUMP_LIST} & 限定 bump 集合 \\
\kw{NET_PAIR} & 网表对 \\
\kw{USE_CLAMP_CELL/INST/FILE} & 限定参与 clamp \\
\kw{B2B_LOOP_LENGTH} & 各级 clamp 数量 \\
\kw{RADIUS} & C2C/B2C CD 选择半径（$\mu$m） \\
\kw{SHORT_BUMP_IN_NET} & 短接同网 bump（封装低阻路径） \\
\kw{SHORT_BUMP_IN_NET_GROUP} & 按 POWER/GROUND/SIGNAL 短接 \\
\kw{CLAMP_POS_PIN}/\kw{CLAMP_NEG_PIN} & B2C 分别测 HBM 二极管阳/阴极 \\
\kw{INST_FILE}/\kw{CELL_FILE} & C2I/C2M/B2I 实例或单元列表 \\
\kw{SAMPLE_POINT} & C2M 采样点（BOTTOM/TOP/层） \\
\kw{TRANSISTOR_PIN} & MMX 晶体管 pin 模式 \\
\kw{RES_RATIO} & B2I 电阻比阈值 \\
\kw{SAMPLE_MODE} & \texttt{UNIFORM|RES_BY_AREA} \\
\kw{B2I_MACRO_MODE} & 宏单元 B2I 模式 \\
\kw{B2C_NAME} & B2I 引用的 B2C 规则名 \\
\kw{CHECK_CONNECTION 1} & 输出 \texttt{esd_info.rpt}（未保护实例等） \\
\kw{SAVE_CLAMP_DB}/\kw{LOAD_CLAMP_DB} & 保存/加载 clamp DB（仅一生效） \\
\kw{ESD_GSR 1} & 生成精简 \texttt{esdGsr.gsr} \\
\bottomrule
\end{longtable}

\subsection{电阻报告示例}
\texttt{perform clampcheck -o instConn.txt -instConn} 输出未连接 clamp：
\begin{lstlisting}
######## List of Unconnected Clamp Instances ########
# <CELL NAME>:
#     <PIN_NAME> <X> <Y> <LAYER> <LOCID> <INSTANCE_NAME>
inst_ndiode_0:
VDDO 1.07374e+06 1.07374e+06 metal1 VDDO inst_ndiode_0/adsU4
\end{lstlisting}

\texttt{-isolatedBump} 报告与 clamp 隔离的 bump。B2B 报告含 bump 对、\kw{LOOP_R}、\kw{PARALLEL_R}、clamp locID。

\subsection{GUI 查看电阻结果}
View $\rightarrow$ ESD Resistance Lists / Maps：
\begin{itemize}
  \item List of Bump-to-Clamp、Clamp-To-Clamp（按网表/实例过滤）
  \item Bump to Bump Resistance：绿/红表示是否参与通过 B2B 路径
  \item List of Bump-to-Bump Para：最差 \kw{PARALLEL_R}
  \item F-Line：环路飞线；Loop\_R 列表；SPT 最小电阻路径
  \item C2I 超限飞线与最差路径；Analysis Histogram
\end{itemize}

\figplaceholder{Figure 16-9}{按网表/实例名的电阻检查}
\figplaceholder{Figure 16-10}{Bump-to-bump 电阻显示}
\figplaceholder{Figure 16-12}{F-line 环路 R 路径}
\figplaceholder{Figure 16-14}{最小电阻路径}
\figplaceholder{Figure 16-19}{直方图对话框}
"""


def gen_ch16_cd_rules() -> str:
    return r"""
\subsection{模式 1 电流密度规则关键字详述}
除前文示例外，\kw{TYPE CURRENT_DENSITY}（或 \kw{DC}/\kw{CD}）支持：

\begin{longtable}{@{}p{0.34\textwidth}p{0.61\textwidth}@{}}
\toprule
\textbf{关键字} & \textbf{说明} \\
\midrule
\endhead
\kw{B2B_RULE_NAME} & 复用已有 B2B 结果加速非线性 clamp CD \\
\kw{BUMP_PAIR}/\kw{PIN_PAIR} & 放电端点对；首 bump 接 zapping 正极 \\
\kw{BUMP_PAIR_FILE} & bump 对列表文件 \\
\kw{PIN_PAIR_VTH} & 差分电压超过阈值写入 \texttt{esd_pinPair.rpt} \\
\kw{SHOTGUN_MODE} & 多网联合弧分析，缩短 I/O 到 clamp 的 CD 时间 \\
\kw{CDM_ALL_NET} & 对所有经 clamp 连接的域充电（CDM） \\
\kw{NET_PAIR_DOMAIN} & \texttt{SAME|DIFF} 同域/跨域违例报告 \\
\kw{FROM_NET}/\kw{TO_NET}/\kw{TERMINAL_NET} & 网表级 from/to/终端 \\
\kw{*_NET_GROUP} & Power/Ground/Signal 组 \\
\kw{JEDEC_MODE} & \texttt{BIDIR|POS|NEG}，可选 \texttt{OPEN} \\
\kw{ZAP_VOLTAGE}/\kw{ZAP_R}/\kw{ZAP_CURRENT} & zapping 源；电流模式忽略电压/电阻 \\
\kw{ZAP_*_RANGE} & 多电平扫描，摘要写入 \texttt{esd_summary.rpt} \\
\kw{ZAP_FROM}/\kw{ZAP_TO} & 命名坐标点 \\
\kw{EXTEND_CLAMP_CONN 1} & 经 power rail 并联放电；同网 clamp 两端 \\
\kw{IGNORE_EM_IN_CLAMP} & DC 中忽略 clamp 内 EM（默认 0） \\
\kw{EM_SCALE}/\kw{EM_RULE_SET} & EM 电流缩放与规则集 \\
\kw{NET_PAIR_VTH}/\kw{PEAK_VOLT}/\kw{DIFF_VOLT} & 驱动-接收与峰值/差分电压 \\
\kw{CLAMP_IMAX}/\kw{CLAMP_VMAX} & 击穿阈值（I-V 规则优先） \\
\kw{SHORT_CLAMP_NODE} & 计算电阻时短接 clamp 节点 \\
\kw{CACHE_EM} & 0/1/2/3：EM 缓存加速（2 显著加速；3 存 DB） \\
\kw{EM/REFF/I/V_THRESHOLD} & 保存 DB 的阈值 \\
\kw{SAVE_CLAMP_FAIL}/\kw{SAVE_EM} & 条件保存 DB；\texttt{import esdcd} 重载 EM \\
\kw{EXCEL}/\kw{EXCEL_REPORT} & 生成 \texttt{esd_excel.rpt} \\
\bottomrule
\end{longtable}

仅指定 \kw{ESD_STAGE} 时不计算 B2B 电阻以省时；若指定 \kw{LOOP_R} 或 \kw{PARALLEL_R} 则计算。

\subsection{模式 2：指定 clamp 路径}
\begin{lstlisting}
CLAMP_INST_PIN <instance> <locID1> <locID2>
USE_CLAMP_FILE <file>
# 文件中 USE_CLAMP_CELL / USE_CLAMP_INST（支持通配符）
\end{lstlisting}

\subsection{弧基电流密度关键字}
\kw{ZAP_BUMP_CLAMP}、\kw{ZAP_CLAMP_BUMP}、\kw{ZAP_CLAMP_CLAMP}、\kw{ZAP_PIN_CLAMP}、\kw{ZAP_CLAMP_PIN}；

网表内：\kw{ZAP_B2C_NET}、\kw{ZAP_C2B_NET}、\kw{ZAP_C2C_NET}、\kw{ZAP_P2C_NET}、\kw{ZAP_C2P_NET} 及 \kw{*_NET_GROUP}。

\kw{FROM_CLAMP_TYPE}/\kw{TO_CLAMP_TYPE}、\kw{SAME_CLAMP_TYPE}、\kw{DIFF_CLAMP_TYPE}；

\kw{TIE_CLAMP <method> ?m?}：\texttt{PARALLEL|INST|MIN_DIST}，多指并联二极管。

\kw{FROM_TO_SELECT}：\texttt{FROM_MIN_DIST|FROM_MIN_RES|TO_MIN_DIST|TO_MIN_RES} 与数量。

\kw{USE_CLAMP_IV 1} 或按 CELL/INST/TYPE 含 clamp 电阻。

点到点：
\begin{lstlisting}
perform esdcheck
    -from {<x> <y> <layer> <net>} -to {...}
    ? -zapI <I> | -zapV <V> -zapR <R> ?
    -ruleName <name> ? -clamp <file> ?
\end{lstlisting}
多个 \texttt{-from}/\texttt{-to} 可短接后接 zapping 源（须同网物理连通）。
"""


def gen_ch16_rule_types_detail() -> str:
    return r"""
\subsection{各类电阻检查说明}
\subsubsection*{B2C、B2I、C2C、C2I、C2M 与 D2R}

\textbf{Bump-to-Clamp（B2C）}：计算 pad 到 clamp 有效电阻并与 \kw{ARC_R} 比较。pad 与 clamp 连接点可手工指定或由工具自动选取（默认倾向有效电阻最大点）。\kw{CLAMP_POS_PIN 1} 仅测 HBM 二极管阳极；\kw{CLAMP_NEG_PIN 1} 仅测阴极。

\textbf{Bump-to-Instance（B2I）}：对每个 bump，比较到实例电阻与到保护 clamp（最小 B2C 电阻）的电阻；若存在更小实例路径则失败。

\textbf{Clamp-to-Clamp（C2C）}：报告任意两 clamp 间有效电阻，与 \kw{ARC_R} 比较。

\textbf{Clamp-to-Inst（C2I）}：核心实例到 clamp 的 CDM 风险检查。须提供实例列表；标准单元选\textbf{最小}有效电阻点，宏单元选\textbf{最大}有效电阻点（宏面积大，最坏点更保守）。同时报告 \kw{LOOP_R} 与 \kw{ARC_R} 通过/失败。

\textbf{Clamp-to-Macro（C2M）}：与 C2I 类似，但在 LEF pin 几何的 bottom/top/指定层上选\textbf{多个}最小电阻节点以提高覆盖；仅报告 \kw{ARC_R}。

\textbf{跨域 D2R-to-Bump}：检查跨电压域驱动-接收实例对的 P/G pin 到各 bump 的电阻差或比值（经 clamp 间接连接 포함）。

\subsection{封装电阻与 3D-IC}
\subsubsection*{Package and 3D-IC Inputs}

封装子电路显著影响 ESD 路径：电感短接、互感开路、电容开路。GSR \kw{PACKAGE_SPICE_SUBCKT} 引入封装后，电阻从 BGA 经封装、bump、P/G 网络、clamp 再回到 VSS/BGA。

封装相关规则：
\begin{itemize}
  \item \kw{PIN2CLAMP}（P2C）：封装 pin 到 clamp，类似 B2C
  \item \kw{PIN2PIN}（P2P）：封装 pin 间，类似 B2B（含多级）
  \item P2C/P2P/P2PM 必须以封装 pin 为端点；其他规则默认不含封装（\kw{PACKAGE 0}）
\end{itemize}

\textbf{3D-IC 关键字：}
\begin{itemize}
  \item \kw{FROM_DIE}/\kw{TO_DIE}：zapping 源高/低端所在 die
  \item \kw{DIE_NAME}：仅分析指定 die；clamp 中可标注 \kw{DIE_NAME}
  \item \kw{BEGIN_DIE}/\kw{END_DIE}：按 die 组织 clamp 列表
\end{itemize}

\subsection{perform esdcheck 命令选项详述}
\begin{lstlisting}
perform esdcheck
    -rule {<file1> <file2> ...}
    -clamp {<file1> <file2> ...}
    ? -thread <num_threads> ?
    ? -optimize <mode>? ? -detail ? ? -append ?
    ? -outDir <results_dir> ? ? -ignoreError ?
    ? -saveDBDir <path> ? ? -jobCount <num_jobs> ?
    ? -collate ? ? -jobFile <job_defin_file> ?
    ? -progress <timeInterval> ?
    ? -noCompress ?
    ? -slaveOnly | -hostOnly ?
\end{lstlisting}

\begin{itemize}
  \item \texttt{-thread}：线程数（默认 2）
  \item \texttt{-optimize}：0 全关；1 基本优化（约 2$\times$）；2 激进优化（默认，最高约 20$\times$）；3 对 C2I/C2M/B2I 额外优化
  \item \texttt{-detail}：B2B/多级检查含坐标、层、单元名
  \item \texttt{-ignoreError}：单条规则出错仍继续其余规则
  \item \texttt{-saveDBDir}：保存 DB 供同事务重载
  \item \texttt{-jobCount}：多进程；建议先 \texttt{-setupClamp}
  \item \texttt{-collate}：合并多作业文本报告到 \texttt{-outDir}
  \item \texttt{-progress}：写 \texttt{esd\_progress.rpt}（小时为单位）
  \item \texttt{export esdcheck}/\texttt{import esdcheck}：导出/导入 DB
  \item \texttt{report esdcheck}：生成文本报告
  \item DMP：\texttt{-slaveOnly} 仅 worker；\texttt{-hostOnly} master+worker
\end{itemize}

\paragraph{作业分配文件}
\begin{lstlisting}
BEGIN_ESD_JOB
    NAME Job1
    WORK_DIR ./adsESD1
    RULE CD my_cd_rule 50.0
    RULE_COUNT C2I core_rule 100
    EXCLUDE_RULE B2B slow_b2b
    CLAMP clamp_file.txt
END_ESD_JOB
\end{lstlisting}
\texttt{RULE <percent>} 与 \texttt{RULE_COUNT <arcCount>} 可拆分 CD/R 规则的 from/to 弧；\texttt{arcCount} 优先于 \texttt{percent}。未分配规则由 PF-S 自动均衡到各 job。

\subsection{C2I/C2M/B2I 规则示例}
C2I：
\begin{lstlisting}
BEGIN_ESD_RULE
    NAME core_usage_1
    TYPE C2I
    INST_FILE inst.list
    ARC_R 2.3
    LOOP_R 4
END_ESD_RULE
\end{lstlisting}

C2M（含层与晶体管 pin）：
\begin{lstlisting}
BEGIN_ESD_RULE
    NAME macro_c2m
    TYPE C2M
    INST_FILE macro.list
    ARC_R 5.0
    LAYER BOTTOM
    SAMPLE_POINT 4
    TRANSISTOR_PIN 1
END_ESD_RULE
\end{lstlisting}

B2I：
\begin{lstlisting}
BEGIN_ESD_RULE
    NAME esd_b2i_rule
    TYPE B2I
    B2C_NAME esd_b2c_rule
    INST_FILE inst.list
    RES_RATIO 1.2
    B2I_REPORT_PARTIAL_PASS 1
END_ESD_RULE
report esdcheck -type b2i -name esd_b2i_rule -b2cName esd_b2c_rule
\end{lstlisting}

\subsection{电阻检查 GUI 与工具}
Tools $\rightarrow$ Path Finder S $\rightarrow$ ESD Resistance Check 启动电阻检查对话框（图~\ref{fig:esd-gui-res}）。

\figplaceholder{Figure 16-5}{ESD 电阻检查对话框}

\texttt{perform res\_calc} 约束文件 \kw{IP_RESISTANCE} 示例：
\begin{lstlisting}
# CELL CONSTRAINT: <cell> <Pin> <Res_Constr> ?<x> <y> ?<layer>?
CHECKBUMP 5
INSTANCE inst_129422/inst_7768 VSS 3.0
\end{lstlisting}
输出默认 \texttt{adsRpt/<design\_name>.res\_calc}，含 PASS/FAIL 与最远 bump 列表。
"""


def gen_ch16_hbm_intro() -> str:
    return r"""
\paragraph{HBM、MM 与 CDM 测试背景}
\textbf{HBM}：带电人体（约 100\,pF、1.5\,k$\Omega$）接触器件引脚，放电经保护网络到参考地，用于模拟生产/使用中的静电损伤。

\textbf{MM}：测试设备（低阻抗、小电容）向器件放电，上升时间更短、峰值更高，检验快速 ESD 脉冲下的保护能力。

\textbf{CDM}：器件在组装中积累电荷，经接地 pin 对地放电；对大宏单元与 I/O 尤其重要，PathFinder 的 C2I/C2M 规则针对此类失效机制。

传统流片前审查难以覆盖全芯片所有放电路径；PF-S 在 clamp 导通假设下计算静态电阻，并结合电流密度检查评估 IR 与 EM，作为动态仿真的互补 sign-off 手段。
"""


def gen_ch16_cd_reports_detail() -> str:
    return r"""
\subsection{CD 规则文件完整模板}
\begin{lstlisting}
BEGIN_ESD_RULE
    NAME mydc
    TYPE CURRENT_DENSITY
    LOOP_R 6.0
    ESD_STAGE 2
    B2B_RULE_NAME esd_b2b_rule
    BUMP_PAIR VSS1 VDD5
    ZAP_VOLTAGE 100
    ZAP_R 1000
    NET_PAIR_VTH 0.2 VDD VSS
    PEAK_VOLT 25.0
    DIFF_VOLT 7.0
    CACHE_EM 2
    SAVE_EM 1
    EXCEL 1
END_ESD_RULE
\end{lstlisting}

\subsection{报告文件说明}
执行 \texttt{perform esdcheck} 后（默认 \texttt{adsRpt/ESD/}）：
\begin{itemize}
  \item \texttt{esd\_fail.rpt}/\texttt{esd\_pass.rpt}：失败/通过路径明细
  \item \texttt{esd\_summary.rpt}：摘要；含 zapping 源、等效电阻、clamp 电流
  \item \texttt{esd\_info.rpt}：连接性、采样点、作业分配（\kw{CHECK_CONNECTION}）
  \item \texttt{esd\_inst.rpt}：clamp 实例 IR
  \item \texttt{esd\_em.rpt}：路径 EM 百分比；\kw{EM_BY_LIMIT_ONLY 1} 过滤低百分比
  \item \texttt{esd\_pad.rpt}：pad 电流列表
  \item \texttt{esd\_pinPair.rpt}：\kw{PIN_PAIR_VTH} 超限 pin 对
  \item \texttt{esd\_excel.rpt}：Excel 汇总（\kw{EXCEL 1}）
\end{itemize}

\texttt{report esdcheck -type B2C -name abc* -glob -detail -excel} 支持通配符与按单元过滤。\texttt{-failedOnly} 仅失败项。\texttt{-summary} 主要为 CD 摘要。

\subsection{导入/导出 CD 数据库}
\begin{lstlisting}
import esdcd RuleABC
export esdcd -rule RuleABC -outDir ./esd_db
\end{lstlisting}
默认压缩 DB；\texttt{-noCompress} 或规则 \kw{COMPRESS_DB 0} 关闭。阈值 \kw{EM_THRESHOLD}、\kw{REFF_THRESHOLD}、\kw{I_THRESHOLD}、\kw{V_THRESHOLD} 控制哪些结果写入 DB。

\subsection{GUI 电流密度彩图}
View $\rightarrow$ ESD Current Density $\rightarrow$ Current Density Test List 列出已完成 CD 规则。

\begin{itemize}
  \item \textbf{Peak Voltage Map}：各节点峰值电压；可 on-the-fly 改阈值重绘
  \item \textbf{Differential Voltage Map}：差分电压分布
  \item \textbf{Current Map}：金属/Via 电流密度
  \item \textbf{Wire \& Via Voltage Map}：线/过孔电压；点选可在 Log 窗口看详细值
  \item \textbf{Electromigration Map}：EM 百分比色阶；配合 \texttt{get em} 查询
  \item \textbf{Pad Current Map}：pad 注入电流
\end{itemize}

色阶范围可通过各图 ``Set Color Range'' 配置。失败路径可用 SPT 追踪最小电阻路由辅助 debug。
"""


def gen_ch16_extra() -> str:
    return r"""
\subsection{perform clampcheck 选项补充}
\begin{itemize}
  \item \texttt{-cell}/\texttt{-celltype}：按单元名或 clamp 类型过滤报告
  \item \texttt{-inst}：指定 clamp 实例
  \item \texttt{-volt}：列出连接到某节点电压的 clamp
  \item \texttt{-net}：列出连接到指定网络（双向）的 clamp 节点
  \item \texttt{-bumpConn}/\texttt{-allBumpConn}：bump 到 clamp 连通性
  \item \texttt{-loop}：列出查询网表对的全部 B2B 环路 clamp 实例
  \item \texttt{-b2bLoopLength}：与 \texttt{-loopLength} 类似，专用于 B2B 精确级数
  \item \texttt{-append}：追加到已有输出文件
\end{itemize}

\subsection{perform esdcheck 高级选项}
\texttt{-addNode}：在指定坐标创建节点以提高电阻精度（配合 \texttt{-from}/\texttt{-to} 点查）。

\texttt{-name}/\texttt{-type}：仅运行规则文件中匹配名称/类型的规则。

\texttt{-excel}：生成 \texttt{esd\_excel.rpt} 汇总电阻与 CD 结果。

\texttt{-hostOnly}/\texttt{-slaveOnly}：DMP 流程下控制 master/worker 执行范围。

\texttt{export esdcheck -outDir <dir>}：导出 DB 供 \texttt{import esdcheck} 在其他会话加载（须首条 Tcl 为 \texttt{setup analysis\_mode esd}）。

\subsection{Bump-Clamp 与 Clamp-Clamp 电流密度检查}
\subsubsection*{Bump-to-Clamp and Clamp-to-Clamp Current Density Checking}

除 B2B 经 clamp 放电外，PF-S 支持弧基 CD：bump$\rightarrow$clamp、clamp$\rightarrow$bump、clamp$\rightarrow$clamp、pin$\rightarrow$clamp 等。网表级 \kw{ZAP_*_NET} 与 \kw{ZAP_*_NET_GROUP} 可对 POWER/GROUND/SIGNAL 全网表自动配对 zapping。

\kw{RADIUS} 限制 C2C/B2C 所选 clamp 距离；\kw{SAME_CLAMP_TYPE}/\kw{DIFF_CLAMP_TYPE} 控制同类型或异类型 clamp 间检查。

\figplaceholder{Figure 16-21}{ESD 彩图菜单}
\figplaceholder{Figure 16-22}{峰值与差分电流密度图}
\figplaceholder{Figure 16-23}{电流密度检查结果}
\figplaceholder{Figure 16-24}{线/过孔电压 ESD 结果}
\figplaceholder{Figure 16-25}{EM 检查结果}

\subsection{B2B/B2C/C2C 规则文件示例}
\begin{lstlisting}
BEGIN_ESD_RULE
    NAME esd_b2b_rule
    TYPE BUMP2BUMP
    LOOP_R 5.0
    PARALLEL_R 2.0
    ESD_STAGE 1 3
    B2B_LOOP_LENGTH 1 2
    PAD_FILE design.ploc
    SHORT_BUMP_IN_NET VSS
    USE_CLAMP_FILE clamp_cells.txt
END_ESD_RULE

BEGIN_ESD_RULE
    NAME esd_b2c_rule
    TYPE BUMP2CLAMP
    ARC_R 3.0
    CLAMP_POS_PIN 1
    NET_PAIR VDD VSS
END_ESD_RULE

BEGIN_ESD_RULE
    NAME esd_c2c_rule
    TYPE CLAMP2CLAMP
    ARC_R 1.5
    RADIUS 500
    SAME_CLAMP_TYPE 0
    DIFF_CLAMP_TYPE 1
END_ESD_RULE
\end{lstlisting}

\subsection{合并规则与 Clamp Pin 节点}
规则与 clamp pin 位置可合并为单一 \texttt{-rule} 文件。GSR \kw{ESD_CLAMP_FILES} 在指定 pin 坐标创建节点以提高弧电阻精度。Tcl \kw{pfs export clamp_pin} 可导出模板；\kw{pfs setup clamp} 与 \texttt{perform esdcheck -setupClamp} 配合缓存 DB。

\subsection{弧基 CD 规则示例}
\begin{lstlisting}
BEGIN_ESD_RULE
    NAME b2c_cd_rule
    TYPE CURRENT_DENSITY
    ZAP_BUMP_CLAMP VDD1 clamp_io_0 pad_1
    ZAP_VOLTAGE 50
    ZAP_R 1500
    FROM_CLAMP_TYPE io_clamp
    TO_CLAMP_TYPE pwr_clamp
    TIE_CLAMP PARALLEL 4
    FROM_TO_SELECT FROM_MIN_RES 3
    USE_CLAMP_IV 1
END_ESD_RULE

BEGIN_ESD_RULE
    NAME c2c_cd_sig
    TYPE CD
    ZAP_C2C_NET_GROUP SIGNAL
    ZAP_CURRENT 0.5
    CACHE_EM 2
END_ESD_RULE
\end{lstlisting}

\subsection{排除关键字补充说明}
除前述 \kw{EXCLUDE_*} 外，规则文件还支持：
\begin{itemize}
  \item \kw{EXCLUDE_PAD_FILE}：与 \kw{PAD_FILE} 配合排除部分 bump
  \item \kw{NO_SHORT_BUMP_IN_NET}：在 \kw{SHORT_BUMP_IN_NET_GROUP} 下排除特定网表
  \item \kw{EXCLUDE_RULE}：在 \texttt{BEGIN_ESD_JOB} 中排除整条规则
  \item 通配符：\kw{USE_CLAMP_CELL}/\kw{USE_CLAMP_INST} 名称支持 \texttt{*} 与正则（\texttt{report esdcheck -regexp}）
\end{itemize}

\subsection{电阻/电流密度报告片段}
B2B 失败路径示例（\texttt{esd\_fail.rpt}）：
\begin{lstlisting}
# BUMP2BUMP Rule: esd_b2b_rule
# Bump1 Bump2 LOOP_R PARALLEL_R Status
VDD1 VSS1 8.2 3.1 FAIL
# Clamp path: clamp_a/loc1 -> clamp_b/loc2
\end{lstlisting}

CD 摘要（\texttt{esd\_summary.rpt}）：
\begin{lstlisting}
# Rule: mydc  TYPE: CURRENT_DENSITY
# Zap: VDD5 -> VSS1  V=100V  R=1000Ohm  I=0.1A
# Clamp IR: clamp_12/locA 2.5V  clamp_34/locB 1.8V
# Worst EM: metal3_seg_44  112.3%
\end{lstlisting}

\subsection{GUI 菜单索引}
\textbf{File}：Import/Export ESD DB（导入已保存的 esdcheck 数据库）。

\textbf{Edit}：ESD Clamp ECO——GUI 增删改 clamp 单元/实例参数。

\textbf{View $\rightarrow$ ESD Resistance Lists}：Bump-to-Clamp、Clamp-to-Clamp、Bump-to-Bump Para、Loop\_R、C2I 失败列表；底部 SPT 按钮追踪最小电阻路径。

\textbf{View $\rightarrow$ ESD Resistance Maps}：电阻色图；可 on-the-fly 修改阈值并重绘。

\textbf{View $\rightarrow$ ESD Clamp Lists}：clamp 实例与 pin 对列表。

\textbf{View $\rightarrow$ ESD Current Density}：Peak/Diff Voltage、Current、Wire/Via Voltage、EM、Pad Current 彩图。

\textbf{Results $\rightarrow$ Analysis Histogram}：电阻或 EM 结果直方图统计。

\subsection{HBM/MM/CDM 与检查类型对照}
\begin{table}[htbp]
\centering
\caption{ESD 模型与 PathFinder 检查类型}
\small
\begin{tabular}{p{2cm}p{4.5cm}p{6.5cm}}
\toprule
\textbf{模型} & \textbf{典型失效} & \textbf{推荐 PF-S 规则} \\
\midrule
HBM & I/O 与电源 clamp 路径 & B2B、B2C、B2I、CD（zap 跨 VDD/VSS） \\
MM & 快速脉冲、多指二极管 & B2C、C2C、弧基 CD、\kw{TIE_CLAMP} \\
CDM & 宏单元/core 到 clamp & C2I、C2M、\kw{CDM_ALL_NET}、\kw{SHOTGUN_MODE} \\
\bottomrule
\end{tabular}
\end{table}

\subsection{PathFinder-D 与规则检查关系}
PathFinder-D 对 IP 级版图做 HBM/CDM/MM 瞬态仿真 sign-off；PF-S 规则检查覆盖全芯片单元级电阻与 CD，二者互补。模拟/混合信号 IP 另见 PathFinder 应用笔记（Totem 流程）。

\begin{seeAlsoBox}
GSR ESD 关键字（\kw{ESD_CLAMP_FILE}、\kw{ESD_RULE_FILE}、\kw{ESD_CLAMP_PIN_NODE_DISTANCE} 等）见附录 C；\texttt{perform esdcheck}、\texttt{perform clampcheck}、\texttt{pfs} 完整 Tcl 语法见附录 D。
\end{seeAlsoBox}
"""


def gen_ch16_exclusions() -> str:
    return r"""
\section{规则文件包含与排除}
\subsection*{General Rule File Inclusions and Exclusions}

电阻与电流密度规则均可指定包含/排除的 clamp、bump、实例或 pin。

\subsection{Clamp 元素排除}
\begin{lstlisting}
EXCLUDE_CLAMP <cellname>
EXCLUDE_CLAMP_INST <instance_name>
EXCLUDE_CLAMP_CELL_PIN <cellname> <loc_ID>
EXCLUDE_CLAMP_INST_PIN <instance_name> <loc_ID>
\end{lstlisting}

\subsection{Bump 排除}
\begin{lstlisting}
EXCLUDE_BUMP <bump_name>
EXCLUDE_BUMP_FILE <filename>
\end{lstlisting}

\subsection{实例与单元排除}
\begin{lstlisting}
EXCLUDE_INSTANCE <inst_name>
EXCLUDE_INSTANCE_FILE <filename>
EXCLUDE_CELL <cell_name>
EXCLUDE_CELL_FILE <filename>
\end{lstlisting}

\subsection{包含关键字（对照）}
\begin{lstlisting}
USE_CLAMP_CELL <cell> ?<locID1> <locID2>?
USE_CLAMP_INST <inst> ?<locID1> <locID2>?
USE_CLAMP_FILE <file>
BUMP_LIST { <bump1> ... }
INST_FILE <filename>
CELL_FILE <filename>
INCLUDE_NET_GROUP <groupName>
EXCLUDE_NET_GROUP <groupName>
\end{lstlisting}

\begin{noteBox}
低功耗分析模式（\texttt{setup analysis\_mode lowpower}）下 ESD 检查自动关闭。运行 ESD 前须 \texttt{setup analysis\_mode ESD}。大规模设计建议 \kw{ESD_GSR} 流程、\texttt{-jobCount}、\kw{CACHE_EM}、\texttt{-setupClamp} 提升吞吐。
\end{noteBox}

\subsection{快速参考：常用 Tcl 命令}
\begin{lstlisting}
setup analysis_mode ESD
perform esdcheck -clamp clamp.txt -setupClamp
perform esdcheck -rule rules.txt -thread 4 -optimize 2 -jobCount 4
perform clampcheck -instConn -isolatedBump -o topo.rpt
report esdcheck -type B2B -name esd_b2b_rule -detail
report esdcheck -type CD -name mydc -excel -failedOnly
import esdcd mydc
pfs export clamp_pin clamp_out.txt -esdCell clamp.txt
perform min_res_path -instance core_inst/foo -fromClamp
\end{lstlisting}
"""


def gen_ch16_topology() -> str:
    return r"""
\subsection{ESD 规则文件}
\subsubsection*{ESD Rules Files}

规则文件定义检查类型（\kw{BUMP2BUMP}、\kw{BUMP2CLAMP}、\kw{CLAMP2CLAMP}、\kw{PIN2CLAMP}、\kw{PIN2PIN}）、规则名、\kw{ARC_R}/\kw{LOOP_R}/\kw{PARALLEL_R} 限值、级数及包含/排除的 clamp、bump、网表。

\subsubsection{定义网表组}
\begin{lstlisting}
BEGIN_NET_GROUP
    NAME <userDefinedGroupName>
    NET <netName1>
    NET <netName2>
    ...
END_NET_GROUP
\end{lstlisting}

\subsection{缩小设计规模}
\subsubsection*{Reducing Design Size for Improved ESD Analysis}

\begin{enumerate}
  \item 原 GSR 加 \kw{ESD_CLAMP_FILE}、\kw{ESD_RULE_FILE}
  \item 规则文件加 \kw{ESD_GSR 1}
  \item 运行至 \texttt{setup design}，生成 \texttt{esdGsr.gsr}（\kw{IGNORE_CELLS}、移除 \kw{SPLIT_VIA_ARRAY}、\kw{DEF_IGNORE_SPECIFIC_LAYERS} 等）
  \item 用 \texttt{esdGsr.gsr} 替换原 GSR 重跑（可提速约 50\%）
\end{enumerate}

\section{Bump 与 Clamp 拓扑及连接检查}
\subsection*{Topology and Connectivity Checking of Bumps and Clamps}

\begin{lstlisting}
perform clampcheck ?-o <file>? ?-instConn?
    ? -isolatedBump? ?-cell <cell_name>? ?-celltype <type>?
    ? -inst <inst_name>? ? -volt <voltage>? ?-net <net_name>?
    ? -netConn <net1> <net2> ...? ? -allNetConn ?
    ? -bumpConn <bump_name> ? ? -allBumpConn ? ? -loop?
    ? -loopLength <stage_num>? ? -b2bLoopLength <stage_num>?
    ? -roff <R_thresh> ? ? -rptDisConn ?
    ? -rule <rule_file> ? ? -esdStage {min,max} | <stage_num>?
    ? -detail? ?-append?
\end{lstlisting}

主要选项：\texttt{-instConn} 未连接 clamp；\texttt{-isolatedBump} 与 clamp 隔离的 bump；\texttt{-netConn}/\texttt{-allNetConn} 网表对连通性；\texttt{-rptDisConn} 无 clamp 的网表对；\texttt{-esdStage} 级数范围；\texttt{-loopLength} 精确级数；\texttt{-roff} clamp 关断电阻阈值（默认 1e6\,$\Omega$）。

示例：\texttt{perform clampcheck -o instConn.txt -instConn}、\texttt{report clampcheck -rptDisConn -allNetConn}。

\section{Bump 与 Clamp 版图电阻检查}
\subsection*{Layout Resistance Checking of Bumps and Clamps}

\subsection{概述}
\subsubsection*{Overview}

PF-S 支持六类电阻检查（低功耗分析模式自动关闭 ESD）：
\begin{itemize}
  \item \textbf{B2B}（\kw{BUMP2BUMP}）：含多级
  \item \textbf{B2C}（\kw{BUMP2CLAMP}）
  \item \textbf{B2I}（\kw{BUMP2INSTANCE}）
  \item \textbf{C2C}（\kw{CLAMP2CLAMP}）
  \item \textbf{C2I}（\kw{CLAMP2INST}）
  \item \textbf{C2M}（\kw{CLAMP2MACRO}）
\end{itemize}

\subsection{数据流与输入}
\subsubsection*{Data Flow / Description of Inputs}

可在 RedHawk（LEF/DEF，亦支持 GDS）或 Totem（GDS + Spice）中运行（图~\ref{fig:esd-dataflow}）。

\figplaceholder{Figure 16-4}{PathFinder 数据流}

输入：Technology LEF、Apache tech 文件、PLOC 文件、ESD 规则与 clamp 定义、\texttt{setup analysis\_mode ESD}。

PLOC 示例：
\begin{lstlisting}
# pad location points
vdd1  6808  11091  metal7  POWER
vss1  7038  11612  metal7  GROUND
\end{lstlisting}

作业控制：\texttt{-thread} 多线程；\texttt{-jobCount} 多进程（建议先 \texttt{-setupClamp}）。
"""


def build_ch16() -> str:
    head = CH16.read_text(encoding="utf-8")
    anchor = "\\subsubsection{Clamp DB 创建}"
    idx = head.find(anchor)
    if idx < 0:
        raise SystemExit("ch16 anchor Clamp DB not found")
    prefix = head[:idx].rstrip()
    mid_end = head.find("\\subsection{ESD 规则文件}", idx)
    if mid_end < 0:
        mid_end = head.find("\\section{Bump 与 Clamp 拓扑", idx)
    mid = head[idx:mid_end] if mid_end > idx else head[idx:idx + 2500]
    body = (
        gen_ch16_clamp_expand()
        + "\n"
        + mid
        + "\n"
        + gen_ch16_topology()
        + gen_ch16_hbm_intro()
        + gen_ch16_rule_types_detail()
        + gen_ch16_resistance_rules()
        + r"""
\section{电流密度检查}
\subsection*{Current Density Checking}

PF-S 对用户指定 B2B、P2P、P2PM ESD 路径做电流密度分析，报告 IR 与 EM，GUI 显示图，支持 DC 路径分析与违例诊断。

\begin{itemize}
  \item \textbf{模式 1}：考虑所有 clamp 路径，迭代收敛确定 On/Off clamp 集合
  \item \textbf{模式 2}：指定 clamp 路径与 bump 对
\end{itemize}

命令：\texttt{perform esdcheck}（见上文选项详述）。

"""
        + gen_ch16_cd_rules()
        + r"""
\section{查看电流密度检查结果}
\subsection*{Viewing Current Density Checking Results}
"""
        + gen_ch16_cd_reports_detail()
        + gen_ch16_extra()
        + gen_ch16_exclusions()
    )
    return prefix + "\n" + body


def main() -> None:
    ch09 = build_ch09()
    ch16 = build_ch16()
    CH09.write_text(ch09, encoding="utf-8")
    CH16.write_text(ch16, encoding="utf-8")
    n09 = len(ch09.splitlines())
    n16 = len(ch16.splitlines())
    s09 = ch09.count("\\section{") + ch09.count("\\subsection{") + ch09.count("\\subsubsection{")
    s16 = ch16.count("\\section{") + ch16.count("\\subsection{") + ch16.count("\\subsubsection{")
    print(f"09_apl_char.tex: {n09} lines, {s09} section/subsection/subsubsection")
    print(f"16_pathfinder_esd.tex: {n16} lines, {s16} section/subsection/subsubsection")


if __name__ == "__main__":
    main()
