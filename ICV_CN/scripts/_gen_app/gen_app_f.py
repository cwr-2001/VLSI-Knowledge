# -*- coding: utf-8 -*-
"""Generate F_third_party.tex from raw_app_ef.txt.
Chinese for overview/section intros; English license text kept in lstlisting.
"""
from pathlib import Path
import re

RAW = Path(r"d:\IC Design\VLSI\ICV_CN\scripts\raw_app_ef.txt")
OUT = Path(r"d:\IC Design\VLSI\ICV_CN\chapters\F_third_party.tex")

text = RAW.read_text(encoding="utf-8", errors="replace")
# Drop content before Appendix F start (line ~297 area: "F\nThird-Party")
m = re.search(r"\nF\nThird-Party Licenses", text)
if not m:
    raise SystemExit("Cannot find Appendix F start")
text = text[m.start() + 1 :]  # from F\n...

# Strip page chrome
lines = []
for ln in text.splitlines():
    s = ln.strip()
    if not s:
        lines.append("")
        continue
    if s == "Feedback":
        continue
    if s.startswith("IC Validator User Guide"):
        continue
    if re.fullmatch(r"X-2025\.06", s):
        continue
    if re.fullmatch(r"\d{3,4}", s):  # bare page numbers
        continue
    if s.startswith("Appendix F:"):
        continue
    # form-feed leftovers
    if "\x0c" in ln:
        ln = ln.replace("\x0c", "")
        s = ln.strip()
        if not s or s == "Feedback" or s.startswith("IC Validator") or s.startswith("Appendix F:"):
            continue
    lines.append(ln.rstrip())

# Collapse excessive blank lines
cleaned = []
blank = 0
for ln in lines:
    if not ln.strip():
        blank += 1
        if blank <= 2:
            cleaned.append("")
        continue
    blank = 0
    cleaned.append(ln)

body = "\n".join(cleaned)

# Package section markers (order matters; longer names first where needed)
PACKAGES = [
    ("ANTLR", "ANTLR"),
    ("Boost", "Boost"),
    ("cx_Freeze", "cx\\_Freeze"),
    ("Flatbuffers", "Flatbuffers"),
    ("libdp", "libdp"),
    ("libxml2", "libxml2"),
    ("MariaDB Connector", "MariaDB Connector"),
    ("MariaDB", "MariaDB"),
    ("MCPP Public Domain Code", "MCPP Public Domain Code"),
    ("NumPy*", "NumPy*"),
    ("patchELF", "patchELF"),
    ("pyparsing*", "pyparsing*"),
    ("Python 3.6 License", "Python 3.6 License"),
    ("scikit-learn", "scikit-learn"),
    ("SciPy*", "SciPy*"),
    ("Shroud-1.0", "Shroud-1.0"),
    ("SQLite", "SQLite"),
    ("TclLib", "TclLib"),
    ("Tcl/Tk", "Tcl/Tk"),
    ("zlib", "zlib"),
    ("Zstandard", "Zstandard"),
]

STD_LICENSES = [
    ("Apache-2.0", "Apache-2.0"),
    ("Artistic-1.0-Perl", "Artistic-1.0-Perl"),
    ("GPL-1.0", "GPL-1.0"),
    ("GPL-3.0", "GPL-3.0"),
]


def find_section_spans(src: str, titles: list[tuple[str, str]], end_markers: list[str]):
    """Return list of (raw_title, latex_title, start, end) for each title found in order."""
    positions = []
    for raw, latex in titles:
        # Match title at beginning of a line (possibly indented)
        pat = re.compile(r"(?m)^[ \t]*" + re.escape(raw) + r"[ \t]*$")
        mm = pat.search(src)
        if not mm:
            # try without trailing asterisk variants already in name
            print(f"WARN: section not found: {raw}")
            continue
        positions.append((raw, latex, mm.start()))
    positions.sort(key=lambda x: x[2])
    spans = []
    for i, (raw, latex, start) in enumerate(positions):
        # content starts after the title line
        nl = src.find("\n", start)
        content_start = nl + 1 if nl != -1 else start
        if i + 1 < len(positions):
            end = positions[i + 1][2]
        else:
            end = len(src)
            for em in end_markers:
                emm = re.search(r"(?m)^[ \t]*" + re.escape(em) + r"[ \t]*$", src[content_start:])
                if emm:
                    end = content_start + emm.start()
                    break
        spans.append((raw, latex, content_start, end))
    return spans


def escape_lstlisting(s: str) -> str:
    # lstlisting with basicstyle; avoid ending the environment early
    return s.replace("\\end{lstlisting}", "\\end{lstlisting}")


def latex_lstlisting(content: str) -> str:
    content = content.strip("\n")
    # Dedent common leading spaces from PDF extract
    clines = content.splitlines()
    # remove trailing chrome-ish leftovers
    out_lines = []
    for ln in clines:
        t = ln.rstrip()
        # drop leftover running headers that slipped through
        if t.strip() in ("OSS Package Notices", "Standard OSS License Text", "Licensing Overview"):
            continue
        out_lines.append(t)
    while out_lines and not out_lines[0].strip():
        out_lines.pop(0)
    while out_lines and not out_lines[-1].strip():
        out_lines.pop()
    body = "\n".join(out_lines)
    return (
        "\\begin{lstlisting}[basicstyle=\\ttfamily\\footnotesize,breaklines=true]\n"
        + body
        + "\n\\end{lstlisting}\n"
    )


# Split overview / OSS / Standard
# Find "Licensing Overview" paragraph block after TOC
oss_start = re.search(r"(?m)^[ \t]*OSS Package Notices[ \t]*$", body)
std_start = re.search(r"(?m)^[ \t]*Standard OSS License Text[ \t]*$", body)
if not oss_start or not std_start:
    raise SystemExit(f"markers missing oss={bool(oss_start)} std={bool(std_start)}")

# Overview narrative: from "Licensing Overview" heading after TOC list to OSS Package Notices
# There are two "Licensing Overview" - one in TOC and one as section. Use the second occurrence
lo_matches = list(re.finditer(r"(?m)^[ \t]*Licensing Overview[ \t]*$", body[: oss_start.start()]))
if len(lo_matches) < 1:
    raise SystemExit("Licensing Overview not found")
# Prefer the last one before OSS (actual section)
lo = lo_matches[-1]
overview_text = body[lo.end() : oss_start.start()].strip()

oss_body = body[oss_start.end() : std_start.start()]
std_body = body[std_start.end() :]

header = r"""% 附录 F Third-Party Licenses
\biappendix{第三方许可}{Third-Party Licenses}
\label{app:f}

本附录提供 IC Validator 工具所用第三方软件的许可信息。
\begin{itemize}
  \item 许可概述（Licensing Overview）
  \item OSS 软件包声明（OSS Package Notices）
  \begin{itemize}
    \item ANTLR
    \item Boost
    \item cx\_Freeze
    \item Flatbuffers
    \item libdp
    \item libxml2
    \item MariaDB Connector
    \item MariaDB
    \item MCPP Public Domain Code
    \item NumPy*
    \item patchELF
    \item pyparsing*
    \item Python 3.6 License
    \item scikit-learn
    \item SciPy*
    \item Shroud-1.0
    \item SQLite
    \item TclLib
    \item Tcl/Tk（注：tbcload 代码是 Tcl 的一部分）
    \item zlib
    \item Zstandard
  \end{itemize}
  \item 标准 OSS 许可文本（Standard OSS License Text）
  \begin{itemize}
    \item Apache-2.0
    \item Artistic-1.0-Perl
    \item GPL-1.0
    \item GPL-3.0
  \end{itemize}
\end{itemize}

% ============================================================
\section{许可概述}
\subsection*{Licensing Overview}

本文档包含与 Synopsys\textsuperscript{\textregistered} IC Validator 产品（下称``SOFTWARE''）所含自由与开源软件（``OSS''）相关的许可信息。适用的 OSS 许可条款约束 Synopsys\textsuperscript{\textregistered} 对 SOFTWARE 的分发以及您对 SOFTWARE 的使用。Synopsys\textsuperscript{\textregistered} 以及 SOFTWARE 的第三方作者、许可方与分发方，对因任何使用与分发 SOFTWARE 而产生的全部保证与全部责任予以免责。若 OSS 在与 Synopsys\textsuperscript{\textregistered} 的协议下提供，且该协议不同于适用的 OSS 许可，则那些条款仅由 Synopsys\textsuperscript{\textregistered} 单独提供。

Synopsys\textsuperscript{\textregistered} 已在下文转载 OSS 软件包中出现的版权与其他许可声明。尽管 Synopsys\textsuperscript{\textregistered} 力求为每个 OSS 软件包提供完整准确的版权与许可信息，但 Synopsys\textsuperscript{\textregistered} 不声明或保证下列信息完整、正确或无误。鼓励 SOFTWARE 接收方：(a)~核查所识别的 OSS 软件包以确认本文所提供许可信息的准确性；(b)~将本文档中发现的任何不准确或错误通知 Synopsys\textsuperscript{\textregistered}，以便 Synopsys\textsuperscript{\textregistered} 相应更新本文档。

某些 OSS 许可（例如 GNU General Public Licenses、GNU Library/Lesser General Public Licenses、Affero General Public Licenses、Mozilla Public Licenses、Common Development and Distribution Licenses、Common Public License 以及 Eclipse Public License）要求：与所分发 OSS 二进制相对应的源代码，须按同一 OSS 许可的条款向接收方或其他请求者提供。

希望收到此类对应源代码副本的接收方或请求者，应向 Synopsys\textsuperscript{\textregistered} 邮寄请求至：
\begin{quote}
Synopsys\\
Attn: Open Source Requests\\
690 E. Middlefield Road\\
Mountain View, CA 94043
\end{quote}

提交的全部 OSS 请求中请提供下列信息：
\begin{itemize}
  \item 您请求源代码的 OSS 软件包；
  \item 所请求 OSS 软件包随其分发的 Synopsys\textsuperscript{\textregistered} 产品（以及任何可用的版本信息）；
  \item Synopsys\textsuperscript{\textregistered} 可就该请求联系您的电子邮箱（如有）；以及
  \item 请求源代码的投递邮寄地址。
\end{itemize}

已在 OSS 软件包名称后添加星号（*），以表示这些组件可能包含在使用 ZeBu 开发的软件或硬件产品中。这些组件的 OSS 许可信息也转载于随 SOFTWARE 提供的 IC Validator 可再分发 OSS 声明文本文件中。

\begin{noteBox}
下列各 OSS 软件包与标准许可小节中的法律许可原文保留英文；中文仅译章节说明与概述。
\end{noteBox}

% ============================================================
\section{OSS 软件包声明}
\subsection*{OSS Package Notices}

"""

parts = [header]

oss_spans = find_section_spans(oss_body, PACKAGES, ["Standard OSS License Text"])
def latex_escape_title(s: str) -> str:
    return s.replace("_", "\\_").replace("&", "\\&").replace("%", "\\%")

for raw, latex, start, end in oss_spans:
    content = oss_body[start:end]
    parts.append(f"\\subsection{{{latex}}}\n")
    parts.append(f"\\subsubsection*{{{latex_escape_title(raw)}}}\n\n")
    # Short Chinese lead-in where useful
    parts.append(f"以下为 {latex_escape_title(raw)} 的许可声明原文。\n\n")
    parts.append(latex_lstlisting(content))
    parts.append("\n")

parts.append(
    r"""% ============================================================
\section{标准 OSS 许可文本}
\subsection*{Standard OSS License Text}

本节转载若干标准开源许可的完整法律文本（英文原文）。

"""
)

std_spans = find_section_spans(std_body, STD_LICENSES, [])
for raw, latex, start, end in std_spans:
    content = std_body[start:end]
    parts.append(f"\\subsection{{{latex}}}\n")
    parts.append(f"\\subsubsection*{{{latex_escape_title(raw)}}}\n\n")
    parts.append(f"以下为 {latex_escape_title(raw)} 许可原文。\n\n")
    parts.append(latex_lstlisting(content))
    parts.append("\n")

OUT.write_text("".join(parts), encoding="utf-8")
print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")
print(f"OSS packages found: {len(oss_spans)}/{len(PACKAGES)}")
print(f"Std licenses found: {len(std_spans)}/{len(STD_LICENSES)}")
for raw, _, _, _ in oss_spans:
    print("  OSS:", raw)
for raw, _, _, _ in std_spans:
    print("  STD:", raw)
