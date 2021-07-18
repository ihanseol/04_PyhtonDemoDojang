
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = 'https://www.assembly.go.kr/assm/memact/congressman/memCond/memCondListAjax.do'
params = {'currentPage':1, 'rowPerPage':300}
html = requests.get(url, params=params).text
soup=BeautifulSoup(html, 'html.parser')



#
# for idx, tag in enumerate(soup.select('a[href*=jsMemPop]'), 1):
#     print('[{}] {}'.format(idx, tag.text))

names = []
for tag in soup.select('a[href*=jsMemPop]'):
    names.append(tag.text)

series = pd.Series(names)
series.str.slice(0, 1).value_counts().plot(kind='bar', figsize=(12, 3))


