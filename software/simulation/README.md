# 仿真与 PC 测试

## Wokwi

| 文件 | 说明 |
|------|------|
| `diagram.json` | 电路连接（ESP32 + MPU6050） |
| `wokwi.toml` | Wokwi 工程配置 |
| `src/main.cpp` | 早期仿真固件（可能与 `firmware/` 不同步） |

在 [Wokwi](https://wokwi.com) 导入本目录或打开 VS Code Wokwi 扩展。

## PC 单元测试（`pc-test/`）

与 `firmware/src/detector` 同算法的离线测试（无硬件）。

```bash
cd software/simulation/pc-test
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build
./build/test_detector
```

`pc-test/src/detector.*` 应与 `software/firmware/src/detector.*` 保持逻辑一致；修改算法后两边同步更新。

## 与量产固件的关系

| 路径 | 用途 |
|------|------|
| `simulation/` | 算法验证、Wokwi 演示 |
| `software/firmware/` | 板载量产固件（GY-87 + OLED） |

新算法优先在 `pc-test` 验证，再合入 `firmware/src/detector.cpp`。
