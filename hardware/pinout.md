# ESP32 2×15 引脚定义 (KiCad 载板权威)

[← 硬件文档索引](HARDWARE.md)

> **Agent / KiCad 脚本**以本文 Pin 1–30 编号为准。开发板丝印左/右列对照见 [`modules/esp32-devkitc.md`](modules/esp32-devkitc.md)。

## 左列引脚 (Pin 1–15, 从上到下)

| Pin | 引脚 | 功能说明 |
|-----|------|----------|
| 1 | 3V3 | 3.3V 电源输出 |
| 2 | EN | 使能/复位 (高电平有效) |
| 3 | GPIO36 | VP, ADC1_CH0, 仅输入 |
| 4 | GPIO39 | VN, ADC1_CH3, 仅输入 |
| 5 | GPIO34 | ADC1_CH6, 仅输入 |
| 6 | GPIO35 | ADC1_CH7, 仅输入 |
| 7 | GPIO32 | ADC1_CH4 / TOUCH9 |
| 8 | GPIO33 | ADC1_CH5 / TOUCH8 |
| 9 | GPIO25 | ADC2_CH8 / DAC_1 |
| 10 | GPIO26 | ADC2_CH9 / DAC_2 |
| 11 | GPIO27 | ADC2_CH7 / TOUCH7 |
| 12 | GPIO14 | ADC2_CH6 / TOUCH6 / MTMS |
| 13 | GPIO12 | ADC2_CH5 / TOUCH5 / MTDI |
| 14 | GND | 接地 |
| 15 | VIN | 外部电源输入 (5V) |

## 右列引脚 (Pin 16–30, 从上到下)

| Pin | 引脚 | 功能说明 |
|-----|------|----------|
| 16 | GPIO23 | VSPI MOSI |
| 17 | GPIO22 | I2C SCL |
| 18 | GPIO21 | I2C SDA |
| 19 | GND | 接地 |
| 20 | GPIO19 | VSPI MISO |
| 21 | GPIO18 | VSPI SCK |
| 22 | GPIO5 | VSPI SS / TOUCH5 |
| 23 | GPIO17 | UART2 TXD |
| 24 | GPIO16 | UART2 RXD |
| 25 | GPIO4 | TOUCH0 / ADC2_CH0 |
| 26 | GPIO2 | TOUCH2 / 板载 LED |
| 27 | GPIO15 | U0 RTS / TOUCH3 |
| 28 | GND | 接地 |
| 29 | 3V3 | 3.3V 电源输出 |
| 30 | NC | 未使用 |

## 本设计使用的引脚

| ESP32 引脚 | Pin# | 连接 |
|------------|------|------|
| GPIO4 (SDA) | 25 | → MPU6050 SDA |
| GPIO5 (SCL) | 22 | → MPU6050 SCL |
| GPIO2 (INT) | 26 | → MPU6050 INT |
| VIN | 15 | ← PM11 5V (经开关) |
| 3V3 | 1 | → MPU6050 VCC |
| GND | 14/19/28 | → 共地 |
| GPIO14 | 12 | → 扩展 Pin1（预留） |
| GPIO25 | 9 | → 扩展 Pin2（预留） |
| GPIO26 | 10 | → 扩展 Pin3（预留） |

## 固件引脚配置

```cpp
// Arduino: I2C 非默认引脚
Wire.begin(4, 5);  // SDA=GPIO4, SCL=GPIO5
// INT 接 GPIO2（与板载 LED 共用）
```

载板接线与网络名见 [`carrier/nets.md`](carrier/nets.md)。
