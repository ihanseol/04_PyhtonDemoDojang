import datetime
import os
import pandas as pd
from selenium import webdriver

#
# <option value="108" >서울(유)</option>
# <option value="102" >백령도(유)</option>
# <option value="98" >동두천(무)</option>
# <option value="99" >파주(무)</option>
#
# <option value="">--------</option>
# <option value="112" >인천(유)</option>
# <option value="119" >수원(유)</option>
# <option value="201" >강화(무)</option>
# <option value="202" >양평(무)</option>
# <option value="203" >이천(무)</option>
# <option value="">--------</option>
#
# <option value="93" >북춘천(유)</option>
# <option value="95" >철원(무)</option>
# <option value="101" >춘천(무)</option>
# <option value="114" >원주(무)</option>
# <option value="121" >영월(무)</option>
# <option value="211" >인제(무)</option>
# <option value="212" >홍천(무)</option>
#
# <option value="">--------</option>
# <option value="104" >북강릉(유)</option>
# <option value="115" >울릉도(유)</option>
# <option value="105" >강릉(무)</option>
# <option value="90" >속초(무)</option>
# <option value="100" >대관령(무)</option>
# <option value="106" >동해(무)</option>
# <option value="216" >태백(무)</option>
#
# <!--2011.12.01 추가 시작-->
# <option value="217" >정선군(무)</option>
# <!--2011.12.01 추가 끝-->
# <option value="">--------</option>
# <option value="131" >청주(유)</option>
# <option value="127" >충주(무)</option>
# <option value="135" >추풍령(무)</option>
# <option value="221" >제천(무)</option>
# <option value="226" >보은(무)</option>
#
# <option value="">--------</option>
# <option value="177" >홍성(유)</option>
# <option value="133" >대전(유)</option>
# <option value="129" >서산(무)</option>
# <option value="232" >천안(무)</option>
# <option value="235" selected="selected">보령(무)</option>
# <option value="236" >부여(무)</option>
# <option value="238" >금산(무)</option>
#
# <option value="">--------</option>
# <option value="146" >전주(유)</option>
# <option value="140" >군산(무)</option>
# <option value="243" >부안(무)</option>
# <option value="244" >임실(무)</option>
# <option value="245" >정읍(무)</option>
# <option value="247" >남원(무)</option>
# <option value="248" >장수(무)</option>
# <option value="254" >순창(무)</option>
# <option value="172" >고창(무)</option>
# <option value="251" >고창(구)</option>
#
# <option value="">--------</option>
# <option value="156" >광주(유)</option>
# <option value="165" >목포(유)</option>
# <option value="169" >흑산도(유)</option>
# <option value="168" >여수(유)</option>
# <option value="170" >완도(무)</option>
# <option value="175" >진도(첨찰산)(무)</option>
#
# <!--2014.09.15 진도군(공)추가 -->
# <option value="268" >진도군(무)</option>
# <option value="252" >영광(무)</option>
# <option value="174" >순천(무)</option>
# <option value="256" >순천(구)</option>
# <option value="260" >장흥(무)</option>
# <option value="261" >해남(무)</option>
# <option value="262" >고흥(무)</option>
# <!--2011.12.01 추가 시작-->
# <option value="259" >강진군(무)</option>
# <option value="258" >보성군(무)</option>
# <option value="266" >광양(무)</option>
#
# <!--2011.12.01 추가 끝-->
# <option value="">--------</option>
# <option value="136" >안동(유)</option>
# <option value="138" >포항(유)</option>
# <option value="143" >대구(유)</option>
# <option value="176" >대구(구)</option>
# <option value="130" >울진(무)</option>
# <option value="137" >상주(무)</option>
# <option value="271" >봉화(무)</option>
# <option value="272" >영주(무)</option>
# <option value="273" >문경(무)</option>
# <option value="277" >영덕(무)</option>
# <option value="278" >의성(무)</option>
# <option value="279" >구미(무)</option>
# <option value="281" >영천(무)</option>
#
# <!--2011.12.01 추가 시작-->
# <option value="276" >청송군(무)</option>
# <option value="283" >경주(무)</option>
# <!--2011.12.01 추가 끝-->
#
# <option value="">--------</option>
# <option value="159" >부산(유)</option>
# <option value="152" >울산(유)</option>
# <option value="155" >창원(유)</option>
# <!--2011.12.01 추가 시작-->
# <option value="255" >북창원(무)</option>
# <!--2011.12.01 추가 끝-->
# <option value="162" >통영(무)</option>
# <option value="192" >진주(무)</option>
# <option value="284" >거창(무)</option>
# <option value="285" >합천(무)</option>
# <option value="288" >밀양(무)</option>
# <option value="289" >산청(무)</option>
# <option value="294" >거제(무)</option>
# <option value="295" >남해(무)</option>
# <option value="253" >김해시(무)</option>
# <!--2011.12.01 추가 시작-->
# <option value="257" >양산(무)</option>
# <option value="263" >의령군(무)</option>
# <option value="264" >함양군(무)</option>
# <!--2011.12.01 추가 끝-->
#
# <option value="">--------</option>
# <option value="184" >제주(유)</option>
# <option value="185" >고산(무)</option>
# <option value="189" >서귀포(무)</option>
# <option value="188" >성산(무)</option>


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def write_to_pdfile(weather_data):
    file_name = get_desktop() + "\\pandas_to_excel.xlsx"
    df = pd.DataFrame(weather_data)
    df.to_excel(file_name, sheet_name='new_sheet_name')


def get_weatherdata(driver, nyear, narea):
    url = "https://www.weather.go.kr/weather/climate/past_table.jsp?stn="  + str(narea)  +  "&yy=" + str(nyear) +  "&obs=21&x=22&y=12"
    driver.get(url)
    weather_data = []
    weather_data.append(str(nyear))

    for i in range(2, 14):
        search_string = f"/html/body/div/div[3]/div[2]/div[2]/table/tbody/tr[32]/td[{i}]"
        elem = driver.find_element_by_xpath(search_string)
        weather_data.append(elem.text)

    return weather_data


def get_10year(narea):
    now = datetime.datetime.now()
    year10_data = []
    nyear = now.year - 1
    j = nyear - 9  # 2020-9 = 2011

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('window-size=1920x1080')
    chrome_options.add_argument("disable-gpu")
    driver = webdriver.Chrome(r"C:\Program Files\SeleniumBasic\chromedriver.exe", options=chrome_options)

    driver.implicitly_wait(3)

    for i in range(j, j+10):
        weather_data = get_weatherdata(driver, i, narea)
        year10_data.append(weather_data)
        print(weather_data)

    driver.close()
    write_to_pdfile(year10_data)


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
    write_to_pdfile(year30_data)


def main():
    if __name__ == '__main__':
        get_30year(131)


main()






