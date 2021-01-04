
import urllib.request
import bs4

url = "https://www.naver.com"
html = urllib.request.urlopen(url)

bsobj = bs4.BeautifulSoup(html, "html.parser")

# print(bsobj)

topright = bsobj.find("div", {"class" : "service_area"})
print(topright)

atag = topright.find_all("a")

print(type(atag))

print(atag[0].text)

























