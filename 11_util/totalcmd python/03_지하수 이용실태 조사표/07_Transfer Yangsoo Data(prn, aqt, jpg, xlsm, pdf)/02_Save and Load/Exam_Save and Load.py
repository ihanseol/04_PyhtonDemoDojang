import os
import pickle

# Define the directory to save the file
save_directory = 'c:\\Program Files\\totalcmd\\AqtSolv\\'
os.makedirs(save_directory, exist_ok=True)  # Create the directory if it doesn't exist

# Define the file path
file_path = os.path.join(save_directory, 'SaveFolder.sav')

# Example data to save
# data = {'key': 'value'}
data = "d:\\09_hardRain\\09_ihanseol - 2024\\00_YangSoo File Move TestBed\\04_양수시험\\"


# Save the data to the file
with open(file_path, 'wb') as file:
    pickle.dump(data, file)

print(f'File saved to {file_path}')
