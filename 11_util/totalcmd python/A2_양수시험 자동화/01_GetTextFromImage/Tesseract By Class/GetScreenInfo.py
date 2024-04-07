""""

01_지하수용도 (YongDo) : 1790,528   105x46
02_지하수세부용도 (Sebu): 1551, 595  105x46
03_심도 (Simdo ): 1551x662  105x32
04_굴착직경 (WellDiameter): 1790x662  101x32
05_동력장치마력 (WellHP) : 1790x691 105x46
06_양수능력 (WellQ): 1551x691 - 105x46
07_토출관 (WellTochul ): 1551x743 - 105x46

"""


from selenium import webdriver
import time
from screeninfo import get_monitors

primary_monitor = get_monitors()[0]
print(f"Primary Monitor Resolution: {primary_monitor.width}x{primary_monitor.height}")


driver = webdriver.Chrome()
driver.get("http://naver.com")

driver.maximize_window()
size = driver.get_window_size()
width = size['width']
height = size['height']

print(f"Width: {width}, Height: {height}")

time.sleep(10)

driver.quit()


