import csv

learning_processes = {
    "Academic Writing Learning Process": [
        "Understanding the importance of academic writing",
        "Learning the basic structure of academic writing",
        "Mastering literature review techniques",
        "Learning citation and reference formats",
        "Practicing academic paper writing",
        "Accepting peer review and revision",
        "Participating in academic conferences and seminars"
    ],
    "Linux and HPC Cluster Learning Process": [
        "Learning basic Linux commands",
        "Understanding high-performance computing concepts",
        "Learning parallel programming models",
        "Mastering job scheduling system usage",
        "Learning performance optimization techniques",
        "Practicing large-scale computing tasks",
        "Understanding data management and storage"
    ],
    "Time Series Model Learning Process": [
        "Understanding time series data characteristics",
        "Learning basic statistics and probability theory",
        "Mastering classical time series models (ARIMA)",
        "Learning state space models",
        "Understanding machine learning applications in time series",
        "Learning deep learning time series models",
        "Practicing real dataset analysis"
    ]
}

# Assign start and end dates for each process
start_dates = {
    "Academic Writing Learning Process": "2024-07-01",
    "Linux and HPC Cluster Learning Process": "2024-07-15",
    "Time Series Model Learning Process": "2024-08-01"
}

end_dates = {
    "Academic Writing Learning Process": "2025-03-01",
    "Linux and HPC Cluster Learning Process": "2025-02-15",
    "Time Series Model Learning Process": "2025-02-28"
}

# Write to CSV
with open('../learning_processes.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Process', 'Step', 'Start Date', 'End Date'])

    for process, steps in learning_processes.items():
        for i, step in enumerate(steps):
            writer.writerow([process, step, start_dates[process], end_dates[process]])

print("Learning processes have been exported to 'learning_processes.csv'")