import sqlite3
import pandas as pd

# 连接到SQLite数据库（如果不存在则创建）
conn = sqlite3.connect('../tasks.db')
cursor = conn.cursor()

# 创建主任务表
cursor.execute('''
CREATE TABLE IF NOT EXISTS main_tasks (
    id INTEGER PRIMARY KEY,
    task TEXT,
    category TEXT,
    subtask TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT
)
''')

# 创建训练课程子任务表
cursor.execute('''
CREATE TABLE IF NOT EXISTS training_subtasks (
    id INTEGER PRIMARY KEY,
    task TEXT,
    category TEXT,
    subtask TEXT,
    start_date TEXT,
    end_date TEXT,
    status TEXT
)
''')

# 主任务数据
main_tasks = [
    ("Attend the training course", "Training", "Attend the training course", "2024-07-01", "2025-03-01", "In Progress"),
    ("Finish the review article", "Work", "Read related literature", "2024-07-01", "2024-09-01", "In Progress"),
    ("Finish the review article", "Work", "Write Article", "2024-09-02", "2024-09-30", "Not Started"),
    ("Finish the review article", "Work", "Optimization", "2024-09-30", "2025-01-15", "Not Started"),
    ("Complete Python Script(HPC)", "Work", "Requirements Analysis", "2024-07-01", "2024-07-15", "Completed"),
    ("Complete Python Script(HPC)", "Work", "Design", "2024-07-16", "2024-08-15", "Completed"),
    ("Complete Python Script(HPC)", "Work", "Implementation", "2024-08-16", "2024-10-15", "In Progress"),
    ("Complete Python Script(HPC)", "Work", "Unit Testing", "2024-10-16", "2024-11-15", "Not Started"),
    ("Complete Python Script(HPC)", "Work", "Integration Testing", "2024-11-16", "2024-12-15", "Not Started"),
    ("Complete Python Script(HPC)", "Work", "Deployment to HPC", "2024-12-16", "2025-01-15", "Not Started"),
    ("Complete Python Script(HPC)", "Work", "Maintenance and Optimization", "2025-01-16", "2025-03-01", "Not Started"),
    ("Write Transfer Report", "Work", "Write Report", "2024-10-01", "2024-11-01", "Not Started"),
    ("Write Transfer Report", "Work", "Optimization", "2024-11-01", "2024-12-15", "Not Started"),
    ("Conduct Experiments", "Research", "Design Experiments", "2024-07-15", "2024-08-15", "In Progress"),
    ("Conduct Experiments", "Research", "Run Experiments", "2024-08-16", "2024-11-30", "Not Started"),
    ("Conduct Experiments", "Research", "Analyze Results", "2024-12-01", "2025-01-31", "Not Started"),
    ("Attend Conferences", "Networking", "Prepare Presentation", "2024-09-01", "2024-09-30", "Not Started"),
    ("Attend Conferences", "Networking", "Attend Conference A", "2024-10-15", "2024-10-20", "Not Started"),
    ("Attend Conferences", "Networking", "Attend Conference B", "2025-02-01", "2025-02-05", "Not Started"),
    ("Publish Papers", "Research", "Draft Paper 1", "2024-11-01", "2024-12-31", "Not Started"),
    ("Publish Papers", "Research", "Submit and Revise Paper 1", "2025-01-01", "2025-02-28", "Not Started")
]

# 插入主任务数据
cursor.executemany('''
INSERT INTO main_tasks (task, category, subtask, start_date, end_date, status)
VALUES (?, ?, ?, ?, ?, ?)
''', main_tasks)

# 训练课程子任务数据
training_subtasks = [
    ("Attend the training course", "Training", "Introduction to Linux for HPC", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Introduction to High Performance Computing", "2024-07-01", "2024-07-31", "Finished"),
    ("Attend the training course", "Training", "Software development practices for Research", "2024-07-25", "2024-08-15", "Finished"),
    ("Attend the training course", "Training", "Applications and containers on HPC", "2024-09-10", "2024-10-15", "To do"),
    ("Attend the training course", "Training", "High Performance Python", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Word for Thesis Part 1A", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Word for Thesis Part 1B", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Word for Thesis Part 1C", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Word for Thesis Part 1D", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Word for Thesis Part 2", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Individual Writing Consultations for PGRs", "2024-07-31", "2025-03-01", "Time Unknown"),
    ("Attend the training course", "Training", "Foundations in Teaching", "2024-07-01", "2024-07-04", "Finished")
]

# 插入训练课程子任务数据
cursor.executemany('''
INSERT INTO training_subtasks (task, category, subtask, start_date, end_date, status)
VALUES (?, ?, ?, ?, ?, ?)
''', training_subtasks)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("Database setup completed.")