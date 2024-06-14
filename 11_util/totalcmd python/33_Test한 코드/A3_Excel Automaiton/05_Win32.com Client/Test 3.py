#
# 이코드는 동작함, 하지만 어떤경우에는 동작하지 않고 있다. 그이유는 알수가 없어
#

import xlwings as xw


def control_existing_excel():
    try:
        # 이미 실행 중인 Excel 애플리케이션에 연결
        app = xw.apps.active
    except Exception as e:
        print("실행 중인 엑셀 인스턴스를 찾을 수 없습니다.")
        return

    # 현재 활성화된 워크북 선택
    wb = app.books.active

    # 워크시트 선택
    sheet = wb.sheets.active  # 현재 활성화된 시트 선택

    # 셀에 데이터 작성
    sheet.range('A1').value = 'Hello, Existing Excel!'  # A1 셀에 문자열 쓰기
    sheet.range('A2').value = 54321  # A2 셀에 숫자 쓰기

    # 변경사항이 있을 경우, 파일 저장
    # wb.save('저장할_파일_경로.xlsx')  # 필요에 따라 주석 해제 및 경로 수정

    print("기존 엑셀 인스턴스에 데이터를 성공적으로 작성했습니다.")


# 함수 실행
control_existing_excel()
