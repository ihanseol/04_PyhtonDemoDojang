import tkinter as tk
import random
import string
from tkinter import messagebox


def generate_password():
    length = int(length_entry.get())
    use_upper = upper_var.get()
    use_lower = lower_var.get()
    use_digits = digits_var.get()
    use_special = special_var.get()
    avoid_similar = not_similar_var.get()

    characters = ""
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_special:
        characters += "!@#$%^&*()_+-=[]{}|;:',.<>?/"

    if avoid_similar:
        characters = characters.translate(str.maketrans("", "", "1Il0O"))

    if not characters:
        messagebox.showerror("Error", "Please select at least one character set!")
        return

    password = "".join(random.choice(characters) for _ in range(length))
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_entry.get())
    root.update()


# Create main window
root = tk.Tk()
root.title("Random Password Generator")

# Password entry and button
password_label = tk.Label(root, text="Randomly generated password")
password_label.grid(row=0, column=0, columnspan=2, pady=5)

password_entry = tk.Entry(root, width=30)
password_entry.grid(row=1, column=0, padx=5)

copy_button = tk.Button(root, text="Copy", command=copy_to_clipboard)
copy_button.grid(row=1, column=1, padx=5)

# Generate password button
generate_button = tk.Button(root, text="Generate Password", command=generate_password)
generate_button.grid(row=2, column=0, columnspan=2, pady=10)

# Options
options_frame = tk.LabelFrame(root, text="Password Options")
options_frame.grid(row=3, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

upper_var = tk.BooleanVar(value=True)
upper_check = tk.Checkbutton(options_frame, text="Use: ABCDEFGHIJKLMNOPQRSTUVWXYZ", variable=upper_var)
upper_check.grid(row=0, column=0, sticky="w")

lower_var = tk.BooleanVar(value=True)
lower_check = tk.Checkbutton(options_frame, text="Use: abcdefghijklmnopqrstuvwxyz", variable=lower_var)
lower_check.grid(row=1, column=0, sticky="w")

digits_var = tk.BooleanVar(value=True)
digits_check = tk.Checkbutton(options_frame, text="Use: 0123456789", variable=digits_var)
digits_check.grid(row=2, column=0, sticky="w")

special_var = tk.BooleanVar(value=True)
special_check = tk.Checkbutton(options_frame, text="Use: !@#$%^&*()...", variable=special_var)
special_check.grid(row=3, column=0, sticky="w")

not_similar_var = tk.BooleanVar(value=False)
not_similar_check = tk.Checkbutton(options_frame, text="Not use: 1 I l 0 O", variable=not_similar_var)
not_similar_check.grid(row=4, column=0, sticky="w")

# Password length
length_label = tk.Label(root, text="Password Length")
length_label.grid(row=4, column=0, pady=5)

length_entry = tk.Entry(root, width=10)
length_entry.insert(0, "18")
length_entry.grid(row=4, column=1, pady=5)

root.mainloop()
