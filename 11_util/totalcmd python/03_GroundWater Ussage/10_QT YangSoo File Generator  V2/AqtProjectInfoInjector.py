import shutil
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from datetime import datetime

import fnmatch
import time
import os
import pyperclip
import re
from natsort import natsorted
import pyautogui
import ctypes
import pandas as pd

import re
from FileManager import FileBase


class AqtProjectInfoInjector(FileBase):
    def __init__(self, directory, _company):
        super().__init__()
        self.COMPANY = _company
        self.ADDRESS = ""
        self.DEBUG = True
        self.DIRECTORY = directory

    def set_address(self, value):
        self.ADDRESS = value

    def set_company(self, value):
        self.COMPANY = value

    def open_aqt(self, filename):
        if not self.ISAQTOPEN:
            print(f'open_aqt: {filename}')
            os.startfile(self.AQTESOLV_PATH)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

        pyautogui.hotkey('ctrl', 'o')
        pyautogui.press('backspace')
        pyautogui.typewrite(self.SEND + filename)
        time.sleep(self.DELAY)
        pyautogui.press('enter')
        time.sleep(self.DELAY)

    def open_aqt_file(self, filename):
        if not self.ISAQTOPEN:
            print(f'open_aqt: {self.SEND + filename}')
            os.startfile(self.SEND + filename)
            self.ISAQTOPEN = True
            time.sleep(self.DELAY)

    def close_aqt(self):
        if self.ISAQTOPEN:
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.DELAY)
            pyautogui.hotkey('alt', 'f4')
            time.sleep(self.DELAY)

        self.ISAQTOPEN = False

    def main_job(self, well, address):
        if self.ISAQTOPEN:
            time.sleep(0.2)
            pyperclip.copy(self.COMPANY)
            # enter project info
            pyautogui.hotkey('alt', 'e')
            # time.sleep(0.2)
            pyautogui.press('r')
            # project info

            pyautogui.hotkey('ctrl', 'v')

            for _ in range(3):
                pyautogui.press('tab')
                # time.sleep(0.2)

            pyperclip.copy(address)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('tab')
            pyperclip.copy(well)
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('tab')
            pyautogui.hotkey('ctrl', 'v')

            pyautogui.press('enter')
            pyautogui.hotkey('ctrl', 's')
            time.sleep(self.DELAY)

    def aqt_mainaction(self, well_no, address, wfiles):
        """
        :param well_no:
             공번,
        :param address:
              주소
        :param wfiles:
            프로젝트 인포 세팅할 , 파일리스트
        """
        for j, file in enumerate(wfiles):
            self.open_aqt_file(file)
            self.main_job(f"W-{well_no}", address)
            self.close_aqt()

    @staticmethod
    def process_address(input_str):
        """
        :param input_str:
            주어진 주소값을 입력받고, 그 주소가 길면
            그 주소를 정해진 규칙에 의해서 잘라서
            반환한다.
            aqtsolv project_info 의 주소길이에 맟추어서

            부여읍,신정리177,실지번,산37-1 <-- AqtSolver 에 들어가는 최대치
            글자의 갯수로 20자이다.

        :return:
        """

        input_str = input_str.strip().replace('특별', '').replace('광역', '')
        input_str = re.sub(r'\s+', ' ', input_str).strip()

        if ',' in input_str:
            input_str = input_str.split(',')[0]

        if '(' in input_str:
            input_str = input_str.split('(')[0]

        if len(input_str) >= 18:
            if input_str.endswith('호'):
                input_str = input_str.replace('번지 ', '-')
                input_str = input_str[0:-1]  # remove '호'
            else:
                input_str = input_str.replace('번지', '')

            parts = input_str.split(' ')
            i = 0

            for part in parts:
                if part.endswith('도') or part.endswith('시') or part.endswith('구') or part.endswith('동'):
                    break
                i += 1

            result = ' '.join(parts[(i + 1):])
            address_list = result.split(' ')

            filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
            address_string = ' '.join(filtered_list)

            return address_string
        else:
            return input_str

    @staticmethod
    def extract_number(s):
        """
        주어진 입력값에서 숫자만 추출하여 정수로 반환합니다.
        비정상적인 입력에 대한 예외 처리가 포함되어 있습니다.
        """
        try:
            # 1. 입력값이 문자열이 아닌 경우를 대비해 타입 체크 또는 변환
            if not isinstance(s, str):
                s = str(s)

            # 2. 정규표현식으로 숫자 추출
            numbers = re.findall(r'\d+', s)
            num_str = ''.join(numbers)

            # 3. 추출된 숫자가 없을 경우 처리
            if not num_str:
                return 0  # 또는 상황에 따라 None이나 raise ValueError를 사용하세요.

            # 4. 정수 변환
            return int(num_str)

        except ValueError as e:
            # 숫자로 변환할 수 없는 예기치 못한 상황 처리
            print(f"Value Error: {e}")
            return 0
        except Exception as e:
            # 기타 발생 가능한 모든 에러 처리
            print(f"An unexpected error occurred: {e}")
            return 0

    def change_aqt_filename(self):
        """
        aqtfile 을 SEND 에서 불러와서
        파일이름중에, 복사본이 있으면, 이것을 바꾸어 준다.
        """
        aqtfiles = self.get_aqt_files()
        for filename in aqtfiles:
            name, ext = self.seperate_filename(filename)

            if ext == ".aqt" and "_01" not in name:
                suffixes = [" - 복사본", " - Copy"]
                for suffix in suffixes:
                    if suffix in name:
                        new_name = name.replace(suffix, "_01") + ext
                        os.rename(os.path.join(self.SEND, filename), os.path.join(self.SEND, new_name))
                        break

    def get_wellno_list_insend(self):
        """
            Send folder 에 있는 , aqtfiles 의 관정번호를
            Set으로 추려서 유닉하게 만든다.
        """

        aqtfiles = self.get_aqt_files()
        aqtfiles = natsorted(aqtfiles)

        wellnos = [self.extract_number(f.split('_')[0]) for f in aqtfiles]
        return list(set(wellnos))

    def Set_Projectinfo(self, company, address):
        print(f"Set_Projectinfo,1 - company: {company} / address: {address}")
        self.change_aqt_filename()

        processed_address = self.process_address(address)
        self.set_company(company)
        self.set_address(processed_address)

        print(f'len(address) - {len(processed_address)}')
        if len(processed_address) > 21:
            print(f"its over the size ...{processed_address}")
        else:
            print(f"its in the size ...{processed_address}")

        self.block_user_input()

        aqtfiles = self.get_aqt_files()
        print(f'Set_Projectinfo2, - aqtfiles: {aqtfiles}')

        if not self.ISAQTOPEN:
            if aqtfiles:
                w_list = self.get_wellno_list_insend()
                for i in w_list:
                    wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
                    print(f'Set_Projectinfo3, - wfiles: {wfiles}')
                    if wfiles:
                        self.aqt_mainaction(i, processed_address, wfiles)
            else:
                print('aqt files does not found ...')
        else:
            self.ISAQTOPEN = False

        time.sleep(0.5)
        self.unblock_user_input()


if __name__ == "__main__":
    # fp = PrepareYangsoofile()
    # fp.aqtfile_to_send(well_no=1)
    # fp.duplicate_yangsoo(3)

    # tyd = TransferYangSooFile()
    # tyd.setBASEDIR()
    # tyd.move_origin_to_ihanseol(tyd.SEND2)

    # tyd.move_origin_to_ihanseol()
    # tyd.move_send2_to_ihanseol()

    #
    # tyd.move_documents_to_ihanseol()
    # tyd.Test()

    # main
    # spi = AqtProjectInfoInjector("d:\\05_Send", "aa")
    # print(spi.process_address("충청남도 당진시 송악읍 신평로 1469"))

    # test, initial_set_yangsoo_excel
    py = PrepareYangsoofile()
    py.initial_set_yangsoo_excel()
