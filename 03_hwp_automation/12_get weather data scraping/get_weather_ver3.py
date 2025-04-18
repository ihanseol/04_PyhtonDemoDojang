import os
import sys
import datetime
from bs4 import BeautifulSoup
from lxml import etree
import requests
import pandas as pd

headers = {
    'Referer': 'https://www.weather.go.kr/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.70'
}


def get_desktop():

    if os.name == 'posix':
        desktop = os.path.expanduser('~/Desktop/')
    else:
        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def write_to_pd_file(weather_data, area):
    # write 30year data and 10year data by separate sheet

    list_year10 = weather_data[20:30]

    path = get_desktop() + f"\\pandas_to_excel_{str(area)}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    df1 = pd.DataFrame(weather_data)
    df1.to_excel(writer, sheet_name=str(area))

    df2 = pd.DataFrame(list_year10)
    df2.to_excel(writer, sheet_name='10year')

    writer.save()


def write_file(weather_data, area):
    path = get_desktop() + f"\\pandas_to_excel_{str(area)}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    df1 = pd.DataFrame(weather_data)
    df1.to_excel(writer, sheet_name=str(area))

    writer.save()


def get_weather_data(year, area):
    url = "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=" + str(area) + "&yy=" + str(year) + "&obs=21&x=22&y=12"

    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    tds = soup.findAll('table', {'class': 'table_develop'})[0].find_all('tr')[32].find_all('td')

    weather_data = [year]

    for td in tds[1:]:
        weather_data.append(float(td.text))

    return weather_data


def get_30year(area):
    now = datetime.datetime.now()
    year30_data = []
    year = now.year - 1
    j = year - 29  # 2020-29 = 1991

    for i in range(j, j + 30):
        weather_data = get_weather_data(i, area)
        year30_data.append(weather_data)
        print(weather_data)

    write_to_pd_file(year30_data, area)


def get_n_year(how_many_years, area):
    now = datetime.datetime.now()
    year30_data = []
    year = now.year - 1
    j = year - (how_many_years - 1)  # 2020-29 = 1991
    # 2020 - 3 - 1 = 2018

    for i in range(j, j + how_many_years):
        weather_data = get_weather_data(i, area)
        year30_data.append(weather_data)
        print(weather_data)

    write_file(year30_data, area)


def main():
    # get_weather 10 133
    # get_weather 30 133

    if __name__ == '__main__':
        n = len(sys.argv)
        if n != 3:
            get_n_year(3, 133)
        else:
            if int(sys.argv[1]) != 30:
                area = int(sys.argv[2])
                how_many = int(sys.argv[1])
                get_n_year(how_many, area)
            else:
                area = int(sys.argv[2])
                get_30year(area)


main()
