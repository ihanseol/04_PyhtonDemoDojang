from win32com.client import Dispatch
import os
import shutil
import win32com.client as win32
import openpyxl

import os


def goto_page(hwp, page):
    hwp.HAction.GetDefault("Goto", hwp.HParameterSet.HGotoE.HSet)
    hwp.HParameterSet.HGotoE.HSet.SetItem("DialogResult", page)
    hwp.HParameterSet.HGotoE.SetSelectionIndex = 1
    hwp.HAction.Execute("Goto", hwp.HParameterSet.HGotoE.HSet)

    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveNextWord")
    hwp.HAction.Run("MoveNextWord")
    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run("MoveNextWord")
    hwp.HAction.Run("MoveRight")


def paste_value(hwp):
    # hwp.HAction.GetDefault("Paste", hwp.HParameterSet.HSelectionOpt.HSet)
    # hwp.HParameterSet.HSelectionOpt.Option = 5
    # hwp.HAction.Execute("Paste", hwp.HParameterSet.HSelectionOpt.HSet)
    hwp.Run('Paste')


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def get_hwp(filename):
    hwp = win32.gencache.EnsureDispatch('HWPFrame.HwpObject')
    hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')
    hwp = win32.gencache.EnsureDispatch('HWPFrame.HwpObject')
    hwp.XHwpWindows.Item(0).Visible = True
    hwp.RegisterModule('FilePathCheckDLL', 'FilePathCheckerModule')
    hwp.Open(filename)
    return hwp


def get_excel(str_filename):
    xl = Dispatch("Excel.Application")
    wb = xl.Workbooks.Open(str_filename)
    xl.Visible = True
    return wb


# 1 : -- 2, 19 (i = 1+1, 1+18)
# 2 : -- 20, 39
# ws.Range("b2:n19").Copy()  # copy works on all range objects (ws.Columns(), ws.Cells, etc)

def get_excel_data(wb, page):
    ws = wb.Worksheets(1)
    i = (page-1)*18 + 2
    j = i + 18
    range = f"b{i}:n{j}"
    ws.Range(range).Copy()
    return


def get_last_row(str_filename):
    wb = openpyxl.load_workbook(str_filename)
    sheet = wb.active
    nb_row = sheet.max_row
    wb.close()
    print(nb_row)
    return nb_row


def paste_work(c1, str_filename):
    desktop = get_desktop()
    wb = get_excel(f"{desktop}\\data.xlsx")
    hwp = get_hwp(f"{desktop}\\data-soil.hwp")

    for i in range(c1+1):
        get_excel_data(wb, i+1)
        goto_page(hwp, i+1)
        paste_value(hwp)

    hwp.Save()
    hwp.Quit()
    wb.Close()


def main():
    if __name__ == '__main__':
        desktop = get_desktop()
        last_row = get_last_row(f"{desktop}\\data.xlsx") - 1

        cnt = last_row/3
        (c1, c2) = divmod(cnt, 6)
        d1 = int(c1)

        paste_work(d1, f"{desktop}\\data.xlsx")

        # ws = read_excel(f"{desktop}\\data.xlsx")
        # write_data(ws, f"{desktop}\\data-soil.hwp")


main()



