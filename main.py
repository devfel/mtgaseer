import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import pandas as pd
import math
import os


#######################################################
# DATA LOADING AND PREPARATION
#######################################################

# Get the directory of the current script file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Navigate up one level ('..') and then to the 'data' directory
data_dir = os.path.join(current_dir, "data")

# Load your data

file_path = os.path.join(data_dir, "card-ratings-2023-11-20.csv")
mtg_data = pd.read_csv(file_path)
file_path_colors = os.path.join(data_dir, "colors-2023-11-20.csv")
mtg_data_colors = pd.read_csv(file_path_colors)

# Load the color stats data
color_stats_df = pd.read_csv(file_path_colors)

# Extract overall win rate and create a dictionary for color win rates
overall_win_rate = color_stats_df[color_stats_df["Color"] == "All Decks"][
    "Win Rate"
].values[0]
# Create a dictionary to map color combinations to their win rates
color_win_rates = color_stats_df.set_index("Color")["Win Rate"].to_dict()


#######################################################
# DATA CLEANING AND PROCESSING
#######################################################

# Define columns with percentage values and clean them
percentage_columns = ["GNS WR", "GIH WR", "GD WR", "OH WR", "GP WR", "% GP"]
for col in percentage_columns:
    mtg_data[col] = (
        mtg_data[col]
        .str.strip()  # Remove leading/trailing white spaces
        .replace("%", "", regex=True)  # Remove '%' sign
        .replace("", 0)  # Replace empty strings with 0 or use np.nan
        .astype(float)  # Convert to float
    )

# Clean and convert the IWD column
mtg_data["IWD"] = (
    mtg_data["IWD"]
    .str.strip()  # Remove leading/trailing white spaces
    .replace(
        {"pp": "", "[^0-9.-]": ""}, regex=True
    )  # Remove 'pp' and any other non-numeric characters
    .replace("", 0)  # Replace empty strings with 0 or use np.nan
    .astype(float)  # Convert to float
)

# Define columns for NaN replacement and replace NaN values
nan_replacement_columns = [
    "ALSA",
    "# Picked",
    "ATA",
    "# GP",
    "% GP",
    "GP WR",
    "# OH",
    "OH WR",
    "# GD",
    "GD WR",
    "# GIH",
    "GIH WR",
    "# GNS",
    "GNS WR",
    "IWD",
]
for col in nan_replacement_columns:
    mtg_data[col] = mtg_data[col].fillna("-")

# Clean 'Color' and 'Rarity' columns for leading/trailing spaces and missing values
for col in ["Color", "Rarity"]:
    mtg_data[col] = mtg_data[col].str.strip().replace("", "-").fillna("-")


#######################################################
# GUI SETUP - MAIN WINDOW AND STYLING
#######################################################

# Setting up the main window
root = tk.Tk()
root.title("MTG Cards Data")
root.configure(background="white")
root.minsize(800, 600)


# Create a style
style = ttk.Style()
style.theme_use("clam")  # or 'default', 'classic', 'alt', etc.
# Modify the settings of the tab
style.configure("TNotebook.Tab", borderwidth=2, relief="raised")
# Apply the modified style to the Notebook

# notebook = ttk.Notebook(root, style="TNotebook") TODO: DELETE
# Create the Notebook widget for tab organization
notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True, fill="both")

# Create the frames for each tab
tab1 = ttk.Frame(notebook)  # Tab for the Card Details Information
tab2 = ttk.Frame(notebook)  # Tab for the two-color win rates

# Add the tabs to the notebook
notebook.add(tab1, text="Card Information")
notebook.add(tab2, text="Two-Color Win Rates")


#######################################################
# SEARCH FUNCTIONALITY
#######################################################


# Function to dynamically search and filter data
def dynamic_search(event):
    search_query = search_var.get()
    filter_data(search_query)


# Function to filter data based on search query
def filter_data(search_query):
    filtered_data = mtg_data[
        mtg_data["Name"].str.contains(search_query, case=False, na=False)
    ]
    update_table(filtered_data)


#######################################################
# DATA TABLE (TREEVIEW) SETUP AND FUNCTIONS
#######################################################


# Function to update the table with filtered data
def update_table(data):
    for i in tree.get_children():
        tree.delete(i)
    for index, row in data.iterrows():
        tree.insert(
            "",
            tk.END,
            values=(
                row["Name"],
                row["ALSA"],
                row["Color"],
                row["Rarity"],
                row["% GP"],
                row["GIH WR"],
                row["IWD"],
            ),
        )
    auto_resize_columns(tree, padding=10)


# Automatically adjust column widths
def auto_resize_columns(treeview, padding=10):
    for column in treeview["columns"]:
        header_width = Font().measure(column.title())
        max_width = header_width
        for row in treeview.get_children():
            cell_value = treeview.set(row, column)
            cell_width = Font().measure(cell_value)
            if cell_width > max_width:
                max_width = cell_width
        treeview.column(column, width=max_width + padding)


# Function to update column header with sort indicator
def update_sort_column_header(tv, col, reverse):
    global current_sort_column, current_sort_order
    for c in tv["columns"]:
        if c == col:
            # Add an arrow symbol to the current sorted column
            arrow = "↑" if reverse else "↓"
            tv.heading(c, text=f"{c} {arrow}")
        else:
            # Remove arrow symbol from other columns
            tv.heading(c, text=c)
    current_sort_column = col
    current_sort_order = reverse


# Function to sort the table considering NaN, hyphens, and non-numeric values
def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children("")]

    # Custom sorting function
    def custom_sort(tup):
        val, _ = tup

        # Check for hyphen or empty values, treat them as 'last' in sorting always
        if val == "-" or val == "" or val is None:
            return (2, math.inf)

        # Try converting to float for numeric sorting
        try:
            numeric_val = float(val)
            return (0, -numeric_val if reverse else numeric_val)
        except ValueError:
            # Non-numeric values get sorted as strings (case-insensitive)
            return (1, val.lower() if isinstance(val, str) else val)

    # Sort using the custom function
    l.sort(
        key=custom_sort, reverse=False
    )  # Always sort in ascending order based on custom_sort logic

    # Rearrange the items in the treeview
    for index, (_, k) in enumerate(l):
        tv.move(k, "", index)

    # Change the sort order for the next time
    tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

    update_sort_column_header(tv, col, reverse)


# Function for sorting alphabetically ('Color', 'Rarity', 'Name')
def treeview_sort_column_alphabetic(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children("")]

    def custom_sort(tup):
        val, _ = tup
        if val == "-" or val == "" or val is None:
            return (1, math.inf)
        return (0, val.lower() if isinstance(val, str) else val)

    l.sort(key=custom_sort, reverse=reverse)
    for index, (_, k) in enumerate(l):
        tv.move(k, "", index)

    tv.heading(
        col, command=lambda: treeview_sort_column_alphabetic(tv, col, not reverse)
    )

    update_sort_column_header(tv, col, reverse)


#######################################################
# GUI SETUP - SEARCH AND FILTERING WIDGETS
#######################################################

# Frame for Search Widgets
search_frame = ttk.Frame(tab1)
search_frame.pack(pady=10)

# Frame for Color Selection
color_selection_frame = ttk.Frame(tab1)
color_selection_frame.pack(pady=10)


#######################################################
# GUI SETUP - COLOR SELECTION WIDGETS
#######################################################

# Label for the Color Selection Combobox
color_label = tk.Label(
    color_selection_frame,
    text="Select Color:",
    font=("Helvetica", 12),
    background="#dcdad5",
)
color_label.pack(side=tk.LEFT, padx=(0, 10))

# Combobox for Color Selection
color_selection_var = tk.StringVar()
color_selection_combobox = ttk.Combobox(
    color_selection_frame, textvariable=color_selection_var, state="readonly"
)
color_selection_combobox["values"] = (
    "All Colors",
    "White (W)",
    "Blue (U)",
    "Black (B)",
    "Red (R)",
    "Green (G)",
)
# Set 'All Colors' as the default selected option
color_selection_combobox.set("All Colors")
color_selection_combobox.pack(side=tk.LEFT)

# Mapping from colors to their combinations
color_combinations = {
    "White (W)": ["WU", "WB", "WR", "WG"],
    "Blue (U)": ["WU", "UB", "UR", "UG"],
    "Black (B)": ["WB", "UB", "BR", "BG"],
    "Red (R)": ["WR", "UR", "BR", "RG"],
    "Green (G)": ["WG", "UG", "BG", "RG"],
}

# Mapping from simple codes to full names
color_code_to_name = {
    "WU": "Azorius (WU)",
    "WB": "Orzhov (WB)",
    "WR": "Boros (RW)",
    "WG": "Selesnya (GW)",
    "UB": "Dimir (UB)",
    "UR": "Izzet (UR)",
    "UG": "Simic (GU)",
    "BR": "Rakdos (BR)",
    "BG": "Golgari (BG)",
    "RG": "Gruul (RG)",
}

# Add some horizontal space between the two elements
spacer_label = tk.Label(color_selection_frame, text="", width=2, background="#dcdad5")
spacer_label.pack(side=tk.LEFT)

# Label for the Color Combination Selection Combobox
combo_label = tk.Label(
    color_selection_frame,
    text="Color Combination:",
    font=("Helvetica", 12),
    background="#dcdad5",
)
combo_label.pack(side=tk.LEFT, padx=(0, 10))

# Combobox for Color Combination Selection
color_combo_var = tk.StringVar()
color_combo_combobox = ttk.Combobox(
    color_selection_frame, textvariable=color_combo_var, state="disabled"
)
color_combo_combobox.pack(side=tk.LEFT)

##################################################################

# Styling
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 8, "bold"))

# Search field label
search_label = tk.Label(
    search_frame, text="Search Card:", font=("Helvetica", 12), background="#dcdad5"
)
search_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some padding for spacing

#### Get the default background color for the theme ###
# default_bg = style.lookup("TFrame", "background")
# Print the default background color
# print(f"The default background color for the 'clam' style is: {default_bg}")

# Search field entry
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Helvetica", 10))
search_entry.pack(side=tk.LEFT)
search_entry.bind("<KeyRelease>", dynamic_search)

# Add title label for displaying the stats
title_label = tk.Label(
    tab1,
    text="Showing Overall Data",
    font=("Helvetica", 12, "bold"),
    background="#dcdad5",
)
title_label.pack(pady=(5, 10))  # Adjust padding as needed


#######################################################
# COLOR SELECTION AND DATA FILTERING
#######################################################


# Function for updating the title based on color selection
def update_title(selected_color_code=None):
    selected_color_name = color_code_to_name.get(selected_color_code, None)
    if selected_color_name and selected_color_name in color_win_rates:
        win_rate = color_win_rates[selected_color_name]
        title_text = f"{selected_color_name} - Avg. Win Rate: {win_rate}"
    else:
        title_text = f"Overall - Avg. Win Rate: {overall_win_rate}"
    title_label.config(text=title_text)


# Function for loading data from a file
def load_data_from_file(file_path):
    global mtg_data
    try:
        mtg_data = pd.read_csv(file_path)

        # Repeat the same cleaning and processing as for the general file
        # Clean percentage columns
        for col in percentage_columns:
            mtg_data[col] = (
                mtg_data[col]
                .str.strip()  # Remove leading/trailing white spaces
                .replace("%", "", regex=True)  # Remove '%' sign
                .replace("", 0)  # Replace empty strings with 0 or use np.nan
                .astype(float)  # Convert to float
            )

        # Clean and convert the IWD column
        mtg_data["IWD"] = (
            mtg_data["IWD"]
            .str.strip()  # Remove leading/trailing white spaces
            .replace(
                {"pp": "", "[^0-9.-]": ""}, regex=True
            )  # Remove 'pp' and any other non-numeric characters
            .replace("", 0)  # Replace empty strings with 0 or use np.nan
            .astype(float)  # Convert to float
        )

        # Replace NaN values in specified columns
        for col in nan_replacement_columns:
            mtg_data[col] = mtg_data[col].fillna("-")

        # Clean 'Color' and 'Rarity' columns
        for col in ["Color", "Rarity"]:
            mtg_data[col] = mtg_data[
                col
            ].str.strip()  # Remove leading/trailing white spaces
            mtg_data[col] = mtg_data[col].replace(
                "", "-"
            )  # Replace empty strings with '-'
            mtg_data[col] = mtg_data[col].fillna("-")  # Replace NaN values with '-'

        # Update the table with the new data
        update_table(mtg_data)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        # Optionally, load a default dataset or show an error message
        tk.messagebox.showerror("Error", f"File not found: {file_path}")
        # Another option would be to use the default dataset to load it here
        # e.g., load_data_from_file("path_to_default_dataset.csv")


# Event handler for color selection
def on_color_selected(event):
    selected_color = color_selection_var.get()
    if selected_color != "All Colors":
        combo_values = color_combinations.get(selected_color, [])
        color_combo_combobox["values"] = combo_values
        color_combo_combobox.set("")  # Clear the default selection
        color_combo_combobox["state"] = "readonly"  # Enable the combobox
        # Update title for single color selection
        # title_label.config(text="Showing Overall Data")
    else:
        color_combo_combobox["values"] = []
        color_combo_combobox.set("")  # Clear any existing value
        color_combo_combobox["state"] = "disabled"  # Disable the combobox
        # Update title for no selection
        # title_label.config(text="Showing Overall Data")

    update_title(selected_color)  # Update the title with the selected color's win rate

    combo_file_path = os.path.join(data_dir, "card-ratings-2023-11-20.csv")
    load_data_from_file(combo_file_path)
    update_table(mtg_data)

    dynamic_search(None)  # Trigger the search


# Bind the color selection combobox to the event handler
color_selection_combobox.bind("<<ComboboxSelected>>", on_color_selected)


def on_color_combo_selected(event):
    selected_combo_code = color_combo_var.get()
    selected_combo_name = color_code_to_name.get(selected_combo_code, None)

    if selected_combo_name:
        combo_file_path = os.path.join(
            data_dir, f"card-ratings-2023-11-20({selected_combo_code}).csv"
        )
        load_data_from_file(combo_file_path)
    else:
        print("Data Not Found (Color Combination)")

    update_title(
        selected_combo_code
    )  # Update the title with the selected combination's win rate

    update_table(mtg_data)


# Bind the color combination combobox to the dynamic search (modify as needed)
color_combo_combobox.bind("<<ComboboxSelected>>", on_color_combo_selected)


#######################################################
# GUI SETUP - TREEVIEW FOR CARD DATA
#######################################################

# Frame for Treeview and Scrollbar
tree_frame = ttk.Frame(tab1)
tree_frame.pack(pady=20, expand=True, fill="both")

# Treeview setup
columns = [
    "Card Name",
    "Avg. Pick Turn",
    "Color",
    "Rarity",
    "Games Played %",
    "WinRate In Hand (%)",
    " (% WR H - % WR not H)",
]
tree = ttk.Treeview(tree_frame, columns=columns, show="headings")

# Set column properties and assign sorting functions with initial sorting order
for col in columns:
    if col != "Name":
        tree.column(col, anchor="center")  # Center-align the column contents
    if col in ["Color", "Rarity", "Name"]:
        tree.heading(
            col,
            text=col,
            anchor="center",
            command=lambda c=col: treeview_sort_column_alphabetic(tree, c, False),
        )
    else:
        tree.heading(
            col,
            text=col,
            anchor="center",
            command=lambda c=col: treeview_sort_column(tree, c, False),
        )


# Scrollbar setup
scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
tree.configure(yscrollcommand=scrollbar.set)
tree.pack(side=tk.LEFT, fill="both", expand=True)

# Initially displaying all data
update_table(mtg_data)
update_title()  # Initialize the title with overall stats


#######################################################
# GUI SETUP - TREEVIEW FOR TWO-COLOR WIN RATES
#######################################################

# Frame for the Two-Color Winrates Treeview
two_color_winrates_frame = ttk.Frame(tab2)
two_color_winrates_frame.pack(pady=10, expand=True, fill="both")

# Treeview for Two-Color Winrates
two_color_columns = ["Name (Colors)", "Win Rate"]
two_color_tree = ttk.Treeview(
    two_color_winrates_frame, columns=two_color_columns, show="headings", height=10
)  # Set height to limit the number of rows displayed

# Define the two-color combinations you want to include
two_color_combinations = [
    "Azorius (WU)",
    "Dimir (UB)",
    "Rakdos (BR)",
    "Gruul (RG)",
    "Selesnya (GW)",
    "Orzhov (WB)",
    "Golgari (BG)",
    "Simic (GU)",
    "Izzet (UR)",
    "Boros (RW)",
]

# Filter out only the specific two-color combinations
two_color_data = mtg_data_colors[mtg_data_colors["Color"].isin(two_color_combinations)]

# Extract the relevant columns
two_color_winrates = two_color_data[["Color", "Win Rate"]].copy()

# Define the column headings and add the data
for col in two_color_columns:
    two_color_tree.heading(
        col,
        text=col,
        anchor="center",
        command=lambda c=col: treeview_sort_column_alphabetic(two_color_tree, c, False),
    )
    two_color_tree.column(
        col,
        anchor="center",
        width=100,
    )

# Populate the Treeview with the two-color data
for index, row in two_color_winrates.iterrows():
    # Insert the data as is, assuming 'Win Rate' is already a string like '59.60%'
    two_color_tree.insert("", "end", values=(row["Color"], row["Win Rate"]))

two_color_tree.pack()


#######################################################
# MAIN EVENT LOOP
#######################################################

root.mainloop()
