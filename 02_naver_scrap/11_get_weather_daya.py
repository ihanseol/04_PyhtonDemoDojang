from bs4 import BeautifulSoup
import requests
import datetime
from openpyxl import Workbook
import os


def get_bs_obj(url):
    result = requests.get(url)
    bs_obj = BeautifulSoup(result.content, "html.parser")
    return bs_obj


def get_weather(nYear, nArea):
    url = "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=" + str(nArea) + "&yy=" + str(nYear) + "&obs=21&x=22&y=12"
    bs_obj = get_bs_obj(url)

    no_today = bs_obj.find("table", {'class':'table_develop'})
    trs = no_today.find_all("tr")
    tds = trs[32].find_all("td")

    ret = [str(nYear)]
    for td in tds[1:]:
        ret.append(td.text)

    return ret


def main_engine():
    username = os.getlogin()
    write_wb = Workbook()
    now = datetime.datetime.now()
    nyear = now.year - 30

    write_ws = write_wb.active
    data = []
    for i in range(nyear, nyear+30):
        itm = get_weather(i, 133)
        data.append(itm)
        write_ws.append(itm)
        print(itm)

    write_wb.save(f"C:\\Users\\{username}\\Desktop\\weather.xlsx")
    return data


main_engine()






















