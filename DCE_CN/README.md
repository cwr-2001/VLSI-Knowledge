# DC Explorer User Guide — 中文学习译本

基于 Synopsys *DC Explorer User Guide*（**S-2021.06**, June 2021）的非官方个人学习翻译工程。体例仿照同仓库 `ICC2_CN`。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径等技术标识符保留英文。

## 工程结构

```
DCE_CN/
├── main.tex / DCE_CN.pdf
├── preamble.tex
├── chapters/
│   ├── 00_preface.tex … 14_milkyway.tex
│   ├── A_design_file_mgmt.tex … C_basic_commands.tex
│   └── G_glossary.tex
├── figures/
├── scripts/extract_pages.{ps1,py}
├── build.bat
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约起始页 | 状态 |
|----|----------|----------|------|
| 前言 | About This Manual | 14 | 已译 |
| 1 | About DC Explorer | 18 | 已译 |
| 2 | Working With DC Explorer | 25 | 已译 |
| 3 | Setting Up the Libraries | 45 | 已译 |
| 4 | Tolerance for Incomplete or Mismatched Data | 66 | 已译 |
| 5 | Working With Designs in Memory | 90 | 已译 |
| 6 | Defining the Design Environment | 128 | 已译 |
| 7 | Defining Design Constraints | 137 | 已译 |
| 8 | UPF Exploration | 156 | 已译 |
| 9 | Using Floorplan Physical Constraints | 169 | 已译 |
| 10 | Optimization | 228 | 已译 |
| 11 | Using Hierarchical Models | 284 | 已译 |
| 12 | Working With the GUI | 296 | 已译 |
| 13 | Analyzing and Resolving Design Problems | 325 | 已译 |
| 14 | Using a Milkyway Database | 347 | 已译 |
| A | Design File Management for Synthesis | 353 | 已译 |
| B | Design Example | 375 | 已译 |
| C | Basic Commands | 391 | 已译 |
| 术语表 | Glossary | 396 | 已译 |

原书共约 **403** 页。

## 编译方法

```bat
cd "d:\IC Design\VLSI\DCE_CN"
build.bat
```

产物为 `DCE_CN.pdf`（与文件夹名一致）。字体默认 `SimSun` / `Microsoft YaHei` / `FangSong`；缺字体时改 `preamble.tex`。

## 续译 / 校对约定

1. `python scripts\extract_pages.py START END out.txt` 抽原版页。
2. 中文叙述 + 英文术语夹注；命令/选项不译（如 `de_shell`、`compile_exploration`）。
3. 插图：截图放入 `figures/` 后 `\includegraphics` 替换占位框。
