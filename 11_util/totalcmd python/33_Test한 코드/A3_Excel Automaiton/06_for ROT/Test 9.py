import os
import pyautogui
import win32gui
import win32com.client as win32

def get_excel_from_filename(app_name):
    # Get the filename without extension

    # Find the window handle associated with the application
    hwnd = None
    while not hwnd:
        hwnd = win32gui.FindWindow(None, app_name)
        if not hwnd:
            print("Waiting for the application to open...")
            pyautogui.sleep(1)  # Wait for 1 second before retrying

    # Get the Excel application object using the window handle
    excel = win32.GetObject(Class="Excel.Application", hWnd=hwnd)

    return excel



excel_obj = get_excel_from_filename("Excel")
print(excel_obj)