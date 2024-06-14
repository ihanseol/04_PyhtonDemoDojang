#
# 코드는 동작함, 다만 새로운 인스턴스를 열어서 거기에다가 출력할뿐
#

import xlwings as xw
import win32gui
import win32process

def get_excel_window_info():
    # Find the Excel window
    hwnd = win32gui.FindWindow("XLMAIN", None)
    if hwnd == 0:
        return None, None

    # Get the process ID associated with the window
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    return hwnd, pid

def control_excel():
    hwnd, pid = get_excel_window_info()
    if hwnd is None or pid is None:
        print("엑셀이 실행되지 않았습니다.")
        return

    # 엑셀 앱 인스턴스 생성
    app = xw.App(visible=True)
    try:
        # 새 워크북 생성 또는 기존 워크북 열기
        wb = app.books.add()  # 새 워크북을 생성합니다.
        # wb = app.books.open('파일경로')  # 기존 파일을 열고 싶을 때 사용합니다.

        # 시트 선택 또는 추가
        sheet = wb.sheets['Sheet1']  # 기본 시트 선택
        # sheet = wb.sheets.add('새 시트')  # 새 시트를 추가하고 싶을 때 사용합니다.

        # 셀에 데이터 작성
        sheet.range('A1').value = 'Hello, Excel!'  # A1 셀에 문자열 쓰기
        sheet.range('A2').value = 12345  # A2 셀에 숫자 쓰기

        # 파일 저장
        wb.save('example.xlsx')
        print("파일을 저장했습니다.")
    except Exception as e:
        print(f"엑셀 제어 중 오류 발생: {e}")
    finally:
        # 엑셀 앱 종료
        app.quit()

# 함수 실행
control_excel()
