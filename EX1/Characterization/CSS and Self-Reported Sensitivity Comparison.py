import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots


# Set the desired working directory
input_directory = r"C:\Users\julie\OneDrive - Danmarks Tekniske Universitet\Speciale\Analyse\JulieCode\CSS"
os.chdir(input_directory)

# Load the CSV file
data = pd.read_csv(os.path.join(input_directory, 'CSS_Sensitivity.csv'), sep=',')


#########################################################################################################################

# Define the lists of IDs for comparison
ID_sensitive = [34, 35, 65, 39, 19, 4, 22, 6, 7, 9, 47, 10, 31, 32, 15, 17, 37]
ID_non_sensitive = [1, 52, 2, 36, 18, 53, 38, 20, 54, 21, 56, 41, 23, 55, 57, 58, 24, 42, 26, 59, 44, 27, 8, 69, 28, 29, 30, 61, 45, 46, 11, 63, 64, 49, 13, 14, 66, 16, 51, 67, 50, 68]

# Filter participants with IAQ_CSS == 1 and IAQ_CSS == 0
sensitive = data[data['IAQ_CSS'] == 1][['ID', 'Total_Score']]
non_sensitive = data[data['IAQ_CSS'] == 0][['ID', 'Total_Score']]

# Check mismatches for sensitive and non-sensitive groups
sensitive_mismatch = sensitive[~sensitive['ID'].isin(ID_sensitive)].copy()
sensitive_mismatch['Group'] = 'Sensitive Mismatch'
non_sensitive_mismatch = non_sensitive[~non_sensitive['ID'].isin(ID_non_sensitive)].copy()
non_sensitive_mismatch['Group'] = 'Non-Sensitive Mismatch'

# Combine both mismatched dataframes into one
combined_mismatch = pd.concat([sensitive_mismatch, non_sensitive_mismatch])

print(len(combined_mismatch))


# Output the results
print("Persons in this have defined themselves as non-sensitive but are actually sensitive:")
print(sensitive_mismatch)
print("Persons in this have defined themselves as sensitive but are actually non-sensitive:")
print(non_sensitive_mismatch)


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
custom_palette = ["#AACCEE", "#CCDDAA"]

# Apply the custom color palette
sns.set_palette(custom_palette)


#########################################################################################################################

# Boxplot of sensitivity mismatches between CSS and self-reports


# Create the boxplot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.boxplot(x='Group', y='Total_Score', data=combined_mismatch, palette=custom_palette, zorder=3)

# Set y-axis limits from 0 to 105
plt.ylim(0, 105)

# Add titles and labels
plt.title('Boxplot of Sensitivity Mismatches Between CSS and Self-Reports', fontsize=20, zorder=4)
plt.xlabel('Mismatch Group', fontsize=18, zorder=4)
plt.ylabel('Sensitivity Score from CSS', fontsize=18, zorder=4)

# Set tick font sizes
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()


#########################################################################################################################

# Pie chart for self-reported sensitivity


# Calculate the sizes for each category
sensitive_count = len(ID_sensitive)
non_sensitive_count = len(ID_non_sensitive)

# Pie chart labels and sizes
labels = ['Sensitive', 'Non-Sensitive']
sizes = [sensitive_count, non_sensitive_count]
colors = ["#CCDDAA", "#AACCEE"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(7, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=00)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)  

plt.title('Self-Reported Sensitivity', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Pie chart for CSS sensitivity


# Calculate the sizes for each category
sensitiveCSS_count = len(sensitive)
non_sensitiveCSS_count = len(non_sensitive)

# Pie chart labels and sizes
labels = ['Sensitive', 'Non-Sensitive']
sizes = [sensitiveCSS_count, non_sensitiveCSS_count]
colors = ["#CCDDAA", "#AACCEE"]
explode = [0.002, 0.002] 

# Create the pie chart
plt.figure(figsize=(7, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=-10)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('CSS Sensitivity', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()