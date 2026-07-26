# IC Compiler II Implementation User Guide — 中文学习译本

基于 Synopsys *IC Compiler II Implementation User Guide*（**V-2023.12**, December 2023）的非官方个人学习翻译工程。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径等技术标识符保留英文。

## 工程结构

```
ICC2_CN/
├── main.tex              # 主文件（XeLaTeX）
├── preamble.tex          # 宏包、双语标题、提示框、Tcl 代码样式
├── chapters/
│   ├── 00_preface.tex    # 前言（已译）
│   ├── 01_working_with_icc2.tex   # 第 1 章（已译）
│   ├── 02_…12_….tex      # 第 2–12 章（目录占位，待续译）
├── figures/              # 原书插图截图放置处
├── scripts/
│   └── extract_pages.ps1 # 从原版 PDF 提取指定页文本
├── build.bat             # Windows 一键编译
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约起始页 | 状态 |
|----|----------|----------|------|
| 前言 | About This User Guide | 27 | 已译 |
| 1 | Working With the IC Compiler II Tool | 30 | 已译 |
| 2 | Preparing the Design | 66 | 已译 |
| 3 | Placement and Optimization | 181 | 已译 |
| 4 | Clock Tree Synthesis | 225 | 已译 |
| 5 | Routing and Postroute Optimization | 323 | 已译 |
| 6 | Chip Finishing and Design for Manufacturing | 466 | 已译 |
| 7 | IC Validator In-Design | 545 | 占位 |
| 8 | Routing Using Custom Router | 631 | 占位 |
| 9 | Physical Datapath With Relative Placement | 666 | 占位 |
| 10 | Hierarchical Implementation | 702 | 占位 |
| 11 | RedHawk and RedHawk-SC Fusion | 740 | 占位 |
| 12 | ECO Flow | 821 | 占位 |

原书共约 **882** 页，建议按章续译。

## 编译方法

需安装 TeX 发行版（TeX Live / MiKTeX），并确保可用 **XeLaTeX**。

```bat
cd "d:\IC Design\VLSI\ICC2_UG_CN"
build.bat
```

或手动：

```bat
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### 字体

默认使用 Windows 的 `SimSun` / `Microsoft YaHei` / `FangSong`。若编译报缺字体，编辑 `preamble.tex` 中的 `\setCJKmainfont` 等为你机器上已有的中文字体。

## 续译约定

1. 用 `scripts/extract_pages.ps1` 从原版 PDF 抽页。
2. 按第 1 章体例写入对应 `chapters/0N_*.tex`：中文叙述 + 英文术语夹注；Tcl 用 `lstlisting`；注意框用 `noteBox`。
3. 插图：从 PDF 截图放入 `figures/`，用 `\includegraphics` 替换占位框。
4. 技术标识符不译：`place_opt`、`set_app_options`、`mv.upf.enable_golden_upf` 等。

## 提取页文本示例

```powershell
.\scripts\extract_pages.ps1 -Start 66 -End 100 -OutFile raw_ch2.txt
```
