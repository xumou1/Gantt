import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.dates as mdates
import matplotlib.patches as mpatches

# 创建任务数据，包含主任务和子任务，并添加状态和类别
tasks = [
    {"Task": "Attend the training course", "Category": "Training", "Subtask": "Attend the training course",
     "Start": "2024-07-01", "End": "2025-03-01", "Status": "In Progress"},
    {"Task": "Finish the review article", "Category": "Work", "Subtask": "Read related literature",
     "Start": "2024-07-01", "End": "2024-09-01", "Status": "In Progress"},
    {"Task": "Finish the review article", "Category": "Work", "Subtask": "Write Article",
     "Start": "2024-09-02", "End": "2024-09-30", "Status": "Not Started"},
    {"Task": "Finish the review article", "Category": "Work", "Subtask": "Optimization",
     "Start": "2024-09-30", "End": "2025-01-15", "Status": "Not Started"},
    {"Task": "Complete Python Script(HPC)", "Category": "Work", "Subtask": "Write Script",
     "Start": "2024-07-01", "End": "2024-10-01", "Status": "In Progress"},
    {"Task": "Complete Python Script(HPC)", "Category": "Work", "Subtask": "(1)",
     "Start": "2024-10-01", "End": "2024-10-15", "Status": "In Plan"},
    {"Task": "Complete Python Script(HPC)", "Category": "Work", "Subtask": "(2)",
     "Start": "2024-10-15", "End": "2024-10-31", "Status": "Not Started"},
    {"Task": "Complete Python Script(HPC)", "Category": "Work", "Subtask": "(3)",
     "Start": "2024-11-01", "End": "2024-11-10", "Status": "Not Started"},
    {"Task": "Complete Python Script(HPC)", "Category": "Work", "Subtask": "(4)",
     "Start": "2024-11-10", "End": "2024-11-30", "Status": "Not Started"},
    {"Task": "Complete Python Script(HPC)", "Category": "Work", "Subtask": "Optimization",
     "Start": "2024-12-01", "End": "2025-03-01", "Status": "In Plan"},
    {"Task": "Write Transfer Report", "Category": "Work", "Subtask": "Write Report",
     "Start": "2024-10-01", "End": "2024-11-01", "Status": "Not Started"},
    {"Task": "Write Transfer Report", "Category": "Work", "Subtask": "Optimization",
     "Start": "2024-11-01", "End": "2024-12-15", "Status": "Not Started"}
]

# 转换为DataFrame
df = pd.DataFrame(tasks)

# 转换日期格式
df['Start'] = pd.to_datetime(df['Start'])
df['End'] = pd.to_datetime(df['End'])

# RGB转0-1标准化
def rgb_to_mpl(rgb):
    return tuple([x / 255.0 for x in rgb])

# 设置颜色映射，使用RGB值
status_colors = {
    "Not Started": rgb_to_mpl((255, 0, 0)),      # Red
    "In Progress": rgb_to_mpl((255, 255, 0)),    # Yellow
    "Completed": rgb_to_mpl((0, 255, 0)),         # Green
    "In Plan": rgb_to_mpl((0, 255, 255)),         # Green
}

# 设置任务类别的边框颜色，使用RGB值
category_colors = {
    "Training": rgb_to_mpl((0, 0, 255)),         # Blue
    "Work": rgb_to_mpl((255, 165, 0))            # Orange
}

# 设置图形大小和字体
font_size = 12  # 可以调整字体大小
plt.figure(figsize=(12, 8))
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = font_size

# 创建甘特图
unique_tasks = df['Task'].unique()
for task in unique_tasks:
    task_data = df[df['Task'] == task]
    task_category = task_data['Category'].iloc[0]
    # 绘制主任务的边框
    main_task_start = task_data['Start'].min()
    main_task_end = task_data['End'].max()
    plt.barh(task, (main_task_end - main_task_start).days, left=main_task_start, edgecolor=category_colors[task_category], color='none', linewidth=10)  # 加粗边框并设置颜色
    # 绘制子任务
    for i, subtask in task_data.iterrows():
        plt.barh(task, (subtask['End'] - subtask['Start']).days, left=subtask['Start'], color=status_colors[subtask['Status']], edgecolor='black', linewidth = 2)  # 设置边框为无色
        # 在子任务色块上显示子任务名字
        plt.text(subtask['Start'] + (subtask['End'] - subtask['Start']) / 2, task, subtask['Subtask'], ha='center', va='center', color='black', fontsize=font_size)

# 设置横轴的日期范围
min_start_date = df['Start'].min() - pd.Timedelta(days=10)
max_end_date = df['End'].max() + pd.Timedelta(days=10)
plt.xlim(min_start_date, max_end_date)

# 设置日期格式为 mm-yy
plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b %y'))

# 添加标题和标签
# plt.xlabel('Date', fontsize=font_size, fontweight='bold')
# plt.ylabel('Tasks', fontsize=font_size, fontweight='bold')
plt.title('Gantt Chart with Main Tasks and Subtasks', fontsize=font_size + 18, fontweight='bold')

# 添加图例
patches_legend = [mpatches.Patch(color=color, label=status) for status, color in status_colors.items()]
category_legend = [mpatches.Patch(edgecolor=color, facecolor='none', linewidth=3, label=category) for category, color in category_colors.items()]
plt.legend(handles=patches_legend + category_legend, fontsize=font_size, loc='upper right')

# 自动调整日期标签
plt.gcf().autofmt_xdate()

# 添加网格
plt.grid(True)

# 添加注释
plt.annotate('This is a custom annotation.', xy=(0, -0.15), xycoords='axes fraction', ha='left', va='center', fontsize=font_size)
plt.annotate('(1) Combine Different Models', xy=(0, -0.2), xycoords='axes fraction', ha='left', va='center', fontsize=font_size)
plt.annotate('(2) Check HPC environment', xy=(0, -0.25), xycoords='axes fraction', ha='left', va='center', fontsize=font_size)
plt.annotate('(3) Test Script on HPC', xy=(0, -0.3), xycoords='axes fraction', ha='left', va='center', fontsize=font_size)
plt.annotate('(4) Get Final Results', xy=(0, -0.35), xycoords='axes fraction', ha='left', va='center', fontsize=font_size)

# 将图以600 DPI, JPEG格式导出
plt.savefig('gantt_chart.jpg', format='jpeg', dpi=600, bbox_inches='tight')

# 显示图形
plt.show()
