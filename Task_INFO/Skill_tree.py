import csv
from datetime import datetime

# 定义技能树
skill_tree = {
    "Programming": {
        "Python": {
            "Basics": "2024-07-01",
            "Data Structures": "2024-08-15",
            "Algorithms": "2024-10-01"
        },
        "Machine Learning": {
            "Supervised Learning": "2024-12-01",
            "Unsupervised Learning": "2025-01-15"
        }
    },
    "HPC": {
        "Linux": {
            "Bash Scripting": "2024-07-15"
        },
        "Parallel Computing": {
            "MPI": "2024-09-01",
            "OpenMP": "2024-10-01"
        }
    },
    "Data Analysis": {
        "Statistics": {
            "Descriptive Statistics": "2024-08-01",
            "Inferential Statistics": "2024-09-15"
        },
        "Big Data": {
            "Hadoop": "2024-11-15",
            "Spark": "2025-01-15"
        }
    }
}


# 将技能树转换为CSV格式
def skill_tree_to_csv(skill_tree, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Category', 'Skill', 'SubSkill', 'Date'])  # 写入表头

        for category, skills in skill_tree.items():
            for skill, subskills in skills.items():
                for subskill, date in subskills.items():
                    # 确保日期格式正确
                    try:
                        formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
                    except ValueError:
                        print(f"Warning: Invalid date format for {subskill}. Using original string.")
                        formatted_date = date

                    writer.writerow([category, skill, subskill, formatted_date])

    print(f"CSV file '{filename}' has been created successfully.")


# 运行转换
skill_tree_to_csv(skill_tree, '../skill_tree.csv')