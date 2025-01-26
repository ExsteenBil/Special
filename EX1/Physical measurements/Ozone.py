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
    Line2D([0], [0], color='#0046a1', lw=2, linestyle='-', label='HEPA 7 (Supply)'),
    Line2D([0], [0], color='#0046a1', lw=2, linestyle='--', label='HEPA 7 (Exhaust)'),
    Line2D([0], [0], color='#00b3ef', lw=2, linestyle='-', label='HEPA 5 (Supply)'),
    Line2D([0], [0], color='#00b3ef', lw=2, linestyle='--', label='HEPA 5 (Exhaust)'),
    Line2D([0], [0], color='#7ed348', lw=2, linestyle='-', label='APS N (Supply)'),
    Line2D([0], [0], color='#7ed348', lw=2, linestyle='--', label='APS N (Exhaust)'),
    Line2D([0], [0], color='#009650', lw=2, linestyle='-', label='APS U (Supply)'),
    Line2D([0], [0], color='#009650', lw=2, linestyle='--', label='APS U (Exhaust)')
]

custom_legend2 = [
    Line2D([0], [0], color='#0046a1', lw=2, linestyle='--', label='HEPA 7'),
    Line2D([0], [0], color='#00b3ef', lw=2, linestyle='--', label='HEPA 5'),
    Line2D([0], [0], color='#7ed348', lw=2, linestyle='--', label='APS N'),
    Line2D([0], [0], color='#009650', lw=2, linestyle='--', label='APS U')
]

start_time = '08:55:00'
end_time = '20:05:00'

# Initialize Tkinter root for file selection
root = tk.Tk()
root.withdraw()

# Select the Ozone data file
ozone_file_path = filedialog.askopenfilename(title="Select Ozone CSV File", filetypes=[("CSV Files", "*.csv")])

if not ozone_file_path:
    print("File selection incomplete.")
    exit()

# Load Ozone data
ozone_df = pd.read_csv(ozone_file_path, delimiter=';', decimal=".")
ozone_df['dtm'] = pd.to_datetime(ozone_df['Date-Time'], dayfirst=True, format='%d-%m-%Y %H:%M')

ozone_df = ozone_df.dropna(subset=['Indoor to Outdoor (adjusted) ratio'])

# Replace values smaller than 0 with NaN
ozone_df.loc[ozone_df['Indoor to Outdoor (adjusted) ratio'] < 0, 'Indoor to Outdoor (adjusted) ratio'] = np.nan

# Replace values in the 'Filter' column
ozone_df['Filter'] = ozone_df['Filter'].replace({'APSN': 'APS N', 'APSU': 'APS U'})

# Filter and process Ozone data for each date
ozone_per_day = {}
for date in all_dates:
    start_timestamp = pd.Timestamp(f'{date} {start_time}')
    end_timestamp = pd.Timestamp(f'{date} {end_time}')
    
    # Filter data by date and time
    ozone_day_df = ozone_df[(ozone_df['dtm'] >= start_timestamp) & (ozone_df['dtm'] <= end_timestamp)]
    ozone_day_df['Seconds Since Midnight'] = (
        ozone_day_df['dtm'].dt.hour * 3600 +
        ozone_day_df['dtm'].dt.minute * 60 +
        ozone_day_df['dtm'].dt.second
    )
    ozone_per_day[date] = ozone_day_df[['Seconds Since Midnight', 'Ozone-Supply', 'Ozone-Exhaust', 'Indoor to Outdoor (adjusted) ratio']]

def plot_filter_type_separate(data, filter_type, color_map, output_folder):
    # Activate the 'science' style
    plt.style.use(['science', 'no-latex'])

    # Define marker styles for the dates
    marker_styles = ['o', 's', '*', '^', 'P', 'D', 'X', 'v']
    columns = ['Ozone-Supply', 'Ozone-Exhaust', 'Indoor to Outdoor (adjusted) ratio']
    y_labels = ['Ozone Supply [ppb]', 'Ozone Exhaust [ppb]', 'Ozone Ratio [-]']
    titles = [f'{filter_type} - Comparison of Dates - Ozone Supply', f'{filter_type} - Comparison of Dates - Ozone Exhaust', f'{filter_type} - Comparison of Dates - Ozone Exhaust/Supply Ratio']

    # Iterate over the three data columns
    for column, ylabel, title in zip(columns, y_labels, titles):
        # Create a new figure for each column
        fig, ax = plt.subplots(figsize=(10, 7))
        
        # Plot data for each date with unique marker style
        for i, date in enumerate(data.keys()):
            df = data[date]
            ax.plot(
                df['Seconds Since Midnight'], 
                df[column], 
                marker=marker_styles[i % len(marker_styles)],  # Cycle through marker styles
                linestyle='None',  # No connecting lines
                color=color_map[date], 
                label=date
            )
        
        # Ensure 0 is included on the y-axis
        ax = plt.gca()
        y_min, y_max = ax.get_ylim()
        ax.set_ylim(-0.1, 50)  # Extend y-axis to include 0 if necessary

        # Apply labels, titles, and grid
        ax.set_xlabel('Time of Day [HH:MM]', fontsize=18)
        ax.set_ylabel(ylabel, fontsize=18)
        ax.set_title(title, fontsize=20)
        ax.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)
        ax.set_xticks([32400, 36000, 39600, 43200, 46800, 50400, 54000, 57600, 61200, 64800, 68400, 72000])
        ax.set_xticklabels(['09:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00'])
        ax.tick_params(axis='both', which='major', labelsize=16)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title="Dates", title_fontsize=16)

        # Save the figure
        filename = f'{filter_type}_{column.replace(" ", "_")}.png'
        save_path = os.path.join(output_folder, filename)
        plt.tight_layout()
        plt.savefig(save_path, format='png', dpi=300)  # Save as a high-resolution PNG
        plt.close(fig)  # Close the figure to save memory


# Group data by filter types
filter_groups = {
    'HEPA 7': A,
    'HEPA 5': C,
    'APS N': D,
    'APS U': B
}

# Output folder for plots
output_folder = filedialog.askdirectory(title="Select Output Folder for Plots")
if not output_folder:
    print("Output folder selection incomplete.")
    exit()

# Plot data for each filter group
for filter_type, dates in filter_groups.items():
    filter_data = {date: ozone_per_day[date] for date in dates if date in ozone_per_day}
    plot_filter_type_separate(filter_data, filter_type, color_map, output_folder)

print("Plots saved successfully!")