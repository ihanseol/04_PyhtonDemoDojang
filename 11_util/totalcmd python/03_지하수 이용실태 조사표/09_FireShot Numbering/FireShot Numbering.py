import os
import re
import tkinter as tk
from tkinter import messagebox
import natsort


def rename_files():
    directory = r'D:\05_Send'
    extension = '.pdf'
    files = [f for f in os.listdir(directory) if f.endswith(extension)]
    files = natsort.natsorted(files)
    start_number = int(entry.get())
    for i, file in enumerate(files):
        filename, file_extension = os.path.splitext(file)
        parts = filename.split(' - ')

        if remove_header_var.get():
            new_filename = f'{str(start_number + i).zfill(3)} - {parts[1]}{file_extension}'
        else:
            new_filename = f'FireShot Capture {str(start_number + i).zfill(3)} - {parts[1]}{file_extension}'

        os.rename(os.path.join(directory, file), os.path.join(directory, new_filename))
    messagebox.showinfo("Success", "Files renamed successfully!")


root = tk.Tk()
root.title("Fire Shot PDF File Renamer")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Set the window size
window_width = 380
window_height = 160
remove_header_var = tk.BooleanVar()

# Calculate the x and y coordinates to center the window
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

# Set the window geometry
root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

main_frame = tk.Frame(root)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

label = tk.Label(main_frame, text="Enter the starting number:", font=("Arial", 10))
label.pack(pady=5)

entry = tk.Entry(main_frame, font=("Arial", 12), width=20)
entry.pack(pady=5)

# 체크박스
checkbox = tk.Checkbutton(main_frame, text="Remove Header", variable=remove_header_var, font=("Arial", 10))
checkbox.pack(pady=5)

button = tk.Button(main_frame, text="   Rename Files   ", command=rename_files, font=("Arial", 10))
button.pack(pady=7)

root.mainloop()
