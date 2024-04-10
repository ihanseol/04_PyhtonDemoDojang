# ********************************************************************************************
# 2024.3.25
# 이파일을 양수시험 2단계 로서
# 필요한것은, 양수시험 XLSM 파일과, AQTESOLVER FIle 3가지가 필요하다. 단계 , 장기, 회복
# 하나하나 데이타를 써주는 1차작업을 한다.
# 작업디렉토리는 D:\05_Send 가 되고
# 이곳에다가, xlsm 파일, 그 공에 해당하는 aqt 파일 3개 ( 단계, 장기, 회복 ) 이렇게 넣어두고
# 기존에 수작업으로 하던 작업을, 이것으로 자동으로 돌려주게 된다.
# 그러면, 양수시험을 해서 ..
# T1, T2, S1, S2 를 획득하게 되어, 그것을 엑셀파일에 모두 반영하고
# 그 엑셀파일을, 다시 저장하게 된다.
# 단 한가지, 엑셀파일 저장은 수작업으로 해야한다.
#
# ********************************************************************************************

import win32com.client as win32
import time
import re
import os
import shutil
import fnmatch
import ctypes
from natsort import natsorted
import Get_TS_from_AQTESOLV_OCR as GetTS

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
destination_folder = "d:\\06_Send2\\"

DEBUG_YES = True
DELAY = 0.5
IS_BLOCK = False


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

    def delete_files(_files):
        if _files:
            for file in _files:
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


def inject_value_to_sheet(file_path, file_name, well):
    try:
        def duplicate_file(_well):
            dest_file = DIRECTORY + f"w{_well}_02_long_01.aqt"
            shutil.copyfile(DIRECTORY + f"w{_well}_02_long.aqt", dest_file)

        def InjecttionStep(_ws_step):
            print('**************************************************')
            print('*  StepTest Starting ....                        *')
            print('**************************************************')

            _ws_step.Activate()
            os.chdir(DIRECTORY)

            click_excel_button(_ws_step, "CommandButton1")
            if DEBUG_YES:
                print('Step.Select,  StepPrn_Button1')
            time.sleep(1)
            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_01_step.aqt")
            time.sleep(1)
            print(val_T, val_S)

        def InjecttionLongTest_01(_ws_janggi, _ws_skin):
            print('**************************************************')
            print('*  LongTermTest Phase 1 Starting ....            *')
            print('**************************************************')

            # 장기 1단계 양수시험, T,S 구하기
            _ws_janggi.Activate()

            # toggle radius click
            click_excel_button(_ws_janggi, "CommandButton4")
            if DEBUG_YES:
                print('Janggi.Select,  ToggleRadius_Button4')
            time.sleep(1)

            click_excel_button(_ws_janggi, "CommandButton1")
            if DEBUG_YES:
                print('Janggi.Select,  JangGi*01_Button1')
            time.sleep(1)

            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_02_long.aqt")
            print(val_T, val_S)

            _ws_skin.Activate()
            _ws_skin.Range("D5").Value = val_T
            _ws_skin.Range("E10").Value = val_S
            time.sleep(1)

        def InjecttionLongTest_02(_ws_janggi, _ws_skin):
            print('**************************************************')
            print('*  LongTermTest Phase 2 Starting ....            *')
            print('**************************************************')

            # 장기 2단계 양수시험, T,S 구하기
            _ws_janggi.Activate()
            click_excel_button(_ws_janggi, "CommandButton2")
            if DEBUG_YES:
                print('Janggi.Select,  JangGi*02_Button2')
            time.sleep(1)
            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_02_long_01.aqt")
            print(val_T, val_S)

            _ws_skin.Activate()
            _ws_skin.Range("I16").Value = val_S
            time.sleep(1)

        def InjectionRecover(_ws_recover, _ws_skin):
            print('**************************************************')
            print('*  RecoverTest Starting ....                     *')
            print('**************************************************')

            # 회복 양수시험, T,S 구하기
            _ws_recover.Activate()
            click_excel_button(_ws_recover, "CommandButton1")
            if DEBUG_YES:
                print('Recover.Select,  Recover Prn_Button1')
            time.sleep(1)
            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_03_recover.aqt")
            print(val_T, val_S)

            _ws_skin.Activate()
            _ws_skin.Range("H13").Value = val_T
            _ws_skin.Range("I13").Value = val_S


        def IsStepFileExist(_well):
            # w1_01_step.aqt
            os.chdir(DIRECTORY)
            files = os.listdir()
            aqtfiles = [f for f in files if f.endswith('.aqt')]
            aqtfiles = fnmatch.filter(aqtfiles, f"w{_well}_01_step.aqt")

            if aqtfiles:
                return True
            else:
                return False

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_path + file_name)
        excel.Visible = True

        # 여기서 well 은 숫자, 공별숫자이다.
        duplicate_file(well)

        # StepTest
        # Input * 3,  SkinFactor * 4, SafeYield * 5, StepTest * 6, LongTest * 7
        # Step.Select * 8, Janggi.Select * 9, Recover.Select * 10

        ws_skin = wb.Worksheets(4)
        ws_step = wb.Worksheets(8)
        ws_janggi = wb.Worksheets(9)
        ws_recover = wb.Worksheets(10)

        if IsStepFileExist(well):
            InjecttionStep(ws_step)

        InjecttionLongTest_01(ws_janggi, ws_skin)
        InjecttionLongTest_02(ws_janggi, ws_skin)
        InjectionRecover(ws_recover, ws_skin)

        time.sleep(3)

        # click_excel_button(ws_recover, "CommandButton2")

        excel.ScreenUpdating = True

        try:
            wb.DisplayAlerts = False
            # helpful if saving multiple times to save file, it means you won't get a pop up for overwrite and will default to save it.
            wb.SaveAs(DOCUMENTS + "out_" + file_name, FileFormat=52, CreateBackup=False)

            # wb.Close(SaveChanges=True)
        except Exception as e:
            print("failed to save the excel file")
            print(str(e))
        finally:
            wb.Close(SaveChanges=True)
            excel.Quit()

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


# 1, Step Test
# 2, LongTerm 01 Test
# 3, LongTerm 02 Test
# 4, Recover Test


if __name__ == "__main__":
    main()
