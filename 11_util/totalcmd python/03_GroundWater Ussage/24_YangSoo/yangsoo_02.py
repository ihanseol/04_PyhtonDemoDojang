import time
import re
import os
import sys
import fitz
import shutil
import fnmatch
import ctypes

import pyautogui
import pygetwindow as gw
from screeninfo import get_monitors

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

import subprocess
import win32gui
import win32con
import win32com.client as win32
import threading

from natsort import natsorted
from threading import Timer
from playsound import playsound

from Save.FileProcessing_V3 import FileBase
from Save.FileProcessing_V3 import PathChecker

sys.path.append(
    r"c:\Program Files\totalcmd\ini\02_python\03_GroundWater Ussage\23_QT_YangSoo All Step\YangSoo\GetTS_FromPDF.py")
# sys.path.append("c:\\Program Files\\totalcmd\ini\\02_python\02_양수시험\\04_양수시험, GetTS From PDF\\")
# sys.path.append(r"d:\05_Send\pythonProject\03_GroundWater Ussage\23_QT_YangSoo All Step\YangSoo\GetTS_FromPDF.py")


fpv3 = FileBase()
pathcheck = PathChecker()


class AQTBASE:
    def __init__(self, text_widget=None):

        self.text_widget = text_widget

        self.program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.AQTESOLV_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.IMG_SAVE_PATH = "c:\\Users\\minhwasoo\\Documents\\Downloads\\"
        self.DAT_FILE = ''

        self.DOCUMENTS = os.path.join(os.path.expanduser("~"), "Documents\\")
        self.SEND = 'D:\\05_Send\\'
        self.SEND2 = 'D:\\06_Send2\\'

        self.YANGSOO_EXCEL = "A1_ge_OriginalSaveFile.xlsm"
        self.YANGSOO_REST = "_ge_OriginalSaveFile.xlsm"
        self.TC_DIR = 'C:\\Program Files\\totalcmd\\AqtSolv\\'

        self.STEP_FILE = "_01_step.aqt"
        self.LONG_FILE = "_02_long.aqt"
        self.RECOVER_FILE = "_03_recover.aqt"

        self.ISAQTOPEN = False
        self.DEBUG_YES = True
        self.DELAY = 0.5
        self.IS_BLOCK = False

    @staticmethod
    def get_screen_width() -> int:
        hmonitor = len(get_monitors())
        print('get_monitors:', hmonitor)

        screen1 = get_monitors()[0]
        screen2 = get_monitors()[0]

        if hmonitor != 1:
            screen2 = get_monitors()[1]

        if screen1.width > screen2.width:
            screen = screen1
        else:
            screen = screen2

        print(f'screen width : {screen.width}')
        return screen.width

    @staticmethod
    def get_screen_height() -> int:
        hmonitor = len(get_monitors())
        print('get_monitors:', hmonitor)

        screen1 = get_monitors()[0]
        screen2 = get_monitors()[0]

        if hmonitor != 1:
            screen2 = get_monitors()[1]

        if screen1.width > screen2.width:
            screen = screen1
        else:
            screen = screen2

        print(f'screen height : {screen.height}')
        return screen.height

    @staticmethod
    def check_screen_dimension():
        print('get screen width ', get_screen_width())
        print('get screen height ', get_screen_height())

    @staticmethod
    def tkMessageBox(message):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo("Notice", message)

    def print_debug(self, message):
        if self.DEBUG_YES:
            if message in "*-@#$%&":
                self.printinfo(message * 180)
            else:
                self.printinfo(message)

    def printinfo(self, *args, **kwargs):
        """Print function that outputs to the text widget instead of console."""
        if self.text_widget is None:
            return
        message = ' '.join(map(str, args))
        if kwargs:
            message += ' ' + ' '.join(f'{k}={v}' for k, v in kwargs.items())
        self.text_widget.insert(tk.END, message + '\n')
        self.text_widget.see(tk.END)
        self.text_widget.update()


class AutoScript(AQTBASE):
    def __init__(self, text_widget=None):
        # Instantiate the AutoScript class
        super().__init__(text_widget)

    def click_and_wait(self, x, y) -> None:
        pyautogui.click(x=x, y=y)
        time.sleep(self.DELAY)

    def press_and_wait(self, key) -> None:
        pyautogui.press(key)
        time.sleep(self.DELAY)

    def press_and_wait_hotkey(self, key, ctrl_key='alt') -> None:
        pyautogui.hotkey(ctrl_key, key)
        time.sleep(self.DELAY)

    def type_and_wait(self, text) -> None:
        pyautogui.typewrite(text)
        time.sleep(self.DELAY)

    def browse_for_file(self):
        self.click_and_wait(42, 33)  # file
        self.click_and_wait(92, 173)  # import
        self.press_and_wait('enter')

        # browse for filename
        self.press_and_wait_hotkey('r')
        self.press_and_wait('backspace')
        load_file = os.path.join(self.DOCUMENTS, self.DAT_FILE)
        self.printinfo(f'browse_for_file: {load_file}')

        self.type_and_wait(load_file)
        self.press_and_wait('enter')
        self.press_and_wait_hotkey('f')
        self.press_and_wait('enter')

    def set_unit_and_setting(self):
        self.press_and_wait_hotkey('e')
        self.press_and_wait('u')  # unit
        self.press_and_wait_hotkey('t')
        self.press_and_wait('m')  # unit
        self.press_and_wait('enter')

    def automatic_match(self):
        self.press_and_wait_hotkey('m')
        self.press_and_wait('u')  # automatic
        self.press_and_wait('enter')
        for _ in range(3):
            self.press_and_wait('enter')

    def capture_in_main_screen(self):
        # implement this method according to your requirements
        pass

    def close_program(self):
        self.press_and_wait_hotkey('s', 'ctrl')
        self.press_and_wait_hotkey('f4')

    def run_script(self, dat_file):
        self.DAT_FILE = dat_file

        self.browse_for_file()
        self.set_unit_and_setting()
        self.automatic_match()


class AqtPDF(AutoScript):
    def __init__(self):
        AutoScript.__init__(self)
        self.pdf_path = os.path.join(self.SEND, 'aqt_data.pdf')

    def get_tsx(self):

        if pathcheck.check_path(self.pdf_path) == pathcheck.RET_FILE:
            document = fitz.open(self.pdf_path)
        else:
            ValueError(f"The {self.pdf_path} is not found ...")
            return None

        page = document.load_page(0)
        text = page.get_text("text")

        value_t = 0.0
        value_s = 0.0
        value_x = 0.0

        lines = text.split('\n')
        value_s = float(lines[-2].split('=')[1])
        value_t = float(lines[-3].split('=')[1].split(' ')[1])

        for line in lines:
            if 'Observation Wells' in line:
                index = lines.index(line)
                value_x = float(lines[index + 5])
                break

        return [value_t, value_s, value_x]


class AQTProcessor(AQTBASE):
    def __init__(self, mode_value, text_widget=None):
        super().__init__(text_widget)
        if mode_value == '':
            self._mode = 'auto'
        else:
            self._mode = mode_value

        """
            mode : auto
            mode : mannual        
        """
        self.auto_script = AutoScript()
        self.aqtpdf = AqtPDF()

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, value) -> None:
        self._mode = value

    def has_path(self, file_name) -> bool:  # if file_name include path like c:\\user\\this ...
        head, tail = os.path.split(file_name)
        self.printinfo(f"head :'{head}'  tail : {tail} ")

        if head:
            return True
        else:
            return False

    @staticmethod
    def extract_number(s):
        return int(re.findall(r'\d+', s)[0])

    def open_aqt(self, file_name) -> int:
        if self.has_path(file_name):
            if os.path.exists(file_name):
                os.startfile(file_name)
                self.printinfo(f"open aqtsolver : {file_name}")
            else:
                self.printinfo("The file does not exist.")
                raise

        if self.has_path(file_name):
            fn = os.path.basename(file_name)
            well = self.extract_number(fn)
        else:
            well = self.extract_number(file_name)

        time.sleep(1)

        match self.get_screen_width():
            case 2160:
                pyautogui.click(x=1282, y=93)  # maximize sub window 2560x1440

            case 3200:
                pyautogui.click(x=1931, y=93)  # maximize sub window 2560x1440

            case 2560:
                if self.get_screen_height() == 1440:
                    pyautogui.click(x=1557, y=93)  # maximize sub window 2560x1440
                else:
                    pyautogui.click(x=1501, y=93)  # maximize sub window 2560x1600

            case 1920:
                if self.get_screen_height() == 1200:
                    if len(get_monitors()) == 1:
                        pyautogui.click(x=1126, y=94)  # maximize sub window 1920x1200
                    else:
                        pyautogui.click(x=1127, y=95)
                        # just in case dual monitor, main FHD, sub 1920x1200 - maximize sub window 1920x1200
                else:
                    if self.get_screen_height() == 1080:
                        if len(get_monitors()) == 1:
                            pyautogui.click(x=1152, y=94)  # maximize sub window 1920x1200
                        else:
                            pyautogui.click(x=1127, y=95)
                            # just in case dual monitor, main FHD, sub 1920x1200 - maximize sub window 1920x1200

            case 3072:
                pyautogui.click(x=1860, y=96)  # maximize sub window 3072x1200

            case _:
                pyautogui.click(x=1152, y=94)

        time.sleep(0.5)
        return well

    def print_pdf(self, fname):
        fpv3.delete_file(fname)

        pyautogui.hotkey('ctrl', 'p')
        pyautogui.press('enter')
        time.sleep(self.DELAY)
        pyautogui.typewrite(fname)
        pyautogui.press('enter')
        time.sleep(3)

    @staticmethod
    def wait_for_user_input(sec=10):
        time.sleep(sec)

    @staticmethod
    def determine_runningstep(file_name) -> int:
        if os.path.exists(file_name):
            if "step" in file_name:
                return 1
            elif "02_long.aqt" in file_name:
                return 2
            elif "02_long_01.aqt" in file_name:
                return 3
            else:
                return 4
        else:
            return 1

    def AqtesolverMain(self, file_name) -> object:
        well = self.open_aqt(file_name)
        running_step = self.determine_runningstep(file_name)

        dat_file = ''
        step = 0

        match running_step:
            case (1):
                step = 1
                dat_file = f"A{well}_ge_step_01.dat"
            case (2):
                step = 2
                dat_file = f"A{well}_ge_janggi_01.dat"
            case (3):
                step = 3
                dat_file = f"A{well}_ge_janggi_02.dat"
            case (4):
                step = 4
                dat_file = f"A{well}_ge_recover_01.dat"
            case _:
                self.printinfo('Match case exception ...')
                raise FileNotFoundError("cannot determin DAT_FILE ...")

        self.printinfo(f'DAT_FILE: {dat_file}, and Step = {step}')
        self.auto_script.run_script(dat_file)

        if running_step == 4:
            if self.mode == 'mannual':
                self.printinfo('\n\nAQTProcessor running mode --> Mannual')

                match self.get_screen_width():
                    case 2560:
                        pyautogui.click(x=363, y=58)  # 2560x1440
                    case 1920:
                        pyautogui.click(x=368, y=61)  # 1920x1200, 1920x1080 : curve fitting by hand
                    case 3072:
                        pyautogui.click(x=368, y=61)  # 1920x1200, 1920x1080 : curve fitting by hand
                    case _:
                        pyautogui.click(x=368, y=61)  # 1920x1200, 1920x1080 : curve fitting by hand

                rt_timer = RunTimeTimer(10)
                rt_timer.run_dual()
            else:
                self.printinfo('\n\nAQTProcessor running mode --> Auto')

        self.print_pdf(os.path.join(self.SEND, 'aqt_data.pdf'))
        time.sleep(1)
        result = self.aqtpdf.get_tsx()
        self.auto_script.close_program()

        return result


class RunTimeTimer():
    def __init__(self, seconds=10):
        self.sec = seconds
        self.program_name = r"c:\Program Files\totalcmd\ini\02_python\tkinter_timer.py"
        self.mp3_name = r"c:\Program Files\totalcmd\mp3\beep.mp3"

    @property
    def seconds(self):
        return self.sec

    @seconds.setter
    def seconds(self, value):
        self.sec = value

    def run_background_timer(self):
        def run_command_with_timeout(icommand, timeout_sec):
            process = subprocess.Popen(icommand, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            timer = Timer(timeout_sec, process.kill)

            try:
                timer.start()
                stdout, stderr = process.communicate()
            finally:
                timer.cancel()

            return stdout, stderr

        # Example usage:
        command = ['python.exe', self.program_name]
        timeout_seconds = self.seconds

        run_command_with_timeout(command, timeout_seconds)

    @staticmethod
    def set_window_always_on_top(window_title):
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
        else:
            print(f"Window with title '{window_title}' not found.")

    def timer_callback(self):
        print("Timer completed!")
        for i in range(1):
            playsound(self.mp3_name)

    def run_timer(self):
        sec = abs(self.seconds - 4)
        timer = threading.Timer(sec, self.timer_callback)
        timer.start()

    def run_dual(self):
        self.run_timer()
        self.run_background_timer()


class FileProcessing(AQTBASE):
    def __init__(self, directory="d:\\05_Send\\", text_widget=None):
        super().__init__(text_widget)
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

    def has_path(self, file_name) -> bool:
        """
        file_name has path or not
        if file_name include path like c:\\user\\this ...

        :param file_name: filename
        :return:
            head --> file path
            tail --> file
        """
        head, tail = os.path.split(file_name)
        self.printinfo(f"head :'{head}'  tail : {tail}  includes a path. Performing action...")

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

    def move_file(self, source, destination) -> None:
        """
        move file source to destination

        :param source:
        :param destination:

        """
        try:
            shutil.move(source, destination)
            self.printinfo(f"File moved successfully from '{source}' to '{destination}'")
        except Exception as e:
            self.printinfo(f"Error moving file: {e}")

    def delete_files(self, folder_path, files) -> None:
        try:
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.exists(file_path):
                    os.remove(file_path)
                    self.printinfo(f"{file_name} has been removed successfully from {folder_path}.")
                else:
                    self.printinfo(f"The file {file_name} does not exist in the folder {folder_path}.")
        except Exception as e:
            self.printinfo(f"An error occurred while deleting files: {e}")

    def duplicate_aqtfile_long(self, well):
        shutil.copyfile(self.SEND + f"w{well}_02_long.aqt", self.SEND + f"w{well}_02_long_01.aqt")

    def after_work(self, well_no):
        self.set_directory(self.DOCUMENTS)
        xlsmfiles = self.get_xlsm_files()
        datfiles = self.get_dat_files()

        for file in xlsmfiles:
            self.move_file(self.DOCUMENTS + file, self.SEND2 + file)

        for file in datfiles:
            self.move_file(self.DOCUMENTS + file, self.SEND2 + file)

        # -----------------------------------------
        # move aqt to Send2
        # -----------------------------------------

        self.set_directory(self.SEND)
        aqtfiles = self.get_aqt_files()
        aqt_files = natsorted(fnmatch.filter(aqtfiles, f"w{well_no}_*.aqt"))

        for file in aqt_files:
            self.move_file(self.SEND + file, self.SEND2 + file)


class InjectValueToSheet(FileProcessing):
    def __init__(self, directory="d:\\05_Send\\", text_widget=None):
        super().__init__(directory, text_widget=text_widget)

    def click_excel_button(self, ws, button_name):
        def find_button():
            for obj in ws.OLEObjects():
                if obj.Name == button_name:
                    return obj
            return None

        button_obj = find_button()
        if button_obj:
            try:
                button_obj.Object.Value = True
                # self.printinfo(f"Clicked button '{button_name}' successfully in worksheet {ws}.")
            except Exception as e:
                self.printinfo(f"Error clicking button '{button_name}' in worksheet {ws}: {e}")
        else:
            self.printinfo(f"Button '{button_name}' not found in worksheet {ws}.")

    def change_window(self, name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)

        if gwindows:
            window = gwindows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            self.printinfo(f"No  {name_title} found.")

    def injecttion_step(self, well, ws_step):
        self.printinfo('=' * 100)
        self.printinfo(f'=  W{well} - StepTest Starting ....           ')
        self.printinfo('=' * 100)

        ws_step.Activate()
        os.chdir(self.SEND)

        self.click_excel_button(ws_step, button_name="CommandButton1")
        if self.DEBUG_YES:
            self.printinfo('Step.Select,  StepPrn_Button1')
        time.sleep(1)

        get_ts = AQTProcessor('auto', text_widget)
        val_t, val_s, val_x = get_ts.AqtesolverMain(file_name=self.SEND + f"w{well}_01_step.aqt")

        self.printinfo(f'T: {val_t}, S: {val_s} X: {val_x} - Type:{type(val_t)}')
        self.printinfo()

    def injecttion_long_test_01(self, well, ws_janggi, ws_skin):
        self.printinfo('=' * 100)
        self.printinfo(f'* W{well} - LongTermTest Phase 1 Starting ....')
        self.printinfo('=' * 100)

        # 장기 1단계 양수시험, T,S 구하기
        ws_janggi.Activate()
        time.sleep(1)

        # toggle radius click
        self.click_excel_button(ws_janggi, button_name="CommandButton4")
        if self.DEBUG_YES:
            self.printinfo('Janggi.Select,  ToggleRadius_Button4')
        time.sleep(1)

        self.click_excel_button(ws_janggi, button_name="CommandButton1")
        if self.DEBUG_YES:
            self.printinfo('Janggi.Select,  JangGi*01_Button1')
        time.sleep(2)

        get_ts = AQTProcessor('auto', self.text_widget)
        val_t, val_s, val_x = get_ts.AqtesolverMain(file_name=self.SEND + f"w{well}_02_long.aqt")
        self.printinfo(f'T: {val_t}, S: {val_s} X: {val_x} - Type:{type(val_t)}')
        self.printinfo("")

        ws_skin.Activate()
        ws_skin.Range("D5").Value = val_t
        ws_skin.Range("E10").Value = val_s
        time.sleep(1)

    def injecttion_long_test_02(self, well, ws_janggi, ws_skin):
        self.printinfo('=' * 100)
        self.printinfo(f'* W{well} - LongTermTest Phase 2 Starting')
        self.printinfo('=' * 100)

        # 장기 2단계 양수시험, T,S 구하기
        ws_janggi.Activate()
        self.click_excel_button(ws_janggi, button_name="CommandButton2")
        if self.DEBUG_YES:
            self.printinfo('Janggi.Select,  JangGi*02_Button2')
        time.sleep(1)

        get_ts = AQTProcessor('auto', self.text_widget)
        val_t, val_s, val_x = get_ts.AqtesolverMain(file_name=self.SEND + f"w{well}_02_long_01.aqt")
        self.printinfo(f'T: {val_t}, S: {val_s} X: {val_x} - Type:{type(val_t)}')
        self.printinfo("")

        ws_skin.Activate()
        ws_skin.Range("I16").Value = val_s
        time.sleep(0.5)

    def injection_recover(self, well, ws_recover, ws_skin, mode='auto'):
        self.printinfo('=' * 100)
        self.printinfo(f'* W{well} - RecoverTest Starting')
        self.printinfo('=' * 100)

        # 회복 양수시험, T,S 구하기
        ws_recover.Activate()
        self.click_excel_button(ws_recover, button_name="CommandButton1")
        if self.DEBUG_YES:
            self.printinfo('Recover.Select,  Recover Prn_Button1')
        time.sleep(1)

        if not self.is_exist(self.SEND + f"w{well}_03_recover.aqt"):
            return False

        if mode == 'mannual':
            get_ts = AQTProcessor('mannual', self.text_widget)
            val_t, val_s, val_x = get_ts.AqtesolverMain(file_name=self.SEND + f"w{well}_03_recover.aqt")
        else:
            get_ts = AQTProcessor('auto', self.text_widget)
            val_t, val_s, val_x = get_ts.AqtesolverMain(file_name=self.SEND + f"w{well}_03_recover.aqt")

        self.printinfo(f'T: {val_t}, S: {val_s} X: {val_x} - Type:{type(val_t)}')
        self.printinfo("")

        ws_skin.Activate()
        ws_skin.Range("H13").Value = val_t

        ws_skin.Range("I13").Value = val_s
        time.sleep(0.5)

    def is_step_file_exist(self, well) -> bool:
        path = self.SEND

        self.set_directory(path)
        path_in_aqt_stepfiles = self.get_aqt_files()
        self.printinfo(path_in_aqt_stepfiles)

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

    def main_process(self, well, mode=1) -> None:
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

        if (mode != 3) and (mode != 4):
            self.duplicate_aqtfile_long(well)

        ws_skin = wb.Worksheets("SkinFactor")
        ws_step = wb.Worksheets("Step.Select")
        ws_janggi = wb.Worksheets("Janggi.Select")
        ws_recover = wb.Worksheets("Recover.Select")

        if ((mode != 3) and (mode != 4)) and self.is_step_file_exist(well):
            self.injecttion_step(well, ws_step)

        if ((mode != 3) and (mode != 4)) and mode:
            self.injecttion_long_test_01(well, ws_janggi, ws_skin)
            self.injecttion_long_test_02(well, ws_janggi, ws_skin)

        if (mode == 2 or mode == 3) and mode != 4:
            self.injection_recover(well, ws_recover, ws_skin, mode='mannual')
            # click_excel_button(ws_recover, "CommandButton2")
        else:
            self.injection_recover(well, ws_recover, ws_skin, mode='auto')

        excel.ScreenUpdating = True

        try:
            """
            helpful if saving multiple times to save file, it means you won't get a pop up for overwrite 
            and will default to save it.
            """

            self.change_window(name_title="EXCEL")

            excel.DisplayAlerts = False
            wb.SaveAs(self.DOCUMENTS + "out_" + self.gen_excel_filename(well), FileFormat=52, CreateBackup=False)

            """
            self.change_window(name_title="EXCEL")
            time.sleep(1)
            pyautogui.press('enter')
            """

            # wb.Close(SaveChanges=True)
        except Exception as e:

            self.printinfo("failed to save the excel file")
            self.printinfo(str(e))
        finally:
            wb.Close(SaveChanges=True)
            excel.Quit()


class PumpTestAutomation(FileProcessing):
    def __init__(self, directory="d:\\05_Send\\", text_widget=None):
        super().__init__(directory, text_widget)
        self.injection = InjectValueToSheet(directory, self.text_widget)

    def countdown(self, n):
        self.printinfo('Please Move Command Window to Side !')

        while n > 0:
            self.printinfo(n)
            time.sleep(1)
            n -= 1
        self.printinfo("Time's up!")

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
        file_processing = FileProcessing(self.DOCUMENTS, self.text_widget)

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

        # :param mode: if mode is recovertest_manual --> Only Run Recover Test
        # :return:
        """

        self.countdown(3)

        xlsmfiles = self.get_xlsm_filter(self.SEND, sfilter="*_ge_OriginalSaveFile.xlsm")

        user32 = ctypes.windll.user32
        if self.IS_BLOCK:
            user32.BlockInput(True)

        pyautogui.hotkey('win', 'shift', 'right')

        for file in xlsmfiles:
            self.initial_clear()
            well = self.extract_number(file)
            self.injection.main_process(well, Mode)

            self.after_work(well)
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


def main():
    root = tk.Tk()
    root.title("Pump Test Automation")
    root.geometry("900x1100")  # Initial size, but will expand

    # Create a scrolled text widget that fills the entire window
    text_widget = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=100, height=40, font=('Consolas', 11))
    text_widget.pack(fill=tk.BOTH, expand=True)

    # Initialize pump_test with text widget
    pump_test = PumpTestAutomation("d:\\05_Send\\", text_widget)

    # Run the process
    pump_test.main_processing(Mode=2)

    # Keep the window open
    root.mainloop()


if __name__ == "__main__":
    #     aqt_processor = AQTProcessor('mannual')
    #     self.printinfo(aqt_processor.AqtesolverMain(r"d:\05_Send\w1_03_recover.aqt"))
    main()
