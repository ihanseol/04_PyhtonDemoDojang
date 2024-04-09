import os
import re
import time
import shutil
import ctypes
import GetTSAqtSolverStepTest as GetTS
import win32com.client as win32
from natsort import natsorted
import fnmatch

# Configuration
DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
DESTINATION_FOLDER = "d:\\06_Send2\\"
DEBUG_YES = False
DELAY = 0.5
IS_BLOCK = True


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def move_file(source, destination):
    try:
        shutil.move(source, destination)
        print(f"File moved successfully from '{source}' to '{destination}'")
    except Exception as e:
        print(f"Error moving file: {e}")


def initial_clear():
    folder_path = r"c:/Users/minhwasoo/Documents/"
    files = os.listdir(folder_path)
    extensions = ['.xlsm', '.aqt', '.dat']

    for ext in extensions:
        matching_files = [f for f in files if f.endswith(ext)]
        for file in matching_files:
            file_path = os.path.join(folder_path, file)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"{file} has been removed successfully.")
            else:
                print(f"The file {file} does not exist in the folder {folder_path}.")


def click_excel_button(ws, button_name):
    button = None
    for obj in ws.OLEObjects():
        if obj.Name == button_name:
            button = obj
            break

    if button:
        button.Object.Value = True


def duplicate_file(well):
    try:
        src_file = DIRECTORY + f"w{well}_02_long.aqt"
        dest_file = DIRECTORY + f"w{well}_02_long_01.aqt"
        shutil.copyfile(src_file, dest_file)
        print(f"File duplicated successfully from '{src_file}' to '{dest_file}'")
    except Exception as e:
        print(f"Error duplicating file: {e}")


def inject_values_to_sheet(file_path, file_name, well):
    try:
        def inject_step_test(ws_step):
            print('**************************************************')
            print('*  StepTest Starting ....                        *')
            print('**************************************************')

            ws_step.Activate()
            os.chdir(DIRECTORY)
            click_excel_button(ws_step, "CommandButton1")
            if DEBUG_YES: print('Step.Select,  StepPrn_Button1')
            time.sleep(1)
            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_01_step.aqt", 1)

            print(val_T, val_S)

        def inject_long_test_phase_1(ws_janggi, ws_skin):
            print('**************************************************')
            print('*  LongTermTest Phase 1 Starting ....            *')
            print('**************************************************')

            ws_janggi.Activate()

            click_excel_button(ws_janggi, "CommandButton4")
            if DEBUG_YES: print('Janggi.Select,  ToggleRadius_Button4')
            time.sleep(1)

            click_excel_button(ws_janggi, "CommandButton1")
            if DEBUG_YES: print('Janggi.Select,  JangGi*01_Button1')
            time.sleep(1)

            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_02_long.aqt", 2)
            print(val_T, val_S)

            ws_skin.Activate()
            ws_skin.Range("D5").Value = val_T
            ws_skin.Range("E10").Value = val_S
            time.sleep(1)

        def inject_long_test_phase_2(ws_janggi, ws_skin):
            print('**************************************************')
            print('*  LongTermTest Phase 2 Starting ....            *')
            print('**************************************************')

            ws_janggi.Activate()
            click_excel_button(ws_janggi, "CommandButton2")
            if DEBUG_YES: print('Janggi.Select,  JangGi*02_Button2')
            time.sleep(1)

            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_02_long_01.aqt", 3)
            print(val_T, val_S)

            ws_skin.Activate()
            ws_skin.Range("I16").Value = val_S
            time.sleep(0.5)

        def inject_recover_test(ws_recover, ws_skin):
            print('**************************************************')
            print('*  RecoverTest Starting ....                     *')
            print('**************************************************')

            ws_recover.Activate()
            click_excel_button(ws_recover, "CommandButton1")
            if DEBUG_YES: print('Recover.Select,  Recover Prn_Button1')
            time.sleep(1)

            val_T, val_S = GetTS.AqtesolverMain(f"w{well}_03_recover.aqt", 4)
            print(val_T, val_S)

            ws_skin.Activate()
            ws_skin.Range("H13").Value = val_T
            ws_skin.Range("I13").Value = val_S
            time.sleep(0.5)

        def is_step_file_exist(well):
            files = os.listdir()
            aqt_files = fnmatch.filter(files, f"w{well}_01_step.aqt")
            return bool(aqt_files)

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False
        wb = excel.Workbooks.Open(file_path + file_name)
        excel.Visible = True

        duplicate_file(well)

        ws_skin = wb.Worksheets(4)
        ws_step = wb.Worksheets(8)
        ws_janggi = wb.Worksheets(9)
        ws_recover = wb.Worksheets(10)

        if is_step_file_exist(well):
            inject_step_test(ws_step)

        inject_long_test_phase_1(ws_janggi, ws_skin)
        inject_long_test_phase_2(ws_janggi, ws_skin)
        inject_recover_test(ws_recover, ws_skin)

        excel.ScreenUpdating = True

        try:
            wb.DisplayAlerts = False
            wb.SaveAs(DOCUMENTS + "out_" + file_name, FileFormat=52, CreateBackup=False)
        except Exception as e:
            print("Failed to save the Excel file")
            print(str(e))
        finally:
            wb.Close(SaveChanges=True)
            excel.Quit()
            excel = None

    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    os.chdir(DIRECTORY)
    xlsm_files = [f for f in os.listdir() if f.endswith('.xlsm')]
    xlsm_files = fnmatch.filter(xlsm_files, "*_ge_OriginalSaveFile.xlsm")
    xlsm_files = natsorted(xlsm_files)

    user32 = ctypes.windll.user32
    if IS_BLOCK:
        user32.BlockInput(True)

    for file in xlsm_files:
        initial_clear()
        well = extract_number(file)
        inject_values_to_sheet(DIRECTORY, file, well)
        after_work()
        time.sleep(2)

    if IS_BLOCK:
        user32.BlockInput(False)


if __name__ == "__main__":
    main()
