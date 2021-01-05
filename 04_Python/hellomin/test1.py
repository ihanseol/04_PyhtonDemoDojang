

import xlwings as xw

wb = xw.Book()
wsData = wb.sheets[0]

wsData.name = 'data'

ws2 = wb.sheets['min']

wsData.cells.clear_contents()

wsData.range('a1').value = [[100,200], [33,43]]

ws2.cells(1,1).value = 'hello'
