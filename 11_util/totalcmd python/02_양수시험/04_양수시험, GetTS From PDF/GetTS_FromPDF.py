# and this program must run in a 2560x1440 dual-monitor environment
# Also, the AQTSOLVE.exe must be located on the main monitor
# Can screen capture
#
# ABSOLVE shall be located in the main window on the dual monitor.
# That's how you can use pyautogui.
#
#
# file location ...
#
# c:\Users\minhwasoo\Documents\A1_ge_janggi_01.dat
# c:\Users\minhwasoo\Documents\A1_ge_janggi_02.dat
# c:\Users\minhwasoo\Documents\A1_ge_recover_01.dat
# c:\Users\minhwasoo\Documents\A1_ge_step_01.dat
#
#  and screen support 2560x1440 and 1920x1200 and 1920x1080
# 2024/04/09
#
# Class Version 
#

import os
import fitz
import pyautogui
import re
from screeninfo import get_monitors
import tkinter as tk
from tkinter import messagebox
import subprocess
import win32gui
import win32con
import threading
from threading import Timer
import time
from playsound import playsound
import FileProcessing_V3

fpv3 = FileProcessing_V3.FileBase()
pathcheck = FileProcessing_V3.PathChecker()


def tkMessageBox(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Notice", message)


def get_screen_width() -> int:
    hmonitor = len(get_monitors())
    print('get_monitors:', hmonitor)

    screen1 = get_monitors()[0]
    # if hmonitor != 1:
    #     screen2 = get_monitors()[1]
    #
    # if hmonitor == 1:
    #     screen = screen1
    # else:
    #     if screen1.width > screen2.width:
    #         screen = screen1
    #     else:
    #         screen = screen2

    screen = screen1
    print(f'screen width : {screen.width}')
    return screen.width


def get_screen_height() -> int:
    hmonitor = len(get_monitors())
    print('get_monitors:', hmonitor)

    screen1 = get_monitors()[0]
    # if hmonitor != 1:
    #     screen2 = get_monitors()[1]
    #
    # if hmonitor == 1:
    #     screen = screen1
    # else:
    #     if screen1.width > screen2.width:
    #         screen = screen1
    #     else:
    #         screen = screen2

    screen = screen1
    print(f'screen height : {screen.height}')
    return screen.height


def check_screen_dimension():
    print('get screen width ', get_screen_width())
    print('get screen height ', get_screen_height())


class AQTBASE:
    def __init__(self):

        self.program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.AQTESOLV_PATH = 'C:\\WHPA\\AQTEver3.4(170414)\\AQTW32.EXE'
        self.IMG_SAVE_PATH = "c:\\Users\\minhwasoo\\Documents\\Downloads\\"
        self.DAT_FILE = ''

        self.DOCUMENTS = os.path.expanduser("~\\Documents")
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
        """
        self.IS_BLOCK = False :
         because while running the program causes block or wait for user input
         then can't do anything
         so it must be False, user input allowed ...
        """

    def print_debug(self, message):
        if self.DEBUG_YES:
            if message in "*-@#$%&":
                print(message * 180)
            else:
                print(message)


class AutoScript(AQTBASE):
    def __init__(self):
        # Instantiate the AutoScript class
        super().__init__()

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
        print(f'browse_for_file: {load_file}')

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

    def run_script(self, DAT_FILE):
        self.DAT_FILE = DAT_FILE

        self.browse_for_file()
        self.set_unit_and_setting()
        self.automatic_match()


class AqtPDF(AutoScript):
    def __init__(self):
        AutoScript.__init__(self)
        self.pdf_path = os.path.join(self.SEND, 'aqt_data.pdf')

    def getTSX(self):

        if pathcheck.check_path(self.pdf_path) == pathcheck.RET_FILE:
            document = fitz.open(self.pdf_path)
        else:
            ValueError(f"The {self.pdf_path} is not found ...")
            return None

        page = document.load_page(0)
        text = page.get_text("text")

        T_value = None
        S_value = None
        X_value = None

        lines = text.split('\n')
        S_value = float(lines[-2].split('=')[1])
        T_value = float(lines[-3].split('=')[1].split(' ')[1])

        for line in lines:
            if 'Observation Wells' in line:
                index = lines.index(line)
                X_value = float(lines[index + 5])
                break

        return [T_value, S_value, X_value]


class AQTProcessor(AQTBASE):
    def __init__(self, mode_value):
        super().__init__()
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

    @staticmethod
    def has_path(file_name) -> bool:  # if file_name include path like c:\\user\\this ...
        head, tail = os.path.split(file_name)
        print(f"head :'{head}'  tail : {tail} ")

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
                print(f"open aqtsolver : {file_name}")
            else:
                print("The file does not exist.")
                raise

        if self.has_path(file_name):
            fn = os.path.basename(file_name)
            well = self.extract_number(fn)
        else:
            well = self.extract_number(file_name)

        time.sleep(1)

        match get_screen_width():
            case 2560:
                pyautogui.click(x=1557, y=93)  # maximize sub window 2560x1440
            case 1920:
                if get_screen_height() == 1200:
                    if len(get_monitors()) == 1:
                        pyautogui.click(x=1126, y=94)  # maximize sub window 1920x1200
                    else:
                        pyautogui.click(x=1127, y=95)  # just in case dual monitor, main FHD, sub 1920x1200 - maximize sub window 1920x1200
                else:
                    pyautogui.click(x=1127, y=95)  # maximize sub window 1920x1080

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

        match running_step:
            case (1):
                step = 1
                DAT_FILE = f"A{well}_ge_step_01.dat"
            case (2):
                step = 2
                DAT_FILE = f"A{well}_ge_janggi_01.dat"
            case (3):
                step = 3
                DAT_FILE = f"A{well}_ge_janggi_02.dat"
            case (4):
                step = 4
                DAT_FILE = f"A{well}_ge_recover_01.dat"
            case _:
                print('Match case exception ...')
                raise FileNotFoundError("cannot determin DAT_FILE ...")

        print(f'DAT_FILE: {DAT_FILE}')
        self.auto_script.run_script(DAT_FILE)

        if running_step == 4:
            if self.mode == 'mannual':
                print('\n\nAQTProcessor running mode --> Mannual')

                match get_screen_width():
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
                print('\n\nAQTProcessor running mode --> Auto')

        self.print_pdf(os.path.join(self.SEND, 'aqt_data.pdf'))
        time.sleep(1)
        result = self.aqtpdf.getTSX()
        self.auto_script.close_program()

        return result


class RunTimeTimer:
    def __init__(self, seconds=10):
        self.sec = seconds
        self.program_name = (r"c:\Program Files\totalcmd\ini\02_python\tkinter_timer.py")
        self.mp3_name = r"c:\Program Files\totalcmd\mp3\race-start-beeps-125125.mp3"

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


# To run the program
if __name__ == '__main__':
    aqt_processor = AQTProcessor('mannual')
    print(aqt_processor.AqtesolverMain(r"d:\05_Send\w1_03_recover.aqt"))
