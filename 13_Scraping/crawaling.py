from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager
import time

customService = Service(ChromeDriverManager().install())
customOption = Options()

driver = webdriver.Chrome(service=customService, options=customOption)


URL = 'https://datalab.naver.com/shoppingInsight/sCategory.naver'
driver.get(URL)
driver.implicitly_wait(10)



