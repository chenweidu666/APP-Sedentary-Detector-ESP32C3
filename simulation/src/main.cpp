#include <Wire.h>
#include <MPU6050.h>

#define I2C_SDA 21
#define I2C_SCL 22
#define LED_GREEN 17
#define LED_RED   16

#define MPU_ADDR 0x68
#define SAMPLE_INTERVAL_MS 2000
#define DEBOUNCE_COUNT 3
#define SEDENTARY_MINUTES 45

MPU6050 mpu;

// 状态
enum State { VACANT, OCCUPIED };
State currentState = VACANT;
int debounceCounter = 0;
unsigned long occupiedStartTime = 0;

// 校准
float baselineAngle = 0;
bool calibrated = false;

// 角度计算
float calculateTiltAngle(int16_t ax, int16_t ay, int16_t az) {
  float x = ax / 16384.0;
  float y = ay / 16384.0;
  float z = az / 16384.0;
  return atan2(sqrt(x * x + y * y), z) * 180.0 / PI;
}

void setup() {
  Serial.begin(115200);
  Wire.begin(I2C_SDA, I2C_SCL);

  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);

  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("[ERROR] MPU6050 connection failed!");
    while (1) { delay(500); }
  }
  Serial.println("[OK] MPU6050 connected");

  // 校准: 采集 5 次取平均作为无人基准
  float sum = 0;
  for (int i = 0; i < 5; i++) {
    int16_t ax, ay, az;
    mpu.getAcceleration(&ax, &ay, &az);
    sum += calculateTiltAngle(ax, ay, az);
    delay(200);
  }
  baselineAngle = sum / 5.0;
  calibrated = true;
  Serial.print("[CAL] Baseline angle: ");
  Serial.print(baselineAngle, 2);
  Serial.println(" deg");
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  float currentAngle = calculateTiltAngle(ax, ay, az);
  float delta = abs(currentAngle - baselineAngle);

  // 判定
  bool likelyOccupied = (delta > 1.0);
  bool likelyVacant = (delta < 0.5);

  if (likelyOccupied && currentState == VACANT) {
    debounceCounter++;
    if (debounceCounter >= DEBOUNCE_COUNT) {
      currentState = OCCUPIED;
      occupiedStartTime = millis();
      debounceCounter = 0;
      Serial.print("[EVENT] -> OCCUPIED (delta=");
      Serial.print(delta, 2);
      Serial.println(" deg)");
    }
  } else if (likelyVacant && currentState == OCCUPIED) {
    debounceCounter++;
    if (debounceCounter >= DEBOUNCE_COUNT) {
      currentState = VACANT;
      debounceCounter = 0;
      unsigned long durationMin = (occupiedStartTime > 0) ? (millis() - occupiedStartTime) / 60000 : 0;
      Serial.print("[EVENT] -> VACANT (坐了 ");
      Serial.print(durationMin);
      Serial.println(" 分钟)");
      occupiedStartTime = 0;
    }
  } else {
    debounceCounter = 0;
  }

  // LED 指示
  digitalWrite(LED_GREEN, currentState == OCCUPIED ? HIGH : LOW);

  unsigned long sedentaryMin = 0;
  if (currentState == OCCUPIED && occupiedStartTime > 0) {
    sedentaryMin = (millis() - occupiedStartTime) / 60000;
  }
  digitalWrite(LED_RED, (sedentaryMin >= SEDENTARY_MINUTES) ? HIGH : LOW);

  // 串口输出
  Serial.print("[");
  Serial.print(millis() / 1000);
  Serial.print("s] angle=");
  Serial.print(currentAngle, 2);
  Serial.print(" delta=");
  Serial.print(delta, 2);
  Serial.print(" state=");
  Serial.print(currentState == OCCUPIED ? "OCC" : "VAC");
  if (currentState == OCCUPIED) {
    Serial.print(" min=");
    Serial.print(sedentaryMin);
  }
  Serial.println();

  delay(SAMPLE_INTERVAL_MS);
}
