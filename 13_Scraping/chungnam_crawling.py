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
# 대전, 금산, 보령, 부여, 서산, 천안, 청주, 충주
data = [
    {'Area': '관악산', 'name': 'GwanAkSan', 'Code': 116, 'aCode': 15, 'switch': 14},
    {'Area': '서울', 'name': 'Seoul', 'Code': 108, 'aCode': 16, 'switch': 14},
    {'Area': '강화', 'name': 'GangHwa', 'Code': 201, 'aCode': 23, 'switch': 22},
    {'Area': '백령도', 'name': 'BaengNyeongDo', 'Code': 102, 'aCode': 24, 'switch': 22},
    {'Area': '인천', 'name': 'InCheon', 'Code': 112, 'aCode': 25, 'switch': 22},
    {'Area': '동두천', 'name': 'DongDuCheon', 'Code': 98, 'aCode': 33, 'switch': 32},
    {'Area': '수원', 'name': 'SuWon', 'Code': 119, 'aCode': 34, 'switch': 32},
    {'Area': '양평', 'name': 'YangPyung', 'Code': 202, 'aCode': 35, 'switch': 32},
    {'Area': '이천', 'name': 'LeeCheon', 'Code': 203, 'aCode': 36, 'switch': 32},
    {'Area': '파주', 'name': 'PaJu', 'Code': 99, 'aCode': 37, 'switch': 32},

    {'Area': '강릉', 'name': 'GangNeung', 'Code': 105, 'aCode': 39, 'switch': 38},
    {'Area': '대관령', 'name': 'DaeGwallYeong', 'Code': 100, 'aCode': 40, 'switch': 38},
    {'Area': '동해', 'name': 'DongHae', 'Code': 106, 'aCode': 41, 'switch': 38},
    {'Area': '북강릉', 'name': 'NorthGangNeung', 'Code': 104, 'aCode': 42, 'switch': 38},
    {'Area': '북춘천', 'name': 'BukChunCheon', 'Code': 93, 'aCode': 43, 'switch': 38},
    {'Area': '삼척', 'name': 'Samcheok', 'Code': 214, 'aCode': 44, 'switch': 38},
    {'Area': '속초', 'name': 'SokCho', 'Code': 90, 'aCode': 45, 'switch': 38},
    {'Area': '영월', 'name': 'YoungWol', 'Code': 121, 'aCode': 46, 'switch': 38},
    {'Area': '원주', 'name': 'WonJu', 'Code': 114, 'aCode': 47, 'switch': 38},
    {'Area': '인제', 'name': 'InJae', 'Code': 211, 'aCode': 48, 'switch': 38},
    {'Area': '정선군', 'name': 'JungSeonGun', 'Code': 217, 'aCode': 49, 'switch': 38},
    {'Area': '철원', 'name': 'CheolWon', 'Code': 95, 'aCode': 50, 'switch': 38},
    {'Area': '춘천', 'name': 'ChunCheon', 'Code': 101, 'aCode': 51, 'switch': 38},
    {'Area': '태백', 'name': 'TaeBaeg', 'Code': 216, 'aCode': 52, 'switch': 38},
    {'Area': '홍천', 'name': 'HongCheon', 'Code': 212, 'aCode': 53, 'switch': 38},


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

    {'Area': '광주', 'name': 'GwangJu', 'Code': 156, 'aCode': 27, 'switch': 26},
    {'Area': '고창', 'name': 'GoChang', 'Code': 172, 'aCode': 69, 'switch': 68},
    {'Area': '고창군', 'name': 'GochangGun', 'Code': 251, 'aCode': 70, 'switch': 68},
    {'Area': '군산', 'name': 'GunSan', 'Code': 140, 'aCode': 71, 'switch': 68},
    {'Area': '남원', 'name': 'NamWon', 'Code': 247, 'aCode': 72, 'switch': 68},
    {'Area': '부안', 'name': 'BuAn', 'Code': 243, 'aCode': 73, 'switch': 68},
    {'Area': '순창군', 'name': 'SunchangGun', 'Code': 254, 'aCode': 74, 'switch': 68},
    {'Area': '임실', 'name': 'ImSil', 'Code': 244, 'aCode': 75, 'switch': 68},
    {'Area': '장수', 'name': 'JangSsoo', 'Code': 248, 'aCode': 76, 'switch': 68},
    {'Area': '전주', 'name': 'JeonJu', 'Code': 146, 'aCode': 77, 'switch': 68},
    {'Area': '정읍', 'name': 'Jungeup', 'Code': 245, 'aCode': 78, 'switch': 68},
    {'Area': '강진군', 'name': 'Gangjingun', 'Code': 259, 'aCode': 80, 'switch': 79},
    {'Area': '고흥', 'name': 'Goheung', 'Code': 262, 'aCode': 81, 'switch': 79},
    {'Area': '광양시', 'name': 'Gwangyang', 'Code': 266, 'aCode': 82, 'switch': 79},
    {'Area': '목포', 'name': 'MokPo', 'Code': 165, 'aCode': 83, 'switch': 79},
    {'Area': '무안', 'name': 'MuAn', 'Code': 164, 'aCode': 84, 'switch': 79},
    {'Area': '보성군', 'name': 'BosungGun', 'Code': 258, 'aCode': 85, 'switch': 79},
    {'Area': '순천', 'name': 'Suncheon', 'Code': 174, 'aCode': 86, 'switch': 79},
    {'Area': '여수', 'name': 'Yeosu', 'Code': 168, 'aCode': 87, 'switch': 79},
    {'Area': '영광군', 'name': 'YeongGwangGun', 'Code': 252, 'aCode': 88, 'switch': 79},
    {'Area': '완도', 'name': 'WanDo', 'Code': 170, 'aCode': 89, 'switch': 79},
    {'Area': '장흥', 'name': 'JangHeung', 'Code': 260, 'aCode': 90, 'switch': 79},
    {'Area': '주암', 'name': 'JuAm', 'Code': 256, 'aCode': 91, 'switch': 79},
    {'Area': '진도(첨철산)', 'name': 'JinDo', 'Code': 175, 'aCode': 92, 'switch': 79},
    {'Area': '진도군', 'name': 'JinDoGun', 'Code': 268, 'aCode': 93, 'switch': 79},
    {'Area': '해남', 'name': 'HaeNam', 'Code': 261, 'aCode': 94, 'switch': 79},
    {'Area': '흑산도', 'name': 'HeukSanDo', 'Code': 169, 'aCode': 95, 'switch': 79},

    {'Area': '대구', 'name': 'DaeGu', 'Code': 143, 'aCode': 20, 'switch': 19},
    {'Area': '대구(기)', 'name': 'DaeGuGi', 'Code': 176, 'aCode': 21, 'switch': 19},
    {'Area': '울산', 'name': 'WoolSan', 'Code': 152, 'aCode': 31, 'switch': 30},
    {'Area': '부산', 'name': 'BuSan', 'Code': 159, 'aCode': 18, 'switch': 17},
    {'Area': '경주시', 'name': 'GyungJuSi', 'Code': 283, 'aCode': 97, 'switch': 96},
    {'Area': '구미', 'name': 'GuMi', 'Code': 279, 'aCode': 98, 'switch': 96},
    {'Area': '문경', 'name': 'MunGyung', 'Code': 273, 'aCode': 99, 'switch': 96},
    {'Area': '봉화', 'name': 'BongHwa', 'Code': 271, 'aCode': 100, 'switch': 96},
    {'Area': '상주', 'name': 'SangJu', 'Code': 137, 'aCode': 101, 'switch': 96},
    {'Area': '안동', 'name': 'AnDong', 'Code': 136, 'aCode': 102, 'switch': 96},
    {'Area': '영덕', 'name': 'YeongDeok', 'Code': 277, 'aCode': 103, 'switch': 96},
    {'Area': '영주', 'name': 'YeongJu', 'Code': 272, 'aCode': 104, 'switch': 96},
    {'Area': '영천', 'name': 'YeongCheon', 'Code': 281, 'aCode': 105, 'switch': 96},
    {'Area': '울릉도', 'name': 'UlLeungDo', 'Code': 115, 'aCode': 106, 'switch': 96},
    {'Area': '울진', 'name': 'UlJin', 'Code': 130, 'aCode': 107, 'switch': 96},
    {'Area': '의성', 'name': 'UiSeong', 'Code': 278, 'aCode': 108, 'switch': 96},
    {'Area': '청송군', 'name': 'CheongSongGun', 'Code': 276, 'aCode': 109, 'switch': 96},
    {'Area': '포항', 'name': 'PoHang', 'Code': 138, 'aCode': 110, 'switch': 96},
    {'Area': '거제', 'name': 'GeoJae', 'Code': 294, 'aCode': 112, 'switch': 111},
    {'Area': '거창', 'name': 'GeoChang', 'Code': 284, 'aCode': 113, 'switch': 111},
    {'Area': '김해시', 'name': 'KimHaeSi', 'Code': 253, 'aCode': 114, 'switch': 111},
    {'Area': '남해', 'name': 'NamHae', 'Code': 295, 'aCode': 115, 'switch': 111},
    {'Area': '밀양', 'name': 'MilYang', 'Code': 288, 'aCode': 116, 'switch': 111},
    {'Area': '북창원', 'name': 'BukChangWon', 'Code': 255, 'aCode': 117, 'switch': 111},
    {'Area': '산청', 'name': 'SanCheong', 'Code': 289, 'aCode': 118, 'switch': 111},
    {'Area': '양산시', 'name': 'YangSan', 'Code': 257, 'aCode': 119, 'switch': 111},
    {'Area': '의령군', 'name': 'UiRyung', 'Code': 263, 'aCode': 120, 'switch': 111},
    {'Area': '진주', 'name': 'JinJu', 'Code': 192, 'aCode': 121, 'switch': 111},
    {'Area': '창원', 'name': 'ChangWon', 'Code': 155, 'aCode': 122, 'switch': 111},
    {'Area': '통영', 'name': 'TongYeong', 'Code': 162, 'aCode': 123, 'switch': 111},
    {'Area': '함양군', 'name': 'HamYang', 'Code': 264, 'aCode': 124, 'switch': 111},
    {'Area': '합천', 'name': 'HapCheon', 'Code': 285, 'aCode': 125, 'switch': 111},

    {'Area': '고산', 'name': 'GoSan', 'Code': 185, 'aCode': 127, 'switch': 126},
    {'Area': '서귀포', 'name': 'SeoGuiPo', 'Code': 189, 'aCode': 128, 'switch': 126},
    {'Area': '성산', 'name': 'SungSan', 'Code': 188, 'aCode': 129, 'switch': 126},
    {'Area': '성산2', 'name': 'SungSan2', 'Code': 187, 'aCode': 130, 'switch': 126},
    {'Area': '성산포', 'name': 'SungSanPo', 'Code': 265, 'aCode': 131, 'switch': 126},
    {'Area': '제주', 'name': 'JaeJu', 'Code': 184, 'aCode': 132, 'switch': 126}

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
    driver.implicitly_wait(20)

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
    # CN_LIST = ["대구", "전주", "부산"]

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

