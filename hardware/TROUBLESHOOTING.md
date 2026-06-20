# KiCad 踩坑记录

## 2026-06-20 - Phase 1 排座 PCB

### 问题 1: PWR_FLAG 符号显示 "??"

**现象：**
- 原理图中 `#PWR_FLAG` 符号显示红色 "??" 框
- 符号无法正确加载

**原因：**
- KiCad 7 的 `#PWR_FLAG` 符号位于 `power` 库中
- 原理图书库未正确配置，导致符号无法解析

**解决方案：**
1. 在 KiCad 中打开原理图
2. 工具 → 编辑原理图符号和模型文件关联
3. 添加 `power` 库到项目库列表
4. 或者直接使用全局标签 (Global Label) 替代 PWR_FLAG

**替代方案（推荐）：**
```kicad_sch
; 不使用 PWR_FLAG 符号，直接用全局标签声明电源
(label "3V3" ...)  ; 电源网络用全局标签即可
```

---

### 问题 2: PCB 文件加载错误 "应为 ')' in ... line 1, offset 45"

**现象：**
- KiCad 打开 PCB 时报错
- 错误信息：`应为 ')' in '...SedentaryDetector.kicad_pcb', line 1, offset 45`

**原因：**
- KiCad 7 PCB 文件格式版本不匹配
- 使用了错误的 `version` 字段或 `host` 字段

**正确格式（KiCad 7.0）：**
```kicad_pcb
(kicad_pcb (version 20221018) (generator pcbnew)
  ...
)
```

**错误格式：**
```kicad_pcb
(kicad_pcb (version 20221018) (host pcbnew "(2022-10-18)")
  ; host 字段格式可能导致解析错误
)
```

**解决方案：**
1. 移除 `host` 字段，只保留 `version`
2. 确保 version 是 `20221018` (KiCad 7.0)
3. 在 KiCad 中重新保存 PCB 文件，让 KiCad 自动格式化

---

### 问题 3: git 提交时子仓库冲突

**现象：**
- `git add` 时提示 "正在添加嵌入式 git 仓库"
- Projects 下的子项目本身是 git 仓库

**原因：**
- 子项目目录有自己的 `.git` 文件夹
- git 将其识别为 submodule 而非普通目录

**解决方案：**
```bash
# 只添加特定文件，不添加整个目录
git add Projects/04-APP-Sedentary-Detector-ESP32C3/hardware/kicad/*.kicad_*

# 或者移除子项目的 .git（如果不需保留子项目历史）
rm -rf Projects/xxx/.git
```

---

## 待办

- [ ] 验证 PWR_FLAG 符号库配置
- [ ] 修复 PCB 文件格式
- [ ] 添加 DRC 检查通过截图
- [ ] 添加 3D 预览截图
