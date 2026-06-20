# 硬件设计文档

## 采购链接

| 模块 | 链接 |
|------|------|
| ESP32-WROOM-32 开发板 | https://detail.tmall.com/item.htm?id=805161973303&skuId=5879086331469 |
| 陀螺仪模块 (MPU6050/GY-521) | https://detail.tmall.com/item.htm?id=729656168752&skuId=5367169145529 |
| PM11锂电池包 (3.7V+充电+升压5V/2.4A) | https://item.taobao.com/item.htm?id=1007451636387&skuId=6002389453662 |
| SS-12D00 滑动开关 | 待补充 |
| JST-PH 2.0 座子 | 待补充 |

---

## 芯片选型说明

### 为什么选 ESP32-WROOM-32？

| 对比 | ESP32-WROOM-32 | ESP32-C3 | nRF52840 |
|------|----------------|----------|----------|
| 内核 | Xtensa 双核 240MHz | RISC-V 单核 160MHz | Cortex-M4 64MHz |
| BLE | 5.0 | 5.0 | 5.0 |
| WiFi | 2.4GHz | 2.4GHz | 无 |
| Deep Sleep | ~7 μA | ~5 μA | ~2 μA |
| 价格 | ~¥15 (合宙) | ~¥15 | ~¥15 |
| 开发难度 | Arduino/ESP-IDF | Arduino/ESP-IDF | nRF SDK/Zephyr |

ESP32-WROOM-32 性价比高，有 WiFi+BLE 双模，开发生态成熟。

### 为什么选 MPU6050？

| 对比 | MPU6050 | ADXL345 | LIS3DH |
|------|---------|---------|--------|
| 轴数 | 6 轴 (加速度+陀螺仪) | 3 轴 (仅加速度) | 3 轴 (仅加速度) |
| 接口 | I2C / SPI | I2C / SPI | I2C / SPI |
| 运动中断 | 支持 | 支持 | 支持 |
| DMP | 内置数字运动处理器 | 无 | 无 |
| 价格 | ~¥25 (GY-521) | ~¥5 | ~¥6 |

MPU6050 有内置 DMP 可硬件计算姿态角，减轻 MCU 负担；6 轴数据可同时用角度和振动两种判据，准确率更高。

---

## 模块尺寸与引脚

### ESP32-WROOM-32 开发板 (合宙)

![ESP32-WROOM-32 引脚图](images/esp32-wroom-32-pinout.jpg)

```
尺寸: 51.85 × 23.5 mm
引脚: 2 × 15pin 排针, 2.54mm 间距, 排针间距 23.5mm
安装孔: 4× φ3mm, 距边 3mm

             USB-C (下方)
      ─────────────────────────────────┐
      │ O                             O │ ← 安装孔 φ3mm
  GND │ ●  [ESP32-WROOM-32]          ● │ GND
   5V │ ●                             ● │ 3V3
  IO0 │ ●                             ● │ IO10
  IO1 │ ●                             ● │ IO9
  IO2 │ ●  ← INT (唤醒)              ● │ IO8
  IO3 │ ●                             ● │ IO7
  IO4 │ ●  ← SDA                     ● │ IO6
  IO5 │ ●  ← SCL                     ● │ IO5
   RX │ ●                             ● │ TX
      │ O                             O │
      ─────────────────────────────────┘
        ←──── 51.85mm ────→

实际引脚定义 (从图片):
左列 (上→下): EN, GPIO15, GPIO14, GPIO13, GPIO12, GPIO11, GPIO10, GPIO9, GPIO8, GPIO7, GPIO6, GPIO5, GPIO4, GPIO3, GPIO2, GND, VIN
右列 (上→下): GPIO23, GPIO22, GPIO21, GPIO19, GPIO18, GPIO5, GPIO17, GPIO16, GPIO4, GPIO2, GPIO15, GPIO13, GND, VCC 3V3

本设计使用:
  - GPIO4 → SDA (I2C 数据)
  - GPIO5 → SCL (I2C 时钟)
  - GPIO2 → MPU6050 INT (运动中断唤醒)
  - 5V/VIN → 电源输入 (PM11 升压 5V)
  - GND → 共地
```

### GY-521 模块 (MPU6050)

```
尺寸: 15.6 × 20.2 mm
重量: ~15g
引脚: 1 × 8pin 单排, 2.54mm 间距

      ┌──────────────┐
      │              │
      │  [MPU6050]   │  ← 15.6mm
      │   GY-521     │
      │              │
      └─┬─┬─┬─┬─┬─┬─┬┘
        │ │ │ │ │ │ │ │
       VCC GND SCL SDA XDA XCL AD0 INT
       ↑
       20.2mm

本设计使用 (5 根):
  - VCC → 3V3
  - GND → GND
  - SCL → ESP32 GPIO5
  - SDA → ESP32 GPIO4
  - INT → ESP32 GPIO2
未使用: XDA, XCL, AD0 (AD0 默认接 GND, I2C 地址 0x68)
```

### PM11锂电池包 (自带充电+升压)

```
尺寸: ~40 × 20 × 12mm (含外壳)
接口: JST-PH 2.0 (输出 5V/2.4A)

功能:
  - 3.7V LiPo 电池内置
  - TP4056 充电电路 (Type-C 充电)
  - 升压模块5V/2.4A输出
  - 低电量保护

本设计使用:
  - 5V 输出 → 滑动开关 → ESP32 VIN
  - GND → ESP32 GND
  - 充电口外露, 无需载板走线
```

---

## 接线图

```
ESP32-WROOM-32         外设
────────────          ────
GPIO4 (SDA) ─────────── MPU6050 SDA
GPIO5 (SCL) ─────────── MPU6050 SCL
GPIO2       ─────────── MPU6050 INT (运动中断唤醒)

3V3  ────────────────── MPU6050 VCC
GND  ────────────────── MPU6050 GND


电源部分:
                 ┌───────────────
 USB ─────────→ │ PM11 电池模块  │
                │  (内置充电+升压) │
                │               │
                │  5V OUT ──────┼──→ 滑动开关 ──→ ESP32 VIN (5V)
                │  GND    ──────┼──→ ESP32 GND
                ───────────────┘

注: PM11 模块内置 3.7V 电池 + TP4056 充电 + 升压到 5V/2.4A。
    JST 接口输出 5V, 经滑动开关接入 ESP32 VIN。
    ESP32 板载 LDO 将 5V 稳压到 3.3V, 3.3V 引脚供 MPU6050 使用。
```

---

## 供电设计

### PM11 电池模块

```
     USB ──→ [PM11 模块]
             ┌─────────────────────┐
             │  3.7V LiPo 电池      │
             │  TP4056 充电电路     │
             │  升压 5V/2.4A        │
             │                     │
     JST ──→ │  5V OUT ──→ 开关 ──→ ESP32 VIN
             │  GND  ──→ GND        │
             └─────────────────────┘
```

- **充电**: PM11 自带 USB 充电口，插入即可充电
- **升压**: 内置升压电路，JST 输出稳定 5V/2.4A
- **开关**: 滑动开关串联在 5V 输出和 ESP32 VIN 之间，物理断电
- **ESP32 稳压**: ESP32 板载 LDO 将 5V 转为 3.3V，3.3V 引脚供 MPU6050

### 功耗估算

| 状态 | 电流 | 时间占比 |
|------|------|----------|
| ESP32 Deep Sleep | ~7 μA | ~99.5% |
| 唤醒 + MPU6050 读取 | ~30 mA | ~0.3% (每 2s 唤醒, 读取 ~15ms) |
| BLE 广播 (状态变化时) | ~50 mA | ~0.2% (~5ms/次) |

**平均功耗: ~0.15 mA**

> 1000mAh LiPo 电池理论续航 ≈ 1000 / 0.15 ≈ 6666 小时 ≈ **277 天**
> 考虑电池自放电和效率损耗，保守估计 **~6 个月**，Type-C 随时可充。

---

## 载板 PCB 设计

### 概述

载板 (Carrier Board) 用于插接两个现成开发板模块（ESP32-WROOM-32、GY-521），通过 PCB 走线完成模块间互连，替代杜邦线。板上集成滑动开关。电池使用 PM11锂电池包（自带充电+升压 5V/2.4A），无需额外充放电模块。

### 规格参数

| 参数 | 值 |
|------|-----|
| PCB 尺寸 | 80mm × 50mm (2 层) |
| 工作电压 | 5V (PM11 电池模块升压输出) |
| 模块插接 | 排母座 2.54mm 间距 |
| 电池接口 | PM11 自带 JST 接口 (直连载板) |
| 开关 | SS-12D00 滑动开关 |
| 扩展 | 预留 4 个 GPIO 排针 |

### 载板原理图

```
                       载板 PCB 连接关系
┌──────────────────────────────────────────────────────────┐
│                                                          │
│  PM11 电池模块 (5V 输出)                                  │
│   5V ──────── SS-12D00 开关 ─────── ESP32 VIN (5V)       │
│   GND ─────── GND (共地总线)                              │
│                                                          │
│  ESP32 3V3 ──────── GY-521 VCC                           │
│  ESP32 GND ──────── GY-521 GND                           │
│  ESP32 GPIO4 ────── GY-521 SDA                           │
│  ESP32 GPIO5 ────── GY-521 SCL                           │
│  ESP32 GPIO2 ────── GY-521 INT                           │
│                                                          │
│  扩展排针: GPIO3, GPIO6, GPIO7, GPIO8 (预留)              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

### PCB 布局建议

```
              80mm
┌──────────────────────────────────┐
│                                  │  ↑
│  ┌──────────────┐  ┌─────────┐  │
│  │  ESP32-WROOM │  │ GY-521  │  │
│  │  -32         │  │ MPU6050 │  │  50mm
│  │  (排母 2×15)  │  │(排母1×8)│  │
│  │              │  │         │  │
│  └──────────────  └─────────┘  │
│                                  │
│  [开关]  [PM11电池JST]           │
│  SS-12D00  JST-PH 2P             │
│  ○ ○ ○ ○                         │
│  扩展GPIO                        │
│          ↑ USB-C 充电口朝外       │
──────────────────────────────────┘

安装孔: 四角 M3 (φ3.2mm), 距边 3mm
```

### 布线规则

| 参数 | 值 |
|------|-----|
| 最小线宽 | 10mil (0.254mm) |
| 电源线 (VIN/3V3) | 20mil (0.5mm) |
| GND | 大面积铺铜 |
| 最小间距 | 8mil |
| 过孔 | 0.3mm 孔径 / 0.6mm 焊盘 |
| 板厚 | 1.6mm |
| 铜厚 | 1oz |

### 载板 BOM

| # | 元件 | 型号/规格 | 封装 | 数量 | 备注 |
|---|------|----------|------|:----:|------|
| 1 | 排母座 (ESP32) | 1×15P 2.54mm | 直插 | 2 | 双排插接 ESP32-WROOM-32 |
| 2 | 排母座 (MPU6050) | 1×8P 2.54mm | 直插 | 1 | 插接 GY-521 |
| 3 | 滑动开关 | SS-12D00 | 直插 3P | 1 | 电源通断 |
| 4 | JST-PH 座子 | PH 2.0mm 2P | 卧式直插 | 1 | PM11 电池接口 |
| 5 | 排针 (扩展) | 1×4P 2.54mm | 直插 | 1 | 预留 GPIO 扩展 |
| 6 | PCB 打样 | 80×50mm 2层 | - | 5 | 嘉立创 5 片起打 |

**载板物料合计: ≈ ¥5**

---

## 载板接线表 (立创 EDA 直接可用)

> ⚠️ **重要**: 以下引脚定义基于常见 ESP32-WROOM-32 排布。收到板后**务必用万用表核对丝印**，如有差异在此更新。

### ESP32-WROOM-32 排母 (2×15P, 双排)

```
排母 A (左侧, 1×15P):
Pin 1  → GND
Pin 2  → 3V3  (板载 LDO 输出 3.3V, 供 MPU6050)
Pin 3  → GPIO0 (BOOT, 烧录用)
Pin 4  → GPIO1 (预留扩展)
Pin 5  → GPIO2 (MPU6050 INT 中断唤醒)
Pin 6  → GPIO3 (预留扩展)
Pin 7  → GPIO4 (MPU6050 SDA, I2C 数据)
Pin 8  → GPIO5 (MPU6050 SCL, I2C 时钟)
Pin 9  → GND
Pin 10 → 5V
Pin 11 → GPIO4
Pin 12 → GPIO5
Pin 13 → GPIO6 (预留扩展)
Pin 14 → GPIO7 (预留扩展)
Pin 15 → GND

排母 B (右侧, 1×15P):
Pin 1  → GND
Pin 2  → VIN  (5V 输入, 经开关接 PM11 5V OUT)
Pin 3  → GPIO8  (预留扩展)
Pin 4  → GPIO9  (预留扩展)
Pin 5  → GPIO10 (预留扩展)
Pin 6  → RX     (预留扩展)
Pin 7  → TX     (预留扩展)
Pin 8  → GPIO18 (预留扩展)
Pin 9  → GPIO19 (预留扩展)
Pin 10 → GND
Pin 11-15 → NC
```

### GY-521 MPU6050 排母 (1×8P)

```
Pin 1  → VCC  (接 ESP32 3V3)
Pin 2  → GND  (接 ESP32 GND)
Pin 3  → SCL  (接 ESP32 GPIO5)
Pin 4  → SDA  (接 ESP32 GPIO4)
Pin 5  → XDA  → 不接 (I2C 辅助, 用不到)
Pin 6  → XCL  → 不接
Pin 7  → AD0  → 不接 (默认 GND, I2C 地址 0x68)
Pin 8  → INT  (接 ESP32 GPIO2)
```

### PM11 电池模块 JST-PH 2P

```
Pin 1 (红) → 5V OUT (经 SS-12D00 开关 → ESP32 VIN)
Pin 2 (黑) → GND (直连 ESP32 GND)
```

### SS-12D00 滑动开关 (3P)

```
Pin 1 → PM11 5V OUT (常开端)
Pin 2 → 公共端 → ESP32 VIN
Pin 3 → 悬空 (或接 Pin1 作常闭)
```

### 扩展排针 (1×4P)

```
Pin 1 → GPIO1 (可复用)
Pin 2 → GPIO3 (可复用)
Pin 3 → GPIO6 (可复用)
Pin 4 → GND
```

---

## 载板网络表 (立创 EDA 原理图画线用)

| 网络名 | 起点 | 终点 | 线宽建议 |
|--------|------|------|----------|
| 5V_PM11 | JST Pin1 | 开关 Pin1 | 20mil |
| VIN_SW | 开关 Pin2 | ESP32 VIN (排母B Pin2) | 20mil |
| GND | JST Pin2 → ESP32 GND → GY521 GND | 大面积铺铜 | 铺铜 |
| 3V3 | ESP32 3V3 (排母A Pin2) → GY521 VCC | 15mil |
| I2C_SDA | ESP32 GPIO4 (排母A Pin7) → GY521 SDA | 10mil |
| I2C_SCL | ESP32 GPIO5 (排母A Pin8) → GY521 SCL | 10mil |
| MPU_INT | ESP32 GPIO2 (排母A Pin5) → GY521 INT | 10mil |
| EXT1 | ESP32 GPIO1 (排母A Pin4) → 扩展 Pin1 | 10mil |
| EXT2 | ESP32 GPIO3 (排母A Pin6) → 扩展 Pin2 | 10mil |
| EXT3 | ESP32 GPIO6 (排母B Pin3) → 扩展 Pin3 | 10mil |
| EXT_GND | ESP32 GND → 扩展 Pin4 | 铺铜 |

---

## 立创 EDA 操作步骤

### 1. 新建项目

1. 打开 https://lceda.cn → 登录 → 新建项目 → "Sedentary-Detector-CarrierBoard"
2. 新建原理图

### 2. 放置元件

| 搜索关键词 | 元件 | 数量 |
|-----------|------|:----:|
| `Header Female 1x15` | 2.54mm 排母 1×15P | 2 |
| `Header Female 1x8` | 2.54mm 排母 1×8P | 1 |
| `SS-12D00` | 滑动开关 | 1 |
| `JST PH 2P` 或 `B2B-PH-SM` | JST-PH 2.0 座子 | 1 |
| `Header Male 1x4` | 2.54mm 排针 1×4P | 1 |

### 3. 原理图连线

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

### 4. 转 PCB 并布局

1. 菜单 → `设计` → `原理图转PCB`
2. 设置板框: 80 × 50mm
3. 按"PCB 布局建议"摆放元件
4. 四角放 M3 安装孔 (焊盘 → 过孔 → φ3.2mm)
5. 手动布线 / 自动布线
6. 底层铺铜 GND

### 5. 检查与下单

1. `设计` → `DRC 检查` → 修正所有错误
2. `制造` → `PCB 订单` → 预览 Gerber
3. 选: 2 层, 1.6mm, 绿油白丝印, 5 片
4. 嘉立创新用户首单免费

---

## 3D 底座配合

载板 PCB 四角 M3 安装孔与 3D 打印底座对应:

```
底座截面 (侧视):

    ┌─ 载板 PCB ──────────┐
    │  (M3 螺丝固定)       │
 ───┴──────────────────────┴───  ← 底座上表面
 │         LiPo 电池            │  ← 电池仓 (底座内)
 │         (扁平软包)            │
 └──────────────────────────────┘  ← 底座底面 (贴椅子)
         ↑ 双面胶/扎带固定到椅子
```

底座内部预留:
- 电池仓: 50 × 30 × 8mm (适配 1000mAh 扁平 LiPo)
- PCB 固定柱: 4 个 M3 铜柱, 高度 10mm (电池上方)
- Type-C 开口: 侧面留缺口
- 开关开口: 侧面留缺口
