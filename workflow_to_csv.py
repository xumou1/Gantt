import csv
from datetime import datetime, timedelta

# Define the work flow data
work_flow_data = [
    {
        "Project": "HPC Script Development",
        "Phase": "Planning",
        "Task": "Requirements Gathering",
        "Start Date": "2024-07-01",
        "End Date": "2024-07-15",
        "Related Tasks": []
    },
    {
        "Project": "HPC Script Development",
        "Phase": "Development",
        "Task": "Code Implementation",
        "Start Date": "2024-07-16",
        "End Date": "2024-09-30",
        "Related Tasks": ["Requirements Gathering"]
    },
    {
        "Project": "HPC Script Development",
        "Phase": "Testing",
        "Task": "Unit Testing",
        "Start Date": "2024-10-01",
        "End Date": "2024-10-31",
        "Related Tasks": ["Code Implementation"]
    },
    {
        "Project": "HPC Script Development",
        "Phase": "Testing",
        "Task": "Integration Testing",
        "Start Date": "2024-11-01",
        "End Date": "2024-11-30",
        "Related Tasks": ["Unit Testing"]
    },
    {
        "Project": "HPC Script Development",
        "Phase": "Deployment",
        "Task": "HPC Deployment",
        "Start Date": "2024-12-01",
        "End Date": "2024-12-31",
        "Related Tasks": ["Integration Testing"]
    },
    {
        "Project": "HPC Script Development",
        "Phase": "Maintenance",
        "Task": "Performance Optimization",
        "Start Date": "2025-01-01",
        "End Date": "2025-02-28",
        "Related Tasks": ["HPC Deployment"]
    },
    {
        "Project": "Transfer Report",
        "Phase": "Writing",
        "Task": "Literature Review",
        "Start Date": "2024-07-01",
        "End Date": "2024-08-31",
        "Related Tasks": []
    },
    {
        "Project": "Transfer Report",
        "Phase": "Writing",
        "Task": "Draft Report",
        "Start Date": "2024-09-01",
        "End Date": "2024-10-31",
        "Related Tasks": ["Literature Review", "Code Implementation"]
    },
    {
        "Project": "Transfer Report",
        "Phase": "Review",
        "Task": "Internal Review",
        "Start Date": "2024-11-01",
        "End Date": "2024-11-30",
        "Related Tasks": ["Draft Report"]
    },
    {
        "Project": "Transfer Report",
        "Phase": "Revision",
        "Task": "Revise Report",
        "Start Date": "2024-12-01",
        "End Date": "2024-12-31",
        "Related Tasks": ["Internal Review", "Integration Testing"]
    }
]

# Write data to CSV file
with open('work_flow_with_relations.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Project", "Phase", "Task", "Start Date", "End Date", "Related Tasks"])
    writer.writeheader()
    for row in work_flow_data:
        row["Related Tasks"] = ", ".join(row["Related Tasks"])
        writer.writerow(row)

print("Work flow CSV file with task relations has been generated successfully.")