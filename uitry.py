import tkinter as tk
from tkinter import filedialog
import os
import subprocess
import psutil
import platform
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QPushButton, QLabel


def recover_all():
    
    def recover_files_from_drive(file_formats):
        drive = drive_entry.get() + ":"
        drive_path = "\\\\.\\" + drive

        with open(drive_path, "rb") as fileD:
            size = 512      # Size of bytes to read
            byte = fileD.read(size) # Read 'size' bytes
            offs = 0       # Offset location
            rcvd = {ext: 0 for ext in file_formats.values()}  # Recovered file ID for each extension

            while byte:
                for signature, ext in file_formats.items():
                    found = byte.find(signature)
                    if found >= 0:
                        print(f'==== Found {ext.upper()} file at location: {hex(found + (size * offs))} ====')
                        # Now let's create a recovered file
                        fileN = open(f"{rcvd[ext]}.{ext}", "wb")
                        fileN.write(byte[found:])
                        while True:
                            byte = fileD.read(size)
                            if not byte:
                                break
                            bfind = byte.find(b'\x00\x00\x01\xB7')  # End of media file
                            if bfind >= 0:
                                fileN.write(byte[:bfind + 4])
                                print(f'==== Wrote {ext.upper()} file to location: {rcvd[ext]}.{ext} ====\n')
                                rcvd[ext] += 1
                                fileN.close()
                                break
                            else:
                                fileN.write(byte)
                byte = fileD.read(size)
                offs += 1

    def browse_drive():
        selected_drive = filedialog.askdirectory(title="Select Drive")
        drive_entry.delete(0, tk.END)
        drive_entry.insert(0, selected_drive[0])

    # Create the main window
    root = tk.Tk()
    root.title("Deleted File Recovery")
    root.geometry("400x200") 
    root.title("AFR - (All Files Recovery) --- All file type")

    # Create UI elements
    drive_label = tk.Label(root, text="Enter drive letter to scan (e.g., C):")
    drive_label.pack()

    drive_entry = tk.Entry(root)
    drive_entry.pack()

    browse_button = tk.Button(root, text="Browse Drive", command=browse_drive)
    browse_button.pack(pady=10)

    file_formats = {
        b'\xFF\xD8\xFF\xE0': "jpg",  # JPEG format
        b'\x89\x50\x4E\x47': "png",  # PNG format
        b'\x52\x49\x46\x46': "avi",  # AVI format
        b'\x66\x74\x79\x70\x6D\x70\x34\x32': "mp4",  # MP4 format
        b'\x49\x44\x33': 'mp3',
        # Add more formats and their signatures here
    }

    recover_button = tk.Button(root, text="Recover Deleted Files", command=lambda: recover_files_from_drive(file_formats))
    recover_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack()



    


def recover_multimedia():
   
    def recover_media_from_drive(media_formats):
        drive = drive_entry.get() + ":"
        drive_path = "\\\\.\\" + drive

        with open(drive_path, "rb") as fileD:
            size = 512      # Size of bytes to read
            byte = fileD.read(size) # Read 'size' bytes
            offs = 0       # Offset location
            rcvd = 0        # Recovered file ID

            while byte:
                for signature, ext in media_formats.items():
                    found = byte.find(signature)
                    if found >= 0:
                        print(f'==== Found {ext.upper()} file at location: {hex(found + (size * offs))} ====')
                        # Now let's create a recovered media file
                        fileN = open(f"{rcvd}.{ext}", "wb")
                        fileN.write(byte[found:])
                        while True:
                            byte = fileD.read(size)
                            if not byte:
                                break
                            bfind = byte.find(b'\x00\x00\x01\xB7')  # End of media file
                            if bfind >= 0:
                                fileN.write(byte[:bfind + 4])
                                print(f'==== Wrote {ext.upper()} file to location: {rcvd}.{ext} ====\n')
                                rcvd += 1
                                fileN.close()
                                break
                            else:
                                fileN.write(byte)
                byte = fileD.read(size)
                offs += 1

    def browse_drive():
        selected_drive = filedialog.askdirectory(title="Select Drive")
        drive_entry.delete(0, tk.END)
        drive_entry.insert(0, selected_drive[0])

    # Create the main window
    root = tk.Tk()
    root.geometry("400x200") 
    root.title("AFR - (All Files Recovery) --- Multimedia")
    

    # Create UI elements
    drive_label = tk.Label(root, text="Enter drive letter to scan (e.g., C):")
    drive_label.pack()

    drive_entry = tk.Entry(root)
    drive_entry.pack()

    browse_button = tk.Button(root, text="Browse Drive", command=browse_drive)
    browse_button.pack(pady=10)

    media_formats = {
        b'\x52\x49\x46\x46': "avi",  # AVI format
        b'\x66\x74\x79\x70\x6D\x70\x34\x32': "mp4",  # MP4 format
        b'\x49\x44\x33': 'mp3',
        # Add more formats and their signatures here
    }

    recover_button = tk.Button(root, text="Recover Deleted Media", command=lambda: recover_media_from_drive(media_formats))
    recover_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack()


def recover_pictures():
    
    def recover_images_from_drive():
        drive = drive_entry.get() + ":"
        drive_path = "\\\\.\\" + drive

        image_formats = [b'\xFF\xD8\xFF\xE0', b'\x89\x50\x4E\x47']  # JPEG and PNG signatures

        with open(drive_path, "rb") as fileD:
            size = 512      # Size of bytes to read
            byte = fileD.read(size) # Read 'size' bytes
            offs = 0       # Offset location
            rcvd = 0        # Recovered file ID

            while byte:
                for signature in image_formats:
                    found = byte.find(signature)
                    if found >= 0:
                        ext = "jpg" if signature == b'\xFF\xD8\xFF\xE0' else "png"
                        print(f'==== Found {ext.upper()} file at location: {hex(found + (size * offs))} ====')
                        # Now let's create a recovered image file
                        fileN = open(f"{rcvd}.{ext}", "wb")
                        fileN.write(byte[found:])
                        while True:
                            byte = fileD.read(size)
                            if not byte:
                                break
                            bfind = byte.find(b'\xFF\xD9')  # End of image file
                            if bfind >= 0:
                                fileN.write(byte[:bfind + 2])
                                print(f'==== Wrote {ext.upper()} file to location: {rcvd}.{ext} ====\n')
                                rcvd += 1
                                fileN.close()
                                break
                            else:
                                fileN.write(byte)
                byte = fileD.read(size)
                offs += 1

    def browse_drive():
        selected_drive = filedialog.askdirectory(title="Select Drive")
        drive_entry.delete(0, tk.END)
        drive_entry.insert(0, selected_drive[0])

    # Create the main window
    root = tk.Tk()
    root.geometry("400x200") 
    root.title("AFR - (All Files Recovery) --- Image")
    

    # Create UI elements
    drive_label = tk.Label(root, text="Enter drive letter to scan (e.g., C):")
    drive_label.pack()

    drive_entry = tk.Entry(root)
    drive_entry.pack()

    browse_button = tk.Button(root, text="Browse Drive", command=browse_drive)
    browse_button.pack(pady=10)

    recover_button = tk.Button(root, text="Recover Deleted Images", command=recover_images_from_drive)
    recover_button.pack(pady=10)

    quit_button = tk.Button(root, text="Quit", command=root.quit)
    quit_button.pack()

    


def recover_documents():
    
    def recover_pdf_from_drive():
        drive = drive_entry.get() + ":"
        drive_path = "\\\\.\\" + drive

        with open(drive_path, "rb") as fileD:
            size = 512      # Size of bytes to read
            byte = fileD.read(size) # Read 'size' bytes
            offs = 0       # Offset location
            drec = False      # Recovery mode
            rcvd = 0        # Recovered file ID

            while byte:
                found = byte.find(b'\x25\x50\x44\x46\x2D')  # PDF signature: %PDF-
                if found >= 0:
                    drec = True
                    print('==== Found PDF at location: ' + str(hex(found + (size * offs))) + ' ====')
                    # Now let's create a recovered file and search for ending signature
                    fileN = open(str(rcvd) + '.pdf', "wb")
                    fileN.write(byte[found:])
                    while drec:
                        byte = fileD.read(size)
                        bfind = byte.find(b'\x25\x25\x45\x4F\x46\x0A')  # %%EOF
                        if bfind >= 0:
                            fileN.write(byte[:bfind + 6])
                            fileD.seek((offs + 1) * size)
                            print('==== Wrote PDF to location: ' + str(rcvd) + '.pdf ====\n')
                            drec = False
                            rcvd += 1
                            fileN.close()
                        else:
                            fileN.write(byte)
                byte = fileD.read(size)
                offs += 1

    def browse_drive():
        selected_drive = filedialog.askdirectory(title="Select Drive")
        drive_entry.delete(0, tk.END)
        drive_entry.insert(0, selected_drive[0])

    # Create the main window
    root1 = tk.Tk()
    root1.geometry("400x200") 
    root1.title("AFR - (All Files Recovery) --- Documents")

    # Create UI elements
    drive_label = tk.Label(root1, text="Enter drive letter to scan (e.g., C):")
    drive_label.pack()

    drive_entry = tk.Entry(root1)
    drive_entry.pack()

    browse_button = tk.Button(root1, text="Browse Drive", command=browse_drive)
    browse_button.pack(pady=10)

    recover_button = tk.Button(root1, text="Recover Deleted PDFs", command=recover_pdf_from_drive)
    recover_button.pack(pady=10)

    quit_button = tk.Button(root1, text="Exit", command=root1.quit)
    quit_button.pack()


def open_task_manager():{
    
    #subprocess.run(["taskmgr"], shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    
    }

# Create the main window

root = tk.Tk()
root.title("AFR - (All File Recover) ")
root.geometry("600x400")  # Set the desired width and height
heading_label = tk.Label(root, text="Recovery Can Be Done Anywhere At Anytime", font=("Helvetica", 14, "bold"))
heading_label.pack(pady=10)

# Create and place a label for showing recovery path
recovery_path_label = tk.Label(root, text="", fg="green")
recovery_path_label.pack(pady=10)



# Create and place widgets
all_doc_button = tk.Button(root, text="All kind of files", command=recover_all)
all_doc_button.pack(pady=10)

media_button = tk.Button(root, text="Multimedia", command=recover_multimedia)
media_button.pack(pady=10)

video_button = tk.Button(root, text="Pictures", command=recover_pictures)
video_button.pack(pady=10)

doc_button = tk.Button(root, text="Documents", command=recover_documents)
doc_button.pack(pady=10)

#system_analysis_button = tk.Button(root, text="System Analysis", command=open_task_manager)
#system_analysis_button.pack(pady=10)

exit_button = tk.Button(root, text="Exit", command=root.quit)
exit_button.pack(pady=20)

recovery_label = tk.Label(root, text="", fg="black")
recovery_label.pack(pady=10)


# Start the GUI event loop
root.mainloop()
