import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import random
import string
import pyperclip


def generate_password():
    """Generates a random password based on selected options."""

    length = int(password_length_spinbox.get())
    characters = ""

    if use_uppercase_var.get():
        characters += string.ascii_uppercase

    if use_lowercase_var.get():
        characters += string.ascii_lowercase

    if use_digits_var.get():
        characters += string.digits

    if use_symbols_var.get():
        characters += "!#$%_()*+-/<>=?@₩^~"

    if use_symbolsone_var.get():
        characters += "!#$@!@^^&&&=%_@*=?^@"

    if exclude_chars_entry_var.get():
        exclude_chars_str = "1IiLl|!0Oo"
    else:
        exclude_chars_str = ""

    final_chars = ""
    for char in characters:
        if char not in exclude_chars_str:
            final_chars += char

    if not final_chars:
        password_entry.delete(0, tk.END)
        password_entry.insert(0, "선택된 문자 유형이 없습니다.")  # No character type selected
        return

    password = ''.join(random.choice(final_chars) for i in range(length))

    # Moved line to ensure password_entry is ready
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    # password_entry.config(state='normal')  # Set to read-only after creation

    # messagebox.showinfo("Title", password)
    return password


def copy_password():
    """Copies the generated password to the clipboard."""
    password_to_copy = password_entry.get()
    if password_to_copy:
        pyperclip.copy(password_to_copy)


def generate_and_copy():
    """Generates password and copies it to clipboard."""
    generate_password()
    copy_password()


root = tk.Tk()
root.title(" Random Password Generator for My v1.1")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = 480
window_height = 300

# Calculate the x and y coordinates to center the window
x = (screen_width / 2) - (window_width / 2)
y = (screen_height / 2) - (window_height / 2)

# Frame for password display
password_frame = ttk.Frame(root, padding=10)
password_frame.pack(fill=tk.X)

password_label = ttk.Label(password_frame, text="Random PassWord :")
password_label.pack(side=tk.LEFT)

password_entry = ttk.Entry(password_frame, width=30)
password_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
password_entry.config(state='normal')  # Initially read-only

# copy_button_image = tk.PhotoImage(file="clipboard.png")
# You need to create or find a clipboard icon and save it as clipboard.png in the same directory
# If you don't have clipboard.png, you can comment out image part and just use text="Copy"
# copy_button = ttk.Button(password_frame, image=copy_button_image, command=copy_password)
copy_button = ttk.Button(password_frame, text="Copy", command=copy_password)  # Text-based copy button if no image
copy_button.pack(side=tk.LEFT, padx=5)

# Frame for buttons
button_frame = ttk.Frame(root, padding=5)
button_frame.pack(fill=tk.X)

generate_button = ttk.Button(button_frame, text="Generate Password And Copy", command=generate_and_copy)
generate_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

menu_button = ttk.Button(button_frame, text="Menu")  # Menu button - functionality can be added later
menu_button.pack(side=tk.LEFT, padx=5)

# Frame for Password Options
options_frame = ttk.Frame(root, padding=10)
options_frame.pack(fill=tk.X)

options_label = ttk.Label(options_frame, text="Password Options", font=('TkDefaultFont', 10, 'bold'))
options_label.pack(anchor=tk.W)

# Checkboxes for character sets
use_uppercase_var = tk.BooleanVar(value=True)
use_uppercase_check = ttk.Checkbutton(options_frame, text="Use: ABCDEFGHIJKLMNOPQRSTUVWXYZ", variable=use_uppercase_var)
use_uppercase_check.pack(anchor=tk.W)

use_lowercase_var = tk.BooleanVar(value=True)
use_lowercase_check = ttk.Checkbutton(options_frame, text="Use: abcdefghijklmnopqrstuvwxyz", variable=use_lowercase_var)
use_lowercase_check.pack(anchor=tk.W)

use_digits_var = tk.BooleanVar(value=True)
use_digits_check = ttk.Checkbutton(options_frame, text="Use: 0123456789", variable=use_digits_var)
use_digits_check.pack(anchor=tk.W)

use_symbols_var = tk.BooleanVar(value=False)  # Default to False as in the image
use_symbols_check = ttk.Checkbutton(options_frame, text="Use: ! # $ % _ ( ) * + - / < > = ? @ ₩ ^ ~",
                                    variable=use_symbols_var)
use_symbols_check.pack(anchor=tk.W)

use_symbolsone_var = tk.BooleanVar(value=False)  # Default to False as in the image
use_symbolsone_check = ttk.Checkbutton(options_frame, text="Use: ! # $ % _ * = ? ^ @", variable=use_symbolsone_var)
use_symbolsone_check.pack(anchor=tk.W)

not_use_frame = ttk.Frame(options_frame)  # Frame for "Not Use" to align label and entry
not_use_frame.pack(anchor=tk.W, fill=tk.X)

exclude_chars_entry_var = tk.BooleanVar(value=True)
notuse_digits_check = ttk.Checkbutton(options_frame, text="Not Use: 1 I i L l | ! 0 O o",
                                      variable=exclude_chars_entry_var)
notuse_digits_check.pack(anchor=tk.W)

# Frame for Password Length
length_frame = ttk.Frame(root, padding=10)
length_frame.pack(fill=tk.X)

length_label = ttk.Label(length_frame, text="Password Length")
length_label.pack(side=tk.LEFT)

password_length_spinbox = tk.Spinbox(length_frame, from_=1, to=100, width=5)  # You can adjust the range
password_length_spinbox.pack(side=tk.LEFT)
password_length_spinbox.delete(0, "end")
password_length_spinbox.insert(0, "18")  # Default length from the image

# Set the window geometry
root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

root.mainloop()
