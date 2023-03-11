import os
import pyautogui
import time
import pygetwindow

# Define the path to the AQTW32.EXE program
program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'

# Open the AQTW32.EXE program
os.startfile(program_path)

# Wait for the program to open
time.sleep(2)

# Find the AQTW32 window using pygetwindow
window_title = 'AQTW32'
aqtw32_window = None
while aqtw32_window is None:
    try:
        aqtw32_window = pygetwindow.getWindowsWithTitle(window_title)[0]
    except IndexError:
        pass

# Switch to the AQTW32 window
aqtw32_window.activate()

# Wait for the window to activate
time.sleep(2)

# Press Alt+F to open the File menu
pyautogui.hotkey('alt', 'f')

# Press O to select the Open option
pyautogui.press('o')

# Wait for the Open dialog to appear
time.sleep(2)

# Type the path to the file and press Enter
filename = 'w1_02_long.aqt'
file_path = os.path.abspath(filename)
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
maximize_image = r'd:\05_Send\maximize.png'
maximize_pos = None
while maximize_pos is None:
    maximize_pos = pyautogui.locateOnScreen(maximize_image, region=aqtw32_window.lefttop+aqtw32_window.size)

if maximize_pos is not None:
    # If the button is found, get its center coordinates
    maximize_center = pyautogui.center(maximize_pos)
    # Click the center of the button
    pyautogui.click(maximize_center)
else:
    # If the button is not found, print an error message
    print(f"Maximize button ({maximize_image}) not found on screen.")
