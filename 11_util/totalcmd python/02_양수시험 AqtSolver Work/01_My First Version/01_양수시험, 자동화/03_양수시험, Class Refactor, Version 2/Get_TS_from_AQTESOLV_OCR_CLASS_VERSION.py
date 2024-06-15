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
import time
import cv2
import pyautogui
import pytesseract
import re
from PIL import Image
import pygetwindow as gw
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


def tkMessageBox(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Notice", message)


def get_screen_width() -> int:
    hmonitor = len(get_monitors())
    print('get_monitors:', hmonitor)

    screen1 = get_monitors()[0]
    if hmonitor != 1:
        screen2 = get_monitors()[1]

    if hmonitor == 1:
        screen = screen1
    else:
        if screen1.width > screen2.width:
            screen = screen1
        else:
            screen = screen2

    print(f'screen width : {screen.width}')
    return screen.width


def get_screen_height() -> int:
    hmonitor = len(get_monitors())
    print('get_monitors:', hmonitor)

    screen1 = get_monitors()[0]
    if hmonitor != 1:
        screen2 = get_monitors()[1]

    if hmonitor == 1:
        screen = screen1
    else:
        if screen1.width > screen2.width:
            screen = screen1
        else:
            screen = screen2

    print(f'screen width : {screen.width}')
    return screen.height


class AQTbase:
    def __init__(self):
        self.program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
        self.IMG_SAVE_PATH = "c:\\Users\\minhwasoo\\Documents\\Downloads\\"
        self.directory = "d:\\05_Send\\"
        self.documents = "c:\\Users\\minhwasoo\\Documents\\"
        self.delay = 0.5
        self.is_block = True
        self.dat_file = ''


class CaptureScreen(AQTbase):
    def __init__(self):
        # Instantiate the AutoScript class
        super().__init__()

    @staticmethod
    def get_tesseract_config(use_method="NUM") -> str:
        match use_method:
            case ("NUM"):
                return 'digits'

            case ("ENG"):
                return '-l eng --oem 3 --psm 7'

            case ("KOR"):
                return '-l kor --oem 3 --psm 11'

            case _:
                return 'digits'

    @staticmethod
    def capture_area_to_file(area, filename):
        pyautogui.screenshot(region=area).save(filename, quality=95)
        pyautogui.screenshot('my_screenshot.png')

    @staticmethod
    def resize_image(image_path) -> str:
        img = Image.open(image_path)
        [w, h] = img.size
        # resized_size = tuple([int(dim * 2) for dim in original_size])

        resized_size = (w * 2, h * 2)
        print(f"module resize_image : {image_path} --> {resized_size}")

        img = img.resize(resized_size, Image.Resampling.LANCZOS)
        resized_image_path = f"{image_path}_resized.jpg"
        img.save(resized_image_path)
        return resized_image_path

    def read_text_from_image(self, image_path, use_method="NUM"):
        """
            in here teserect image scaling result is not good
            image ocr recognition is bad result
            so use it original image

            use_method :
             NUM - number only
             ENG - eng
             KOR - korean

        """
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        cv2.imwrite(image_path, gray)
        print(f"read_text_from_image --> {image_path}")

        config = self.get_tesseract_config(use_method)
        text = pytesseract.image_to_string(Image.open(image_path), config=config)

        return text

    def replace_comma_to_dot(self, _text) -> str:
        _text = _text.replace('\n', '')
        print(f'replace comma to dot before -> {_text}')

        if _text[-1:] == '.':
            _text = _text[:-1]

        if ' ' in _text and _text.count(' ') != 1:
            _text = _text.replace(' ', '.')

        if _text.count(".") >= 2:
            cleaned_number = _text.replace(".", "")
            formatted_number = "0." + cleaned_number[1:]
        else:
            formatted_number = _text

        if formatted_number.count(".") != 1:
            formatted_number = self.move_decimal(formatted_number)

        if len(formatted_number) >= 3 and formatted_number.count(".") == 0:
            formatted_number = self.move_decimal(formatted_number)

        # print('after :', text)
        print(f'replace comma to dot after ->  {formatted_number}')
        return formatted_number

    @staticmethod
    def move_decimal(num_str):
        if len(num_str) == 1:
            return "0." + num_str
        return num_str[:1] + '.' + num_str[1:]

    @staticmethod
    def extract_real_numbers(_text) -> float:
        pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern matches floating-point numbers or integers
        real_numbers = re.findall(pattern, _text)

        real_numbers = [float(number) for number in real_numbers]
        numeric_value = float(real_numbers[0])

        return numeric_value

    def after_process(self, text) -> float:
        text = self.replace_comma_to_dot(text)
        num = abs(self.extract_real_numbers(text))
        return num

    @staticmethod
    def change_window(name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)
        if gwindows:
            window = gwindows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            print(f"No {name_title} found.")

    def capture_in_main_screen(self, well, step) -> object:

        # area or region - [left, top, width, and height]
        screen_2560x1440 = [
            ([1062, 263, 46, 21], 'screenshot_01_T.jpg'),
            ([1062, 284, 90, 21], 'screenshot_02_S.jpg')
        ]

        screen_1920x1200 = [
            ([919, 263, 46, 22], 'screenshot_01_T.jpg'),
            ([917, 283, 88, 22], 'screenshot_02_S.jpg')
        ]

        screen_1920x1080 = [
            ([844, 265, 46, 22], 'screenshot_01_T.jpg'),
            ([844, 283, 88, 22], 'screenshot_02_S.jpg')
        ]

        screen_1920x1080_4 = [
            ([848, 265, 46, 22], '1920x1080_4_01_T.jpg'),
            ([848, 283, 88, 22], '1920x1080_4_02_S.jpg')
        ]

        screen_3072x1728 = [
            ([1238, 263, 46, 22], 'screenshot_01_T.jpg'),
            ([1238, 283, 88, 22], 'screenshot_02_S.jpg')
        ]


        match get_screen_width():
            case 2560:
                areas_filenames = screen_2560x1440
            case 1920:
                if get_screen_height() == 1200:
                    areas_filenames = screen_1920x1200
                else:
                    if step == 4:
                        areas_filenames = screen_1920x1080_4
                    else:
                        areas_filenames = screen_1920x1080

            case 3072:
                areas_filenames = screen_3072x1728
                print(' selected ...')
            case _:
                areas_filenames = screen_1920x1200
                print(' else ...')

        self.change_window(name_title="AQTESOLV")

        result = []
        for i, (area, filename) in enumerate(areas_filenames, 1):
            self.capture_area_to_file(area, self.IMG_SAVE_PATH + f"w{well}_{step}_" + filename)
            text = self.read_text_from_image(self.IMG_SAVE_PATH + f"w{well}_{step}_" + filename, use_method="NUM")
            result.append(text)
            print(text)

        val_T = self.after_process(result[0])
        val_S = self.after_process(result[1])
        return [val_T, val_S]


class AutoScript(AQTbase):
    def __init__(self):
        # Instantiate the AutoScript class
        super().__init__()

    def click_and_wait(self, x, y) -> None:
        pyautogui.click(x=x, y=y)
        time.sleep(self.delay)

    def press_and_wait(self, key) -> None:
        pyautogui.press(key)
        time.sleep(self.delay)

    def press_and_wait_hotkey(self, key, ctrl_key='alt') -> None:
        pyautogui.hotkey(ctrl_key, key)
        time.sleep(self.delay)

    def type_and_wait(self, text) -> None:
        pyautogui.typewrite(text)
        time.sleep(self.delay)

    def browse_for_file(self):
        self.click_and_wait(42, 33)  # file
        self.click_and_wait(92, 173)  # import
        self.press_and_wait('enter')

        # browse for filename
        self.press_and_wait_hotkey('r')
        self.press_and_wait('backspace')
        self.type_and_wait(self.documents + self.dat_file)
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
        self.dat_file = dat_file

        self.browse_for_file()
        self.set_unit_and_setting()
        self.automatic_match()


class AQTProcessor(AQTbase):
    def __init__(self, mode_value):
        # Instantiate the AutoScript class
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
        self.auto_capture = CaptureScreen()

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
                if get_screen_width() == 1200:
                    pyautogui.click(x=1126, y=94)  # maximize sub window 1920x1200
                else:
                    pyautogui.click(x=1152, y=94)  # maximize sub window 1920x1080

            case 3072:
                pyautogui.click(x=1860, y=96)  # maximize sub window 3072x1200
            case _:
                pyautogui.click(x=1152, y=94)

        time.sleep(0.5)
        return well

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
                print('Match case exception ...')
                raise FileNotFoundError("cannot determin dat_file ...")

        self.auto_script.run_script(dat_file)

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

        result = self.auto_capture.capture_in_main_screen(well, step)
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
