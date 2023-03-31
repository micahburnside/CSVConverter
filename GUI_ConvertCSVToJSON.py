import tkinter as tk
from tkinter import filedialog
import csv
import json
import os

root = tk.Tk()
root.title("CSV to JSON Converter")

# Set initial width of GUI to 400
root.geometry("400x200")

file_path = ""

# Function to handle file selection
def choose_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    label_file_path.config(text="Selected file: " + file_path)
    # Set the width of the GUI to fit the label text
    root.geometry(str(label_file_path.winfo_reqwidth()+20)+"x200")

# Function to handle JSON conversion
def convert_to_json():
    global file_path
    if file_path == "":
        label_file_path.config(text="Please select a CSV file first")
        return
    csv_file_name = os.path.splitext(os.path.basename(file_path))[0]
    output_path = filedialog.askdirectory()
    if not output_path:
        return
    json_file_name = entry_json_file_name.get().strip()
    if not json_file_name:
        json_file_name = csv_file_name + ".json"
    json_file_path = os.path.join(output_path, json_file_name)
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        data = [row for row in csv_reader]
    with open(json_file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)
    label_file_path.config(text="CSV file converted to JSON: " + json_file_path)
    # Set the width of the GUI to fit the label text
    root.geometry(str(label_file_path.winfo_reqwidth()+20)+"x200")

# Create widgets
button_choose_file = tk.Button(root, text="Choose CSV File", command=choose_file)
button_choose_file.pack(pady=10)

label_file_path = tk.Label(root, text="No file selected")
label_file_path.pack(pady=10)

label_json_file_name = tk.Label(root, text="Enter JSON file name (optional):")
label_json_file_name.pack(pady=5)

entry_json_file_name = tk.Entry(root)
entry_json_file_name.pack(pady=5)

button_convert_to_json = tk.Button(root, text="Convert to JSON", command=convert_to_json)
button_convert_to_json.pack(pady=10)

root.mainloop()
