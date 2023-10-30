from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from webdriver_manager.chrome import ChromeDriverManager
import time
import os
import pandas as pd
from datetime import datetime

# Define the data as a list of dictionaries
data = [
    {'Area': '보은', 'name': 'BoEun', 'Code': 226, 'aCode': 55, 'switch': 54},
    {'Area': '서청주', 'name': 'SeoCheongJu', 'Code': 181, 'aCode': 56, 'switch': 54},
    {'Area': '제천', 'name': 'JaeCheon', 'Code': 221, 'aCode': 57, 'switch': 54},
    {'Area': '청주', 'name': 'CheongJu', 'Code': 131, 'aCode': 58, 'switch': 54},
    {'Area': '추풍령', 'name': 'ChuPungNyeong', 'Code': 135, 'aCode': 59, 'switch': 54},
    {'Area': '충주', 'name': 'ChungJu', 'Code': 127, 'aCode': 60, 'switch': 54},
    {'Area': '대전', 'name': 'DaeJeon', 'Code': 133, 'aCode': 28, 'switch': 28},
    {'Area': '세종', 'name': 'SeJong', 'Code': 239, 'aCode': 134, 'switch': 132},
    {'Area': '금산', 'name': 'GeumSan', 'Code': 238, 'aCode': 62, 'switch': 61},
    {'Area': '보령', 'name': 'BoRyung', 'Code': 235, 'aCode': 63, 'switch': 61},
    {'Area': '부여', 'name': 'BuYeo', 'Code': 236, 'aCode': 64, 'switch': 61},
    {'Area': '서산', 'name': 'SeoSan', 'Code': 129, 'aCode': 65, 'switch': 61},
    {'Area': '천안', 'name': 'CheonAn', 'Code': 232, 'aCode': 66, 'switch': 61},
    {'Area': '홍성', 'name': 'HongSung', 'Code': 177, 'aCode': 67, 'switch': 61},
]


def get_last_filename():
    download_folder = os.path.expanduser("~\\Downloads\\")
    # Get a list of all files in the directory
    files = os.listdir(download_folder)

    # Filter out only files (not directories)
    files = [f for f in files if os.path.isfile(os.path.join(download_folder, f))]

    # Get the most recently modified file
    latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(download_folder, f)))

    return latest_file


def change_filename_bydate(strArea, old_filename):
    download_folder = os.path.expanduser("~\\Downloads\\")
    os.chdir(download_folder)

    base_name, extension = os.path.splitext(old_filename)
    extension = extension[1:]

    current_date = datetime.now().strftime("%Y-%m-%d")
    new_filename = f'{strArea}_{current_date}.{extension}'

    if os.path.exists(new_filename):
        print(f"The file '{new_filename}' already exists. It will be overridden.")
        os.remove(new_filename)  # Remove the existing file

    os.rename(old_filename, new_filename)

    print('-----------------------------------------------------------------------')
    print(f"The file '{old_filename}' has been renamed to '{new_filename}'.")
    print('-----------------------------------------------------------------------')


def download_30year_data(driver, df, AreaSelection):
    myCode = df[df['Area'] == AreaSelection]['Code'].values[0]
    mySwitch = df[df['Area'] == AreaSelection]['switch'].values[0]

    one_string = f"ztree_{mySwitch}_switch"
    two_string = f"{AreaSelection} ({myCode})"

    print(f"one_string : {one_string}")
    print(f"two_string : {two_string}")

    # -------------------------------------------
    URL = 'https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69'
    driver.get(URL)
    driver.implicitly_wait(50)

    ddl = driver.find_element(By.CSS_SELECTOR, "#dataFormCd")
    select = Select(ddl)
    select.select_by_visible_text("월")
    time.sleep(1)

    # 지역선택
    driver.find_element(By.ID, "btnStn").click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, f"#{one_string}").click()
    time.sleep(1)

    driver.find_element(By.LINK_TEXT, two_string).click()
    time.sleep(1)

    driver.find_element(By.LINK_TEXT, "선택완료").click()
    time.sleep(1)

    # -------------------------------------------
    eYear = datetime.now().year - 1
    sYear = eYear - 29
    # -------------------------------------------
    # 년 월 버튼 , 클릭
    # -------------------------------------------

    ddl = driver.find_element(By.CSS_SELECTOR, "#startYear")
    select = Select(ddl)
    select.select_by_visible_text(str(sYear))
    time.sleep(0.5)

    ddl = driver.find_element(By.CSS_SELECTOR, "#endYear")
    select = Select(ddl)
    select.select_by_visible_text(str(eYear))
    time.sleep(0.5)

    # -------------------------------------------
    # 검색버튼 클릭
    # -------------------------------------------

    driver.find_element(By.CSS_SELECTOR, "button.SEARCH_BTN").click()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "a.DOWNLOAD_BTN").click()
    time.sleep(3)

    return get_last_filename()


def main():
    # Create a DataFrame from the data
    CN_LIST = ["대전", "금산", "보령", "부여", "서산", "천안"]

    customService = Service(ChromeDriverManager().install())
    customOption = Options()
    customOption.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=customService, options=customOption)

    df = pd.DataFrame(data)

    for location in CN_LIST:
        AreaSelection = location
        old_filename = download_30year_data(driver, df, AreaSelection)
        change_filename_bydate(AreaSelection, old_filename)

    driver.quit()


if __name__ == "__main__":
    main()

