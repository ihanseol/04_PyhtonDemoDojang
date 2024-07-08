import os
import pickle

# Define the directory to load the file from
load_directory = 'c:\\Program Files\\totalcmd\\AqtSolv\\'

# Define the file path
file_path = os.path.join(load_directory, 'SaveFolder.sav')

# Load the data from the file
with open(file_path, 'rb') as file:
    loaded_data = pickle.load(file)

print(f'File loaded from {file_path}')
print(f'Data: {loaded_data}')
