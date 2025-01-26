import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.lines import Line2D  # For custom legend
import scienceplots
import seaborn as sns

Title = 'Comparison of dates/Conditions - Atmocube'

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

# Initialize Tkinter root for folder selection (hidden window)
root = tk.Tk()
root.withdraw()

# Select folders for Tail and HOBO data, and specific GrayWolf CSV file
tail_folder_path = filedialog.askdirectory(title="Select Folder Containing Tail CSV Files")

# Load and process Tail data
tail_data = {}
for file in os.listdir(tail_folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(tail_folder_path, file)
        tail = file.split('TAIL-')[-1][:2]
        df = pd.read_csv(file_path)
        df['dtm'] = pd.to_datetime(df['dtm'].str.replace('+02:00', ''), format='%d-%b-%Y %H:%M:%S', errors='coerce')
        tail_data[f'Tail-{tail}'] = df

average_tails_per_day = {}

for date in all_dates:
    start_timestamp = pd.Timestamp(f'{date} {start_time}')
    end_timestamp = pd.Timestamp(f'{date} {end_time}')
    
    # Tail data filtering and averaging
    selected_tails = [tail_data[tail][(tail_data[tail]['dtm'] >= start_timestamp) & (tail_data[tail]['dtm'] <= end_timestamp)] for tail in ['Tail-16', 'Tail-17', 'Tail-18', 'Tail-19']]
    #selected_tails = [tail_data[tail][(tail_data[tail]['dtm'] >= start_timestamp) & (tail_data[tail]['dtm'] <= end_timestamp)] for tail in ['Tail-18', 'Tail-19']]
    averages_day = pd.concat(selected_tails).groupby('dtm').mean()
    averages_day = averages_day[['temperature, °C', 'co2, ppm', 'humidity, %', 'voc, ppm', 'pm10, μg/m³', 'pm25, μg/m³', 'light, lux', 'noise, db']]
    # Convert VOC from ppm to ppb
    averages_day['voc, ppb'] = averages_day['voc, ppm'] * 1000
    averages_day['Seconds Since Midnight'] = averages_day.index.hour * 3600 + averages_day.index.minute * 60 + averages_day.index.second
    average_tails_per_day[date] = averages_day[['Seconds Since Midnight', 'temperature, °C', 'co2, ppm', 'humidity, %', 'voc, ppb', 'pm10, μg/m³', 'pm25, μg/m³', 'light, lux', 'noise, db']]

plt.style.use(['science', 'no-latex'])

# Plot Temperature data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['temperature, °C'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Temperature [$\degree$C]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - Temperature', fontsize=20)
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

# Plot CO2 data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['co2, ppm'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('CO$_2$ [ppm]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - CO$_2$', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(0, 3000)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()

# Plot RH data (only Tail averages for RH)
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['humidity, %'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Relative Humidity [%]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - Relative Humidity', fontsize=20)
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

# Plot VOC data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['voc, ppb'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('VOC [ppb]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - VOC', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(0, 1750)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()


# Plot PM10 data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['pm10, μg/m³'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('PM$_{10}$ [$\mu$g/m$^3$]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - PM$_{1}$$_0$', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(0, 2.5)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()


# Plot PM1 data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['pm25, μg/m³'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('PM$_{2.5}$ [$\mu$g/m$^3$]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - PM$_{2}$$_.$$_5$', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(0, 2.5)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()



# Plot Light data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['light, lux'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Light [LUX]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - Light', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
ax.set_ylim(0, 110)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()



# Plot Noise data
plt.figure(figsize=(10, 7))
for date in all_dates:
    color = color_map[date]
    plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], average_tails_per_day[date]['noise, db'], '--', color=color, label=f'{date} Tail Average')

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Noise [dB]', fontsize=18)
plt.title(f'Comparison of Dates - Atmocubes - Noise', fontsize=20)
plt.legend(handles=custom_legend, title="Conditions", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax = plt.gca()
#ax.set_ylim(0, 2.5)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)  # Add gridlines
plt.tight_layout()
plt.show()


# Custom color palette
custom_palette = {
    'HEPA 7': '#77AADD',
    'HEPA 5': '#99DDFF',
    'APS N': '#44BB99',
    'APS U': '#BBCC33',
}

# Step 1: Map filter types to each date
filter_map = {
    **{date: 'HEPA 7' for date in A},
    **{date: 'HEPA 5' for date in C},
    **{date: 'APS N' for date in D},
    **{date: 'APS U' for date in B},
}

# Step 2: Add filtertype column to each DataFrame
for date, df in average_tails_per_day.items():
    df['filtertype'] = filter_map[date]

# Step 3: Combine all DataFrames for boxplot
combined_df = pd.concat(average_tails_per_day.values())

# Activate the 'science' style
plt.style.use(['science', 'no-latex'])

# Boxplot for VOC
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
    x='filtertype', y='voc, ppb', data=combined_df,
    order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'],
    palette=custom_palette  # Explicit palette for this plot
)
plt.title('Comparison of Conditions - Atmocubes - VOC', fontsize=20)
plt.xlabel('Conditions', fontsize=18)
plt.ylabel('VOC [ppb]', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax.set_ylim(0, 1750)

plt.tight_layout()
plt.show()


# Boxplot for PM10
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
    x='filtertype', y='pm10, μg/m³', data=combined_df,
    order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'],
    palette=custom_palette  # Explicit palette for this plot
)
plt.title('Comparison of Conditions - Atmocubes - PM$_{1}$$_0$', fontsize=20)
plt.xlabel('Conditions', fontsize=18)
plt.ylabel('PM$_{10}$ [$\mu$g/m$^3$]', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax.set_ylim(0, 2.5)

plt.tight_layout()
plt.show()


# Boxplot for PM1
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
    x='filtertype', y='pm25, μg/m³', data=combined_df,
    order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'],
    palette=custom_palette  # Explicit palette for this plot
)
plt.title('Comparison of Conditions - Atmocubes - PM$_{2}$$_.$$_5$', fontsize=20)
plt.xlabel('Conditions', fontsize=18)
plt.ylabel('PM$_{2.5}$ [$\mu$g/m$^3$]', fontsize=18)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

ax.set_ylim(0, 2.5)

plt.tight_layout()
plt.show()