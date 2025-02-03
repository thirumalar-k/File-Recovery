import os
import tkinter as tk
from tkinter import filedialog

def deep_scan_drive(drive_letter):
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, f"Scanning drive {drive_letter}...\n\n")

    for root, dirs, files in os.walk(drive_letter + ":\\"):
        for file in files:
            file_path = os.path.join(root, file)
            result_text.insert(tk.END, "Found: " + file_path + "\n")
    
    result_text.config(state=tk.DISABLED)

def on_button_pressed():
    drive_letter = drive_entry.get()
    deep_scan_drive(drive_letter)

# Create the main window
root = tk.Tk()
root.title("Drive Scanner")

# Create UI elements
drive_label = tk.Label(root, text="Enter drive letter to scan (e.g., C):")
drive_label.pack()

drive_entry = tk.Entry(root)
drive_entry.pack()

scan_button = tk.Button(root, text="Scan Drive", command=on_button_pressed)
scan_button.pack()

result_text = tk.Text(root, wrap=tk.WORD, state=tk.DISABLED)
result_text.pack()

quit_button = tk.Button(root, text="Quit", command=root.quit)
quit_button.pack()

# Start the main event loop
root.mainloop()

