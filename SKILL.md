---
name: imi-trajs-diy
description: 将 CSV 轨迹坐标（RAS 格式）转换为 3D Slicer Python Console 可执行代码，导入为 Markups Line 节点。触发词：slicer导入轨迹、traj坐标生成Line、slicer line生成、RAS坐标导入slicer、csv转slicer代码、IMI trajectory slicer import。当用户提供轨迹CSV文件并希望导入到Slicer时使用此技能。
agent_created: true
---

# IMI_trajs_diy — CSV 轨迹坐标 → Slicer Line 代码生成

## 完整流水线

```
原始文本(R/P/S) → DeepSeek网页端 → CSV(RAS) → 本Skill → Slicer Python代码
```

### 上游步骤：获取 CSV

原始数据来自手术规划系统，格式为 `eN: Rxx Pxx Sxx` / `tN: Rxx Pxx Sxx`。

将此文本连同 `references/deepseek_prompt.md` 粘贴到 DeepSeek 网页端，获得 CSV 输出（参考 `references/csv_template.csv`）。

### 下游步骤：本 Skill

读取 DeepSeek 生成的 CSV，输出 Slicer Python Console 代码。

## CSV 预期格式

```
label,axis,value
e1,r1,33.90
e1,a1,-25.79
e1,s1,68.24
t1,r2,28.21
t1,a2,-30.63
t1,s2,21.14
e2,...
```

- `eN` = trajN 的 entry 点，`tN` = trajN 的 target 点
- `r`/`a`/`s` = RAS 坐标分量（Right/Anterior/Superior，mm）

## 工作流

### 1. 读取 CSV 并解析坐标

解析每行，将 eN 和 tN 按轨迹编号分组，收集各自的 RAS 坐标。

### 2. 生成 Slicer 代码

参考 `references/slicer_line_template.py` 生成代码。核心结构：

```python
trajs = [
    # name, entry_label, entry(R,A,S), target_label, target(R,A,S), color(RGB)
    ("traj1", "e1", [R, A, S], "t1", [R, A, S], [1.0, 0.0, 0.0]),
    ...
]
```

#### 颜色约定

- traj1 → 红 `[1.0, 0.0, 0.0]`
- traj2 → 绿 `[0.0, 1.0, 0.0]`
- traj3 → 蓝 `[0.0, 0.0, 1.0]`
- 后续轨迹按颜色表循环

#### 必须设置的属性

| 属性 | 方法 | 值 | 说明 |
|------|------|-----|------|
| 节点名称 | `SetName(name)` | "traj1" 等 | |
| 控制点标签 | `SetNthControlPointLabel(n, label)` | "e1"/"t1" 等 | 与 CSV 一致 |
| 颜色 | `disp.SetColor(rgb)` | [0-1] | |
| 选中色 | `disp.SetSelectedColor(rgb)` | [min(c+0.3, 1)] | |
| Glyph 类型 | `disp.SetGlyphType(...)` | `slicer.vtkMRMLMarkupsDisplayNode.Vertex2D` | |
| 文字比例 | `disp.SetTextScale(0.0)` | 0.0 | 不显示标签文字 |
| 控制点锁定 | `SetNthControlPointLocked(n, True)` | True | 防止误拖拽 |
| 节点锁定 | `SetLocked(True)` | True | 防止误修改 |

#### 禁止设置的属性

- **不要设置 Line Thickness** — Slicer Python API 中 `SetLineThickness`、`SetLineDiameterMm`、`SetAbsoluteLineThickness` 等方法在不同版本间不兼容，容易导致代码中断。此设置由用户在 GUI 中按需操作。

#### 代码健壮性

- 每条轨迹外层包裹 `try-except`，一条失败不影响其他
- 使用 `for` 遍历列表（非 `dict.items()`），减少版本兼容问题

### 3. 输出格式

同时生成两个文件（放在 CSV 同级目录）：

1. **`.md` 文件** — 方便用户直接复制粘贴代码块到 Slicer Python Console
2. **`.py` 文件** — 可直接执行或参考

## 已知限制

- `SetAbsoluteLineThickness` 在旧版 Slicer Python wrapping 中不存在（`has no attribute`）
- VTK On/Off 模式 (`AbsoluteLineThicknessOn`) 同样可能缺失
- 仅设置数据与显示属性，不处理 thickness
