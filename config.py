import matplotlib.pyplot as plt

# RGB转0-1标准化
def rgb_to_mpl(rgb):
    return tuple([x / 255.0 for x in rgb])

# 设置颜色映射，使用RGB值
STATUS_COLORS = {
    "Not Started": rgb_to_mpl((244, 62, 6)),  # YinZhu 银朱
    "In Progress": rgb_to_mpl((254, 186, 7)),  # HupoHuang 琥珀黄
    "Completed": rgb_to_mpl((65, 174, 60)),  # BaoShiLv 宝石绿
    "In Plan": rgb_to_mpl((14, 176, 201)),  # KongQueLan 孔雀蓝
    "Finished": rgb_to_mpl((44, 150, 120)),  # QingFanLv 青矾绿
    "To do": rgb_to_mpl((250, 126, 35)),  # Orange
    "Time Unknown": rgb_to_mpl((115, 124, 123))  # EHui 垩灰
}

# 设置任务类别的边框颜色，使用RGB值
CATEGORY_COLORS = {
    "Training": rgb_to_mpl((26, 148, 188)),  # Blue
    "Work": rgb_to_mpl((204, 204, 214)),  # Light Gray
    "Research": rgb_to_mpl((255, 127, 14)),  # Orange
    "Networking": rgb_to_mpl((44, 160, 44))  # Green
}

# 设置图形大小和字体
FONT_SIZE = 12
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = FONT_SIZE

# 学习流程颜色
LEARNING_PROCESS_COLORS = {
    "Academic Writing Learning Process": rgb_to_mpl((26, 148, 188)),
    "Linux and HPC Cluster Learning Process": rgb_to_mpl((255, 127, 14)),
    "Time Series Model Learning Process": rgb_to_mpl((44, 160, 44))
}