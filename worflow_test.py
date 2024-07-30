import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import ConnectionPatch

# Load the work flow data
df_work_flow = pd.read_csv('work_flow_with_relations.csv', parse_dates=['Start Date', 'End Date'])

# Create the plot
fig, ax = plt.subplots(figsize=(24, 16))  # Increased figure size

# Get unique projects and phases
projects = df_work_flow['Project'].unique()
phases = df_work_flow.groupby('Project')['Phase'].unique()

# Set colors
project_colors = plt.cm.Set3(np.linspace(0, 1, len(projects)))
phase_colors = plt.cm.Set2(np.linspace(0, 1, max(len(phase_set) for phase_set in phases)))

# Calculate horizontal positions for projects
project_positions = {proj: i for i, proj in enumerate(projects)}

# Dictionary to store task positions
task_positions = {}

# Calculate the total width needed
total_width = len(projects) * 3  # 3 units per project

# Draw tree diagram
for proj_idx, (project, project_color) in enumerate(zip(projects, project_colors)):
    project_data = df_work_flow[df_work_flow['Project'] == project]
    x = (proj_idx + 0.5) * (total_width / len(projects))  # Distribute projects evenly

    # Draw main project line
    ax.plot([x, x], [project_data['Start Date'].min(), project_data['End Date'].max()],
            color=project_color, linewidth=3)

    # Add project label
    ax.text(x, project_data['End Date'].max() + pd.Timedelta(days=15), project,
            ha='center', va='bottom', fontsize=12, fontweight='bold', rotation=0)

    phase_width = (total_width / len(projects)) / (len(phases[project]) + 1)
    for phase_idx, phase in enumerate(phases[project]):
        phase_data = project_data[project_data['Phase'] == phase]
        phase_x = x + (phase_idx + 1 - len(phases[project])/2) * phase_width  # Center phases around project line

        # Draw phase line
        ax.plot([phase_x, phase_x], [phase_data['Start Date'].min(), phase_data['End Date'].max()],
                color=phase_colors[phase_idx], linewidth=2)

        # Draw connection line from project to phase
        ax.plot([x, phase_x], [phase_data['Start Date'].min(), phase_data['Start Date'].min()],
                color=project_color, linestyle='--', linewidth=1.5)

        # Add phase label
        ax.text(phase_x, phase_data['Start Date'].min() - pd.Timedelta(days=7), phase,
                ha='right', va='center', fontsize=10, fontweight='bold', rotation=45)

        for task_idx, (_, task) in enumerate(phase_data.iterrows()):
            # Calculate vertical offset for tasks within the same phase
            offset = task_idx * 0.2  # Adjust this value to change vertical spacing between tasks
            task_y = task['Start Date'] + pd.Timedelta(days=offset)

            # Draw task point
            task_point = ax.scatter(phase_x, task_y, color=phase_colors[phase_idx], s=40)

            # Add task label with adjusted position
            ax.text(phase_x + 0.1, task_y, task['Task'],
                    ha='left', va='center', fontsize=8, rotation=0)

            # Store task position
            task_positions[task['Task']] = (phase_x, task_y)

# Draw relations between tasks
for _, task in df_work_flow.iterrows():
    if isinstance(task['Related Tasks'], str):
        related_tasks = task['Related Tasks'].split(', ')
        for related_task in related_tasks:
            if related_task in task_positions and task['Task'] in task_positions:
                start = task_positions[related_task]
                end = task_positions[task['Task']]
                con = ConnectionPatch(xyA=start, xyB=end, coordsA="data", coordsB="data",
                                      axesA=ax, axesB=ax, arrowstyle="->", color='gray', alpha=0.5,
                                      connectionstyle="arc3,rad=0.3")
                ax.add_artist(con)

# Set axis limits and labels
ax.set_xlim(0, total_width)
ax.yaxis.set_major_locator(mdates.MonthLocator())
ax.yaxis.set_major_formatter(mdates.DateFormatter('%b %y'))
plt.setp(ax.yaxis.get_majorticklabels(), rotation=0)

# Hide x-axis ticks
ax.xaxis.set_visible(False)

# Set title and labels
ax.set_title('Work Flow Timeline with Task Relations', fontsize=16, fontweight='bold')
ax.set_ylabel('Date', fontsize=12)

# Add grid
ax.grid(True, axis='y', linestyle='--', alpha=0.7)

# Set y-axis range to include all data points
ax.set_ylim(df_work_flow['Start Date'].min() - pd.Timedelta(days=30),
            df_work_flow['End Date'].max() + pd.Timedelta(days=30))
ax.invert_yaxis()

# Add legend
legend_elements = [Line2D([0], [0], color=color, lw=2, label=proj)
                   for proj, color in zip(projects, project_colors)]
legend_elements.append(Line2D([0], [0], color='gray', lw=1, ls='-.', label='Task Relation'))
ax.legend(handles=legend_elements, loc='upper right', fontsize=10, bbox_to_anchor=(1.25, 1))

# Adjust layout
plt.tight_layout()
plt.subplots_adjust(right=0.95, bottom=0.1, top=0.9, left=0.05)

# Show the plot
plt.show()