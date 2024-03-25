import win32gui


def get_chrome_window_handle():
    chrome_window = None
    toplist = []
    winlist = []

    def enum_cb(hwnd, results):
        winlist.append((hwnd, win32gui.GetWindowText(hwnd)))

    win32gui.EnumWindows(enum_cb, toplist)

    for (hwnd, title) in winlist:
        if '지하수' in title:
            chrome_window = hwnd
            break

    return chrome_window


# Usage
chrome_handle = get_chrome_window_handle()
print("Chrome Window Handle:", chrome_handle)
