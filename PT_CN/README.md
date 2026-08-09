# PrimeTime User Guide — 中文学习译本

基于 Synopsys *PrimeTime User Guide*（**T-2022.03**, March 2022）的非官方个人学习翻译工程。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径等技术标识符保留英文。

## 工程结构

```
PT_CN/
├── main.tex              # 主文件（XeLaTeX）
├── preamble.tex          # 宏包、双语标题、提示框、Tcl 代码样式
├── chapters/
│   ├── 00_preface.tex … 24_….tex   # 前言 + 第 1–24 章（已译）
│   ├── A_deprecated.tex            # 附录 A（已译）
│   └── G_glossary.tex              # 术语表（已译）
├── figures/              # 原书插图截图放置处
├── scripts/
│   ├── extract_pages.ps1 # 从原版 PDF 提取指定页文本
│   └── gen_ch*.py        # 各章 UTF-8 生成脚本
├── build.bat             # Windows 一键编译
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约起始页 | 状态 |
|----|----------|----------|------|
| 前言 | About This User Guide | 35 | 已译 |
| 1 | Introduction to PrimeTime | 38 | 已译 |
| 2 | Getting Started | 53 | 已译 |
| 3 | Licensing | 69 | 已译 |
| 4 | Managing Performance and Capacity | 82 | 已译 |
| 5 | Working With Design Data | 158 | 已译 |
| 6 | Constraining the Design | 174 | 已译 |
| 7 | Clocks | 204 | 已译 |
| 8 | Timing Paths and Exceptions | 266 | 已译 |
| 9 | Operating Conditions | 304 | 已译 |
| 10 | Delay Calculation | 335 | 已译 |
| 11 | Back-Annotation | 365 | 已译 |
| 12 | Case and Mode Analysis | 421 | 已译 |
| 13 | Variation | 441 | 已译 |
| 14 | Multivoltage Design Flow | 470 | 已译 |
| 15 | SMVA Graph-Based Simultaneous Multivoltage Analysis | 508 | 已译 |
| 16 | Signal Integrity Analysis | 540 | 已译 |
| 17 | Advanced Analysis Techniques | 639 | 已译 |
| 18 | Constraint Consistency | 681 | 已译 |
| 19 | Reporting and Debugging Analysis Results | 827 | 已译 |
| 20 | Graphical User Interface | 888 | 已译 |
| 21 | ECO Flow | 986 | 已译 |
| 22 | Hierarchical Analysis | 1081 | 已译 |
| 23 | Using PrimeTime With SPICE | 1268 | 已译 |
| 24 | Using PrimeTime With Design Compiler | 1286 | 已译 |
| A | Deprecated Features | 1291 | 已译 |
| — | Glossary | 1308 | 已译 |

原书共约 **1323** 页；正文与附录、术语表均已完成结构化中文译本。

## 编译方法

需安装 TeX 发行版（TeX Live / MiKTeX），并确保可用 **XeLaTeX**。

```bat
cd "d:\IC Design\VLSI\PT_CN"
build.bat
```

或手动：

```bat
xelatex -interaction=nonstopmode -jobname=PT_CN main.tex
xelatex -interaction=nonstopmode -jobname=PT_CN main.tex
```

产物为 `PT_CN.pdf`（与文件夹名一致）。
### 字体

默认使用 Windows 的 `SimSun` / `Microsoft YaHei` / `FangSong`。若编译报缺字体，编辑 `preamble.tex` 中的 `\setCJKmainfont` 等为你机器上已有的中文字体。

## 续译 / 修订约定

1. 用 `scripts/extract_pages.ps1` 从原版 PDF 抽页。
2. 用 Python（`Path.write_text(..., encoding='utf-8')`）写入 `chapters/*.tex`，避免 PowerShell 编码破坏中文。
3. 体例：中文叙述 + 英文术语夹注；Tcl 用 `lstlisting`；注意框用 `noteBox`；插图用 `\figplaceholder{英文原题}{中文题}{label}`（三参数）。
4. 技术标识符不译：`pt_shell`、`set_app_var`、`report_timing`、`update_timing` 等。
5. 插图可将截图放入 `figures/` 后用 `\includegraphics` 替换占位框。
