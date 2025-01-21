import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots
from collections import Counter


# List of genders
gender_list = [
    "Female", "Female", "Male", "Female", "Male", "Female", "Female", "Female", "Female", 
    "Female", "Male", "Male", "Male", "Female", "Male", "Female", "Female", "Male", 
    "Male", "Male", "Male", "Female", "Female", "Female", "Male", "Female", "Female", 
    "Female", "Female", "Male", "Male", "Female", "Female", "Male", "Female", "Male", 
    "Male", "Female", "Female"
]

# List of ages
ages = [
    25, 23, 23, 26, 22, 27, 19, 19, 23, 33, 18, 26, 24, 24, 24, 22, 22, 22, 22, 
    21, 24, 22, 28, 20, 26, 25, 24, 22, 23, 21, 20, 34, 23, 22, 27, 24, 22, 22, 22
]


#########################################################################################################################

# Custom function to display percentage and count in Pie Charts
def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        count = int(round(pct * total / 100.0))
        return f'{pct:.1f}%\n({count})'  # Shows percentage and count
    return my_autopct


#########################################################################################################################

# Style for charts


# Activate the 'science' style
plt.style.use(['science', 'no-latex'])

# Define a custom color palette
custom_palette = ["#CCDDAA", "#AACCEE"]

# Apply the custom color palette
sns.set_palette(custom_palette)


#########################################################################################################################

# Pie chart for gender


# Count occurrences of each gender
gender_counts = Counter(gender_list)

# Pie chart labels and sizes
labels = ['Women', 'Men']
sizes = gender_counts.values()
colors = custom_palette
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(7, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=120)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)  

plt.title('Gender Distribution of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar chart for age


# Count frequency of each age
age_counts = Counter(ages)

# Extract ages and their counts for plotting
ages_sorted = sorted(age_counts.keys())  # Sorted ages for better display
counts_sorted = [age_counts[age] for age in ages_sorted]

# Determine maximum frequency for y-axis ticks
max_frequency = max(counts_sorted)

# Create bar chart
plt.figure(figsize=(10, 7))
plt.bar(ages_sorted, counts_sorted, color=custom_palette[0], edgecolor='black', zorder=3)

# Customize the chart
plt.title('Age Distribution of Participants', fontsize=20, zorder=4)
plt.xlabel('Age', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(ticks=range(min(ages), max(ages) + 1), fontsize=16, zorder=4)
plt.yticks(ticks=range(0, max_frequency + 1), fontsize=16, zorder=4)
plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)

# Show the plot
plt.show()