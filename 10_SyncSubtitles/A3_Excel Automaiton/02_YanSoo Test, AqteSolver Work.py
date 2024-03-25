import win32com.client as win32
import time
import pandas as pd
import subprocess
import pyautogui
import re
import os
import random
import shutil
import fnmatch
import ctypes
from natsort import natsorted
import GetTSAqtSolverStepTest as GetTS

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
destination_folder = "d:\\06_Send2\\"

ISAQTOPEN = False
DEBUG_YES = False
DELAY = 0.5
IS_BLOCK = True


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def get_well_number(file_name, mode="NUM"):
    well_designation = file_name.split("_")[0]

    if mode == "FULL":
        return well_designation
    elif mode == "NUM":
        return int(well_designation[1:])
    else:
        raise ValueError("Invalid mode. Use 'FULL' or 'NUM'.")


def seperate_path(file_path):
    directory_path = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    return directory_path, base_name


def get_basename_of_path(file_path):
    directory_path = os.path.dirname(file_path)
    return directory_path + "\\"


def get_basename_of_file(file_path):
    base_name = os.path.basename(file_path)
    return base_name



def after_work():
    def move_file(source, destination):
        try:
            # Move the file from source to destination
            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
        except Exception as e:
            print(f"Error moving file: {e}")

    os.chdir(DOCUMENTS)
    files = os.listdir()

    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    datfiles = [f for f in files if f.endswith('.dat')]

    for file in xlsmfiles:
        move_file(DOCUMENTS + file, destination_folder + file)

    for file in datfiles:
        move_file(DOCUMENTS + file, destination_folder + file)



def initial_clear():
    folder_path = r"c:/Users/minhwasoo/Documents/"
    files = os.listdir(folder_path)
    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    aqtfiles = [f for f in files if f.endswith('.aqt')]
    datfiles = [f for f in files if f.endswith('.dat')]

    def delete_files(files):
        if files:
            for file in files:
                print(file)
                if os.path.exists(folder_path + file):
                    os.remove(folder_path + file)
                    print(f"{file} has been removed successfully.")
                else:
                    print(f"The file {file} does not exist in the folder {folder_path}.")

    delete_files(xlsmfiles)
    delete_files(aqtfiles)
    delete_files(datfiles)


def click_excel_button(ws, button_name):
    button = None
    for obj in ws.OLEObjects():
        if obj.Name == button_name:
            button = obj
            break

    # If button is found, click it
    if button:
        button.Object.Value = True


# inject_value_to_sheet(DIRECTORY + file, well)
def inject_value_to_sheet(file_path, file_name, well):
    try:
        def duplicate_file(well):
            dest_file = DIRECTORY + f"w{well}_02_long_01.aqt"
            shutil.copyfile(DIRECTORY + f"w{well}_02_long.aqt", dest_file)

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_path + file_name)
        excel.Visible = True

        duplicate_file(well)

        # StepTest
        # Input - 3,  SkinFactor - 4, SafeYield - 5, StepTest - 6, LongTest - 7
        # Step.Select - 8, Janggi.Select - 9, Recover.Select - 10

        ws_skin = wb.Worksheets(4)
        ws_LongTest = wb.Worksheets(7)
        ws_step = wb.Worksheets(8)
        ws_janggi = wb.Worksheets(9)
        ws_recover = wb.Worksheets(10)

        # d:\05_Send\w9_01_step.aqt
        # d:\05_Send\w9_02_long.aqt
        # d:\05_Send\w9_02_long_01.aqt
        # d:\05_Send\w9_03_recover.aqt

        ws_step.Activate()
        os.chdir(DIRECTORY)

        click_excel_button(ws_step, "CommandButton1")
        time.sleep(1)
        val_T, val_S = GetTS.AqtesolverMain(f"w{well}_01_step.aqt", 1)
        print(val_T, val_S)


        # 장기양수시험일보에서, 안정수위 도달시간 세팅 랜덤으로 ...

        ws_LongTest.Activate()
        values = [720, 780, 840]
        selected_value = random.choice(values)
        ws_LongTest.OLEObjects("ComboBox1").Object.Value = selected_value


        # 장기 1단계 양수시험, T,S 구하기
        ws_janggi.Activate()
        click_excel_button(ws_janggi, "CommandButton4")
        time.sleep(0.5)
        # toggle radius click
        click_excel_button(ws_janggi, "CommandButton1")
        time.sleep(1)
        val_T, val_S = GetTS.AqtesolverMain(f"w{well}_02_long.aqt", 2)
        print(val_T, val_S)

        ws_skin.Activate()
        ws_skin.Range("D5").Value = val_T
        ws_skin.Range("E10").Value = val_S
        time.sleep(0.5)



        # 장기 2단계 양수시험, T,S 구하기
        ws_janggi.Activate()
        click_excel_button(ws_janggi, "CommandButton2")
        time.sleep(1)
        val_T, val_S = GetTS.AqtesolverMain(f"w{well}_02_long_01.aqt",3)
        print(val_T, val_S)

        ws_skin.Activate()
        ws_skin.Range("I16").Value = val_S
        time.sleep(0.5)



        # 회복 양수시험, T,S 구하기
        ws_recover.Activate()
        click_excel_button(ws_recover, "CommandButton1")
        time.sleep(1)
        val_T, val_S = GetTS.AqtesolverMain(f"w{well}_03_recover.aqt", 4)
        print(val_T, val_S)

        ws_skin.Activate()
        ws_skin.Range("H13").Value = val_T
        ws_skin.Range("I13").Value = val_S
        time.sleep(0.5)

        # click_excel_button(ws_recover, "CommandButton2")

        excel.ScreenUpdating = True

        try:
            wb.DisplayAlerts = False
            # helpful if saving multiple times to save file, it means you won't get a pop-up for overwrite and will default to save it.
            wb.SaveAs(DOCUMENTS + "out_" + file_name, FileFormat=52, CreateBackup=False)

            # wb.Close(SaveChanges=True)
        except Exception as e:
            print("failed to save the excel file")
            print(str(e))
        finally:
            wb.Close(SaveChanges=True)
            excel.Quit()
            excel = None


    except Exception as e:
        print(f"An error occurred, {file_name} : ", e)


def main():
    os.chdir(DIRECTORY)
    files = os.listdir()

    xlsmfiles = [f for f in files if f.endswith('.xlsm')]
    xlsmfiles = fnmatch.filter(xlsmfiles, "*_ge_OriginalSaveFile.xlsm")
    xlsmfiles = natsorted(xlsmfiles)

    user32 = ctypes.windll.user32
    if IS_BLOCK:
        user32.BlockInput(True)

    for file in xlsmfiles:
        initial_clear()
        well = extract_number(file)
        inject_value_to_sheet(DIRECTORY, file, well)
        after_work()
        time.sleep(2)

    if IS_BLOCK:
        user32.BlockInput(False)


# def main():
#     def duplicate_aqt_janggi(aqtfiles):
#         wfiles = fnmatch.filter(aqtfiles, f"*long*.aqt")
#         if wfiles:
#             for file in wfiles:
#                 duplicate_file(DIRECTORY + file)
#
#         return None
#
#     initial_clear()
#     os.chdir(DIRECTORY)
#     files = os.listdir()
#
#     xlsmfiles = [f for f in files if f.endswith('.xlsm')]
#     aqtfiles = [f for f in files if f.endswith('.aqt')]
#     aqtfiles = natsorted(aqtfiles)
#
#     duplicate_aqt_janggi(aqtfiles)
#
#     xlsmfiles = fnmatch.filter(xlsmfiles, "*_ge_OriginalSaveFile.xlsm")
#     xlsmfiles = natsorted(xlsmfiles)
#
#     if xlsmfiles:
#         for file in xlsmfiles:
#             well = extract_number(file)
#
#             #open excel sheet by well
#
#             do_step_test(well)
#             do_longTerm_test(well)
#             do_recover_test(well)


# 1, Step Test
# 2, LongTerm 01 Test
# 3, LongTerm 02 Test
# 4, Recover Test


if __name__ == "__main__":
    main()







