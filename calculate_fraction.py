import pandas as pd

# Load the data
csv_path = "data/output_parallel_tool/lulc_basin1988_pixel_counts.csv"  # Replace with your actual CSV path
data = pd.read_csv(csv_path)

# Calculate the total count for each row
data["Total"] = data[
    ["Cropland", "Forest", "Urban", "Water", "Baresoil", "Pasture"]
].sum(axis=1)

# Remove rows with a total count of 0
data = data[data["Total"] > 0]

# Convert counts to fractions
for column in ["Cropland", "Forest", "Urban", "Water", "Baresoil", "Pasture"]:
    data[column + "_Fraction"] = data[column] / data["Total"]

# Remove the total count column if you don't need it in the final CSV
data.drop(columns=["Total"], inplace=True)

# Save the updated data to a new CSV file
updated_csv_path = csv_path  # Change this to your desired output file path
data.to_csv(updated_csv_path, index=False)
