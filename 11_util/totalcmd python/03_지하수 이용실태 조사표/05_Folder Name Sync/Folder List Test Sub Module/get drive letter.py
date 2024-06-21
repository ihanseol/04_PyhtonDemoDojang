import os

def get_drive_letter(path):
    drive, _ = os.path.splitdrive(path)
    return drive

# Example usage:
path = r'C:\Users\Example\Documents\file.txt'
drive_letter = get_drive_letter(path)
print(f"Drive letter: {drive_letter}")
