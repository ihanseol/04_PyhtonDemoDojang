# 소스코드 - 자세한 사용법은 유튜브 영상을 참조하세요.
# 영상 제작 날짜 기준의 코드입니다. 이후 사이트 구조가 달라지거나 기타 이유로 작동하지 않을 수 있습니다.
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

import time

driver = webdriver.Chrome()
url = 'https://google.com'
driver.get(url)
driver.maximize_window()
action = ActionChains(driver)

driver.find_element_by_css_selector('#gb_70').click()

action.send_keys('본인아이디').perform()
action.reset_actions()
driver.find_element_by_css_selector('.CwaK9').click()

time.sleep(2)
driver.find_element_by_css_selector('.whsOnd.zHQkBf').send_keys('본인비밀번호')
driver.find_element_by_css_selector('.CwaK9').click()
time.sleep(2)

driver.get('https://mail.google.com/mail/u/0/?ogbl#inbox')
time.sleep(2)

driver.find_element_by_css_selector('.T-I.J-J5-Ji.T-I-KE.L3').click()
time.sleep(1)

send_buton = driver.find_element_by_css_selector('.gU.Up')

(
action.send_keys('보낼메일주소').key_down(Keys.ENTER).pause(2).key_down(Keys.TAB)
.send_keys('제목입니다.').pause(2).key_down(Keys.TAB)
.send_keys('abcde').pause(2).key_down(Keys.ENTER)
.key_down(Keys.SHIFT).send_keys('abcde').key_up(Keys.SHIFT).pause(2)
.move_to_element(send_buton).click()
.perform()
)