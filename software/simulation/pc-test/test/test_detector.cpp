#include <cstdio>
#include <cassert>
#include "detector.h"
#include "mpu6050_sim.h"

static int tests_run = 0;
static int tests_failed = 0;

#define TEST(name) void name()
#define RUN_TEST(name) do { \
  printf("  RUN %s\n", #name); \
  tests_run++; \
  name(); \
  printf("  PASS %s\n", #name); \
} while(0)

#define ASSERT_EQ(a, b) do { \
  if ((a) != (b)) { \
    printf("  FAIL: %s == %s (got %d vs %d)\n", #a, #b, (int)(a), (int)(b)); \
    tests_failed++; \
    return; \
  } \
} while(0)

#define ASSERT_FLOAT_EQ(a, b) do { \
  if (std::abs((a) - (b)) > 0.001f) { \
    printf("  FAIL: %s == %s (got %.4f vs %.4f)\n", #a, #b, (double)(a), (double)(b)); \
    tests_failed++; \
    return; \
  } \
} while(0)

// ========== 测试用例 ==========

TEST(test_baseline_angle_calculation) {
  // 水平放置: ax=0, ay=0, az=16384 (1g)
  int16_t ax = 0, ay = 0, az = 16384;
  float angle = calculate_tilt_angle(ax, ay, az);
  ASSERT_FLOAT_EQ(angle, 0.0f);

  // 倾斜 2°: 微小 X 分量
  ax = 572;  // 16384 * sin(2°) ≈ 572
  az = 16374; // 16384 * cos(2°) ≈ 16374
  angle = calculate_tilt_angle(ax, ay, az);
  ASSERT_FLOAT_EQ(angle, 2.0f);
}

TEST(test_detector_calibration) {
  SedentaryDetector detector;
  detector.calibrate(0.5f);  // 基准角度 0.5°
  ASSERT_EQ(detector.get_state(), SedentaryDetector::VACANT);
}

TEST(test_detector_vacant_no_change) {
  SedentaryDetector detector;
  detector.calibrate(0.0f);

  // 持续无人状态 (角度 = 0°)
  for (int i = 0; i < 10; i++) {
    int result = detector.update(0.0f);
    ASSERT_EQ(result, 0);  // 无变化
    ASSERT_EQ(detector.get_state(), SedentaryDetector::VACANT);
  }
}

TEST(test_detector_sit_down) {
  SedentaryDetector detector;
  detector.calibrate(0.0f);

  // 第一次: 角度 2° (有人), 去抖计数 1
  ASSERT_EQ(detector.update(2.0f), 0);

  // 第二次: 角度 2°, 去抖计数 2
  ASSERT_EQ(detector.update(2.0f), 0);

  // 第三次: 角度 2°, 去抖计数 3 → 变为有人
  ASSERT_EQ(detector.update(2.0f), 1);
  ASSERT_EQ(detector.get_state(), SedentaryDetector::OCCUPIED);
}

TEST(test_detector_stand_up) {
  SedentaryDetector detector;
  detector.calibrate(0.0f);

  // 先坐下 (3 次确认)
  detector.update(2.0f);
  detector.update(2.0f);
  detector.update(2.0f);
  ASSERT_EQ(detector.get_state(), SedentaryDetector::OCCUPIED);

  // 站起来: 角度恢复到 0°
  detector.update(0.0f);
  detector.update(0.0f);
  ASSERT_EQ(detector.get_state(), SedentaryDetector::OCCUPIED);  // 还没去抖完成

  detector.update(0.0f);  // 第 3 次
  ASSERT_EQ(detector.get_state(), SedentaryDetector::VACANT);
}

TEST(test_detector_sedentary_timer) {
  SedentaryDetector::Config config;
  config.sedentary_minutes = 5;  // 测试用 5 分钟
  SedentaryDetector detector(config);
  detector.calibrate(0.0f);

  // 坐下
  detector.update(2.0f);
  detector.update(2.0f);
  detector.update(2.0f);

  // 模拟时间流逝: 每次 update 前进 2 秒
  // 5 分钟 = 300 秒 = 150 次采样
  for (int i = 0; i < 149; i++) {
    detector.update(2.0f);
  }
  ASSERT_EQ(detector.is_sedentary_alert(), false);

  detector.update(2.0f);  // 第 150 次 = 5 分钟
  ASSERT_EQ(detector.is_sedentary_alert(), true);
}

TEST(test_detector_debounce_noise) {
  SedentaryDetector detector;
  detector.calibrate(0.0f);

  // 角度波动: 2° → 0° → 2° (噪声, 不应触发状态变化)
  detector.update(2.0f);
  detector.update(0.0f);  // 去抖重置
  detector.update(2.0f);
  detector.update(0.0f);  // 去抖重置
  detector.update(2.0f);

  ASSERT_EQ(detector.get_state(), SedentaryDetector::VACANT);  // 不应变化
}

TEST(test_full_simulation) {
  MPU6050Simulator mpu;
  SedentaryDetector detector;
  detector.calibrate(0.0f);

  // 场景: 无人 → 坐下 → 久坐 → 站起
  printf("  [仿真] 初始状态: 无人\n");

  mpu.set_chair_occupied(false);
  for (int i = 0; i < 5; i++) {
    int16_t ax, ay, az;
    mpu.get_acceleration(ax, ay, az);
    float angle = calculate_tilt_angle(ax, ay, az);
    int result = detector.update(angle);
    ASSERT_EQ(result, 0);
  }

  // 有人坐下
  printf("  [仿真] 有人坐下\n");
  mpu.set_chair_occupied(true);
  for (int i = 0; i < 3; i++) {
    int16_t ax, ay, az;
    mpu.get_acceleration(ax, ay, az);
    float angle = calculate_tilt_angle(ax, ay, az);
    int result = detector.update(angle);
    if (i == 2) ASSERT_EQ(result, 1);  // 第 3 次确认
  }
  ASSERT_EQ(detector.get_state(), SedentaryDetector::OCCUPIED);

  // 站起
  printf("  [仿真] 有人站起\n");
  mpu.set_chair_occupied(false);
  for (int i = 0; i < 3; i++) {
    int16_t ax, ay, az;
    mpu.get_acceleration(ax, ay, az);
    float angle = calculate_tilt_angle(ax, ay, az);
    int result = detector.update(angle);
    if (i == 2) ASSERT_EQ(result, -1);  // 第 3 次确认
  }
  ASSERT_EQ(detector.get_state(), SedentaryDetector::VACANT);

  printf("  [仿真] 完整场景通过\n");
}

// ========== 主函数 ==========

int main() {
  printf("=== 久坐检测器单元测试 ===\n\n");

  RUN_TEST(test_baseline_angle_calculation);
  RUN_TEST(test_detector_calibration);
  RUN_TEST(test_detector_vacant_no_change);
  RUN_TEST(test_detector_sit_down);
  RUN_TEST(test_detector_stand_up);
  RUN_TEST(test_detector_sedentary_timer);
  RUN_TEST(test_detector_debounce_noise);
  RUN_TEST(test_full_simulation);

  printf("\n=== 结果: %d 运行, %d 失败 ===\n", tests_run, tests_failed);
  return tests_failed > 0 ? 1 : 0;
}
