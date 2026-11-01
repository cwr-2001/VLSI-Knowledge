# 译本体例（必须遵守）

对照 `d:\IC Design\VLSI\ICC2_CN\chapters\01_working_with_icc2.tex` 前 80 行。

- 章节文件只含正文，不要 `\documentclass`。
- 章首：`\bichapter{中文标题}{English Title}` 与 `\label{...}`。分册续写文件不要再写 `\bichapter`。
- 节：`\section{中文}` 下一行 `\subsection*{English heading}`。
- 小节：`\subsection{中文}` 下一行 `\subsubsection*{English heading}`。
- 全文中文。术语首次出现写「中文（English）」。
- 命令、选项、文件名、应用选项、变量、菜单名、窗口名保持英文：行文用 `\cmd{}`、`\opt{}`、`\appopt{}`；菜单路径用 `\textbf{View > Preferences}`。
- Tcl / 命令行示例用 `lstlisting`，不要翻译命令本身。
- 表用 `tabularx` 或 `longtable` + `booktabs`，`\caption` 为中文。
- Note 用 `noteBox`，See Also 用 `seeAlsoBox`。
- 真正的图题（行首 `Figure N 标题`，不是 “Figure N shows”）插入：

```
\begin{figure}[htbp]
\centering
\includegraphics[width=0.92\textwidth]{PREFIX-fig-NNN.png}
\caption{中文图题}
\label{fig:PREFIX-N}
\end{figure}
```

`PREFIX` 为 `gui` 或 `dp`，`NNN` 为三位数字。图中英文不要改写进图，只译 caption。
- 跳过页眉、Feedback、页脚和 `===== PDF page =====` 标记。
- LaTeX 特殊字符在正文中转义：`_` `%` `&` `#` `$`。`\cmd` 与 `lstlisting` 内部的下划线照常。
- 不要缩写流程。步骤、选项表、示例都要译全。
