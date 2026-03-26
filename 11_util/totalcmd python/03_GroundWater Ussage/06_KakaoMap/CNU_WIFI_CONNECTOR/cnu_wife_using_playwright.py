import asyncio
from playwright.async_api import async_playwright
import datetime

async def main():
    async with async_playwright() as p:
        # 브라우저 실행 (headless=False로 설정해야 눈으로 확인 가능합니다)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = await context.new_page()

        print("Chrome 시작, https://cic.cnu.ac.kr/cic/service/guestlogin.do")
        await page.goto('https://cic.cnu.ac.kr/cic/service/guestlogin.do')

        try:
            # Selenium의 WebDriverWait 역할: Selector가 나타날 때까지 대기
            await page.wait_for_selector("#privacy", timeout=10000)
            print("페이지 로딩 완료. '#privacy' 요소를 찾았습니다.")
        except Exception as e:
            print(f"페이지 로딩 중 오류 발생 또는 요소 탐색 실패: {e}")
            await browser.close()
            return

        # -------------------------------------------
        # 입력 및 클릭 동작
        # -------------------------------------------
        
        print('page.click("#privacy")')
        await page.click("#privacy")
        await asyncio.sleep(1)

        print('page.fill("#strName", "민화수")')
        await page.fill("#strName", "민화수")
        await asyncio.sleep(1)

        print('page.fill("#ph", "010-3411-9213")')
        await page.fill("#ph", "010-3411-9213")
        await asyncio.sleep(1)

        print('page.fill("#strId", "cnumin")')
        await page.fill("#strId", "cnumin")
        await asyncio.sleep(1)

        print('page.fill("#strPw", "1234")')
        await page.fill("#strPw", "1234")
        await asyncio.sleep(1)

        print('page.fill("#strPwConfirm", "1234")')
        await page.fill("#strPwConfirm", "1234")
        await asyncio.sleep(1)

        print('page.click("#requestpw")')
        await page.click("#requestpw")

        # 결과 확인을 위한 대기
        await asyncio.sleep(5)
        
        # 브라우저 종료
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())