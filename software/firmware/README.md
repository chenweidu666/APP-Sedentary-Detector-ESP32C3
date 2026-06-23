# 固件联调指南

**平台**：ESP32-WROOM-32 + IO 扩展板（或载板 J1）  
**传感器**：GY-87（固件使用 MPU6050 @ `0x68`）  
**显示**：SSD1306 OLED @ `0x3C`（与 IMU 共享 I2C）

## 接线

杜邦线联调与载板 J2 引脚定义见 **[hardware/HARDWARE.md](../../hardware/HARDWARE.md)**：

- [杜邦线联调（扩展板）](../../hardware/HARDWARE.md#杜邦线联调esp32-扩展板)
- [J2 排母引脚映射](../../hardware/HARDWARE.md#j2-排母引脚映射载板--直插)
- [OLED 接法](../../hardware/HARDWARE.md#oled-显示屏)

## 安装姿态

**竖直立放**（台架）：基准角约 ±90°（实测 ~97°），看 **delta** 判人。  
**水平安装**（坐垫下）：基准约 0°，装好后串口发 `c` 重校准。

## 编译烧录

```bash
cd Projects/02-APP-Sedentary-Detector-ESP32/software/firmware
pio run -t upload
pio device monitor
```

`platformio.ini` 中 `MOCK_MPU6050=0`（已接 GY-87）；无传感器时改为 `1`。

## 串口示例

```
[I2C] scan SDA=GPIO4 SCL=GPIO5
  device 0x68
  device 0x77
[MPU6050] connected
[OLED] connected
[CAL] baseline=97.17 deg (mock=0)
```

`0x77` = GY-87 上 BMP180，固件忽略。

## 命令

| 键 | 作用 |
|----|------|
| `r` | I2C 重扫 |
| `c` | 重校准基准角 |
| `m` | 切换 mock（仅 MPU 不可用时） |

算法与状态机见 [ARCHITECTURE.md](ARCHITECTURE.md)。
