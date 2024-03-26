import win32com.client
import win32com.client as win32
import time
import pandas as pd
import re
import os
from natsort import natsorted

DIRECTORY = "d:\\05_Send\\"
DEBUG_YES = True


def get_excel_row(df, row_index):
    result = []
    result = df.iloc[row_index, :].tolist()
    return result


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def run_excel_macro(excel, wb, macro_name):
    excel.Application.Run("'" + wb.Name + "'!" + macro_name)
    return None


def click_excel_button(ws, button_name):
    button = None
    for obj in ws.OLEObjects():
        if obj.Name == button_name:
            button = obj
            break

    # If button is found, click it
    if button:
        button.Object.Value = True


def PressPumpingTestOnly(file_name):
    try:
        excel = win32.gencache.EnsureDispatch('Excel.Application')
        # excel = win32.Dispatch('Excel.Application')

        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_name)
        excel.Visible = True

        excel.WindowState = -4137  # xlMaximizedWindow

        ws = wb.Worksheets("Input")
        ws.Activate()

        click_excel_button(ws, "CommandButton1")
        if DEBUG_YES: print('Input,  PumpingTest_Button1')
        time.sleep(1)

        excel.ScreenUpdating = True
        sheet = None
        wb.Close(SaveChanges=True)
        excel.Quit()
        time.sleep(2)
        excel = None
    except Exception as e:
        print(f"An error occurred, {file_name} : ", e)


def inject_value_to_sheet(file_name):
    try:
        # excel = win32com.client.Dispatch("Excel.Application")
        # excel = win32com.client.gencache.EnsureDispatch("Excel.Application")

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        # excel = win32.Dispatch('Excel.Application')

        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_name)
        excel.Visible = True

        excel.WindowState = -4137  # xlMaximizedWindow

        ws = wb.Worksheets("Input")
        ws.Activate()

        click_excel_button(ws, "CommandButton2")
        if DEBUG_YES: print('Input, SetCB1_Button2')
        time.sleep(1)
        click_excel_button(ws, "CommandButton3")
        if DEBUG_YES: print('Input, SetCB2_Button3')
        time.sleep(1)
        click_excel_button(ws, "CommandButton6")
        if DEBUG_YES: print('Input, Chart_Button6')
        time.sleep(1)
        click_excel_button(ws, "CommandButton1")
        # PumpingTest Click
        if DEBUG_YES: print('Input, PumpingTest_Button1')
        time.sleep(1)

        # StepTest Fit
        ws = wb.Worksheets("stepTest")
        ws.Activate()

        time.sleep(1)

        click_excel_button(ws, "CommandButton1")
        if DEBUG_YES: print('Step, FindAnswer_Button1')
        time.sleep(2)
        click_excel_button(ws, "CommandButton2")
        if DEBUG_YES: print('Step, Check_Button2')
        time.sleep(1)

        # LongTermTes
        ws = wb.Worksheets("LongTest")
        ws.Activate()

        time.sleep(1)
        click_excel_button(ws, "CommandButton5")
        if DEBUG_YES: print('Long, Reset 0.1_Button5')
        time.sleep(2)
        click_excel_button(ws, "CommandButton4")
        if DEBUG_YES: print('Long, FindAnswer_Button5')
        time.sleep(1)
        click_excel_button(ws, "CommandButton7")
        if DEBUG_YES: print('Long, Check_Button7')

        excel.ScreenUpdating = True
        sheet = None
        wb.Close(SaveChanges=True)
        excel.Quit()
        excel = None
    except Exception as e:
        print(f"An error occurred, {file_name} : ", e)


def main():
    os.chdir(DIRECTORY)
    files = os.listdir()

    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    xlsmfiles = natsorted(xlsmfiles)

    for file in xlsmfiles:
        print('Processing file: ', file)
        PressPumpingTestOnly(DIRECTORY + file)


if __name__ == "__main__":
    main()
