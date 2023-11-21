import tkinter as tk
from tkinter import filedialog
import re


def read_log_file():
    # Use the file path from the entry widget
    file_path = file_path_entry.get()
    try:
        with open(file_path, "r") as file:
            log_data = file.read()
            username = extract_username(log_data)
            username_label.config(text="Username: " + username)
    except Exception as e:
        username_label.config(text="Error: " + str(e))

    # Schedule this function to run again after 2000 milliseconds
    root.after(2000, read_log_file)


def extract_username(log_text):
    matches = re.findall(
        r"\[Accounts - Login\] Logged in successfully. Display Name: (.+?#\d+)",
        log_text,
    )
    return matches[-1] if matches else "Not found"


# Create the main window
root = tk.Tk()
root.title("Log Reader")

# Default file path
default_file_path = (
    "C:\\Users\\LFVAR\\AppData\\LocalLow\\Wizards Of The Coast\\MTGA\\Player.log"
)

# Create the Entry widget with a default value
file_path_entry = tk.Entry(root, width=100)
file_path_entry.insert(0, default_file_path)
file_path_entry.pack()

# Create a label to display the username
username_label = tk.Label(root, text="Username: ")
username_label.pack()

# Initial call to start the update process
root.after(2000, read_log_file)

# Run the application
root.mainloop()
