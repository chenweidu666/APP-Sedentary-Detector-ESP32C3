# 固件设计文档

> **平台**：ESP32-WROOM-32（`platformio.ini` 中 `board = esp32dev`）。载板 I2C 为 GPIO4/5，板载 LED 为 GPIO2。

## 固件架构

```
┌─────────────────────────────────────────────────┐
│                   main.cpp                       │
│              初始化 + 主循环 + Deep Sleep         │
├──────────┬──────────┬───────────┬───────────────┤
│ mpu6050  │ detector │ ble_adv   │    power      │
│ .h/.cpp  │ .h/.cpp  │ .h/.cpp   │   .h/.cpp     │
├──────────┼──────────┼───────────┼───────────────┤
│ MPU6050  │ 久坐检测  │ BLE 广播  │ Deep Sleep    │
│ I2C 驱动  │ 状态机    │ 管理      │ 电源管理      │
│ DMP 姿态  │ 角度判定  │ 状态上报  │ 电池电量      │
│ 加速度读取 │ 滞回去抖  │ 心跳包    │ ADC 检测      │
└──────────┴──────────┴───────────┴───────────────┘
                    │
              config.h
           参数配置 (阈值/时间)
```

## 检测算法

### 状态机

```
            坐下 (角度变化 > 阈值, 持续 3s 确认)
  ┌────────┐ ─────────────────────→ ┌─────────┐
  │  无人   │                        │  有人    │
  │(VACANT)│ ←───────────────────── │(OCCUPIED)│
  └────────┘  站起 (角度恢复, 持续 5s) └────┬────┘
                                        │
                                  连续坐 ≥ 45min
                                        ↓
                                  久坐提醒 (BLE 通知)
                                        │
                                  每隔 15min 再次提醒
```

### 判定算法

```
1. 基准校准 (上电时):
   - 记录无人状态下的基准倾斜角 baseline_angle

2. 每次唤醒:
   - 读取 MPU6050 加速度数据
   - 计算当前倾斜角 current_angle
   - delta = |current_angle - baseline_angle|
   - 计算振动幅度 vibration (加速度标准差)

3. 判定:
   - delta > 1.0° AND vibration > threshold → 有人
   - delta < 0.5° AND vibration < quiet_threshold → 无人
   - 中间值 → 维持当前状态 (滞回)

4. 去抖:
   - 状态切换需连续 N 次 (3-5次) 确认
```

### 参数配置

| 参数 | 默认值 | 说明 |
|------|--------|------|
| 采样间隔 | 2s | Deep Sleep RTC 唤醒周期 |
| 角度阈值 (坐下) | 1.0° | 倾斜角变化超过此值判定有人 |
| 角度阈值 (站起) | 0.5° | 回到此范围内判定无人 (滞回) |
| 去抖次数 | 3 次 | 连续确认次数 |
| 久坐阈值 | 45 min | 连续有人超过此时间触发提醒 |
| 重复提醒间隔 | 15 min | 久坐后每隔此时间再次提醒 |
| 心跳间隔 | 5 min | 定时上报状态 |

---

## 通信方式

### BLE 广播 (默认)

无需配对，通过 BLE Manufacturer Specific Data 广播状态：

```
Manufacturer Specific Data (AD Type 0xFF):

Byte 0-1: Company ID = 0xFFFF (测试用)
Byte 2:   Message Type
            0x01 = 状态变化
            0x02 = 心跳
            0x03 = 久坐提醒
            0x04 = 低电量
Byte 3:   Occupancy State (0x00=无人, 0x01=有人)
Byte 4-5: 久坐时长 (uint16, 分钟)
Byte 6:   电池电量 (0-100%)
Byte 7:   当前倾斜角 (int8, 度×10)
```

### WiFi/MQTT (可选)

通过 WiFi 连接 MQTT Broker，上报到 Home Assistant：

```
Topic: home/chair/desk/status      → "occupied" / "vacant"
Topic: home/chair/desk/duration    → 久坐时长 (分钟)
Topic: home/chair/desk/battery     → 电量 (%)
Topic: home/chair/desk/angle       → 当前倾斜角 (度)
```

> WiFi 模式功耗较高 (~100mA 连接时)，建议仅在状态变化时短暂开启 WiFi 上报后关闭。

---

## 电源管理

### Deep Sleep 策略

```
┌──────────────────────────────────────────────┐
│              Deep Sleep 循环                   │
│                                              │
│  RTC 唤醒 (每 2s)                             │
│     │                                        │
│     ↓                                        │
│  读取 MPU6050 (15ms)                          │
│     │                                        │
│     ↓                                        │
│  检测算法判定                                  │
│     │                                        │
│     ├── 状态变化 → BLE 广播 → Deep Sleep      │
│     ├── 久坐提醒 → BLE 广播 → Deep Sleep      │
│     └── 无变化 → 直接 Deep Sleep              │
│                                              │
│  唤醒源:                                       │
│  1. RTC 定时器 (2s)                           │
│  2. MPU6050 INT (运动中断)                     │
└──────────────────────────────────────────────┘
```

### 唤醒源配置

| 唤醒源 | 配置 | 说明 |
|--------|------|------|
| RTC 定时器 | 2000ms | 定期采样 MPU6050 |
| MPU6050 INT | GPIO2, 下降沿 | 运动检测中断，加速响应 |

### 电池电量检测

```
ESP32-WROOM-32 ADC → PM11 电池电压分压

- PM11 输出 5V (升压后), 无法直接测电池电压
- 方案: 在 PM11 电池正负极间加分压电阻
- 选用 ADC1 通道引脚（如 GPIO36/39 等仅输入 ADC 脚），读取分压值换算电量
- 低电量阈值: 3.3V (约 10%)
```

### 功耗优化

| 措施 | 效果 |
|------|------|
| Deep Sleep 2s 周期 | 平均功耗 ~0.15mA |
| MPU6050 读取后进入 standby | 减少传感器功耗 |
| BLE 仅在状态变化时广播 | 减少射频功耗 |
| WiFi 按需开启 | 避免持续连接功耗 |
| 关闭未使用外设 | 减少静态漏电 |

---

## 固件模块设计

### mpu6050.h / .cpp - MPU6050 驱动

```cpp
class MPU6050Driver {
public:
    void init();                    // I2C 初始化
    void calibrate();               // 上电校准基准角度
    float readAngle();              // 读取当前倾斜角
    float readVibration();          // 读取振动幅度 (加速度标准差)
    void setMotionInterrupt();      // 配置运动检测中断
    void sleep();                   // MPU6050 进入低功耗
    void wake();                    // MPU6050 唤醒
};
```

### detector.h / .cpp - 久坐检测算法

```cpp
class SedentaryDetector {
public:
    enum State { VACANT, OCCUPIED };

    void init();                    // 初始化, 记录基准角度
    State update(float angle, float vibration);  // 状态更新
    State getState();               // 获取当前状态
    uint16_t getDuration();         // 获取连续久坐时长 (分钟)
    void reset();                   // 重置计时器
};
```

### ble_adv.h / .cpp - BLE 广播管理

```cpp
class BLEAdvertiser {
public:
    void init();                    // BLE 初始化
    void broadcastState(State state, uint16_t duration,
                        uint8_t battery, int8_t angle);  // 广播状态
    void broadcastHeartbeat();      // 心跳包
    void broadcastAlert();          // 久坐提醒
    void broadcastLowBattery();     // 低电量告警
};
```

### power.h / .cpp - 电源管理

```cpp
class PowerManager {
public:
    void init();                    // 电源初始化
    void enterDeepSleep(uint64_t us);  // 进入 Deep Sleep
    uint8_t readBatteryLevel();     // 读取电池电量 (%)
    bool isLowBattery();            // 低电量判断
};
```

### config.h - 参数配置

```cpp
// 采样参数
#define SAMPLE_INTERVAL_US      2000000ULL    // 2s (us)
#define ANGLE_THRESHOLD_SEAT    1.0f          // 坐下角度阈值 (°)
#define ANGLE_THRESHOLD_STAND   0.5f          // 站起角度阈值 (°)
#define DEBOUNCE_COUNT          3             // 去抖次数

// 久坐参数
#define SEATED_THRESHOLD_MIN    45            // 久坐阈值 (分钟)
#define REMINDER_INTERVAL_MIN   15            // 重复提醒间隔 (分钟)
#define HEARTBEAT_INTERVAL_MIN  5             // 心跳间隔 (分钟)

// 电池参数
#define LOW_BATTERY_THRESHOLD   10            // 低电量阈值 (%)
#define BATTERY_ADC_PIN         GPIO_NUM_36   // ADC1_CH0（仅输入，需外部分压）
```

---

## main.cpp 主流程

```cpp
void setup() {
    // 1. 初始化各模块
    power.init();
    mpu6050.init();
    detector.init();
    ble.init();

    // 2. 校准基准角度 (上电时)
    mpu6050.calibrate();

    // 3. 配置 Deep Sleep 唤醒源
    esp_sleep_enable_timer_wakeup(SAMPLE_INTERVAL_US);
    esp_sleep_enable_ext0_wakeup(MPU6050_INT_PIN, LOW);
}

void loop() {
    // 1. 读取传感器
    float angle = mpu6050.readAngle();
    float vibration = mpu6050.readVibration();

    // 2. 更新检测状态
    SedentaryDetector::State newState = detector.update(angle, vibration);

    // 3. 状态变化时广播
    if (newState != lastState) {
        ble.broadcastState(newState, detector.getDuration(),
                          power.readBatteryLevel(), (int8_t)(angle * 10));
        lastState = newState;
    }

    // 4. 久坐提醒
    if (newState == SedentaryDetector::OCCUPIED &&
        detector.getDuration() >= SEATED_THRESHOLD_MIN) {
        ble.broadcastAlert();
    }

    // 5. 心跳包
    if (millis() - lastHeartbeat > HEARTBEAT_INTERVAL_MIN * 60000) {
        ble.broadcastHeartbeat();
        lastHeartbeat = millis();
    }

    // 6. 进入 Deep Sleep
    mpu6050.sleep();
    esp_deep_sleep_start();
}
```

---

## PlatformIO 工程配置

当前工程（见 `platformio.ini`）：

```ini
[env:esp32dev]
platform = espressif32
board = esp32dev
framework = arduino
monitor_speed = 115200
build_flags =
    -DCORE_DEBUG_LEVEL=3
    -DMOCK_MPU6050=1    ; 无传感器联调时保持 1；接上 MPU6050 后改为 0
lib_deps =
    electroniccats/MPU6050@^1.4.3
```

烧录与串口联调步骤见 [README.md](README.md)。

## 开发工具链

| 工具 | 用途 |
|------|------|
| PlatformIO (VSCode) | 固件开发 IDE |
| Wokwi | 在线仿真验证 |
| ESP-IDF | 底层 SDK (可选) |
| nRF Connect | BLE 广播测试 |
| MQTT Explorer | WiFi/MQTT 调试 |
