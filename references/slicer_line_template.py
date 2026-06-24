# ===== Slicer Python Console: 导入轨迹为 Markups Line =====
# 源数据: {{csv_filename}} (RAS坐标, mm)
# 生成时间: {{timestamp}}
#
# 效果:
#   traj1 → 红色 Line
#   traj2 → 绿色 Line
#   traj3 → 蓝色 Line
#   Glyph: Vertex2D | Text Size: 0%
#
# 用法: 复制全部代码到 Slicer Python Console 执行

import slicer

# ---- 坐标数据 (R, A, S) ----
# entry点在前, target点在后

trajs = [
    # name,    entry_label, entry(R,A,S),           target_label, target(R,A,S),         color(RGB)
    ("traj1",  "e1", [33.90, -25.79, 68.24],  "t1", [28.21, -30.63, 21.14], [1.0, 0.0, 0.0]),   # 红
    ("traj2",  "e2", [34.13, -26.53, 67.91],  "t2", [28.05, -17.68, 19.33], [0.0, 1.0, 0.0]),   # 绿
    ("traj3",  "e3", [34.10, -26.84, 67.62],  "t3", [31.10, -18.00,  9.02], [0.0, 0.0, 1.0]),   # 蓝
]

for name, elabel, entry, tlabel, target, color in trajs:
    try:
        # 创建 Markups Line 节点
        line = slicer.mrmlScene.AddNewNodeByClass("vtkMRMLMarkupsLineNode")
        line.SetName(name)

        # 添加控制点 (entry → target)
        line.AddControlPoint(entry)
        line.AddControlPoint(target)

        # 控制点名称与CSV一致
        line.SetNthControlPointLabel(0, elabel)
        line.SetNthControlPointLabel(1, tlabel)

        # ---- 显示属性 ----
        disp = line.GetDisplayNode()

        # 颜色
        disp.SetColor(color)
        disp.SetSelectedColor([min(x + 0.3, 1.0) for x in color])

        # Glyph 类型: Vertex2D
        disp.SetGlyphType(slicer.vtkMRMLMarkupsDisplayNode.Vertex2D)

        # 文字大小: 0% (不显示标签)
        disp.SetTextScale(0.0)

        # 锁定控制点坐标，防止误拖拽
        line.SetNthControlPointLocked(0, True)   # entry
        line.SetNthControlPointLocked(1, True)   # target

        # 同时锁定整个节点 (可选, 如不需要可注释)
        line.SetLocked(True)

        print(f"✓ {name}: color={color}, Glyph=Vertex2D")

    except Exception as e:
        print(f"✗ {name} 失败: {e}")

print("\n完成!")
