import seaborn as sns
import pandas as pd
import matplotlib
import matplotlib.patches as mpatches
import tkinter as tk
matplotlib.use('TkAgg')  # Set the backend to TkAgg
import matplotlib.pyplot as plt

# Assuming `df` is your DataFrame
df = pd.read_csv('only_symptoms_DIG_standard_with_scores.csv')

target_columns = [f"Min Confidence for diagnosis {i+1}" for i in range(8)]

# Replace these with the actual column names you want to convert
numeric_columns = ['ICD count', 'Avey code count'] + target_columns
df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric, errors='coerce')

# Fields to plot against
fields = ['Confidence', 'Min Confidence', 'Confidence Age Seriousness']
target = fields[1]

group_by_list = ['ICD count', 'Avey code count']
group_by = group_by_list[1]

#####################################################################################

# Calculate the average confidence for each diagnosis across different ICD counts
average_confidences = df.groupby(group_by)[[f'{target} for diagnosis {i+1}' for i in range(8)]].mean()

# Count the number of instances for each ICD count
instance_counts = df[group_by].value_counts().sort_index()

# Plotting
fig, ax = plt.subplots(figsize=(14, 7))
average_confidences.plot(kind='bar', ax=ax)
plt.title(f'Average {target} for Each Diagnosis by {group_by}')

# Create new x-axis labels with instance counts
labels = [f'{group_by} {icd}\n(n={count})' for icd, count in instance_counts.items()]
ax.set_xticklabels(labels)

plt.xlabel(f'{group_by}')
plt.ylabel(f'Average {target}')
grey_patch = mpatches.Patch(color='red', label='The red data')
plt.legend(handles=[red_patch])
plt.legend(title='Diagnosis')
plt.tight_layout()

# Save the plot to a file
plt.savefig(f'average_{"_".join(target.lower().split())}_by_{"_".join(group_by.lower().split())}.png', dpi=300)  # Save as a PNG file with high resolution
#plt.savefig(f'average_{"_".join(target.lower().split())}_by_{"_".join(group_by.lower().split())}.svg', format='svg')  # Save as an SVG file for vector graphics

# Show the plot
plt.show()