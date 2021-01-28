from win32com.client import Dispatch
import win32com.client as win32
import openpyxl
import os


def goto_page(hwp: object, page: object) -> object:
    """
    hwp object
    :type page: number
    :type hwp: object
    """
    hwp.HAction.GetDefault("Goto", hwp.HParameterSet.HGotoE.HSet)
    hwp.HParameterSet.HGotoE.HSet.SetItem("DialogResult", page)
    hwp.HParameterSet.HGotoE.SetSelectionIndex = 1
    hwp.HAction.Execute("Goto", hwp.HParameterSet.HGotoE.HSet)

    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveDown")


# function OnScriptMacro_사이즈2()
# {
# 	HAction.GetDefault("Paste", HParameterSet.HSelectionOpt.HSet);
# 	with (HParameterSet.HSelectionOpt)
# 	{
# 		Option = 5;
# 	}
# 	HAction.Execute("Paste", HParameterSet.HSelectionOpt.HSet);
# }

def paste_value(hwp: object):
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
    i = (page-1)*15 + 2
    j = i + 14
    srange = f"b{i}:n{j}"
    ws.Range(srange).Copy()
    return


def get_last_row(str_filename):
    wb = openpyxl.load_workbook(str_filename)
    sheet = wb.active
    nb_row = sheet.max_row
    wb.close()
    print(nb_row)
    return nb_row


def paste_work(page):
    desktop = get_desktop()
    wb = get_excel(f"{desktop}\\data.xlsx")
    hwp = get_hwp(f"{desktop}\\data-rock.hwp")

    for i in range(1, page + 1):
        get_excel_data(wb, i)
        goto_page(hwp, i)
        paste_value(hwp)

    hwp.Save()
    hwp.Quit()
    wb.Close()


def main():
    if __name__ == '__main__':
        desktop = get_desktop()
        last_row = get_last_row(f"{desktop}\\data.xlsx") - 1
        c1 = last_row // 15

        print(f"c1 : {c1} ")
        paste_work(c1)

main()



