import pygetwindow as gw

# Excel 창의 타이틀 가져오기
excel_windows = gw.getWindowsWithTitle('Excel')
all_title = gw.getAllTitles()

for window in excel_windows:
    print("Excel 창 타이틀:", window.title)






