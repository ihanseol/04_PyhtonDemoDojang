import os
import time
import fnmatch
import argparse
import pyautogui
import win32gui
import ctypes

# if install error occured
# If the issue persists, you can try installing the pywin32 module instead of win32gui,
# which includes win32gui as well as other Windows-specific modules.
# You can install it using the following command:
# pip install pywin32

PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.6
IS_BLOCK = True


def setview_mode(mode):
    pyautogui.hotkey('alt', 'v')
    time.sleep(0.1)

    if mode == 'report':
        pyautogui.press('r')
    else:
        pyautogui.press('d')


def delete_pdf(dir_path):
    for filename in os.listdir(dir_path):
        if filename.endswith(".pdf"):
            os.remove(os.path.join(dir_path, filename))
            print("Deleted existing PDF file: {}".format(filename))


def delete_existing_pdffile():
    global DIRECTORY

    print('----------------------------------------------------------------')
    dir_path = os.path.expanduser("~\\Documents\\")
    delete_pdf(dir_path)
    delete_pdf(DIRECTORY)


def exit_program():
    global DELAY

    pyautogui.hotkey('alt', 'f4')
    time.sleep(DELAY)
    pyautogui.press('n')


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


def remove_extension(file_name):
    return os.path.splitext(file_name)[0]


def printpdf(fname):
    global DELAY

    pyautogui.hotkey('ctrl', 'p')
    pyautogui.press('enter')
    time.sleep(DELAY)
    pyautogui.typewrite(fname)
    pyautogui.press('enter')
    time.sleep(DELAY)


def open_file(filename):
    global DELAY
    
    pyautogui.hotkey('ctrl', 'o')
    pyautogui.press('backspace')  # 231103 this code , clear filename area text in aqtsolv file open area ...
    pyautogui.typewrite(DIRECTORY+filename)
    time.sleep(DELAY)
    pyautogui.press('enter')
    time.sleep(DELAY)


def printing_job(well, i, filename, mode):
    open_aqt()
    open_file(filename)
    time.sleep(DELAY)
    printpdf(f'a{well}-{i}')

    if mode == 'dual':
        setview_mode('report')
        time.sleep(DELAY)
        printpdf(f'p{well}-{i}')


def open_aqt():
    global ISAQTOPEN
    global PROGRAM_PATH

    if not ISAQTOPEN:
        os.startfile(PROGRAM_PATH)
        ISAQTOPEN = True

    time.sleep(DELAY)


def get_wellnum(mode, f):
    # 1 -- return 'w1'
    # else -- return 1
    well = f.split("_")[0]

    if mode == 1:
        return well
    else:
        return int(well[1:])


def get_window_title():
    hwnd = win32gui.GetForegroundWindow()
    window_text = win32gui.GetWindowText(hwnd)

    if 'aqtesolv' in window_text.lower():
        return True
    else:
        return False


def close_aqtesolvapp(n, mode):
    check = get_window_title()

    # if n is None:
    #     return 'Empty Files ....'

    print('Enter Shutdown Process ...')

    if check:
        pyautogui.hotkey('alt', 'f4')

    if mode == 'single':
        return 'exit single ...'
    else:
        for i in range(1, n + 1):
            pyautogui.press('n')
            print(f'closing window {i} ... ')

        return 'exit dual ...'


def main_job(mode):
    global DIRECTORY
    change_filename()
    delete_existing_pdffile()

    files = os.listdir(DIRECTORY)
    aqtfiles = [f for f in files if f.endswith('.aqt')]
    n_aqtfiles = len(aqtfiles)
    well_num = aqtfiles[0][1:2]

    print('----------------------------------------------------------------')
    print(f'aqtfiles : {len(aqtfiles)}')
    print('----------------------------------------------------------------')

    # if (3 <= n_aqtfiles <= 4) and (well_num != '1'):
    if (n_aqtfiles in [3, 4]) and (well_num != '1'):
        wfiles = fnmatch.filter(aqtfiles, f"w{well_num}_*.aqt")
        for j, file in enumerate(wfiles):
            print(f'{get_wellnum(2, file)}-{j + 1}  - {file}')
            printing_job(well_num, j + 1, file, mode)
    else:
        for i in range(1, 19):  # maximum well number is 18
            wfiles = fnmatch.filter(aqtfiles, f"w{i}_*.aqt")
            for j, file in enumerate(wfiles):
                print(f'{get_wellnum(2, file)}-{j + 1}  - {file}')            
                printing_job(i, j + 1, file, mode)

    if aqtfiles:
        return n_aqtfiles
    else:
        return 0


def main():
    parser = argparse.ArgumentParser(description="Select 'single' or 'dual' mode.")
    parser.add_argument('mode', choices=['single', 'dual'])
    args = parser.parse_args()

    user32 = ctypes.windll.user32
    if IS_BLOCK:
        user32.BlockInput(True)

    n = main_job(args.mode)
    print('----------------------------------------------------------------')
    print(f'Process end .... return value from main_process is {n}')
    print('Shutdown AQTW32  Application ...')
    print('----------------------------------------------------------------')
    close_aqtesolvapp(n, args.mode)
    time.sleep(1)

    if IS_BLOCK:
        user32.BlockInput(False)


if __name__ == "__main__":
    main()
