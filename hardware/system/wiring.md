# 系统接线图

[← 硬件文档索引](../HARDWARE.md)

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

载板 PCB 逐 Pin 接线见 [`carrier/nets.md`](../carrier/nets.md)。
