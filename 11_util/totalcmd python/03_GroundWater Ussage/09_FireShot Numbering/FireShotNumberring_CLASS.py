import os
import tkinter as tk
from tkinter import messagebox, filedialog
import natsort


class PDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FireShot PDF File Renamer")

        # Get the screen width and height
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Set the window size
        window_width = 380
        window_height = 180
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)

        # Set the window geometry
        self.root.geometry(f"{window_width}x{window_height}+{int(x)}+{int(y)}")

        self.directory = None
        self.remove_header_var = tk.BooleanVar()

        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets."""
        main_frame = tk.Frame(self.root)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        label = tk.Label(main_frame, text="Enter the starting number:", font=("Arial", 10))
        label.pack(pady=3)

        self.entry = tk.Entry(main_frame, font=("Arial", 12), width=20)
        self.entry.pack(pady=3)

        # Checkbox for header removal
        checkbox = tk.Checkbutton(main_frame, text="Remove Header", variable=self.remove_header_var, font=("Arial", 10))
        checkbox.pack(pady=3)

        # Button to select directory
        dir_button = tk.Button(main_frame, text=" Select Directory ", command=self.select_directory, font=("Arial", 10))
        # dir_button.pack(pady=1)
        dir_button.pack(side="left", padx=5)

        # Button to rename files
        rename_button = tk.Button(main_frame, text="  Rename Files  ", command=self.rename_files, font=("Arial", 10))
        # rename_button.pack(pady=3)
        rename_button.pack(side="left", padx=5)

    def select_directory(self):
        """Open a file dialog to select a directory."""
        self.directory = filedialog.askdirectory(title="Select Directory")
        if not self.directory:
            messagebox.showerror("Error", "No directory selected!")

    def rename_files(self):
        """Rename files in the selected directory."""
        if not self.directory:
            # messagebox.showerror("Error", "Please select a directory first!")
            # return
            self.directory = "d:\\05_Send"

        try:
            start_number = int(self.entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid starting number!")
            return

        extension = '.pdf'
        files = [f for f in os.listdir(self.directory) if f.endswith(extension)]
        files = natsort.natsorted(files)

        if not files:
            messagebox.showerror("Error", "No PDF files found in the selected directory!")
            return

        for i, file in enumerate(files):
            filename, file_extension = os.path.splitext(file)
            parts = filename.split(' - ')

            if len(parts) < 2:
                messagebox.showwarning("Warning", f"File {file} does not match the expected format. Skipping.")
                continue

            if self.remove_header_var.get():
                new_filename = f'{str(start_number + i).zfill(3)} - {parts[1]}{file_extension}'
            else:
                new_filename = f'FireShot Capture {str(start_number + i).zfill(3)} - {parts[1]}{file_extension}'

            try:
                os.rename(os.path.join(self.directory, file), os.path.join(self.directory, new_filename))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to rename {file}: {e}")
                return

        messagebox.showinfo("Success", "Files renamed successfully!")


if __name__ == "__main__":
    root = tk.Tk()
    app = PDFRenamerApp(root)
    root.mainloop()
