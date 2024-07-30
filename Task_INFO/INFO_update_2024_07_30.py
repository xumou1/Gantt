import sqlite3

# 连接到SQLite数据库
conn = sqlite3.connect('/tasks.db')
cursor = conn.cursor()

# 删除旧的 "Finish the review article" 相关任务
cursor.execute("DELETE FROM main_tasks WHERE task = 'Finish the review article'")

# 插入新的科学综述论文撰写流程任务
new_tasks = [
    ("Write Scientific Review", "Research", "Literature Search and Reading", "2024-07-01", "2024-08-15", "Not Started"),
    ("Write Scientific Review", "Research", "Develop Outline", "2024-08-16", "2024-08-31", "Not Started"),
    ("Write Scientific Review", "Research", "Write First Draft", "2024-09-01", "2024-10-31", "Not Started"),
    ("Write Scientific Review", "Research", "Revise and Refine", "2024-11-01", "2024-12-15", "Not Started"),
    ("Write Scientific Review", "Research", "Peer Review", "2024-12-16", "2025-01-15", "Not Started"),
    ("Write Scientific Review", "Research", "Final Revision and Submission", "2025-01-16", "2025-02-28", "Not Started")
]

# 插入新任务
cursor.executemany('''
INSERT INTO main_tasks (task, category, subtask, start_date, end_date, status)
VALUES (?, ?, ?, ?, ?, ?)
''', new_tasks)

# 提交更改并关闭连接
conn.commit()
conn.close()

print("Database updated with new Scientific Review writing process.")