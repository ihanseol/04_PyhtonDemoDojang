from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time



s=Service("C:\\Program Files\\SeleniumBasic\\chromedriver.exe")
driver=webdriver.Chrome(service=s)
driver.maximize_window()
driver.get("https://www.facebook.com")

driver.find_element(By.XPATH, "//a[text()='새 계정 만들기']").click()

time.sleep(1)
month=driver.find_element(By.ID, "month")
monthDD=Select(month)


monthDD.select_by_index(3)
time.sleep(3)

monthDD.select_by_value('6')
time.sleep(3)

monthDD.select_by_visible_text("8월")