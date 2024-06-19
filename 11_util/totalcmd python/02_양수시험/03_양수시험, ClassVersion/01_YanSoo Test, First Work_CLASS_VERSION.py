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
# *************************************************************************
"""
from typing import Any

import win32com.client as win32
import time
import pandas as pd
import re
import os
import random
from natsort import natsorted
import pyautogui
import pygetwindow as gw


class YangSooInjector:
    def __init__(self, directory):
        self.directory = directory
        # self.spec_file = spec_file
        self.df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
        # self.df = pd.read_excel(spec_file)
        self.debug_yes = True
        self.STABLE_TIME = 0
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
        def click_button():
            for obj in ws.OLEObjects():
                if obj.Name == button_name:
                    obj.Object.Value = True
                    break

        while True:
            try:
                click_button()
                break  # Exit the loop if no exception is raised
            except Exception as e:
                print(f"{ws} - {button_name} : Error in Button Click Function", e)
                time.sleep(1)  # Optional: Wait a bit before retrying
            finally:
                self.change_window('EXCEL')
                time.sleep(1)
                pyautogui.press('enter')
                time.sleep(1)

    def get_excel_row(self, row_index):
        try:
            r_value = self.df.iloc[row_index, :].tolist()
        except IndexError:
            return None

        return r_value

    def make_cell_values(self, row_index):

        row_data: bool | Any = self.get_excel_row(row_index)

        if row_data is None: return None

        len_row_data = len(row_data)
        print('len(row_data):', len_row_data)

        address = row_data[1]
        hp = row_data[2]
        casing = row_data[3]
        well_rad = row_data[4]
        simdo = row_data[5]
        q = row_data[6]
        natural = row_data[7]
        stable = row_data[8]

        project_name = ''
        jigu_name = ''
        company_name = ''
        self.STABLE_TIME = row_data[12]

        if len_row_data > 9:
            project_name = row_data[9]
            jigu_name = row_data[10]
            company_name = row_data[11]

        # 2024년 6월 15일 추가
        # 조사명, 지구명을 추가해줌,  YanSoo.xlsx 파일에 ...

        # 안정수위가 자연수위보다 낮을경우 .... 자연수위와 안정수위를 바꿔 준다. 에러방지를 위해서
        if stable < natural:
            natural = row_data[7]
            stable = row_data[6]

        gong = self.extract_number(row_data[0])
        str_gong = f"공  번 : W - {gong}"

        time.sleep(1)

        if len_row_data <= 9:
            return {"J48": str_gong, "I46": address, "I52": casing, "I48": hp, "M44": well_rad, "M45": simdo,
                    "M48": natural, "M49": stable, "M51": q}
        else:
            return {"J48": str_gong, "I46": address, "I52": casing, "I48": hp, "M44": well_rad, "M45": simdo,
                    "M48": natural, "M49": stable, "M51": q, "I44": project_name, "I45": jigu_name, "I47": company_name}

    def inject_value_to_cells(self, book):
        sheet = book.Worksheets("Input")
        filename = os.path.basename(book.Name)
        row_index = self.extract_number(filename) - 1
        if self.debug_yes: print('inject value to cell, processing make_cell_values...')

        cell_values = self.make_cell_values(row_index)
        if cell_values is None:
            return None

        sheet.Range("M49").Value = 300  # 안정수위를 일단 300으로 , 에러를 차단하기 위해서 ...

        for cell, value in cell_values.items():
            print(f'inject_value_to_cells : {cell} - {value}')
            sheet.Range(cell).Value = value
            time.sleep(1)

        if self.debug_yes: print('inject value to cell, finished...')

    def inject_values(self, wb, excel):
        if self.debug_yes: print('inject value to cell, _inject_input is started ...')
        result = self._inject_input(wb)

        if result is None:
            return None

        if self.debug_yes: print('inject step test ...')
        self._inject_step_test(wb)

        if self.debug_yes: print('inject long term test ...')
        self._inject_long_term_test(wb, excel)

    def _inject_input(self, wb):
        ws = wb.Worksheets("Input")
        ws.Activate()
        time.sleep(1)
        result = self.inject_value_to_cells(wb)

        if result is None:
            return None
        else:
            time.sleep(1)

        print('_inject_input -- SetCB1 ')
        self.click_excel_button(ws, "CommandButton2")
        time.sleep(1)

        print('_inject_input -- SetCB2 ')
        self.click_excel_button(ws, "CommandButton3")
        time.sleep(1)

        print('_inject_input -- Chart Fitting')
        self.click_excel_button(ws, "CommandButton6")

        print('_inject_input -- PumpingTest ')
        time.sleep(1)
        self.click_excel_button(ws, "CommandButton1")

    def _inject_step_test(self, wb):
        ws = wb.Worksheets("stepTest")
        ws.Activate()
        time.sleep(1)

        print('_inject_step_test -- FindAnswer Button ')
        self.click_excel_button(ws, "CommandButton1")
        time.sleep(2)

        print('_inject_step_test -- Check Button ')
        self.click_excel_button(ws, "CommandButton2")

    def _inject_long_term_test(self, wb, excel):
        ws = wb.Worksheets("LongTest")
        ws.Activate()
        values = [540, 600, 660, 720, 780, 840]

        # Clear GoalSeekTarget
        ws.Range("GoalSeekTarget").Value = 0

        if self.STABLE_TIME == 0:
            selected_value = random.choice(values)
        else:
            selected_value = self.STABLE_TIME

        if self.debug_yes: print(f'stable time selection ... : {selected_value}')

        print('_inject_long_term_test -- Reset 0.1')
        self.click_excel_button(ws, "CommandButton5")  # Reset 0.1
        time.sleep(1)

        ws.OLEObjects("ComboBox1").Object.Value = selected_value
        time.sleep(1)

        print('_inject_long_term_test -- excel.Application.Run("mod_W1LongtermTEST.TimeSetting")')
        excel.Application.Run("mod_W1LongtermTEST.TimeSetting")
        time.sleep(1)

        print('_inject_long_term_test -- Reset 0.1')
        self.click_excel_button(ws, "CommandButton5")  # Reset 0.1
        time.sleep(1)

        print('_inject_long_term_test -- FindAnswer')
        self.click_excel_button(ws, "CommandButton4")  # Find Answer
        time.sleep(2)

        print('_inject_long_term_test -- Check')
        self.click_excel_button(ws, "CommandButton7")  # Check

    def data_validation(self):
        os.chdir(self.directory)
        files = natsorted([f for f in os.listdir() if f.endswith('.xlsm')])

        if files:
            last_file = files[-1]
            print("The last Excel file is:", last_file)
        else:
            last_file = ''
            print("No .xlsm files found.")

        row_index = self.extract_number(last_file) - 1
        check = self.get_excel_row(row_index)

        if check is None:
            return None
        else:
            return files

    def process_files(self):
        self.countdown(5)

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
            result = self.inject_values(wb, excel)

            if result is None:
                print("Index Does not match, DataSheet and YangSoo file ...")
                wb.Close(SaveChanges=False)
                excel.ScreenUpdating = True
                excel.Quit()
                return None
            else:
                wb.Close(SaveChanges=True)

        excel.ScreenUpdating = True
        excel.Quit()
        if self.debug_yes: print('All files processed.')

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
        xlsm_files = [f for f in files if f.endswith('.xlsm')]

        for file in xlsm_files:
            file_path = os.path.join(folder_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file} has been removed successfully.")
            else:
                print(f"The file {file} does not exist in the folder {folder_path}.")


def main():
    injector = YangSooInjector("d:\\05_Send\\")
    injector.initial_delete_output_file(r"c:/Users/minhwasoo/Documents/")
    injector.process_files()
    name = input("Program is Terminated and check console message ... ")


if __name__ == "__main__":
    main()
