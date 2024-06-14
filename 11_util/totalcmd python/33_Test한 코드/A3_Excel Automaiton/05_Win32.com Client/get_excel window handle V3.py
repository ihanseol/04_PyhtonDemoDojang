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


# Get Excel window handle and process ID
hwnd, pid = get_excel_window_info()

if hwnd is not None:
    # Connect to Excel using window handle
    app = xw.apps.Connect(handle=hwnd)

    # Access the active workbook
    wb = app.books.active

    # Write "hello world" to cell A10
    wb.sheets[0].range("A10").value = "hello world"
else:
    print("Excel window not found.")
