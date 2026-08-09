# PrimeTime Workshop Lab Guide — 中文学习译本

基于 Synopsys *PrimeTime Workshop Lab Guide*（**10-I-034-SLG-015**, **2018.06**）的非官方个人学习翻译工程。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径、消息编号等技术标识符保留英文。

## 工程结构

```
PT_Lab_CN/
├── main.tex              # 主文件（XeLaTeX）
├── preamble.tex          # 宏包、提示框、Tcl 代码样式
├── chapters/
│   ├── 00_copyright.tex
│   ├── 01_lab01_flow.tex … 09_lab09_si_noise.tex
│   └── A_job_aids.tex
├── scripts/
│   ├── extract_pages.ps1 # 从原版 PDF 提取页图/OCR
│   └── raw_lab*.txt      # OCR 原文（校对用）
├── build.bat
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约 PDF 页 | 状态 |
|----|----------|-----------|------|
| — | Copyright | 1–2 | 已译 |
| Lab 1 | PrimeTime Flow | 3–18 | 已译 |
| Lab 2 | Constraining Methodology | 19–32 | 已译 |
| Lab 3 | Generating Reports | 33–50 | 已译 |
| Lab 4 | Constraining Multiple Clocks | 51–70 | 已译 |
| Lab 5 | Additional Constraints | 71–82 | 已译 |
| Lab 7 | Path-Based Analysis | 83–90 | 已译 |
| Lab 8 | SI Delay Analysis | 91–102 | 已译 |
| Lab 9 | SI Noise Analysis | 103–114 | 已译 |
| 附录 | Job Aids（速查卡） | 115–124 | 已译 |

说明：原书无 Lab 6（与配套 Student Guide 一致，调试类内容以课堂讲义为主）。

原书共约 **124** 页（扫描件）；正文由 OCR 后人工校对翻译。

## 编译方法

```bat
cd "d:\IC Design\VLSI\PT_Lab_CN"
build.bat
```

需安装 TeX 发行版并可用 **XeLaTeX**。字体默认 `SimSun` / `Microsoft YaHei` / `FangSong`。

## 翻译约定

1. 中文叙述 + 英文术语夹注；Tcl 用 `lstlisting`；注意/提示用对应 tcolorbox；每题答案以「答：」紧跟在同一问题框内。
2. 技术标识符不译：`pt_shell`、`report_timing`、`restore_session`、`PTE-070` 等。
3. 设计名 **ORCA**、目录名 `lab1_flow` 等保持原文。
4. OCR 噪声处对照原版扫描页校对。
