#
# running ok , excel is finding ...
# get_Process_Name
#

import ctypes
import pythoncom

def get_process_names():
    # Load necessary functions from user32.dll
    user32 = ctypes.windll.user32

    # Set up buffers and variables
    process_names = []

    # Callback function to retrieve window titles
    def enum_windows_callback(hwnd, _):
        title = ctypes.create_unicode_buffer(512)  # Buffer for window title
        user32.GetWindowTextW(hwnd, title, ctypes.sizeof(title))
        if title.value:  # Check if title is not empty
            process_names.append(title.value)
        return True

    # Define the type of the callback function
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))

    # Cast the callback function to the correct type
    callback = EnumWindowsProc(enum_windows_callback)

    # Enumerate windows and retrieve titles
    user32.EnumWindows(callback, 0)

    return process_names

if __name__ == "__main__":
    process_names = get_process_names()
    for name in process_names:
        print(name)
