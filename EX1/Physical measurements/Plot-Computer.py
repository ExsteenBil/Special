import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.lines import Line2D
import seaborn as sns
import scienceplots

# Date groups for color coding
A = ['2024-09-03', '2024-09-13', '2024-09-19', '2024-09-25']
B = ['2024-09-04', '2024-09-10', '2024-09-20', '2024-09-26']
C = ['2024-09-05', '2024-09-11', '2024-09-17', '2024-09-27']
D = ['2024-09-06', '2024-09-12', '2024-09-18', '2024-09-24']

all_dates = A + B + C + D
# Custom color map with hex values
color_map = {**{date: '#77AADD' for date in A},   # HEPA 7
             **{date: '#99DDFF' for date in C},   # HEPA 5
             **{date: '#44BB99' for date in D},   # APS N
             **{date: '#BBCC33' for date in B}}   # APS U

# Custom legend for filter types with matching hex colors
custom_legend = [
    Line2D([0], [0], color='#77AADD', lw=2, linestyle='--', label='HEPA 7'),
    Line2D([0], [0], color='#99DDFF', lw=2, linestyle='--', label='HEPA 5'),
    Line2D([0], [0], color='#44BB99', lw=2, linestyle='--', label='APS N'),
    Line2D([0], [0], color='#BBCC33', lw=2, linestyle='--', label='APS U')
]

start_time = '08:30:00'
end_time = '20:30:00'

# Initialize Tkinter root for file selection
root = tk.Tk()
root.withdraw()

# Select the computer data file
compu_file_path = filedialog.askopenfilename(title="Select Computer Data CSV File", filetypes=[("CSV Files", "*.csv")])

if not compu_file_path:
    print("File selection incomplete.")
    exit()

# Load Computer data
compu_df = pd.read_csv(compu_file_path, delimiter=';', decimal=".")
compu_df['dtm'] = pd.to_datetime(compu_df['Date-Time'], dayfirst=True, format='%d-%m-%Y %H:%M:%S')

# Filter and process Computer data for each date
compu_per_day = {}
for date in all_dates:
    start_timestamp = pd.Timestamp(f'{date} {start_time}')
    end_timestamp = pd.Timestamp(f'{date} {end_time}')
    
    # Filter computer data by date and time
    compu_day_df = compu_df[(compu_df['dtm'] >= start_timestamp) & (compu_df['dtm'] <= end_timestamp)]
    compu_day_df['Seconds Since Midnight'] = compu_day_df['dtm'].dt.hour * 3600 + compu_day_df['dtm'].dt.minute * 60 + compu_day_df['dtm'].dt.second
    compu_per_day[date] = compu_day_df[['Seconds Since Midnight', 'Cabin-Temp', 'Cabin-RH']]

plt.style.use(['science', 'no-latex'])

# Plot temperature data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(compu_per_day[date]['Seconds Since Midnight'], compu_per_day[date]['Cabin-Temp'], '--', color=color, label=f'{date} Computer Data')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Temperature [$\degree$C]', fontsize=18)
plt.title(f'Comparison of Dates - Control Computer - Temperature', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(22, 27)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()

# Plot RH data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(compu_per_day[date]['Seconds Since Midnight'], compu_per_day[date]['Cabin-RH'], '--', color=color, label=f'{date} Computer Data')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Relative Humidity [%]', fontsize=18)
plt.title(f'Comparison of Dates - Control Computer - Relative Humidity', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(0, 35)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()

#----------------------Boxplots----------------------

# Combine all daily data into a single DataFrame for boxplots
compu_all_data = pd.concat(
    [compu_per_day[date].assign(Date=date) for date in all_dates], ignore_index=True
)

# Map the 'Date' column to filters using your color_map logic
filter_map = {**{date: 'HEPA 7' for date in A},
              **{date: 'HEPA 5' for date in C},
              **{date: 'APS N' for date in D},
              **{date: 'APS U' for date in B}}
compu_all_data['Filter'] = compu_all_data['Date'].map(filter_map)

print(compu_all_data)

# Custom color palette
custom_palette = {
    'HEPA 7': '#77AADD',
    'HEPA 5': '#99DDFF',
    'APS N': '#44BB99',
    'APS U': '#BBCC33',
}

# Activate the 'science' style
plt.style.use(['science', 'no-latex'])

# Boxplot for Temperature
plt.figure(figsize=(10, 7))

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Turn off vertical gridlines
ax.xaxis.grid(False)
sns.boxplot(
    x='Filter', y='Cabin-Temp', data=compu_all_data,
    order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'],
    palette=custom_palette  # Explicit palette for this plot
)
plt.title('Comparison of Conditions - Control Computer - Temperature', fontsize=20)
plt.xlabel('Conditions', fontsize=18)
plt.ylabel('Temperature [$\degree$C]', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.show()


# Boxplot for Relative Humidity
plt.figure(figsize=(10, 7))

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Turn off vertical gridlines
ax.xaxis.grid(False)

sns.boxplot(
    x='Filter', y='Cabin-RH', data=compu_all_data,
    order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'],
    palette=custom_palette  # Explicit palette for this plot
)
plt.title('Comparison of Conditions - Control Computer - Relative Humidity', fontsize=20)
plt.xlabel('Conditions', fontsize=18)
plt.ylabel('Relative Humidity [%]', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.show()