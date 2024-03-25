from selenium import webdriver
import win32con
import win32gui
import win32process
import psutil
import pyautogui


def maxmize_excel():
    win = pyautogui.getWindowsWithTitle('Excel')[0]
    if not win.isActive:
        win.activate()
    if not win.isMaximized:
        win.maximize()


# Find the excel process ID
def find_process_id(findAPPNAME):
    # excel_process_name = "EXCEL.EXE"
    excel_process_name = findAPPNAME

    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == excel_process_name:
            excel_process_id = proc.pid
            return excel_process_id
    else:
        print("excel  process not found.")
        exit()


# Find  window handle

def find_window_handle(findAPPNAME):
    #excel_process_id = find_process_id("EXCEL.EXE")
    excel_process_id = find_process_id(findAPPNAME)

    window_handle = win32gui.GetTopWindow(0)
    while window_handle:
        thread_id, pid = win32process.GetWindowThreadProcessId(window_handle)
        if pid == excel_process_id:
            break
        window_handle = win32gui.GetWindow(window_handle, win32con.GW_HWNDNEXT)

    if window_handle:
        print(f"excel browser window handle: {window_handle}")
        return window_handle
    else:
        print("excel browser window not found.")
        return False


# hwnd = find_window_handle("EXCEL.EXE")
# win32gui.SetForegroundWindow(hwnd)

maxmize_excel()


# ----------------------------------------------------------------------------------------------------


# import win32gui
# import win32process
# import win32com.client
# import win32con
#
#
# def make_front(hwnd):
#     shell = win32com.client.Dispatch("WScript.Shell")
#     shell.SendKeys('%')
#     win32gui.ShowWindow(hwnd, win32con.SW_SHOWNORMAL)
#     win32gui.SetForegroundWindow(hwnd)
#     win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)  # Maximize the window
#
#
# def main():
#     hwnd = win32gui.FindWindow("XLMAIN", None)
#
#     if hwnd:
#         make_front(hwnd)
#     else:
#         print("Excel window not found.")
#
#
# if __name__ == "__main__":
#     main()


# ----------------------------------------------------------------------------------------------------


# from pywinauto import Application, findwindows
#
#
# def make_front(hwnd):
#     app = Application().connect(handle=hwnd)
#     window = app.window(handle=hwnd)
#     window.set_focus()
#
#
# def main():
#     hwnd = findwindows.find_window(class_name="XLMAIN")
#
#     if hwnd:
#         make_front(hwnd)
#     else:
#         print("Excel window not found.")
#
#
# if __name__ == "__main__":
#     main()
