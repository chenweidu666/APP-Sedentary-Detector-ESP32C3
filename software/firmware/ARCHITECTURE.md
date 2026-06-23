# 固件架构

> **平台**：ESP32-WROOM-32（`board = esp32dev`）。引脚与 I2C 见 `hardware/HARDWARE.md`；编译烧录见 [README.md](README.md)。
>
> **姿态**：台架竖放基准角约 ±90°（实测 ~97°）；产品水平安装约 0°。算法用 `delta = |angle - baseline|`，与绝对角无关。

## 已实现（当前 `main` 分支）

| 能力 | 文件 | 说明 |
|------|------|------|
| I2C 扫描 | `main.cpp` | 串口 `r`，SDA=GPIO4 / SCL=GPIO5 |
| MPU6050 | `main.cpp` | GY-87 @ `0x68`，倾斜角 `atan2` 计算 |
| SSD1306 OLED | `main.cpp` | @ `0x3C`，状态 / 角度 / delta / 久坐分钟 |
| 久坐状态机 | `detector.cpp` | VACANT ↔ OCCUPIED，去抖，久坐计时与提醒标志 |
| 基准校准 | `main.cpp` | 上电自动 + 串口 `c` |
| Mock 模式 | `main.cpp` | `MOCK_MPU6050` 或 MPU 缺失时模拟角度 |
| 板载 LED | `main.cpp` | GPIO2，有人时常亮（与 MPU INT 同脚） |

**串口命令**：`r` 重扫 I2C · `c` 重校准 · `m` 切换 mock（仅 MPU 不可用时）

### 状态机（`detector.cpp`）

```
VACANT ──(delta > 1.0°, 连续去抖)──→ OCCUPIED
OCCUPIED ──(delta < 0.5°, 连续去抖)──→ VACANT
OCCUPIED 且连续 ≥ 45min ──→ is_sedentary_alert()（当前仅串口打印）
```

### 参数（`config.h`）

| 参数 | 值 | 说明 |
|------|-----|------|
| `SAMPLE_INTERVAL_MS` | 2000 | 主循环采样间隔 |
| `ANGLE_OCCUPIED_DEG` | 1.0 | 判「有人」delta 阈值 |
| `ANGLE_VACANT_DEG` | 0.5 | 判「无人」delta 阈值（滞回） |
| `DEBOUNCE_COUNT` | 3 | 状态切换连续确认次数 |
| `SEDENTARY_MINUTES` | 45 | 久坐提醒阈值 |

主循环为 **polling + `delay`**，尚未使用 Deep Sleep。

### 源码结构

```
src/
├── main.cpp      # 初始化、I2C/OLED/MPU、主循环、串口
├── detector.h/cpp
└── config.h
```

---

## 规划中（勿当作已实现）

以下在旧设计文档中描述，**代码中尚未实现**：

| 模块 | 说明 |
|------|------|
| `ble_adv` | BLE Manufacturer Data 广播状态 / 心跳 / 久坐提醒 |
| `power` | Deep Sleep、RTC 周期唤醒、MPU INT 唤醒 |
| WiFi / MQTT | Home Assistant 上报（高功耗，按需） |
| 电池 ADC | PM11 电池电压分压采样 |
| 振动判据 | 加速度标准差辅助有人/无人 |
| MPU DMP | 硬件姿态解算 |
| 载板按键 | 已取消；交互靠串口或后续 BLE |

实现顺序建议：载板焊接联调稳定 → Deep Sleep → BLE 广播 → 电量检测。

---

## 与调试项目的关系

| 项目 | 用途 |
|------|------|
| [../../../04-MCU-GY87-Debug](../../../04-MCU-GY87-Debug) | GY-87 / I2C / BLE 专项验证 |
| [../../../03-ESP32-OLED-Button-Demo](../../../03-ESP32-OLED-Button-Demo) | OLED + I2C 参考 |

本产品固件在通过专项验证后合并能力，不以调试工程为长期依赖。

---

## PlatformIO

见 `platformio.ini`：`MOCK_MPU6050=0` 为接 GY-87 联调；无传感器时改为 `1`。
