import csv
from datetime import datetime

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

# 创建CSV文件并写入数据
with open('../skill_development.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # 写入表头
    writer.writerow(['Category', 'Skill', 'Date'])

    # 遍历技能数据并写入CSV
    for category, skill_list in skills.items():
        for skill, date in skill_list:
            # 将日期字符串转换为datetime对象，然后格式化为所需的字符串格式
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            formatted_date = date_obj.strftime('%Y-%m-%d')
            writer.writerow([category, skill, formatted_date])

print("CSV file 'skill_development.csv' has been created successfully.")