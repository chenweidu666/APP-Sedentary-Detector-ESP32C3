# Sedentary Detector ESP32 - 久坐检测器

<p align="center">
  <img src="https://img.shields.io/badge/Version-0.2.0-blue" alt="Version">
  <img src="https://img.shields.io/badge/Status-硬件载板-yellow" alt="Status">
  <img src="https://img.shields.io/badge/Platform-ESP32--WROOM--32-green" alt="Platform">
  <img src="https://img.shields.io/badge/Power-3.7V_LiPo-orange" alt="Power">
  <img src="https://img.shields.io/badge/License-MIT-lightgrey" alt="License">
</p>

基于 **ESP32-WROOM-32** + **GY-87**（MPU6050）+ **OLED** 的椅子久坐检测器载板方案。本仓库**仅保留硬件**（BOM、接线、KiCad）；固件与联调在独立项目中完成。

**策略**：现成模块 + 定制载板 PCB 插接互连；PM11 锂电包供电（USB 充电，模块自带开关）。

**载板布线节奏**：KiCad 已完成原理图、布局与网络分配；**PCB 尚未布线**。固件与算法仍在 [03](../../03-ESP32-OLED-Button-Demo) / [04](../../04-MCU-GY87-Debug) 中联调，接口与引脚稳定后再走线、DRC、打样，避免返工。

## 当前进度

| 模块 | 状态 |
|------|------|
| 硬件方案 | ✅ MCU + GY-87 + OLED + PM11（无载板按键/开关） |
| 原理图 | ✅ v0.6（J1–J4 网络） |
| 载板 PCB | 🔧 v0.4 已布局 + 网络分配 + J2 对齐；**未布线**（等软件联调稳定后走线打样） |
| GY-87 / IMU 联调 | 🔧 [04-MCU-GY87-Debug](../../04-MCU-GY87-Debug) 调试中 |
| OLED 联调 | 🔧 [03-ESP32-OLED-Button-Demo](../../03-ESP32-OLED-Button-Demo) 调试中 |
| 3D 底座 | ⏳ 待设计 |

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
    │  │ GY-87   │═══════│ ESP32    │   │
    │  │ J2      │       │ DevKitC  │   │
    │  └─────────┘       │ J1       │   │
    │  ┌─────────┐       └──────────┘   │
    │  │ OLED    │═══════ (共享 I2C)     │
    │  │ J4      │                       │
    │  └─────────┘                       │
    └────────────────────────────────────┘
```

检测算法与固件开发见下方**关联软件项目**。

## 文档

| 文档 | 内容 |
|------|------|
| [hardware/HARDWARE.md](hardware/HARDWARE.md) | **硬件权威**：BOM、网络表、模块引脚、电源、PCB 版本 |
| [AGENTS.md](AGENTS.md) | AI / KiCad 自动化工作流 |

### KiCad 载板工程

```bash
kicad hardware/kicad/SedentaryDetector.kicad_pro
```

打样前核对 [hardware/HARDWARE.md §PCB 版本记录](hardware/HARDWARE.md#pcb-版本记录)。

### 关联软件项目（本仓库不含固件源码）

| 项目 | 内容 |
|------|------|
| [03-ESP32-OLED-Button-Demo](../../03-ESP32-OLED-Button-Demo) | SSD1306 OLED + I2C |
| [04-MCU-GY87-Debug](../../04-MCU-GY87-Debug) | GY-87 / MPU6050、久坐检测、BLE |

## 项目结构

```
02-APP-Sedentary-Detector-ESP32/
├── README.md          # 本文件（仓库唯一 README）
├── AGENTS.md
└── hardware/
    ├── HARDWARE.md
    ├── images/
    ├── kicad/
    └── scripts/
```

## 里程碑

| 阶段 | 目标 | 状态 |
|------|------|------|
| M1 模块联调 | 杜邦线验证 GY-87 + OLED（03/04） | 🔧 |
| M2 载板 | 软件稳定后 PCB 布线 → DRC → 打样焊接 | ⏳ |
| M3 整合 | 载板 + 03/04 固件合并产品化 | ⏳ |

## License

MIT
