# -*- coding: utf-8 -*-
"""Generate 11_back_annotation.tex — Chapter 11 Back-Annotation."""
from pathlib import Path

from pt_tex_utils import chapter_header, count_cjk, lst, write_tex

OUT = Path(__file__).resolve().parent.parent / "chapters" / "11_back_annotation.tex"


def build() -> str:
    p: list[str] = []
    p.append(chapter_header(11, "反标", "Back-Annotation", "chap:backann"))

    p.append(
        "反标（back-annotation）是从外部文件读入延时或寄生电阻电容值供时序分析的过程。"
        "通过反标，可在物理设计各阶段后在工具中准确分析电路时序。关于反标，见：\n"
    )
    p.append(
        r"\begin{itemize}" + "\n"
        r"  \item SDF 反标" + "\n"
        r"  \item 反标延时、时序检查与转换时间" + "\n"
        r"  \item 写出 SDF 文件" + "\n"
        r"  \item 设置集总寄生电阻与电容" + "\n"
        r"  \item 详细寄生" + "\n"
        r"  \item 读入寄生文件" + "\n"
        r"  \item 不完整反标寄生" + "\n"
        r"  \item 反标优先级" + "\n"
        r"  \item 报告反标寄生" + "\n"
        r"  \item 移除反标数据" + "\n"
        r"  \item GPD 寄生浏览器" + "\n"
        r"\end{itemize}" + "\n\n"
    )

    # ===== SDF =====
    p.append(r"\section{SDF 反标}" + "\n" + r"\subsection*{SDF Back-Annotation}" + "\n\n")
    p.append(
        "初始静态时序分析中，PrimeTime 基于 wire load 模型估算 net 延时。"
        "实际延时取决于单元与 net 的物理布局布线；floorplanner 或 router 可提供更详细准确的延时信息供 PrimeTime 分析，此过程称为延时反标，信息常以 SDF 文件提供。\n\n"
        "读入 SDF 反标延时信息的方式：\n"
        r"\begin{itemize}" + "\n"
        r"  \item 从 SDF 文件读入延时与时序检查" + "\n"
        r"  \item 不使用 SDF 格式反标延时、时序检查与转换时间" + "\n"
        r"\end{itemize}" + "\n\n"
    )
    p.append(
        "PrimeTime 支持 SDF v1.0 至 2.1 及 v3.0 子集。一般支持除以下外的所有 SDF 结构："
        r"\texttt{PATHPULSE}、\texttt{GLOBALPATHPULSE}；\texttt{NETDELAY}、\texttt{CORRELATION}；"
        r"\texttt{PATHCONSTRAINT}、\texttt{SUM}、\texttt{DIFF}、\texttt{SKEWCONSTRAINT}。"
        "另支持 v3.0 子集：\texttt{RETAIN}、\texttt{RECREM}、\texttt{REMOVAL}、\texttt{CONDELSE}。\n\n"
        "若无 SDF 文件，可在分析脚本中用电容电阻寄生反标命令指定延时。\n\n"
    )

    p.append(r"\subsection{读入 SDF 文件}" + "\n" + r"\subsubsection*{Reading SDF Files}" + "\n\n")
    p.append(
        r"\cmd{read\_sdf} 从 SDF 1.0/1.1/2.0/2.1/3.0 文件读入实例相关 pin-to-pin 叶单元与 net 时序信息并反标到当前设计。"
        "设计中实例名须与时序文件匹配（如 VHDL 命名约定须一致）。"
        "读入后 PrimeTime 报告：SDF 读入错误数；反标延时与时序检查数；不支持的 SDF 结构及出现次数；"
        "SDF 中的 P/T/V；可用 \cmd{report\_annotated\_delay} 与 \cmd{report\_annotated\_check} 查看反标状态。\n\n"
    )
    p.append(
        lst(
            "pt_shell> read_sdf -load_delay cell adder.sdf\n"
            "pt_shell> current_design MY_DESIGN\n"
            "pt_shell> read_sdf -load_delay net -path u1 mult16_u1.sdf\n"
            "pt_shell> read_sdf -cond_use max boo.sdf\n"
            "pt_shell> read_sdf -analysis_type on_chip_variation boo.sdf\n"
            "pt_shell> read_sdf -analysis_type on_chip_variation \\\n"
            "            -min_file boo_bc.sdf -max_file boo_wc.sdf"
        )
    )

    p.append(r"\subsubsection{从子设计时序文件反标}" + "\n" + r"\paragraph*{Annotating Timing From a Subdesign Timing File}" + "\n\n")
    p.append(
        r"使用 \opt{-path} 时，\cmd{read\_sdf} 用子设计时序文件反标当前设计；"
        "不能将子设计端口 net 延时用于反标当前设计。\n\n"
    )

    p.append(r"\subsubsection{反标负载延时}" + "\n" + r"\paragraph*{Annotating Load Delay}" + "\n\n")
    p.append(
        "负载延时（extra source gate delay）是驱动 net 电容负载引起的单元延时部分。"
        "部分延时计算器将其计入 net 延时，部分计入单元延时。"
        "默认 \cmd{read\_sdf} 假定负载延时在单元延时中；若在 net 延时中，使用 \opt{-load\_delay}。\n\n"
    )

    p.append(r"\subsubsection{从 SDF 反标条件延时}" + "\n" + r"\paragraph*{Annotating Conditional Delays From SDF}" + "\n\n")
    p.append(
        "SDF 中延时与时序检查可有条件（通常基于单元输入值的表达式）。"
        "反标方式取决于 Synopsys 库是否定义条件弧：\n"
        r"\begin{itemize}" + "\n"
        r"  \item 库含条件弧：反标所有 SDF 条件延时；库中 \texttt{sdf\_cond} 字符串须与 SDF 完全匹配" + "\n"
        r"  \item 库无条件弧：反标所有条件延时的最大或最小值；用 \opt{-cond\_use max/min} 选择" + "\n"
        r"\end{itemize}" + "\n\n"
    )
    p.append(r"\figplaceholder{Figure 112: Example of state-dependent timing arcs}{状态相关时序弧示例}{fig:ba-sdf-cond}" + "\n\n")
    p.append(
        "库无条件时，SDF 对所有 A 到 Z 弧使用最坏延时；库有条件时可映射到对应弧。"
        r"\figplaceholder{Figure 113}{库无条件时的反标延时}{fig:ba-sdf-nocond}"
        r"\figplaceholder{Figure 114}{库有条件时的反标延时}{fig:ba-sdf-condlib}"
        "\n\n"
        r"\begin{noteBox}" + "\n"
        r"IOPATH 语句反标两 pin 间所有弧；COND IOPATH 优先于 IOPATH。" + "\n"
        r"\end{noteBox}" + "\n\n"
        r"选择 B=0 延时：\cmd{set\_case\_analysis 0 [get\_pins U1/B]}。"
        "常量可通过 tie-high/low 或另一 pin 的 \cmd{set\_case\_analysis} 传播到选择条件弧的 pin。\n\n"
    )

    p.append(r"\subsubsection{反标时序检查}" + "\n" + r"\paragraph*{Annotating Timing Checks}" + "\n\n")
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{时序检查的 SDF 结构（表 19）}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"检查类型 & SDF 结构 \\" + "\n"
        r"\midrule" + "\n"
        r"Setup/Hold & SETUP, HOLD, SETUPHOLD \\" + "\n"
        r"Recovery & RECOVERY \\" + "\n"
        r"Removal & REMOVAL \\" + "\n"
        r"最小脉冲宽度 & WIDTH \\" + "\n"
        r"最小周期 & PERIOD \\" + "\n"
        r"最大 skew & SKEW \\" + "\n"
        r"No change & NOCHANGE \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(r"\subsubsection{报告延时反标状态}" + "\n" + r"\paragraph*{Reporting Delay Back-Annotation Status}" + "\n\n")
    p.append(
        "SDF 文件通常很大（$\geq$100 MB），建议验证所有 net 已反标延时（及时序检查）。"
        r"\cmd{report\_annotated\_delay} 独立报告单元延时与 net 延时；"
        "net 延时分三类：主输入端口 net、主输出端口 net、内部 net（SDF 标准仅反标内部 net）。\n\n"
        r"\cmd{report\_annotated\_check} 报告反标时序检查数量（setup/hold/recovery/removal/mpw/period/skew/nochange）。\n\n"
    )

    p.append(r"\subsubsection{SDF 流中的更快时序更新}" + "\n" + r"\paragraph*{Faster Timing Updates in SDF Flows}" + "\n\n")
    p.append(
        "路径每点 PrimeTime 由输入 slew 与电容计算 slew 并向前传播。"
        "SDF 反标流中可将 \cmd{timing\_enable\_sdf\_annotation\_updates} 设为 \texttt{false}，"
        "使 \cmd{update\_timing} 不重新计算反标延时弧的 slew，显著加快更新（尤其大设计）。"
        "此模式不适用于需精确 slew 传播的分析（如 SI、CCS 详细寄生）。\n\n"
    )

    # ===== Annotating without SDF =====
    p.append(
        r"\section{反标延时、时序检查与转换时间}" + "\n"
        r"\subsection*{Annotating Delays, Timing Checks, and Transition Times}" + "\n\n"
    )
    p.append(
        r"可用 \cmd{set\_annotated\_delay}、\cmd{set\_annotated\_check}、\cmd{set\_annotated\_transition} "
        "直接反标，无需 SDF。\n\n"
        r"\cmd{set\_annotated\_delay} 在 pin 或弧上设置 net 或单元延时；"
        r"\opt{-cell} 指定单元延时，\opt{-net} 指定 net 延时，\opt{-increment} 增量反标。"
        r"\cmd{set\_annotated\_check} 反标 setup/hold/recovery/removal 等；"
        r"\cmd{set\_annotated\_transition} 反标 pin 转换时间。\n\n"
        r"用 \cmd{report\_annotated\_delay}、\cmd{report\_annotated\_check}、\cmd{report\_annotated\_transition} 验证。"
        r"\cmd{remove\_annotated\_delay}、\cmd{remove\_annotated\_check}、\cmd{remove\_annotated\_transition} 移除反标。\n\n"
    )

    # ===== Writing SDF =====
    p.append(r"\section{写出 SDF 文件}" + "\n" + r"\subsection*{Writing an SDF File}" + "\n\n")
    p.append(
        r"\cmd{write\_sdf} 将当前设计延时与时序检查写入 SDF。"
        "常用选项：\opt{-significant\_digits}、\opt{-load\_delay cell/net}、\opt{-include}、\opt{-exclude}、"
        r"\opt{-compress gzip}、\opt{-map}（映射文件）、\opt{-mask\_violations setup/hold/both}。\n\n"
    )
    p.append(
        "并行驱动网络写出 SDF 时，每个驱动器到每个负载的弧均写出；"
        "大规模并行缓冲网络 SDF 可能极大。"
        r"\figplaceholder{Figure 115: Parallel buffers driving parallel buffers}{并行缓冲驱动并行缓冲}{fig:ba-par-buf}"
        r"\figplaceholder{Figure 116: Cell delays in a parallel driver network}{并行驱动网络中的单元延时}{fig:ba-par-cell}"
        "\n\n"
        "可用 \cmd{timing\_reduce\_multi\_drive\_net\_arcs} 缩减并行驱动器弧后再写 SDF。"
        "时钟 mesh/spine 网络可用外部仿真计算延时后反标到时钟 pin。\n\n"
    )

    p.append(r"\subsection{SDF 映射文件}" + "\n" + r"\subsubsection*{SDF Mapping Files}" + "\n\n")
    p.append(
        "默认 \cmd{write\_sdf} 格式固定；可用映射文件自定义输出格式，引用库中 \texttt{timing\_label} 等。"
        "映射语法使用 \texttt{\$SDF\_CELL}、\texttt{\$SDF\_CELL\_END}、\texttt{\$1}...\texttt{\$N} 占位符及函数如 "
        r"\texttt{min\_rise\_delay(label)}、\texttt{pin(name)}、\texttt{bus(name[index])}。\n\n"
        r"\begin{noteBox}" + "\n"
        r"映射文件不支持通配符；不能指定实例级映射；未提供映射的单元使用 \cmd{write\_sdf} 默认格式。" + "\n"
        r"\end{noteBox}" + "\n\n"
    )

    p.append(r"\subsection{写出压缩 SDF}" + "\n" + r"\subsubsection*{Writing Compressed SDF Files}" + "\n\n")
    p.append(r"\begin{lstlisting}" + "\n" + r"pt_shell> write_sdf -compress gzip 1.sdf.gz" + "\n" + r"\end{lstlisting}" + "\n\n")

    p.append(r"\subsection{写出无 Setup/Hold 违例的 SDF}" + "\n" + r"\subsubsection*{Writing SDF Files Without Setup or Hold Violations}" + "\n\n")
    p.append(
        r"\opt{-mask\_violations} 通过调整违例端点最后一条弧的延时掩盖 setup/hold 违例，便于中期门级仿真。"
        "可能需要更高 \opt{-significant\_digits} 避免舍入导致轻微违例。\n\n"
    )

    # ===== Lumped RC =====
    p.append(
        r"\section{设置集总寄生电阻与电容}" + "\n"
        r"\subsection*{Setting Lumped Parasitic Resistance and Capacitance}" + "\n\n"
    )
    p.append(
        r"\figplaceholder{Figure 117: Lumped RC}{集总 RC}{fig:ba-lumped}"
        r"\cmd{set\_resistance}、\cmd{set\_load} 在 net 上反标 R/C，临时覆盖 wire load 或详细寄生。"
        r"\cmd{remove\_resistance}、\cmd{remove\_capacitance} 移除后恢复先前寄生形式。"
        "可单独设置：读入详细寄生后仅用 \cmd{set\_load} 覆盖电容，电阻仍用详细寄生计算。\n\n"
    )
    p.append(r"\subsection{设置 Net 电容}" + "\n" + r"\subsubsection*{Setting Net Capacitance}" + "\n\n")
    p.append(
        r"\cmd{set\_load} 设置端口与 net 电容；层次设计须先 \cmd{link\_design}。"
        "默认 net 总电容为 pin、port 与 wire 电容之和；指定值覆盖内部估算。"
        r"\opt{-wire\_load} 将值计为 wire 电容。用 \cmd{report\_port}、\cmd{report\_net} 查看。\n\n"
    )
    p.append(r"\subsection{设置 Net 电阻}" + "\n" + r"\subsubsection*{Setting Net Resistance}" + "\n\n")
    p.append(
        r"\cmd{set\_resistance} 覆盖内部估算电阻；\cmd{report\_net} 查看；"
        r"\cmd{remove\_resistance} 移除指定 net；\cmd{reset\_design} 移除全设计电阻反标。\n\n"
    )

    # ===== Detailed parasitics =====
    p.append(r"\section{详细寄生}" + "\n" + r"\subsection*{Detailed Parasitics}" + "\n\n")
    p.append(
        "可将详细寄生反标到 PrimeTime，以 R/C 标注布线网表各物理段；比集总寄生更准确但耗时。"
        "RC 网络用于计算各子节点有效电容、slew 与延时。PrimeTime 可读 SPEF 等格式。"
        r"\figplaceholder{Figure 118: Detailed RC}{详细 RC}{fig:ba-det-rc}"
        "适用于时钟树等关键 net；深亚微米设计中 net 延时占比更大时尤其重要。支持 mesh 网络。"
        r"\figplaceholder{Figure 119: Meshed RC}{Mesh RC}{fig:ba-mesh}\n\n"
    )

    # ===== Reading parasitics =====
    p.append(r"\section{读入寄生文件}" + "\n" + r"\subsection*{Reading Parasitic Files}" + "\n\n")
    p.append(
        r"\cmd{read\_parasitics} 可读以下格式："
        r"\begin{itemize}" + "\n"
        r"  \item Galaxy Parasitic Database（GPD）" + "\n"
        r"  \item Standard Parasitic Exchange Format（SPEF）" + "\n"
        r"  \item Detailed Standard Parasitic Format（DSPF）" + "\n"
        r"  \item Reduced Standard Parasitic Format（RSPF，IEEE 1481-1999）" + "\n"
        r"  \item Milkyway（PARA）" + "\n"
        r"\end{itemize}" + "\n\n"
        "SPEF/RSPF 可为 gzip 压缩；格式可自动识别。net 与 pin 名须与设计匹配。"
        "默认 SPEF 电容不含 pin 电容，工具用库 pin 电容；SPEF 中 pin 电容被忽略。"
        "须确保 SPEF 耦合电容对称；可用 \opt{-syntax\_only -keep\_capacitive\_coupling} 检查不对称耦合。"
        "SPEF 中降阶/详细 RC 网络在延时计算中动态计算有效电容；"
        r"\cmd{report\_timing}、\cmd{report\_net} 报告的 Ctotal 为集总电容（含 pin 电容）。"
        "大文件应放本地磁盘并保证足够内存；gzip 可缩短总处理时间。\n\n"
    )

    p.append(r"\subsection{读入多个寄生文件}" + "\n" + r"\subsubsection*{Reading Multiple Parasitic Files}" + "\n\n")
    p.append(
        r"\begin{lstlisting}" + "\n"
        r"read_parasitics A.spef -path [all_instances -hierarchy BLKA]" + "\n"
        r"read_parasitics B.spef" + "\n"
        r"read_parasitics chip_file_name" + "\n"
        r"report_annotated_parasitics -check" + "\n"
        r"\end{lstlisting}" + "\n\n"
        "后读入文件在冲突 net 上覆盖先读入数据（若有效）。"
        r"\figplaceholder{Figure 120: Second annotation is valid}{第二次反标有效}{fig:ba-ann-valid}"
        r"\figplaceholder{Figure 121: Second annotation is invalid}{第二次反标无效}{fig:ba-ann-invalid}\n\n"
    )

    p.append(r"\subsection{对寄生数据应用位置变换}" + "\n" + r"\subsubsection*{Applying Location Transformations to Parasitic Data}" + "\n\n")
    p.append(
        r"\opt{-axis\_flip flip\_x/flip\_y}、\opt{-rotate}、\opt{-transform} 等对寄生坐标变换以匹配设计朝向。"
        r"\figplaceholder{Figure 122: Transformations specified by axis_flip options}{axis\_flip 指定的变换}{fig:ba-transform}\n\n"
    )

    p.append(r"\subsection{读入多物理 Pin 的寄生}" + "\n" + r"\subsubsection*{Reading Parasitics With Multiple Physical Pins}" + "\n\n")
    p.append(
        "一个逻辑 pin 可对应多个物理 pin（如宽金属）；SPEF 中 \texttt{*D} 定义驱动/负载 pin 映射。"
        r"\cmd{read\_parasitics} 自动处理多物理 pin 连接。\n\n"
    )

    p.append(r"\subsection{从多 corner 寄生数据读入单 corner}" + "\n" + r"\subsubsection*{Reading a Single Corner From Multicorner Parasitic Data}" + "\n\n")
    p.append(
        r"GPD 等多 corner 数据可用 \cmd{set\_gpd\_config} 选择 corner，再 \cmd{read\_parasitics -format gpd}。\n\n"
    )

    p.append(r"\subsection{检查反标 Net}" + "\n" + r"\subsubsection*{Checking the Annotated Nets}" + "\n\n")
    p.append(
        r"\cmd{report\_annotated\_parasitics -check} 验证 RC 网络完整性；"
        r"\cmd{check\_parasitics} 检查 SPEF 语法与一致性。\n\n"
    )

    p.append(r"\subsection{缩放寄生值}" + "\n" + r"\subsubsection*{Scaling Parasitic Values}" + "\n\n")
    p.append(
        r"\cmd{read\_parasitics} 的 \opt{-scale\_capacitance}、\opt{-scale\_resistance} 在读入时缩放 R/C；"
        r"或用 \cmd{set\_parasitic\_corner} 管理多 corner 缩放。\n\n"
    )

    p.append(r"\subsection{增量时序分析的寄生读入}" + "\n" + r"\subsubsection*{Reading Parasitics for Incremental Timing Analysis}" + "\n\n")
    p.append(
        "ECO 后可用增量寄生更新；读入新 SPEF 覆盖变更 net。"
        r"\figplaceholder{Figure 123: Incremental update before and after ECO}{ECO 前后增量更新}{fig:ba-incr}\n\n"
    )

    p.append(r"\subsection{寄生文件限制}" + "\n" + r"\subsubsection*{Limitations of Parasitic Files}" + "\n\n")
    p.append(
        "RSPF/DSPF：SPICE 段实例不校验；电阻不能接地；电容须接地（忽略 node-to-node 耦合并警告）。"
        "SPEF：忽略电感；不支持降阶 net 的极点留数；电阻不能接地；"
        "未启用 SI 时交叉耦合电容拆分到地。\n\n"
    )

    # ===== Incomplete =====
    p.append(r"\section{不完整反标寄生}" + "\n" + r"\subsection*{Incomplete Annotated Parasitics}" + "\n\n")
    p.append(
        "PrimeTime 可补全不完整寄生的 net（须来自 SPEF）。不完整寄生 net 不能完成有效电容计算，"
        "延时计算回退到 wire load。仅当缺失段均在两 pin（边界或叶 pin）之间时可补全。"
        r"\figplaceholder{Figure 124}{用 fanout 补全缺失段}{fig:ba-complete-seg}\n\n"
    )
    p.append(r"\subsection{为不完整 Net 选择 Wire Load 模型}" + "\n" + r"\subsubsection*{Selecting a Wire Load Model for Incomplete Nets}" + "\n\n")
    p.append(
        "按顶层 wire load mode（enclosed/top）、包围层次、主库默认等选择 wire load；"
        r"\opt{-complete\_with wlm} 无模型时用零 R/C。\n\n"
    )
    p.append(r"\subsection{补全 Net 上缺失段}" + "\n" + r"\subsubsection*{Completing Missing Segments on the Net}" + "\n\n")
    p.append(
        r"\cmd{complete\_net\_parasitics -complete\_with wlm/zero} 或 \cmd{read\_parasitics -complete\_with}。"
        r"\figplaceholder{Figure 125: Multidrive segments}{多驱动段}{fig:ba-multidrive}"
        "补全后不可撤销；多次 \cmd{read\_parasitics} 时仅在最后一次使用 \opt{-complete\_with}。"
        r"\cmd{remove\_annotated\_parasitics} 可取消所有寄生读入与补全效果。\n\n"
    )

    # ===== Precedence =====
    p.append(r"\section{反标优先级}" + "\n" + r"\subsection*{Back-Annotation Order of Precedence}" + "\n\n")
    p.append(
        "冲突时优先级（高到低）：\n"
        r"\begin{enumerate}" + "\n"
        r"  \item SDF 或 \cmd{set\_annotated\_delay} 反标的延时" + "\n"
        r"  \item \cmd{set\_resistance}/\cmd{set\_load} 集总 R/C" + "\n"
        r"  \item \cmd{read\_parasitics} 详细寄生" + "\n"
        r"  \item 库或 \cmd{set\_wire\_load\_model} 的 wire load 模型" + "\n"
        r"\end{enumerate}" + "\n\n"
    )

    # ===== Reporting =====
    p.append(r"\section{报告反标寄生}" + "\n" + r"\subsection*{Reporting Annotated Parasitics}" + "\n\n")
    p.append(
        r"\cmd{report\_annotated\_parasitics} 报告反标统计；\opt{-check} 验证 RC 网络完整。"
        "报告按 internal net drive、design input port 等分类显示 Total/RC network/Not Annotated。\n\n"
    )

    # ===== Removing =====
    p.append(r"\section{移除反标数据}" + "\n" + r"\subsection*{Removing Annotated Data}" + "\n\n")
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{移除反标的命令（表 22）}" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"反标类型 & 命令 \\" + "\n"
        r"\midrule" + "\n"
        r"延时 & \cmd{remove\_annotated\_delay} \\" + "\n"
        r"检查 & \cmd{remove\_annotated\_check} \\" + "\n"
        r"转换时间 & \cmd{remove\_annotated\_transition} \\" + "\n"
        r"寄生 & \cmd{remove\_annotated\_parasitics} \\" + "\n"
        r"全部 & \cmd{reset\_design} \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
        r"\cmd{reset\_design -keep\_parasitics} 移除约束与延时反标但保留寄生。\n\n"
    )

    # ===== GPD Explorer =====
    p.append(r"\section{GPD 寄生浏览器}" + "\n" + r"\subsection*{GPD Parasitic Explorer}" + "\n\n")
    p.append(
        "Parasitic Explorer 可查询 GPD 格式反标的寄生 R/C，支持："
        r"\cmd{get\_resistors}、\cmd{get\_ground\_capacitors}、\cmd{get\_coupling\_capacitors}；"
        "查询电阻、电容、子节点名、层名、层号、物理位置等属性；"
        r"\cmd{report\_gpd\_properties}、\cmd{set\_gpd\_config}、\cmd{report\_gpd\_config}、"
        r"\cmd{reset\_gpd\_config}、\cmd{get\_gpd\_corners}、\cmd{get\_gpd\_layers}。\n\n"
    )
    p.append(r"\subsection{使能寄生浏览器}" + "\n" + r"\subsubsection*{Enabling the Parasitic Explorer Feature}" + "\n\n")
    p.append(
        lst(
            "pt_shell> set_app_var parasitic_explorer_enable_analysis true\n"
            "pt_shell> read_parasitics -format gpd my_design_dir.gpd \\\n"
            " -keep_capacitive_coupling ..."
        )
    )
    p.append("读入前设为 true 可读入所有 corner 数据；读入后启用则仅能查询当前 corner。\n\n")
    p.append(r"\subsection{寄生电阻与电容集合}" + "\n" + r"\subsubsection*{Parasitic Resistor and Capacitor Collections}" + "\n\n")
    p.append(
        lst(
            "get_resistors -of_objects [get_nets {net_rx*}] -parasitic_corners vhi85c\n"
            "get_ground_capacitors -from_node U235/z -to_node n121:4\n"
            'get_coupling_capacitors -of_objects n2 -filter "capacitance_max > 0.5e-3"'
        )
    )
    p.append(
        r"须用 \opt{-of\_objects} 或 \opt{-from\_node}/\opt{-to\_node} 指定范围；"
        r"\cmd{get\_attribute -class resistor ... resistance} 查询属性；"
        r"\cmd{list\_attributes -application -class resistor} 列出可用属性。\n\n"
    )
    p.append(r"\subsection{查询磁盘上的 GPD 数据}" + "\n" + r"\subsubsection*{Querying GPD Data Stored on Disk}" + "\n\n")
    p.append(
        r"\cmd{report\_gpd\_properties -gpd MyDesignA.gpd} 报告设计名、工具版本、net/cell 数量等；"
        r"\opt{-layers}、\opt{-parasitic\_corners} 报告层与 corner 信息。"
        r"\cmd{set\_gpd\_config} 可设耦合电容绝对/相对过滤阈值，覆盖 StarRC StarXtract 生成的 GPD 配置。\n\n"
    )

    p.append(r"\subsection{写出 SDF 的常用选项}" + "\n" + r"\subsubsection*{Common write_sdf Options}" + "\n\n")
    p.append(
        r"\cmd{write\_sdf} 支持 \opt{-significant\_digits}、\opt{-load\_delay cell|net}、"
        r"\opt{-include}/\opt{-exclude} 过滤弧类型、\opt{-compress gzip}、\opt{-map} 映射文件、"
        r"\opt{-divide\_and\_conquer} 分块写出大设计 SDF。"
        "并行驱动网络写出时每个驱动器到每个负载均有弧；可用并行驱动器缩减后再写以减小文件。\n\n"
    )

    p.append(r"\subsection{SDF 映射函数}" + "\n" + r"\subsubsection*{SDF Mapping Functions}" + "\n\n")
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{常用 SDF 映射函数（摘要）}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}ll@{}}" + "\n"
        r"\toprule" + "\n"
        r"函数 & 说明 \\" + "\n"
        r"\midrule" + "\n"
        r"min\_rise\_delay(label) & 标号弧最小上升延时 \\" + "\n"
        r"max\_rise\_delay(label) & 标号弧最大上升延时 \\" + "\n"
        r"pin(name) & 单元 pin 名 \\" + "\n"
        r"bus(name[i]) & 总线位 \\" + "\n"
        r"min\_period(pin) & 最小周期检查 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
        "库 timing() 组中定义 timing\_label 供映射引用；min\_pulse\_width 可用 timing\_label\_mpw\_low/high 属性。\n\n"
    )

    p.append(r"\subsection{寄生读入缩放与增量分析}" + "\n" + r"\subsubsection*{Parasitic Scaling and Incremental Read}" + "\n\n")
    p.append(
        r"\cmd{read\_parasitics} 的 \opt{-scale\_capacitance}、\opt{-scale\_resistance} 在读入时缩放；"
        "ECO 后增量读入新 SPEF 覆盖变更 net，配合 \cmd{update\_timing -incremental}。"
        "读入前用本地磁盘存放大 SPEF；gzip 压缩可缩短 I/O 时间。\n\n"
    )

    p.append(r"\subsection{反标命令示例}" + "\n" + r"\subsubsection*{Annotation Command Examples}" + "\n\n")
    p.append(
        lst(
            "set_annotated_delay -cell 0.35 -from U1/A -to U1/Z\n"
            "set_annotated_check -setup 0.2 -from FF/D -to FF/CP\n"
            "set_annotated_transition -rise 0.1 -fall 0.12 [get_pins U2/A]\n"
            "report_annotated_delay -list_not_annotated\n"
            "report_annotated_parasitics -check -list_not_annotated"
        )
    )

    return "".join(p)


def main() -> None:
    text = build()
    size = write_tex(OUT, [text])
    cjk = count_cjk(text)
    print(f"Wrote {OUT}")
    print(f"Size: {size:,} bytes, {len(text.splitlines())} lines, CJK={cjk:,}")


if __name__ == "__main__":
    main()
