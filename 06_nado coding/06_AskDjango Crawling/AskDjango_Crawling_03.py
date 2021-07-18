from bs4 import BeautifulSoup
from selenium import webdriver
import requests

# url = 'http://www.ichangtou.com/#company:data_000008.html'
# headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#
# response = requests.get(url, headers=headers)
# print(response.content)


headers = {
    'Referer': 'https://comic.naver.com/webtoon/detail?titleId=710751&no=149&weekday=sun',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70'
}
url = "https://image-comic.pstatic.net/webtoon/710751/149/20210625144015_fbf205edf4fb45d59a46f452886af005_IMAG01_8.jpg"

res = requests.get(url, headers = headers)

with open("test.jpg", "wb") as f:
    f.write(res.content)

