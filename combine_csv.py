import pandas as pd
import numpy as np
import os

output_folder = 'data/output_parallel'  # Adjust to your output directory
combined_csv_path = 'data/output_parallel/combined_median.csv'  # Adjust to your combined CSV file path

# Step 1: List all CSV files in the output folder
csv_files = [os.path.join(output_folder, f) for f in os.listdir(output_folder) if f.endswith('.csv')]

# Step 2: Initialize a dictionary to hold all data
data = {}

# Read each CSV file and append the data
for file in csv_files:
    df = pd.read_csv(file)
    for column in df.columns:
        if column not in data:
            data[column] = []
        data[column].append(df[column])

# Step 3: Calculate median for each column and create a combined DataFrame
median_data = {}
for column, values in data.items():
    # Skip non-class columns if necessary (e.g., 'grid_id', 'latitude', 'longitude')
    if column in ['grid_id', 'latitude', 'longitude']:
        median_data[column] = values[0]  # Copy the first file's data for non-class columns
    else:
        # Calculate median across all CSVs for each cell
        stacked_values = np.vstack(values)
        median_values = np.median(stacked_values, axis=0)
        median_data[column] = median_values

# Create a DataFrame from the median values
median_df = pd.DataFrame(median_data)

# If 'grid_id' was used, set it as index
if 'grid_id' in median_df:
    median_df.set_index('grid_id', inplace=True)

# Save the combined DataFrame to a new CSV
median_df.to_csv(combined_csv_path)
