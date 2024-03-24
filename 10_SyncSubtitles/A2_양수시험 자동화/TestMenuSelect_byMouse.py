import pyautogui
import time
import os
import pytesseract
from PIL import Image


PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = True


# AQTSOLVE 는 듀얼모니터 상에 메인윈도우에 위치 해야한다.
# 그래야 pyautogui 를 사용할수가 있다.


def open_aqt(filename):
    if filename:
        os.startfile(filename)
    else:
        os.startfile("d:\\05_Send\\w3_02_long.aqt")

    time.sleep(1)
    pyautogui.click(x=1557, y=93)  #maximize sub window
    time.sleep(0.5)


def maxmize_aqtsolv():
    win = pyautogui.getWindowsWithTitle('AQTESOLV')[0]
    if not win.isActive:
        win.activate()
    if not win.isMaximized:
        win.maximize()



open_aqt("d:\\05_Send\\w3_02_long.aqt")

# import data
pyautogui.click(x=42, y=33)  # file
time.sleep(DELAY)
pyautogui.click(x=92, y=173)  # import
time.sleep(DELAY)
pyautogui.press('enter')
time.sleep(DELAY)


# browse for filename
pyautogui.hotkey('alt', 'r')
time.sleep(DELAY)
pyautogui.press('backspace')
time.sleep(DELAY)
pyautogui.typewrite("c:\\Users\\minhwasoo\\Documents\\A3_ge_janggi_01.dat")
time.sleep(DELAY)
pyautogui.press('enter')
time.sleep(DELAY)
pyautogui.hotkey('alt', 'f') #finish
time.sleep(DELAY)
pyautogui.press('enter')

#Set Unit

time.sleep(DELAY)
pyautogui.hotkey('alt', 'e') #Edit
pyautogui.press('u') #unit
time.sleep(DELAY)
pyautogui.hotkey('alt', 't') #time
pyautogui.press('m') #unit
time.sleep(DELAY)
pyautogui.press('enter')
time.sleep(DELAY)

#End Set Unit


#Automatic Match

time.sleep(DELAY)
pyautogui.hotkey('alt', 'm') #match
pyautogui.press('u') # automatic
time.sleep(DELAY)
pyautogui.press('enter')
time.sleep(DELAY)
pyautogui.press('enter')
time.sleep(DELAY)
pyautogui.press('enter')
time.sleep(DELAY)

#Automatic Match



# GetText YangSoo Result
# time.sleep(DELAY)
# pyautogui.hotkey('alt', 'm') #match
# pyautogui.press('e') # perturb
# time.sleep(DELAY)
# pyautogui.press('enter')
# time.sleep(DELAY)


im3 = pyautogui.screenshot(region=(1026, 263, 130, 40)) # : 메인창 결과화면을 캡쳐
#im3 = pyautogui.screenshot(region=(1134, 651, 80, 30))


for i in range(70, 100, 2):
    im3.save(DIRECTORY + 'screenshot.jpg', quality=i)
    image = Image.open(DIRECTORY + 'screenshot.jpg')
    text = pytesseract.image_to_string(image)
    print(i, text)




