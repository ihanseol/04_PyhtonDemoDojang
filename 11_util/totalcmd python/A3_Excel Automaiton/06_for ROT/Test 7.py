import pythoncom
import pygetwindow as gw
import win32com.client as win32

def get_excel_process_id(window_title):
    # Find Excel window
    excel_window = gw.getWindowsWithTitle(window_title)
    if excel_window:
        return excel_window[0]._hWnd
    return None

# Connect to Excel application
excel = win32.gencache.EnsureDispatch('Excel.Application')
excel.Visible = True  # Make Excel visible (optional)

# Get the process ID of the Excel window
window_title = "Excel"
excel_hwnd = get_excel_process_id(window_title)

# If Excel window found, activate it
if excel_hwnd:
    excel = win32.GetObject(Class="Excel.Application")
    excel.Visible = True

    # Select cell A10 and insert "Hello World"
    excel.Range("A10").Value = "Hello World"
else:
    print("Excel window not found.")


