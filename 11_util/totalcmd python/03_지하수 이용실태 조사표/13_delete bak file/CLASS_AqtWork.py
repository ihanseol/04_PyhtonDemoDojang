import fnmatch
import time
import os
import pyperclip
import re
from natsort import natsorted
import pyautogui
import ctypes
import pandas as pd

from FileProcessing_V4_20240717 import FileBase
from FileProcessing_V4_20240717 import PathChecker


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
        if len(input_str) > 21:
            parts = input_str.split()
            i = 0

            for part in parts:
                if part.endswith("읍") or part.endswith("면") or part.endswith("동") or part.endswith("구"):
                    break
                i += 1

            result = ' '.join(parts[i:])

            if len(result) > 21:
                result = result.replace('번지', '')

            address_list = result.split()
            filtered_list = [item for item in address_list if not (item.endswith('아파트') or item == ',')]
            address_string = ' '.join(filtered_list)

            return address_string
        else:
            return input_str

    @staticmethod
    def extract_number(s):
        """
        :param s:
            주어진 스트링 S값을 입력받아,
            숫자만 추려서, 정수로 반환한다.
        :return:
        """
        return int(re.findall(r'\d+', s)[0])

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


class AqtExcelProjectInfoInjector(AqtProjectInfoInjector):
    def __init__(self, directory, company):
        super().__init__(directory, company)
        # self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
        self.df = pd.DataFrame()
        self.fb = FileBase()

    def set_dataframe(self, df):
        self.df = df

    def get_gong_n_address(self, row_index):
        """
            줄번호, row_index 를 받아서
            그 해당하는 인덱스의 공번, 주소를 리턴
        """
        try:
            row_data = self.df.iloc[row_index - 1, :].tolist()
            str_gong = row_data[0]
            address = row_data[1]
            time.sleep(1)
        except Exception as e:
            print(f"get_gong_n_address: {e}")
            return None, "None"

        print(str_gong, address)
        return str_gong, address

    def get_last_gong(self):
        """
          엑셀파일의 마지막 공번을 리턴
        :return:
        """
        try:
            str_gong = self.df.iloc[-1, 0]
            gong = self.df.extract_number(str_gong)
            time.sleep(1)
            return gong
        except Exception as e:
            print(f"get_last_gong: {e}")
            return None

    def get_gong_list(self):
        """
        :return:
            Excel 파일을 df 로 불러들여
            이곳에서 공번만을 주려서
            그것을  정수로, 돌려준다.
        """
        g_list = []
        gong_column = self.df['gong'].tolist()
        for f in gong_column:
            n = self.extract_number(f)
            g_list.append(n)
        print(f'g_list: {g_list}')
        return g_list

    def delete_difference(self, file_list):
        """
        :param file_list:
            [3, 4, 5]
            파일리스트에, 지워야할 관정파일들의 리스트를 받고
            그것을 SEND폴더에서 찾아서, 엑셀에 없는 공번들을 가진 aqt 파일을 지운다.
        :return:
        """
        aqtfiles = natsorted(self.get_aqt_files())

        for f in file_list:
            ffiles = fnmatch.filter(aqtfiles, f"w{f}_*.aqt")
            for _ in ffiles:
                os.remove(_)

    def process_projectinfo_byexcel(self, company, address):

        if self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        self.set_company(company)
        self.set_address(address)
        self.change_aqt_filename()

        send_list = self.get_wellno_list_insend()
        xlsx_list = self.get_gong_list()

        difference_set = list(set(send_list) - set(xlsx_list))
        self.delete_difference(difference_set)

        aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])
        aqtfiles = self.get_aqt_files()
        print(f'aqtfiles: {aqtfiles}')
        # self.block_user_input()

        for i in xlsx_list:
            gong, excel_address = self.get_gong_n_address(i)

            if gong is None:
                self.close_aqt()
                return None

            processed_address = self.process_address(excel_address)
            print(f'gong: {gong}, address: {processed_address}')
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            print(f"wfiles: {wfiles}")

            if wfiles:
                if self.DEBUG:
                    print('Processing file: ', wfiles)
                self.aqt_mainaction(self.extract_number(gong), processed_address, wfiles)

        if self.DEBUG:
            print('All files processed.')

        self.unblock_user_input()

    def process_projectinfo_likesejong(self, company):

        if self.is_exist(r"d:\05_Send\YanSoo_Spec.xlsx"):
            df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
            self.set_dataframe(df)

        self.set_company(company)
        # self.set_address(address)
        self.change_aqt_filename()

        send_list = self.get_wellno_list_insend()
        xlsx_list = self.get_gong_list()

        difference_set = list(set(send_list) - set(xlsx_list))
        self.delete_difference(difference_set)

        aqtfiles = natsorted([f for f in os.listdir() if f.endswith('.aqt')])
        aqtfiles = self.get_aqt_files()
        if not aqtfiles:
            print('Error No AQT')
            return None

        print(f'aqtfiles: {aqtfiles}')
        # self.block_user_input()

        for i in xlsx_list:
            gong, excel_address = self.get_gong_n_address(i)

            if gong is None:
                self.close_aqt()
                return None

            processed_address = self.process_address(excel_address)
            self.set_address(processed_address)

            print(f'gong: {gong}, address: {processed_address}')
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            print(f"wfiles: {wfiles}")

            if wfiles:
                if self.DEBUG:
                    print('Processing file: ', wfiles)
                self.aqt_mainaction(self.extract_number(gong), processed_address, wfiles)

        if self.DEBUG:
            print('All files processed.')

        self.unblock_user_input()

