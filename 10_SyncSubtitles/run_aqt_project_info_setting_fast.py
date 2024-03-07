import os
import time
import fnmatch
import argparse
import pyautogui
import win32gui
import ctypes
import pyperclip


PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = True

G_COMPANY = "동아인재(주)"
G_ADDRESS = "대전시 유성구 장대동 278-13"


def enter_project_info():
    pyautogui.hotkey('alt', 'e')
    time.sleep(0.2)
    pyautogui.press('r')


def open_aqt(filename):
    global PROGRAM_PATH
    global DELAY
    global ISAQTOPEN

    if not ISAQTOPEN:
        os.startfile(PROGRAM_PATH)
        ISAQTOPEN = True
        time.sleep(DELAY)

    pyautogui.hotkey('ctrl', 'o')
    pyautogui.press('backspace')
    pyautogui.typewrite(DIRECTORY+filename)
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)


def close_aqt():
    pyautogui.hotkey('ctrl', 's')
    time.sleep(DELAY)
    pyautogui.hotkey('alt', 'f4')
    time.sleep(DELAY)


def main_job(well, address, company):
    time.sleep(0.2)
    enter_project_info()
    pyperclip.copy(company)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('tab',3)
    pyperclip.copy(address)
    pyautogui.hotkey('ctrl', 'v')
    pyperclip.copy(well)
    pyautogui.press('tab')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('tab')
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.press('enter')
    pyautogui.hotkey('ctrl', 's')
    time.sleep(DELAY)


def main():
    user32 = ctypes.windll.user32
    if IS_BLOCK:
        user32.BlockInput(True)

    files = os.listdir(DIRECTORY)
    aqtfiles = [f for f in files if f.endswith('.aqt')]
    
    for i in range(1, 19):  # maximum well number is 18
        wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
        if len(wfiles) != 0:
            for j, file in enumerate(wfiles):
                open_aqt(file)
                main_job(f"w-{i}", G_ADDRESS, G_COMPANY)

    close_aqt()
    time.sleep(1)

    if IS_BLOCK:
        user32.BlockInput(False)


if __name__ == "__main__":
    main()
