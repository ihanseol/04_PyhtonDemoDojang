import time
import pyautogui

# Open Notepad
pyautogui.press('win')
pyautogui.typewrite('notepad')
pyautogui.press('enter')

# Wait for Notepad to open
time.sleep(2)

# Type "Hello, world!" into Notepad
pyautogui.typewrite('Hello, world!')

# Save the file
pyautogui.hotkey('ctrl', 's')
pyautogui.typewrite('hello.txt')
pyautogui.press('enter')

# Wait for the save dialog to close
time.sleep(2)

# Print the file to PDF using the Windows Print to PDF feature
pyautogui.hotkey('ctrl', 'p')
time.sleep(2)
pyautogui.hotkey('alt', 'n')
time.sleep(2)
pyautogui.typewrite('Microsoft Print to PDF')
pyautogui.press('enter')
time.sleep(2)
pyautogui.typewrite('hello.pdf')
pyautogui.press('enter')
time.sleep(2)
pyautogui.hotkey('alt', 'p')
