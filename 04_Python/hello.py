import xlwings as xw


def sayhello():
    wb = xw.Book.caller()
    wb.sheets[0].range('a1').value = 'hello world'


