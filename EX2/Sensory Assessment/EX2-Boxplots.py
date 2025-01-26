import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import scienceplots

#What to save: 
Filtertype = '01-10-2024'  # Use a string format for date

#Level:
Level='Rigtig'

# Step 1: Open Dialog box to select the CSV file
Tk().withdraw()  # Prevents an empty tkinter window from appearing
file_path = askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])

# Step 2: Load the CSV file and check if it was done correctly
if file_path:
    try:
        # Read the CSV file
        data = pd.read_csv(file_path, encoding='latin1', delimiter=';')
        print("Data correctly loaded.")
        
        # Rename the first column to "Name"
        data.rename(columns={data.columns[0]: 'Number'}, inplace=True)

        # Apply str.strip() to all string columns
        data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        #Fjerner NaN linjer
        data = data.dropna(subset=['Number'])

        # Ensure 'Date' is in a datetime format
        data['Date'] = pd.to_datetime(data['Date'], format='%d-%m-%Y', errors='coerce')

        # Output the result
        print(data)

    except UnicodeDecodeError as e:
        print(f"Could not read the file correctly due to encoding error: {e}")
else:
    print("File not found.")

#------------------------ Data Processing for Boxplots ------------------------

# Convert Filtertype to a datetime object
Filtertype_date = pd.to_datetime(Filtertype, format='%d-%m-%Y')

# Filter rows so only the same day is used
data = data[data['Date'] == Filtertype_date]

# Filter rows so only the same 'Filter-Level' is used
filtered_data = data[data['Filter-Final'] == Level]

row_count = filtered_data['Number'].nunique()

#print(filtered_data)

#------------------------ Rename Tubes ------------------------
# Define mappings for each date
title_mappings = {
    '01-10-2024': 'HEPA',
    '02-10-2024': 'Charcoal',
    '03-10-2024': 'APS'
}


# Apply the appropriate mapping if it exists
if Filtertype in title_mappings:
    Title = title_mappings[Filtertype]
else:
    print("No mapping found for the specified date.")


    # Define mappings for each date
tube_mappings = {
    '01-10-2024': {1: 'H - F1', 2: 'H - F10', 3: 'H - EX1, U', 4: 'H - F6', 5: 'H - F2', 6: 'H - F5', 7: 'H - F3', 8: 'Chamber Air'},
    '02-10-2024': {1: 'C - F1', 2: 'C - F8', 3: 'C - EX1, U', 4: 'C - F6', 5: 'C - EX1, N', 6: 'C - F5', 7: 'C - F3', 8: 'Chamber Air'},
    '03-10-2024': {1: 'APS - F1', 2: 'APS - F8', 3: 'APS - EX1, U', 4: 'APS - F6', 5: 'APS - EX1, N', 6: 'APS - F5', 7: 'APS - F3', 8: 'Chamber Air'}
}

# Apply the appropriate mapping if it exists
if Filtertype in tube_mappings:
    filtered_data['Tube'] = filtered_data['Tube'].replace(tube_mappings[Filtertype])
else:
    print("No mapping found for the specified date.")


# Define the desired order for each date
# Define the desired order for each date
tube_order_mappings = {
    '01-10-2024': ['Chamber Air', 'H - EX1, U', 'H - F10', 'H - F2', 'H - F1', 'H - F6', 'H - F5', 'H - F3'],
    '02-10-2024': ['Chamber Air', 'C - EX1, N', 'C - EX1, U', 'C - F8', 'C - F1', 'C - F6', 'C - F5', 'C - F3'],
    '03-10-2024': ['Chamber Air', 'APS - EX1, N', 'APS - EX1, U', 'APS - F8', 'APS - F1', 'APS - F6', 'APS - F5', 'APS - F3']
}

# Use the appropriate tube order for the selected date
if Filtertype in tube_order_mappings:
    tube_order = tube_order_mappings[Filtertype]
else:
    print("No tube order mapping found for the specified date.")
    tube_order = None  # Default order

#------------------------ Boxplots ------------------------

# Define a custom color palette (you can use any hex codes you like)
custom_palette = ["#332288", "#88CCEE", "#44AA99", "#117733", "#999933", "#DDCC77", "#CC6677", "#882255"]

# Activate the 'science' style
plt.style.use(['science', 'no-latex'])

# Apply the custom color palette
sns.set_palette(custom_palette)

#---------- Odour ----------
plt.figure(figsize=(10, 7))

# Create the boxplot
sns.boxplot(x='Tube', y='Odour', data=filtered_data, order=tube_order)

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Turn off vertical gridlines
ax.xaxis.grid(False)

# Add titles and labels
plt.title(f'Odour Rating by Filter - {Filtertype} - {Title} - N={row_count}', fontsize=20)
plt.xlabel('Filter', fontsize=18)
plt.ylabel('$None$ ---- Rating [-] ---- $Overpowering$', fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)

# Set the y-axis limits
ax.set_ylim(-0.1, 5.1)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()

#---------- Pungency ----------
plt.figure(figsize=(10, 7))

# Create the boxplot
sns.boxplot(x='Tube', y='Pungency', data=filtered_data, order=tube_order)

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Turn off vertical gridlines
ax.xaxis.grid(False)

# Add titles and labels
plt.title(f'Pungency Rating by Filter - {Filtertype} - {Title} - N={row_count}', fontsize=20)
plt.xlabel('Filter', fontsize=18)
plt.ylabel('$None$ ---- Rating [-] ---- $Overpowering$', fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)

# Set the y-axis limits
ax.set_ylim(-0.1, 5.1)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()

#---------- Air quality ----------
plt.figure(figsize=(10, 7))

# Create the boxplot
sns.boxplot(x='Tube', y='Air quality', data=filtered_data, order=tube_order)

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Turn off vertical gridlines
ax.xaxis.grid(False)

# Add titles and labels
plt.title(f'Air Quality Rating by Filter - {Filtertype} - {Title} - N={row_count}', fontsize=20)
plt.xlabel('Filter', fontsize=18)
plt.ylabel('$Unacceptable$ ---- Rating [-] ---- $Acceptable$', fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)

# Set the y-axis limits
ax.set_ylim(-1.02, 1.02)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()

#---------- Freshness ----------
plt.figure(figsize=(10, 7))

# Create the boxplot
sns.boxplot(x='Tube', y='Freshness', data=filtered_data, order=tube_order)

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Turn off vertical gridlines
ax.xaxis.grid(False)

# Add titles and labels
plt.title(f'Freshness Rating by Filter - {Filtertype} - {Title} - N={row_count}', fontsize=20)
plt.xlabel('Filter', fontsize=18)
plt.ylabel('$Fresh$ ---- Rating [-] ---- $Stuffy$', fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)

# Set the y-axis limits
ax.set_ylim(-2, 102)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()

