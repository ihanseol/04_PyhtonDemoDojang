import os

# Get the starting number from the console input
start_number = int(input("Enter the starting number: "))

# Get the current directory
current_dir = os.getcwd()

# Loop through the files in the directory
for filename in os.listdir(current_dir):
    # Check if the filename is a file (not a directory)
    if os.path.isfile(os.path.join(current_dir, filename)):
        # Construct the new filename with a file number
        new_filename = f'{start_number} - {filename}'
        # Increment the file number
        start_number += 1
        # Rename the file
        os.rename(os.path.join(current_dir, filename), os.path.join(current_dir, new_filename))
