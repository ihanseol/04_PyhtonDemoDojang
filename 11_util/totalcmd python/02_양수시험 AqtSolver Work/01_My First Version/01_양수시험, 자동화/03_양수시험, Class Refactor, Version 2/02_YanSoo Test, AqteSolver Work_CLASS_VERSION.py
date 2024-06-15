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
#
#
#  2024.6.15
#  오늘, 에러를 수정하고, 에러가 날수있는 부분의 차단을 위해, 엑셀파일의 SetCB1, SetCB2 부분수정, 차트 수정등
# 여러가지를 마무리 지었따.
#
# ********************************************************************************************


import time
import re
import os
import shutil
import fnmatch
import ctypes
from natsort import natsorted
import pyautogui
import pygetwindow as gw
import sys
import win32com.client as win32

sys.path.append(
    "c:/Program Files/totalcmd/ini/02_python/02_양수시험 AqtSolver Work/01_My First Version/01_양수시험, 자동화/03_양수시험, Class Refactor, Version 2/")
import Get_TS_from_AQTESOLV_OCR_CLASS_VERSION as GetTS


class AQTBASE:
    def __init__(self):
        self.AQTESOLV_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
        self.SEND = "d:\\05_Send\\"
        self.SEND2 = "d:\\06_Send2\\"
        self.ISAQTOPEN = False
        self.DEBUG_YES = True
        self.DELAY = 0.5
        self.IS_BLOCK = False
        """
            self.IS_BLOCK = False :
            
             because while run the program cause block or wait for user input
             then cann't do anything
             so it must be False, userinput allowed ...
        """


class FileProcessing(AQTBASE):
    def __init__(self, directory="d:\\05_Send\\"):
        super().__init__()
        self._directory = directory
        os.chdir(self._directory)
        self.files = os.listdir(directory)

    @property
    def directory(self):
        """
        directory , getter ...
        :return:
        """
        return self._directory

    @directory.setter
    def directory(self, value) -> None:
        """
        directory , setter
        :param value: setting directory to
        :return: void
        """
        if self._directory != value:  # if _directory changed then refresh files
            self._directory = value
            self.files = os.listdir(value)

    def set_directory(self, directory) -> None:
        """
          Reset the value of the internal directory variable
          Accordingly, the value of the file list is also updated.

            directory and files value refresh

        :param directory:
        :return:
        """
        self._directory = directory
        self.files = os.listdir(directory)

    def get_files_by_extension(self, extension):
        """Returns a list of files with the specified extension."""
        return [f for f in self.files if f.endswith(extension)]

    def get_xlsm_files(self):
        """Returns a list of .xlsm files."""
        return self.get_files_by_extension('.xlsm')

    def get_aqt_files(self):
        """Returns a list of .aqt files."""
        return self.get_files_by_extension('.aqt')

    def get_dat_files(self):
        """Returns a list of .dat files."""
        return self.get_files_by_extension('.dat')

    def get_xlsm_filter(self, path="d:\\05_Send\\", sfilter="*_ge_OriginalSaveFile.xlsm") -> list:
        """
        :param sfilter:
        :param path: the directory where the filter will run
        :paramsfilter: string to filter
        :return:
                list of filtered xlsm files

        """

        self.set_directory(path)
        """ 
            set directory to work
            and refresh files : file list in the path
            so xlsm, aqt, dat files retrived ...         
        """
        xl_files = self.get_xlsm_files()

        xlsmfiles = fnmatch.filter(xl_files, sfilter)
        return natsorted(xlsmfiles)

    @staticmethod
    def has_path(file_name) -> bool:
        """
        file_name has path or not
        if file_name include path like c:\\user\\this ...

        :param file_name: filename
        :return:
            head --> file path
            tail --> file
        """
        head, tail = os.path.split(file_name)
        print(f"head :'{head}'  tail : {tail}  includes a path. Performing action...")

        if head:
            return True
        else:
            return False

    @staticmethod
    def separate_path(file_path):
        directory_path = os.path.dirname(file_path)
        base_name = os.path.basename(file_path)
        return directory_path, base_name

    @staticmethod
    def get_basename_of_path(file_path) -> str:
        return os.path.dirname(file_path) + "\\"

    @staticmethod
    def get_basename_of_file(file_path) -> str:
        return os.path.basename(file_path)

    @staticmethod
    def is_exist(file_path) -> bool:
        """
        is file exisit ... give file_path ...

        :return:
        true --> file exist
        false --> file does not exist

        """
        return os.path.exists(file_path)

    @staticmethod
    def move_file(source, destination) -> None:
        """
        move file source to destination

        :param source:
        :param destination:

        """
        try:
            shutil.move(source, destination)
            print(f"File moved successfully from '{source}' to '{destination}'")
        except Exception as e:
            print(f"Error moving file: {e}")

    @staticmethod
    def delete_files(folder_path, files) -> None:
        try:
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    print(f"{file_name} has been removed successfully from {folder_path}.")
                else:
                    print(f"The file {file_name} does not exist in the folder {folder_path}.")
        except Exception as e:
            print(f"An error occurred while deleting files: {e}")

    def duplicate_aqtfile_long(self, well):
        shutil.copyfile(self.SEND + f"w{well}_02_long.aqt", self.SEND + f"w{well}_02_long_01.aqt")

    def after_work(self):
        self.set_directory(self.DOCUMENTS)
        xlsmfiles = self.get_xlsm_files()
        datfiles = self.get_dat_files()

        for file in xlsmfiles:
            self.move_file(self.DOCUMENTS + file, self.SEND2 + file)

        for file in datfiles:
            self.move_file(self.DOCUMENTS + file, self.SEND2 + file)


class InjectValueToSheet(FileProcessing):
    def __init__(self):
        super().__init__()

    @staticmethod
    def click_excel_button(ws, button_name):
        def find_button():
            for obj in ws.OLEObjects():
                if obj.Name == button_name:
                    return obj
            return None

        button_obj = find_button()
        if button_obj:
            try:
                button_obj.Object.Value = True
                # print(f"Clicked button '{button_name}' successfully in worksheet {ws}.")
            except Exception as e:
                print(f"Error clicking button '{button_name}' in worksheet {ws}: {e}")
        else:
            print(f"Button '{button_name}' not found in worksheet {ws}.")

    def change_window(self, name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)

        if gwindows:
            window = gwindows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            print(f"No  {name_title} found.")

    def InjecttionStep(self, well, ws_step):
        print('**************************************************')
        print(f'*  W{well} - StepTest Starting ....           ')
        print('**************************************************')

        ws_step.Activate()
        os.chdir(self.SEND)

        self.click_excel_button(ws_step, button_name="CommandButton1")
        if self.DEBUG_YES:
            print('Step.Select,  StepPrn_Button1')
        time.sleep(1)

        getTS = GetTS.AQTProcessor('auto')
        val_T, val_S = getTS.AqtesolverMain(file_name=self.SEND + f"w{well}_01_step.aqt")

        print(val_T, val_S)

    def InjecttionLongTest_01(self, well, ws_janggi, ws_skin):
        print('**************************************************')
        print(f'* W{well} - LongTermTest Phase 1 Starting ....')
        print('**************************************************')

        # 장기 1단계 양수시험, T,S 구하기
        ws_janggi.Activate()

        # toggle radius click
        self.click_excel_button(ws_janggi, button_name="CommandButton4")
        if self.DEBUG_YES:
            print('Janggi.Select,  ToggleRadius_Button4')
        time.sleep(1)

        self.click_excel_button(ws_janggi, button_name="CommandButton1")
        if self.DEBUG_YES:
            print('Janggi.Select,  JangGi*01_Button1')
        time.sleep(1)

        getTS = GetTS.AQTProcessor('auto')
        val_T, val_S = getTS.AqtesolverMain(file_name=self.SEND + f"w{well}_02_long.aqt")
        print(val_T, val_S)

        ws_skin.Activate()
        ws_skin.Range("D5").Value = val_T
        ws_skin.Range("E10").Value = val_S
        time.sleep(1)

    def InjecttionLongTest_02(self, well, ws_janggi, ws_skin):
        print('**************************************************')
        print(f'* W{well} - LongTermTest Phase 2 Starting')
        print('**************************************************')

        # 장기 2단계 양수시험, T,S 구하기
        ws_janggi.Activate()
        self.click_excel_button(ws_janggi, button_name="CommandButton2")
        if self.DEBUG_YES:
            print('Janggi.Select,  JangGi*02_Button2')
        time.sleep(1)

        getTS = GetTS.AQTProcessor('auto')
        val_T, val_S = getTS.AqtesolverMain(file_name=self.SEND + f"w{well}_02_long_01.aqt")
        print(val_T, val_S)

        ws_skin.Activate()
        ws_skin.Range("I16").Value = val_S
        time.sleep(0.5)

    def InjectionRecover(self, well, ws_recover, ws_skin, mode='auto'):
        print('**************************************************')
        print(f'* W{well} - RecoverTest Starting')
        print('**************************************************')

        # 회복 양수시험, T,S 구하기
        ws_recover.Activate()
        self.click_excel_button(ws_recover, button_name="CommandButton1")
        if self.DEBUG_YES:
            print('Recover.Select,  Recover Prn_Button1')
        time.sleep(1)

        if mode == 'mannual':
            getTS = GetTS.AQTProcessor('mannual')
            val_T, val_S = getTS.AqtesolverMain(file_name=self.SEND + f"w{well}_03_recover.aqt")
        else:
            getTS = GetTS.AQTProcessor('auto')
            val_T, val_S = getTS.AqtesolverMain(file_name=self.SEND + f"w{well}_03_recover.aqt")

        print(val_T, val_S)

        ws_skin.Activate()
        ws_skin.Range("H13").Value = val_T

        ws_skin.Range("I13").Value = val_S
        time.sleep(0.5)

    def IsStepFileExist(self, well) -> bool:
        path = self.SEND

        self.set_directory(path)
        path_in_aqt_stepfiles = self.get_aqt_files()
        print(path_in_aqt_stepfiles)

        if f"w{well}_01_step.aqt" in path_in_aqt_stepfiles:
            return True
        else:
            return False

    @staticmethod
    def gen_excel_filename(well):
        return f"A{well}_ge_OriginalSaveFile.xlsm"

    def press_and_wait(self, key) -> None:
        pyautogui.press(key)
        time.sleep(self.DELAY)

    def press_and_wait_hotkey(self, key, ctrl_key='alt') -> None:
        pyautogui.hotkey(ctrl_key, key)
        time.sleep(self.DELAY)

    def main_process(self, well, Mode=1) -> None:
        """
            If the input here is received only by the well number - gongbun (well: 1),
            the rest is determined by it.

        mode_functions = {
            1: "automatic_process",
            2: "automatic_with_manual_process",
            3: "recover_manual_test_only"
            4: "run_recover_auto_test_only"
        }


        """

        excel = win32.gencache.EnsureDispatch('Excel.Application')
        excel.ScreenUpdating = False
        xlname = self.SEND + self.gen_excel_filename(well)

        wb = excel.Workbooks.Open(xlname)
        excel.Visible = True
        excel.WindowState = -4137  # maximize window

        # 여기서 well 은 숫자, 공별숫자이다.

        if (Mode != 3) and (Mode != 4):
            self.duplicate_aqtfile_long(well)

        # StepTest
        # Input * 3,  SkinFactor * 4, SafeYield * 5, StepTest * 6, LongTest * 7
        # Step.Select * 8, Janggi.Select * 9, Recover.Select * 10

        ws_skin = wb.Worksheets(4)
        ws_step = wb.Worksheets(8)
        ws_janggi = wb.Worksheets(9)
        ws_recover = wb.Worksheets(10)

        if ((Mode != 3) and (Mode != 4)) and self.IsStepFileExist(well):
            self.InjecttionStep(well, ws_step)

        if ((Mode != 3) and (Mode != 4)) and Mode:
            self.InjecttionLongTest_01(well, ws_janggi, ws_skin)
            self.InjecttionLongTest_02(well, ws_janggi, ws_skin)

        if (Mode == 2 or Mode == 3) and Mode != 4:
            self.InjectionRecover(well, ws_recover, ws_skin, mode='mannual')
            # click_excel_button(ws_recover, "CommandButton2")
        else:
            self.InjectionRecover(well, ws_recover, ws_skin, mode='auto')

        excel.ScreenUpdating = True

        try:
            wb.DisplayAlerts = False
            """
            helpful if saving multiple times to save file, it means you won't get a pop up for overwrite 
            and will default to save it.
            """

            self.change_window(name_title="EXCEL")
            wb.SaveAs(self.DOCUMENTS + "out_" + self.gen_excel_filename(well), FileFormat=52, CreateBackup=False)

            """
            self.change_window(name_title="EXCEL")
            time.sleep(1)
            pyautogui.press('enter')
            """

            # wb.Close(SaveChanges=True)
        except Exception as e:

            print("failed to save the excel file")
            print(str(e))
        finally:
            wb.Close(SaveChanges=True)
            excel.Quit()


class PumpTestAutomation(FileProcessing):
    def __init__(self):
        super().__init__()
        self.injection = InjectValueToSheet()

    @staticmethod
    def countdown(n):
        print('Please Move Command Window to Side !')

        while n > 0:
            print(n)
            time.sleep(1)
            n -= 1
        print("Time's up!")

    @staticmethod
    def extract_number(s):
        numbers = re.findall(r'\d+', s)
        if numbers:  # Check if numbers were found
            return int(numbers[-1])  # Return the last number found
        else:
            return None  # Return None if no numbers were found

    @staticmethod
    def get_well_number(file_name, mode="NUM"):
        """
        :param file_name: A22_ge_OriginalSaveFile.xlsm
        :param mode: NUM
        :return: 22

        :param mode: FULL
        :return: A22

        """
        well_designation = file_name.split("_")[0]
        if mode == "FULL":
            return well_designation
        elif mode == "NUM":
            return int(well_designation[1:])
        else:
            raise ValueError("Invalid mode. Use 'FULL' or 'NUM'.")

    def initial_clear(self):
        # directory is to set self.SOURCE = "C:\User\minhwasoo\Documents\"
        file_processing = FileProcessing(self.DOCUMENTS)

        xlsmfiles = file_processing.get_xlsm_files()
        aqtfiles = file_processing.get_aqt_files()
        datfiles = file_processing.get_dat_files()

        file_processing.delete_files(self.DOCUMENTS, xlsmfiles)
        file_processing.delete_files(self.DOCUMENTS, aqtfiles)
        file_processing.delete_files(self.DOCUMENTS, datfiles)

    def main_processing(self, Mode=1):
        """
        mode_functions = {
            1: "automatic_process",
            2: "automatic_with_manual_process",
            3: "recover_manual_test_only"
            4: "run_recover_auto_test_only"
        }

        :param mode: if mode is recovertest_manual --> Only Run Recover Test
        :return:
        """

        self.countdown(5)

        xlsmfiles = self.get_xlsm_filter(self.SEND, sfilter="*_ge_OriginalSaveFile.xlsm")

        user32 = ctypes.windll.user32
        if self.IS_BLOCK:
            user32.BlockInput(True)

        for file in xlsmfiles:
            self.initial_clear()
            well = self.extract_number(file)
            self.injection.main_process(well, Mode)

            self.after_work()
            time.sleep(2)

        if self.IS_BLOCK:
            user32.BlockInput(False)


"""
    mode_functions = {
        1: "automatic_process",
        2: "automatic_with_manual_process",
        3: "recover_manual_test_only"
        4: "run_recover_auto_test_only"
    }
    
    Example of how you might call your class methods
"""

if __name__ == "__main__":
    pump_test = PumpTestAutomation()
    pump_test.main_processing(Mode=2)
