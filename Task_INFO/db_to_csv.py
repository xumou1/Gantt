import sqlite3
import pandas as pd


def export_table_to_csv(db_path, table_name, csv_path):
    # 连接到SQLite数据库
    conn = sqlite3.connect(db_path)

    # 读取表格数据到DataFrame
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

    # 将DataFrame导出为CSV文件
    df.to_csv(csv_path, index=False)

    # 关闭数据库连接
    conn.close()

    print(f"Table '{table_name}' has been exported to '{csv_path}'")


# 数据库文件路径
db_path = '../tasks.db'

# 导出主任务表
export_table_to_csv(db_path, 'main_tasks', '../main_tasks.csv')

# 导出训练课程子任务表
export_table_to_csv(db_path, 'training_subtasks', '../training_subtasks.csv')

print("Export completed.")