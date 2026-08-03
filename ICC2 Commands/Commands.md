# Sink
Sink is a pin or port at which a signal is received from a net and is used as an input to a cell or logic element.   
Data sink + Clock sink + Control sink

# Net delay / fanout
`report_timing -max_paths 1 -path_type full -nets # net fanout ` 
`report_delay_calculation -corner ss_125c -from [get_pins I_BLENDER_1/s3_op1_reg[8]/Q ] -to [get_pins I_BLENDER_1/U291/Y] `

# Reference -> Instance
`get_cells -hierarchical -filter "ref_name == MUX21X1_RVT"`
# Instance -> Reference 
```
get_attribute -objects [get_cells I_BLENDER_1/U291] -name ref_name

sizeof_collection [get_clocks *CLK*]   

change_selection [all_fanout -from [get_pins -of_objects [get_object_name [get_attribute [get_clocks SYS_2x_CLK] sources]]]]   
change_selection [all_fanout -from [get_attribute [get_clocks SYS_2x_CLK] sources]]   


report_timing -max_paths 1   
report_timing -to [get_cells I_BLENDER_1/s3_op1_reg[8]]   
report_timing -from [get_cells I_BLENDER_1/R_476]  
```


# IR-Drop、EM、Noise、天线效应
> - IR-Drop ↔ PG 网络宽度、via 数量、拥塞、cell activity、局部电流密度
> - EM ↔ 金属宽度、via 阵列、驱动电流、线长、局部电流密度
> - Noise ↔ aggressor/victim 耦合、线长、parallel run length、slew、driver strength、shield
> - Antenna ↔ 长金属面积、层级、gate 面积、jumper、diode

---

## 1. 总体修复流程

```text
Violation
   │
   ├── IR-Drop
   ├── EM
   ├── Noise
   └── Antenna
   │
   ▼
定位具体 net / instance / region
   │
   ▼
判断根因
   │
   ├── PG 不足？
   ├── routing 资源不足？
   ├── via 不足？
   ├── driver 太强/负载太大？
   ├── 长线/耦合严重？
   └── antenna ratio 超标？
   │
   ▼
局部修复
   │
   ├── 改 PG
   ├── 加宽金属
   ├── 增加 via
   ├── 换层
   ├── 插 buffer
   ├── 换 drive strength
   ├── reroute / rip-up
   ├── shield
   ├── jumper
   └── diode
   │
   ▼
增量验证
   │
   ├── DRC
   ├── LVS / connectivity
   ├── Timing
   ├── IR-Drop
   ├── EM
   ├── Noise
   └── Antenna
```

---

# 2. IR-Drop 修复

## 2.1 IR-Drop 
PDN 上负载电流经过电源网络的电阻产生电压下降。
因此修复方向只有两个核心：

1. **降低电流 I**
2. **降低 PDN 电阻 R**

实际后端中通常优先降低 R，同时通过 placement / power optimization 降低局部电流密度。

---

## 2.2 Static IR-Drop

Static IR 主要关注：

- 电源网络电阻
- PG stripe / rail 宽度
- via 数量
- macro PG 连接
- tap / rail 连通性
- 局部 power density

### 常见原因

- PG stripe 太少
- stripe 太窄
- PG via 太少
- macro 周围 PG 不连续
- standard-cell rail 连接不足
- 某区域 cell density / power density 太高
- 电源网络存在高阻路径

### 修复方法

### 方法 1：增加 PG stripe

提高该区域的供电能力：

```text
增加 stripe 数量
增加 stripe 宽度
缩短供电路径
```

适合：

- 大面积 IR hotspot
- macro 周围
- 高功耗 block

---

### 方法 2：增加 PG via

例如：

```text
M6
│ │ │
via array
│ │ │
M5
```

减少垂直方向的等效电阻。

尤其关注：

- macro PG pin
- stripe intersection
- ring ↔ stripe
- 不同 PG layer 之间

---

### 方法 3：增加 power mesh 密度

如果某区域：

```text
PG stripe       PG stripe
    │               │
    │               │
    │   hotspot     │
    │               │
```

可以增加中间 stripe，缩短 standard cell 到主干 PG 的距离。

---

### 方法 4：降低局部 power density

如果 IR hotspot 与高功耗 cell 高度重合：

- spreading high-power cells
- 调整 placement
- 增加局部 whitespace
- 避免大量高 switching cell 集中
- 合理放置 macro / high-power block

---

## 2.3 Dynamic IR-Drop

Dynamic IR 与瞬时 switching activity 强相关。

主要因素：

```text
Dynamic IR
   ↓
瞬时电流
   ↓
同时翻转数量
   ↓
局部 power density
   ↓
PDN impedance
```

### 修复方向

- 优化高 activity cell placement
- 降低局部 switching concentration
- 加强局部 PG
- 增加 decap
- 优化 power grid
- 必要时调整 cell size / buffering

### Decap 的作用

Decap 可以在瞬态负载变化时提供局部电荷，因此可以降低瞬态电压波动。

---

# 3. EM 修复

## 3.1 EM 是什么

Electromigration（EM）与**电流密度**密切相关。因此 EM 修复核心：
**降低单位面积电流密度。**

---

## 3.2 Metal EM

### 方法 1：加宽 metal

---

### 方法 2：增加并行金属

把一根高电流线拆成多条分摊电流。

---

### 方法 3：换到更高金属层

高层 metal 通常具有更大的 routing resource 和更适合大电流传输的几何尺寸。因此高电流 PG / clock / signal 可以根据工艺规则考虑向更高层迁移。

---

### 方法 4：增加 via 数量
并联 via 可以降低等效电阻和局部电流密度。

---

## 3.3 Via EM

如果 violation 是 via EM：

优先考虑：

1. 增加 via 数量
2. 使用 via array
3. 增加并行路径
4. 改善上下层 metal 宽度
5. 避免电流集中在单个 via

---

## 3.4 Signal EM

对于 signal EM，可以考虑：

- 降低 driver strength（如果 timing 允许）
- 缩短 wire
- 增加 metal width
- 增加 via
- 优化 buffer location
- 减小过大的负载

---

# 4. Noise 修复

## 4.1 Noise 的主要来源

数字 IC 中常见 signal integrity noise 包括：

- Crosstalk
- Capacitive coupling
- Inductive coupling
- Aggressor switching

最常见的是Aggressor 翻转导致 victim 上产生噪声。

---

# 4.2 Noise 修复方法

## 方法 1：增加 spacing
尤其适合：

- 长 parallel run
- timing-critical net
- clock net
- reset net
- high-speed signal

---

## 方法 2：减少 parallel run length
平行距离非常长，可以 reroute，减少 coupling length。

---

## 方法 3：Shield

例如使用 VSS/VDD shield：

```text
VSS | Signal | VSS
```

降低 aggressor 对 victim 的耦合。

常用于：

- clock
- reset
- 高速控制信号
- 特殊关键 net

---

## 方法 4：降低 aggressor slew
如果 aggressor transition 太快，可以考虑：
- 降低 driver strength
- 调整 buffer
- 增加合理负载

但必须检查 timing。

---

## 方法 5：增强 victim driver

如果 victim 本身很弱，可以适当 upsizing，提高 victim 对噪声的容忍能力。

---

# 5. Antenna Effect 修复

## 5.1 Antenna 是什么

Antenna effect 主要发生在制造过程中：

> 长金属在某些工艺阶段连接到 MOS gate，可能积累电荷并对 gate oxide 造成损伤。

因此 antenna violation 常与：

```text
metal area / gate area
```

相关。

---

# 5.2 方法 1：Jumper / Layer hopping
目的：
> 减少制造阶段与 gate 相连的低层 metal 面积。

---

## 5.3 方法 2：Antenna diode

增加 antenna diode，让积累电荷有泄放路径。

优点：

- 局部有效
- 对严重 antenna violation 很直接

缺点：

- 增加面积
- 增加 capacitance
- 可能影响 timing
- 增加 leakage / power

---

## 5.4 方法 3：重新 routing

对于局部严重 antenna：

```text
rip-up
   ↓
change routing layer
   ↓
insert jumper
   ↓
reroute
```

通常比单纯插 diode 更适合大规模优化。

---

# 6. 四类问题的修复对照表

| Violation | 核心物理原因 | 优先修复 |
|---|---|---|
| IR-Drop | PDN R 太大 / 局部 I 太大 | 加宽 PG、增加 stripe、via、decap、优化 power density |
| EM | 电流密度过高 | 加宽 metal、增加并行线、增加 via、换高层 |
| Noise | coupling 太强 / victim 太弱 | spacing、缩短 parallel run、shield、优化 driver |
| Antenna | metal/gate antenna ratio 过大 | jumper、换层、diode、reroute |

---
