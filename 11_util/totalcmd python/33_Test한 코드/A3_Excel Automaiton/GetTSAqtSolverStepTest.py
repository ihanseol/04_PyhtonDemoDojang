import fnmatch
import time
import os
import subprocess
import pygetwindow as gw
import pyautogui
from PIL import Image
import pytesseract
import re

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DOCUMENTS = "c:\\Users\\minhwasoo\\Documents\\"
DELAY = 0.5
IS_BLOCK = True


# ABSOLVE 는 듀얼모니터 상에 메인윈도우에 위치 해야한다.
# 그래야 pyautogui 를 사용할수가 있다.

# ------------------------------------------------------------------------------------------------------------

def replace_comma_to_dot(text):
    if ',' in text:
        text = text.replace(',', '.')
    # print('after :', text)
    return text


def extract_real_numbers(text):
    # Define a regular expression pattern to match real numbers
    pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern matches floating-point numbers or integers

    # Use the findall function from the re module to extract all matches
    real_numbers = re.findall(pattern, text)

    # Convert the matched strings to actual floating-point numbers
    real_numbers = [float(number) for number in real_numbers]
    numeric_value = float(real_numbers[0])

    return numeric_value


# Example usage:
text = "There are 3.14 apples and -2.5 oranges."
numbers = extract_real_numbers(text)
print("Real numbers in the text:", numbers)


# capture in Main Screen
def capture_in_main_screen():
    im1 = pyautogui.screenshot(region=(1026, 263, 144, 24))  # T
    im1.save(DIRECTORY + 'screenshot_t.jpg', quality=95)
    image1 = Image.open(DIRECTORY + 'screenshot_t.jpg')

    im2 = pyautogui.screenshot(region=(1026, 282, 144, 24))  # S
    im2.save(DIRECTORY + 'screenshot_s.jpg', quality=95)
    image2 = Image.open(DIRECTORY + 'screenshot_s.jpg')

    text1 = pytesseract.image_to_string(image1, config="--psm 7")
    text2 = pytesseract.image_to_string(image2, config="--psm 7")

    text1 = replace_comma_to_dot(text1)
    val_T = extract_real_numbers(text1)
    # print(val_T)

    text2 = replace_comma_to_dot(text2)
    val_S = extract_real_numbers(text2)
    # print(val_S)

    return [val_T, val_S]


# ------------------------------------------------------------------------------------------------------------


def extract_number(s):
    return int(re.findall(r'\d+', s)[0])


def open_aqt(filename):
    if os.path.exists(DIRECTORY + filename):
        os.startfile(DIRECTORY + filename)
        print(f"open aqtsolver : {DIRECTORY + filename} ....")
    else:
        print("The file does not exist.")

    well = extract_number(filename)

    time.sleep(1)
    pyautogui.click(x=1557, y=93)  # maximize sub window
    time.sleep(0.5)

    return well


#
# def open_aqt(filename):
#     def open_program_on_primary_monitor():
#         subprocess.Popen(PROGRAM_PATH)
#         primary_monitor = gw.getWindowsAt(0, 0)
#         if primary_monitor:
#             primary_monitor[0].moveTo(0, 0)
#
#     def maxmize_aqtsolv():
#         win = pyautogui.getWindowsWithTitle('AQTESOLV')[0]
#         if not win.isActive:
#             win.activate()
#         if not win.isMaximized:
#             win.maximize()
#
#
#     if os.path.exists(DIRECTORY + filename):
#         open_program_on_primary_monitor()
#         pyautogui.click(100, 100)
#
#         maxmize_aqtsolv()
#         time.sleep(DELAY)
#
#         pyautogui.hotkey('ctrl', 'o')
#         pyautogui.press('backspace')
#
#         pyautogui.typewrite(DIRECTORY + filename)
#         time.sleep(DELAY)
#         pyautogui.press('enter')
#
#         print(f"open aqtsolver : {DIRECTORY + filename} ....")
#     else:
#         print("The file does not exist.")
#
#     pyautogui.click(x=2081, y=93)  # maximize sub window
#     time.sleep(0.5)


def maxmize_aqtsolv():
    win = pyautogui.getWindowsWithTitle('AQTESOLV')[0]
    if not win.isActive:
        win.activate()
    if not win.isMaximized:
        win.maximize()


# c:\Users\minhwasoo\Documents\A1_ge_janggi_01.dat
# c:\Users\minhwasoo\Documents\A1_ge_janggi_02.dat
# c:\Users\minhwasoo\Documents\A1_ge_recover_01.dat
# c:\Users\minhwasoo\Documents\A1_ge_step_01.dat

def AqtesolverMain(filename, running_step):
    def determine_yangsoo_type(filename):
        if os.path.exists(filename):
            filename = os.path.basename(filename)

    well = open_aqt(filename)
    match (running_step):
        case (1):
            dat_file = f"A{well}_ge_step_01.dat"
        case (2):
            dat_file = f"A{well}_ge_janggi_01.dat"
        case (3):
            dat_file = f"A{well}_ge_janggi_02.dat"
        case (4):
            dat_file = f"A{well}_ge_recover_01.dat"
        case _:
            print('Match case exception ...')

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

    result = capture_in_main_screen()

    # AqtSolv Program Close
    pyautogui.hotkey('ctrl', 's')  # match
    time.sleep(DELAY)
    pyautogui.hotkey('alt', 'f4')  # match
    time.sleep(DELAY)
    # AqtSolv Program Close

    return result[0], result[1]


def main():
    AqtesolverMain("d:\\05_Send\\w1_01_step.aqt")


if __name__ == '__main__':
    main()
