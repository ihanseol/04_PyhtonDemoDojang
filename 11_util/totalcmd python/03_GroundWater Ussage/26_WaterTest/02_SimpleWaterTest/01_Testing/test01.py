import pandas as pd
import openpyxl



def main_job():
    # 엑셀 파일 경로 지정
    excel_file = 'ex_water_test.xlsx'  # 실제 파일 경로로 변경하세요

    # 엑셀 파일 로드
    wb = openpyxl.load_workbook(excel_file)

    # 모든 시트 이름 가져오기
    sheet_names = wb.sheetnames
    print(f"발견된 시트: {sheet_names}\n")
    print("=" * 80)

    # 각 시트별로 처리
    for sheet_name in sheet_names:
        print(f"\n{'=' * 80}")
        print(f"시트 이름: {sheet_name}")
        print(f"{'=' * 80}\n")

        # B12:F26 범위 읽기 (skiprows=11은 1~11행 건너뛰기, usecols는 B~F열)
        df = pd.read_excel(
            excel_file,
            sheet_name=sheet_name,
            usecols='B:F',  # B~F 열만 읽기
            skiprows=11,  # 1~11행 건너뛰기 (12행부터 읽기)
            nrows=15  # 15행만 읽기 (12~26행)
        )

        # 데이터프레임 출력
        print(df)
        print(f"\n데이터프레임 크기: {df.shape}")
        print(f"컬럼: {list(df.columns)}")
        print("\n" + "-" * 80 + "\n")

    # 워크북 닫기
    wb.close()

    print("\n모든 시트 처리 완료!")

def TableFindSample():
    # Table 찾아가기
    # https://www.inflearn.com/community/questions/1453780/%ED%91%9C-%EC%B0%BE%EC%95%84%EA%B0%80%EA%B8%B0-%EB%8F%84%EC%99%80%EC%A3%BC%EC%84%B8%EC%9A%94-%E3%85%A0%E3%85%A0

    Table_list = [i for i in hwp.ctrl_list if i.UserDesc == "표"]
    print(Table_list)

    hwp.select_ctrl(Table_list[0])
    hwp.ShapeObjTableSelCell()
    hwp.goto_addr("C2")
    hwp.insert_text(f"{well}")

    # =========================================================================

    hwp.get_into_nth_table(0)
    hwp.goto_addr("C2")
    hwp.insert_text(f"{well}")

    # =========================================================================

    Table_list = [i for i in hwp.ctrl_list if i.UserDesc == "표"]
    Table_index = 0

    hwp.move_to_ctrl(Table_list[Table_index])
    hwp.find_ctrl()
    hwp.ShapeObjTableSelCell()  # A1 셀을 선택한 상태가 됨
    hwp.goto_addr("C2")
    hwp.SelectAll()
    hwp.Delete()
    hwp.insert_text(f"{well}")
    # =========================================================================
    hwp.ShapeObjTableSelCell()
    hwp.TableCellBlock()
    hwp.TableCellBlockExtend()
    hwp.TableCellBlockExtend()


if __name__ == "__main__":
    main_job()



