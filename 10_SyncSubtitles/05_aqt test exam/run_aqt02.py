import os
import pyautogui
import time

# Define the path to the AQTW32.EXE program
program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'

# Define the path to the file you want to open
filename = 'w1_02_long.aqt'
file_path = os.path.abspath(filename)

# Open the AQTW32.EXE program
os.startfile(program_path)

# Wait for the program to open
time.sleep(2)

# Press Alt+F to open the File menu
pyautogui.hotkey('ctrl', 'o')

# Wait for the Open dialog to appear
time.sleep(2)

# Type the path to the file and press Enter
pyautogui.typewrite(file_path)
pyautogui.press('enter')

# Wait for the file to open
time.sleep(2)

# Press Alt+V to open the View menu
pyautogui.hotkey('alt', 'v')

# Press R to refresh the view
pyautogui.press('r')

# Wait for the view to refresh
time.sleep(2)

# Find the maximize button on the screen
# maximize_image = r'd:\05_Send\maximize.png'
# maximize_pos = pyautogui.locateOnScreen(maximize_image)
maximize_pos = pyautogui.locateOnScreen(r'd:\05_Send\maximize.png', region=(2560, 0, 2560, 1440))

if maximize_pos is not None:
    # If the button is found, get its center coordinates
    maximize_center = pyautogui.center(maximize_pos)
    # Click the center of the button
    pyautogui.click(maximize_center)
else:
    # If the button is not found, print an error message
    print(f"Maximize button ({maximize_image}) not found on screen.")



