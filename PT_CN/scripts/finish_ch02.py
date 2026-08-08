# -*- coding: utf-8 -*-
"""Complete and write 02_getting_started.tex from gen_ch02 chunks + ending."""
from pathlib import Path
import runpy

# Execute gen_ch02.py namespace to get chunks (it doesn't write yet)
ns = {}
src = Path(__file__).with_name("gen_ch02.py").read_text(encoding="utf-8")
# Strip any existing write at end if present; exec only definitions
exec(compile(src, "gen_ch02.py", "exec"), ns)
chunks = ns["chunks"]

ending = r"""% ============================================================
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

# Ensure install TclPro paragraph before checker section if missing
text = "".join(chunks)
if "SNPS_TCLPRO_HOME" not in text and "指定已安装程序的路径" not in text:
    insert = r"""使用 TclPro 工具前，需在系统上安装 TclPro，并通过设置环境变量 \texttt{SNPS\_TCLPRO\_HOME} 指定已安装程序的路径。例如，若将 TclPro 1.5 安装于 \texttt{/u/tclpro1.5}，则将该环境变量指向该目录。PrimeTime 以此变量为基路径启动部分 TclPro 工具；其他 Synopsys 应用也使用该变量链接到 TclPro 工具。

"""
    marker = r"\subsection{用 TclPro Checker"
    text = text.replace(marker, insert + marker)

if "debug_script" in text and "这将使" not in text[text.find("debug_script"):text.find("debug_script")+400]:
    pass  # already described

text = text + ending

# Fix man -html sentence if truncated in gen_ch02
if "使用 \\cmd{man} 命令的" not in text and "man command_variable" in text:
    text = text.replace(
        r"""pt_shell> man command_variable_or_message_name
\end{lstlisting}
""",
        r"""pt_shell> man command_variable_or_message_name
\end{lstlisting}
        使用 \cmd{man} 命令的 \opt{-html} 选项可在 HTML Web 浏览器中打开 man 页。
\end{itemize}

""",
    )

# Fix missing -no_init mention
if "-no_init" not in text and r"\opt{-no\_init}" not in text:
    text = text.replace(
        "此文件中的变量设置会覆盖用户自定义与系统级 setup 文件中的对应设置。\n\\end{enumerate}\n",
        "此文件中的变量设置会覆盖用户自定义与系统级 setup 文件中的对应设置。\n\\end{enumerate}\n\n"
        "要用 \\cmd{pt\\_shell} 启动工具时抑制所有 \\texttt{.synopsys\\_pt.setup} 文件的执行，请使用 \\opt{-no\\_init} 选项。\n",
    )

out = Path(r"d:\IC Design\VLSI\PT_CN\chapters\02_getting_started.tex")
out.write_text(text, encoding="utf-8")
cjk = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
print(f"Wrote {out} bytes={out.stat().st_size} CJK={cjk}")
