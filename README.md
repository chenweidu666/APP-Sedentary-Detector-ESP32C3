# Sedentary Detector ESP32 - 久坐检测器

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.2.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Status-联调中-yellow" alt="Status">
  <img src="https://img.shields.io/badge/Platform-ESP32--WROOM--32-green" alt="Platform">
  <img src="https://img.shields.io/badge/Power-3.7V_LiPo-orange" alt="Power">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

基于 **ESP32-WROOM-32** + **GY-87**（固件用 MPU6050）+ **OLED** 的椅子久坐检测器。检测坐垫倾斜变化判断有人/无人，超时提醒起身。供电为 **PM11** 锂电包（USB 充电，模块自带开关）。

**策略**：现成模块 + 定制载板 PCB 插接互连，模块可拆换迭代。

## 当前进度

| 模块 | 状态 |
|------|------|
| 硬件方案 | ✅ MCU + GY-87 + OLED + PM11（无载板按键/开关） |
| 原理图 | ✅ v0.6（J1–J4 网络） |
| 载板 PCB | 🔧 v0.4 待按 v0.6 改 J2 等走线后打样 |
| GY-87 杜邦联调 | ✅ I2C `0x68` / `0x77`，竖放基准角 ~97° |
| 固件 bring-up | 🔧 MPU6050 + OLED + 状态机 + 串口 |
| Wokwi / PC 仿真 | ✅ 算法单元测试 |
| 3D 底座 | ⏳ 待设计 |
| BLE / Deep Sleep | ⏳ 见 `software/firmware/ARCHITECTURE.md` 规划项 |

## 系统架构

```
         USB 充电
            │
    ┌───────┴────────────────────────────┐
    │  PM11 电源 (自带 ON/OFF)              │
    │       5V / GND                       │
    └───────┬────────────────────────────┘
            │ J3
    ┌───────┴────────────────────────────┐
    │  载板 PCB (100×80)                  │
    │  ┌─────────┐  I2C   ┌──────────┐   │
    │  │ GY-87   │═══════│ ESP32    │──→ 串口 / (规划 BLE)
    │  │ J2      │       │ DevKitC  │   │
    │  └─────────┘       │ J1       │   │
    │  ┌─────────┐       └──────────┘   │
    │  │ OLED    │═══════ (共享 I2C)     │
    │  │ J4      │                       │
    │  └─────────┘                       │
    └────────────────────────────────────┘
```

检测思路：MPU6050 测重力方向 → 计算相对基准角的 **delta** → 状态机判 VACANT / OCCUPIED → 久坐计时与提醒。详见 [software/firmware/ARCHITECTURE.md](software/firmware/ARCHITECTURE.md)。

## 文档地图

| 文档 | 内容 |
|------|------|
| [hardware/README.md](hardware/README.md) | 硬件入口、KiCad 工程 |
| [hardware/HARDWARE.md](hardware/HARDWARE.md) | **硬件权威**：BOM、网络表、模块引脚、电源 |
| [software/README.md](software/README.md) | 软件入口 |
| [software/firmware/README.md](software/firmware/README.md) | 编译、烧录、串口命令 |
| [software/firmware/ARCHITECTURE.md](software/firmware/ARCHITECTURE.md) | 算法、状态机（已实现 vs 规划） |
| [software/simulation/README.md](software/simulation/README.md) | Wokwi 与 PC 测试 |
| [AGENTS.md](AGENTS.md) | AI / KiCad 自动化工作流 |

## 项目结构

```
02-APP-Sedentary-Detector-ESP32/
├── README.md
├── AGENTS.md
├── hardware/          # 载板、BOM、KiCad
└── software/          # firmware、simulation
```

## 里程碑

| 阶段 | 目标 | 状态 |
|------|------|------|
| M1 联调 | 杜邦线 GY-87 + 串口日志 | ✅ |
| M2 固件 | OLED + 状态机 bring-up | 🔧 |
| M3 载板 | PCB v0.6 打样焊接 | ⏳ |
| M4 产品化 | 坐垫安装、阈值调优、BLE/低功耗 | ⏳ |

## License

MIT
