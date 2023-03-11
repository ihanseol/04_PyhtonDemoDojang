import os
import pyautogui
import time

# Define the path to the AQTW32.EXE program
program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'

# Define the path to the file you want to open
filename = 'w1_02_long.aqt'
file_path = os.path.abspath(filename)

# Open the AQTW32.EXE program on the primary display
os.startfile(program_path)

# Wait for the program to open
time.sleep(2)

# Get the handle of the AQTW32.EXE window
# window_handle = pyautogui.getWindowsWithTitle('AQTW32.EXE')[0].handle
# window_handle = pyautogui.getWindowsWithTitle('AQTW32')[0].handle
# window_handle = pyautogui.getWindowsWithTitle('*AQTW32*')[0].handle

windows = pyautogui.getAllWindows()
for window in windows:
    if window.className == 'AQTW32':
        window_handle = window.handle
        break



# Get the rectangle of the AQTW32.EXE window
window_rect = pyautogui.getWindow(window_handle)

# Calculate the position of the window on the primary display
program_region = (window_rect.left, window_rect.top, window_rect.width, window_rect.height)

# Open the file
pyautogui.hotkey('ctrl', 'o')
pyautogui.typewrite(file_path)
pyautogui.press('enter')

# Wait for the file to open
time.sleep(2)

# Refresh the view
pyautogui.hotkey('alt', 'v')
pyautogui.press('r')

# Wait for the view to refresh
time.sleep(2)

# Find the maximize button on the screen
maximize_image = r'd:\05_Send\maximize.png'
maximize_pos = pyautogui.locateOnScreen(maximize_image, region=program_region)

if maximize_pos is not None:
    # If the button is found, get its center coordinates
    maximize_center = pyautogui.center(maximize_pos)
    # Click the center of the button
    pyautogui.click(maximize_center)
else:
    # If the button is not found, print an error message
    print(f"Maximize button ({maximize_image}) not found on screen.")
