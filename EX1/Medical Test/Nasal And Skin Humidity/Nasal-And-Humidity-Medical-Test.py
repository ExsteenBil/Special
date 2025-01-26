import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import csv
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.axes as ax
import scienceplots

#What to save: 
Filtertype = 'C'

#Flow/Nasal:
Typetest='-F'

# Step 1: Open Dialog box to select the CSV file
Tk().withdraw()  # Prevents an empty tkinter window from appearing
file_path = askopenfilename(title="Select CSV File", filetypes=[("CSV Files", "*.csv")])

# Step 2: Load the CSV file and check if it was done correctly
if file_path:
    try:
        # Read the CSV file
        data = pd.read_csv(file_path, encoding='latin1', delimiter=';')
        print("Data correctly loaded.")
        
        # Apply str.strip() to all string columns
        data = data.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

        # Rename the first column to "Name"
        data.rename(columns={data.columns[0]: 'Name'}, inplace=True)

        # Filter rows where the 7th column (Filter) contains 'A'
        filtered_data = data[data['Filter'] == Filtertype]

        # Define the essential columns to keep
        essential_columns = ['Name', 'Number', 'Seat Number', 'Day', 'Date', 'Filter']

        # Define which columns to keep based on "H" or "F"
        columns_to_keep = [col for col in data.columns if Typetest in col]

        # Combine the essential columns and the filtered H or F columns
        all_columns_to_keep = essential_columns + columns_to_keep

        # Filter the dataset to keep only those columns
        filtered_data = filtered_data[all_columns_to_keep]

        # Output the result
        print(filtered_data)

        # Step 3: Ask where to save the cleaned data
        save_path = asksaveasfilename(title="Save Cleaned CSV File", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

        if save_path:
            # Save the cleaned DataFrame to a CSV file
            filtered_data.to_csv(save_path, index=False, sep=';')
            print(f"Data successfully saved to {save_path}")

    except UnicodeDecodeError as e:
        print(f"Could not read the file correctly due to encoding error: {e}")
else:
    print("File not found.")

#------------------------ Data Processing for Boxplots ------------------------

# Define the groups (e.g., M1, M2, M3, etc.)
groups = ['M1', 'M2', 'M3']  # Add more if needed

# Define the types (e.g., 'H' for Humidity and 'F' for Flow)
types = ['H', 'F']

# Loop through each group and type to calculate avg, diff, flag, and remove outliers
for group in groups:
    for t in types:
        # Define column names dynamically (e.g., M1-H1, M1-H2, M1-H3 or M1-F1, M1-F2, M1-F3)
        cols = [f'{group}-{t}1', f'{group}-{t}2', f'{group}-{t}3']
        
        # Ensure the columns exist in the data
        if all(col in data.columns for col in cols):
            # Calculate the average for the group
            data[f'{group}-{t}_avg'] = data[cols].mean(axis=1)
            
            # Calculate the percentage difference between max and min for the group
            data[f'{group}-{t}_diff'] = (data[cols].max(axis=1) - data[cols].min(axis=1)) / data[cols].min(axis=1) * 100
            
            # Assign 'Nej' if the difference is > 10%, otherwise 'OK'
            data[f'{group}-{t}_flag'] = np.where(data[f'{group}-{t}_diff'] > 10, 'Nej', 'OK')
            
            # Loop over rows where the difference is greater than 10% (i.e., flagged rows)
            for idx, row in data[data[f'{group}-{t}_flag'] == 'Nej'].iterrows():
                # Get the values for the current row (e.g., H1, H2, H3 or F1, F2, F3)
                values = row[cols].values
                
                # Find the median value
                median_val = np.median(values)
                
                # Calculate the distances from the median
                dist_to_min = np.abs(np.min(values) - median_val)
                dist_to_max = np.abs(np.max(values) - median_val)
                
                # Remove the value farthest from the median (either min or max)
                if dist_to_max > dist_to_min:
                    # Remove max value
                    non_outliers = values[values != np.max(values)]
                else:
                    # Remove min value
                    non_outliers = values[values != np.min(values)]
                
                # Recalculate the average without the outlier
                new_avg = non_outliers.mean() if len(non_outliers) > 0 else np.nan
                
                # Update the average in the DataFrame
                data.at[idx, f'{group}-{t}_avg'] = new_avg

# Extract the 'Number' column and all calculated average columns
average_columns = [col for col in data.columns if '_avg' in col]
CleanedCSV = data[['Number', 'Date', 'Filter'] + average_columns]

# Ask where to save the CleanedCSV file
cleaned_save_path = asksaveasfilename(
    title="Save Cleaned CSV File with Averages", 
    defaultextension=".csv", 
    filetypes=[("CSV Files", "*.csv")]
)

if cleaned_save_path:
    # Save the CleanedCSV DataFrame to a CSV file
    CleanedCSV.to_csv(cleaned_save_path, index=False, sep=';')
    print(f"Cleaned CSV successfully saved to {cleaned_save_path}")

#------------------------ Boxplots ------------------------

# Define a custom color palette (you can use any hex codes you like)
group_palette = ["#77AADD", "#99DDFF", "#44BB99", "#BBCC33"]
filter_palette = ["#EEDD88", "#EE8866", "#FFAABB"]

#------------------------- Humidity Boxplots -------------------------
# Activate the 'science' style
plt.style.use(['science', 'no-latex'])

# Apply the custom color palette
sns.set_palette(group_palette)

# Plot 1: Humidity by Group
# Melt the data to bring the groups ('M1-H_avg', 'M2-H_avg', 'M3-H_avg') into one column
melted_data = pd.melt(data, id_vars=['Filter'], value_vars=[f'{g}-H_avg' for g in groups], var_name='Group', value_name='H_avg')

# Replace 'M1-H_avg' with 'M1', 'M2-H_avg' with 'M2', etc. for cleaner group names
melted_data['Group'] = melted_data['Group'].str.replace('-H_avg', '')

# Further customize to replace 'M1', 'M2', 'M3' with 'MT1', 'MT2', 'MT3'
melted_data['Group'] = melted_data['Group'].replace({'M1': 'MT1', 'M2': 'MT2', 'M3': 'MT3'})

# Rename the Filter categories for better understanding
melted_data['Filter'] = melted_data['Filter'].replace({
    'A': 'HEPA 7', 
    'B': 'APS U', 
    'C': 'HEPA 5', 
    'D': 'APS N'
})

# Set up the matplotlib figure
plt.figure(figsize=(10, 7))

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Create a boxplot with Group on x-axis, H_avg on y-axis, and hue as Filter
sns.boxplot(x='Group', y='H_avg', hue='Filter', data=melted_data, hue_order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'])

# Set titles and labels
plt.title('Skin Humidity Test - All', fontsize=20)
plt.xlabel('Medical Test', fontsize=18)
plt.ylabel('Average humidity [%]', fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Display the legend
plt.legend(title='Conditions', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

y_min, y_max = ax.get_ylim()
ax.set_ylim(0, max(y_max, 0))

# Show the plot
plt.tight_layout()
plt.show()


# Apply the custom color palette
sns.set_palette(filter_palette)

# Plot 2: Humidity by Filter
plt.figure(figsize=(10, 6))

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Create a boxplot with Filter on x-axis, H_avg on y-axis, and hue as Group
sns.boxplot(x='Filter', y='H_avg', hue='Group', data=melted_data, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'])

# Set titles and labels
plt.title('Skin humidity by Filter and Group', fontsize=20)
plt.xlabel('Conditions', fontsize=16)
plt.ylabel('Average humidity [%]', fontsize=16)

# Set tick font sizes
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Display the legend
plt.legend(title='Group', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12, title_fontsize=14)

y_min, y_max = ax.get_ylim()
ax.set_ylim(0, max(y_max, 0))

# Show the plot
plt.tight_layout()
plt.show()

#------------------------- Flow Boxplots -------------------------

# Apply the custom color palette
sns.set_palette(group_palette)

# Plot 3: Flow by Group
# Melt the data to bring the groups ('M1-F_avg', 'M2-F_avg', 'M3-F_avg') into one column
melted_data_F = pd.melt(data, id_vars=['Filter'], value_vars=[f'{g}-F_avg' for g in groups], var_name='Group', value_name='F_avg')

# Replace 'M1-F_avg' with 'M1', 'M2-F_avg' with 'M2', etc. for cleaner group names
melted_data_F['Group'] = melted_data_F['Group'].str.replace('-F_avg', '')

# Further customize to replace 'M1', 'M2', 'M3' with 'MT1', 'MT2', 'MT3'
melted_data_F['Group'] = melted_data_F['Group'].replace({'M1': 'MT1', 'M2': 'MT2', 'M3': 'MT3'})

# Rename the Filter categories for better understanding
melted_data_F['Filter'] = melted_data_F['Filter'].replace({
    'A': 'HEPA 7', 
    'B': 'APS U', 
    'C': 'HEPA 5', 
    'D': 'APS N'
})

# Set up the matplotlib figure
plt.figure(figsize=(10, 7))

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Create a boxplot with Group on x-axis, F_avg on y-axis, and hue as Filter
sns.boxplot(x='Group', y='F_avg', hue='Filter', data=melted_data_F, hue_order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'])

# Set titles and labels
plt.title('Nasal Peak Flow Test - All', fontsize=20)
plt.xlabel('Medical Test', fontsize=18)
plt.ylabel('Average flow [L/min]', fontsize=18)

# Set tick font sizes
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

# Display the legend
plt.legend(title='Conditions', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=14, title_fontsize=16)

y_min, y_max = ax.get_ylim()
ax.set_ylim(0, max(y_max, 0))

# Show the plot
plt.tight_layout()
plt.show()


# Apply the custom color palette
sns.set_palette(filter_palette)

# Plot 4: Flow by Filter
plt.figure(figsize=(10, 6))

# Get the current axis
ax = plt.gca()

# Set gridlines to be below the boxplots
ax.set_axisbelow(True)

# Add horizontal gridlines
ax.yaxis.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75)

# Create a boxplot with Filter on x-axis, F_avg on y-axis, and hue as Group
sns.boxplot(x='Filter', y='F_avg', hue='Group', data=melted_data_F, order=['HEPA 7', 'HEPA 5', 'APS N', 'APS U'])

# Set titles and labels
plt.title('Flow test by Filter and Group', fontsize=20)
plt.xlabel('Filter', fontsize=16)
plt.ylabel('Average flow [L/min]', fontsize=16)

# Set tick font sizes
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# Display the legend
plt.legend(title='Group', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12, title_fontsize=14)

y_min, y_max = ax.get_ylim()
ax.set_ylim(0, max(y_max, 0))

# Show the plot
plt.tight_layout()
plt.show()