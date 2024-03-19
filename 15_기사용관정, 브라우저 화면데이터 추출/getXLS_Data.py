import xlrd

# XLS 파일 경로
xls_file = r'c:\Users\minhwasoo\Downloads\info.xls'

# 원하는 셀 위치
cell_positions = ['B7', 'D7', 'D9', 'B9', 'B10']

# XLS 파일 열기
workbook = xlrd.open_workbook(xls_file)

# 첫 번째 시트 선택
sheet = workbook.sheet_by_index(0)

# 셀 값 가져오기
cell_values = []
for position in cell_positions:
    cell_value = sheet.cell_value(*xlrd.cellname_to_rowcol(position))
    cell_values.append(cell_value)

# 결과 출력
for position, value in zip(cell_positions, cell_values):
    print(f'{position} 셀 값: {value}')

