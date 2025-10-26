import win32com.client
import os


def analyze_water_quality(file_path):
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  # Excel 창을 보이지 않게 설정

    try:
        # 워크북 열기
        workbook = excel.Workbooks.Open(file_path)
        sheet = workbook.ActiveSheet

        # Well 정보 읽기
        well = sheet.Range("D12").Value
        print(f"분석 대상: {well}")
        print("=" * 50)

        # 데이터 리스트 초기화
        times = []
        temps = []
        ecs = []
        phs = []

        # 데이터 읽기 (14행부터 23행까지)
        for row in range(14, 24):
            time_val = sheet.Range(f"B{row}").Value
            temp_val = sheet.Range(f"D{row}").Value
            ec_val = sheet.Range(f"E{row}").Value
            ph_val = sheet.Range(f"F{row}").Value

            # None이 아닌 경우에만 리스트에 추가
            if time_val is not None:
                times.append(time_val)
            if temp_val is not None:
                temps.append(temp_val)
            if ec_val is not None:
                ecs.append(ec_val)
            if ph_val is not None:
                phs.append(ph_val)

        # 최대/최소값 계산 및 출력
        if temps:
            temp_max = round(max(temps), 1)
            temp_min = round(min(temps), 1)
            print(f"온도(°C)")
            print(f"  최대값: {temp_max}")
            print(f"  최소값: {temp_min}")
            print()

        if ecs:
            ec_max = int(round(max(ecs)))
            ec_min = int(round(min(ecs)))
            print(f"EC(μS/cm)")
            print(f"  최대값: {ec_max}")
            print(f"  최소값: {ec_min}")
            print()

        if phs:
            ph_max = round(max(phs), 2)
            ph_min = round(min(phs), 2)
            print(f"pH")
            print(f"  최대값: {ph_max}")
            print(f"  최소값: {ph_min}")
            print()

        # 결과를 딕셔너리로 반환
        results = {
            'well': well,
            'temp_max': temp_max if temps else None,
            'temp_min': temp_min if temps else None,
            'ec_max': ec_max if ecs else None,
            'ec_min': ec_min if ecs else None,
            'ph_max': ph_max if phs else None,
            'ph_min': ph_min if phs else None
        }

        return results

    except Exception as e:
        print(f"오류 발생: {e}")
        return None

    finally:
        # 워크북 닫기 (저장하지 않음)
        workbook.Close(SaveChanges=False)
        # Excel 애플리케이션 종료
        excel.Quit()


if __name__ == "__main__":
    # Excel 파일 경로 설정 (본인의 파일 경로로 수정하세요)
    file_path = r"d:\05_Send\pythonProject\03_GroundWater Ussage\26_WaterTest\02_SimpleWaterTest\ex_water_test.xlsx"

    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        print("파일 경로를 확인해주세요.")
    else:
        # 분석 실행
        results = analyze_water_quality(file_path)

        if results:
            print("=" * 50)
            print("분석 완료!")
