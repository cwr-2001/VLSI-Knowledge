# Fusion Compiler User Guide — 中文学习译本

基于 Synopsys *Fusion Compiler User Guide*（**V-2023.12-SP3**, May 2024）的非官方个人学习翻译工程。体例仿照同仓库 `ICC2_CN`。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径等技术标识符保留英文。

## 工程结构

```
FC_CN/
├── main.tex / main.pdf   # 主文件与编译产物（XeLaTeX）
├── preamble.tex
├── chapters/
│   ├── 00_preface.tex … 13_eco_flow.tex
│   └── 02_fc_*.tex       # 第 2 章 FC 相对 ICC2 新增节
├── figures/
├── scripts/extract_pages.{ps1,py}
├── build.bat
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约起始页 | 状态 |
|----|----------|----------|------|
| 前言 | About This User Guide | 28 | 已译 |
| 1 | Working With the Fusion Compiler Tool | 32 | 已译 |
| 2 | Preparing the Design | 72 | 已译（含 FC 增补节） |
| 3 | Physical Synthesis | 212 | 已译 |
| 4 | Clock Gating | 285 | 已译 |
| 5 | Clock Tree Synthesis | 338 | 已由 ICC2 同主题适配 |
| 6 | Routing and Postroute Optimization | 438 | 已由 ICC2 同主题适配 |
| 7 | Chip Finishing and Design for Manufacturing | 581 | 已由 ICC2 同主题适配 |
| 8 | IC Validator In-Design | 660 | 已由 ICC2 同主题适配 |
| 9 | Routing Using Custom Router | 746 | 已由 ICC2 同主题适配 |
| 10 | Physical Datapath With Relative Placement | 781 | 已由 ICC2 同主题适配 |
| 11 | Hierarchical Implementation | 817 | 已译 |
| 12 | RedHawk and RedHawk-SC Fusion | 867 | 已译 |
| 13 | ECO Flow | 948 | 已译 |

原书共约 **1009** 页；中文译本当前约 **529** 页 PDF。第 5–10 章由 `ICC2_CN` 对应译本批量适配（`icc2_shell`→`fc_shell` 等），若与 FC 原文有差异请对照原版续校。

## 编译方法

```bat
cd "d:\IC Design\VLSI\FC_CN"
build.bat
```

字体默认 `SimSun` / `Microsoft YaHei` / `FangSong`；缺字体时改 `preamble.tex`。

## 续译 / 校对约定

1. `python scripts\extract_pages.py START END out.txt` 抽原版页。
2. 中文叙述 + 英文术语夹注；命令/选项不译。
3. 插图：截图放入 `figures/` 后 `\includegraphics` 替换占位框。
