import pandas as pd

# 엑셀 파일 읽기
dataframe = pd.read_excel(r'c:\Users\minhwasoo\Downloads\info.xls')

# CSV 파일로 변환
dataframe.to_csv('info.csv', index=False, encoding='utf-8-sig')


