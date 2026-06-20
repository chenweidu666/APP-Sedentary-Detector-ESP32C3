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

---

### 问题 4: PCB 布尔值格式错误 "应为 'true|false'"

**现象：**
- KiCad 打开 PCB 报错：`应为 'true|false' in '...SedentaryDetector.kicad_pcb', line 45, offset 28`
- 错误位置在 `(pcbplotparams ...)` 区域

**原因：**
- KiCad 7 的 PCB 文件格式要求布尔值使用 `true`/`false`
- 手写文件时使用了 `yes`/`no` (KiCad 6 或旧格式)

**错误格式：**
```kicad_pcb
(pcbplotparams
  (usegerberextensions no)
  (usegerberattributes yes)
  (mirror no)
)
```

**正确格式：**
```kicad_pcb
(pcbplotparams
  (usegerberextensions false)
  (usegerberattributes true)
  (mirror false)
)
```

**修复：**
```bash
sed -i 's/(usegerberextensions no)/(usegerberextensions false)/g' file.kicad_pcb
sed -i 's/(usegerberattributes yes)/(usegerberattributes true)/g' file.kicad_pcb
sed -i 's/(mirror no)/(mirror false)/g' file.kicad_pcb
```

---

### 问题 5: PCB 元件标识符 uuid vs tstamp

**现象：**
- KiCad 报错：`应为 'locked, placed, tedit, tstamp, at, ...' in '...kicad_pcb', line 82, offset 6`

**原因：**
- KiCad 7 的 footprint 使用 `(tstamp UUID)` 而不是 `(uuid UUID)`
- 手写 PCB 文件时误用了 `uuid` 关键字

**错误格式：**
```kicad_pcb
(footprint "..." (layer "F.Cu")
  (uuid "a1b2c3d4-...")
  (at 20 25 0)
)
```

**正确格式：**
```kicad_pcb
(footprint "..." (layer "F.Cu")
  (tstamp 03d6bcdb-bcf8-4789-97c2-7161b855755d)
  (at 20 25 0)
)
```

---

### 问题 6: PCB pad 定义缺少 tstamp

**现象：**
- KiCad 报错：`应为 'a symbol or number' in '...kicad_pcb', line 87, offset 94`

**原因：**
- KiCad 7 的 pad 定义需要 `(tstamp UUID)` 字段
- 手写时只写了 `(net N)` 而缺少 tstamp

**错误格式：**
```kicad_pcb
(pad "1" thru_hole rect (at 0 0) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (net 1))
```

**正确格式：**
```kicad_pcb
(pad "1" thru_hole rect (at 0 0) (size 1.7 1.7) (drill 1) (layers "*.Cu" "*.Mask") (tstamp UUID) (net 1))
```

---

## 经验总结

### 手写 KiCad 文件的最佳实践

1. **不要手写 `.kicad_pcb`** — KiCad 7+ 文件格式复杂，字段顺序和关键字严格
2. **从 demo 复制模板** — 使用 `/usr/share/kicad/demos/` 中的文件作为起点
3. **用 KiCad GUI 保存** — 让 KiCad 自动生成正确格式的文件
4. **布尔值用 true/false** — KiCad 7 不再接受 yes/no
5. **uuid → tstamp** — KiCad 7 的元件/焊盘标识符关键字是 `tstamp`
6. **pad 必须有 tstamp** — 每个 pad 都需要唯一的 tstamp UUID

### 推荐工作流

```bash
# 1. 从 demo 复制模板
cp /usr/share/kicad/demos/microwave/microwave.kicad_pcb myboard.kicad_pcb

# 2. 用 KiCad GUI 打开并编辑
kicad myboard.kicad_pro

# 3. 保存后检查格式
kicad-cli pcb export svg myboard.kicad_pcb -o output.svg --layers F.Cu
```

---

---

### 问题 7: KiCad 9 Python API 环境配置

**现象：**
- `import pcbnew` 报 `libwx_gtk3u_gl-3.3.so.2: cannot open shared object file`
- 直接调用 AppImage 的 Python 会 stack smashing

**原因：**
- KiCad 9 AppImage 使用 `sharun` 运行时（`AppRun`）设置隔离环境
- 直接调用 Python 时 glibc 版本冲突（AppDir 内置 2.38 vs Ubuntu 24.04 系统 2.39）
- 必须通过 `AppRun` 启动才能正确加载 AppDir 内的库

**解决方案：**
```bash
# 正确启动方式
APPDIR=/path/to/AppDir
SHARUN_DIR=$APPDIR $APPDIR/AppRun python3.11 script.py
```

**KiCad 9 API 变更 (相对于 KiCad 7/8)：**
- `SetPadType` → `SetAttribute` (在 KiCad 9 中已移除)
- `PAD_TYPE_TH` → `PAD_ATTRIB_PTH` (常量名变化)
- `ZONE_CONNECTION_FULL` → `ZONE_CONNECTION_FULL` (未变)
- Kicad 9 CLI 输出格式已改变

---

## 最终方案

**推荐 KiCad 9 Python 工作流：**
```bash
APPDIR=/path/to/AppDir
SHARUN_DIR=$APPDIR $APPDIR/AppRun python3.11 gen_pcb.py
SHARUN_DIR=$APPDIR $APPDIR/AppRun kicad-cli pcb export svg board.kicad_pcb -o out.svg --layers F.Cu
```

## 待办

- [ ] 添加 DRC 检查通过截图
- [ ] 添加 3D 预览截图
- [ ] 完善 PCB 走线 (I2C / INT / Power)
