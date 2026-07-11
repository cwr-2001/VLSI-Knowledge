# Synopsys 常见文件格式说明

- **`*.vg`, `*.g.v`** – Verilog gate-level netlist file.  
  Verilog 门级网表文件。有时用这些扩展名区分 RTL 源文件与门级网表。

- **`*.svf`** – Automated Setup File.  
  自动设置文件。帮助 Formality 处理设计流程中其他工具引入的设计变更；用于辅助比较点（compare-point）匹配与形式验证，便于对齐待验证设计中的比较点。每加载一个 SVF，Formality 会解析并保存其内容，供基于名称的比较点匹配阶段使用。

- **`*.ddc`** – Synopsys internal database format.  
  Synopsys 内部数据库格式。官方推荐用于保存门级网表。

- **`*.vcd`** – Value Change Dump format.  
  值变化转储格式，用于保存信号翻转波形。因是文本格式，文件往往很大。可用 `vcd2vpd`、`vpd2vcd`、`vcd2saif` 等工具做格式转换。

- **`*.vpd`** – VCD Plus.  
  Synopsys 专有的压缩二进制波形格式，同样用于保存信号翻转轨迹。

- **`*.saif`** – Switching Activity Interchange Format.  
  开关活动交换格式，用于存储信号翻转活动。支持 signal、port、generate、枚举、record、array、integer 等。

- **`*.tcl`** – Tool Command Language script.  
  Tcl 脚本。Synopsys 工具的主要驱动/脚本语言。

- **`*.sdc`** – Synopsys Design Constraints.  
  Synopsys 设计约束。基于 Tcl 的约束格式，用于在 EDA 工具间传递设计意图。通常包含：
  - SDC 版本
  - 单位（Units）
  - 时序约束（Timing constraints）
  - 设计约束（Design constraints）
  - 注释（Comments）

- **`*.lib`** – Technology Library source file.  
  工艺库源文件（Liberty）。包含标准单元表征数据，例如：
  - 单元名（Cell names）
  - 管脚名（Pin names）
  - 面积（Area）
  - 延时（Delay）
  - 管脚电容（Pin capacitance）
  - 设计规则约束（Design rule constraints）
  - 工作条件（Operating conditions）
  - 线负载模型（Wire-load models）

- **`*.db`** – Technology Library.  
  工艺库。`.lib` 的编译后二进制版本。

- **`*.plib`** – Physical Library source file.  
  物理库源文件。包含物理版图相关信息，用于：
  - Floorplanning（布局规划）
  - RC estimation（RC 估算）
  - Placement（布局）
  - Routing（布线）

- **`*.pdb`** – Physical Library.  
  物理库。`.plib` 的编译版本。

- **`*.slib`** – Symbol Library source file.  
  符号库源文件。定义库单元在原理图中的图形符号，供 Design Compiler / Design Vision 使用。

- **`*.sdb`** – Symbol Library.  
  符号库。`.slib` 的编译版本。

- **`*.sldb`** – DesignWare Library.  
  DesignWare 库。包含 DesignWare IP 库信息。

- **`*.def`** – Design Exchange Format.  
  设计交换格式。常用于 Cadence 工具描述物理版图；Synopsys 传统上多用 Milkyway。

- **`*.lef`** – Library Exchange Format.  
  库交换格式。描述标准单元物理抽象。Cadence 工具广泛使用；Synopsys 历史上常将 LEF 转换为 Milkyway/NDM。

- **`*.rpt`** – Report file.  
  报告文件。Synopsys 工具生成的纯文本报告。

- **`*.tf`** – Vendor Technology File.  
  厂商工艺文件。包含工艺相关信息，例如：
  - 金属层定义（Metal layer definitions）
  - 物理/电学特性（Physical/electrical characteristics）
  - 设计规则（Design rules）

- **`*.itf`** – Interconnect Technology File.  
  互连工艺文件。描述工艺剖面与连通性，包括导体层与介质层属性。

- **`*.map`** – Mapping file.  
  映射文件。将厂商工艺文件中的名称映射到工艺 ITF 中使用的名称。

- **`*.tluplus`** – TLUPlus file.  
  TLUPlus 文件。由 ITF 生成，包含高级 RC 提取模型，供 Synopsys 布局布线工具使用。

- **`*.spef`** – Standard Parasitic Exchange Format.  
  标准寄生交换格式。用于保存布局布线后提取的寄生电阻与电容。

- **`*.sbpf`** – Synopsys Binary Parasitic Format.  
  Synopsys 二进制寄生格式。SPEF 的专有压缩二进制版本，加载更快、体积更小。

- **`*.nmw` / Milkyway Database** – Synopsys physical design database.  
  Synopsys 物理设计数据库。包含：
  - 标准单元库（Standard cell libraries）
  - Macro 库（Macro libraries）
  - 物理版图（Physical layout）
  - 时序信息（Timing information）
  - Floorplan
  - Placement
  - Routing
  - 设计层次（Design hierarchy）

  Milkyway 库分为多种 view，例如：
  - CEL（cell view，单元视图）
  - FRAM（frame view，框架视图）
  - NET
  - PIN
  - 等

  > **Note / 注意：** 在 ICC2 中，Milkyway 已被 **NDM（New Data Model）** 取代。

- **`simv`** – Compiled simulation executable.  
  编译后的仿真可执行文件。由 Synopsys VCS 编译生成。

- **`alib-52`** – Characterized target technology library cache.  
  目标工艺库表征缓存。Design Compiler 生成的伪库，通过缓存工艺表征数据加速优化。
