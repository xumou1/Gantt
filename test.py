import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
from config import *

# 读取CSV文件
df_main_tasks = pd.read_csv('main_tasks.csv', parse_dates=['start_date', 'end_date'])
df_subtasks_training_course = pd.read_csv('training_subtasks.csv', parse_dates=['start_date', 'end_date'])
df_learning_processes = pd.read_csv('learning_processes.csv', parse_dates=['Start Date', 'End Date'])
df_skills = pd.read_csv('skill_tree.csv', parse_dates=['Date'])

# 创建一个2x2的子图布局
fig, axs = plt.subplots(2, 2, figsize=(24, 18), gridspec_kw={'width_ratios': [2, 1]})

# 创建任务到数字的映射
unique_tasks = df_main_tasks['task'].unique()
task_to_num = {task: i for i, task in enumerate(unique_tasks)}

# ----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*
# 绘制整体甘特图 (左上角)
'''
    Gantt图完整版 Version1.0
    状态：暂定完成
    整体甘特图：
    - 主任务：用不同颜色表示不同类别
    - 子任务：用不同颜色表示不同状态
    - 文本：显示子任务名称
'''

for task in unique_tasks:
    task_data = df_main_tasks[df_main_tasks['task'] == task]
    task_category = task_data['category'].iloc[0]
    task_num = task_to_num[task]

    # 绘制主任务的边框
    main_task_start = task_data['start_date'].min()
    main_task_end = task_data['end_date'].max()
    axs[0, 0].barh(task_num, (main_task_end - main_task_start).days, left=main_task_start,
                   edgecolor=CATEGORY_COLORS[task_category], color='none', linewidth=10)

    # 绘制子任务
    for i, subtask in task_data.iterrows():
        bar = axs[0, 0].barh(task_num, (subtask['end_date'] - subtask['start_date']).days, left=subtask['start_date'],
                             color=STATUS_COLORS[subtask['status']], edgecolor='black', linewidth=2)

        # 计算文本位置和旋转
        text_x = subtask['start_date'] + pd.Timedelta((subtask['end_date'] - subtask['start_date']).total_seconds() / 2,
                                                      unit='s')
        text_y = task_num
        rotation = 0
        ha = 'center'
        va = 'center'

        # 如果条形太窄，将文本旋转90度
        if (subtask['end_date'] - subtask['start_date']).days < 30:
            rotation = 90
            ha = 'left'
            va = 'center'
            text_y += 0.2

        axs[0, 0].text(text_x, text_y, subtask['subtask'],
                       ha=ha, va=va, color='black', fontsize=FONT_SIZE - 2, rotation=rotation)

# 设置y轴标签为实际的任务名称
axs[0, 0].set_yticks(list(task_to_num.values()))
axs[0, 0].set_yticklabels(list(task_to_num.keys()))

# 设置横轴的日期范围和格式
min_start_date = df_main_tasks['start_date'].min() - pd.Timedelta(days=10)
max_end_date = df_main_tasks['end_date'].max() + pd.Timedelta(days=10)
axs[0, 0].set_xlim(min_start_date, max_end_date)
axs[0, 0].xaxis.set_major_locator(mdates.MonthLocator())
axs[0, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

# 添加标题和标签
axs[0, 0].set_title('Timetable from July 24 to Mar 25', fontsize=FONT_SIZE + 2, fontweight='bold')

# 添加图例
patches_legend = [mpatches.Patch(color=color, label=status) for status, color in STATUS_COLORS.items()]
category_legend = [mpatches.Patch(edgecolor=color, facecolor='none', linewidth=3, label=category) for category, color in
                   CATEGORY_COLORS.items()]
axs[0, 0].legend(handles=patches_legend + category_legend, fontsize=FONT_SIZE - 2, loc='upper right',
                 bbox_to_anchor=(1.15, 1))

# 添加网格
axs[0, 0].grid(True, alpha=0.3)

# 为训练课程子任务创建编号
subtask_to_num = {subtask: i for i, subtask in enumerate(df_subtasks_training_course['subtask'])}

# ----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------
# 绘制特定主任务的细节甘特图 (左下角)
'''
    Gantt图完全版 Version1.0
    状态：暂定完成
    细节Gantt图：
    - 子任务：[子任务名称]
    - 开始日期：[开始日期]
    - 结束日期：[结束日期]
    - 状态：[状态]
'''

for i, subtask in df_subtasks_training_course.iterrows():
    task_category = subtask['category']
    subtask_num = subtask_to_num[subtask['subtask']]
    axs[1, 0].barh(subtask_num, (subtask['end_date'] - subtask['start_date']).days, left=subtask['start_date'],
                   color=STATUS_COLORS[subtask['status']], edgecolor='black', linewidth=2, height=0.4)

# 设置y轴标签为实际的子任务名称
axs[1, 0].set_yticks(list(subtask_to_num.values()))
axs[1, 0].set_yticklabels(list(subtask_to_num.keys()))

# 设置横轴的日期范围和格式
min_start_date_task = df_subtasks_training_course['start_date'].min() - pd.Timedelta(days=10)
max_end_date_task = df_subtasks_training_course['end_date'].max() + pd.Timedelta(days=10)
axs[1, 0].set_xlim(min_start_date_task, max_end_date_task)
axs[1, 0].xaxis.set_major_locator(mdates.MonthLocator())
axs[1, 0].xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

# 添加标题
axs[1, 0].set_title('Sub-Gantt for Attending the Training Course', fontsize=FONT_SIZE + 2, fontweight='bold')

# 添加网格
axs[1, 0].grid(True, alpha=0.3)

# ----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------
# 绘制学习流程图 (右上角)
'''
    Gantt图完全版 Version1.0
    状态：待施工
    学习流程图：
    - 每个学习流程步骤创建一个唯一的编号
    - 每个学习流程步骤用条形图表示，条形图的高度为0.3
    - 每个学习流程步骤的条形图颜色由LEARNING_PROCESS_COLORS字典决定
    - 每个学习流程步骤的条形图边缘颜色为黑色，线条宽度为1
    - 每个学习流程步骤的条形图在y轴上的位置由步骤编号决定
    - 每个学习流程步骤的条形图的x轴范围由步骤的开始日期和结束日期决定
'''
ax_right = axs[0, 1]

# 为每个学习流程步骤创建一个唯一的编号
steps = df_learning_processes['Step'].unique()
step_to_num = {step: i for i, step in enumerate(steps[::-1])}  # 反转顺序，使得最上面的任务在图的顶部

for process in df_learning_processes['Process'].unique():
    process_data = df_learning_processes[df_learning_processes['Process'] == process]
    color = LEARNING_PROCESS_COLORS[process]

    for _, row in process_data.iterrows():
        step_num = step_to_num[row['Step']]
        ax_right.barh(step_num, (row['End Date'] - row['Start Date']).days,
                      left=row['Start Date'], color=color, edgecolor='black',
                      linewidth=1, height=0.3)

# 设置y轴标签为实际的步骤名称
ax_right.set_yticks(list(step_to_num.values()))
ax_right.set_yticklabels(list(step_to_num.keys()))

# 设置x轴为日期格式
ax_right.xaxis.set_major_locator(mdates.MonthLocator())
ax_right.xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

# 设置标题和标签
ax_right.set_title('Learning Processes Timeline', fontsize=FONT_SIZE + 2, fontweight='bold')
ax_right.set_xlabel('Date', fontsize=FONT_SIZE)

# 添加网格
ax_right.grid(True, alpha=0.3)

# 调整x轴范围以匹配主甘特图
ax_right.set_xlim(axs[0, 0].get_xlim())

# ----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*----------*
# 绘制技能树状图（右下角）
'''
    Gantt图完全版 Version1.0
    状态：暂定完成
    技能树状图：
    - 每个技能类别作为主干
    - 每个技能点作为主干上的分支
    - 技能点的时间作为分支的高度
    
    注意：由于技能树状图的数据量较大，可能需要调整绘图参数以适应页面大小
'''
ax_skill_tree = axs[1, 1]

# 获取唯一的主要类别和技能
categories = df_skills['Category'].unique()
skills = df_skills.groupby('Category')['Skill'].unique()

# 设置颜色
category_colors = plt.cm.Set3(np.linspace(0, 1, len(categories)))
skill_colors = plt.cm.Set2(np.linspace(0, 1, max(len(skill_set) for skill_set in skills)))

# 计算每个类别的水平位置
category_positions = {cat: i for i, cat in enumerate(categories)}

# 绘制树状图
for cat_idx, (category, category_color) in enumerate(zip(categories, category_colors)):
    category_data = df_skills[df_skills['Category'] == category]
    x = category_positions[category]

    # 绘制主类别线
    ax_skill_tree.plot([x, x], [category_data['Date'].min(), category_data['Date'].max()],
                       color=category_color, linewidth=2)

    # 添加类别标签
    ax_skill_tree.text(x, ax_skill_tree.get_ylim()[1], category,
                       ha='center', va='bottom', fontsize=10, fontweight='bold', rotation=45)

    for skill_idx, skill in enumerate(skills[category]):
        skill_data = category_data[category_data['Skill'] == skill]
        skill_x = x + (skill_idx + 1) * 0.2  # 调整这个值来改变子分支的间距

        # 绘制技能线
        ax_skill_tree.plot([skill_x, skill_x], [skill_data['Date'].min(), skill_data['Date'].max()],
                           color=skill_colors[skill_idx], linewidth=1.5)

        # 绘制从主类别到技能的连接线
        ax_skill_tree.plot([x, skill_x], [skill_data['Date'].min(), skill_data['Date'].min()],
                           color=category_color, linestyle=':', linewidth=1)

        # 添加技能标签
        ax_skill_tree.text(skill_x, skill_data['Date'].min(), skill,
                           ha='right', va='center', fontsize=8, fontweight='bold', rotation=45)

        for _, subskill in skill_data.iterrows():
            # 绘制子技能点
            ax_skill_tree.scatter(skill_x, subskill['Date'], color=skill_colors[skill_idx], s=30)

            # 添加子技能标签
            ax_skill_tree.text(skill_x + 0.05, subskill['Date'], subskill['SubSkill'],
                               ha='left', va='center', fontsize=7)

# 设置坐标轴
ax_skill_tree.set_xlim(-0.5, len(categories) - 0.5)

# 设置y轴（日期）
ax_skill_tree.yaxis.set_major_locator(mdates.MonthLocator())
ax_skill_tree.yaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
plt.setp(ax_skill_tree.yaxis.get_majorticklabels(), rotation=0)

# 隐藏x轴刻度
ax_skill_tree.xaxis.set_visible(False)

# 设置标题和标签
ax_skill_tree.set_title('Hierarchical Skill Development Over Time', fontsize=FONT_SIZE + 2, fontweight='bold')
ax_skill_tree.set_ylabel('Date', fontsize=FONT_SIZE)

# 添加网格
ax_skill_tree.grid(True, axis='y', linestyle='--', alpha=0.7)

# 设置y轴范围以匹配其他图表
ax_skill_tree.set_ylim(axs[0, 1].get_ylim())

# 反转y轴，使得较早的日期在顶部
ax_skill_tree.invert_yaxis()

# 调整子图之间的间距
plt.tight_layout()

# 显示图形
plt.show()