import datetime
import os
import pandas as pd
from selenium import webdriver

def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop

# https://stackoverflow.com/questions/42370977/how-to-save-a-new-sheet-in-an-existing-excel-file-using-pandas


def write_to_pdfile(weather_data, narea):
    list_year10 = weather_data[20:30]

    path = get_desktop() + f"\\pandas_to_excel_{str(narea)}.xlsx"
    writer = pd.ExcelWriter(path, engine='xlsxwriter')

    df1 = pd.DataFrame(weather_data)
    df1.to_excel(writer, sheet_name=str(narea))

    df2 = pd.DataFrame(list_year10)
    df2.to_excel(writer, sheet_name='10year')

    writer.save()
    writer.close()


def get_weatherdata(driver, nyear, narea):
    url = "https://www.weather.go.kr/weather/climate/past_table.jsp?stn="+str(narea)+"&yy=" + str(nyear)+"&obs=21&x=22&y=12"
    driver.get(url)
    weather_data = [str(nyear)]

    for i in range(2, 14):
        search_string = f"/html/body/div/div[3]/div[2]/div[2]/table/tbody/tr[32]/td[{i}]"
        elem = driver.find_element_by_xpath(search_string)
        weather_data.append(elem.text)

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
    driver = webdriver.Chrome(r"C:\Program Files\SeleniumBasic\chromedriver.exe", options=chrome_options)

    for i in range(j, j+30):
        weather_data = get_weatherdata(driver, i, narea)
        year30_data.append(weather_data)
        print(weather_data)

    driver.close()
    write_to_pdfile(year30_data, narea)


def main():
    if __name__ == '__main__':
        get_30year(131)


main()






