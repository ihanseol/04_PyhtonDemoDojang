import requests
from bs4 import BeautifulSoup

url = "https://news.naver.com"



raw = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
html = BeautifulSoup(raw.text, "html.parser")


main_title = html.find("ul", {"class" : "hdline_article_list"})

lis = main_title.find_all("li")

for li in lis:
    # print(f"'{li.text}'")
    str_text = li.text
    str_text = str_text.strip()
    str_text = str_text.replace("\n","")
    print(str_text)





