# -*- coding: utf-8 -*-
"""Generate chapters/20_gui.tex — PrimeTime UG Ch.20 GUI (UTF-8 via Path.write_text)."""
from pathlib import Path

from ch20_supplement import build_supplement as ch20_extra
from pt_tex_utils import (
    chapter_header,
    cmd,
    count_cjk,
    fig,
    itemize,
    lst,
    note,
    opt,
    section,
    see_also,
    subsubsection,
    subsection,
    write_tex,
)

OUT = Path(__file__).resolve().parent.parent / "chapters" / "20_gui.tex"


def build() -> str:
    p: list[str] = []
    p.append(chapter_header(20, "图形用户界面", "Graphical User Interface", "chap:gui"))

    p.append(
        "PrimeTime 图形用户界面（GUI）允许您可视化设计数据，"
        "并使用直方图、原理图、抽象时钟图、波形图与数据表等分析工具查看分析结果。"
        "要学习如何使用 PrimeTime GUI，请参阅以下主题：\n"
    )
    p.append(
        itemize(
            [
                "打开与关闭 GUI",
                "快速入门指南",
                "GUI 窗口",
                "分析时序路径集合",
                "在抽象时钟图中检查时钟路径",
                "分析时钟域与时钟间关系",
                "在原理图中检查时序路径与设计逻辑",
                "查看与修改原理图",
                "检查路径元素",
                "查看对象属性",
                "重新计算时序路径",
                "布局视图与 GUI 中的 ECO",
                "时序路径的交互式多场景分析",
                "GUI Tcl 命令",
            ]
        )
    )

    # --- Opening and Closing ---
    p.append(section("打开与关闭 GUI", "Opening and Closing the GUI"))
    p.append(
        "PrimeTime GUI 是在 Linux 上运行于 X 窗口环境中的窗口与菜单驱动界面。"
        "您可在启动 PrimeTime 时打开 GUI，也可在 PrimeTime 会话期间打开。\n\n"
        "打开 PrimeTime GUI 时，工具会读取 GUI 设置与首选项文件，并打开新的 PrimeTime 主窗口：\n"
    )
    p.append(
        itemize(
            [
                "设置文件执行基本设置任务，例如初始化变量与声明设计库；"
                "首选项文件设置原理图与抽象时钟图视图属性以及全局应用首选项。",
                "主窗口包含用于执行时序分析与其他分析任务的菜单、工具栏与视图窗口。",
            ]
        )
    )
    p.append(
        "您可在会话期间随时打开或关闭 GUI。例如，当需要在 "
        f"{cmd('pt_shell')} 中执行耗时任务或批处理时，可关闭 GUI；"
        "完成后再重新打开 GUI 进行可视化分析。\n\n"
    )
    p.append(see_also(["打开 GUI", "关闭 GUI"]))

    p.append(subsection("打开 GUI", "Opening the GUI"))
    p.append(
        "打开 GUI 前，请确认 DISPLAY 环境变量已设置为您的 Linux 显示名称。"
        "也可在启动会话时同时设置 DISPLAY 变量。\n\n"
        "要启动 PrimeTime 会话并打开 GUI，输入：\n"
    )
    p.append(lst("% pt_shell -gui"))
    p.append(
        "若要在启动 PrimeTime 会话时设置 DISPLAY 环境变量，"
        f"可使用 {opt('-display')} 选项，其中 host\\_name 为 Linux 显示终端名称。例如：\n"
    )
    p.append(lst("% pt_shell -gui -display 192.180.50.155:0.0"))
    p.append(
        f"要在 PrimeTime 会话期间打开 GUI，在 {cmd('pt_shell')} 提示符下输入：\n"
    )
    p.append(lst("pt_shell> gui_start"))

    p.append(subsection("关闭 GUI", "Closing the GUI"))
    p.append(
        "关闭 GUI 时，设计仍保留在内存中，命令行提示符在 shell 中保持活动。\n\n"
        "要在不退出 pt_shell 的情况下关闭 GUI：\n"
        "选择菜单 File > Close GUI；"
        f"或在控制台或 {cmd('pt_shell')} 命令行输入 {cmd('gui_stop')}。\n\n"
        "要关闭 GUI 并完全退出 PrimeTime 会话，选择 File > Exit。\n\n"
    )

    # --- Quick Start ---
    p.append(section("快速入门指南", "Quick Start Guide"))
    p.append(
        "以下步骤介绍 GUI 的部分功能。请从已加载、已约束且已完成时序更新的设计开始。\n"
    )
    p.append("在 GUI 中创建要分析的路径集合。例如：\n")
    p.append(
        lst(
            "pt_shell> set mypaths [get_timing_paths -nworst 20 -max_paths 500 \\\n"
            "  -slack_lesser_than 0.2]"
        )
    )
    p.append("打开 GUI：\n")
    p.append(lst("pt_shell> gui_start"))
    p.append(
        itemize(
            [
                "单击 Path Collections 选项卡。",
                "右键单击路径集合名称，选择 Show Paths。"
                "将显示路径 slack 直方图与路径集合中的路径列表。",
                "在列表中选择并高亮感兴趣的路径（例如最差 slack 的路径），"
                "然后单击 Inspector 按钮打开路径检查器。",
                "在 Path Inspector 中查看 Delay Profiles、Path Summary、Path Elements 与 Timing report 等选项卡。",
                "在 Schematic 视图中查看路径逻辑；使用 View Settings 面板调整显示。",
                "使用 Clock > Clock Analyzer 分析时钟域关系。",
            ],
            env="enumerate",
        )
    )
    p.append(fig("Figure 302", "PrimeTime 主窗口", "fig:pt-main-window"))

    # --- GUI Windows ---
    p.append(section("GUI 窗口", "GUI Windows"))
    p.append(
        "PrimeTime GUI 在窗口中显示信息，为执行不同任务提供灵活工作环境。"
        "这些窗口在 X 窗口环境中独立运行，但共享内存中的同一设计、"
        "当前时序信息以及工具中的全局选择数据。\n\n"
        "打开 GUI 时自动显示 PrimeTime 主窗口，提供多种分析视图。"
        "每个应用窗口包含标题栏、菜单、工具栏与面板、状态栏，"
        "以及显示特定设计信息的视图窗口。视图窗口与面板出现在工具栏与状态栏之间的工作区。\n\n"
    )
    p.append(fig("Figure 302", "PrimeTime 主窗口结构", "fig:gui-main"))

    p.append(subsection("视图窗口", "View Windows"))
    p.append(
        "视图窗口是 GUI 窗口内显示设计信息的子窗口。打开新视图窗口时，"
        "GUI 在工作区底部显示对应选项卡。\n\n"
        "在视图窗口内单击可激活该视图（标题栏高亮）。"
        "重叠时活动视图位于最前。可通过选项卡或 Window 菜单激活视图；"
        "也可使用 Window > Next Window 或 Previous 循环切换。\n\n"
        "含多个子视图的窗口为每个视图提供选项卡；打开时显示默认视图，"
        "单击其他选项卡可切换。\n\n"
    )

    p.append(subsection("视图设置面板", "View Settings Panel"))
    p.append(
        "可通过 View Settings 面板查看并修改活动视图的显示设置。"
        f"显示或隐藏面板：View > Toolbars > View Settings，或按 F8。"
        "可用设置取决于窗口类型。\n\n"
        "默认情况下，更改选项后选项与 Apply 按钮变蓝；单击 Apply 使更改生效。"
        "可通过 Options 菜单或齿轮图标操作面板；可保存/恢复首选项或写入脚本。"
        "Auto apply 选项可跳过 Apply 按钮立即应用所有更改。\n\n"
    )
    p.append(fig("Figure 303", "视图设置面板", "fig:view-settings"))

    p.append(subsection("工具栏与面板", "Toolbars and Panels"))
    p.append(
        "工具栏为视图窗口中最常用命令与交互操作提供快捷访问；"
        "面板是增强工具栏，包含设置选项或处理设计数据的工具。\n\n"
        "显示或隐藏工具栏/面板：View > Toolbars > toolbar\\_name。\n\n"
        "主窗口工具栏包括：Clock、View Zoom、History of Zoom/Pan、"
        "Schematics、View Tools、Highlight、ECO 等。\n\n"
    )
    p.append(fig("Figure 304", "主窗口工具栏", "fig:main-toolbars"))

    p.append(subsection("层次浏览器", "Hierarchy Browser"))
    p.append(
        "层次浏览器用于遍历设计层次并选择设计部分以进行后续分析。"
        "若未打开层次浏览器视图，选择 View > Hierarchy Browser 打开。\n\n"
        "左窗格用 [+] 与 [–] 浏览单元层次；选择左窗格单元后，"
        "右窗格显示该单元内容。可选择列出对象类型：层次单元、所有单元、pin/port、net 等。\n\n"
        "可用上下箭头键滚动对象列表；列宽不足时悬停指针可显示 InfoTip。"
        "单击列标题可排序，可调整列宽。\n\n"
        "在层次浏览器中选择对象时，其他视图（如原理图）中也会同步选中。\n\n"
    )
    p.append(fig("Figure 305", "层次浏览器", "fig:hier-browser"))

    p.append(subsection("控制台", "Console"))
    p.append(
        "控制台用于执行 pt_shell 命令、查看文本格式 PrimeTime 响应以及命令历史。"
        "底部 pt_shell 按钮右侧的长框中可输入命令。\n\n"
        "控制台操作与 pt_shell 终端窗口输入输出一致；"
        "可在终端或控制台任一处输入命令并查看响应。不需要控制台时可关闭，仅使用终端。\n\n"
        "控制台提供终端没有的视图，底部选项卡可选择显示文本类型：\n"
    )
    p.append(
        itemize(
            [
                "Log 选项卡：显示工具 pt_shell 响应。",
                "History 选项卡：查看最近执行命令历史。",
            ]
        )
    )
    p.append("右下角齿轮图标提供搜索、选择、复制与重用控制台内容的选项。\n\n")
    p.append(fig("Figure 306", "控制台", "fig:console"))

    p.append(subsection("对象选择", "Object Selection"))
    p.append(
        "可在视图窗口中单击对象，或通过 Select 菜单命令选择对象以进行后续操作。"
        "交互式多选时按住 Ctrl 键；否则每次新选择会取消先前选择。\n\n"
        "所选对象在所有视图中同步选中，不仅限于当前视图。"
        "例如某单元出现在两个原理图窗口与层次浏览器列表中，"
        "在任一处选中该单元，三处均会高亮。\n\n"
    )
    p.append(subsection("选择时序路径", "Selecting Timing Paths"))
    p.append(
        "可选择特定时序路径，或选择设计中 slack 最差的一条或多条路径。"
        "例如显示路径 profile 前需先选择路径。"
        "简便方法是在 Path Collections 表中单击感兴趣路径。\n\n"
        "创建路径集合示例：\n"
    )
    p.append(lst("set mypath1 [get_timing_paths -from ... -to ...]"))

    p.append(subsection("设置 GUI 首选项", "Setting GUI Preferences"))
    p.append(
        "打开 GUI 时从首选项文件加载 GUI 首选项。默认系统首选项针对大多数设计已优化。\n\n"
        "设置 GUI 首选项：View > Preferences。"
        "更改后 GUI 自动将新设置保存到主目录下 "
        f"{cmd('.synopsys_pt_prefs.tcl')}；下次打开 GUI 时从此文件加载。\n\n"
    )

    # --- Path Analyzer ---
    p.append(section("分析时序路径集合", "Analyzing Timing Path Collections"))
    p.append(
        "可分析时序路径集合以确定设计中时序失败位置。"
        "路径分析器（path analyzer）基于可用属性规则对路径分类；"
        "可选择预定义分类规则或定义自定义规则，也可添加子类别。\n\n"
        "路径分析器是高级时序分析工具，支持自定义趋势分析。例如：\n"
    )
    p.append(
        itemize(
            [
                "按 path group 分类路径，查看违例是否集中于特定 path group。",
                "为 slack 违例超过一个时钟周期的路径创建自定义规则，"
                "判断是否需要 multicycle path 约束。",
                "按 start clock 与 end clock 分类，识别跨域路径（两值不同）。",
                "为物理分区等块打 block mark，再按 block mark 属性分类，"
                "查看失败是否来自特定块。",
            ]
        )
    )
    p.append(f"打开路径分析器：Timing > Path Analyzer。\n\n")
    p.append(fig("Figure 307", "初始路径分析器", "fig:path-analyzer-init"))
    p.append(
        "进一步分析需加载时序路径集合（Collections 按钮）并对路径分类（Create 按钮）。\n\n"
    )
    p.append(fig("Figure 308", "加载并分类后的路径分析器", "fig:path-analyzer-cat"))

    p.append(subsection("加载路径集合", "Loading Path Collections"))
    p.append("要将时序路径集合加载到路径分析器：\n")
    p.append(
        itemize(
            [
                "在路径分析器中单击 Collections 按钮。",
                "在对话框中选择要加载的集合，单击 OK。",
            ],
            env="enumerate",
        )
    )

    p.append(subsection("对时序路径分类", "Categorizing the Timing Paths"))
    p.append(
        "要对时序路径分类：\n"
        "1. 单击 Create 按钮。\n"
        "2. 选择预定义规则（如 End Point、Start Clock、End Clock、Path Group 等）"
        "或自定义规则。\n"
        "3. 单击 OK。\n\n"
        "要删除类别或子类别，在 Categories 树中右键选择 Remove。\n\n"
    )

    p.append(subsection("将路径类别保存到文件", "Saving Path Categories to a File"))
    p.append(
        "要将路径类别保存为脚本文件：在路径分析器中选择类别，"
        "右键选择 Save Categories，指定文件名。\n\n"
    )

    p.append(subsection("从文件加载路径类别", "Loading Path Categories From a File"))
    p.append(
        "要从脚本文件加载路径类别：右键选择 Load Categories，选择先前保存的文件。\n\n"
    )

    p.append(subsection("标记块并应用块分类规则", "Marking Blocks and Applying Block Category Rules"))
    p.append(
        "可为设计中的块（如物理分区）打 block mark，"
        "然后使用基于 block mark 属性的分类规则分析路径。\n\n"
        "预定义块分类规则示例：\n"
    )
    p.append(
        r"\begin{table}[htbp]" + "\n"
        r"\centering" + "\n"
        r"\caption{块的分类规则}" + "\n"
        r"\small" + "\n"
        r"\begin{tabular}{@{}lll@{}}" + "\n"
        r"\toprule" + "\n"
        r"规则名 & 属性 & 定义 \\" + "\n"
        r"\midrule" + "\n"
        r"Inside block & block\_mark & 路径完全位于带 mark 的块内 \\" + "\n"
        r"Crossing block & block\_mark & 路径穿越块边界 \\" + "\n"
        r"Starting in block & block\_mark & 路径起点在块内 \\" + "\n"
        r"Ending in block & block\_mark & 路径终点在块内 \\" + "\n"
        r"\bottomrule" + "\n"
        r"\end{tabular}" + "\n"
        r"\end{table}" + "\n\n"
    )

    p.append(subsection("创建自定义分类规则", "Creating Custom Category Rules"))
    p.append(
        "创建自定义分类规则：\n"
        "1. 单击 Create，选择 Custom Rule。\n"
        "2. 输入规则名称。\n"
        "3. 在 Category Attribute Chooser 中选择属性。\n"
        "4. 可选：在 Filter Attribute Chooser 中定义过滤表达式。\n"
        "5. 单击 OK。\n\n"
        "使用斜杠（/）分隔属性值可创建层次化子类别。\n\n"
    )

    # --- Abstract Clock Graph ---
    p.append(section("在抽象时钟图中检查时钟路径", "Examining Clock Paths in an Abstract Clock Graph"))
    p.append(
        "抽象时钟图（abstract clock graph）以图形方式显示时钟树结构与传播。"
        "可展开/折叠分支、显示/隐藏时钟元素、查看时钟延迟随时间布局等。\n\n"
    )
    p.append(fig("Figure 316", "抽象时钟图窗口", "fig:abstract-clk-graph"))

    p.append(subsection("打开抽象时钟图视图", "Opening Abstract Clock Graph Views"))
    p.append(
        "创建显示所有时钟的抽象时钟图：Clock > Abstract Clock Graph > All Clocks。\n\n"
        "创建显示选定时钟的图：先选择时钟对象，再选择 Clock > Abstract Clock Graph > Selected Clocks。\n\n"
    )

    p.append(subsection("显示与隐藏时钟路径元素", "Displaying and Hiding Clock Path Elements"))
    p.append(
        "在 View Settings 面板 Elements 选项卡中，可选择显示或隐藏："
        "时钟源、缓冲器、反相器、ICG 单元、寄存器时钟 pin、端口等。\n\n"
        "展开弧或 metacell：选中后右键 Expand Selected，或双击。\n\n"
    )
    p.append(fig("Figure 317", "展开选定弧", "fig:expand-arc"))

    p.append(subsection("撤销与重做更改", "Reversing and Reapplying Changes"))
    p.append(
        "在抽象时钟图视图中可撤销/重做操作（Edit > Undo / Redo，或工具栏按钮）。\n\n"
    )

    p.append(subsection("折叠选定侧分支", "Collapsing Selected Side Branches"))
    p.append(
        "可折叠侧分支为单行以腾出空间：\n"
        "1. 选择要折叠的分支根。\n"
        "2. 右键 Collapse Branches。\n\n"
        "展开已折叠侧分支：选择分支根，右键 Expand Branches。\n\n"
    )
    p.append(fig("Figure 318", "分支折叠示例", "fig:branch-collapse"))

    p.append(subsection("查看时钟延迟随时间变化", "Viewing Clock Latency Over Time"))
    p.append(
        "可在抽象时钟图视图中按调度关系显示时钟延迟，分析 skew、瓶颈、插入延迟与 ICG 内在路径延迟。\n\n"
        "操作步骤：\n"
        "1. 在 View Settings 面板单击 Settings 选项卡。\n"
        "2. 选择 Show latency。\n"
        "3. 单击 Apply。\n\n"
        "x 轴表示相对时间的时钟树逻辑；逻辑门按输入时钟 pin 延迟左对齐。\n"
    )
    p.append(fig("Figure 319", "抽象时钟图中的时钟延迟布局", "fig:clk-latency-layout"))

    p.append(subsection("层次化显示时钟树", "Displaying the Clock Trees Hierarchically"))
    p.append(
        "默认抽象时钟图以扁平方式显示每条时钟路径。"
        "可在 View Settings > Elements 中选择 Hierarchy，将图折叠到顶层设计，"
        "再展开各层次单元。可选择逻辑层次（默认）或物理层次（Physical hierarchy）。\n\n"
    )

    # --- Clock Analyzer ---
    p.append(section("分析时钟域与时钟间关系", "Analyzing Clock Domains and Clock-to-Clock Relationships"))
    p.append(
        "使用时钟分析器（clock analyzer）识别设计中时钟间关系并驱动时钟分析，"
        "帮助确定哪些时钟域相互通信并识别时钟域交叉（CDC）。\n\n"
        "时钟域由主时钟或生成时钟及其派生时钟组成；生成时钟有独立子域。"
        "打开时钟分析器：Clock > Clock Analyzer。\n\n"
        "窗口左侧为层次化时钟树视图，右侧为时钟矩阵视图。\n"
    )
    p.append(fig("Figure 320", "时钟分析器", "fig:clock-analyzer"))

    p.append(
        "时钟树视图显示主时钟名称；选择主时钟即选择整个时钟域（含其下生成时钟域）。"
        "时钟矩阵中每行每列代表一个时钟，用编号标注。\n\n"
        "矩阵单元表示时钟域或特定 launch-capture 时钟对关系；"
        "字母与颜色标识路径约束及同步/异步关系。"
        "折叠时钟域时单元显示约束摘要（浅棕色单元）。\n\n"
        "选中矩阵单元后，可在 Legend、Launch Clock、Capture Clock 框查看信息。"
        "右键可对 launch-capture 对执行 Analyze failing paths、Report exceptions、"
        "Report timing、Report clock skew 等操作。\n\n"
        "可将时钟树或矩阵数据导出为 CSV 文件。\n\n"
    )

    p.append(subsubsection("查询 Launch-Capture 时钟对", "Querying Launch-Capture Clock Pairs"))
    p.append(
        "使用 Query 工具查询矩阵单元：\n"
        "1. 单击时钟分析器窗口右上角 Query 按钮。\n"
        "2. 单击矩阵单元，Query 面板显示 launch/capture 时钟与 interclock 关系。\n\n"
    )

    p.append(subsubsection("选择时钟或时钟域", "Selecting Clocks or Clock Domains"))
    p.append(
        "可在时钟树或矩阵视图中单击选择时钟；Ctrl+单击多选；Shift+单击选范围。\n"
        "对给定主时钟深度选择所有生成时钟：选中 launch 时钟，右键 Deep Select all Generated Clocks。\n\n"
        "选中时钟后可右键创建 Clock Graph of Selected Clocks、Clock Graph for Clock Domain、"
        "Schematic of Selected Clocks、Select Source Pins or Ports 等。\n\n"
    )

    p.append(subsubsection("排序时钟树视图", "Sorting the Clock Tree View"))
    p.append("单击列标题降序排序，再次单击升序；层次结构保持。\n\n")

    p.append(subsubsection("按名称查找时钟", "Finding Clocks by Name"))
    p.append(
        "选中时钟树中时钟，右键 Find Clock(s) 显示 Find 工具栏。"
        "可按名称、功能定义（如路径上 pin）等查找。\n\n"
    )
    p.append(fig("Figure 321", "Find 工具栏", "fig:find-toolbar"))

    p.append(subsubsection("过滤时钟域", "Filtering Clock Domains"))
    p.append(
        "可使用过滤条件缩小显示的时钟集合，Focus 于特定时钟域分析。\n\n"
    )

    p.append(subsubsection("保存时钟属性或矩阵约束数据", "Saving Clock Attribute or Clock Matrix Constraint Data"))
    p.append("可将时钟树属性或 launch-capture 矩阵约束导出为 CSV。\n\n")

    p.append(subsubsection("时钟矩阵符号与颜色", "Clock Matrix Symbols and Colors"))
    p.append(
        "矩阵单元使用字母标识关系类型，例如：\n"
    )
    p.append(
        itemize(
            [
                "S — 同步（synchronous）",
                "A — 异步（asynchronous）",
                "E — 显式路径（explicit path）",
                "I — 隐式路径（implicit path）",
                "等（详见原书颜色图例）",
            ]
        )
    )

    # --- Schematic ---
    p.append(section("在原理图中检查时序路径与设计逻辑", "Examining Timing Paths and Design Logic in a Schematic"))
    p.append(
        "实例原理图（instance schematic）可图形显示时序路径、选定设计逻辑或 fanin/fanout 逻辑，"
        "用于可视化分析时序与逻辑并指导其他分析任务。\n\n"
        "实例原理图在扁平单页原理图中显示单元实例、pin、net、port、总线、ripper 与层次穿越，"
        "可跨多个层次级别。实例可为块（层次单元）或叶单元。\n\n"
        "打开实例原理图：\n"
        "1. 选择要在原理图中显示的设计对象或时序路径（层次浏览器、路径表、"
        "Select > Paths From/To/Through、Select > Fanin/Fanout 等）。\n"
        "2. 选择 Schematic > Schematic View。\n\n"
    )
    p.append(fig("Figure 325", "实例原理图", "fig:instance-schematic"))

    p.append(
        "含多层次时可用彩色边界按层次组织对象，可下移/上移层次查看块内容。"
        "可将缓冲器/反相器链或未重要块折叠为抽象 metacell。"
        "可在活动原理图视图中增删逻辑（不改变网表，不影响其他视图）。\n\n"
    )

    p.append(subsection("检查层次单元", "Examining Hierarchical Cells"))
    p.append(
        "默认以扁平单页显示可跨层次的时序路径与逻辑；层次单元初始显示为折叠 metacell。\n"
        "展开所有层次：Schematic > Expand > All Hierarchy。\n"
        "展开选定层次：选中后 Schematic > Expand > Selected Objects 或双击。\n"
        "折叠所有层次：Schematic > Collapse > All Hierarchy。\n"
        "折叠选定层次：Schematic > Collapse > Selected Hierarchy By Parent。\n\n"
    )
    p.append(fig("Figure 326", "层次展开与折叠视图", "fig:hier-expand-collapse"))

    p.append(subsection("在设计层次中下移或上移", "Moving Down or Up the Design Hierarchy"))
    p.append(
        "下移：选中层次单元，Schematic > Move Down 或双击。\n"
        "上移：Schematic > Move Up。\n\n"
    )
    p.append(note("下移/上移时 GUI 会更新原理图选项卡上显示的设计名称。"))

    p.append(subsection("显示或隐藏缓冲器与反相器", "Displaying or Hiding Buffers and Inverters"))
    p.append(
        "默认扁平显示含层次穿越（菱形）的时序路径。"
        "可折叠缓冲器/反相器链或树为 metacell：\n"
    )
    p.append(
        itemize(
            [
                "Schematic > Collapse > All Buffers/Inverters/Crossings By Chain",
                "Schematic > Collapse > All Buffers/Inverters/Crossings By Tree",
                "选中对象后 Schematic > Collapse > Selected Buffers/Inverters/Crossings",
            ]
        )
    )

    p.append(subsection("展开或折叠总线", "Expanding or Collapsing Buses"))
    p.append("可展开总线 net 与 pin 查看各位，或折叠为总线符号。\n\n")

    # --- Viewing and Modifying Schematics ---
    p.append(section("查看与修改原理图", "Viewing and Modifying Schematics"))
    p.append(
        "原理图视图提供缩放、平移、高亮、标注与查询工具。"
        "View Settings 面板可配置显示颜色、线宽、pin 标签、路径高亮样式等。\n\n"
        "Select 菜单支持按名称选择/高亮对象；Query 工具可查看 pin/net/单元属性。\n\n"
        "可撤销/重做原理图中的展开、折叠、增删对象等操作（Edit > Undo/Redo）。\n\n"
    )

    # --- Path Inspector ---
    p.append(section("检查路径元素", "Inspecting Timing Path Elements"))
    p.append(
        "路径检查器（Path Inspector）提供时序路径的详细视图，包括：\n"
    )
    p.append(
        itemize(
            [
                "Delay Profiles — 路径延迟分布",
                "Path Summary — 路径摘要（slack、组、时钟等）",
                "Path Elements — 路径上各 pin 的到达时间、转换时间、增量延迟",
                "Timing report — 文本格式时序报告",
            ]
        )
    )
    p.append(
        "配置路径检查器：在 Path Inspector 窗口 Preferences 中设置显示列与格式。\n\n"
        "可从路径分析器或路径表选中路径后单击 Inspector 打开。\n\n"
    )
    p.append(fig("Figure 330", "路径检查器", "fig:path-inspector"))

    # --- Object Attributes ---
    p.append(section("查看对象属性", "Viewing Object Attributes"))
    p.append(
        "Attribute Browser 与 Query 面板可查看设计对象属性。"
        "Attribute Group Manager 可创建、修改、复制与重命名属性组。\n\n"
    )
    p.append(subsection("查看当前选择", "Viewing the Current Selection"))
    p.append(
        f"使用 {cmd('get_selection')} 或在 GUI 中查看选择摘要。"
        "Select > Selection Summary 可报告当前选中对象数量与类型。\n\n"
    )

    p.append(subsection("管理属性组", "Managing Attribute Groups"))
    p.append(
        "打开 Attribute Group Manager：Tools > Attribute Group Manager。\n"
        "可创建自定义属性组、从首选项恢复、修改 Basic/Placement/SchemAnnotAttr/Timing 组。\n\n"
        "复制组：选中组后单击 Copy；重命名：Rename 按钮编辑名称。\n\n"
    )

    # --- Recalculated Paths ---
    p.append(section("重新计算时序路径", "Recalculating Timing Paths"))
    p.append(
        "可通过重新计算路径表访问并比较正常路径与其重新计算对应项。"
        "使用带 "
        f"{opt('-pba_mode path')} 的 {cmd('get_timing_paths')} 生成重新计算路径集合。例如：\n"
    )
    p.append(lst("set my_recalc_path [get_timing_paths -from ... -to ... -pba_mode path]"))

    p.append(subsection("比较正常与重新计算路径", "Comparing Normal and Recalculated Paths"))
    p.append(
        "在 GUI 中：从路径分析器选择路径，选择 Timing > Recalculated Path Comparison Table。"
        "表格显示 endpoint、path group、正常 slack 与重新计算 slack；"
        "违例单元红色，通过为绿色。\n\n"
    )
    p.append(fig("Figure 345", "重新计算路径表", "fig:recalc-path-table"))

    p.append(subsection("比较正常与重新计算路径 pin", "Comparing Normal and Recalculated Path Pins"))
    p.append(
        "选择重新计算路径表中的行，选择 Timing > Recalculated Path Pin Comparison Table。"
        "并排比较 pin 转换时间、路径延迟、增量延迟等；正负变化分别以绿/红高亮。\n\n"
        "仅当正常与重新计算路径具有相同 through pin 数量时启用 pin 比较表。\n\n"
    )
    p.append(fig("Figure 346", "路径 pin 比较表", "fig:recalc-pin-table"))

    # --- Layout View and ECO ---
    p.append(section("布局视图与 GUI 中的 ECO", "Layout View and ECOs in the GUI"))
    p.append(
        "要在 GUI 中查看芯片布局以准备工程变更指令（ECO），"
        "在主窗口选择 Window > Layout window。\n\n"
        "使用布局视图需用 "
        f"{cmd('set_eco_options')} 指定物理数据（IC Compiler II 或 LEF/DEF 格式）。"
        f"用 {cmd('check_eco')} 检查物理数据有效性。\n\n"
        "可在 GUI 中生成并查看 ECO，包括插入缓冲器、删除缓冲器、调整单元尺寸；"
        "需要 PrimeTime-ADV-PLUS 许可证。更改后可轻松撤销。\n\n"
    )
    p.append(fig("Figure 347", "GUI 中的布局视图", "fig:layout-view"))
    p.append(fig("Figure 348", "GUI 中的 ECO 菜单", "fig:eco-menu"))

    p.append(
        "启用撤销：确保 ECO 菜单中 Enabled 选项有勾选；不使用时可禁用以节省内存。\n\n"
        "可高亮时序路径并仅显示路径上实际 net 形状（含相关 via），不含无关 fanout。\n\n"
    )
    p.append(fig("Figure 349", "Net 形状显示", "fig:net-shape"))
    p.append(fig("Figure 350", "Net 形状显示选项", "fig:net-shape-opts"))

    p.append(
        "使用 ECO > Insert Buffer 或 ECO > Size Cell（"
        f"{cmd('insert_buffer')} / {cmd('size_cell')}）执行手动 ECO 时，"
        "工具自动在内存中执行增量仅路径时序更新，可立即查看更改的时序影响。\n\n"
        "布局期间 on-route 缓冲器引导会遵守 placement blockage。"
        "要禁用自动增量更新，单击 GUI 底部 Fast Timing Path update Enabled 旁的 Disable。\n\n"
    )
    p.append(fig("Figure 351", "GUI 中的手动 ECO 操作", "fig:manual-eco-gui"))

    p.append(
        "在布局窗口显示彩色单元密度图与 pin 密度图："
        "View > Map > Cell Density 或 Pin Density（需 PrimeTime-ADV-PLUS）。\n"
        "显示功耗密度图：View > Map > Cell Power Density（需 PrimePower 分析数据）。\n\n"
    )
    p.append(fig("Figure 352", "布局视图中的单元密度图", "fig:cell-density-map"))
    p.append(fig("Figure 353", "布局视图中的 pin 密度图", "fig:pin-density-map"))
    p.append(fig("Figure 354", "布局视图中的单元功耗密度图", "fig:power-density-map"))

    # --- IMSA ---
    p.append(section("时序路径的交互式多场景分析", "Interactive Multi-Scenario Analysis of Timing Paths"))
    p.append(
        "PrimeTime GUI 提供交互式多场景分析（IMSA）模式，"
        "可从不同运行或场景恢复时序路径集合并一起分析，"
        "作为跨分析运行调试与跟踪违例的快速工具。\n\n"
        "示例流程：\n"
    )
    p.append(
        lst(
            "# PrimeTime Session 1\n"
            "...\n"
            "set my_paths1 [get_timing_paths ...]\n"
            "save_session -only_timing_paths $my_paths1 /dir/s1\n\n"
            "# PrimeTime Session 2\n"
            "...\n"
            "set my_paths2 [get_timing_paths ...]\n"
            "save_session -only_timing_paths $my_paths2 /dir/s2\n\n"
            "# PrimeTime multi-scenario analysis session\n"
            "gui_start\n"
            "restore_session /dir/s1\n"
            "restore_session /dir/s2\n"
            "# 在 GUI 中显示、分类、排序多会话路径 ..."
        )
    )
    p.append(
        note(
            "恢复的仅路径会话须具有相同网表与时钟（约束可不同），"
            "且 save/restore 会话的 PrimeTime 版本须匹配。"
            "IMSA 会话中命令集受限，仅可运行分析已恢复路径集合的命令。"
        )
    )

    p.append(subsection("交互式多场景分析流程", "Interactive Multi-Scenario Analysis Flow"))
    p.append(
        "IMSA 流程可：加载并调试多组时序路径集合；分类与排序（见路径分析器）；"
        "按指定值平移类别 slack 以便组间比较；增删信息列。\n\n"
        "使用步骤：\n"
        "1. 用 get_timing_paths 创建路径集合。\n"
        "2. 用 save_session -only_timing_paths 保存。\n"
        "3. 在新会话中 gui_start，restore_session 加载各会话路径。\n"
        "4. 在路径分析器 Setup Collections 中选择集合并 Apply。\n"
        "5. 创建分类规则（如 End Point）分析路径。\n\n"
    )

    p.append(subsubsection("平移类别的 Slack", "Shifting the Slack for a Category"))
    p.append(
        "在 IMSA 流程中可将类别 slack 平移用户定义值：\n"
        "1. 在路径分析器中选择类别。\n"
        "2. 右键 Shift Category，在 Shift Histogram 对话框设置平移值与父类别。\n"
        "3. 在 Table Histogram 中选择 Slack+Shift 或 Slack 列查看直方图。\n\n"
    )
    p.append(fig("Figure 355", "Shift Histogram 对话框", "fig:shift-histogram"))
    p.append(fig("Figure 356", "Table Histogram 对话框", "fig:table-histogram"))
    p.append(fig("Figure 357", "路径 Slack 与 Slack+Shift", "fig:slack-shift"))

    p.append(subsubsection("IMSA 保存与恢复的属性", "IMSA Attributes Saved and Restored"))
    p.append(
        "save_session -only_timing_paths 保存路径对象及 IMSA 相关属性，"
        "包括 session 名称、场景标识、约束差异标记等，便于跨会话比较。\n\n"
    )

    # --- GUI Tcl Commands ---
    p.append(section("GUI Tcl 命令", "GUI Tcl Commands"))
    p.append(
        "PrimeTime 支持一组控制与查询 GUI 窗口的 Tcl 命令，"
        "可用于编写脚本控制 GUI 外观与内容。例如：\n"
    )
    p.append(
        itemize(
            [
                "创建菜单命令",
                "创建工具栏",
                "添加命令按钮",
                "向 Favorites 面板添加按钮",
                "设置对象颜色",
                "在布局窗口中添加颜色高亮与标注",
            ]
        )
    )
    p.append(
        "GUI 控制能力类似于 IC Compiler II。"
        "列出 GUI 相关命令：\n"
    )
    p.append(
        lst(
            "pt_shell> help gui_*\n"
            " gui_change_highlight  # 更改全局高亮状态\n"
            " gui_create_attrgroup    # 创建 GUI 属性组\n"
            " gui_create_pref_category # 创建首选项类别\n"
            " gui_create_pref_key     # 创建首选项键值对\n"
            " gui_create_vm           # 创建新 Visual Mode\n"
            " ..."
        )
    )
    p.append(lst("pt_shell> man gui_change_highlight"))
    p.append(
        f"{cmd('gui_change_highlight')} 用于操纵全局高亮对象集。\n\n"
    )

    p.append(ch20_extra())

    return "".join(p)


def main() -> None:
    text = build()
    size = write_tex(OUT, [text])
    cjk = count_cjk(text)
    print(f"Wrote {OUT}")
    print(f"Size: {size:,} bytes")
    print(f"CJK characters: {cjk:,}")


if __name__ == "__main__":
    main()
