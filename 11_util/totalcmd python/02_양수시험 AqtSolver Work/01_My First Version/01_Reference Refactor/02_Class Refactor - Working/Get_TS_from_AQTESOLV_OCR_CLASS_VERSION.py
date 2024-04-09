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


class AQTbase:
    def __init__(self):
        self.program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
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
    def get_tesseract_config(use_english) -> str:
        if use_english:
            return '-l eng  --psm 7'
        else:
            return '-l kor --oem 3 --psm 11'

    @staticmethod
    def capture_area_to_file(area, filename):
        pyautogui.screenshot(region=area).save(filename, quality=95)

    @staticmethod
    def resize_image(image_path) -> str:
        img = Image.open(image_path)
        [w, h] = img.size
        # resized_size = tuple([int(dim * 2) for dim in original_size])

        resized_size = (w * 2, h * 2)
        print(resized_size)

        img = img.resize(resized_size, Image.Resampling.LANCZOS)
        resized_image_path = f"{image_path}_resized.jpg"
        img.save(resized_image_path)
        return resized_image_path

    def read_text_from_image(self, image_path, use_english=False):
        image_path = self.resize_image(image_path)

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_image_path = f"{image_path}_processed.jpg"
        cv2.imwrite(processed_image_path, gray)

        config = self.get_tesseract_config(use_english)
        text = pytesseract.image_to_string(Image.open(processed_image_path), config=config)

        return text

    @staticmethod
    def replace_comma_to_dot(text):
        if ',' in text:
            text = text.replace(',', '.')
        if ' ' in text:
            text = text.replace(' ', '.')

        # print('after :', text)
        return text

    @staticmethod
    def extract_real_numbers(text):
        pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern matches floating-point numbers or integers
        real_numbers = re.findall(pattern, text)

        real_numbers = [float(number) for number in real_numbers]
        numeric_value = float(real_numbers[0])

        return numeric_value

    def after_process(self, text):
        text = self.replace_comma_to_dot(text)
        return self.extract_real_numbers(text)

    @staticmethod
    def get_screen_width() -> int:
        screen = get_monitors()[0]
        return screen.width

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

    def capture_in_main_screen(self) -> object:
        screen_2560x1440 = [
            ([1026, 263, 144, 24], 'screenshot_01_T.jpg'),
            ([1026, 282, 144, 24], 'screenshot_02_S.jpg')
        ]

        screen_1920x1200 = [
            ([917, 263, 49, 22], 'screenshot_01_T.jpg'),
            ([917, 283, 76, 16], 'screenshot_02_S.jpg')
        ]

        if self.get_screen_width() == 2560:
            areas_filenames = screen_2560x1440
        else:
            areas_filenames = screen_1920x1200

        self.change_window(name_title="AQTESOLV")

        result = []
        for i, (area, filename) in enumerate(areas_filenames, 1):
            self.capture_area_to_file(area, filename)
            text = self.read_text_from_image(filename, use_english=True)
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
    def __init__(self):
        # Instantiate the AutoScript class
        super().__init__()
        self.auto_script = AutoScript()
        self.auto_capture = CaptureScreen()

    @staticmethod
    def get_screen_width() -> int:
        screen = get_monitors()[0]
        return screen.width

    @staticmethod
    def has_path(file_name) -> bool:
        head, tail = os.path.split(file_name)

        if head:
            # print(f"The filename '{tail}' includes a path. Performing action...")
            return True
        else:
            # print(f"The filename '{tail}' does not include a path.")
            return False

    @staticmethod
    def extract_number(s):
        return int(re.findall(r'\d+', s)[0])

    def open_aqt(self, file_name) -> int:
        if self.has_path(file_name):
            if os.path.exists(file_name):
                os.startfile(file_name)
                print(f"open aqtsolver : {file_name} ....")
        else:
            print("The file does not exist.")
            raise

        if self.has_path(file_name):
            fn = os.path.basename(file_name)
            well = self.extract_number(fn)
        else:
            well = 1
            raise FileNotFoundError("The file does not exist.")

        time.sleep(1)
        if self.get_screen_width() == 2560:
            pyautogui.click(x=1557, y=93)  # maximize sub window 2560x1440
        else:
            pyautogui.click(x=1126, y=94)  # maximize sub window 1920x1200

        time.sleep(0.5)
        return well

    @staticmethod
    def determine_runningstep(file_name) -> int:
        if os.path.exists(file_name):
            if "step" in file_name:
                return 1
            elif "janggi_01" in file_name:
                return 2
            elif "janggi_02" in file_name:
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
                dat_file = f"A{well}_ge_step_01.dat"
            case (2):
                dat_file = f"A{well}_ge_janggi_01.dat"
            case (3):
                dat_file = f"A{well}_ge_janggi_02.dat"
            case (4):
                dat_file = f"A{well}_ge_recover_01.dat"
            case _:
                dat_file = f"A{well}_ge_step_01.dat"
                print('Match case exception ...')
                raise FileNotFoundError("cannot determin dat_file ...")

        self.auto_script.run_script(dat_file)
        result = self.auto_capture.capture_in_main_screen()
        self.auto_script.close_program()

        return result


# To run the program
if __name__ == '__main__':
    aqt_processor = AQTProcessor()
    print(aqt_processor.AqtesolverMain("d:\\05_Send\\w1_01_step.aqt"))
