import os, time, glob
import fnmatch
import copy, argparse
import pyautogui
import win32gui
import ctypes

# if install error occured
# If the issue persists, you can try installing the pywin32 module instead of win32gui,
# which includes win32gui as well as other Windows-specific modules.
# You can install it using the following command:
# pip install pywin32

program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
isAqtOpen = False
directory = "d:\\05_Send\\"
_DELAY_ = 0.4


def setview_mode(mode):
    pyautogui.hotkey('alt', 'v')
    time.sleep(0.2)

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
    print('----------------------------------------------------------------')
    dir_path = os.path.expanduser("~\\Documents\\")
    delete_pdf(dir_path)
    delete_pdf(directory)

def printpdf(fname):
    pyautogui.hotkey('ctrl', 'p')
    pyautogui.press('enter')
    time.sleep(_DELAY_ )
    pyautogui.typewrite(fname)
    pyautogui.press('enter')
    time.sleep(_DELAY_)


def exit_program():
    pyautogui.hotkey('alt', 'f4')
    time.sleep(_DELAY_)
    pyautogui.press('n')


def change_filename():
    global directory
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext == ".aqt" and "_01" not in name:  # Added condition to avoid renaming files that already have the "_01" suffix
            if "- 복사본" in name:  # Moved this condition to the top of the if statement for readability 
                new_name = name.replace(" - 복사본", "_01") + ext
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))

            if "- Copy" in name:  # Moved this condition to the top of the if statement for readability 
                new_name = name.replace(" - Copy", "_01") + ext
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))


def remove_extension(file_name):
    return os.path.splitext(file_name)[0]


def printing_job(well, i, filename, mode):
    open_aqt()
    open_file(filename)
    printpdf(f'a{well}-{i}')

    if mode == 'dual':
        setview_mode('report')
        printpdf(f'p{well}-{i}')
        

def open_aqt():
    global isAqtOpen 

    if not isAqtOpen: 
        os.startfile(program_path) 
        isAqtOpen = True 

    time.sleep(_DELAY_) 

    
def open_file(filename): 
    pyautogui.hotkey('ctrl', 'o') 
    pyautogui.typewrite(directory+filename) 
    pyautogui.press('enter')

    time.sleep(_DELAY_)  


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
    if n == 0:
        return 'Empty Files ....'

    print('Enter Shutdown Process ...')

    if check: 
        pyautogui.hotkey('alt', 'f4')

    if mode == 'single':
        return 'exit single ...'

    for i in range(1, n + 1):
        pyautogui.press('n')
        print(f'closing window {i} ... ')

    return 'exit dual ...'



def main_job(mode):
    change_filename()
    delete_existing_pdffile()

    files = os.listdir()
    aqtfiles = [f for f in os.listdir() if f.endswith('.aqt')]
    print('----------------------------------------------------------------')
    print(f'aqtfiles : {len(aqtfiles)}')
    print('----------------------------------------------------------------')

    for i in range(1, 13):
        wfiles = fnmatch.filter(files, f"w{i}*.aqt")
        if not wfiles: return len(aqtfiles)
        for j, file in enumerate(wfiles): # Added enumerate to keep track of the index of the file in the list 
            print(f'{get_wellnum(2, file)}-{j + 1}  - {file}') # Added +1 to j to start counting from 1 instead of 0 
            printing_job(i, j + 1, file, mode)



def main():
    parser = argparse.ArgumentParser(description="Select 'single' or 'dual' mode.")
    parser.add_argument('mode', choices=['single', 'dual'])
    args = parser.parse_args()

    user32 = ctypes.windll.user32
    user32.BlockInput(True)

    n = main_job(args.mode)
    print('----------------------------------------------------------------')
    print(f'Process end .... return value from main_process is {n}')
    print('Shutdown AQTW32  Application ...')
    print('----------------------------------------------------------------')
    close_aqtesolvapp(n, args.mode)
    time.sleep(1)

    user32.BlockInput(False)

if __name__ == "__main__":
    main()

