
import pytesseract
from PIL import Image


PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = True


# im1 = pyautogui.screenshot(region=(996, 1208, 130, 22)) #T
# im1.save(DIRECTORY + 'screenshot_t.jpg', quality=95)

image1 = Image.open(r"d:\05_Send\pythonProject\outputname.png")
text1 = pytesseract.image_to_string(image1, config="--psm 7")
print(text1)

