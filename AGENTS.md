# AGENTS.md — OpenCode Instructions for 02-APP-Sedentary-Detector-ESP32

## Project

久坐检测器载板 PCB (KiCad 10)。**ESP32-WROOM-32** + **GY-87** + **OLED** + PM11（载板无按键/滑动开关）。原理图 **v0.6**；**PCB v0.4** 待改版打样。

## Design authority

**引脚、网络、BOM 的唯一来源**：[`hardware/HARDWARE.md`](hardware/HARDWARE.md)

修改或生成原理图/PCB 前必读：

| 章节 | 内容 |
|------|------|
| §载板全网络表 | J1–J4 网络分配 |
| §J2 排母引脚映射 | GY-87 Pin1=VCC_IN … Pin8=DRDY |
| §OLED 显示屏 | J4 与 I2C 地址 |
| §J3 / PM11 | 5V → ESP32 VIN |
| §PCB 版本记录 | 原理图 vs 已打样 PCB 差异 |

**禁止在本文件重复维护引脚表**——只改 `HARDWARE.md`，避免双份漂移。

### 原理图接线（agent 操作规则）

- **禁止手写 wire** — 用标签（label）放在引脚原点即可创建同名网络连接
- **标签必须放在引脚原点**（与 ERC 报告坐标一致），否则不连接
- 获取正确坐标：跑 `kicad-cli sch erc`，从中 grep 引脚位置
- **不要自己计算坐标** — 符号位置可能变化
- 标签格式见 `../../../Skills/sedentary-kicad/SKILL.md`
- 网络名：`3V3`, `5V`, `GND`, `I2C_SCL`, `I2C_SDA`, `MPU_INT`
- J2 Pin2/6/8 悬空，不加标签

通用 Agent PCB 工作流见 monorepo 文档：[`Docs/KiCad/agent-pcb-design.md`](../../Docs/KiCad/agent-pcb-design.md)。

## KiCad 安装

| 组件 | 路径 / 版本 |
|------|-------------|
| GUI + CLI | `/usr/bin/kicad`, `/usr/bin/kicad-cli` — **10.0.4** (PPA `kicad-10.0-releases`) |
| 符号库 | `/usr/share/kicad/symbols/` |
| 封装库 | `/usr/share/kicad/footprints/` |
| pcbnew API | `/usr/lib/python3/dist-packages/pcbnew.py` (系统 Python 3.12) |

打开工程：

```bash
kicad hardware/kicad/SedentaryDetector.kicad_pro
```

`~/.local/bin/kicad` 是干净启动器（剥离 conda 干扰），始终调用系统 KiCad。**不要用 conda base 环境直接启动 KiCad GUI。**

## Conda 环境 `kicad_env`

专用于 KiCad 脚本（`pcbnew` API、`kiutils` 生成文件），与 GUI 分离。

```bash
# 首次创建（已配置则跳过）
conda env create -f Tools/kicad-env/environment.yml

# 激活
conda activate kicad_env

# 推荐：用包装脚本（自动设置 pcbnew 路径）
Tools/kicad-env/kicad-python hardware/scripts/gen_sch.py
Tools/kicad-env/kicad-python Tools/gen_kicad_pcb.py
```

包装脚本设置：

- `PYTHONPATH=/usr/lib/python3/dist-packages` — 加载系统 `pcbnew`
- `LD_LIBRARY_PATH=/usr/lib/kicad/lib`
- `KICAD_STOCK_DATA_HOME=/usr/share/kicad`
- `PYTHONNOUSERSITE=1` — 避免 conda 包污染 pcbnew

**规则：**

- GUI / `kicad-cli` → 系统 `/usr/bin/`，不经过 conda
- Python 生成脚本 → `kicad_env` + `kicad-python` 包装器
- 不要在 `kicad_env` 里 `pip install pcbnew`（必须用系统自带的）

## 工程文件

| 文件 | 说明 |
|------|------|
| `hardware/kicad/SedentaryDetector.kicad_pro` | 工程入口 |
| `hardware/kicad/SedentaryDetector.kicad_sch` | 原理图 |
| `hardware/kicad/SedentaryDetector.kicad_pcb` | PCB |
| `hardware/kicad/fp-lib-table` | 封装库表 |
| `hardware/kicad/sym-lib-table` | 符号库表 |
| [`Docs/KiCad/TROUBLESHOOTING.md`](../../Docs/KiCad/TROUBLESHOOTING.md) | KiCad 踩坑（monorepo） |

## 生成脚本

脚本在 `hardware/scripts/`，输出到 `hardware/kicad/`：

```bash
# 从 HARDWARE.md 逻辑重生成原理图
Tools/kicad-env/kicad-python hardware/scripts/gen_sch.py

# PCB 骨架生成（板框 + 网络定义）
Tools/kicad-env/kicad-python Tools/gen_kicad_pcb.py
```

修改设计后重跑脚本，再在 KiCad GUI 中检查、布局、布线。

## 原理图规则

- 优先使用 `lib_symbols` 内联符号，减少外部库依赖
- 自定义符号命名空间：`CarrierBoard:`
- 实物元件：`in_bom yes`, `on_board yes`；电源符号：`no`
- 引脚 `name` 用功能名（`VCC`, `SDA`），`number` 对应封装焊盘号
- 未用引脚标 `no_connect`
- 网络名必须与 `HARDWARE.md` 网络表一致

## PCB 规则

| 参数 | 值 |
|------|-----|
| 尺寸 | 50mm × 35mm，双层，1.6mm |
| 电源线 | 0.5mm |
| 信号线 | 0.254mm |
| GND | 底层 `B.Cu` 铺铜 |
| 安装孔 | M3，φ3.2mm，距边 3mm |
| 排母 | `PinSocket_*_P2.54mm_Vertical`（不是 PinHeader） |

**禁止手写 `.kicad_pcb` S-expression** — 用 KiCad GUI 或 `pcbnew`/`kiutils` API 生成。详见 [`Docs/KiCad/TROUBLESHOOTING.md`](../../Docs/KiCad/TROUBLESHOOTING.md)。

## 标准封装（KiCad 10 库）

| 元件 | 封装 | 备注 |
|------|------|------|
| J1 ESP32 2×15 排母 | `Connector_PinSocket_2.54mm:PinSocket_2x15_P2.54mm_Vertical` | 排针间距 24.5mm, 板宽 23.5mm |
| J2 GY-87 1×8 排母 | `Connector_PinSocket_2.54mm:PinSocket_1x08_P2.54mm_Vertical` | 见 `hardware/HARDWARE.md` J2 表 |
| J3 JST 电源座 | `Connector_JST:JST_PH_B2B-PH-K_1x02_P2.00mm_Vertical` | |
| J4 OLED 1×4 排母 | `Connector_PinSocket_2.54mm:PinSocket_1x04_P2.54mm_Vertical` | |
| 安装孔 | `MountingHole:MountingHole_3.2mm_M3` | φ3mm |

## ESP32-WROOM-32 模块尺寸

```
排针间距 24.5mm
┌──────────────────────────────────┐
│  O                            O  │ ← 安装孔 φ3mm
│  ●  [ESP32-WROOM-32]          ●  │
│  ●                             ●  │
│  ●                             ●  │
│  ●  ← INT (唤醒)              ●  │
│  ●                             ●  │
│  ●  ← SDA                     ●  │
│  ●  ← SCL                     ●  │
│  ●                             ●  │
│  ●                             ●  │
│  O                            O  │
──────────────────────────────────┘
  23.5mm           51.85mm

引脚: 2 × 19pin 排针, 2.54mm 间距
安装孔: 4× φ3mm, 距边 3mm
```

## CLI 常用命令

```bash
# DRC
kicad-cli pcb drc hardware/kicad/SedentaryDetector.kicad_pcb

# 导出 SVG 预览
kicad-cli pcb export svg hardware/kicad/SedentaryDetector.kicad_pcb \
  -o /tmp/pcb.svg --layers F.Cu,B.Cu,Edge.Cuts --page-size-mode 2

# 导出 Gerber
kicad-cli pcb export gerbers hardware/kicad/SedentaryDetector.kicad_pcb -o hardware/kicad/gerbers/
```

## Agent 工作流（本项目）

```
HARDWARE.md → gen_sch.py → ERC → gen_kicad_pcb.py → GUI 布局/布线 → kicad-cli drc → kicad-happy 评审 → Gerber
```

- **创建**：脚本生成骨架，禁止手写 `.kicad_pcb` S-expression
- **验证**：DRC 通过后，用 kicad-happy 跑 schematic + PCB + EMC + SPICE
- **出板**：Gerber 含 Cu / Edge.Cuts / Mask / Silkscreen / Drill

## kicad-happy（AI 辅助）

仓库根目录 `Tools/kicad-happy/` 已通过 `opencode.json` 注册 skills。用于原理图分析、PCB 审查、EMC、BOM、制板文件等，依赖系统 `kicad-cli`。完整评审清单见 [`Docs/KiCad/agent-pcb-design.md`](../../Docs/KiCad/agent-pcb-design.md#路径-bkicad-happy-辅助审查验证)。

## Python 依赖

| 包 | 环境 | 用途 |
|----|------|------|
| `kiutils` | `kicad_env` | 类型化生成 `.kicad_sch` / `.kicad_pcb`（参考项目 03） |
| `pcbnew` | 系统 Python 3.12 | 运行时加载，不 pip 安装 |

## 当前状态（2026-06-23）

- [x] KiCad 10.0.4 系统安装
- [x] `kicad_env` conda 环境
- [x] 原理图 v0.6：J1/J2/J3/J4（无载板按键/开关）
- [x] PCB 网络分配：J1/J2/J3/J4
- [x] 模块联调：GY-87 → `../04-MCU-GY87-Debug`；OLED → `../03-ESP32-OLED-Button-Demo`
- [x] 本仓库已移除 `software/`（固件不在此维护）
- [ ] PCB 走线：全板待布（v0.4 → v0.6 对齐）
- [ ] DRC 通过
- [ ] 产品固件：合并 03/04 能力后迁入本仓库或独立 app 工程（待定）

## pcbnew API 踩坑（KiCad 10）

### 1. Pad 位置用绝对坐标
```python
# ❌ 相对坐标（KiCad 10 可能不生效）
pd.SetPosition(pcbnew.VECTOR2I(x, y))  # 相对 footprint
fp.Add(pd)

# ✅ 绝对坐标（推荐）
fp_pos_x, fp_pos_y = int(-22*mm), int(-7*pp)
pd.SetPosition(pcbnew.VECTOR2I(fp_pos_x + col*rs, fp_pos_y + row*pp))
```
**原因**: KiCad 10 的 `SetPosition` 行为可能变化，用绝对坐标最安全。

### 2. 清除飞线 (Ratsnest)
```python
# 飞线来自 net 分配。未走线前先不分配 net，避免 KiCad 显示蓝色飞线
nets = board.GetNetsByName()
empty_net = nets['']  # net 0
for fp in board.GetFootprints():
    for pd in fp.Pads():
        pd.SetNet(empty_net)
```

### 3. 禁止手写 S-expression
KiCad 10 格式严格（tab 缩进、uuid 需引号、boolean 用 true/false）。
**始终用 `pcbnew` API 或 KiCad GUI 生成文件。**

### 4. 工作流：先布局后走线
1. pcbnew API 放封装 + 板框 + 丝印 → 在 KiCad GUI 验证
2. 确认布局无误后，再加走线
3. 走线前不要分配 net（避免飞线干扰视觉）

### 5. 常用 API 常量
| 常量 | 值 | 用途 |
|------|-----|------|
| `PAD_ATTRIB_PTH` | 0 | 通孔焊盘 |
| `PAD_ATTRIB_NPTH` | 1 | 非金属化孔 (安装孔) |
| `PAD_SHAPE_CIRCLE` | 0 | 圆形 |
| `PAD_SHAPE_RECT` | 1 | 矩形 |
| `SHAPE_T_SEGMENT` | 0 | 线段 (板框) |
| `F_Cu` / `B_Cu` | - | 顶层/底层铜 |
| `Edge_Cuts` | - | 板框层 |
| `F_SilkS` | - | 顶层丝印 |
| `ZONE_CONNECTION_FULL` | - | 铺铜全连接 |
