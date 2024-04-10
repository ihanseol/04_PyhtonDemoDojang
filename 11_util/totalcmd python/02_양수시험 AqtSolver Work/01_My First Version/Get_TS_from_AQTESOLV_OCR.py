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


import time
import os
import cv2
import pyautogui
from PIL import Image
import pygetwindow as gw
import pytesseract
import re
from screeninfo import get_monitors

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False

DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
IMG_SAVE_PATH = "c:\\Users\\minhwasoo\\Documents\\Downloads\\"
DELAY = 0.6
IS_BLOCK = True


def after_process(text):
    def replace_comma_to_dot(_text) -> str:
        _text = _text.replace('\n', '')
        print(f'replace comma to dot before -> {_text}')

        if ',' in _text:
            _text = _text.replace(',', '.')
        if ' ' in _text and not ('m' in _text):
            _text = _text.replace(' ', '.')

        if _text.count(".") >= 2:
            cleaned_number = _text.replace(".", "")
            formatted_number = "0." + cleaned_number[1:]
        else:
            formatted_number = _text

        if formatted_number.count(".") != 1:
            formatted_number = move_decimal(formatted_number)

        # print('after :', text)
        print(f'replace comma to dot after ->  {formatted_number}')
        return formatted_number

    def extract_real_numbers(_text) -> float:
        pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern matches floating-point numbers or integers
        real_numbers = re.findall(pattern, _text)

        real_numbers = [float(number) for number in real_numbers]
        numeric_value = float(real_numbers[0])

        return abs(numeric_value)

    def move_decimal(num_str):
        if len(num_str) == 1:
            return "0." + num_str
        return num_str[:1] + '.' + num_str[1:]

    text = replace_comma_to_dot(text)
    return extract_real_numbers(text)


# Example usage:
# text = "There are 3.14 apples and -2.5 oranges."
# numbers = extract_real_numbers(text)
# print("Real numbers in the text:", numbers)


def get_screen_width() -> int:
    screen = get_monitors()[0]
    return screen.width


def change_window(name_title) -> None:
    gwindows = gw.getWindowsWithTitle(name_title)
    if gwindows:
        window = gwindows[0]
        window.activate()
        if not window.isMaximized:
            window.maximize()
    else:
        print(f"No  {name_title} found.")


# capture in Main Screen
def capture_in_main_screen(well, step):
    screen_2560x1440 = [
        ([1062, 263, 90, 21], 'screenshot_01_T.jpg'),
        ([1062, 284, 90, 21], 'screenshot_02_S.jpg')
    ]

    screen_1920x1200 = [
        ([917, 263, 60, 22], 'screenshot_01_T.jpg'),
        ([917, 283, 88, 22], 'screenshot_02_S.jpg')
    ]

    if get_screen_width() == 2560:
        areas_filenames = screen_2560x1440
    else:
        areas_filenames = screen_1920x1200

    change_window(name_title="AQTESOLV")

    result = []
    for i, (area, filename) in enumerate(areas_filenames, 1):
        # capture_area_to_file(area, filename)
        # text = read_text_from_image(filename, use_english=True)
        #
        capture_area_to_file(area, IMG_SAVE_PATH + f"w{well}_{step}_" + filename)
        text = read_text_from_image(IMG_SAVE_PATH + f"w{well}_{step}_" + filename, use_english=True)
        result.append(text)
        print(text)

    val_T = after_process(result[0])
    val_S = after_process(result[1])

    return [val_T, val_S]


def get_tesseract_config(use_english) -> str:
    if use_english:
        return '-l eng  --psm 7'
    else:
        return '-l kor --oem 3 --psm 11'


def capture_area_to_file(area, filename):
    pyautogui.screenshot(region=area).save(filename, quality=95)


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


def read_text_from_image(image_path, use_english=False):
    """
        in here teserect image scaling result is not good
        image ocr recognition is bad result
        so use it original image

    """

    # image_path = resize_image(image_path)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # processed_image_path = f"{image_path}_processed.jpg"
    # cv2.imwrite(processed_image_path, gray)

    cv2.imwrite(image_path, gray)
    config = get_tesseract_config(use_english)
    # text = pytesseract.image_to_string(Image.open(processed_image_path), config=config)

    text = pytesseract.image_to_string(Image.open(image_path), config=config)
    return text


# ------------------------------------------------------------------------------------------------------------

def extract_number(s) -> int:
    if has_path(s):
        s = os.path.basename(s)

    numbers = re.findall(r'\d+', s)
    if numbers:  # Check if numbers were found
        return int(numbers[0])  # Return the last number found
    else:
        return False  # Return None if no numbers were found


def has_path(file_name) -> bool:
    head, tail = os.path.split(file_name)
    print(f"The filename head :'{head}'  tail : {tail}  includes a path. Performing action...")

    if head:
        return True
    else:
        return False


def open_aqt(file_name) -> int:
    if not has_path(file_name):
        file_name = DIRECTORY + file_name

    if os.path.exists(file_name):
        os.startfile(file_name)
        print(f"open aqtsolver : {file_name} ....")
    else:
        print("The file does not exist.")
        raise

    time.sleep(1)

    if get_screen_width() == 2560:
        pyautogui.click(x=1557, y=93)  # maximize sub window 2560x1440
    else:
        pyautogui.click(x=1126, y=94)  # maximize sub window 1920x1200

    well = extract_number(file_name)
    time.sleep(0.5)

    return well


#
# def maxmize_aqtsolv() -> None:
#     win = pyautogui.getWindowsWithTitle('AQTESOLV')[0]
#     if not win.isActive:
#         win.activate()
#     if not win.isMaximized:
#         win.maximize()


def AqtesolverMain(file_name) -> list:
    def determine_runningstep(_file_name) -> int:
        if "step" in _file_name:
            return 1
        elif "02_long.aqt" in _file_name:
            return 2
        elif "02_long_01.aqt" in _file_name:
            return 3
        else:
            return 4

    well = open_aqt(file_name)
    running_step = determine_runningstep(file_name)

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

    # import data
    pyautogui.click(x=42, y=33)  # file
    time.sleep(DELAY)
    pyautogui.click(x=92, y=173)  # import
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)

    # browse for filename
    pyautogui.hotkey('alt', 'r')
    time.sleep(DELAY)
    pyautogui.press('backspace')
    time.sleep(DELAY)
    pyautogui.typewrite(DOCUMENTS + dat_file)

    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)
    pyautogui.hotkey('alt', 'f')  # finish
    time.sleep(DELAY)
    pyautogui.press('enter')

    # Set Unit, UnitSetting
    time.sleep(DELAY)
    pyautogui.hotkey('alt', 'e')  # Edit
    pyautogui.press('u')  # unit
    time.sleep(DELAY)
    pyautogui.hotkey('alt', 't')  # time
    pyautogui.press('m')  # unit
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)
    # End Set Unit

    # Automatic Match
    time.sleep(DELAY)
    pyautogui.hotkey('alt', 'm')  # match
    pyautogui.press('u')  # automatic
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)
    # Automatic Match

    result = capture_in_main_screen(well, step)

    # AqtSolv Program Close
    time.sleep(1)
    pyautogui.hotkey('ctrl', 's')  # match
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')  # match
    time.sleep(1)
    # AqtSolv Program Close

    return result


def main():
    result = AqtesolverMain(r"d:\05_Send\w1_02_long.aqt")
    print(result)


if __name__ == '__main__':
    main()
