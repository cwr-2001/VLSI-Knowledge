# RedHawk User Manual — 中文学习译本

基于 ANSYS *RedHawk User Manual*（**Software Release 2021R1**, Manual Version: Production）的非官方个人学习翻译工程。

## 版权声明

原文版权归 **ANSYS, Inc.**（Apache Design Business Unit）所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、GSR 关键字、文件路径等技术标识符保留英文。

## 工程结构

```
RH_CN/
├── main.tex              # 主文件（XeLaTeX）
├── preamble.tex          # 宏包、双语标题、提示框、Tcl 代码样式
├── chapters/             # 前言 + 第 1–20 章 + 附录 A/C–F
├── figures/              # 原书插图截图放置处
├── scripts/
│   ├── extract_pages.ps1 # 从原版 PDF 提取指定页文本
│   └── raw_*.txt         # 各章抽取原文
├── build.bat             # Windows 一键编译
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约起始页（正文页码） | PDF 页（约） | 状态 |
|----|----------|----------------------|--------------|------|
| 前言 | Copyright / About | — | 1–38 | 已译 |
| 1 | Introduction | 1-1 | 39 | 已译 |
| 2 | RedHawk Flow | 2-5 | 43 | 已译 |
| 3 | User Interface and Data Preparation | 3-9 | 47 | 已译 |
| 4 | Power Calculation, Static IR Drop and EM Analysis | 4-33 | 71 | 已译 |
| 5 | Dynamic Voltage Drop Analysis | 5-79 | 117 | 已译 |
| 6 | Reports | 6-102 | 140 | 已译 |
| 7 | Fixing and Optimizing Grid and Power Performance | 7-122 | 160 | 已译 |
| 8 | Analysis of DvD and Cross-coupling Noise Impacts on Timing | 8-171 | 209 | 已译 |
| 9 | Characterization Using Apache Power Library | 9-213 | 251 | 已译 |
| 10 | Memory and I/O Modeling | 10-284 | 322 | 已译 |
| 11 | Distributed Machine Processing | 11-298 | 336 | 已译 |
| 12 | Package and Board Analysis | 12-324 | 362 | 已译 |
| 13 | Low Power Design Analysis | 13-343 | 381 | 已译 |
| 14 | Chip Power Modeling (CPM) | 14-394 | 432 | 已译 |
| 15 | Reliability and EM Analysis | 15-419 | 457 | 已译 |
| 16 | Pathfinder ESD Analysis | 16-435 | 473 | 已译 |
| 17 | Memory and Mixed Signal Design Analysis | 17-508 | 546 | 已译 |
| 18 | Chip Thermal Modeling and Analysis | 18-509 | 547 | 已译 |
| 19 | Timing File Creation Using Apache Timing Engine (ATE) | 19-517 | 555 | 已译 |
| 20 | Chip-Package Analysis (CPA) | 20-529 | 567 | 已译 |
| A | Installation Procedure | A-542 | 580 | 已译 |
| C | File Definitions | C-547 | 585 | 已译（GSR 关键字分类表） |
| D | Command and GUI Reference | D-766 | 804 | 已译（命令摘要+GUI 概要） |
| E | Utility Programs | E-885 | 923 | 已译 |
| F | Third-Party Software Licenses | F-961 | 999 | 已译（中文导读+英文许可正文） |

原书 PDF 共 **1027** 页；正文页码 ≈ PDF 页码 − 38。原书目录未单独列出 Appendix B。

译本已按原文做**精译扩写**（步骤/选项/关键字/示例尽量译全）；`RH_CN.pdf` 约 **624** 页（插图以占位框表示）。附录 C 含 600+ GSR 关键字逐条说明；附录 D/E 为命令与实用程序详解。

## 编译方法

需安装 TeX 发行版（TeX Live / MiKTeX），并确保可用 **XeLaTeX**。

```bat
cd "d:\IC Design\VLSI\RH_CN"
build.bat
```

或手动：

```bat
xelatex -interaction=nonstopmode -jobname=RH_CN main.tex
xelatex -interaction=nonstopmode -jobname=RH_CN main.tex
```

产物为 `RH_CN.pdf`（与文件夹名一致）。

### 字体

默认使用 Windows 的 `SimSun` / `Microsoft YaHei` / `FangSong`。若编译报缺字体，编辑 `preamble.tex` 中的 `\setCJKmainfont` 等为本机已有中文字体。

## 续译约定

1. 用 `scripts/extract_pages.ps1` 从原版 PDF 抽页（可用 `-DocPage` 按正文页码）。
2. 按第 1 章体例写入对应 `chapters/*.tex`：中文叙述 + 英文术语夹注；Tcl 用 `lstlisting`；注意框用 `noteBox`。
3. 插图：从 PDF 截图放入 `figures/`，用 `\includegraphics` 替换 `\figplaceholder`。
4. 技术标识符不译：`perform analysis`、`TOGGLE_RATE`、`import design` 等。

## 提取页文本示例

```powershell
# 按 PDF 页码
.\scripts\extract_pages.ps1 -Start 39 -End 42 -OutFile scripts\raw_ch1.txt

# 按正文页码（自动 +38）
.\scripts\extract_pages.ps1 -DocPage -Start 1 -End 4 -OutFile scripts\raw_ch1.txt
```
