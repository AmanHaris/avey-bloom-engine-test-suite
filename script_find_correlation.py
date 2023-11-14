
import csv
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import numpy as np


# Fields to plot against
fields = ['Confidence', 'Min Confidence', 'Confidence Age Seriousness']
target = fields[2]

# which ICD/avey code count we're plotting for
code_count = 1


column_names = [f'{target} for diagnosis {i+1}' for i in range(8)]
diagnoses = []

with open('only_symptoms_DIG_standard_with_scores.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        diagnoses_str = row['Any reasonable diagnoses? (Pick 1-8)']
        diagnoses_list = []
        if diagnoses_str:
            diagnoses_list = diagnoses_str.split(',')
        confidences = [row[column_names[i]] for i in range(8)]
        diagnoses.append((row['ID'], diagnoses_list, confidences, int(row['ICD count'])))

# for entry in diagnoses:
#     print(entry)

print(len(diagnoses))

# plot diagnoses with ID as the x axis and confidence as the y axis. Mark in a special color the diagnoses that are in the diagnosis_list for that ID.
colors = ['grey' for i in range(8)]  # colors for each diagnosis
highlight_color = '#77e0ff'  # color to highlight picked diagnoses

# Filter the diagnoses to only include entries where the 'ICD count' is code_count
filtered_diagnoses = [entry for entry in diagnoses if entry[3] == code_count]

# Plotting
fig, ax = plt.subplots(figsize=(14, 7))

for index, (id, diagnosis_list, confidences, _) in enumerate(filtered_diagnoses):
    print(id, diagnoses_list, confidences)
    bar_colors = [highlight_color if str(i+1) in diagnosis_list else colors[i] for i in range(8)]
    x = np.arange(8) + index*10  # offset x-coordinates for each batch
    confidences = [float(s) if s!='' else 0.0 for s in confidences]
    ax.bar(x, confidences, color=bar_colors, width=1)

ax.set_xticklabels(["" for i in range(len(filtered_diagnoses))])
title = f'{target} for Each Diagnosis by ID for claims with {code_count} ICD Codes'
plt.title(title)
plt.xlabel('ID')
plt.ylabel(target)


blue_patch = mpatches.Patch(color='#77e0ff', label='Approved Diagnoses')
grey_patch = mpatches.Patch(color='grey', label='Rejected Diagnoses')
plt.legend(handles=[blue_patch, grey_patch])
plt.tight_layout()

# Save the plot to a file
plt.savefig(f'{title}.png', dpi=300)  # Save as a PNG file with high resolution

plt.show()