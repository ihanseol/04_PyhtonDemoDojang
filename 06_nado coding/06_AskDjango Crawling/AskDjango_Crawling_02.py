import requests
from bs4 import BeautifulSoup

# importing required package of webdriver
from selenium import webdriver

# Just Run this to execute the below script

if __name__ == '__main__':
    # Instantiate the webdriver with the executable location of MS Edge web driver
    browser = webdriver.Edge(r"c:\Program Files\SeleniumBasic\msedgedriver.exe")
    # Simply just open a new Edge browser and go to lambdatest.com
    browser.get('https://www.google.com/')

soup = BeautifulSoup(browser.page_source, 'html.parser')
print(soup.find('h1').text)



