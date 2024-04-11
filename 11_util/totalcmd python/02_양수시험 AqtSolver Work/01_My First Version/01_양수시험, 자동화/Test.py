import win32com.client
import pyautogui


def activate_excel_and_send_keys():
    try:
        # Try to get an existing instance of Excel
        xl_app = win32com.client.GetActiveObject("Excel.Application")
    except:
        # If Excel is not running, create a new instance
        xl_app = win32com.client.Dispatch("Excel.Application")

    # Make Excel application window visible and bring it to the front

    print(xl_app)


    # Send Enter key press event
    pyautogui.press('enter')



if __name__ == "__main__":
    activate_excel_and_send_keys()
