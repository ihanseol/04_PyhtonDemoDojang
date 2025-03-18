"""

# *************************************************************************
# 2024.3.25
# 이파일을 양수시험 1단계 로서
# 관정스펙을 읽어서 YangSoo.xlsx
# 하나하나 데이타를 써주는 1차작업을 한다.
# gong  hp  casing  well_rad    simdo   q   natual  stable
# 공번, 마력, 케이싱, 구경, 심도, 양수량, 자연수위, 안정수위
#
# 2024.4.9일
# 이것을 클래스로 전환, 그리고 에러처리 ....
# 에러처리를 위해서, 버튼클릭함수를 에러처리를 추가해서 변경해주고
# 입력시트에서 자연수위, 안정수위로 에러가나는것을 방지해주기 위해 처리해줌
#
#
# 2024.6.15일
# YanSoo.xlsl 파일에 조사명, 지역명 추가해서 처리해주는 부분 추가
# 그리고, click_excel_button 에서, 에러가 나서 빠지는것을 막기위해
# While True: 로 처리 ....
#
#
# 2024.6.19일
# 안정수위 도달시간을 , 데이타시트 (YanSoo_Spec.xlsx) 에 추가해주고
# 이것이 들어올때, 없을때의 처리 추가 해줌
#
#
# 2024.6.26
# 신규로 수정한 양수시험일보를 적용하기위해
# 구버전과 신버전을 동시 지원을 위해 self.isOLD 추가해주고, 처리

# 그리고 리팩토
# *************************************************************************
"""
from typing import Any

import win32com.client as win32

import pandas as pd
import re
import os
import time
import keyboard
import random

from natsort import natsorted
import pyautogui
import pygetwindow as gw
import pytz
from datetime import datetime, timedelta


def clear_screen():
    # Clear console based on OS
    os.system('cls' if os.name == 'nt' else 'clear')


# ANSI 색상 코드
COLOR_RESET = "\033[0m"
INVERTED = "\033[7m"  # 반전 색상 (흰색 배경, 검은색 글씨)


class ConsoleMenu:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.running = True

    def display_menu(self):
        clear_screen()
        print("Use ↑↓ arrows to navigate, Enter to select:\n")
        for i, option in enumerate(self.options):
            if i == self.selected:
                # 선택된 항목에 반전 색상 적용
                print(f"{INVERTED}> {option} {COLOR_RESET}")
            else:
                print(f"  {option}")

    def move_up(self):
        if self.selected > 0:
            self.selected -= 1
            self.display_menu()

    def move_down(self):
        if self.selected < len(self.options) - 1:
            self.selected += 1
            self.display_menu()

    def select(self):
        self.running = False
        return self.options[self.selected]

    def run(self):
        # Bind arrow keys and enter
        keyboard.on_press_key("up", lambda _: self.move_up())
        keyboard.on_press_key("down", lambda _: self.move_down())
        keyboard.on_press_key("enter", lambda _: self.select())

        # Display initial menu
        self.display_menu()

        # Keep running until selection is made
        while self.running:
            time.sleep(0.1)

        # Unbind keys after selection
        keyboard.unhook_all()
        return self.options[self.selected]


class YangSooPrinter:
    def __init__(self, directory):
        self.directory = directory
        # self.spec_file = spec_file

        try:
            self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
        except Exception as e:
            print(f"YanSoo.xlsx Not Found - {e}")

        # self.df = pd.read_excel(spec_file)
        self.isOLD = True
        self.debug_yes = True
        self.STABLE_TIME = 0
        self.LONG_TERM_TEST_TIME = pd.Timestamp('2024-06-29 15:45:09')
        '''
            여기서, 안정수위 도달시간 stable_time = 0 이면
            이것은, 자동으로 처리한다는 의미이다.        
        '''

    @staticmethod
    def countdown(n):
        print(' Please Move the Command Window to Side ! ')
        while n > 0:
            print(n)
            time.sleep(1)
            n -= 1
        print("Time's up!")

    @staticmethod
    def extract_number(s):
        return int(re.findall(r'\d+', s)[0])

    def click_excel_button(self, ws, button_name):

        """
            def click_button():
                for i in range(1, ws.OLEObjects().Count + 1):
                    obj = ws.OLEObjects().Item(i)
                    if obj.Name == button_name:
                        obj.Object.Value = True
                        return True
                return False
        """

        def click_button():
            for obj in ws.OLEObjects():
                if obj.Name == button_name:
                    obj.Object.Value = True
                    return True
            return False

        while True:
            try:
                if not click_button(): return False
                break  # Exit the loop if no exception is raised
            except Exception as e:
                print(f"{ws} - {button_name} : Error in Button Click Function", e)
                time.sleep(1)  # Optional: Wait a bit before retrying
            finally:
                self.change_window('EXCEL')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

        return True

    def click_excel_buttons(self, ws, button_names):
        check = False
        for button_name in button_names:
            check = self.click_excel_button(ws, button_name)
            if not check:
                print(button_name, " Not Found ...")
            else:
                print("Button Click Function", button_name)
        return check

    @staticmethod
    def isit_oldversion(ws, button_name):
        """
        :param ws:
        :param button_name:
        :return:
            button_name found is ws then this is True

        """
        for obj in ws.OLEObjects():
            if obj.Name == button_name:
                return False
        return True

    @staticmethod
    def change_window(name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)

        if gwindows:
            window = gwindows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            print(f"No  {name_title} found.")

    @staticmethod
    def initial_delete_output_file(folder_path):
        files = os.listdir(folder_path)
        pdf_files = [f for f in files if f.endswith('.pdf')]


        for file in pdf_files:
            file_path = os.path.join(folder_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file} has been removed successfully.")
            else:
                print(f"The file {file} does not exist in the folder {folder_path}.")


    def data_validation(self):
        def collect_ge_original_save_files():
            files = natsorted([f for f in os.listdir() if f.endswith('.xlsm')])
            filtered_files = [f for f in files if "ge_OriginalSaveFile" in f]

            return filtered_files

        os.chdir(self.directory)
        yangsoo_files = collect_ge_original_save_files()

        if not yangsoo_files:
            print("No YangSoo .xlsm files found.")
            return None

        last_file = yangsoo_files[-1]
        row_index = self.extract_number(last_file) - 1

        return yangsoo_files

    def print_report(self, wb, choice):
        ws = wb.Worksheets("Recover.Select")
        ws.Activate()

        if choice in "STEP":
            self.click_excel_button(ws, "CommandButton_Print_LS")
        else:
            self.click_excel_button(ws, "CommandButton_Print_Long")

    def process_files(self, Choice):
        files = self.data_validation()
        if files is None:
            print("Index Does not have YangSoo file ...")
            return None

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False

        excel.Visible = True
        excel.WindowState = -4137  # xlMaximizedWindow
        self.change_window('EXCEL')

        for file in files:
            if self.debug_yes: print('Processing file: ', file)
            wb = excel.Workbooks.Open(self.directory + file)
            self.print_report(wb, Choice)
            wb.Close(SaveChanges=True)

        excel.ScreenUpdating = True
        excel.Quit()
        if self.debug_yes: print('All files processed.')


def main():
    menu_options = [
        "Print YangSoo Report LONGTERM Test Only         ",
        "Print YangSoo Report STEP and LONGTERM Test ... "
    ]

    injector = YangSooPrinter("d:\\05_Send\\")
    injector.initial_delete_output_file(r"c:/Users/minhwasoo/Documents/")

    menu = ConsoleMenu(menu_options)
    selected_option = menu.run()

    if "STEP" in selected_option:
        print("STEP and LongTerm Test ...")
        injector.process_files("STEP")
    else:
        print("LONGTERM Test Only ...")
        injector.process_files("LONGTERM")

    # name = input("Program is Terminated and check console message ... ")


if __name__ == "__main__":
    main()
