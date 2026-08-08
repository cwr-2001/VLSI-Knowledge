# -*- coding: utf-8 -*-
"""Generate 02_getting_started.tex with proper UTF-8 encoding."""
from pathlib import Path

chunks = []
chunks.append(
    r"""% 第 2 章 Getting Started
\bichapter{入门}{Getting Started}
\label{chap:start}

要开始用 PrimeTime 进行静态时序分析，请参阅：
\begin{itemize}
  \item 安装 PrimeTime 软件与许可证
  \item 配置 PrimeTime 工作环境
  \item 启动 PrimeTime 会话
  \item 许可证检出（License Checkouts）
  \item 输入 \cmd{pt\_shell} 命令
  \item 在命令行获取帮助
  \item PrimeTime 静态时序分析流程
  \item 在 PrimeTime 中使用 Tcl/Tk
  \item 用 TclPro Toolkit 检查与编译脚本
  \item 限制系统消息
  \item 保存与查看系统消息
  \item 结束 PrimeTime 会话
\end{itemize}

"""
)

chunks.append(
    r"""% ============================================================
\section{安装 PrimeTime 软件与许可证}
\subsection*{Installing the PrimeTime Software and Licenses}

使用 PrimeTime 之前，必须为站点安装软件与许可证。相关信息见：
\begin{itemize}
  \item \textit{Synopsys Installation Guide}：\url{http://www.synopsys.com/install}
  \item \textit{Synopsys Licensing Quickstart Guide}：\url{http://www.synopsys.com/licensing}
\end{itemize}

% ============================================================
\section{配置 PrimeTime 工作环境}
\subsection*{Configuring the PrimeTime Work Environment}

启动 PrimeTime 会话时，工具会执行 PrimeTime setup 文件中的命令。可在这些文件中初始化参数、设置变量、指定设计环境，并配置偏好的工作选项。

Setup 文件同名均为 \texttt{.synopsys\_pt.setup}，但位于不同目录。PrimeTime 按以下顺序从三个目录读取文件：
\begin{enumerate}
  \item Synopsys 根目录（\texttt{\$SYNOPSYS/admin/setup}）\\
        该系统级 setup 文件包含：
  \begin{itemize}
    \item Synopsys 定义的系统变量
    \item 面向站点所有用户的通用 PrimeTime setup 信息
  \end{itemize}
        仅系统管理员可修改此文件。
  \item 用户主目录（home directory）\\
        在该用户自定义 setup 文件中，可指定对 PrimeTime 工作环境的偏好。此文件中的变量设置会覆盖系统级 setup 文件中的对应设置。
  \item 启动 PrimeTime 时的当前工作目录\\
        在该设计相关 setup 文件中，可指定项目或设计环境。此文件中的变量设置会覆盖用户自定义与系统级 setup 文件中的对应设置。
\end{enumerate}

"""
)

chunks.append(
    r"""% ============================================================
\section{启动 PrimeTime 会话}
\subsection*{Starting a PrimeTime Session}

可用命令行界面或图形用户界面启动 PrimeTime 会话：
\begin{itemize}
  \item 命令行界面：在 Linux shell 提示符下输入：
\begin{lstlisting}
% pt_shell
\end{lstlisting}
        工具显示类似如下的启动信息后进入 \texttt{pt\_shell>} 提示符。
  \item 图形用户界面（GUI）：输入：
\begin{lstlisting}
% pt_shell -gui
\end{lstlisting}
\end{itemize}

\figplaceholder{Figure 8: PrimeTime GUI window}{PrimeTime GUI 窗口}{fig:pt-gui}

\begin{seeAlsoBox}
图形用户界面，见第~\ref{chap:gui}~章。
\end{seeAlsoBox}

% ============================================================
\section{许可证检出}
\subsection*{License Checkouts}

启动 PrimeTime 会话时，工具会自动检出一枚 PrimeTime 许可证。

分析过程中，工具按所用功能自动按需检出额外许可证，并给出信息消息，例如：
\begin{lstlisting}
Information: Checked out license 'PrimeTime-SI' (PT-019)
\end{lstlisting}

查看当前已检出许可证数量，使用 \cmd{list\_licenses} 命令：
\begin{lstlisting}
pt_shell> list_licenses
Licenses in use:
     PrimeTime    (1)
     PrimeTime-SI     (1)
1
\end{lstlisting}

还有许多附加功能可用于控制许可证使用方式。详见第~\ref{chap:licensing}~章「控制许可证行为」。

% ============================================================
\section{输入 pt\_shell 命令}
\subsection*{Entering pt\_shell Commands}

通过基于 Tool Command Language（Tcl）的 \cmd{pt\_shell} 命令与工具交互。PrimeTime 命令语言提供类似 Linux 命令 shell 的能力，包括变量、命令条件执行与控制流命令。运行 PrimeTime 时，可以：
\begin{itemize}
  \item 在 \texttt{pt\_shell>} 提示符下交互输入单条命令；
  \item 在 GUI 控制台命令行交互输入单条命令；
  \item 运行一个或多个 Tcl 命令脚本（包含 \cmd{pt\_shell} 命令的文本文件）。
\end{itemize}

关于 Tcl 命令行界面的一般信息，见 SolvNetPlus 上的 \textit{Using Tcl With Synopsys Tools}。

% ============================================================
\section{在命令行获取帮助}
\subsection*{Getting Help on the Command Line}

运行 PrimeTime 时，可使用以下帮助资源：
\begin{itemize}
  \item \textbf{命令帮助}
  \begin{itemize}
    \item 按命令组列出所有 PrimeTime 命令：
\begin{lstlisting}
pt_shell> help
\end{lstlisting}
    \item 显示某命令的简要说明：
\begin{lstlisting}
pt_shell> help command_name
\end{lstlisting}
    \item 显示某命令的所有选项与参数：
\begin{lstlisting}
pt_shell> help -verbose command_name
\end{lstlisting}
  \end{itemize}
  \item \textbf{Man 页}\\
        显示命令、变量或消息的 man 页：
\begin{lstlisting}
pt_shell> man command_variable_or_message_name
\end{lstlisting}
        使用 \cmd{man} 命令的 \opt{-html} 选项可在 HTML Web 浏览器中打开 man 页。
\end{itemize}

"""
)

chunks.append(
    r"""% ============================================================
\section{PrimeTime 静态时序分析流程}
\subsection*{The PrimeTime Static Timing Analysis Flow}

执行 PrimeTime 静态时序分析时，遵循表~\ref{tab:pt-sta-flow} 所列典型流程。

\begin{longtable}{@{}c p{0.28\textwidth} p{0.32\textwidth} p{0.22\textwidth}@{}}
\caption{典型 PrimeTime 静态时序分析流程}\label{tab:pt-sta-flow}\\
\toprule
步骤 & 任务 & 典型命令 & 相关主题 \\
\midrule
\endfirsthead
\multicolumn{4}{c}{\tablename\ \thetable{}（续）}\\
\toprule
步骤 & 任务 & 典型命令 & 相关主题 \\
\midrule
\endhead
\bottomrule
\endfoot
1 & 读入设计数据（门级网表与相关逻辑库） &
\cmd{set search\_path}\\
\cmd{set link\_path}\\
\cmd{read\_verilog}\\
\cmd{link\_design} &
处理设计数据 \\
\midrule
2 & 指定时序与设计规则约束 &
\cmd{set\_input\_delay}\\
\cmd{set\_output\_delay}\\
\cmd{set\_min\_pulse\_width}\\
\cmd{set\_max\_capacitance}\\
\cmd{set\_min\_capacitance}\\
\cmd{set\_max\_fanout}\\
\cmd{set\_max\_transition} &
约束设计 \\
\midrule
3 & 指定时钟特性 &
\cmd{create\_clock}\\
\cmd{set\_clock\_uncertainty}\\
\cmd{set\_clock\_latency}\\
\cmd{set\_clock\_transition} &
时钟 \\
\midrule
4 & 指定时序例外 &
\cmd{set\_multicycle\_path}\\
\cmd{set\_false\_path}\\
\cmd{set\_disable\_timing} &
时序路径与例外 \\
\midrule
5 & 指定环境与分析条件（如工作条件与延时模型） &
\cmd{set\_operating\_conditions}\\
\cmd{set\_driving\_cell}\\
\cmd{set\_load}\\
\cmd{set\_wire\_load\_model} &
工作条件、延时计算 \\
\midrule
6 & 指定 case 与 mode 分析设置 &
\cmd{set\_case\_analysis}\\
\cmd{set\_mode} &
Case 与 Mode 分析 \\
\midrule
7 & 反标延时与寄生参数 &
\cmd{read\_sdf}\\
\cmd{read\_parasitics} &
反标 \\
\midrule
8 & 应用 variation（可选） &
\cmd{read\_ocvm}\\
\cmd{set\_aocvm\_coefficient}\\
\cmd{set\_aocvm\_table\_group}\\
\cmd{set\_ocvm\_table\_group}\\
\cmd{set\_timing\_derate} &
Variation \\
\midrule
9 & 指定功耗信息 &
\cmd{load\_upf}\\
\cmd{create\_power\_domain}\\
\cmd{create\_supply\_net}\\
\cmd{create\_supply\_set}\\
\cmd{create\_supply\_port}\\
\cmd{connect\_supply\_net}\\
\cmd{set\_voltage} &
多电压设计流程 \\
\midrule
10 & 指定信号完整性分析选项与数据 &
\cmd{set si\_enable\_analysis true}\\
\cmd{read\_parasitics -keep\_capacitive\_coupling} &
信号完整性分析 \\
\midrule
11 & 应用特定设计技术选项 &
\cmd{set\_latch\_loop\_breaker}\\
\cmd{set\_multi\_input\_switching\_coefficient}\\
\cmd{define\_scaling\_lib\_group} 等 &
高级分析技术等 \\
\midrule
12 & 检查设计数据与分析设置 &
\cmd{check\_timing}\\
\cmd{check\_constraints}\\
\cmd{report\_design}\\
\cmd{report\_port}\\
\cmd{report\_net}\\
\cmd{report\_clock}\\
\cmd{report\_wire\_load}\\
\cmd{report\_path\_group}\\
\cmd{report\_cell}\\
\cmd{report\_hierarchy}\\
\cmd{report\_reference}\\
\cmd{report\_lib} &
检查约束 \\
\midrule
13 & 执行完整时序分析并查看结果 &
\cmd{report\_global\_timing}\\
\cmd{report\_timing}\\
\cmd{report\_constraint}\\
\cmd{report\_bottleneck}\\
\cmd{report\_analysis\_coverage}\\
\cmd{report\_delay\_calculation}\\
\cmd{update\_timing} &
报告与调试分析结果、GUI \\
\midrule
14 & 生成 ECO 以修复时序违例或回收功耗 &
\cmd{set\_eco\_options}\\
\cmd{fix\_eco\_drc}\\
\cmd{fix\_eco\_timing}\\
\cmd{fix\_eco\_power}\\
\cmd{write\_changes} &
ECO 流程 \\
\midrule
15 & 保存 PrimeTime 会话 &
\cmd{save\_session} &
保存会话 \\
\end{longtable}

"""
)

chunks.append(
    r"""% ============================================================
\section{在 PrimeTime 中使用 Tcl/Tk}
\subsection*{Using Tcl/Tk in PrimeTime}

PrimeTime 命令界面基于 Tool Command Language（Tcl）与 Tk 工具包，与许多其他 Synopsys 工具相同。关于 Tcl 及其在 Synopsys 命令 shell 中的用法，见 SolvNetPlus 上的 \textit{Using Tcl With Synopsys Tools}。

查看当前 PrimeTime 版本所用的 Tcl/Tk 版本：
\begin{lstlisting}
pt_shell> printvar tcl_version
tcl_version   = "8.6"
\end{lstlisting}

\subsection{Tcl 包与 Autoload}
\subsubsection*{Tcl Packages and Autoload}

PrimeTime 支持标准 Tcl package 与 autoload 机制。但不支持 \cmd{load} 命令，因此需要共享库的包无法使用。工具随 Tcl 发行版中标准实现的包一同提供；可在 Synopsys 安装根目录下的 \texttt{auxx/tcllib/lib/tcl8.6} 目录中找到这些包。

向 PrimeTime 添加新 Tcl 包，可执行以下操作之一：
\begin{itemize}
  \item 将包安装到 Synopsys 目录树中；
  \item 在 \texttt{.synopsys\_pt.setup} 中向 \cmd{auto\_path} 变量添加新目录。
\end{itemize}

PrimeTime 提供以下默认位置用于加载包：
\begin{itemize}
  \item 应用相关 Tcl 包：\texttt{auxx/tcllib/primetime}
  \item 适用于所有基于 Tcl 的 Synopsys 工具的包：\texttt{auxx/tcllib/snps\_tcl}
\end{itemize}

例如，若有名为 \texttt{mycompanyPT} 的 Tcl 包（包含 mycompany 所用的 PrimeTime 报告功能），可在 \texttt{auxx/tcllib/primetime} 下创建 \texttt{mycompanyPT} 目录，并将该包的 \texttt{pkgIndex.tcl} 与 Tcl 源文件放入其中。在脚本中用以下命令使用该包：
\begin{lstlisting}
package require mycompanyPT
\end{lstlisting}

\subsection{对 incr Tcl 扩展的支持}
\subsubsection*{Support of the incr Tcl Extension}

PrimeTime 支持 incr Tcl（itcl）扩展，为 Tcl 增加面向对象编程构造。关于 incr Tcl，见 Tcl Developer Xchange 网站：\url{http://tcl.tk}。

% ============================================================
\section{用 TclPro Toolkit 检查与编译脚本}
\subsection*{Checking and Compiling Scripts With the TclPro Toolkit}

TclPro 是面向 Tcl 编程的开源工具包，支持：
\begin{itemize}
  \item 用 TclPro Checker 检查脚本语法
  \item 用 TclPro Compiler 创建字节码编译脚本
  \item 用 TclPro Debugger 调试脚本
\end{itemize}
更多信息见 \url{http://tcl.sourceforge.net}。

\subsection{安装 TclPro 工具}
\subsubsection*{Installing TclPro Tools}

"""
)

chunks.append(
    r"""\subsection{用 TclPro Checker 检查脚本语法}
\subsubsection*{Checking the Syntax in Scripts With the TclPro Checker}

基于 TclPro Checker（\cmd{procheck}）的 Synopsys Syntax Checker 可帮助发现 Tcl 脚本中的语法与语义错误。语法与语义检查所需内容均随 PrimeTime 提供，不必另行下载 TclPro 即可进行语法检查。

Synopsys Syntax Checker（\cmd{snps\_checker}）检查以下内容：
\begin{itemize}
  \item 未知选项
  \item 歧义的选项缩写
  \item 互斥选项的使用
  \item 缺少必需选项
  \item 对字面选项值的数值范围校验（range、$\leq$、$\geq$）
  \item 对 one-of-string（关键字）选项的校验
  \item 递归进入带有脚本参数的构造（如 \cmd{redirect} 与 \cmd{foreach\_in\_collection}）
  \item 重复选项覆盖先前值的警告
\end{itemize}

\subsubsection{运行 Synopsys Syntax Checker}
\paragraph*{Running the Synopsys Syntax Checker}

在 Synopsys 环境中运行 \cmd{snps\_checker} 有两种方式：从 PrimeTime 工具内启动，或独立运行。

独立运行时，须使用 PrimeTime 安装提供的 wrapper 脚本；直接运行 \cmd{snps\_checker} 无效。对于 linux64 平台，脚本位于安装目录 \texttt{linux64/syn/bin/ptprocheck}。

从 PrimeTime 内启动时，需加载安装提供的包：
\begin{lstlisting}
package require snpsTclPro
\end{lstlisting}
这将使 \cmd{check\_script} 命令可用。将待检查脚本名传给该命令即可。

下列示例脚本含有错误，可用于测试 \cmd{snps\_checker}：
\begin{lstlisting}
create_clock [get_ports CLK] -period
create_clock [get_ports CLK] -period -12.2
sort_collection
set paths [get_timing_paths -nworst 10 -delay_type mx_fall -r]
my_report -from [sort_collection \
 [sort_collection $a b] {b c d} -x]
foreach_in_collection x $objects {
  query_objects $x
  report_timing -through $x -through $y -from a -from b -to z > r.out
}
all_fanout -from X -clock_tree
puts [pwd xyz]
\end{lstlisting}

"""
)

chunks.append(
    r"""\begin{lstlisting}[caption={snps\_checker 输出示例}]
% /synopsys/linux64/syn/bin/ptprocheck ex1.tcl
Synopsys Tcl Syntax Checker - Version 1.0

Loading snps_tcl.pcx...
Loading primetime.pcx...
scanning: /disk/scripts/ex1.tcl
checking: /disk/scripts/ex1.tcl
/disk/scripts/ex1.tcl:1 (warnUndefProc) undefined procedure:
get_ports
get_ports CLK
^
/disk/scripts/ex1.tcl:1 (SnpsE-MisVal) Value not specified for
'create_clock -period'
create_clock [get_ports CLK] -period
                            ^
/disk/scripts/ex1.tcl:2 (SnpsE-BadRange) Value -12.2 for
'create_clock -period' must be >= 0.000000
create_clock [get_ports CLK] -period -12.2
                                    ^
/disk/scripts/ex1.tcl:3 (SnpsE-MisReq) Missing required
positional options for sort_collection: collection criteria
sort_collection
^
/disk/scripts/ex1.tcl:4 (badKey) invalid keyword "mx_fall"
must be: max min min_max max_rise max_fall min_rise min_fall
get_timing_paths -nworst 10 -delay_type mx_fall -r
                                            ^
/disk/scripts/ex1.tcl:4 (SnpsE-AmbOpt) Ambiguous option
'get_timing_paths -r'
get_timing_paths -nworst 10 -delay_type mx_fall -r
                                                    ^
/disk/scripts/ex1.tcl:5 (warnUndefProc) undefined procedure:
my_report
my_report -from [sort_collection \
^
/disk/scripts/ex1.tcl:5 (SnpsE-UnkOpt) Unknown option
'sort_collection -x'
sort_collection \
[sort_collection $a b] {b c d} -x
                                   ^
/disk/scripts/ex1.tcl:9 (SnpsW-DupOver) Duplicate option
'report_timing -from' overrides previous value
report_timing -through $x -through $y -from a -from b -to z > r.out
                                              ^
\end{lstlisting}

\subsubsection{Synopsys Syntax Checker 的限制}
\paragraph*{Limitations of the Synopsys Syntax Checker}

\begin{itemize}
  \item 不检查命令缩写；缩写命令会显示为未定义过程。
  \item 由 \cmd{alias} 创建的别名不会展开，也会显示为未定义过程。
  \item 应用运行时进行的少量检查可能不会被覆盖，例如某些「某选项要求另一选项」的情况。
  \item 无法检查极大脚本。
  \item PrimeTime 允许在命令行以非严格引号形式指定 Verilog 风格总线名（如 \texttt{A[0]}）。索引 0--255 的该格式会被检查；通配符 \texttt{*} 与 \texttt{\%} 也会被检查。其他形式（含范围如 \texttt{A[15:0]}）会显示为未定义过程，除非写成 \texttt{\{A[15:0]\}}。
  \item 由 \cmd{define\_proc\_attributes} 增强的用户自定义过程不被检查；此类过程以 \cmd{args} 声明，不会报告语义错误。
\end{itemize}

\subsection{用 TclPro Compiler 创建字节码编译脚本}
\subsubsection*{Creating Bytecode-Compiled Scripts With the TclPro Compiler}

可用 TclPro Compiler（\cmd{procomp}）创建字节码编译脚本。相对 ASCII 脚本，其优势包括：
\begin{itemize}
  \item 加载高效
  \item 内容不可读，更安全
  \item 编译后的 Tcl 过程体被隐藏
\end{itemize}

用 \cmd{source} 命令加载字节码编译脚本即可；除应用程序外无需其他文件。

\subsection{用 TclPro Debugger 调试脚本}
\subsubsection*{Debugging Scripts With the TclPro Debugger}

TclPro debugger（\cmd{prodebug}）是该工具包中最复杂的工具，类似大多数源代码调试器：可单步、步入过程、设置断点等。它不是独立运行的，调试脚本时需要应用程序正在运行。

运行前通过 \texttt{SNPS\_TCLPRO\_HOME} 指定 TclPro 安装路径。用 \cmd{debug\_script} 命令调试脚本。从 PrimeTime 启动 \cmd{prodebug} 需先加载：
\begin{lstlisting}
package require snpsTclPro
\end{lstlisting}
"""
)

chunks.append(
    r"""% ============================================================
\section{限制系统消息}
\subsection*{Limiting System Messages}

触发警告消息的条件可能在单次操作中出现多次，导致数百条重复消息。为控制会话日志大小，工具会自动限制每类条件生成的消息数量。

可用以下方法控制消息限制：
\begin{itemize}
  \item 对整个会话中特定消息类型设置限制，使用 \cmd{set\_message\_info}：
\begin{lstlisting}
pt_shell> set_message_info -id PARA-020 -limit 200
1
\end{lstlisting}
  \item 对 \cmd{read\_parasitics}、\cmd{read\_sdf}、\cmd{report\_annotated\_parasitics -check} 与 \cmd{update\_timing} 生成的消息指定限制，设置 \cmd{sh\_message\_limit} 变量：
\begin{lstlisting}
pt_shell> set_app_var sh_message_limit 50
50
pt_shell> printvar sh_limited_messages
sh_limited_messages = "DES-002 RC-002 RC-004 RC-005 RC-006 RC-009 ..."
\end{lstlisting}
        该限制分别适用于每种消息类型，以及每次运行命令（如 \cmd{read\_sdf}）。默认每次命令执行为每类消息 100 条。
  \item 指定适用于所有消息类型的总体限制，设置 \cmd{sh\_global\_per\_message\_limit}。默认在整个 PrimeTime 会话中每类 10{,}000 条：
\begin{lstlisting}
pt_shell> set_app_var sh_global_per_message_limit 800
800
\end{lstlisting}
\end{itemize}

第一种方法优先于后两种。第二种与第三种方法之间，取较低限制。

% ============================================================
\section{保存与查看系统消息}
\subsection*{Saving and Reviewing System Messages}

可保存工具报告的系统消息，随时查看，并查询消息中报告的数值与字符串。例如，PTE-064 信息消息报告路径相关时钟：
\begin{lstlisting}
Information: Related clock set 0 includes clock 'SDRAM_CLK' with period
 7.500. (PTE-064)
\end{lstlisting}

保存会话中生成的 PTE-064 消息，使用 \cmd{set\_message\_info} 的 \opt{-save\_limit} 选项：
\begin{lstlisting}
pt_shell> set_message_info -id PTE-064 -save_limit 100
\end{lstlisting}
这指示工具保存接下来生成的 100 条 PTE-064 消息。默认 \opt{-save\_limit} 为 $-1$（不保存）；设为 0 表示无限制。

查询消息格式与保存限制，使用 \cmd{get\_message\_info}：
\begin{lstlisting}
pt_shell> get_message_info -id PTE-064
id PTE-064 severity Information limit 10000 save_limit 100 occurrences
 22 suppressed 0 message {Related clock set %d includes clock '%s' with
 period %.3f.}
\end{lstlisting}

创建已保存消息的集合并查询内容，使用 \cmd{get\_message\_instances} 与 \cmd{get\_attribute}：
\begin{lstlisting}
pt_shell> set my_msgs [get_message_instances PTE-064]
...
\end{lstlisting}

\cmd{message\_instance} 对象类的属性可用于查询参数（消息中报告的值与字符串）、完整消息体与消息 ID：
\begin{lstlisting}
pt_shell> get_attribute -class message_instance $my_msgs arguments
0,SDRAM_CLK,7.500 0,SD_DDR_CLK,7.500 1,SYS_CLK,8.000 ...

pt_shell> get_attribute -class message_instance $my_msgs message_body
{Related clock set 0 includes clock 'SDRAM_CLK' with period 7.500.}
{Related clock set 0 includes clock 'SD_DDR_CLK' with period 7.500.}
...
pt_shell> get_attribute -class message_instance $my_msgs message_id
PTE-064 PTE-064 PTE-064 PTE-064 PTE-064 PTE-064 ...
\end{lstlisting}

从集合中每条消息取第二个参数，可用类似脚本：
\begin{lstlisting}
foreach_in_collection x [get_message_instances PTE-064] {
    # To replay the message
  echo [get_attribute $x message_body]
    # To fetch arguments and process them
    # Get arguments string delimited by ','
  set y [get_attribute $x arguments]
  set z [split $y ',']
    # The second argument (with index 1) is the clock
  set my_clock [get_clock [lindex $z 1]]
    # This helps report the clock fetched from the second argument
    # in each case
  query_objects $my_clock
"""
)

chunks.append(
    r"""% ============================================================
\section{结束 PrimeTime 会话}
\subsection*{Ending a PrimeTime Session}

可随时结束会话并退出工具。详见：
\begin{itemize}
  \item 保存 PrimeTime 会话
  \item 退出 PrimeTime 会话
  \item 命令日志文件
\end{itemize}

\subsection{保存 PrimeTime 会话}
\subsubsection*{Saving a PrimeTime Session}

结束工作会话前，可能希望保存当前会话数据。若需稍后查看分析结果，用 \cmd{save\_session} 保存会话；稍后用 \cmd{restore\_session} 恢复到分析中的同一时点。

保存与恢复会话适用于以下情形：
\begin{itemize}
  \item 用脚本过夜运行 PrimeTime；脚本在最终 \cmd{update\_timing} 后使用 \cmd{save\_session}。之后可恢复会话，并用 \cmd{gui\_start}、\cmd{report\_delay\_calculation}、\cmd{report\_timing} 等查看结果。
  \item 将当前分析状态保存为检查点（checkpoint），以便在出错或分析环境意外变化时恢复。
  \item 保存当前会话并多次恢复，以应用不同芯片工作模式。这是以 SDF 格式保存并应用时序数据的替代方案。
\end{itemize}

更多信息见「保存与恢复会话」。

\subsection{退出 PrimeTime 会话}
\subsubsection*{Exiting a PrimeTime Session}

在 \texttt{pt\_shell>} 提示符下输入 \cmd{quit} 或 \cmd{exit} 退出会话：
\begin{lstlisting}
pt_shell> exit
Timing updates: 2 (1 implicit, 1 explicit)
  (0 incremental, 1 full, 1 logical)
Noise updates: 0 (0 implicit, 0 explicit) (0 incremental, 0 full)
Maximum memory usage for this session: 318.43 MB
CPU usage for this session: 2 seconds (2.06 seconds aggregate)
Elapsed time for this session: 47 seconds
Diagnostics summary: 2 errors, 1 warning, 3 informationals

Thank you for using pt_shell!
\end{lstlisting}

在 PrimeTime GUI 主窗口中，\textbf{File $>$ Exit} 菜单命令效果相同，关闭整个 PrimeTime 工具。若要关闭 GUI 窗口但保持 \cmd{pt\_shell} 窗口打开，使用 \textbf{File $>$ Close GUI}，或点击 GUI 窗口角上的关闭按钮。

\subsection{命令日志文件}
\subsubsection*{Command Log File}

结束会话时，工具将会话历史保存到命令日志文件。该文件包含会话期间执行的所有命令，作为工作记录。之后可用 \cmd{source} 将该文件作为脚本运行，以重复整个会话。

工具在当前工作目录创建 \texttt{pt\_shell\_command.log}；同名已有日志会被覆盖。启动新会话前，请重命名需保留的日志文件。

要为命令日志指定不同文件名，在 setup 文件中设置 \cmd{sh\_command\_log\_file} 变量。工作会话期间不能更改该变量。

"""
)

out = Path(__file__).resolve().parent.parent / "chapters" / "02_getting_started.tex"
out.write_text("".join(chunks), encoding="utf-8", newline="\n")
print(f"Wrote {out} ({out.stat().st_size} bytes)")
