cmake_minimum_required(VERSION 3.10)
project(sedentary_detector_test CXX)

set(CMAKE_CXX_STANDARD 17)

# 测试可执行文件
add_executable(test_detector
  src/detector.cpp
  src/mpu6050_sim.cpp
  test/test_detector.cpp
)

target_include_directories(test_detector PRIVATE src)
