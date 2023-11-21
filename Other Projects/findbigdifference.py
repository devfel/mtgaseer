import pandas as pd
import numpy as np


def read_data(file_path):
    try:
        data = pd.read_csv(file_path)
        # Clean 'GIH WR' column
        data["GIH WR"] = (
            data["GIH WR"]
            .str.strip()  # Remove leading/trailing white spaces
            .replace("%", "", regex=True)  # Remove '%' sign
            .replace("", 0)  # Replace empty strings with 0
            .astype(float)  # Convert to float
        )
        return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None


# General file path
general_file_path = "C:\\Users\\LFVAR\\Downloads\\card-ratings-2023-11-20.csv"
general_data = read_data(general_file_path)

# Color combinations
color_combinations = ["UB", "UR", "UG", "WU", "WB", "WR", "WG", "BR", "BG", "RG"]

# Generate file paths for each color combination
color_files = [
    f"C:\\Users\\LFVAR\\Downloads\\card-ratings-2023-11-20({combo}).csv"
    for combo in color_combinations
]

# Dictionary to hold the differences
differences = {}

# Iterate through each color file
for file_path in color_files:
    color_data = read_data(file_path)
    if color_data is not None:
        # Merge with the general data on 'Card Name'
        merged_data = general_data.merge(
            color_data, on="Name", suffixes=("_general", "_color")
        )
        # Calculate the difference in 'GIH WR'
        merged_data["difference"] = np.abs(
            merged_data["GIH WR_general"] - merged_data["GIH WR_color"]
        )
        # Update differences dictionary
        for _, row in merged_data.iterrows():
            card_name = row["Name"]
            diff = row["difference"]
            if not np.isnan(diff) and diff > differences.get(card_name, (0, ""))[0]:
                differences[card_name] = (diff, file_path)

# Get the top 10 differences
top_10 = sorted(differences.items(), key=lambda x: x[1][0], reverse=True)[:10]

# Print the results
for card, (diff, file_name) in top_10:
    print(f"Card: {card}, Difference: {diff}, File: {file_name}")
