# RH_CN 精译规范

对照 `scripts/raw_*.txt` **逐段精译**，覆盖现有 `chapters/*.tex`（整文件重写覆盖）。

## 必须做到
1. **不写摘要版**：原文每个 section/subsection、步骤枚举、GSR/TCL 选项说明、示例、表格、注意事项均译出。
2. 体例同现有第 1–2 章：`ichapter`/`iappendix`、`\section{中文}`+`\subsection*{English}`、深层 `\subsection`/`\subsubsection*`。
3. `\label{chap:...}` 保持与 `main.tex` 一致；交叉引用用 `ef{chap:...}`。
4. 命令/关键字/文件名英文：`\cmd{}` `\gsr{}` `	exttt{}`；Tcl 用 `lstlisting`。
5. 注意框 `noteBox` / 参见 `seeAlsoBox`；图用 `igplaceholder{Figure X-Y}{中文}`。
6. 中文流畅准确，术语中英夹注（如「去耦电容（decap）」）。
7. **LaTeX 安全**：`# $ % _ &` 在正文妥善转义；`	exttt`/`\gsr`/`\cmd` 内可用裸下划线（已 detokenize）；菜单箭头用 `$ightarrow$`；环境变量写 `	exttt{\$APACHEROOT}`。
8. 无 `\documentclass`；文件须可直接 `\input`。
9. 禁止留下 `\chapterstub` 或「待译」占位。

## 目标行数（对照 raw 大幅扩写）
| 章节文件 | raw 源 | `\label` | 目标行数 |
|----------|--------|----------|----------|
| `07_grid_opt.tex` | `raw_07_grid_opt.txt` | `chap:grid` | >1100 |
| `08_dvd_noise_timing.tex` | `raw_08_dvd_noise_timing.txt` | `chap:noise` | >900 |
| `13_low_power.tex` | `raw_13_low_power.txt` | `chap:lp` | >1100 |
| `14_cpm.tex` | `raw_14_cpm.txt` | `chap:cpm` | >700 |

## 各章扩写要点
- **第 7 章**：示例 A–F 完整日志、FAO DvD 示例 G–H decap 报告、cell swap 选项、mesh/decap 命令表与 GSR 关键字全译。
- **第 8 章**：PJX fullchip/sign-off 对比、skew 模式、时序配置关键字全译（含 EXTEND\_CYCLE\_SELECTION、耦合阈值等）。
- **第 13 章**：多 Vdd 查看/报告、电源门控四态与 charge\_switch.rpt、IP 开关流程、开关 RAM Case 1–4、LDO/APLDO 全流程。
- **第 14 章**：`perform powermodel` 全选项、VectorLess/谐振感知/功率瞬态/用户可配置模式、验证步骤。

## 超长附录策略
- 附录 C：tech/GSC/GSR **按原书分类完整翻译**每个关键字的用途、语法、默认值与示例（可 longtable）。
- 附录 D：TCL 命令摘要表全译 + 各主要命令语法与选项详译；GUI 菜单/按钮按原文结构译。
- 附录 E：每个实用程序全文精译（语法、选项、示例）。
- 附录 F：各第三方组件中文导读 + 许可正文可保留英文 `lstlisting`。
