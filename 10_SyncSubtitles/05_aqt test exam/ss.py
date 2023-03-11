import os
import subprocess
import pyautogui

# Define the path to the AQTW32.EXE program
program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'

# Define the path to the file you want to open
filename = 'w1_02_long.aqt'
file_path = os.path.abspath(filename)

# Start the program using subprocess
subprocess.Popen([program_path, file_path])

# Wait for the program to open
pyautogui.sleep(2)

# Get the active window handle
window_handle = pyautogui.getActiveWindow()

# Get the position and size of the program window
window_rect = pyautogui.getWindowRect(window_handle)

# Move the window to the desired monitor (in this case, the main monitor)
if window_rect.left < 0 or window_rect.top < 0:
    pyautogui.moveWindow(window_handle, 0, 0)
