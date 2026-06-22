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

## 当前进度

| 模块 | 状态 |
|------|------|
| 硬件方案 | ✅ 已完成 (ESP32-C3 + GY-521 + PM11) |
| 载板 PCB 设计 | ✅ 已完成 (接线表、网络表、立创 EDA 步骤) |
| Wokwi 仿真 | ✅ 已完成 (ESP32 + MPU6050, 检测算法验证) |
| 固件开发 | ⏳ 待开始 |
| 3D 底座 | ⏳ 待设计 |
| 采购 | ⏳ 待下单 |

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

## 硬件成本

| 物料 | 型号 | 单价 | 说明 |
|------|------|------|------|
| 主控模块 | ESP32-C3 Mini 开发板 | ¥35.67 | CP2102 Type-C, WiFi+BLE |
| 陀螺仪模块 | GY-521 (MPU6050) | ¥25.55 | 6轴加速度+陀螺仪, I2C |
| 电池模块 | PM11锂电池包 (3.7V+充电+升压5V/2.4A) | ¥19.00 | 内置电池+充电+升压 |
| 开关 | SS-12D00 滑动开关 | ~0.50 | 串联在电源通路上 |
| 载板 PCB | 定制 PCB (嘉立创打样) | ~5.00 | 5片起打, 排母座插接各模块 |
| 排母座 | 2.54mm 排母 | ~2.00 | 焊在载板上, 模块插入 |
| 电池接口 | JST-PH 2.0 座子 | ~0.50 | PM11 电池可插拔 |
| 底座 | 3D 打印 (PLA) | ~3.00 | 固定载板 PCB + 电池 |
| **合计** | | **~¥91.22** | |

## 文档索引

| 文档 | 内容 |
|------|------|
| [hardware/HARDWARE.md](hardware/HARDWARE.md) | 硬件选型、BOM、接线图、供电设计、PCB载板设计、3D底座 |
| [firmware/FIRMWARE.md](firmware/FIRMWARE.md) | 固件架构、检测算法、状态机、BLE/WiFi通信、功耗管理 |
| [hardware/module_pages/MODULES.md](hardware/module_pages/MODULES.md) | 核心模块商品页存档及关键参数 |

## 项目结构

```
02-APP-Sedentary-Detector-ESP32C3/
├── README.md                    # 项目总览 (本文件)
├── hardware/
│   ├── HARDWARE.md              # 硬件设计文档 (选型、BOM、接线、供电、PCB、3D底座)
│   └── module_pages/            # 核心模块商品页存档
│       ├── MODULES.md           # 模块参数汇总
│       ├── esp32-c3-mini.html   # ESP32-C3 商品页
│       ├── mpu6050-gy521.html   # MPU6050 商品页
│       └── pm11-battery.html    # PM11 电池商品页
├── simulation/                  # Wokwi 仿真
│   ├── diagram.json             # 电路连接
│   ├── wokwi.toml               # Wokwi 配置
│   └── src/
│       └── main.cpp             # 仿真固件
├── firmware/                    # ESP32-C3 固件 (待开发)
│   ├── src/
│   │   ├── main.cpp             # 主逻辑
│   │   ├── mpu6050.h / .cpp     # MPU6050 驱动
│   │   ├── detector.h / .cpp    # 久坐检测算法
│   │   ├── ble_adv.h / .cpp     # BLE 广播
│   │   ├── power.h / .cpp       # 电源管理
│   │   └── config.h             # 参数配置
│   └── platformio.ini           # PlatformIO 工程
├── mechanical/                  # 3D 打印底座
│   └── base.stl                 # 底座模型 (待设计)
└── docs/
    └── calibration.md           # 校准指南 (待编写)
```

## 开发计划

### Phase 1: 仿真验证 (当前)

- [x] Wokwi 仿真 (ESP32 + MPU6050 + LED)
- [x] 角度检测算法验证
- [x] 久坐计时逻辑
- [ ] 在 Wokwi 中调整参数，确认检测准确率
- [ ] 购买 ESP32-C3 Mini + GY-521 + PM11 模块
- [ ] 面包板搭建原型，验证接线
- [ ] 实测椅子坐下/站起时的角度变化数据
- [ ] 确定安装位置和固定方式

### Phase 2: 载板 PCB + 固件开发

- [ ] 立创 EDA 绘制载板 PCB
- [ ] 嘉立创打样、焊接排母座和开关
- [ ] 固件移植 (Wokwi → 真实硬件)
- [ ] MPU6050 DMP 姿态解算
- [ ] Deep Sleep + RTC 定时唤醒
- [ ] MPU6050 Motion Interrupt 唤醒
- [ ] BLE 广播实现
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
