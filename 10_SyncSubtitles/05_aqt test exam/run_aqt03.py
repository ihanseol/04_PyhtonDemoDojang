import os
import pyautogui
import subprocess


program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
screen_width, screen_height = pyautogui.size()

filename = 'w1_02_long.aqt'
file_path = os.path.abspath(filename)


subprocess.Popen([program_path, file_path])

pyautogui.sleep(2)

window_handle = pyautogui.getActiveWindow()
window_rect = pyautogui.getWindowRect(window_handle)
if window_rect.left < 0 or window_rect.top < 0:
    pyautogui.moveWindow(window_handle, 0, 0)



time.sleep(1)


pyautogui.hotkey('ctrl', 'o')
time.sleep(1)


pyautogui.typewrite(file_path)
pyautogui.press('enter')
time.sleep(1)


pyautogui.hotkey('alt', 'v')
pyautogui.press('r')
time.sleep(1)



mpos = pyautogui.locateOnScreen('max.png', region=(2560, 0, 2560, 1440))

if mpos is not None:
    # If the button is found, get its center coordinates
    mcenter = pyautogui.center(mpos)
    # Click the center of the button
    pyautogui.click(mcenter)
else:
    # If the button is not found, print an error message
    print(f"Maximize button not found on screen.")


