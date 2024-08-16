import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageOps


def convert_to_coloring_book(image_path, dpi):
    # Load the image
    image = Image.open(image_path)

    # Convert the image to grayscale
    gray_image = ImageOps.grayscale(image)

    # Increase contrast
    high_contrast_image = ImageOps.autocontrast(gray_image, cutoff=2)

    # Apply a binary threshold to create a coloring book effect
    threshold_image = high_contrast_image.point(lambda p: p > 128 and 255)

    # Set DPI and save the image
    output_path = f"{image_path.rsplit('.', 1)[0]}_converted.jpg"
    threshold_image.save(output_path, dpi=(dpi, dpi))

    messagebox.showinfo("Success", f"Image saved as: {output_path}")


def open_file():
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.jpeg;*.bmp;*.gif")])
    if filepath:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, filepath)


def on_convert():
    image_path = file_entry.get()
    dpi = dpi_entry.get()

    if not image_path:
        messagebox.showwarning("Input Error", "Please select an image file.")
        return

    try:
        dpi_value = int(dpi) if dpi else 300
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for DPI.")
        return

    convert_to_coloring_book(image_path, dpi_value)


# Create the main application window
root = tk.Tk()
root.title("Image to Coloring Book Converter")

# File selection
tk.Label(root, text="Select Image File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
file_entry = tk.Entry(root, width=40)
file_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=open_file).grid(row=0, column=2, padx=10, pady=5)

# DPI input
tk.Label(root, text="DPI (Optional):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
dpi_entry = tk.Entry(root, width=40)
dpi_entry.grid(row=1, column=1, padx=10, pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=on_convert)
convert_button.grid(row=2, column=1, pady=10)

# Start the application
root.mainloop()
