import xlwings as xw
import win32gui
import win32process

def get_excel_window_info():
    # Find the Excel window
    hwnd = win32gui.FindWindow("XLMAIN", None)
    if hwnd == 0:
        return None, None

    # Get the process ID associated with the window
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return hwnd, pid

def connect_to_excel():
    hwnd, pid = get_excel_window_info()
    if hwnd is not None and pid is not None:
        app = xw.App(connect=False)
        app.connect(handle=hwnd)
        return app
    else:
        print("Excel window not found.")
        return None

# Example usage
excel_app = connect_to_excel()
if excel_app:
    print("Connected to Excel application.")
else:
    print("Failed to connect to Excel application.")
