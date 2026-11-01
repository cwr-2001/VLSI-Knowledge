# IC Compiler II Timing Analysis User Guide — 中文学习译本

基于 Synopsys *IC Compiler II Timing Analysis User Guide*（**M-2016.12-SP4**, June 2017）的非官方个人学习翻译。版式与 `ICC2_CN` 一致。

## 版权声明

原文版权归 **Synopsys, Inc.** 所有。本目录仅为个人学习笔记式译本，**不得商业传播或替代官方文档**。命令名、选项名、文件路径等技术标识符保留英文。插图截自原版 PDF。

## 工程结构

```
ICC2_TA_CN/
├── main.tex
├── preamble.tex
├── chapters/          # 前言 + 第 1–7 章
├── figures/           # 原书 Figure 2-1 … 5-3 截图
├── scripts/
└── build.bat
```

## 编译

需安装 TeX 发行版，并确保可用 **XeLaTeX**。默认字体为 Windows 的 SimSun / Microsoft YaHei / FangSong。

```bat
cd "d:\IC Design\VLSI\ICC2_TA_CN"
build.bat
```
