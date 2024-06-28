import fnmatch
import time
import os
import ctypes
import pyperclip
from pick import pick
import pandas as pd
import re
from natsort import natsorted
import pyautogui


class AqtSolveProjectInfoInjector:
    def __init__(self, directory, company):
        self.DIRECTORY = directory
        self.COMPANY = company
        self.DEBUG_YES = True
        self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")

        self.PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.DELAY = 0.5
        self.ISAQTOPEN = False
        self.IS_BLOCK = True

    def open_aqt(self, filename):
        if not self.ISAQTOPEN:
            os.startfile(self.PROGRAM_PATH)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

        pyautogui.hotkey('ctrl', 'o')
        pyautogui.press('backspace')
        pyautogui.typewrite(self.DIRECTORY + filename)
        time.sleep(self.DELAY)
        pyautogui.press('enter')
        time.sleep(self.DELAY)

    def close_aqt(self):
        if self.ISAQTOPEN:
            self.ISAQTOPEN = False

        pyautogui.hotkey('ctrl', 's')
        time.sleep(self.DELAY)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(self.DELAY)

    def main_job(self, well, address):
        def enter_project_info():
            pyautogui.hotkey('alt', 'e')
            time.sleep(0.2)
            pyautogui.press('r')

        time.sleep(0.2)

        # ---- company name ---
        pyperclip.copy(self.COMPANY)
        enter_project_info()
        pyautogui.hotkey('ctrl', 'v')

        # ---- location ---
        for i in range(3):
            pyautogui.press('tab')
            time.sleep(0.2)

        pyperclip.copy(address)
        pyautogui.hotkey('ctrl', 'v')

        # ---- well ---
        pyautogui.press('tab')
        pyperclip.copy(well)
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('tab')
        pyautogui.hotkey('ctrl', 'v')

        pyautogui.press('enter')
        pyautogui.hotkey('ctrl', 's')
        time.sleep(self.DELAY)

    def get_gong_n_address(self, row_index):
        row_data = self.df.iloc[row_index - 1, :].tolist()

        str_gong = row_data[0]
        address = row_data[1]

        time.sleep(1)
        return str_gong, address

    @staticmethod
    def process_address(input_str):
        # Split the input string by spaces
        parts = input_str.split()

        print(parts)  # For debugging

        # Initialize the index
        i = 0

        # Iterate over the parts to find the target index
        for part in parts:
            if part.endswith("면") or part.endswith("구"):
                break
            i += 1

        # Select the parts you want to keep
        result = ' '.join(parts[i:])

        if len(result) > 21:
            result = result.replace('번지', '')

        address_list = result.split()

        filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
        print(filtered_list)

        return filtered_list

    def process_files(self):
        os.chdir(self.DIRECTORY)
        aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])

        if aqtfiles:
            for i in range(1, 33):  # maximum well number is 32
                gong, address = self.get_gong_n_address(i)
                address = self.process_address(address)
                print(gong, address)
                wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")

                if wfiles:
                    for j, file in enumerate(wfiles):
                        if self.DEBUG_YES: print('Processing file: ', file)

                        self.open_aqt(file)
                        self.main_job(gong, address)
                        self.close_aqt()
        else:
            print('aqt files does not found ...')

        if self.DEBUG_YES: print('All files processed.')


def main():
    title = 'Please choose your Company: '
    options = ['SanSu', 'DaeWoong', 'WooKyung', 'HanIL', 'DongHae', 'HyunYoon', 'JunIL', 'BuYeo', 'TaeYang', 'SamWon',
               'MainGeo']

    MyCompany = ["산수개발(주)", "대웅엔지니어링 주식회사", "(주) 우경엔지니어링", "주식회사 한일지하수", "(주)동해엔지니어링",
                 "(주)현윤이앤씨", "(주) 전일", "부여지하수개발 주식회사", "(주)태양이엔지", "삼원개발(주)", "마인지오 주식회사"]

    option, index = pick(options, title, indicator='==>', default_index=1)
    company = MyCompany[index]
    print(option, index, company)

    injector = AqtSolveProjectInfoInjector("d:\\05_Send\\", company)
    # injector = AqtSolveProjectInfoInjector("d:\\05_Send\\", "산수개발(주)")

    injector.process_files()


if __name__ == "__main__":
    main()
