# Sedentary Detector ESP32 - 久坐检测器

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.1.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Status-硬件方案设计中-yellow" alt="Status">
  <img src="https://img.shields.io/badge/Platform-ESP32--C3-green" alt="Platform">
  <img src="https://img.shields.io/badge/Power-3.7V_LiPo-orange" alt="Power">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

基于 ESP32-C3 + MPU6050 陀螺仪的椅子久坐检测器。安装在椅子坐垫下方，通过检测坐垫倾斜角度变化判断是否有人坐，超时提醒起身活动。内置锂电池充放电，Type-C 充电，滑动开关控制电源。

**开发策略**: 全部使用现成开发板模块，设计一块载板 PCB 将各模块插接互连，配合 3D 打印底座固定。模块可拆卸替换，方便快速迭代。

---

## 检测原理

MPU6050 加速度计测量重力向量方向。坐下时椅子坐垫受力产生微小倾斜，加速度分量变化，据此判断有人/无人状态。

```
无人状态                         有人状态
┌──────────────┐               ┌──────────────┐
│   ═══坐垫═══  │               │ 👤 ══坐垫══↘  │
│    (水平)     │               │   (倾斜 1-3°) │
│              │               │              │
│  [MPU6050]   │               │  [MPU6050]   │
│  Z轴 = 1g   │               │  Z轴 < 1g    │
│  X/Y轴 ≈ 0  │               │  X/Y轴 ≠ 0   │
└──────────────┘               └──────────────┘
  角度 ≈ 0°                      角度 ≈ 1-3° → 有人！
```

辅助判据：
- **振动检测**: 人坐着会产生持续微振动（翻身、打字、呼吸），无人时完全静止
- **坐下/站起冲击**: 坐下和站起瞬间加速度有明显脉冲

---

## 系统架构

```
               ┌──────────────────────────────────┐
               │        3D 打印底座 (椅子下方)       │
               │  ┌─ 载板 PCB ─────────────────┐  │
               │  │                            │  │
               │  │  [GY-521]   I2C   [ESP32]  │  │
               │  │  MPU6050  ══════  C3 Mini  │──→ BLE / WiFi
               │  │  (插接)    SDA    (插接)    │  │
               │  │           SCL     ↑ 5V     │  │
               │  │                   │        │  │
               │  │  [PM11]──[开关]───┘        │  │
               │  │  电池包                     │  │
               │  │  (JST)                      │  │
               │  └────────────────────────────┘  │
               │      ↑ PM11 USB 充电口外露        │
               └──────┼───────────────────────────┘
                      │
                   USB 充电
```

载板 PCB 上焊排母座，各开发板模块插接，PCB 走线完成互连。无杜邦线，整洁可靠。

---

## 硬件选型

> 全部使用现成开发板模块，载板 PCB 走线互连，底座固定。

### 物料清单 (BOM)

| 物料 | 型号 | 数量 | 单价(约) | 说明 |
|------|------|:----:|----------|------|
| 主控模块 | ESP32-C3 Mini 开发板 | 1 | ~4 元 | CP2102 Type-C, WiFi+BLE, 板载 LDO |
| 陀螺仪模块 | GY-521 (MPU6050) | 1 | ~3 元 | 6 轴加速度+陀螺仪, I2C, 含上拉 |
| 电池模块 | PM11锂电池包 (3.7V+充电+升压5V/2.4A) | 1 | ~19 元 | 内置电池+充电+升压, JST 输出, 兼容积木 |
| 开关 | SS-12D00 滑动开关 | 1 | ~0.5 元 | 串联在电源通路上 |
| 载板 PCB | 定制 PCB (嘉立创打样) | 1 | ~5 元 | 5片起打, 排母座插接各模块 |
| 排母座 | 2.54mm 排母 | 若干 | ~2 元 | 焊在载板上, 模块插入 |
| 电池接口 | JST-PH 2.0 座子 | 1 | ~0.5 元 | PM11 电池可插拔 |
| 底座 | 3D 打印 (PLA) | 1 | ~3 元 | 固定载板 PCB + 电池 |
| **合计** | | | **~37 元** | |

### 芯片选型说明

**为什么选 ESP32-C3？**

| 对比 | ESP32-C3 | ESP32-S3 | nRF52840 |
|------|----------|----------|----------|
| 内核 | RISC-V 单核 160MHz | Xtensa 双核 240MHz | Cortex-M4 64MHz |
| BLE | 5.0 | 5.0 | 5.0 |
| WiFi | 2.4GHz | 2.4GHz | 无 |
| Deep Sleep | ~5 μA | ~7 μA | ~2 μA |
| 价格 | ~8 元 | ~15 元 | ~15 元 |
| 开发难度 | Arduino/ESP-IDF | Arduino/ESP-IDF | nRF SDK/Zephyr |

ESP32-C3 性价比最高，有 WiFi+BLE 双模，Deep Sleep 功耗够低，开发生态好。

**为什么选 MPU6050？**

| 对比 | MPU6050 | ADXL345 | LIS3DH |
|------|---------|---------|--------|
| 轴数 | 6 轴 (加速度+陀螺仪) | 3 轴 (仅加速度) | 3 轴 (仅加速度) |
| 接口 | I2C / SPI | I2C / SPI | I2C / SPI |
| 运动中断 | 支持 | 支持 | 支持 |
| DMP | 内置数字运动处理器 | 无 | 无 |
| 价格 | ~4 元 | ~5 元 | ~6 元 |

MPU6050 有内置 DMP 可硬件计算姿态角，减轻 MCU 负担；6 轴数据可同时用角度和振动两种判据，准确率更高。

---

## 接线图

```
ESP32-C3 Mini          外设
────────────          ────
GPIO4 (SDA) ─────────── MPU6050 SDA
GPIO5 (SCL) ─────────── MPU6050 SCL
GPIO2       ─────────── MPU6050 INT (运动中断唤醒)

3V3  ────────────────── MPU6050 VCC
GND  ────────────────── MPU6050 GND


电源部分:
                 ┌───────────────┐
 USB ─────────→ │ PM11 电池模块  │
                │  (内置充电+升压) │
                │               │
                │  5V OUT ──────┼──→ 滑动开关 ──→ ESP32-C3 VIN (5V)
                │  GND    ──────┼──→ ESP32-C3 GND
                └───────────────┘

注: PM11 模块内置 3.7V 电池 + TP4056 充电 + 升压到 5V/2.4A。
    JST 接口输出 5V, 经滑动开关接入 ESP32-C3 Mini VIN。
    ESP32-C3 Mini 板载 LDO 将 5V 稳压到 3.3V, 3.3V 引脚供 MPU6050 使用。
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
- **ESP32 稳压**: ESP32-C3 Mini 板载 LDO 将 5V 转为 3.3V，3.3V 引脚供 MPU6050

### 功耗估算

| 状态 | 电流 | 时间占比 |
|------|------|----------|
| ESP32-C3 Deep Sleep | ~5 μA | ~99.5% |
| 唤醒 + MPU6050 读取 | ~30 mA | ~0.3% (每 2s 唤醒, 读取 ~15ms) |
| BLE 广播 (状态变化时) | ~50 mA | ~0.2% (~5ms/次) |

**平均功耗: ~0.15 mA**

> 1000mAh LiPo 电池理论续航 ≈ 1000 / 0.15 ≈ 6666 小时 ≈ **277 天**
> 考虑电池自放电和效率损耗，保守估计 **~6 个月**，Type-C 随时可充。

---

## 检测逻辑

### 状态机

```
            坐下 (角度变化 > 阈值, 持续 3s 确认)
  ┌────────┐ ─────────────────────→ ┌─────────┐
  │  无人   │                        │  有人    │
  │(VACANT)│ ←───────────────────── │(OCCUPIED)│
  └────────┘  站起 (角度恢复, 持续 5s) └────┬────┘
                                        │
                                  连续坐 ≥ 45min
                                        ↓
                                  久坐提醒 (BLE 通知)
                                        │
                                  每隔 15min 再次提醒
```

### 判定算法

```
1. 基准校准 (上电时):
   - 记录无人状态下的基准倾斜角 baseline_angle

2. 每次唤醒:
   - 读取 MPU6050 加速度数据
   - 计算当前倾斜角 current_angle
   - delta = |current_angle - baseline_angle|
   - 计算振动幅度 vibration (加速度标准差)

3. 判定:
   - delta > 1.0° AND vibration > threshold → 有人
   - delta < 0.5° AND vibration < quiet_threshold → 无人
   - 中间值 → 维持当前状态 (滞回)

4. 去抖:
   - 状态切换需连续 N 次 (3-5次) 确认
```

### 参数配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 采样间隔 | 2s | Deep Sleep RTC 唤醒周期 |
| 角度阈值 (坐下) | 1.0° | 倾斜角变化超过此值判定有人 |
| 角度阈值 (站起) | 0.5° | 回到此范围内判定无人 (滞回) |
| 去抖次数 | 3 次 | 连续确认次数 |
| 久坐阈值 | 45 min | 连续有人超过此时间触发提醒 |
| 重复提醒间隔 | 15 min | 久坐后每隔此时间再次提醒 |
| 心跳间隔 | 5 min | 定时上报状态 |

---

## 通信方式

### BLE 广播 (默认)

无需配对，通过 BLE Manufacturer Specific Data 广播状态：

```
Manufacturer Specific Data (AD Type 0xFF):

Byte 0-1: Company ID = 0xFFFF (测试用)
Byte 2:   Message Type
            0x01 = 状态变化
            0x02 = 心跳
            0x03 = 久坐提醒
            0x04 = 低电量
Byte 3:   Occupancy State (0x00=无人, 0x01=有人)
Byte 4-5: 久坐时长 (uint16, 分钟)
Byte 6:   电池电量 (0-100%)
Byte 7:   当前倾斜角 (int8, 度×10)
```

### WiFi/MQTT (可选)

通过 WiFi 连接 MQTT Broker，上报到 Home Assistant：

```
Topic: home/chair/desk/status      → "occupied" / "vacant"
Topic: home/chair/desk/duration    → 久坐时长 (分钟)
Topic: home/chair/desk/battery     → 电量 (%)
Topic: home/chair/desk/angle       → 当前倾斜角 (度)
```

> WiFi 模式功耗较高 (~100mA 连接时)，建议仅在状态变化时短暂开启 WiFi 上报后关闭。

---

## 项目结构

```
APP-Sedentary-Detector-ESP32/
├── README.md                    # 项目说明 (本文件)
├── LICENSE                      # MIT
├── firmware/                    # ESP32-C3 固件
│   ├── src/
│   │   ├── main.cpp             # 主逻辑: 初始化、主循环、Deep Sleep
│   │   ├── mpu6050.h / .cpp     # MPU6050 驱动 (I2C, DMP)
│   │   ├── detector.h / .cpp    # 久坐检测算法 (状态机, 角度判定)
│   │   ├── ble_adv.h / .cpp     # BLE 广播管理
│   │   ├── power.h / .cpp       # 电源管理 (Deep Sleep, 电池电量)
│   │   └── config.h             # 参数配置 (阈值、时间)
│   └── platformio.ini           # PlatformIO 工程配置
├── hardware/                    # 载板 PCB 设计
│   ├── PCB_DESIGN.md            # 载板设计说明
│   ├── BOM.csv                  # 物料清单
│   └── kicad/ 或 easyeda/       # PCB 工程文件
├── mechanical/                  # 3D 打印底座
│   └── base.stl                 # 底座模型
└── docs/
    └── calibration.md           # 校准指南
```

---

## 开发计划

### Phase 1: 硬件验证 (当前)

- [ ] 购买 ESP32-C3 Mini + GY-521 + TP4056 模块
- [ ] 面包板搭建原型，验证接线
- [ ] 测试 MPU6050 数据读取 (加速度、角度)
- [ ] 实测椅子坐下/站起时的角度变化数据
- [ ] 确定安装位置和固定方式

### Phase 2: 载板 PCB + 固件开发

- [ ] 设计载板 PCB (排母座插接各模块)
- [ ] 嘉立创打样、焊接排母座和开关
- [ ] MPU6050 驱动 (I2C 通信 + DMP 姿态解算)
- [ ] 坐人检测算法 (角度 + 振动双判据)
- [ ] Deep Sleep + RTC 定时唤醒
- [ ] MPU6050 Motion Interrupt 唤醒
- [ ] BLE 广播实现
- [ ] 久坐计时与提醒逻辑
- [ ] 电池电量检测 (ADC)
- [ ] 功耗实测与优化

### Phase 3: 整合测试

- [ ] 3D 底座设计与打印
- [ ] 载板 + 电池装入底座
- [ ] 安装到椅子上
- [ ] 长时间稳定性测试 (24h+)
- [ ] 误判率统计与阈值调优
- [ ] 实际功耗测量

---

## License

MIT
