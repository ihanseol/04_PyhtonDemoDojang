
def getXLS_file():
    # Find the Chrome process ID
    chrome_process_name = "chrome.exe"
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == chrome_process_name:
            chrome_process_id = proc.pid
            break
    else:
        print("Chrome browser process not found.")
        exit()

    # Find the Chrome browser window handle
    window_handle = win32gui.GetTopWindow(0)
    while window_handle:
        thread_id, pid = win32process.GetWindowThreadProcessId(window_handle)
        if pid == chrome_process_id:
            break
        window_handle = win32gui.GetWindow(window_handle, win32con.GW_HWNDNEXT)

    if window_handle:
        print(f"Chrome browser window handle: {window_handle}")
    else:
        print("Chrome browser window not found.")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('debuggerAddress', f"localhost:9222/devtools/browser/{window_handle}")

    driver = webdriver.Chrome(options=chrome_options)
    # page_source = driver.page_source
    # print(page_source)

    driver.find_element(By.CSS_SELECTOR, "#sp_info_detail1 > a").click()

    driver.quit()