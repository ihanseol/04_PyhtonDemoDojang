import os, time, glob
import fnmatch
import copy, argparse
import pyautogui
import win32gui

# if install error occured
# If the issue persists, you can try installing the pywin32 module instead of win32gui,
# which includes win32gui as well as other Windows-specific modules.
# You can install it using the following command:
# pip install pywin32

program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
isAqtOpen = False


def setview_mode(mode):
    if mode == 'report':
        pyautogui.hotkey('alt', 'v')
        time.sleep(0.1)
        pyautogui.press('r')
    else:
        pyautogui.hotkey('alt', 'v')
        time.sleep(0.1)
        pyautogui.press('d')


def delete_exisiting_pdffile():
    dir_path = os.path.expanduser("~\\Documents\\")

    for filename in os.listdir(dir_path):
        if filename.endswith(".pdf"):
            os.remove(dir_path + filename)


def printpdf(fname):
    pyautogui.hotkey('ctrl', 'p')
    pyautogui.press('enter')
    time.sleep(0.3)
    pyautogui.typewrite(fname)
    pyautogui.press('enter')
    time.sleep(0.3)


def exit_program():
    pyautogui.hotkey('alt', 'f4')
    time.sleep(0.1)
    pyautogui.press('n')


def change_filename():
    directory = "d:\\05_Send\\"
    for filename in os.listdir():
        if filename.endswith(".aqt"):
            name, ext = os.path.splitext(filename)
            if "- 복사본" in name:
                new_name = name.replace(" - 복사본", "_01") + ext
                os.rename(directory + filename, directory + new_name)


def remove_extension(file_name):
    return os.path.splitext(file_name)[0]


def printing_job(well, i, filename, mode):
    global isAqtOpen
    if not isAqtOpen:
        os.startfile(program_path)
        isAqtOpen = True

    time.sleep(0.3)
    pyautogui.hotkey('ctrl', 'o')
    pyautogui.typewrite(filename)
    pyautogui.press('enter')
    time.sleep(0.3)

    printpdf(f'a{well}-{i}')
    if mode == 'dual':
        setview_mode('report')
        printpdf(f'p{well}-{i}')


# exit_program()

def get_wellnum(mode, f):
    # 1 -- return 'w1'
    # else -- return 1
    if mode == 1:
        return f.split("_")[0]
    else:
        well = f.split("_")[0]
        return int(well[1:])


def get_window_title():
    hwnd = win32gui.GetForegroundWindow()
    window_text = win32gui.GetWindowText(hwnd)
    print(f'current window text : {window_text}')
    if 'aqtesolv' in window_text.lower():
        print("The string contains 'aqtesolv'")
        return True
    else:
        print("The string does not contain 'aqtesolv'")
        return False


def close_aqtesolvapp(n, mode):
    check = get_window_title()
    if n == 0:
        return 'Empty Files ....'
    else:
        print('Enter Shutdown Process ...')
        if check: pyautogui.hotkey('alt', 'f4')
        if mode == 'single':
            return 'exit single ...'
        else:
            for i in range(1, n + 1):
                pyautogui.press('n')
                print(f'closing window {i} ... ')
            return 'exit dual ...'


def main_job(mode):
    change_filename()
    delete_exisiting_pdffile()

    files = os.listdir()
    aqtfiles = [f for f in os.listdir() if f.endswith('.aqt')]
    print(f'aqtfiles : {len(aqtfiles)}')

    for i in range(1, 13):
        j = 0
        wfiles = fnmatch.filter(files, f"w{i}*.aqt")
        if not wfiles: return len(aqtfiles)
        for file in wfiles:
            j += 1
            print(f'{get_wellnum(2, file)}-{j}  - {file}')
            printing_job(i, j, file, mode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['single', 'dual'], help="Select 'single' or 'dual' mode.")
    args = parser.parse_args()

    n = main_job(args.mode)
    print('----------------------------------------------------------------')
    print(f'Process end .... return value from main_process is {n}')
    print('Shutdown AQTW32  Application ...')
    print('----------------------------------------------------------------')
    close_aqtesolvapp(n, args.mode)


if __name__ == "__main__":
    main()
