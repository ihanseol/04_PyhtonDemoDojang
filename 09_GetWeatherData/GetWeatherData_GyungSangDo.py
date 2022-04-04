import now as now
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import datetime
import time

keys = ["대구", "대구(기)", "울산", "부산", "경주시", "구미", "문경", "봉화", "상주", "안동", "영덕", "영주", "영천", "울릉도", "울진", "의성", "청송군",
        "포항", "거제", "거창", "김해시", "남해", "밀양", "북창원", "산청", "양산시", "의령군", "진주", "창원", "통영", "함양군", "합천"]

values = [143, 176, 152, 159, 283, 279, 273, 271, 137, 136, 277, 272, 281, 115, 130, 278, 276, 138, 294, 284, 253, 295,
          288, 255, 289, 257, 263, 192, 155, 162, 264, 285]

strict = [19, 19, 30, 17, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 95, 110, 110, 110, 110, 110, 110, 110,
          110, 110, 110, 110, 110, 110, 110]

location_dict = dict(zip(keys, values))
strict_dict = dict(zip(keys, strict))

#
# print(len(keys))
# print(len(values))
# print(len(strict))


def get_location(name):
    one_string = 'ztree_' + str(strict_dict[name]) + '_switch'
    two_string = name + ' (' + str(location_dict[name]) + ')'
    return one_string, two_string


def find_rainfall(name):
    driver = webdriver.Chrome(r"C:\Program Files\SeleniumBasic\chromedriver.exe")
    url = r'https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69'

    one_string = 'ztree_' + str(strict_dict[name]) + '_switch'
    two_string = name + ' (' + str(location_dict[name]) + ')'

    driver.get(url)
    driver.maximize_window()

    time.sleep(0.5)

    # data separation
    month = driver.find_element(By.ID, "dataFormCd")
    monthDD = Select(month)
    monthDD.select_by_visible_text("월")

    time.sleep(0.5)

    # location
    driver.find_element(By.ID, "txtStnNm").click()
    time.sleep(0.5)
    driver.find_element(By.ID, one_string).click()
    time.sleep(0.5)
    driver.find_element(By.LINK_TEXT, two_string).click()

    time.sleep(0.5)
    # selection complete
    driver.find_element(By.LINK_TEXT, "선택완료").click()

    # start year
    time.sleep(0.5)
    now = datetime.datetime.now()
    e_year = now.year - 1
    s_year = e_year - 29

    startYear = driver.find_element(By.ID, "startYear")
    startYearDD = Select(startYear)
    startYearDD.select_by_visible_text(str(s_year))

    # end year
    time.sleep(0.5)
    endYear = driver.find_element(By.ID, "endYear")
    endYearDD = Select(endYear)
    endYearDD.select_by_visible_text(str(e_year))

    # search button
    time.sleep(0.5)
    driver.find_element(By.CLASS_NAME, "wrap_btn").click()

    # download excel file
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Excel").click()
    time.sleep(1)


find_rainfall('대구')
