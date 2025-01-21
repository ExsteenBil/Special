import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots


# Set the desired working directory
input_directory = r"C:\Users\julie\OneDrive - Danmarks Tekniske Universitet\Speciale\Grundlag\1-Data-Raw-Air-Quality\Data-Questionnaires"
os.chdir(input_directory)

# Load the CSV file
data = pd.read_csv(os.path.join(input_directory, 'Exit_Gigantos-CSV-Filer-redigeret.csv'), sep=';')


#########################################################################################################################

# Medication
# Group by participant ID and Filter, and check for medication usage (for bar chart)
grouped_medication = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'])['Did you take any medication during the flight?'].agg(lambda x: 'Medication' if 'Yes' in x.values else 'No_medication')
# Reset index for visualization
grouped_medication = grouped_medication.reset_index()
# Group by participant ID and determine if they took medication at least once (for pie chart)
unique_medication = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Did you take any medication during the flight?'].agg(lambda x: 'Medication' if 'Yes' in x.values else 'No_medication')


# Eye drops
# Group by participant ID and Filter, and check for medication usage (for bar chart)
grouped_eyedrops = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'])['Did you use eye drops?'].agg(lambda x: 'Eyedrops' if 'Yes' in x.values else 'No_eyedrops')
# Reset index for visualization
grouped_eyedrops = grouped_eyedrops.reset_index()
# Group by participant ID and determine if they took medication at least once (for pie chart)
unique_eyedrops = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Did you use eye drops?'].agg(lambda x: 'Eyedrops' if 'Yes' in x.values else 'No_eyedrops')


# Hand cream
# Group by participant ID and Filter, and check for hand cream usage (for bar chart)
grouped_handcream = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'])['Did you use hand lotion?'].agg(lambda x: 'Handcream' if 'Yes' in x.values else 'No_handcream')
# Reset index for visualization
grouped_handcream = grouped_handcream.reset_index()
# Group by participant ID and determine if they used hand cream at least once (for pie chart)
unique_handcream = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Did you use hand lotion?'].agg(lambda x: 'Handcream' if 'Yes' in x.values else 'No_handcream')


# Contact lenses
# Group by participant ID and Filter, and check for contact lens usage (for bar chart)
grouped_contacts = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'])['Did you wear contact lenses?'].agg(lambda x: 'Contactlenses' if 'Yes' in x.values else 'No_contactlenses')
# Reset index for visualization
grouped_contacts = grouped_contacts.reset_index()
# Group by participant ID and determine if they wore contact lenses at least once (for pie chart)
unique_contacts = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Did you wear contact lenses?'].agg(lambda x: 'Contactlenses' if 'Yes' in x.values else 'No_contactlenses')


# Noise cancelling headphones
# Group by participant ID and Filter, and check for noise cancelling headphones usage (for bar chart)
grouped_headphones = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'])['Did you use noise cancelling headphones?'].agg(lambda x: 'Headphones' if 'Yes' in x.values else 'No_headphones')
# Reset index for visualization
grouped_headphones = grouped_headphones.reset_index()
# Group by participant ID and determine if they wore noise cancelling headphones at least once (for pie chart)
unique_headphones = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Did you use noise cancelling headphones?'].agg(lambda x: 'Headphones' if 'Yes' in x.values else 'No_headphones')


# Irritation
# Group by participant ID and Filter, and check for irritation (for bar chart)
grouped_irritation = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'])['Were you irritated by other participants?'].agg(lambda x: 'Irritation' if 'Yes' in x.values else 'No_irritation')
# Reset index for visualization
grouped_irritation = grouped_irritation.reset_index()
# Group by participant ID and determine if they were irritated at least once (for pie chart)
unique_irritation = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Were you irritated by other participants?'].agg(lambda x: 'Irritation' if 'Yes' in x.values else 'No_irritation')


# Sleep
# Group by participant ID and determine if they slept at least once (for pie chart)
unique_sleep = data.groupby('Please enter your participant number (this can be seen on your boarding pass):')['Did you sleep? If yes, for how long? (Please answer in hours)'].agg(lambda x: 'Sleep' if 'Yes' in x.values else 'No_sleep')
# Replace missing or empty sleep values with 0 (indicating no sleep)
data['SleepMinutes'] = data['Did you sleep? If yes, for how long? (Please answer in hours) - Yes'].fillna(0)
# Convert sleep duration from minutes to hours
data['SleepHours'] = data['SleepMinutes'] / 60
# Group by participant and filter, and calculate the average sleep duration
average_sleep = data.groupby(['Please enter your participant number (this can be seen on your boarding pass):', 'Filter'], as_index=False)['SleepHours'].mean()



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
custom_palette = ["#77AADD", "#99DDFF", "#44BB99", "#BBCC33"]

# Apply the custom color palette
sns.set_palette(custom_palette)


#########################################################################################################################

# Pie chart of medication


# Count the number of participants in each group
group_counts = unique_medication.value_counts()

# Pie chart labels and sizes
labels = ['No medication', 'Medication']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=90)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Medication Usage of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of medication


# Create data for the bar chart
bar_chart_distribution = grouped_medication[grouped_medication['Did you take any medication during the flight?'] == 'Medication'].groupby('Filter').size().reset_index(name='Count')

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='Filter', y='Count', data=bar_chart_distribution, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Frequency of Medication Usage Among Participants Who Used', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Show the plot
plt.show()


#########################################################################################################################

# Pie chart of eye drops


# Count the number of participants in each group
group_counts = unique_eyedrops.value_counts()

# Pie chart labels and sizes
labels = ['No eye drops', 'Eye drops']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=60)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Eye Drops Usage of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of eye drops


# Create data for the bar chart
bar_chart_distribution = grouped_eyedrops[grouped_eyedrops['Did you use eye drops?'] == 'Eyedrops'].groupby('Filter').size().reset_index(name='Count')

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='Filter', y='Count', data=bar_chart_distribution, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Frequency of Eye Drops Usage Among Participants Who Used', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Show the plot
plt.show()


#########################################################################################################################

# Pie chart of hand cream


# Count the number of participants in each group
group_counts = unique_handcream.value_counts()

# Pie chart labels and sizes
labels = ['No hand cream', 'Hand cream']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=60)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Hand Cream Usage of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of hand cream


# Create data for the bar chart
bar_chart_distribution = grouped_handcream[grouped_handcream['Did you use hand lotion?'] == 'Handcream'].groupby('Filter').size().reset_index(name='Count')

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='Filter', y='Count', data=bar_chart_distribution, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Frequency of Hand Cream Usage Among Participants Who Used', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Show the plot
plt.show()


#########################################################################################################################

# Pie chart of contact lenses


# Count the number of participants in each group
group_counts = unique_contacts.value_counts()

# Pie chart labels and sizes
labels = ['No contact lenses', 'Contact lenses']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=70)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Contact Lens Usage of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of contact lenses


# Create data for the bar chart
bar_chart_distribution = grouped_contacts[grouped_contacts['Did you wear contact lenses?'] == 'Contactlenses'].groupby('Filter').size().reset_index(name='Count')

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='Filter', y='Count', data=bar_chart_distribution, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Frequency of Contact Lens Usage Among Participants Who Used', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Show the plot
plt.show()


#########################################################################################################################

# Pie chart of noise cancelling headphones


# Count the number of participants in each group
group_counts = unique_headphones.value_counts()

# Pie chart labels and sizes
labels = ['No headphones', 'Headphones']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=120)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Noise Cancelling Headphones Usage of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of noise cancelling headphones


# Create data for the bar chart
bar_chart_distribution = grouped_headphones[grouped_headphones['Did you use noise cancelling headphones?'] == 'Headphones'].groupby('Filter').size().reset_index(name='Count')

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='Filter', y='Count', data=bar_chart_distribution, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Frequency of NC Headphones Usage Among Participants Who Used', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Show the plot
plt.show()


#########################################################################################################################

# Pie chart of irritation


# Count the number of participants in each group
group_counts = unique_irritation.value_counts()

# Pie chart labels and sizes
labels = ['No irritation', 'Irritation']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=110)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Irritation of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of irritation


# Create data for the bar chart
bar_chart_distribution = grouped_irritation[grouped_irritation['Were you irritated by other participants?'] == 'Irritation'].groupby('Filter').size().reset_index(name='Count')

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='Filter', y='Count', data=bar_chart_distribution, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Frequency of Irritation Among Participants Who Were', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Show the plot
plt.show()


#########################################################################################################################

# Pie chart of sleep


# Count the number of participants in each group
group_counts = unique_sleep.value_counts()

# Pie chart labels and sizes
labels = ['Sleep', 'No sleep']
sizes = group_counts
colors = ["#AACCEE", "#CCDDAA"]
explode = [0.002, 0.002]

# Create the pie chart
plt.figure(figsize=(10, 7))
wedges, texts, autotexts = plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct=make_autopct(sizes), shadow=False, startangle=100)

# Customize font size for the labels and percentages
for text in texts:
    text.set_fontsize(18)

for autotext in autotexts:
    autotext.set_fontsize(16)

plt.title('Sleep Patterns of Participants', fontsize=20)
plt.axis('equal')  # Equal aspect ratio to ensure the pie is circular

# Show the chart
plt.show()


#########################################################################################################################

# Bar graph of sleep


# Define sleep bins and their corresponding labels
bins = [-np.inf, 0, 1, 2, 3, 4, np.inf]  # Edges of the bins, including -inf for no sleep
labels = ['0 hours', '0$–$1 hours', '1$–$2 hours', '2$–$3 hours', '3$–$4 hours', '4+ hours']

# Add a new column for the sleep bins
data['SleepBin'] = pd.cut(data['SleepHours'], bins=bins, labels=labels, right=True)

# Create a list of filters to iterate through
filters = ['HEPA 7', 'HEPA 5', 'APS N', 'APS U']

# Create a DataFrame to store counts for each filter and sleep bin
summary = pd.DataFrame(0, index=labels, columns=filters)

# Count the number of participants for each filter and sleep bin
for f in filters:
    filter_data = data[data['Filter'] == f]
    bin_counts = filter_data.groupby('SleepBin')['Please enter your participant number (this can be seen on your boarding pass):'].nunique()
    summary[f] = bin_counts.reindex(labels, fill_value=0)

# Reshape the data for Seaborn (long-form DataFrame)
summary = summary.reset_index().melt(id_vars='index', var_name='Filter', value_name='Count')
summary.rename(columns={'index': 'SleepBin'}, inplace=True)

# Create the bar plot
plt.figure(figsize=(10, 7))
plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.barplot(x='SleepBin', y='Count', data=summary, hue='Filter', palette=custom_palette, zorder=3, edgecolor='black')

# Customize the chart
plt.title('Distribution of Sleep Hours Across Participants Who Slept', fontsize=20, zorder=4)
plt.xlabel('Sleep Duration [Hours]', fontsize=18, zorder=4)
plt.ylabel('Number of Participants', fontsize=18, zorder=4)
plt.legend(title='Condition', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set ticks
plt.xticks(fontsize=16, zorder=4)
# Get the range of y-ticks
sleep_counts = summary['Count']  # Get the maximum count to scale y-ticks
tick_positions = range(0, sleep_counts.max() + 1, 1)  # Whole numbers for ticks
# Set ticks: Show only every second tick label (i.e., 0, 2, 4, ...)
tick_labels = [str(i) if i % 2 == 0 else '' for i in tick_positions]
# Apply custom ticks and labels
plt.yticks(tick_positions, tick_labels, fontsize=14, zorder=4)
# Disable minor ticks
plt.minorticks_off()

# Adjust layout
plt.tight_layout()

# Show the plot
plt.show()


#########################################################################################################################

# Boxplot of sleep


# Create the boxplot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.boxplot(x='Filter', y='SleepHours', data=average_sleep, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, zorder=3)

# Add titles and labels
plt.title('Boxplot of Sleep Duration', fontsize=20, zorder=4)
plt.xlabel('Condition', fontsize=18, zorder=4)
plt.ylabel('Sleep Duration [Hours]', fontsize=18, zorder=4)

# Set tick font sizes
plt.xticks(fontsize=16, zorder=4)
y_ticks = np.arange(0, average_sleep['SleepHours'].max() + 0.5, 0.5)
plt.yticks(y_ticks, fontsize=16, zorder=4)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()


# Calculate the median sleep duration for each filter
median_sleep = data.groupby('Filter')['SleepHours'].median()
# Display the medians
print("Median Sleep Duration (hours) for Each Filter:")
print(median_sleep)
