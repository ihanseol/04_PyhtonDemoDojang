import pygetwindow as gw
import subprocess
import fnmatch
import time
import os
import pyautogui
from PIL import Image
import pytesseract
import re

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
DELAY = 0.5
IS_BLOCK = True

def open_aqt(filename):
    def open_program_on_primary_monitor():
        subprocess.Popen(PROGRAM_PATH)
        primary_monitor = gw.getWindowsAt(0, 0)
        if primary_monitor:
            primary_monitor[0].moveTo(0, 0)

    def maxmize_aqtsolv():
        win = pyautogui.getWindowsWithTitle('AQTESOLV')[0]
        if not win.isActive:
            win.activate()
        if not win.isMaximized:
            win.maximize()


    if os.path.exists(DIRECTORY + filename):
        open_program_on_primary_monitor()
        pyautogui.click(100, 100)

        maxmize_aqtsolv()
        time.sleep(DELAY)

        pyautogui.hotkey('ctrl', 'o')
        pyautogui.press('backspace')

        pyautogui.typewrite(DIRECTORY + filename)
        time.sleep(DELAY)
        pyautogui.press('enter')

        print(f"open aqtsolver : {DIRECTORY + filename} ....")
    else:
        print("The file does not exist.")

    pyautogui.click(x=2081, y=93)  # maximize sub window
    time.sleep(0.5)



# Example usage:

open_aqt(r"w9_01_step.aqt")




