import os
from datetime import datetime

def get_last_filename():
    download_folder = os.path.expanduser("~\\Downloads\\")
    # Get a list of all files in the directory
    files = os.listdir(download_folder)

    # Filter out only files (not directories)
    files = [f for f in files if os.path.isfile(os.path.join(download_folder, f))]

    # Get the most recently modified file
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(download_folder, f)))

    return latest_file


def change_filename_bydate(old_filename):
    current_date = datetime.now().strftime("%Y-%m-%d")
    new_filename = f'example_{current_date}.txt'
    os.rename(old_filename, new_filename)

    print(f"The file '{old_filename}' has been renamed to '{new_filename}'.")


print(f"The latest file in the download folder is: {get_last_filename()}")


