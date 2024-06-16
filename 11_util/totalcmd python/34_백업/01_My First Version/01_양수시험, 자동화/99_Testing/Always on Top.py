import win32gui
import win32con

def set_window_always_on_top(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd:
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0, win32con.SWP_NOMOVE | win32con.SWP_NOSIZE)
    else:
        print(f"Window with title '{window_title}' not found.")


# run_background_timer()
set_window_always_on_top('timer')
