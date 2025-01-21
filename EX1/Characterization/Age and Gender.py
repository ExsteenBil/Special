import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots


# Set the desired working directory
input_directory = r"C:\Users\julie\OneDrive - Danmarks Tekniske Universitet\Speciale\Analyse\Survey"
os.chdir(input_directory)

# Load the CSV file
data = pd.read_csv(os.path.join(input_directory, 'Deltagere-Total.csv'), sep=';')


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

# Pie chart for gender


# Count occurrences of each unique value in the 'gender' column
gender_counts = data['Køn'].value_counts()

# Pie chart labels and sizes
labels = ['Men', 'Women']
sizes = [gender_counts.get('Mand', 0), gender_counts.get('Kvinde', 0)]  # Counts for 'Mand' and 'Kvinde'
colors = custom_palette
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(7, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=130)

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

# Pie chart for age


# Count occurrences of each unique value in the 'Age' column
age_counts = data['Gruppe'].value_counts()

# Pie chart labels and sizes
labels = ['Juniors', 'Seniors']
sizes = [age_counts.get(1, 0), age_counts.get(2, 0)]
colors = custom_palette
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(7, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=130)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)  

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Age Groups of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()