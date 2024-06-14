import win32gui
import win32process
import win32com.client

def get_excel_window_info():
    # Find the Excel window
    hwnd = win32gui.FindWindow("XLMAIN", None)
    if hwnd == 0:
        return None, None

    # Get the process ID associated with the window
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return hwnd, pid

def connect_to_excel(hwnd):
    # Connect to Excel application using window handle
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = True  # Optional: make Excel visible
    excel.Hwnd = hwnd  # Set the window handle
    return excel

def write_to_cell(excel, cell, value):
    # Access the specific cell and set its value
    excel.Range(cell).Value = value

# Get Excel window handle and process ID
hwnd, pid = get_excel_window_info()
if hwnd is not None:
    # Connect to Excel using window handle
    excel_app = connect_to_excel(hwnd)

    # Write "hello world" to cell A10
    write_to_cell(excel_app, "A10", "hello world")

    # Release Excel application
    excel_app.Quit()
else:
    print("Excel window not found.")