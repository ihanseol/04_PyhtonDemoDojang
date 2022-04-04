import now as now
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import datetime
import time

keys = ['광주', '고창', '고창군', '군산', '남원', '부안', '순창군', '임실', '장수', '전주', '정읍', '강진군', '고흥', '광양시', '목포', '무안', '보성군', '순천',
        '여수', '영광군', '완도', '장흥', '주암', '진도(첨찰산)', '진도군', '해남', '흑산도']
values = [156, 172, 251, 140, 247, 243, 254, 244, 248, 146, 245, 259, 262, 266, 165, 164, 258, 174, 168, 252, 170, 260,
          256, 175, 268, 261, 169]
strict = [26, 67, 67, 67, 67, 67, 67, 67, 67, 67, 67, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78, 78]

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
    GetWeatherData_DaejeonSejong.py
    # download excel file
    time.sleep(1)
    driver.find_element(By.LINK_TEXT, "Excel").click()
    time.sleep(1)


find_rainfall('고흥')
