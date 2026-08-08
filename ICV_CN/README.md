# IC Validator User Guide — 中文学习译本

基于 Synopsys *IC Validator User Guide*（**X-2025.06**, June 2025）的非官方个人学习翻译工程。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本仓库内容仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径、PXL 函数名等技术标识符保留英文。

## 工程结构

```
ICV_CN/
├── main.tex              # 主文件（XeLaTeX）
├── preamble.tex          # 宏包、双语标题、提示框、代码样式
├── chapters/
│   ├── 00_preface.tex    # 前言
│   ├── 01_…17_….tex      # 第 1–17 章
│   └── A_…F_….tex        # 附录 A–F
├── figures/              # 原书插图截图放置处
├── scripts/
│   ├── extract_pages.ps1 # 从原版 PDF 提取指定页文本
│   ├── ch1_part2.tex     # 第 1 章后半
│   └── ch8_part2.tex     # 第 8 章后半
├── build.bat             # Windows 一键编译
└── README.md
```

## 章节对照（原书）

| 章 | 英文标题 | 约起始页 | 状态 |
|----|----------|----------|------|
| 前言 | About This User Guide | 17 | 已译 |
| 1 | IC Validator Basics | 20 | 已译 |
| 2 | Licensing and Resource Requirements | 78 | 已译 |
| 3 | Output Files | 95 | 已译 |
| 4 | IC Validator Dashboard | 110 | 已译 |
| 5 | IC Validator Live DRC | 121 | 已译 |
| 6 | IC Validator Explorer DRC | 161 | 已译 |
| 7 | IC Validator Explorer LVS | 170 | 已译 |
| 8 | PXL | 175 | 已译 |
| 9 | Dynamic-Link Library Support | 244 | 已译 |
| 10 | Unified Fill | 246 | 已译 |
| 11 | Working With Edges | 295 | 已译 |
| 12 | Critical Area Analysis Flow | 299 | 已译 |
| 13 | DRC Error Classification | 306 | 已译 |
| 14 | DRC Waivers | 335 | 已译 |
| 15 | Error Management Utility | 352 | 已译 |
| 16 | Pattern Matching | 376 | 已译 |
| 17 | Pattern Library Manager | 396 | 已译 |
| A | IC Validator Architecture | 426 | 已译 |
| B | LVL Utility | 428 | 已译 |
| C | Layout Integrity Management | 453 | 已译 |
| D | IC Validator PXL Debugger | 471 | 已译 |
| E | PYDB Perl API | 493 | 已译 |
| F | Third-Party Licenses | 499 | 已译（许可法律原文保留英文） |

原书共约 **573** 页。插图目前多为 `\figplaceholder`，可从原版 PDF 截图放入 `figures/` 后替换。

## 编译方法

需安装 TeX 发行版（TeX Live / MiKTeX），并确保可用 **XeLaTeX**。

```bat
cd "d:\IC Design\VLSI\ICV_CN"
build.bat
```

或手动：

```bat
xelatex -interaction=nonstopmode main.tex
xelatex -interaction=nonstopmode main.tex
```

### 字体

默认使用 Windows 的 `SimSun` / `Microsoft YaHei` / `FangSong`。若编译报缺字体，编辑 `preamble.tex` 中的 `\setCJKmainfont` 等为你机器上已有的中文字体。

## 续修约定

1. 用 `scripts/extract_pages.ps1` 从原版 PDF 抽页核对。
2. 体例：中文叙述 + 英文术语夹注；代码用 `lstlisting`；注意框用 `noteBox`。
3. 插图：截图放入 `figures/`，用 `\includegraphics` 替换 `\figplaceholder`。
4. 技术标识符不译：`icv`、`-host_init`、`compare()`、`error_options()` 等。
5. `longtable` 列用 `p{宽度}`，勿用 `tabularx` 的 `X`；表单元格勿以 `[` 开头（需写成 `{[...]}`）。

## 提取页文本示例

```powershell
.\scripts\extract_pages.ps1 -Start 78 -End 94 -OutFile scripts\raw_ch2.txt
```
