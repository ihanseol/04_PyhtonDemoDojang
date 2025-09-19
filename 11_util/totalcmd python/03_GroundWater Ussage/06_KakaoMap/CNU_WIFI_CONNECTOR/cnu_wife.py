from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager

import time
import datetime


def download_30year_data(driver, df, AreaSelection):
    myCode = df[df['Area'] == AreaSelection]['Code'].values[0]
    mySwitch = df[df['Area'] == AreaSelection]['switch'].values[0]

    one_string = f"ztree_{mySwitch}_switch"
    two_string = f"{AreaSelection} ({myCode})"

    print(f"one_string : {one_string}")
    print(f"two_string : {two_string}")

    # -------------------------------------------
    URL = 'https://data.kma.go.kr/stcs/grnd/grndRnList.do?pgmNo=69'
    driver.get(URL)
    driver.implicitly_wait(20)

    ddl = driver.find_element(By.CSS_SELECTOR, "#dataFormCd")
    select = Select(ddl)
    select.select_by_visible_text("월")
    time.sleep(1)

    # 지역선택
    driver.find_element(By.ID, "btnStn").click()
    time.sleep(1)

    driver.find_element(By.CSS_SELECTOR, f"#{one_string}").click()
    time.sleep(1)

    driver.find_element(By.LINK_TEXT, two_string).click()
    time.sleep(1)

    driver.find_element(By.LINK_TEXT, "선택완료").click()
    time.sleep(1)

    # -------------------------------------------
    eYear = datetime.now().year - 1
    sYear = eYear - 29
    # -------------------------------------------
    # 년 월 버튼 , 클릭
    # -------------------------------------------

    ddl = driver.find_element(By.CSS_SELECTOR, "#startYear")
    select = Select(ddl)
    select.select_by_visible_text(str(sYear))
    time.sleep(0.5)

    ddl = driver.find_element(By.CSS_SELECTOR, "#endYear")
    select = Select(ddl)
    select.select_by_visible_text(str(eYear))
    time.sleep(0.5)

    # -------------------------------------------
    # 검색버튼 클릭
    # -------------------------------------------

    driver.find_element(By.CSS_SELECTOR, "button.SEARCH_BTN").click()
    time.sleep(2)

    driver.find_element(By.CSS_SELECTOR, "a.DOWNLOAD_BTN").click()
    time.sleep(3)

    return True


def example():
    """
        Set loginIdElement = driver.FindElementByCss("#loginId")
        loginIdElement.SendKeys "hanseol33@naver.com"
        Sleep (1 * 1000)
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        import time

        # 웹 드라이버 초기화 (예: Chrome)
        driver = webdriver.Chrome()

        # 'loginId'를 CSS 셀렉터로 찾기
        login_id_element = driver.find_element(By.CSS_SELECTOR, "#loginId")

        # 찾은 요소에 키 입력
        login_id_element.send_keys("hanseol33@naver.com")

        # 1초 대기
        time.sleep(1)
    """


def main():
    customService = Service(ChromeDriverManager().install())
    customOption = Options()
    customOption.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=customService, options=customOption)

    print("chrome start, https://cic.cnu.ac.kr/cic/service/guestlogin.do")
    URL = 'https://cic.cnu.ac.kr/cic/service/guestlogin.do'
    driver.get(URL)

    # 페이지 로딩이 완료될 때까지 명시적으로 기다림
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#privacy"))
        )
        print("페이지 로딩 완료. '#privacy' 요소를 찾았습니다.")
    except Exception as e:
        print(f"페이지 로딩 중 오류 발생 또는 요소 탐색 실패: {e}")
        driver.quit()
        return

    print('driver.find_element(By.CSS_SELECTOR, "#privacy").click()')
    driver.find_element(By.CSS_SELECTOR, "#privacy").click()

    # 1초 대기
    time.sleep(1)

    print('elementName = driver.find_element(By.CSS_SELECTOR, "#strName"')
    elementName = driver.find_element(By.CSS_SELECTOR, "#strName")
    elementName.send_keys("민화수")

    # 1초 대기
    time.sleep(1)

    print('elementPhone = driver.find_element(By.CSS_SELECTOR, "#ph")')
    elementPhone = driver.find_element(By.CSS_SELECTOR, "#ph")
    elementPhone.send_keys("010-3411-9213")

    # 1초 대기
    time.sleep(1)

    print('elementAccount = driver.find_element(By.CSS_SELECTOR, "#strId")')
    elementAccount = driver.find_element(By.CSS_SELECTOR, "#strId")
    elementAccount.send_keys("cnumin")

    # 1초 대기
    time.sleep(1)

    print('elementPassword = driver.find_element(By.CSS_SELECTOR, "#strPw")')
    elementPassword = driver.find_element(By.CSS_SELECTOR, "#strPw")
    elementPassword.send_keys("1234")

    # 1초 대기
    time.sleep(1)

    print('elementPasswordConfirm = driver.find_element(By.CSS_SELECTOR, "#strPwConfirm")')
    elementPasswordConfirm = driver.find_element(By.CSS_SELECTOR, "#strPwConfirm")
    elementPasswordConfirm.send_keys("1234")

    # 2초 대기 후 종료
    time.sleep(2)
    driver.quit()


if __name__ == "__main__":
    main()
