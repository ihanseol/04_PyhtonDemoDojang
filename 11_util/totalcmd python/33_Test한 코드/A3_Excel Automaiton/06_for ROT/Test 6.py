import pythoncom
import pygetwindow as gw
import pyautogui
import win32com.client


def get_excel_process_id(window_title):
    # Find Excel window
    excel_window = gw.getWindowsWithTitle(window_title)
    if excel_window:
        return excel_window[0]._hWnd
    return None


# def connect_to_excel_instance(window_title):
#     try:
#         excel = win32com.client.Dispatch("Excel.Application")
#         hwnd = get_excel_process_id(window_title)
#         if hwnd:
#             excel.Hwnd = hwnd
#             return excel
#         else:
#             print("Excel window not found.")
#             return None
#     except Exception as e:
#         print("Error:", e)
#         return None


def connect_to_excel_instance(window_title):
    try:
        hwnd = get_excel_process_id(window_title)
        excel = win32com.client.Dispatch("Excel.Application")

        if hwnd:
            return excel
        else:
            print("Excel window not found.")
            return None
    except Exception as e:
        print("Error:", e)
        return None




if __name__ == "__main__":
    window_title = "Excel"
    excel = connect_to_excel_instance(window_title)
    if excel:
        excel.Visible = True  # Make Excel visible
        wb = excel.ActiveWorkBook
        ws = wb.ActiveSheet
        ws.Range("A10").Value = "Hello, World!"


        print("Data written successfully.")
    else:
        print("Failed to connect to Excel instance.")
