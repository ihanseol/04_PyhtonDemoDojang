#
# 이것은, 기사용관정시에 관정을 클릭하면 관정제원이 나오고
# 다운로드 엑셀버튼을 누르면, 파일을 다운로드 받을수가 있는데
# 그것을 이용해서, 관정데이타를 가져오는 일을 한다.
#


from selenium import webdriver
import win32gui
import win32com.client
from selenium.webdriver.common.by import By

# return [yongdo_origin, yongdo, simdo, diameter, hp, q, tochool]
def write_to_excel(result):
    try:
        # 이미 실행 중인 Excel 애플리케이션에 연결
        excel = win32com.client.GetActiveObject("Excel.Application")
    except Exception as e:
        print("실행 중인 엑셀 인스턴스를 찾을 수 없습니다.")
        return


    wb = excel.ActiveWorkbook
    sheet = wb.ActiveSheet

    sheet.Cells(25, "K").Value = result[1]
    sheet.Cells(25, "F").Value = result[2]
    sheet.Cells(25, "G").Value = result[3]
    sheet.Cells(25, "H").Value = result[4]
    sheet.Cells(25, "I").Value = result[5]
    sheet.Cells(25, "J").Value = result[6]


def find_chrome_window(title_substring):
    def enum_windows_proc(hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd) and title_substring.lower() in win32gui.GetWindowText(hwnd).lower():
            lParam.append(hwnd)
        return True

    hwnds = []
    win32gui.EnumWindows(enum_windows_proc, hwnds)
    return hwnds



# return [yongdo_origin, yongdo, simdo, diameter, hp, q, tochool]
def get_well_data():
    print('-' * 55)
    window_handle = find_chrome_window("지하수")
    if not window_handle: exit()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option('debuggerAddress', f"localhost:9222/devtools/browser/{window_handle}")

    driver = webdriver.Chrome(options=chrome_options)

    _YONGDO_ORIGIN = "#tb_info_detail2 > tbody > tr:nth-child(3) > td:nth-child(4)"
    _YONGDO = "#tb_info_detail2 > tbody > tr:nth-child(4) > td:nth-child(2)"

    _SIMDO = "#tb_info_detail2 > tbody > tr:nth-child(5) > td:nth-child(2)"
    _DIAMETER = "#tb_info_detail2 > tbody > tr:nth-child(5) > td:nth-child(4)"
    _HP = "#tb_info_detail2 > tbody > tr:nth-child(7) > td:nth-child(4)"
    _Q = "#tb_info_detail2 > tbody > tr:nth-child(7) > td:nth-child(2)"
    _TOCHOOL = "#tb_info_detail2 > tbody > tr:nth-child(8) > td"

    yongdo_origin = driver.find_element(By.CSS_SELECTOR, _YONGDO_ORIGIN).text
    yongdo = driver.find_element(By.CSS_SELECTOR, _YONGDO).text

    simdo = driver.find_element(By.CSS_SELECTOR, _SIMDO).text
    diameter = driver.find_element(By.CSS_SELECTOR, _DIAMETER).text
    hp = driver.find_element(By.CSS_SELECTOR, _HP).text
    if not hp:
        hp = "0hp"

    q = driver.find_element(By.CSS_SELECTOR, _Q).text
    tochool = driver.find_element(By.CSS_SELECTOR, _TOCHOOL).text

    print(yongdo_origin, yongdo, simdo, diameter, hp, q, tochool)
    driver.quit()

    return [yongdo_origin, yongdo, simdo, diameter, hp, q, tochool]


def main():
    result = get_well_data()
    write_to_excel(result)


if __name__ == "__main__":
    main()
