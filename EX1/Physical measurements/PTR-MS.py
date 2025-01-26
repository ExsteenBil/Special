# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from matplotlib.lines import Line2D
import seaborn as sns
import scienceplots
import os
import re

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

# Initialize Tkinter root for file selection
root = tk.Tk()
root.withdraw()

# Select the PTR-MS data file
Data_file_path = filedialog.askopenfilename(title="Select PTR-MS Data CSV File", filetypes=[("CSV Files", "*.csv")])
if not Data_file_path:
    print("File selection incomplete.")
    exit()

# Select folder to save plots
Save_folder = filedialog.askdirectory(title="Select Folder to Save Plots")
if not Save_folder:
    print("Folder selection incomplete.")
    exit()

# Load PTR-MS data
Data_df = pd.read_csv(Data_file_path, delimiter=';', decimal=".")
Data_df['dtm'] = pd.to_datetime(Data_df['Date and Time (UTC)'], dayfirst=True, format='%Y-%m-%d %H:%M:%S')

# Add 1 hour to the dtm column
Data_df['dtm'] = Data_df['dtm'] + pd.Timedelta(hours=2)

# Define time ranges
time_plot_start = '08:30:00'
time_plot_end = '20:30:00'

night_plot_start = '00:00:00'
night_plot_end = '07:00:00'

boxplot_start = '10:00:00'
boxplot_end = '19:45:00'

updown_start = '10:00:00'
updown_end = '19:45:00'

# Create a mask for valid Valve_Position
valid_valve_position_mask = Data_df['Valve_Position'] == 'CabinOrOutdoor'

# Filter data to keep only Downstream and Upstream
Data_filtered = Data_df[Data_df['Valve_Position'].isin(['Downstream', 'Upstream'])]

# Add the mapping for filters based on the date
filter_map = {**{date: 'HEPA 7' for date in A},
              **{date: 'HEPA 5' for date in C},
              **{date: 'APS N' for date in D},
              **{date: 'APS U' for date in B}}

# Map the 'Date' column to filters using the filter_map
Data_filtered['Filter'] = Data_filtered['dtm'].dt.strftime('%Y-%m-%d').map(filter_map)

# Use the mask to mark invalid rows as NaN for plotting purposes
for col in Data_df.columns[3:36]:  # Assuming the relevant columns are 3 to 35
    Data_df.loc[~valid_valve_position_mask, col] = np.nan

# Filter and process PTR-MS data for each date
Data_per_day_time_plot = {}
Data_per_night_time_plot = {}
Data_per_day_boxplot = {}
Data_per_day_boxplot_updown = {}
for date in all_dates:
    # Time plot filtering
    time_plot_start_timestamp = pd.Timestamp(f'{date} {time_plot_start}')
    time_plot_end_timestamp = pd.Timestamp(f'{date} {time_plot_end}')
    Data_day_time_plot = Data_df[(Data_df['dtm'] >= time_plot_start_timestamp) & (Data_df['dtm'] <= time_plot_end_timestamp)]
    Data_day_time_plot.loc[:, 'Seconds Since Midnight'] = (
        Data_day_time_plot['dtm'].dt.hour * 3600 +
        Data_day_time_plot['dtm'].dt.minute * 60 +
        Data_day_time_plot['dtm'].dt.second
    )
    Data_per_day_time_plot[date] = Data_day_time_plot.copy()
    
    # Night plot filtering
    night_plot_start_timestamp = pd.Timestamp(f'{date} {night_plot_start}')
    night_plot_end_timestamp = pd.Timestamp(f'{date} {night_plot_end}')
    Data_night_time_plot = Data_df[(Data_df['dtm'] >= night_plot_start_timestamp) & (Data_df['dtm'] <= night_plot_end_timestamp)]
    Data_night_time_plot.loc[:, 'Seconds Since Midnight'] = (
        Data_night_time_plot['dtm'].dt.hour * 3600 +
        Data_night_time_plot['dtm'].dt.minute * 60 +
        Data_night_time_plot['dtm'].dt.second
    )
    Data_per_night_time_plot[date] = Data_night_time_plot.copy()

    # Boxplot filtering
    boxplot_start_timestamp = pd.Timestamp(f'{date} {boxplot_start}')
    boxplot_end_timestamp = pd.Timestamp(f'{date} {boxplot_end}')
    Data_day_boxplot = Data_df[(Data_df['dtm'] >= boxplot_start_timestamp) & (Data_df['dtm'] <= boxplot_end_timestamp)]
    Data_per_day_boxplot[date] = Data_day_boxplot.copy()

    # Boxplot Up and Downstream filtering
    boxplot_UpDown_start_timestamp = pd.Timestamp(f'{date} {updown_start}')
    boxplot_UpDown_end_timestamp = pd.Timestamp(f'{date} {updown_end}')
    Data_day_boxplot_updown = Data_filtered[(Data_filtered['dtm'] >= boxplot_UpDown_start_timestamp) & (Data_filtered['dtm'] <= boxplot_UpDown_end_timestamp)]
    Data_per_day_boxplot_updown[date] = Data_day_boxplot_updown.copy()

# Loop through each column (columns 3-35)
for col_idx in range(3, 36):
    column_name = Data_df.columns[col_idx]
    title_name = re.sub(r'[<>:"\\|?*()]', '', column_name.split(" - ")[0])
    y_label_name = re.sub(r'[<>:"\\|?*]', '', column_name)
    save_name_part = re.sub(r'[<>:"/\\|?*]', '', column_name.split(" - ")[0])
    row_number = col_idx - 2

# ---------------------- Time Plot ----------------------
    plt.style.use(['science', 'no-latex'])
    plt.figure(figsize=(10, 7))
    for date in all_dates:
        color = color_map[date]
        plt.scatter(Data_per_day_time_plot[date]['Seconds Since Midnight'], Data_per_day_time_plot[date][column_name], color=color, label=f'{date} PTR-MS Data', marker='o', s=1)
    
    plt.xlabel('Time of Day [HH:MM]', fontsize=18)
    plt.ylabel(f'{y_label_name} m/z [PPBV]', fontsize=18)
    plt.title(f'Comparison of Filters - Cabin or Outdoor Air - {title_name}', fontsize=20)
    plt.legend(handles=custom_legend, title="Filter", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
    plt.xticks(
        ticks=[32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000],
        labels=['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    ax = plt.gca()
    plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)
    plt.tight_layout()
    plt.savefig(os.path.join(Save_folder, f"{row_number}-1-Time-PTR-MS-{save_name_part}.png"))
    plt.close()

    # ---------------------- Night time Plot ----------------------
    plt.style.use(['science', 'no-latex'])
    plt.figure(figsize=(10, 7))
    for date in all_dates:
        color = color_map[date]
        plt.scatter(Data_per_night_time_plot[date]['Seconds Since Midnight'], Data_per_night_time_plot[date][column_name], color=color, label=f'{date} PTR-MS Data', marker='o', s=1)
    
    plt.xlabel('Time of Night [HH:MM]', fontsize=18)
    plt.ylabel(f'{y_label_name} m/z [PPBV]', fontsize=18)
    plt.title(f'Night Comparison of Filters - Cabin or Outdoor Air - {title_name}', fontsize=20)
    plt.legend(handles=custom_legend, title="Filter", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
    plt.xticks(
        ticks=[0, 3600, 7200, 10800, 14400, 18000, 21600, 25200],
        labels=['00:00', '01:00', '02:00', '03:00', '04:00', '05:00', '06:00', '07:00'])
    
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    ax = plt.gca()
    plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)
    plt.tight_layout()
    plt.savefig(os.path.join(Save_folder, f"{row_number}-2-Night-Time-PTR-MS-{save_name_part}.png"))
    plt.close()

    # ---------------------- Boxplot ----------------------

    # Combine all daily data into a single DataFrame for boxplots
    Data_all_data = pd.concat(
        [Data_per_day_boxplot[date].assign(Date=date) for date in all_dates], ignore_index=True)

    # Map the 'Date' column to filters using your color_map logic
    filter_map = {**{date: 'HEPA 7' for date in A},
                  **{date: 'HEPA 5' for date in C},
                  **{date: 'APS N' for date in D},
                  **{date: 'APS U' for date in B}}
    Data_all_data['Filter'] = Data_all_data['Date'].map(filter_map)

    # Custom color palette
    custom_palette = {
        'HEPA 7': '#77AADD',
        'HEPA 5': '#99DDFF',
        'APS N': '#44BB99',
        'APS U': '#BBCC33',
    }

    plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)
    ax.xaxis.grid(False)
    sns.boxplot(
        x='Filter', y=column_name, data=Data_all_data,
        order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'],
        palette=custom_palette
    )
    plt.title(f'Comparison of Filters - Cabin or Outdoor Air - {title_name}', fontsize=20)
    plt.xlabel('Filter', fontsize=18)
    plt.ylabel(f'{y_label_name} m/z [PPBV]', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(Save_folder, f"{row_number}-3-Boxplot-Cabin-PTR-MS-{save_name_part}.png"))
    plt.close()

    #Boxplot for Up and Downstream
    # ---------------------- Boxplot for Downstream and Upstream ----------------------
    # Combine all data for Boxplot Upstream and Downstream
    Data_all_updown = pd.concat(
        [Data_per_day_boxplot_updown[date].assign(Date=date) for date in all_dates], ignore_index=True)

    # Map the 'Date' column to filters using your color_map logic
    Data_all_updown['Filter'] = Data_all_updown['Date'].map(filter_map)

    # Define custom palette
    custom_palette = {"Upstream": "#117733", "Downstream": "#999933"}

    # Create a new column for Valve Position (Downstream and Upstream) for boxplot plotting
    plt.figure(figsize=(10, 7))
    ax = plt.gca()
    ax.set_axisbelow(True)
    ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)
    ax.xaxis.grid(False)

    # Boxplot for both Downstream and Upstream
    sns.boxplot(
        x='Filter', y=column_name, hue='Valve_Position', data=Data_all_updown,
        order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'], palette=custom_palette, hue_order=['Upstream', 'Downstream']
    )

    # Set plot titles and labels
    plt.title(f'Comparison of Filters - Downstream vs. Upstream - {title_name}', fontsize=20)
    plt.xlabel('Filter', fontsize=18)
    plt.ylabel(f'{y_label_name} m/z [PPBV]', fontsize=18)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.legend(title="Valve Position", loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)
    
    # Tighten layout and save the plot
    plt.tight_layout()
    plt.savefig(os.path.join(Save_folder, f"{row_number}-4-Boxplot-Filter-PTR-MS-{save_name_part}.png"))
    plt.close()

print("Everything saved")