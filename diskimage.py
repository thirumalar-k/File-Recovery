import tkinter as tk
from tkinter import ttk
import subprocess

class DiskImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Imaging")

        self.create_ui()

    def create_ui(self):
        self.source_label = ttk.Label(self.root, text="Source Disk:")
        self.source_label.pack(pady=10)

        self.source_entry = ttk.Entry(self.root)
        self.source_entry.pack(pady=5)

        self.output_label = ttk.Label(self.root, text="Output File:")
        self.output_label.pack(pady=10)

        self.output_entry = ttk.Entry(self.root)
        self.output_entry.pack(pady=5)

        self.create_image_button = ttk.Button(self.root, text="Create Image", command=self.create_image)
        self.create_image_button.pack(pady=5)

        self.log_text = tk.Text(self.root, wrap=tk.WORD, height=20, width=80)
        self.log_text.pack(padx=10, pady=10)

    def create_image(self):
        source_disk = self.source_entry.get()
        output_file = self.output_entry.get()

        if not source_disk or not output_file:
            self.log_text.insert(tk.END, "Please provide source disk and output file paths.\n")
            return

        try:
            command = ["dd", "if=" + source_disk, "of=" + output_file, "bs=4M"]
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            self.log_text.insert(tk.END, result.stdout + "\n")
        except Exception as e:
            self.log_text.insert(tk.END, f"An error occurred: {str(e)}\n")

def main():
    root = tk.Tk()
    app = DiskImageApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
