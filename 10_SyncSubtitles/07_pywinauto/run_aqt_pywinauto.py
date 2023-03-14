import os
import time
import glob
import fnmatch
import copy
from pywinauto import application

program_path = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
is_aqt_open = False

def setview_default():
    app['AQTESOLV for Windows'].MenuSelect("View->Set view->Default")
    time.sleep(0.1)

def setview_report():
    app['AQTESOLV for Windows'].MenuSelect("View->Set view->Report")
    time.sleep(0.1)


def delete_existing_pdf_files():
    dir_path = os.path.expanduser("~\\Documents\\")
    for filename in os.listdir(dir_path):
        if filename.endswith(".pdf"):
            os.remove(os.path.join(dir_path, filename))

def print_pdf(fname):
    app['AQTESOLV for Windows'].TypeKeys("^p")
    app['AQTESOLV for Windows'].TypeKeys("{ENTER}")
    time.sleep(0.3)
    app['AQTESOLV for Windows'].TypeKeys(fname)
    app['AQTESOLV for Windows'].TypeKeys("{ENTER}")
    time.sleep(0.3)

def exit_program():
    app['AQTESOLV for Windows'].TypeKeys("%{F4}")
    time.sleep(0.1)
    app['AQTESOLV for Windows'].TypeKeys("n")

def change_filename(): 
    directory = "d:\\05_Send\\"
    for filename in os.listdir():
        if filename.endswith(".aqt"):
            name, ext = os.path.splitext(filename)
            if "- 복사본" in name:
                new_name = name.replace(" - 복사본", "_01") + ext
                os.rename(os.path.join(directory, filename), os.path.join(directory, new_name))

def remove_extension(file_name):
    return os.path.splitext(file_name)[0]

def main_job(well, i, filename):
    global is_aqt_open
    if not is_aqt_open:
        app = application.Application()
        app.start(program_path)
        is_aqt_open = True

    time.sleep(0.3)
    app['AQTESOLV for Windows'].TypeKeys("^o")
    app['AQTESOLV for Windows'].TypeKeys(filename)
    app['AQTESOLV for Windows'].TypeKeys("{ENTER}")
    time.sleep(0.3)

    print_pdf(f'a{well}-{i}')
    setview_report()
    print_pdf(f'p{well}-{i}')

def get_well_num(mode, f):
    # 1 -- return 'w1'
    # else -- return 1
    if mode == 1:
        return f.split("_")[0]
    else:
        well = f.split("_")[0]
        return int(well[1:])

def shutdown_apps(n):
    print('Enter Shutdown Process ...')
    app['AQTESOLV for Windows'].TypeKeys("%{F4}")
    for i in range(1, n+1):
        app['AQTESOLV for Windows'].TypeKeys("n")
        print(f'closing window {i} ... ')

def main_process():
    change_filename()
    delete_existing_pdf_files()

    files = os.listdir()
    aqt_files = [f for f in os.listdir() if f.endswith('.aqt')]
    print(f'aqt_files: {len(aqt_files)}')

    for i in range(1, 13):
        j = 0
        w_files = fnmatch.filter(files, f"w{i}*.aqt")
        if not w_files:
            return len(aqt_files)
        for file in w_files:
            j += 1
            print(f'{get_well_num(2,file)}-{j}  - {file}')
            main_job(i, j, file)



if __name__ == "__main__":
    app = application.Application()
    main_process()
    print('\n'*1)
    print(f'Process end ....')
    print('Shutdown AQTW32  Application ...')
    print('\n'*1)
    shutdown_apps(len(aqt_files))