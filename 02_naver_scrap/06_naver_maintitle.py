
import urllib.request
import bs4

url = "https://www.naver.com"
html = urllib.request.urlopen(url)

bs_obj = bs4.BeautifulSoup(html, "html.parser")

# print(bs_obj)

main_title = bs_obj.find("ul", {"class" : "list_nav type_fix"})

lis = main_title.find_all("li")

for li in lis:
    print(li.text)
































