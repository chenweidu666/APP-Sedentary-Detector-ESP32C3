#pragma once

// GY-87 联调 / 载板 J2：D4=SDA, D5=SCL, D2=INTA（见 hardware/HARDWARE.md）
constexpr int PIN_I2C_SDA = 4;   // D4
constexpr int PIN_I2C_SCL = 5;   // D5
constexpr int PIN_MPU_INT = 2;   // D2，与 DevKit 板载 LED 共用
constexpr int PIN_LED = 2;

constexpr uint8_t MPU_ADDR = 0x68;

constexpr uint8_t OLED_ADDR = 0x3C;
constexpr int OLED_WIDTH = 128;
constexpr int OLED_HEIGHT = 64;

constexpr unsigned long SAMPLE_INTERVAL_MS = 2000;
constexpr int DEBOUNCE_COUNT = 3;
constexpr int SEDENTARY_MINUTES = 45;
constexpr float ANGLE_OCCUPIED_DEG = 1.0f;
constexpr float ANGLE_VACANT_DEG = 0.5f;
