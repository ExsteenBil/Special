import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
import scienceplots
import matplotlib.lines as mlines

Title = 'APS N'

A=['2024-09-03', '2024-09-13', '2024-09-19', '2024-09-25']
B=['2024-09-04', '2024-09-10', '2024-09-20', '2024-09-26']
C=['2024-09-05', '2024-09-11', '2024-09-17', '2024-09-27']
D=['2024-09-06', '2024-09-12', '2024-09-18', '2024-09-24']

# Date specifications
specified_dates = D
start_time = '08:30:00'
end_time = '20:30:00'

# Define fixed colors for devices
device_colors = {
    'Atmocubes': '#332288',
    'HOBO Left': '#44AA99',
    'HOBO Right': '#117733',
    'GrayWolf': '#999933',
    'Ctrl Comp': '#882255',
    'Innova': '#AA4499'
}

# Define line styles for dates
line_styles = ['-', '--', '-.', ':']

# Initialize Tkinter root for folder selection (hidden window)
root = tk.Tk()
root.withdraw()

# Select folders for Tail and HOBO data, and specific GrayWolf CSV file
tail_folder_path = filedialog.askdirectory(title="Select Folder Containing Tail CSV Files")
HOBO_folder_path = filedialog.askdirectory(title="Select Folder Containing HOBO CSV Files")
specific_file_path = filedialog.askopenfilename(title="Select GrayWolf Data CSV File", filetypes=[("CSV Files", "*.csv")])
compu_file_path = filedialog.askopenfilename(title="Select Computer Data CSV File", filetypes=[("CSV Files", "*.csv")])
invo_file_path = filedialog.askopenfilename(title="Select Innova Data CSV File", filetypes=[("CSV Files", "*.csv")])

if not (tail_folder_path and HOBO_folder_path and specific_file_path):
    print("Folder selection incomplete. Please select all required folders and files.")
    exit()

# Load Computer data
compu_df = pd.read_csv(compu_file_path, delimiter=';', decimal=".")
compu_df['dtm'] = pd.to_datetime(compu_df['Date-Time'], dayfirst=True, format='%d-%m-%Y %H:%M:%S')

# Load Innova data
invo_df = pd.read_csv(invo_file_path, delimiter=';', decimal=".")
invo_df['dtm'] = pd.to_datetime(invo_df['Date-Time'], dayfirst=True, format='%d-%m-%Y %H:%M:%S')

# Load GrayWolf data
graywolf_df = pd.read_csv(specific_file_path, delimiter=';')
graywolf_df['dtm'] = pd.to_datetime(graywolf_df['Date Time'], dayfirst=True, format='%d-%m-%Y %H:%M')

# Adjust the temperatures to replace values over 100 with the last valid temperature
def replace_invalid_temperatures(series):
    last_valid_temp = None
    corrected_temps = []
    for temp in series:
        if temp <= 100:
            last_valid_temp = temp
            corrected_temps.append(temp)
        else:
            corrected_temps.append(last_valid_temp if last_valid_temp is not None else np.nan)
    return pd.Series(corrected_temps)

graywolf_df['Temperature °C'] = replace_invalid_temperatures(graywolf_df['Temperature °C'])

# Load and process Tail data
tail_data = {}
for file in os.listdir(tail_folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(tail_folder_path, file)
        tail = file.split('TAIL-')[-1][:2]
        df = pd.read_csv(file_path)
        df['dtm'] = pd.to_datetime(df['dtm'].str.replace('+02:00', ''), format='%d-%b-%Y %H:%M:%S', errors='coerce')
        tail_data[f'Tail-{tail}'] = df

# Load and process HOBO data based on column positions for temperature and CO2
HOBO_data = {}
for file in os.listdir(HOBO_folder_path):
    if file.endswith('.csv'):
        file_path = os.path.join(HOBO_folder_path, file)
        HOBO_df = pd.read_csv(file_path)
        HOBO_df['dtm'] = pd.to_datetime(HOBO_df.iloc[:, 1], format='%m/%d/%y %I:%M:%S %p')
        HOBO_df = HOBO_df.rename(columns={
            HOBO_df.columns[2]: 'Temperature °C',
            HOBO_df.columns[3]: 'CO2 ppm'
        })
        # Label as "HOBO Left" or "HOBO Right" based on filename
        first_word = file.split('_')[0]
        label = f"HOBO {first_word}" if first_word in ["Left", "Right"] else "HOBO Data"
        HOBO_data[label] = HOBO_df

# Prepare DataFrames for each date for Tail, GrayWolf, and HOBO data
compu_per_day = {}
invo_per_day = {}
graywolf_per_day = {}
average_tails_per_day = {}
HOBO_per_day = {}

for date in specified_dates:
    start_timestamp = pd.Timestamp(f'{date} {start_time}')
    end_timestamp = pd.Timestamp(f'{date} {end_time}')
    
    # Computer data filtering
    compu_day_df = compu_df[(compu_df['dtm'] >= start_timestamp) & (compu_df['dtm'] <= end_timestamp)]
    compu_day_df = compu_day_df[['dtm', 'Cabin-Temp', 'Cabin-RH']]
    compu_day_df.loc[:, 'Seconds Since Midnight'] = (compu_day_df['dtm'].dt.hour * 3600 + compu_day_df['dtm'].dt.minute * 60 + compu_day_df['dtm'].dt.second)
    compu_per_day[date] = compu_day_df[['Seconds Since Midnight', 'Cabin-Temp', 'Cabin-RH']]

    # Innova data filtering
    invo_day_df = invo_df[(invo_df['dtm'] >= start_timestamp) & (invo_df['dtm'] <= end_timestamp)]
    invo_day_df = invo_day_df[['dtm', 'Cabin-CO2']]
    invo_day_df.loc[:, 'Seconds Since Midnight'] = (invo_day_df['dtm'].dt.hour * 3600 + invo_day_df['dtm'].dt.minute * 60 + invo_day_df['dtm'].dt.second)
    invo_per_day[date] = invo_day_df[['Seconds Since Midnight', 'Cabin-CO2']]

    # GrayWolf data filtering
    graywolf_day_df = graywolf_df[(graywolf_df['dtm'] >= start_timestamp) & (graywolf_df['dtm'] <= end_timestamp)]
    graywolf_day_df = graywolf_day_df[['dtm', 'Temperature °C', 'Carbon Dioxide ppm', 'TVOC ppb', 'PM 10.0 µg/m3', 'PM 25 µg/m3', 'Formaldehyde ppb']]
    graywolf_day_df['Seconds Since Midnight'] = graywolf_day_df['dtm'].dt.hour * 3600 + graywolf_day_df['dtm'].dt.minute * 60 + graywolf_day_df['dtm'].dt.second
    graywolf_per_day[date] = graywolf_day_df[['Seconds Since Midnight', 'Temperature °C', 'Carbon Dioxide ppm', 'TVOC ppb', 'PM 10.0 µg/m3', 'PM 25 µg/m3', 'Formaldehyde ppb']]
    
    # Tail data filtering and averaging
    selected_tails = [tail_data[tail][(tail_data[tail]['dtm'] >= start_timestamp) & (tail_data[tail]['dtm'] <= end_timestamp)] for tail in ['Tail-16', 'Tail-17', 'Tail-18', 'Tail-19']]
    averages_day = pd.concat(selected_tails).groupby('dtm').mean()
    averages_day = averages_day[['temperature, °C', 'co2, ppm', 'humidity, %', 'voc, ppm', 'pm10, μg/m³', 'pm25, μg/m³', 'light, lux', 'noise, db']]
    # Convert VOC from ppm to ppb
    averages_day['voc, ppb'] = averages_day['voc, ppm'] * 1000
    averages_day['Seconds Since Midnight'] = averages_day.index.hour * 3600 + averages_day.index.minute * 60 + averages_day.index.second
    average_tails_per_day[date] = averages_day[['Seconds Since Midnight', 'temperature, °C', 'co2, ppm', 'humidity, %', 'voc, ppb', 'pm10, μg/m³', 'pm25, μg/m³', 'light, lux', 'noise, db']]
    
    # HOBO data filtering (each file is plotted separately)
    HOBO_day_dfs = []
    for HOBO_label, HOBO_df in HOBO_data.items():
        HOBO_day_df = HOBO_df[(HOBO_df['dtm'] >= start_timestamp) & (HOBO_df['dtm'] <= end_timestamp)]
        HOBO_day_df['Seconds Since Midnight'] = HOBO_day_df['dtm'].dt.hour * 3600 + HOBO_day_df['dtm'].dt.minute * 60 + HOBO_day_df['dtm'].dt.second
        HOBO_day_dfs.append((HOBO_day_df[['Seconds Since Midnight', 'Temperature °C', 'CO2 ppm']], HOBO_label))
    HOBO_per_day[date] = HOBO_day_dfs

plt.style.use(['science', 'no-latex'])

# Plot Temperature Data
plt.figure(figsize=(10, 7))

# Ordered list of devices as they appear in the script
device_order = ['Atmocubes', 'HOBO Left', 'HOBO Right', 'GrayWolf', 'Ctrl Comp']

# Initialize sets to track plotted devices and dates
plotted_devices = set()
date_handles = []

# Loop through dates to plot data
for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]

    # Atmo Cube
    if 'temperature, °C' in average_tails_per_day[date]:
        plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], 
                 average_tails_per_day[date]['temperature, °C'], 
                 style, color=device_colors['Atmocubes'], label=f'{date} Atmocubes')
        plotted_devices.add('Atmocubes')  # Track Atmo Cube

    # GrayWolf
    if 'Temperature °C' in graywolf_per_day[date]:
        plt.plot(graywolf_per_day[date]['Seconds Since Midnight'], 
                 graywolf_per_day[date]['Temperature °C'], 
                 style, color=device_colors['GrayWolf'], label=f'{date} GrayWolf')
        plotted_devices.add('GrayWolf')  # Track GrayWolf

    # Computer
    if 'Cabin-Temp' in compu_per_day[date]:
        plt.plot(compu_per_day[date]['Seconds Since Midnight'], 
                 compu_per_day[date]['Cabin-Temp'], 
                 style, color=device_colors['Ctrl Comp'], label=f'{date} Ctrl Comp')
        plotted_devices.add('Ctrl Comp')  # Track Computer

    # HOBO data
    for HOBO_df, HOBO_label in HOBO_per_day[date]:
        if 'Temperature °C' in HOBO_df:
            plt.plot(HOBO_df['Seconds Since Midnight'], 
                     HOBO_df['Temperature °C'], 
                     style, color=device_colors[HOBO_label], label=f'{date} {HOBO_label}')
            plotted_devices.add(HOBO_label)  # Track HOBO devices

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

# Configure labels, legends, and appearance
plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Temperature [$\degree$C]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - Temperature', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set x-ticks and y-ticks
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

# Add grid and adjust layout
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Set y-axis limits for temperature
ax = plt.gca()
ax.set_ylim(22, 27)  # Adjust based on temperature range

plt.tight_layout(pad=2)
plt.show()



# Initialize figure
plt.figure(figsize=(10, 7))

# Ordered list of devices as they appear in the script
device_order = ['Atmocubes', 'GrayWolf', 'Innova']

# Initialize sets to track plotted devices and dates
plotted_devices = set()  
date_handles = []

# Loop through dates to plot data
for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]

    # Atmo Cube
    if 'co2, ppm' in average_tails_per_day[date]:
        plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], 
                 average_tails_per_day[date]['co2, ppm'], 
                 style, color=device_colors['Atmocubes'], label=f'{date} Atmocubes')
        plotted_devices.add('Atmocubes')  # Track Atmo Cube

    # GrayWolf
    if 'Carbon Dioxide ppm' in graywolf_per_day[date]:
        plt.plot(graywolf_per_day[date]['Seconds Since Midnight'], 
                 graywolf_per_day[date]['Carbon Dioxide ppm'], 
                 style, color=device_colors['GrayWolf'], label=f'{date} GrayWolf')
        plotted_devices.add('GrayWolf')  # Track GrayWolf

    # Innova
    if 'Cabin-CO2' in invo_per_day[date]:
        plt.plot(invo_per_day[date]['Seconds Since Midnight'], 
                 invo_per_day[date]['Cabin-CO2'], 
                 style, color=device_colors['Innova'], label=f'{date} Innova')
        plotted_devices.add('Innova')  # Track Innova

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

# Configure labels, legends, and appearance
plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('CO$_2$ [ppm]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - CO$_2$', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set x-ticks and y-ticks
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

# Add grid and adjust layout
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Set y-axis limits for CO2
ax = plt.gca()
ax.set_ylim(0, 3100)  # Adjust based on CO2 range

plt.tight_layout()
plt.show()




plt.figure(figsize=(10, 7))
# Ordered list of devices as they appear in the script
device_order = ['Atmocubes', 'Ctrl Comp']

plotted_devices = set()  # To track devices that are actually plotted
date_handles = []

for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]
    # Atmo Cube
    if 'humidity, %' in average_tails_per_day[date]:
        plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], 
                 average_tails_per_day[date]['humidity, %'], 
                 style, color=device_colors['Atmocubes'], label=f'{date} Atmocubes')
        plotted_devices.add('Atmocubes')  # Track the plotted device

    # Computer
    if 'Cabin-RH' in compu_per_day[date]:
        plt.plot(compu_per_day[date]['Seconds Since Midnight'], 
                 compu_per_day[date]['Cabin-RH'], 
                 style, color=device_colors['Ctrl Comp'], label=f'{date} Ctrl Comp')
        plotted_devices.add('Ctrl Comp')  # Track the plotted device

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Add device handles dynamically
#device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
 #                 for device in plotted_devices]

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Relative Humidity [%]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - Relative Humidity', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

ax = plt.gca()
ax.set_ylim(0, 35)

plt.tight_layout()
plt.show()




# Initialize figure
plt.figure(figsize=(10, 7))

# Ordered list of devices as they appear in the script
device_order = ['Atmocubes', 'GrayWolf']

# Initialize sets to track plotted devices and dates
plotted_devices = set()  
date_handles = []

# Loop through dates to plot data
for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]

    # Atmo Cube
    if 'pm10, μg/m³' in average_tails_per_day[date]:
        plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], 
                 average_tails_per_day[date]['pm10, μg/m³'], 
                 style, color=device_colors['Atmocubes'], label=f'{date} Atmocubes')
        plotted_devices.add('Atmocubes')  # Track Atmo Cube

    # GrayWolf
    if 'PM 10.0 µg/m3' in graywolf_per_day[date]:
        plt.plot(graywolf_per_day[date]['Seconds Since Midnight'], 
                 graywolf_per_day[date]['PM 10.0 µg/m3'], 
                 style, color=device_colors['GrayWolf'], label=f'{date} GrayWolf')
        plotted_devices.add('GrayWolf')  # Track GrayWolf

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

# Configure labels, legends, and appearance
plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('PM$_{10}$ [ppm]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - PM$_{10}$', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set x-ticks and y-ticks
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

# Add grid and adjust layout
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Set y-axis limits for PM10
ax = plt.gca()
ax.set_ylim(0, 100)  # Adjust based on PM10 range

plt.tight_layout()
plt.show()







# Initialize figure
plt.figure(figsize=(10, 7))

# Ordered list of devices as they appear in the script
device_order = ['Atmocubes', 'GrayWolf']

# Initialize sets to track plotted devices and dates
plotted_devices = set()  
date_handles = []

# Loop through dates to plot data
for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]

    # Atmo Cube
    if 'pm25, μg/m³' in average_tails_per_day[date]:
        plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], 
                 average_tails_per_day[date]['pm25, μg/m³'], 
                 style, color=device_colors['Atmocubes'], label=f'{date} Atmocubes')
        plotted_devices.add('Atmocubes')  # Track Atmo Cube

    # GrayWolf
    if 'PM 25 µg/m3' in graywolf_per_day[date]:
        plt.plot(graywolf_per_day[date]['Seconds Since Midnight'], 
                 graywolf_per_day[date]['PM 25 µg/m3'], 
                 style, color=device_colors['GrayWolf'], label=f'{date} GrayWolf')
        plotted_devices.add('GrayWolf')  # Track GrayWolf

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

# Configure labels, legends, and appearance
plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('PM$_{2.5}$ [ppm]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - PM$_{2.5}$', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set x-ticks and y-ticks
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

# Add grid and adjust layout
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Set y-axis limits for PM2.5
ax = plt.gca()
ax.set_ylim(0, 100)  # Adjust based on PM2.5 range

plt.tight_layout()
plt.show()




# Initialize figure
plt.figure(figsize=(10, 7))

# Ordered list of devices as they appear in the script
device_order = ['Atmocubes', 'GrayWolf']

# Initialize sets to track plotted devices and dates
plotted_devices = set()  
date_handles = []

# Loop through dates to plot data
for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]

    # Atmo Cube
    if 'voc, ppb' in average_tails_per_day[date]:
        plt.plot(average_tails_per_day[date]['Seconds Since Midnight'], 
                 average_tails_per_day[date]['voc, ppb'], 
                 style, color=device_colors['Atmocubes'], label=f'{date} Atmocubes')
        plotted_devices.add('Atmocubes')  # Track Atmo Cube

    # GrayWolf
    if 'TVOC ppb' in graywolf_per_day[date]:
        plt.plot(graywolf_per_day[date]['Seconds Since Midnight'], 
                 graywolf_per_day[date]['TVOC ppb'], 
                 style, color=device_colors['GrayWolf'], label=f'{date} GrayWolf')
        plotted_devices.add('GrayWolf')  # Track GrayWolf

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

# Configure labels, legends, and appearance
plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('VOC [ppb]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - VOC', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set x-ticks and y-ticks
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

# Add grid and adjust layout
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Set y-axis limits for PM2.5
ax = plt.gca()
ax.set_ylim(0, 2000)  # Adjust based on PM2.5 range

plt.tight_layout()
plt.show()




# Initialize figure
plt.figure(figsize=(10, 7))

# Ordered list of devices as they appear in the script
device_order = ['GrayWolf']

# Initialize sets to track plotted devices and dates
plotted_devices = set()  
date_handles = []

# Loop through dates to plot data
for i, date in enumerate(specified_dates):
    style = line_styles[i % len(line_styles)]

    # GrayWolf
    if 'Formaldehyde ppb' in graywolf_per_day[date]:
        plt.plot(graywolf_per_day[date]['Seconds Since Midnight'], 
                 graywolf_per_day[date]['Formaldehyde ppb'], 
                 style, color=device_colors['GrayWolf'], label=f'{date} GrayWolf')
        plotted_devices.add('GrayWolf')  # Track GrayWolf

    # Add handles for the date legend
    date_handles.append(mlines.Line2D([], [], color='black', linestyle=style, label=date))

# Create device handles based on order and plotted devices
device_handles = [mlines.Line2D([], [], color=device_colors[device], linestyle='-', label=device)
                  for device in device_order if device in plotted_devices]

# Configure labels, legends, and appearance
plt.xlabel('Time of Day [HH:MM]', fontsize=18)
plt.ylabel('Formaldehyde [ppb]', fontsize=18)
plt.title(f'{Title} - Comparison of Dates - Formaldehyde', fontsize=20)

# Add legends
device_legend = plt.legend(handles=device_handles, title="Device", loc='lower left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
plt.gca().add_artist(device_legend)  # Ensure the first legend doesn't overwrite
plt.legend(handles=date_handles, title="Dates", loc='upper left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

# Set x-ticks and y-ticks
plt.xticks(ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000], 
           labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'], 
           fontsize=16)
plt.yticks(fontsize=16)

# Add grid and adjust layout
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Set y-axis limits for PM2.5
ax = plt.gca()
ax.set_ylim(0, 1)  # Adjust based on PM2.5 range

plt.tight_layout()
plt.show()