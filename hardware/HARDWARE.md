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

## 模块引脚

### ESP32-WROOM-32 开发板 (ESP32-DevKitC 风格)

![ESP32-WROOM-32 引脚图](images/esp32-wroom-32-pinout.jpg)

```
尺寸: 51.85 × 23.5 mm
引脚: 左列 15pin + 右列 14pin, 2.54mm 间距, 排针间距 23.5mm
安装孔: 4× φ3mm, 距边 3mm
```

#### 左侧引脚 (从上到下, 15 pin)

| Pin | 引脚 | 功能说明 |
|-----|------|----------|
| 1 | 3V3 | 3.3V 电源输出 |
| 2 | EN | 使能/复位引脚 (高电平有效) |
| 3 | GPIO36 (VP) | ADC1_CH0, 仅输入 |
| 4 | GPIO39 (VN) | ADC1_CH3, 仅输入 |
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

#### 右侧引脚 (从上到下, 14 pin)

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
| 26 | GPIO2 | TOUCH2 / ADC2_CH2 / 板载LED |
| 27 | GPIO15 | U0 RTS / TOUCH3 / ADC2_CH3 |
| 28 | GND | 接地 |
| 29 | 3V3 | 3.3V 电源输出 |

> ⚠️ 注意事项:
> - GPIO34~39 仅输入，无输出、无内上下拉
> - GPIO6~11 被 SPI Flash 占用，不建议使用
> - GPIO12 上电影响 Flash 电压 (MTDI)，上电时保持低
> - GPIO0 下载模式 (板子底部 BOOT 按钮)
> - 板载 LED 在 GPIO2

### GY-521 模块 (MPU6050)

```
尺寸: 15.6 × 20.2 mm
重量: ~15g
引脚: 1 × 8pin 单排, 2.54mm 间距
```

| Pin | 引脚 | 功能 |
|-----|------|------|
| 1 | VCC | 3.3V 电源 |
| 2 | GND | 接地 |
| 3 | SCL | I2C 时钟 |
| 4 | SDA | I2C 数据 |
| 5 | XDA | I2C 辅助 (不用) |
| 6 | XCL | I2C 辅助 (不用) |
| 7 | AD0 | I2C 地址选择 (不接=0x68) |
| 8 | INT | 运动中断 → ESP32 GPIO2 |

---

## 接线表

| 网络 | ESP32 引脚 | MPU6050 引脚 |
|------|-----------|-------------|
| 3V3 | Pin 1 (3V3) | Pin 1 (VCC) |
| GND | Pin 14/19/28 | Pin 2 |
| I2C_SDA | Pin 25 (GPIO4) | Pin 4 (SDA) |
| I2C_SCL | Pin 22 (GPIO5) | Pin 3 (SCL) |
| MPU_INT | Pin 26 (GPIO2) | Pin 8 (INT) |

---

## 电源路径

```
PM11 5V OUT → JST-PH Pin1 → SS-12D00 开关 → ESP32 Pin15 (VIN)
PM11 GND → JST-PH Pin2 → ESP32 Pin14 (GND)
```

## 载板 BOM

| # | 元件 | 规格 | 封装 | 数量 |
|---|------|------|------|:----:|
| 1 | ESP32 排母 (左) | 1×15P 2.54mm | 直插 | 1 |
| 2 | ESP32 排母 (右) | 1×15P 2.54mm | 直插 | 1 |
| 3 | MPU6050 排母 | 1×8P 2.54mm | 直插 | 1 |
| 4 | PCB | 80×50mm 2层 1.6mm | - | 5 |

## PCB 规格

| 参数 | 值 |
|------|-----|
| 尺寸 | 80mm × 50mm, 2层 |
| 板厚 | 1.6mm |
| 铜厚 | 1oz |
| 安装孔 | 4× M3 (φ3.2mm), 距边 3mm |
| 线宽 (信号) | 0.254mm |
| 线宽 (电源) | 0.5mm |
| GND | B.Cu 铺铜 |
