#include <Arduino.h>
#include <Wire.h>
#include <MPU6050.h>
#include <Adafruit_SSD1306.h>

#include "config.h"
#include "detector.h"

MPU6050 mpu;
SedentaryDetector detector;
Adafruit_SSD1306 oled(OLED_WIDTH, OLED_HEIGHT, &Wire, -1);

bool mpu_ok = false;
bool oled_ok = false;
bool use_mock = false;
float baseline_angle = 0.0f;

static float calculate_tilt_deg(int16_t ax, int16_t ay, int16_t az) {
  const float x = ax / 16384.0f;
  const float y = ay / 16384.0f;
  const float z = az / 16384.0f;
  return atan2f(sqrtf(x * x + y * y), z) * 180.0f / PI;
}

static void scan_i2c() {
  Serial.println("[I2C] scan SDA=GPIO4 SCL=GPIO5");
  int found = 0;
  for (uint8_t addr = 1; addr < 127; addr++) {
    Wire.beginTransmission(addr);
    if (Wire.endTransmission() == 0) {
      Serial.printf("  device 0x%02X\n", addr);
      found++;
    }
  }
  if (found == 0) {
    Serial.println("  (no devices — GY-87/MPU6050 未接或接线/供电异常)");
  } else {
    Serial.println("  (0x68=MPU6050; 0x77=BMP180 on GY-87, 可忽略)");
  }
}

static bool init_mpu() {
  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("[MPU6050] not found at 0x68");
    return false;
  }
  Serial.println("[MPU6050] connected");
  return true;
}

static bool init_oled() {
  if (!oled.begin(SSD1306_SWITCHCAPVCC, OLED_ADDR)) {
    Serial.println("[OLED] not found at 0x3C");
    return false;
  }
  oled.clearDisplay();
  oled.setTextColor(SSD1306_WHITE);
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.println("Sedentary Detector");
  oled.println("booting...");
  oled.display();
  Serial.println("[OLED] connected");
  return true;
}

static void draw_oled(float angle, SedentaryDetector::State state,
                      unsigned long seated_min) {
  if (!oled_ok) {
    return;
  }
  oled.clearDisplay();
  oled.setTextSize(1);
  oled.setCursor(0, 0);
  oled.printf("State: %s",
              state == SedentaryDetector::OCCUPIED ? "OCCUPIED" : "VACANT");
  oled.setCursor(0, 16);
  oled.printf("Angle: %.1f deg", angle);
  oled.setCursor(0, 32);
  oled.printf("Delta: %.2f deg", fabsf(angle - baseline_angle));
  oled.setCursor(0, 48);
  if (state == SedentaryDetector::OCCUPIED) {
    oled.printf("Seated: %lu min", seated_min);
  } else {
    oled.print("Seated: --");
  }
  oled.display();
}

static float read_angle() {
  if (use_mock) {
    // 模拟有人/无人：每 20s 切换一次倾斜，便于无传感器时验证状态机
    const bool simulated_occupied = ((millis() / 20000) % 2) == 1;
    return baseline_angle + (simulated_occupied ? 1.5f : 0.1f);
  }

  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);
  return calculate_tilt_deg(ax, ay, az);
}

static void calibrate_baseline() {
  float sum = 0.0f;
  const int samples = 5;
  for (int i = 0; i < samples; i++) {
    sum += read_angle();
    delay(200);
  }
  baseline_angle = sum / samples;
  detector.calibrate(baseline_angle);
  Serial.printf("[CAL] baseline=%.2f deg (mock=%d)\n", baseline_angle, use_mock);
}

void setup() {
  Serial.begin(115200);
  delay(500);
  Serial.println();
  Serial.println("=== Sedentary Detector bring-up ===");
  Serial.printf("Chip: %s @ %u MHz\n", ESP.getChipModel(), ESP.getCpuFreqMHz());
  Serial.printf("Free heap: %u bytes\n", ESP.getFreeHeap());

  pinMode(PIN_LED, OUTPUT);
  digitalWrite(PIN_LED, LOW);

  Wire.begin(PIN_I2C_SDA, PIN_I2C_SCL);
  scan_i2c();

  oled_ok = init_oled();

#if MOCK_MPU6050
  use_mock = true;
  Serial.println("[MODE] MOCK_MPU6050=1 — 使用模拟角度，无需传感器");
#else
  mpu_ok = init_mpu();
  use_mock = !mpu_ok;
  if (use_mock) {
    Serial.println("[MODE] MPU6050 不可用，回退到模拟角度");
  }
#endif

  SedentaryDetector::Config cfg;
  cfg.debounce_count = DEBOUNCE_COUNT;
  cfg.sedentary_minutes = SEDENTARY_MINUTES;
  cfg.sample_interval_ms = SAMPLE_INTERVAL_MS;
  cfg.angle_threshold_occupied = ANGLE_OCCUPIED_DEG;
  cfg.angle_threshold_vacant = ANGLE_VACANT_DEG;
  detector = SedentaryDetector(cfg);

  calibrate_baseline();
  Serial.println("[OK] 每 2s 打印一行；LED(GPIO2)=有人时常亮");
  Serial.println("命令: r=重扫I2C  c=重校准  m=切换mock(仅无MPU时)");
}

void loop() {
  if (Serial.available()) {
    char cmd = static_cast<char>(Serial.read());
    if (cmd == 'r') {
      scan_i2c();
    } else if (cmd == 'c') {
      calibrate_baseline();
    } else if (cmd == 'm' && !mpu_ok) {
      use_mock = !use_mock;
      Serial.printf("[MODE] mock=%d\n", use_mock);
      calibrate_baseline();
    }
  }

  const float angle = read_angle();
  const int transition = detector.update(angle);
  const auto state = detector.get_state();
  const unsigned long seated_min = detector.get_sedentary_minutes();

  digitalWrite(PIN_LED, state == SedentaryDetector::OCCUPIED ? HIGH : LOW);

  if (transition == 1) {
    Serial.println("[EVENT] -> OCCUPIED");
  } else if (transition == -1) {
    Serial.printf("[EVENT] -> VACANT (坐了 %lu 分钟)\n", seated_min);
  }

  if (detector.is_sedentary_alert()) {
    Serial.println("[ALERT] 久坐提醒 (模拟)");
  }

  Serial.printf("[%lus] angle=%.2f delta=%.2f state=%s",
                millis() / 1000,
                angle,
                fabsf(angle - baseline_angle),
                state == SedentaryDetector::OCCUPIED ? "OCC" : "VAC");
  if (state == SedentaryDetector::OCCUPIED) {
    Serial.printf(" seated=%lum", seated_min);
  }
  Serial.printf(" mock=%d\n", use_mock);

  draw_oled(angle, state, seated_min);

  delay(SAMPLE_INTERVAL_MS);
}
