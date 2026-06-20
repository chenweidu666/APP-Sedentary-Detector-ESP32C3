# 载板接线表与网络表

[← 硬件文档索引](../HARDWARE.md) · [载板设计](design.md)

> ⚠️ **重要**: 载板按 **2×15 统一编号**（与 KiCad `PinSocket_2x15` 一致）。完整 30 Pin 定义见 [`pinout.md`](../pinout.md)。收到板后**务必用万用表核对丝印**。

## ESP32 排母 (2×15P)

| Pin | 信号 | 载板连接 |
|-----|------|----------|
| 1 | 3V3 | → GY-521 VCC |
| 9 | GPIO25 | → 扩展 Pin2 |
| 10 | GPIO26 | → 扩展 Pin3 |
| 12 | GPIO14 | → 扩展 Pin1 |
| 14 | GND | → GND 铺铜 |
| 15 | VIN | ← 滑动开关（PM11 5V） |
| 19 | GND | → GND 铺铜 |
| 22 | GPIO5 | → GY-521 SCL |
| 25 | GPIO4 | → GY-521 SDA |
| 26 | GPIO2 | → GY-521 INT |
| 28 | GND | → GND 铺铜 |
| 30 | NC | 不接（DevKitC 右列仅 14 脚） |
| 其余 | — | NC |

## GY-521 MPU6050 排母 (1×8P)

| Pin | 信号 | 载板连接 |
|-----|------|----------|
| 1 | VCC | ESP32 3V3 |
| 2 | GND | ESP32 GND |
| 3 | SCL | ESP32 GPIO5 (Pin 22) |
| 4 | SDA | ESP32 GPIO4 (Pin 25) |
| 5 | XDA | NC |
| 6 | XCL | NC |
| 7 | AD0 | NC (默认 GND, I2C 0x68) |
| 8 | INT | ESP32 GPIO2 (Pin 26) |

## PM11 电池 JST-PH 2P

| Pin | 连接 |
|-----|------|
| 1 (红) | 5V OUT → SS-12D00 → ESP32 VIN |
| 2 (黑) | GND |

## SS-12D00 滑动开关 (3P)

| Pin | 连接 |
|-----|------|
| 1 | PM11 5V OUT |
| 2 | 公共端 → ESP32 VIN (Pin 15) |
| 3 | 悬空 |

## 扩展排针 (1×4P)

| Pin | 连接 |
|-----|------|
| 1 | GPIO14 (ESP32 Pin 12) |
| 2 | GPIO25 (ESP32 Pin 9) |
| 3 | GPIO26 (ESP32 Pin 10) |
| 4 | GND |

---

## 网络表 (KiCad / 立创 EDA 原理图)

| 网络名 | 起点 | 终点 | 线宽建议 |
|--------|------|------|----------|
| 5V_PM11 | JST Pin1 | 开关 Pin1 | 20mil |
| VIN_SW | 开关 Pin2 | ESP32 Pin15 (VIN) | 20mil |
| GND | JST Pin2 → ESP32 Pin14/19/28 → GY521 GND | 大面积铺铜 | 铺铜 |
| 3V3 | ESP32 Pin1 (3V3) → GY521 VCC | 15mil |
| I2C_SDA | ESP32 Pin25 (GPIO4) → GY521 SDA | 10mil |
| I2C_SCL | ESP32 Pin22 (GPIO5) → GY521 SCL | 10mil |
| MPU_INT | ESP32 Pin26 (GPIO2) → GY521 INT | 10mil |
| EXT1 | ESP32 Pin12 (GPIO14) → 扩展 Pin1 | 10mil |
| EXT2 | ESP32 Pin9 (GPIO25) → 扩展 Pin2 | 10mil |
| EXT3 | ESP32 Pin10 (GPIO26) → 扩展 Pin3 | 10mil |
| EXT_GND | ESP32 GND → 扩展 Pin4 | 铺铜 |
