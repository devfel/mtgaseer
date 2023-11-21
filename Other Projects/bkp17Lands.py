import tkinter as tk
from tkinter import ttk
from tkinter.font import Font
import pandas as pd
import math


# Load your data
file_path = "C:\\Users\\LFVAR\\Downloads\\card-ratings-2023-11-20.csv"
mtg_data = pd.read_csv(file_path)

# List of columns with percentage values
percentage_columns = ["GNS WR", "GIH WR", "GD WR", "OH WR", "GP WR", "% GP"]

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


# List of columns where NaN values should be replaced with '-'
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

# Replace NaN values with '-' in the specified columns
for col in nan_replacement_columns:
    mtg_data[col] = mtg_data[col].fillna("-")


# Clean 'Color' and 'Rarity' columns for leading/trailing spaces and missing values
for col in ["Color", "Rarity"]:
    mtg_data[col] = mtg_data[col].str.strip()  # Remove leading/trailing white spaces
    mtg_data[col] = mtg_data[col].replace("", "-")  # Replace empty strings with '-'
    mtg_data[col] = mtg_data[col].fillna("-")  # Replace NaN values with '-'


# Dynamic search function
def dynamic_search(event):
    search_query = search_var.get()
    filter_data(search_query)


# Filter data function
def filter_data(search_query):
    filtered_data = mtg_data[
        mtg_data["Name"].str.contains(search_query, case=False, na=False)
    ]
    update_table(filtered_data)


# Update table function
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


# Setting up the main window
root = tk.Tk()
root.title("MTG Cards Data")
root.configure(background="white")

# Styling
style = ttk.Style()
style.configure("Treeview", font=("Helvetica", 10))
style.configure("Treeview.Heading", font=("Helvetica", 8, "bold"))

# Frame for Search Widgets
search_frame = ttk.Frame(root)
search_frame.pack(pady=10)

# Search field label
search_label = tk.Label(search_frame, text="Search Card:", font=("Helvetica", 12))
search_label.pack(side=tk.LEFT, padx=(0, 10))  # Add some padding for spacing

# Search field entry
search_var = tk.StringVar()
search_entry = tk.Entry(search_frame, textvariable=search_var, font=("Helvetica", 10))
search_entry.pack(side=tk.LEFT)
search_entry.bind("<KeyRelease>", dynamic_search)

# Frame for Treeview and Scrollbar
tree_frame = ttk.Frame(root)
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

root.mainloop()


# [ ] TODO: Search has to be dinamic (when I type it search)
# [ ] TODO: Columns have to be Sortable
# [ ] TODO: Search Button Not Necessary
# [ ] TODO: Postion Has to be Fixed, it is a number based on the GIH WR
# [ ] TODO: IWD Column has to be added
# [ ] TODO: Rarity Column has to be added
# [ ] TODO: Color Column has to be added
# [ ] TODO: The columns title not correspond to the data

# [ ] TODO: make styling better
# [ ] TODO: Do second phase with colors (select color and check % Win Rate of Combinations)
# Roll Bar
# IWD Sorting is bugged
# Better size for columns, make it centralized.


# Add Filter by Color (Actually is the Choosen one and change the Data)
# Add Filter by Rarity
