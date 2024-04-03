import win32gui

def find_chrome_window_by_title(title_name):
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and title_name.lower() in win32gui.GetWindowText(hwnd).lower():
            lParam.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(enum_windows_proc, hwnds)
    return hwnds[0] if hwnds else None

# Replace 'Your Specific Title Here' with the exact title of the Chrome window you're looking for
title_name = "국가지하수"
chrome_hwnd = find_chrome_window_by_title(title_name)
if chrome_hwnd:
    print(f"Found Chrome Window Handle: {chrome_hwnd}")
else:
    print("Chrome window with the specified title not found.")
