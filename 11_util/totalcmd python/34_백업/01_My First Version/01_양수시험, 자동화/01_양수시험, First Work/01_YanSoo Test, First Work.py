"""

# *************************************************************************
# 2024.3.25
# 이파일을 양수시험 1단계 로서
# 관정스펙을 읽어서 YangSoo.xlsx
# 하나하나 데이타를 써주는 1차작업을 한다.
# gong  hp  casing  well_rad    simdo   q   natual  stable
# 공번, 마력, 케이싱, 구경, 심도, 양수량, 자연수위, 안정수위
#
# 에러처리를 위해서, 버튼클릭함수를 에러처리를 추가해서 변경해주고
# 입력시트에서 자연수위, 안정수위로 에러가나는것을 방지해주기 위해 처리해줌
#
# *************************************************************************
"""


import win32com.client as win32
import win32api
import time
import pandas as pd
import re
import os
import random
import pyautogui
from natsort import natsorted
import pygetwindow as gw

DIRECTORY = "d:\\05_Send\\"
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
DEBUG_YES = True


def get_excel_row(df, row_index):
    result = []
    result = df.iloc[row_index, :].tolist()
    return result


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def inject_value_to_cells(book):
    # cell_values = {"I48": hp, "I52": casing, "M44": well_rad, "M45": simdo, "M48": natural, "M49": stable, "M51": q}

    def make_cell_values(row_index):
        row_data = get_excel_row(df, row_index)

        hp = row_data[1]
        casing = row_data[2]
        well_rad = row_data[3]

        simdo = row_data[4]
        q = row_data[5]
        natural = row_data[6]
        stable = row_data[7]

        gong = extract_number(row_data[0])
        str_gong = f"공  번 : W - {gong}"

        return {"J48": str_gong, "I52": casing, "I48": hp, "M44": well_rad, " M45": simdo, "M48": natural,
                "M49": stable, "M51": q}

    sheet = book.Worksheets("Input")

    filename = os.path.basename(book.Name)
    row_index = extract_number(filename) - 1

    if DEBUG_YES: print(f'inject value to cell , processing make_cell_values ...')
    cell_values = make_cell_values(row_index)

    sheet.Range("M49").Value = 300
    # inject 300 stable level, for block error occuring ...

    for cell, value in cell_values.items():
        sheet.Range(cell).Value = value

    if DEBUG_YES: print(f'inject value to cell , finished ...')
    return None


def run_excel_macro(excel, wb, macro_name):
    excel.Application.Run("'" + wb.Name + "'!" + macro_name)
    return None


def click_excel_button(ws, button_name):
    def click_button():
        for obj in ws.OLEObjects():
            if obj.Name == button_name:
                obj.Object.Value = True
                break

    try:
        click_button()
    except Exception as e:
        print(f"{ws} - {button_name} : Error in Button Click Function", e)
    finally:
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        click_button()


def change_window(name_title) -> None:
    gwindows = gw.getWindowsWithTitle(name_title)

    if gwindows:
        window = gwindows[0]
        window.activate()
        if not window.isMaximized:
            window.maximize()
    else:
        print(f"No  {name_title} found.")


def inject_value_to_sheet(file_name):
    try:
        def InjectionInput():
            ws = wb.Worksheets("Input")
            ws.Activate()
            time.sleep(1)

            inject_value_to_cells(wb)

            excel.ActiveWindow.LargeScroll(Down=-1)
            time.sleep(1)

            click_excel_button(ws, "CommandButton2")
            if DEBUG_YES: print('Input, Set_CB1 - Button2')
            time.sleep(1)
            click_excel_button(ws, "CommandButton3")
            if DEBUG_YES: print('Input, Set_CB2 - Button3')
            time.sleep(1)
            click_excel_button(ws, "CommandButton6")
            if DEBUG_YES: print('Input, Chart - Button6')
            time.sleep(1)
            click_excel_button(ws, "CommandButton1")
            # PumpingTest Click
            if DEBUG_YES: print('Input, PumpingTest - Button1')
            time.sleep(1)

        def InjectionStepTest():
            # StepTest Fit
            ws = wb.Worksheets("stepTest")
            ws.Activate()
            time.sleep(1)

            click_excel_button(ws, "CommandButton1")
            if DEBUG_YES: print('StepTest, FindAnswer - Button1')
            time.sleep(2)
            click_excel_button(ws, "CommandButton2")
            if DEBUG_YES: print('StepTest, Check - Button2')
            time.sleep(1)

        def InjectionLongTermTest():
            # LongTermTes
            ws = wb.Worksheets("LongTest")
            ws.Activate()

            if ws.Range("M13").Value != 0: ws.Range("M13").Value = 0

            values = [720, 780, 840]
            selected_value = random.choice(values)
            ws.OLEObjects("ComboBox1").Object.Value = selected_value
            if DEBUG_YES: print(f'LongTest, Assign {selected_value} at ComboBox')

            time.sleep(1)
            click_excel_button(ws, "CommandButton5")
            if DEBUG_YES: print('LongTest, Reset 0.1 - Button5')
            time.sleep(1)
            click_excel_button(ws, "CommandButton4")
            if DEBUG_YES: print('LongTest, FindAnswer - Button4')
            time.sleep(2)
            click_excel_button(ws, "CommandButton7")
            if DEBUG_YES: print('LongTest, Check - Button7')

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        # excel = win32.Dispatch('Excel.Application')

        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_name)
        excel.Visible = True
        excel.WindowState = -4137  # xlMaximizedWindow
        change_window('Excel')

        InjectionInput()
        InjectionStepTest()
        InjectionLongTermTest()

        excel.ScreenUpdating = True
        sheet = None
        wb.Close(SaveChanges=True)
        excel.Quit()
        if DEBUG_YES: print(f'FileSaving , {file_name} ....')
        time.sleep(3)

        excel = None
    except Exception as e:
        print(f"An error occurred, {file_name} : ", e)


def initial_delete_ouputfile():
    folder_path = r"c:/Users/minhwasoo/Documents/"
    files = os.listdir(folder_path)
    xlsmfiles = [f for f in files if f.endswith('.xlsm')]

    if xlsmfiles:
        for file in xlsmfiles:
            print(file)

            if os.path.exists(folder_path + file):
                os.remove(folder_path + file)
                print(f"{file} has been removed successfully.")
            else:
                print(f"The file {file} does not exist in the folder {folder_path}.")

    time.sleep(1)


def main():
    initial_delete_ouputfile()
    os.chdir(DIRECTORY)
    files = os.listdir()

    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    xlsmfiles = natsorted(xlsmfiles)

    for file in xlsmfiles:
        print('Processing file: ', file)
        inject_value_to_sheet(DIRECTORY + file)


if __name__ == "__main__":
    main()
