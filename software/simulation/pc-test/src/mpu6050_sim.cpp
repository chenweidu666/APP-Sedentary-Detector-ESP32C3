#include "mpu6050_sim.h"

void MPU6050Simulator::set_chair_occupied(bool occupied) {
  occupied_ = occupied;
  // 无人: 0°, 有人: 2° (模拟坐下后椅子倾斜)
  angle_deg_ = occupied ? 2.0f : 0.0f;
}

void MPU6050Simulator::set_angle(float angle_deg) {
  angle_deg_ = angle_deg;
  occupied_ = (angle_deg > 1.0f);
}

void MPU6050Simulator::get_acceleration(int16_t& ax, int16_t& ay, int16_t& az) {
  float angle_rad = angle_deg_ * 3.14159265f / 180.0f;
  // 简化模型: 倾斜导致 X 轴分量变化, Z 轴分量减小
  ax = static_cast<int16_t>(16384.0f * std::sin(angle_rad));
  ay = 0;
  az = static_cast<int16_t>(16384.0f * std::cos(angle_rad));
}
