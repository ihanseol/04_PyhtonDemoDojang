import now as now
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

import datetime
import time

# 보은 (226)
# 제천 (221)
# 청주 (131)
# 추풍령 (135)
# 충주 (127)
# 대전 (133)
# 세종 (239)
# 금산 (238)
# 보령 (235)
# 부여 (236)
# 서산 (129)
# 천안 (232)
# 홍성 (177)

keys = ['보은', '제천', '청주', '추풍령', '충주', '대전', '세종', '금산', '보령', '부여', '서산', '천안', '홍성']
values = [226, 221, 131, 135, 127, 133, 239, 238, 235, 236, 129, 232, 177]
strict = [54, 54, 54, 54, 54, 28, 132, 60, 60, 60, 60, 60, 60]
location_dict = dict(zip(keys, values))
strict_dict = dict(zip(keys, strict))


# driver.find_element(By.ID, "ztree_60_switch").click()


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
    time.sleep(0.5)
    driver.find_element(By.LINK_TEXT, "Excel").click()


find_rainfall('금산')

