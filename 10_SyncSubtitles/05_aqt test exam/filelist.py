import os

# Define a function to sort the file names in a way that treats Korean characters as regular characters
def sort_key(file_name):
    return ''.join(chr(ord(c)) if ord(c) > 127 else c for c in file_name)

# Get a list of all files in the current working directory
file_list = os.listdir()

# Sort the list of file names using the custom sort key function
sorted_file_list = sorted(file_list, key=sort_key)

# Print the sorted list of file names
for file_name in sorted_file_list:
    print(file_name)
