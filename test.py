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

# 创建一个2x2的子图布局
fig, axs = plt.subplots(2, 2, figsize=(24, 24), gridspec_kw={'width_ratios': [2, 1]})

# 创建任务到数字的映射
unique_tasks = df_main_tasks['task'].unique()
task_to_num = {task: i for i, task in enumerate(unique_tasks)}

# 绘制整体甘特图 (左上角)
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

# 绘制特定主任务的细节甘特图 (左下角)
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

# 绘制学习流程图 (右侧)
ax_right = axs[0, 1]  # 使用已有的子图，而不是创建新的

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

# 调整子图之间的间距
plt.tight_layout()

# 添加技能树状图（右下角）
ax_skill_tree = axs[1, 1]

# 定义技能数据
skills = {
    'Programming': [
        ('Python Basics', '2024-07-01'),
        ('Data Structures', '2024-08-15'),
        ('Algorithms', '2024-10-01'),
        ('Machine Learning', '2024-12-01'),
        ('Deep Learning', '2025-02-01')
    ],
    'HPC': [
        ('Linux Basics', '2024-07-15'),
        ('Parallel Computing', '2024-09-01'),
        ('MPI', '2024-11-01'),
        ('GPU Programming', '2025-01-01')
    ],
    'Data Analysis': [
        ('Statistics', '2024-08-01'),
        ('Data Visualization', '2024-09-15'),
        ('Big Data Tools', '2024-11-15'),
        ('Time Series Analysis', '2025-01-15')
    ]
}

# 设置颜色
colors = plt.cm.Set3(np.linspace(0, 1, len(skills)))

# 绘制树状图
for i, (skill_category, skill_list) in enumerate(skills.items()):
    x = i * 2  # 水平位置
    dates = [pd.to_datetime(date) for _, date in skill_list]
    y = mdates.date2num(dates)

    # 绘制主干
    ax_skill_tree.plot([x, x], [y[0], y[-1]], color=colors[i], linewidth=2)

    # 绘制分支和技能点
    for j, (skill, _) in enumerate(skill_list):
        ax_skill_tree.plot([x, x + 1], [y[j], y[j]], color=colors[i])
        ax_skill_tree.scatter(x + 1, y[j], color=colors[i], s=50)
        ax_skill_tree.text(x + 1.1, y[j], skill, va='center', ha='left', fontsize=8)

    # 添加技能类别标签
    ax_skill_tree.text(x, y[-1], skill_category, va='bottom', ha='center', fontsize=10, fontweight='bold')

# 设置坐标轴
ax_skill_tree.yaxis_date()
ax_skill_tree.yaxis.set_major_locator(mdates.MonthLocator())
ax_skill_tree.yaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))

ax_skill_tree.set_xlim(-1, len(skills) * 2)
ax_skill_tree.set_ylim(ax_skill_tree.get_ylim()[::-1])  # 反转 y 轴，使时间从上到下

ax_skill_tree.set_title('Skill Development Over Time', fontsize=FONT_SIZE + 2, fontweight='bold')
ax_skill_tree.set_xlabel('Skills', fontsize=FONT_SIZE)
ax_skill_tree.set_ylabel('Time', fontsize=FONT_SIZE)

ax_skill_tree.set_xticks([])
ax_skill_tree.grid(True, axis='y', linestyle='--', alpha=0.7)

# 调整子图之间的间距
plt.tight_layout()

'''
# 添加注释
fig.text(0.01, 0.01, 'Annotation for Complete Python Script(HPC):', ha='left', va='bottom', fontsize=FONT_SIZE + 3,
         fontweight='bold')
fig.text(0.01, 0.005, 'The task follows standard Software Development Life Cycle (SDLC)', ha='left', va='bottom',
         fontsize=FONT_SIZE)
fig.text(0.01, 0, 'including Requirements Analysis, Design, Implementation,', ha='left', va='bottom',
         fontsize=FONT_SIZE)
fig.text(0.01, -0.005, 'Testing (Unit and Integration), Deployment, and Maintenance.', ha='left', va='bottom',
         fontsize=FONT_SIZE)
'''

# 将图以600 DPI, JPEG格式导出
# plt.savefig('complex_gantt_chart_with_learning_processes_english.jpg', format='jpeg', dpi=600, bbox_inches='tight')

# 显示图形
plt.show()