import win32gui
import win32process
import win32com.client


# Function to get the window handle and process ID of Excel
def find_excel_window():
    def callback(hwnd, hwnds):
        if win32gui.GetClassName(hwnd) == 'XLMAIN':
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            hwnds.append((hwnd, pid))
        return True

    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds


# Connect to Excel and set the value of cell A10
def set_excel_cell_value(hwnd, value):
    xl = win32com.client.Dispatch("Excel.Application")
    xl.Visible = True
    xl.Workbooks.Add()
    xl.Visible = True
    xl.Hwnd = hwnd
    wb = xl.Workbooks(1)
    ws = wb.Worksheets(1)
    ws.Range("A10").Value = value


# Main function
def main():
    # Find Excel window handle and process ID
    excel_info = find_excel_window()
    if excel_info:
        hwnd, pid = excel_info[0]
        print("Excel window handle:", hwnd)
        print("Excel process ID:", pid)

        # Set the value of cell A10
        set_excel_cell_value(hwnd, "hello world")
    else:
        print("Excel is not running.")


if __name__ == "__main__":
    main()
