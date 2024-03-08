import os
import time
import fnmatch
import argparse
import pyautogui
import win32gui
import ctypes
import pyperclip
from pick import pick


PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = True

G_COMPANY = "산수개발(주)"
# G_COMPANY = "대웅엔지니어링 주식회사"
# G_COMPANY = "(주) 우경엔지니어링"
# G_COMPANY = "주식회사 한일지하수"
# G_COMPANY = "(주)동해엔지니어링"
# G_COMPANY = "(주)현윤이앤씨"
# G_COMPANY = "(주) 전일"
# G_COMPANY = "부여지하수개발 주식회사"
# G_COMPANY = "(주)태양이엔지"
# G_COMPANY = "삼원개발(주)"
# G_COMPANY = "마인지오 주식회사"

G_ADDRESS = "주소"


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
    title = 'Please choose your Company: '
    options = ['SanSu', 'DaeWoong', 'WooKyung', 'HanIL', 'DongHae', 'HyunYoon', 'JunIL','BuYeo','TaeYang','SamWon','MainGeo']

    MyCompany  = ["산수개발(주)", "대웅엔지니어링 주식회사", "(주) 우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링",
                  "(주)현윤이앤씨",  "(주) 전일", "부여지하수개발 주식회사", "(주)태양이엔지", "삼원개발(주)",  "마인지오 주식회사"]

    option, index = pick(options, title, indicator='==>', default_index=1)
    print(option, index, MyCompany[index])

    address = input('Enter the Company Address :')

    if not address:
        G_ADDRESS = "Empty Address"
    else:
        G_ADDRESS = address

    user32 = ctypes.windll.user32
    if IS_BLOCK:
        user32.BlockInput(True)

    files = os.listdir(DIRECTORY)
    aqtfiles = [f for f in files if f.endswith('.aqt')]

    if aqtfiles:
        for i in range(1, 19):  # maximum well number is 18
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            if wfiles:
                for j, file in enumerate(wfiles):
                    open_aqt(file)
                    main_job(f"W-{i}", G_ADDRESS, MyCompany[index])

        close_aqt()
    else:
        print('aqt files does not found ...')

    time.sleep(0.5)

    if IS_BLOCK:
        user32.BlockInput(False)


if __name__ == "__main__":
    main()
