#
# https://youtu.be/tBd97bErtTw
#
# pandas, 통계, 전처리, 데이터 분석
# xlwings, excel의 기능을 조작하는것
#

from pyhwpx import Hwp

hwp = Hwp()
import xlwings as xw

df = xw.load(index=False)
print(df)
# 이렇게 해주면, 현재 열려있는 엑셀쉬트를 데이터프레임으로 가져온다.

# hwp is open its ok ?
print(hwp.Path)
hwp.table_from_data(df)




xb = xw.books.active
ws = wb.sheets.active

# 연결이 되었나 확인
print(wb.name, ws.name)
print(ws["A3"].value)

cell_dict = {}
for cell in ws.used_range:
    # cell_dic[cell.address] = cell.value
    cell_dic[cell.get_address(row_absolute=False, column_absolute=False)] = cell.value

print(cell_dict)

hwp.get_into_nth_table()
# 생략하면 문서의 처음으로 간다.


def insert_cellvalue(addr, val):
    hwp.goto_addr(addr)
    if not hwp.get_selected_text():
        return hwp.insert_text(val)


for key in cell_dict:
    hwp.goto_addr(key)
    hwp.insert_text(cell_dict[key])

for key, val in cell_dict.items():
    insert_cellvalue(key, val)


def test01():
    # 한글에서 커서가 표안에 들어가 있기만 하면
    # 한글에 값을 넣는 과정
    hwp.get_into_nth_table(0)
    hwp.goto_addr("c4")
    hwp.insert_text(13)

