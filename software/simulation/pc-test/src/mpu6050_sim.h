#pragma once

#include <cmath>
#include <cstdint>

// MPU6050 模拟器: 生成模拟的加速度数据
// 用于 PC 端单元测试, 无需真实硬件
class MPU6050Simulator {
public:
  // 设置椅子状态: true=有人坐, false=无人
  void set_chair_occupied(bool occupied);

  // 设置倾斜角度 (度), 覆盖自动计算
  void set_angle(float angle_deg);

  // 读取加速度原始数据 (16-bit, ±2g range, 16384 LSB/g)
  void get_acceleration(int16_t& ax, int16_t& ay, int16_t& az);

  // 直接读取计算好的倾斜角度
  float get_angle() const { return angle_deg_; }

private:
  float angle_deg_ = 0;
  bool occupied_ = false;
};

// 计算倾斜角度: 从加速度分量
inline float calculate_tilt_angle(int16_t ax, int16_t ay, int16_t az) {
  float x = ax / 16384.0f;
  float y = ay / 16384.0f;
  float z = az / 16384.0f;
  return std::atan2(std::sqrt(x * x + y * y), z) * 180.0f / 3.14159265f;
}
