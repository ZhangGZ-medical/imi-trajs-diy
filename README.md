# imi-trajs-diy — 轨迹坐标 → Slicer Line 完整流水线

## 流水线概览

```
原始文本(R/P/S格式) ──→ DeepSeek 网页端 ──→ CSV(RAS格式) ──→ 本Skill ──→ Slicer Python代码
  (规划系统输出)        (prompt转换)        (中间产物)       (代码生成)      (导入Slicer)
```

## 前置步骤：在 DeepSeek 网页端生成 CSV

原始数据通常来自手术规划系统，格式为：

```
traj1: R6.89 A5.86 D47.69
e1: R33.90 P25.79 S68.24
t1: R28.21 P30.63 S21.14
...
```

将上述文本连同 `references/deepseek_prompt.md` 的提示词一起粘贴到 DeepSeek 网页端对话框，即可获得 `210_trajs.csv` 格式的输出。

## 本 Skill 的作用

读取 DeepSeek 生成的 CSV 文件，输出可在 3D Slicer Python Console 中直接运行的代码，将每条轨迹导入为 Markups Line 节点。

## 文件结构

```
imi-trajs-diy/
├── README.md                             ← 你正在看的文件
├── SKILL.md                              ← Skill 工作流定义
└── references/
    ├── csv_template.csv                  ← CSV 格式示例
    ├── deepseek_prompt.md                ← DeepSeek 网页端转换提示词
    └── slicer_line_template.py           ← Slicer 代码生成模板
```

## 使用方式

1. 将规划系统输出的 R/P/S 文本 + `references/deepseek_prompt.md` 给 DeepSeek
2. 保存 DeepSeek 返回的 CSV
3. 告诉 WorkBuddy："将 XXX.csv 的轨迹生成 Slicer 导入代码"
   （触发 `imi-trajs-diy` skill）
4. 将生成的代码复制到 Slicer Python Console 执行
