import os
import hashlib
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext

def calculate_hash(file_path, hash_algorithm='sha256', chunk_size=65536):
    """Calculate hash of a file."""
    hash_obj = hashlib.new(hash_algorithm)
    with open(file_path, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def extract_email_messages(dd_image_path, output_folder):
    """Extract email messages from a DD image and create data artifacts."""
    email_pattern = r'From:\s*(.*?)\nTo:\s*(.*?)\nSubject:\s*(.*?)\n(.*?)(?=\n\n)'
    
    with open(dd_image_path, 'rb') as image_file:
        content = image_file.read().decode(errors='ignore')
        matches = re.findall(email_pattern, content, re.DOTALL)
        
        for index, match in enumerate(matches):
            from_field, to_field, subject, body = match
            artifact_data = {
                'type': 'email',
                'from': from_field,
                'to': to_field,
                'subject': subject,
                'body': body
            }
            artifact_id = f'email_{index}'
            artifact_file_path = os.path.join(output_folder, f'{artifact_id}.txt')
            
            with open(artifact_file_path, 'w') as artifact_file:
                artifact_file.write(f"Artifact ID: {artifact_id}\n")
                for key, value in artifact_data.items():
                    artifact_file.write(f"{key.capitalize()}: {value}\n")
    
    print("Extraction and artifact creation completed.")

def browse_image():
    dd_image_path = filedialog.askopenfilename(filetypes=[("DD Image Files", "*.dd")])
    image_path_entry.delete(0, tk.END)
    image_path_entry.insert(0, dd_image_path)

def select_output_folder():
    output_folder = filedialog.askdirectory()
    output_folder_entry.delete(0, tk.END)
    output_folder_entry.insert(0, output_folder)

def extract_and_save():
    dd_image_path = image_path_entry.get().strip('"')
    output_folder = output_folder_entry.get()
    
    if not dd_image_path or not output_folder:
        result_text.config(state=tk.NORMAL)
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, "Please select a disk image and output folder.")
        result_text.config(state=tk.DISABLED)
        return
    
    extract_email_messages(dd_image_path, output_folder)
    
    result_text.config(state=tk.NORMAL)
    result_text.delete('1.0', tk.END)
    result_text.insert(tk.END, "Extraction and artifact creation completed.")
    result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Email Message Extraction Tool")
    
    label = tk.Label(root, text="Email Message Extraction Tool")
    label.pack(pady=10)
    
    image_path_label = tk.Label(root, text="DD Image Path:")
    image_path_label.pack()
    image_path_entry = tk.Entry(root)
    image_path_entry.pack(fill=tk.X, padx=10)
    browse_button = tk.Button(root, text="Browse", command=browse_image)
    browse_button.pack(pady=5)
    
    output_folder_label = tk.Label(root, text="Output Folder:")
    output_folder_label.pack()
    output_folder_entry = tk.Entry(root)
    output_folder_entry.pack(fill=tk.X, padx=10)
    output_folder_button = tk.Button(root, text="Select Folder", command=select_output_folder)
    output_folder_button.pack(pady=5)
    
    extract_button = tk.Button(root, text="Extract and Save Artifacts", command=extract_and_save)
    extract_button.pack(pady=10)
    
    result_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=50, height=10)
    result_text.pack(padx=10, pady=5)
    result_text.config(state=tk.DISABLED)
    
    root.mainloop()
