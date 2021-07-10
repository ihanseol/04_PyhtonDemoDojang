import datetime
import os
import sys
import pandas as pd
from selenium import webdriver

def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop

# https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas


def write_to_pd_file(weather_data, area):
    list_year10 = weather_data[20:30]

    path = get_desktop() + f"\\pandas_to_excel_{str(area)}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    df1 = pd.DataFrame(weather_data)
    df1.to_excel(writer, sheet_name=str(area))

    df2 = pd.DataFrame(list_year10)
    df2.to_excel(writer, sheet_name='10year')

    writer.save()
    writer.close()


def get_weatherdata(driver, year, area):
    url = "https://www.weather.go.kr/weather/climate/past_table.jsp?stn=" + str(area) + "&yy=" + str(year) + "&obs=21&x=22&y=12"
    driver.get(url)
    weather_data = [year]

    for i in range(2, 14):
        search_string = f"/html/body/div/div[3]/div[2]/div[2]/table/tbody/tr[32]/td[{i}]"
        elem = driver.find_element_by_xpath(search_string)
        weather_data.append(float(elem.text))

    return weather_data


def get_30year(narea):
    now = datetime.datetime.now()
    year30_data = []
    nyear = now.year - 1
    j = nyear - 29  # 2020-29 = 1991

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--allow-insecure-localhost')
    driver = webdriver.Chrome(r"C:\Program Files\SeleniumBasic\chromedriver.exe", options=chrome_options)

    for i in range(j, j+30):
        weather_data = get_weatherdata(driver, i, narea)
        year30_data.append(weather_data)
        print(weather_data)

    driver.close()
    write_to_pd_file(year30_data, narea)


def main():
    if __name__ == '__main__':
        n = len(sys.argv)
        if n < 2:
            area = 133
        else:
            area = int(sys.argv[1])

        get_30year(area)


main()






