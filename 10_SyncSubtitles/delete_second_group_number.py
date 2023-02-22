import os
import re

# Get the current directory
current_dir = os.getcwd()

# Loop through the files in the directory
for filename in os.listdir(current_dir):
    # Check if the filename is a file (not a directory)
    if os.path.isfile(os.path.join(current_dir, filename)):
        # Use regular expressions to extract the desired output filename
        match = re.search(r'(\d{4}) - (\d{4}) (.+)', filename)
        if match:
            number = match.group(1)
            name = match.group(3)
            new_filename = f'{number} - {name}'
            # Rename the file
            os.rename(os.path.join(current_dir, filename), os.path.join(current_dir, new_filename))