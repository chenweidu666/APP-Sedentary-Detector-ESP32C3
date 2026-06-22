# 固件联调指南

**平台**：ESP32-WROOM-32 开发板（芯片 ESP32-D0WDQ6，`board=esp32dev`）。载板成品 I2C 为 GPIO4/5。

单片机已接 USB（`/dev/ttyUSB0`），**传感器未接**时可先跑本工程验证串口、I2C、状态机。

## 1. 安装 PlatformIO

```bash
pip install platformio
# 或: curl -fsSL https://raw.githubusercontent.com/platformio/platformio/master/scripts/get-platformio.py -o get-platformio.py && python3 get-platformio.py
```

## 2. 编译与烧录

```bash
cd Projects/02-APP-Sedentary-Detector-ESP32/firmware
pio run -t upload
pio device monitor
```

默认 `MOCK_MPU6050=1`：无 MPU6050 时用**模拟角度**驱动检测算法，约每 20s 切换有人/无人，GPIO2 LED 会跟着亮灭。

## 3. 串口应看到

```
=== Sedentary Detector bring-up ===
[I2C] scan SDA=GPIO4 SCL=GPIO5
  (no devices — MPU6050 未接...)
[MODE] MOCK_MPU6050=1
[CAL] baseline=...
[0s] angle=... state=VAC mock=1
```

交互命令（串口监视器里输入单个字符）：

| 键 | 作用 |
|----|------|
| `r` | 重新 I2C 扫描 |
| `c` | 重新校准基准角 |
| `m` | 切换 mock（仅 MPU 未连接时） |

## 4. 接上 MPU6050 之后

1. 按 `hardware/HARDWARE.md` 接线：SDA→GPIO4，SCL→GPIO5，VCC→3V3，GND→GND  
2. 修改 `platformio.ini`：`build_flags` 里把 `-DMOCK_MPU6050=1` 改为 `0`  
3. `pio run -t upload` 重新烧录  
4. I2C 扫描应出现 `0x68`

## 5. 仅开发板、未插载板时

若直接用 DevKit 杜邦线接 MPU6050，可临时改 `src/config.h`：

```cpp
constexpr int PIN_I2C_SDA = 21;
constexpr int PIN_I2C_SCL = 22;
```

载板成品请保持 GPIO4 / GPIO5。

## 6. 其他调试手段

| 工具 | 用途 |
|------|------|
| `simulation/` Wokwi | 有虚拟 MPU6050 时验证算法 |
| `simulation/pc-test/` | PC 上跑 `detector` 单元逻辑 |
| nRF Connect（手机） | 后续 BLE 广播调试 |

详细架构见 [FIRMWARE.md](FIRMWARE.md)。
