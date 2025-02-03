import os
import tkinter as tk
from tkinter import filedialog
import subprocess

class DiskImageConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Image Converter")

        self.select_drive_button = tk.Button(self.root, text="Select Drive", command=self.select_drive)
        self.select_drive_button.pack()

        self.convert_dd_button = tk.Button(self.root, text="Convert to DD", command=self.convert_to_dd)
        self.convert_dd_button.pack()

        #self.convert_e01_button = tk.Button(self.root, text="Convert to E01", command=self.convert_to_e01)
        #self.convert_e01_button.pack()

        self.drive_path = None

    def select_drive(self):
        self.drive_path = filedialog.askdirectory(title="Select Drive to Convert")
        if self.drive_path:
            print("Drive selected:", self.drive_path)

    def convert_to_dd(self):
        if self.drive_path:
            dd_output_path = filedialog.asksaveasfilename(defaultextension=".dd", title="Save DD Image As",
                                                          filetypes=[("DD image files", "*.dd"), ("All files", "*.*")])
            if dd_output_path:
                self.create_dd_image(self.drive_path, dd_output_path)
                print("Conversion to DD complete.")

    def convert_to_e01(self):
        if self.drive_path:
            e01_output_path = filedialog.asksaveasfilename(defaultextension=".e01", title="Save E01 Image As",
                                                           filetypes=[("E01 image files", "*.e01"), ("All files", "*.*")])
            if e01_output_path:
                self.create_e01_image(self.drive_path, e01_output_path)
                print("Conversion to E01 complete.")

    def create_dd_image(self, source_path, output_path):
            # Use PowerShell command to create dd image
            cmd = f"Copy-Item -Path '{source_path}\\*' -Destination '{output_path}' -Recurse"
            subprocess.run(["powershell", "-Command", cmd])

    def create_e01_image(self, source_path, output_path):
        # Use FTK Imager command to create E01 image
            cmd = f"Copy-Item -Path '{source_path}\\*' -Destination '{output_path}' -Recurse"

        #cmd = f"ftkimager.exe i {source_path} {output_path}"
            #subprocess.run(cmd, shell=True)
        #subprocess.run([r'C:\Program Files (x86)\AccessData\FTK Imager\FTK Imager.exe', 'args'])


def main():
    root = tk.Tk()
    root.geometry("400x300")
    app = DiskImageConverterApp(root)
    root.mainloop()
    

if __name__ == "__main__":
    main()
