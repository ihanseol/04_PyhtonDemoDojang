import os
import time
import fnmatch
import pyautogui
import ctypes
import pyperclip
from pick import pick

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = True


#
# A1_ge_janggi_01.dat
# A1_ge_janggi_02.dat
# A1_ge_recover_01.dat
# A1_ge_step_01.dat

# 1. get all aqtfiles
# 2. well number, step , long, copy (복사본), recover 로 분류
# 3. 일단 최대화 하고, 데이타를 로드, 단위를 맞추고, 커브피팅, 값을 획득, 저장
# 이런 순서로 하면 될듯


def change_filename():
    global DIRECTORY
    for filename in os.listdir(DIRECTORY):
        name, ext = os.path.splitext(filename)
        if ext == ".aqt" and "_01" not in name:  # Added condition to avoid renaming files that already have the "_01" suffix
            if "- 복사본" in name:  # Moved this condition to the top of the if statement for readability
                new_name = name.replace(" - 복사본", "_01") + ext
                os.rename(os.path.join(DIRECTORY, filename), os.path.join(DIRECTORY, new_name))

            if "- Copy" in name:  # Moved this condition to the top of the if statement for readability
                new_name = name.replace(" - Copy", "_01") + ext
                os.rename(os.path.join(DIRECTORY, filename), os.path.join(DIRECTORY, new_name))


def open_aqt():
    global ISAQTOPEN
    global PROGRAM_PATH

    if not ISAQTOPEN:
        os.startfile(PROGRAM_PATH)
        ISAQTOPEN = True

    time.sleep(DELAY)


def import_dat_and_rest(file_name):
    open_aqt()

    # aqtesolve window make front maximize

    win = pyautogui.getWindowsWithTitle('AQTESOLV')[0]
    if not win.isActive:  win.activate()
    if not win.isMaximized:  win.maximize()
    pyautogui.click(x=36, y=32)
    time.sleep(DELAY)
    pyautogui.click(x=116, y=171)
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)




def get_well_number(file_name, mode="NUM"):
    """
    Extracts the well number from a given file name.

    Parameters:
        file_name (str): The file name containing the well information.
        mode (str, optional): Determines the format of the output.
            "FULL": Returns the full well designation (e.g., 'w1').
            "NUM": Returns only the numerical part of the well designation (e.g., 1).

    Returns:
        str or int: The extracted well number based on the specified mode.
    """
    well_designation = file_name.split("_")[0]

    if mode == "FULL":
        return well_designation
    elif mode == "NUM":
        return int(well_designation[1:])
    else:
        raise ValueError("Invalid mode. Use 'FULL' or 'NUM'.")


def main_get_aqtfiles():
    files = os.listdir(DIRECTORY)
    aqtfiles = [f for f in files if f.endswith('.aqt')]

    if aqtfiles:
        for i in range(1, 33):  # maximum well number is 18
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            if wfiles:
                for j, file in enumerate(wfiles):
                    print(f'{get_well_number(file, "FULL")}-{j + 1}  - {file}')
                    import_dat_and_rest(file)


def main():
    main_get_aqtfiles()


#
# def main_temp():
#     user32 = ctypes.windll.user32
#     if IS_BLOCK:
#         user32.BlockInput(True)
#
#     if IS_BLOCK:
#         user32.BlockInput(False)


if __name__ == "__main__":
    main()
