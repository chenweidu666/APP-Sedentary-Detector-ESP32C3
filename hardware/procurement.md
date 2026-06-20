# 采购与芯片选型

[← 硬件文档索引](HARDWARE.md)

## 采购链接

| 模块 | 链接 |
|------|------|
| ESP32-WROOM-32 开发板 | https://detail.tmall.com/item.htm?id=805161973303&skuId=5879086331469 |
| 陀螺仪模块 (MPU6050/GY-521) | https://detail.tmall.com/item.htm?id=729656168752&skuId=5367169145529 |
| PM11锂电池包 (3.7V+充电+升压5V/2.4A) | https://item.taobao.com/item.htm?id=1007451636387&skuId=6002389453662 |
| SS-12D00 滑动开关 | 待补充 |
| JST-PH 2.0 座子 | 待补充 |

## 为什么选 ESP32-WROOM-32？

| 对比 | ESP32-WROOM-32 | ESP32-C3 | nRF52840 |
|------|----------------|----------|----------|
| 内核 | Xtensa 双核 240MHz | RISC-V 单核 160MHz | Cortex-M4 64MHz |
| BLE | 5.0 | 5.0 | 5.0 |
| WiFi | 2.4GHz | 2.4GHz | 无 |
| Deep Sleep | ~7 μA | ~5 μA | ~2 μA |
| 价格 | ~¥15 (合宙) | ~¥15 | ~¥15 |
| 开发难度 | Arduino/ESP-IDF | Arduino/ESP-IDF | nRF SDK/Zephyr |

ESP32-WROOM-32 性价比高，有 WiFi+BLE 双模，开发生态成熟。

## 为什么选 MPU6050？

| 对比 | MPU6050 | ADXL345 | LIS3DH |
|------|---------|---------|--------|
| 轴数 | 6 轴 (加速度+陀螺仪) | 3 轴 (仅加速度) | 3 轴 (仅加速度) |
| 接口 | I2C / SPI | I2C / SPI | I2C / SPI |
| 运动中断 | 支持 | 支持 | 支持 |
| DMP | 内置数字运动处理器 | 无 | 无 |
| 价格 | ~¥25 (GY-521) | ~¥5 | ~¥6 |

MPU6050 有内置 DMP 可硬件计算姿态角，减轻 MCU 负担；6 轴数据可同时用角度和振动两种判据，准确率更高。
