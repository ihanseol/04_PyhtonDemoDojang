import psutil
import win32gui
import win32process
import win32con

def get_chrome_pid():
    for proc in psutil.process_iter(['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            return proc.info['pid']
    return None

def get_chrome_window_handle():
    # Find the Chrome browser process ID
    chrome_process_id = get_chrome_pid()
    if chrome_process_id is None:
        print("Chrome process not found.")
        return

    # Find the Chrome browser window handle
    window_handle = win32gui.GetTopWindow(0)
    while window_handle:
        thread_id, pid = win32process.GetWindowThreadProcessId(window_handle)
        if pid == chrome_process_id:
            print(f"Chrome browser window handle: {window_handle}")
            return
        window_handle = win32gui.GetWindow(window_handle, win32con.GW_HWNDNEXT)

    print("Chrome browser window not found.")

# Usage
get_chrome_window_handle()
