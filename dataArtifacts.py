import os
import tkinter as tk
from tkinter import filedialog,messagebox

class DataArtifactsAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Artifacts Analyzer")
        
        # UI elements
        self.directory_path_label = tk.Label(root, text="Select a directory:")
        self.directory_path_label.pack()

        self.directory_path_entry = tk.Entry(root, width=50)
        self.directory_path_entry.pack()

        self.open_directory_button = tk.Button(root, text="Open Directory", command=self.open_directory_dialog)
        self.open_directory_button.pack()

        self.artifact_categories = ["Files", "Internet History", "Chat Logs", "Emails", "System Logs"]
        self.category_var = tk.StringVar(value=self.artifact_categories[0])

        self.category_menu = tk.OptionMenu(root, self.category_var, *self.artifact_categories)
        self.category_menu.pack()

        self.analyze_button = tk.Button(root, text="Analyze", command=self.analyze_directory)
        self.analyze_button.pack()

        self.artifact_listbox = tk.Listbox(root, width=80, height=15)
        self.artifact_listbox.pack()

    def open_directory_dialog(self):
        selected_directory = filedialog.askdirectory()
        if selected_directory:
            self.directory_path_entry.delete(0, tk.END)
            self.directory_path_entry.insert(0, selected_directory)

    def analyze_directory(self):
        selected_category = self.category_var.get()
        directory_path = self.directory_path_entry.get()

        # Implement your artifact analysis logic based on the selected category
        artifacts = self.get_artifacts(selected_category, directory_path)

        self.artifact_listbox.delete(0, tk.END)
        for artifact in artifacts:
            self.artifact_listbox.insert(tk.END, artifact)

    def get_artifacts(self, category, directory_path):
        # Implement artifact analysis logic based on the selected category
        # Return a list of artifacts
        
        # Example for the "Files" category
        if category == "Files":
            artifacts = os.listdir(directory_path)
            return artifacts

        # Implement analysis for other categories here

        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = DataArtifactsAnalyzer(root)
    root.mainloop()
