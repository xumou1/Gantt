import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

# 读取 CSV 文件
df = pd.read_csv('../skill_tree.csv', parse_dates=['Date'])

# 创建图形和坐标轴
fig, ax = plt.subplots(figsize=(12, 8))

# 获取唯一的类别和技能
categories = df['Category'].unique()
skills = df.groupby('Category')['Skill'].unique()

# 设置颜色
category_colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
skill_colors = plt.cm.Set2(np.linspace(0, 1, df['Skill'].nunique()))

# 计算每个类别的水平位置
category_positions = {cat: i for i, cat in enumerate(categories)}

# 绘制树状图
for cat_idx, (category, category_color) in enumerate(zip(categories, category_colors)):
    category_data = df[df['Category'] == category]
    x = category_positions[category]

    # 绘制主类别线
    ax.plot([x, x], [category_data['Date'].min(), category_data['Date'].max()],
            color=category_color, linewidth=2)

    # 添加类别标签
    ax.text(x, ax.get_ylim()[1], category,
            ha='center', va='bottom', fontsize=10, fontweight='bold', rotation=45)

    for skill_idx, skill in enumerate(skills[category]):
        skill_data = category_data[category_data['Skill'] == skill]
        skill_x = x + (skill_idx + 1) * 0.2  # 调整子分支间距

        # 绘制技能线
        ax.plot([skill_x, skill_x], [skill_data['Date'].min(), skill_data['Date'].max()],
                color=skill_colors[skill_idx], linewidth=1.5)

        # 绘制从主类别到技能的连接线
        ax.plot([x, skill_x], [skill_data['Date'].min(), skill_data['Date'].min()],
                color=category_color, linestyle=':', linewidth=1)

        # 添加技能标签
        ax.text(skill_x, skill_data['Date'].min(), skill,
                ha='right', va='center', fontsize=8, fontweight='bold')

        for _, subskill in skill_data.iterrows():
            # 绘制子技能点
            ax.scatter(skill_x, subskill['Date'], color=skill_colors[skill_idx], s=30)

            # 添加子技能标签
            ax.text(skill_x + 0.05, subskill['Date'], subskill['SubSkill'],
                    ha='left', va='center', fontsize=7)

# 设置坐标轴
ax.set_xlim(-0.5, len(categories) - 0.5)

# 设置y轴（日期）
ax.yaxis.set_major_locator(mdates.MonthLocator())
ax.yaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)

# 隐藏x轴刻度
ax.xaxis.set_visible(False)

# 设置标题和标签
ax.set_title('Hierarchical Skill Development Over Time', fontsize=14, fontweight='bold')
ax.set_ylabel('Date', fontsize=12)

# 添加网格
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# 反转y轴，使得较早的日期在顶部
ax.invert_yaxis()

# 调整布局
plt.tight_layout()

# 保存图片
plt.savefig('skill_tree_visualization.png', dpi=600, bbox_inches='tight')

# 显示图形
plt.show()