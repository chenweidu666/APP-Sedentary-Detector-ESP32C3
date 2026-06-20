# 立创 EDA 操作步骤

[← 硬件文档索引](../HARDWARE.md) · [载板设计](design.md) · [网络表](nets.md)

## 1. 新建项目

1. 打开 https://lceda.cn → 登录 → 新建项目 → "Sedentary-Detector-CarrierBoard"
2. 新建原理图

## 2. 放置元件

| 搜索关键词 | 元件 | 数量 |
|-----------|------|:----:|
| `PinSocket 2x15` 或 `Header Female 2x15` | 2.54mm 排母 2×15P | 1 |
| `Header Female 1x8` | 2.54mm 排母 1×8P | 1 |
| `SS-12D00` | 滑动开关 | 1 |
| `JST PH 2P` 或 `B2B-PH-SM` | JST-PH 2.0 座子 | 1 |
| `Header Male 1x4` | 2.54mm 排针 1×4P | 1 |

## 3. 原理图连线

```
网络名       连接
─────       ────
VIN         PM11.5V → SW.COM → ESP32.VIN
3V3         ESP32.3V3 → GY521.VCC
GND         ESP32.GND → GY521.GND → PM11.GND
SDA         ESP32.GPIO4 → GY521.SDA
SCL         ESP32.GPIO5 → GY521.SCL
INT         ESP32.GPIO2 → GY521.INT
5V          JST.PIN1 (PM11 5V 输出) → 开关
GND_JST     JST.PIN2 (PM11 GND) → GND
```

## 4. 转 PCB 并布局

1. 菜单 → `设计` → `原理图转PCB`
2. 设置板框: 80 × 50mm
3. 按 [`design.md`](design.md) 布局建议摆放元件
4. 四角放 M3 安装孔 (焊盘 → 过孔 → φ3.2mm)
5. 手动布线 / 自动布线
6. 底层铺铜 GND

## 5. 检查与下单

1. `设计` → `DRC 检查` → 修正所有错误
2. `制造` → `PCB 订单` → 预览 Gerber
3. 选: 2 层, 1.6mm, 绿油白丝印, 5 片
4. 嘉立创新用户首单免费

> 本项目 KiCad 工程在 `hardware/kicad/`，Agent 生成脚本见仓库根目录 `Tools/gen_kicad_pcb.py`。
