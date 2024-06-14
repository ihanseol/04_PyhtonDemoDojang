import win32gui

def find_chrome_window(title_substring):
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and title_substring.lower() in win32gui.GetWindowText(hwnd).lower():
            lParam.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(enum_windows_proc, hwnds)
    return hwnds

# Use part of the Chrome window title to find it; adjust as needed.
chrome_hwnds = find_chrome_window("Chrome")
for hwnd in chrome_hwnds:
    print(f"Chrome Window Handle: {hwnd}, Window Title: {win32gui.GetWindowText(hwnd)}")
