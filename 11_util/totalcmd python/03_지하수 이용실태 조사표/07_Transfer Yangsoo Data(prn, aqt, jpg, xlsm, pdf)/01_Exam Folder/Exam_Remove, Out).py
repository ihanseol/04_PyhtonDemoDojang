import os

# Define the directory containing the files
directory = '/path/to/your/files'

# Loop through each file in the directory
for filename in os.listdir(directory):
    # Check if the filename starts with 'out_'
    if filename.startswith('out_'):
        # Create the new filename by removing 'out_'
        new_filename = filename[4:]
        # Construct the full old and new file paths
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)
        # Rename the file
        os.rename(old_file, new_file)
        print(f'Renamed: {filename} -> {new_filename}')
