import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import scienceplots


# Set the desired working directory
input_directory = r"C:\Users\julie\OneDrive - Danmarks Tekniske Universitet\Speciale\Grundlag\1-Data-Raw-Air-Quality\Characterization"
os.chdir(input_directory)

# Load the CSV file
data = pd.read_csv(os.path.join(input_directory, 'Characterization_cleaned_uden_duplicates.csv'), sep=',')


#########################################################################################################################

# Select the relevant columns
ID = data.columns[0]
Q1 = data.columns[22]
Q2 = data.columns[23]
Q3 = data.columns[24]
Q4 = data.columns[25]
Q5 = data.columns[26]
Q6 = data.columns[27]
Q7 = data.columns[28]
Q8 = data.columns[29]
Q9 = data.columns[30]
Q10 = data.columns[31]
Q11 = data.columns[32]
Q12 = data.columns[33]
Q13 = data.columns[34]
Q14 = data.columns[35]
Q15 = data.columns[36]
Q16 = data.columns[37]
Q17 = data.columns[38]
Q18 = data.columns[39]
Q19 = data.columns[40]
Q20 = data.columns[41]
Q21 = data.columns[42]

# Adjust columns Q1 to Q21 to change scale from 1-6 to 0-5
columns_to_adjust = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21]

# Subtract 1 from each relevant column to adjust scale
data[columns_to_adjust] = data[columns_to_adjust] - 1


# Define which questions are reverse-scored
reverse_scored_items = [Q2, Q4, Q5, Q6, Q7, Q9, Q10, Q11, Q13, Q16, Q17, Q18, Q19, Q21]

# Define alternative scales with specific max values
# These scales should also be reverse-scored
alternative_scales = {
    Q6: 5,  # Scale 'c': Always (0) to Never (5)
    Q9: 4,  # Scale 'd': Completely deter me (0) to Not at all important (4)
    Q10: 5, # Scale 'e': Almost always (0) to Never (5)
    Q18: 5  # Scale 'f': Always (0) to Never (5)
    }

# General reverse scoring function for any max score
def reverse_score(series, max_score):
    return max_score - series

# Apply reverse scoring to specified items
for item in reverse_scored_items:
    if item in alternative_scales:  # If item has an alternative scale
        max_score = alternative_scales[item]
    else:
        max_score = 5  # Default scale of 0 to 5

    # Apply reverse scoring
    data[item] = reverse_score(data[item], max_score)


# List of question columns to sum for each test person
question_columns = [Q1, Q2, Q3, Q4, Q5, Q6, Q7, Q8, Q9, Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q18, Q19, Q20, Q21]

# Calculate the sum across the specified columns for each test person
data['Total_Score'] = data[question_columns].sum(axis=1)


#########################################################################################################################

# Median and 67th percentile

# Calculate the median of the Total_Score column
median_total_score = data['Total_Score'].median()

# Print the median
print("Median of Total Score:", median_total_score)
# Medianen er 55

# Calculate the 67th percentile of the Total_Score column
percentile_67 = data['Total_Score'].quantile(0.67)
print("67th Percentile of Total Score:", percentile_67)
# 67% kvartilen er 60.86

# Create a new column 'IAQ_CSS' with 1 for high scores and 0 for the rest
data['IAQ_CSS'] = np.where(data['Total_Score'] > percentile_67, 1, 0)

print("How many are sensitive:", sum(data['IAQ_CSS']))
# 20 personer er sensitive ud fra CSS


#########################################################################################################################

# Output CSV

# Select output data
data.rename(columns={ID: 'ID'}, inplace=True)
output_data = data[['ID', 'Total_Score', 'IAQ_CSS']]

# Specify the new output directory
output_directory = r"C:\Users\julie\OneDrive - Danmarks Tekniske Universitet\Speciale\Analyse\JulieCode\CSS"

# Save the output to a CSV file
output_file_path = os.path.join(output_directory, 'CSS_Sensitivity.csv')

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

# Save the output to a CSV file
output_data.to_csv(output_file_path, index=False)

# Display a message to confirm saving
print(f"CSV file saved to {output_file_path}")


#########################################################################################################################

# Style for charts


# Activate the 'science' style
plt.style.use(['science', 'no-latex'])

# Define a custom color palette
custom_palette = ["#AACCEE", "#CCDDAA"]

# Apply the custom color palette
sns.set_palette(custom_palette)


#########################################################################################################################

# Boxplot of sensitivity according to CSS


# Map 0 to "Non-sensitive" and 1 to "Sensitive" for easier interpretation
data['IAQ_CSS'] = data['IAQ_CSS'].map({0: 'Non-sensitive', 1: 'Sensitive'})

# Create the boxplot
plt.figure(figsize=(10, 7))
plt.grid(visible=True, linestyle='--', linewidth=0.5, alpha=0.75, zorder=0)
sns.boxplot(x='IAQ_CSS', y='Total_Score', data=data, palette=custom_palette, order=['Sensitive', 'Non-sensitive'], zorder=3)

# Set y-axis limits from 0 to 105
plt.ylim(0, 105)

# Add titles and labels
plt.title('Boxplot of Sensitivity according to CSS', fontsize=20, zorder=4)
plt.xlabel('Group', fontsize=18, zorder=4)
plt.ylabel('Sensitivity Score from CSS', fontsize=18, zorder=4)

# Set tick font sizes
plt.xticks(fontsize=16, zorder=4)
plt.yticks(fontsize=16, zorder=4)

# Adjust layout
plt.tight_layout()

# Display the plot
plt.show()