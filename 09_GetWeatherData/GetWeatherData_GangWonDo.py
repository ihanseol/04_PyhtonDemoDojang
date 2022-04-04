import now as now
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import datetime
import time

keys = ["강릉", "대관령", "동해", "북강릉", "북춘천", "삼척", "속초", "영월", "원주", "인제", "정선군", "철원", "춘천", "태백", "홍천", ]
values = [105, 100, 106, 104, 93, 214, 90, 121, 114, 211, 217, 95, 101, 216, 212]
strict = [38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38]

location_dict = dict(zip(keys, values))
strict_dict = dict(zip(keys, strict))

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


find_rainfall('춘천')

