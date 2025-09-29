import pandas as pd
from datetime import datetime, timedelta
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import numbers

def pandas_to_excel_date(pandas_timestamp):
    excel_epoch = datetime(1899, 12, 30)
    delta = pandas_timestamp - excel_epoch
    return delta.days + delta.seconds / 86400

# 샘플 데이터프레임 생성
df = pd.DataFrame({'date': [pd.Timestamp('2023-06-30'), pd.Timestamp('2023-07-01')]})
df['excel_date'] = df['date'].apply(pandas_to_excel_date)

# Excel 워크북 생성
wb = Workbook()
ws = wb.active

# 데이터프레임을 Excel 워크시트에 추가
for r in dataframe_to_rows(df, index=False, header=True):
    ws.append(r)

# 'excel_date' 열의 모든 셀에 날짜 형식 적용
for cell in ws['B'][1:]:  # B열이 'excel_date' 열이라고 가정
    cell.number_format = numbers.FORMAT_DATE_DATETIME

# Excel 파일 저장
wb.save("output.xlsx")