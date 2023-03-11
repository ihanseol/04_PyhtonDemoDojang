import time
import os
import pyautogui



def open_aqtfile(file_path):
    # file_path = "path/to/my_file.aqt"
    viewer_path = "c:/WHPA/AQTEver3.4(170414)/AQTW32.EXE"

    # Make sure the file exists before trying to open it
    if os.path.exists(file_path):
        # Construct the command to open the viewer with the file as an argument
        cmd = f'"{viewer_path}" "{file_path}"'
        # Use os.system() to execute the command
        os.system(cmd)
    else:
        print("File not found:", file_path)



# # Set the directory where the AQT files are located
# directory = 'd:/05_Send/'

# Get a list of all the .aqt files in the directory
aqt_files = [f for f in os.listdir() if f.endswith('.aqt')]

# Check if there are any .aqt files in the directory
if len(aqt_files) == 0:
    print('No .aqt files found in directory.')
else:
    # Print the name of the first .aqt file
    filename = aqt_files[0]
    print('Opening file:', filename)

    # Get the absolute file path
    file_path = os.path.abspath(os.path.join(directory, filename))
    open_aqtfile(file_path)









