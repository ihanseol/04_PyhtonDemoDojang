import os
import time
import fnmatch
import argparse
import pyautogui
import win32gui
from natsort import natsorted
import ctypes
import pyperclip
from pick import pick
import re

PROGRAM_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = False

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
    global ISAQTOPEN

    if ISAQTOPEN:
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
    pyautogui.typewrite(DIRECTORY + filename)
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)


def close_aqt():
    global ISAQTOPEN

    if ISAQTOPEN:
        pyautogui.hotkey('ctrl', 's')
        time.sleep(DELAY)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(DELAY)
        ISAQTOPEN = False


def main_job(well, address, company):
    global ISAQTOPEN

    if ISAQTOPEN:
        time.sleep(0.2)
        enter_project_info()
        pyperclip.copy(company)
        pyautogui.hotkey('ctrl', 'v')
        pyautogui.press('tab', 3)
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


def process_address(input_str):
    # Split the input string by spaces
    if len(input_str) <= 21:
        return input_str

    parts = input_str.split()
    print(parts)  # For debugging

    # Initialize the index
    i = 0
    # Iterate over the parts to find the target index
    for part in parts:
        if part.endswith("읍") or part.endswith("면") or part.endswith("동") or part.endswith("구"):
            break
        i += 1

    # Select the parts you want to keep
    result = ' '.join(parts[i:])

    if len(result) > 21:
        result = result.replace('번지', '')

    address_list = result.split()

    filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
    print(filtered_list)
    address_string = ' '.join(filtered_list)

    return address_string


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def get_wellno_list_insend():
    """
     Send folder 에 있는 , aqtfiles 의 관정번호를
     set추려서 유닉하게 만든다.
    """
    global DIRECTORY

    os.chdir(DIRECTORY)
    aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])

    fn_list = []
    for f in aqtfiles:
        num = extract_number(f.split('_')[0])
        fn_list.append(num)

    fn_list = list(set(fn_list))
    return fn_list


def Set_Projectinfo(company, address):
    global ISAQTOPEN

    print(f"iniside, Set_Projectinfo - company: {company} / address: {address}")

    address = process_address(address)
    print(len(address))
    if len(address) > 21:
        print("its over the size ...")

    user32 = ctypes.windll.user32
    if IS_BLOCK:
        user32.BlockInput(True)

    files = os.listdir(DIRECTORY)
    aqtfiles = [f for f in files if f.endswith('.aqt')]
    print(f'Set_Projectinfo - aqtfiles: {aqtfiles}')

    if not ISAQTOPEN:
        if aqtfiles:
            w_list = get_wellno_list_insend()
            for i in w_list:  # maximum well number is 18
                wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
                print(f'Set_Projectinfo - wfiles: {wfiles}')
                if wfiles:
                    for j, file in enumerate(wfiles):
                        open_aqt(file)
                        main_job(f"W-{i}", address, company)
            close_aqt()
        else:
            print('aqt files does not found ...')
    else:
        ISAQTOPEN = False

    time.sleep(0.5)
    if IS_BLOCK:
        user32.BlockInput(False)


def main():
    title = 'Please choose your Company: '
    options = ['SanSu', 'DaeWoong', 'WooKyung', 'HanIL', 'DongHae', 'HyunYoon', 'JunIL', 'BuYeo', 'TaeYang', 'SamWon',
               'MainGeo']

    MyCompany = ["산수개발(주)", "대웅엔지니어링 주식회사", "(주) 우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링",
                 "(주)현윤이앤씨", "(주) 전일", "부여지하수개발 주식회사", "(주)태양이엔지", "삼원개발(주)", "마인지오 주식회사"]

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
        for i in range(1, 33):  # maximum well number is 18
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
    # main()
    Set_Projectinfo("한일지하수", "당진시 순성면 순성로 453-30 , 순성중명아파트")
