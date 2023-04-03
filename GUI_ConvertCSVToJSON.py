import tkinter as tk
from tkinter import filedialog
import csv
import json
import os

root = tk.Tk()
root.title("CSV to JSON Converter")

# Set initial width of GUI to 400
root.geometry("400x400")

file_path = ""
rows = []

# Function to handle file selection
def choose_file():
    global file_path, rows
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    with open(file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        rows = next(csv_reader)
        checkbox_frame = tk.Frame(root)
        checkbox_frame.pack(pady=10)
        checkboxes = []
        row_num = 0
        col_num = 0
        for row in rows:
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(checkbox_frame, text=row, variable=var, onvalue=True, offvalue=False)
            checkbox.grid(row=row_num, column=col_num, sticky="w")
            checkboxes.append(var)
            col_num += 1
            if col_num == 5:
                col_num = 0
                row_num += 1
        button_convert_to_json.config(state=tk.DISABLED)
        button_select_fields.config(state=tk.NORMAL, command=lambda: select_fields(checkboxes))

    label_file_path.config(text="Selected file: " + file_path)
    # Set the width of the GUI to fit the label text and checkboxes
    root.update_idletasks()
    root.geometry(str(max(label_file_path.winfo_reqwidth(), checkbox_frame.winfo_reqwidth()) + 20) + "x" + str(root.winfo_reqheight()))

# Function to handle field selection
def select_fields(checkboxes):
    global rows
    selected_fields = []
    for i in range(len(rows)):
        if checkboxes[i].get():
            selected_fields.append(rows[i])
    if len(selected_fields) == 0:
        label_file_path.config(text="Please select at least one field")
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
        csv_reader = csv.DictReader(csv_file, fieldnames=rows)
        data = [row for row in csv_reader]
    selected_data = [{field: row[field] for field in selected_fields} for row in data]
    with open(json_file_path, 'w') as json_file:
        json.dump(selected_data, json_file, indent=4)
    label_file_path.config(text="CSV file converted to JSON: " + json_file_path)
    # Set the width of the GUI to fit the label text and checkboxes
    root.update_idletasks()
    root.geometry(str(max(label_file_path.winfo_reqwidth(), checkbox_frame.winfo_reqwidth()) + 20) + "x" + str(root.winfo_reqheight()))

# Create widgets
button_choose_file = tk.Button(root, text="Choose CSV File", command=choose_file)
button_choose_file.pack(pady=10)

label_file_path = tk.Label(root, text="No file selected")
label_file_path.pack(pady=10)

label_json_file_name = tk.Label(root, text="Enter JSON file name (optional):")
label_json_file_name.pack(pady=5)

entry_json_file_name = tk.Entry(root)
entry_json_file_name.pack(pady=5)

button_select_fields = tk.Button(root, text="Select Fields", command=None, state=tk.DISABLED)
button_select_fields.pack(pady=10)

button_convert_to_json = tk.Button(root, text="Convert to JSON", command=None, state=tk.DISABLED)
button_convert_to_json.pack(pady=10)

root.mainloop()
