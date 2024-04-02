#
# 결국, 돌아돌아서 엑셀의 인스턴스를 찾을수가 없었던것은 결국 권한 문제였다.
# 파이참의 권한을 관리자 권한으로 올리거나
# 아니면, 엑셀을 일반 유저 권한에서 실행하면 된다.
#



import win32com.client

def control_existing_excel_pywin32():
    try:
        # 이미 실행 중인 Excel 애플리케이션에 연결
        excel = win32com.client.GetActiveObject("Excel.Application")
    except Exception as e:
        print("실행 중인 엑셀 인스턴스를 찾을 수 없습니다.")
        return

    # 현재 활성화된 워크북 선택
    wb = excel.ActiveWorkbook

    # 현재 활성화된 시트 선택
    sheet = wb.ActiveSheet

    # 셀에 데이터 쓰기
    sheet.Cells(1, 1).Value = "Hello, Existing Excel!"
    sheet.Cells(2, 1).Value = 54321

    print("기존 엑셀 인스턴스에 데이터를 성공적으로 작성했습니다.")

# 함수 실행
control_existing_excel_pywin32()
