#
# it works ok
#

import win32gui
import win32com.client as win32

def find_excel_window_handle():
    # Callback function to check if window title contains 'Excel'
    def callback(hwnd, hwnds):
        if 'Excel' in win32gui.GetWindowText(hwnd):
            hwnds.append(hwnd)

    # List to store window handles
    hwnds = []

    # Enumerate through all windows
    win32gui.EnumWindows(callback, hwnds)

    # Return the first window handle found
    return hwnds[0] if hwnds else None


def get_excel_object_by_class(clsid):
    excel = win32.GetObject(Class=clsid)
    return excel

def get_excel_object_by_pathname(pathname):
    excel = win32.GetObject(Pathname=pathname)
    return excel

excel_by_pathname = get_excel_object_by_pathname(r"d:\05_Send\pythonProject\06_for ROT\Set ROT.xlsm")


if excel_by_pathname:
    print("Connected to Excel file using Pathname.")
    print(excel_by_pathname)



