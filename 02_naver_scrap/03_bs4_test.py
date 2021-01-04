import bs4

html = "<html><div></div></html>"
bsobj = bs4.BeautifulSoup(html, "html.parser")

print(type(bsobj))
print(bsobj)
print(bsobj.find("div"))


