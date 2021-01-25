

import shutil
import win32com.client as win32
import pandas as pd
import os
import get_field as gf


def writing_data(df, page, filename):
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")

    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
    hwp.XHwpWindows.Item(0).Visible = True

    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
    hwp.Open(filename)

    field_list = [i for i in hwp.GetFieldList(1, 0x02).split("\x02")]
    return_field = gf.get_index_num(field_list)

    for field, n in return_field.items():
        data: object = df[field].iloc[page]
        if type(data) == str:
            write_data = data
        else:
            write_data = " "

        for i in range(n):
            str_field = f'{field}{{{{{i}}}}}'
            hwp.MoveToField(str_field)
            hwp.PutFieldText(str_field, data)

    hwp.Save()
    hwp.Quit()


def getDesktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def read_excel(str_filename):
    filename = getDesktop() + f'\\{str_filename}'
    df = pd.read_excel(filename)
    return df


def copy_hwp_document(desktop, filename):
    shutil.copyfile(f'{desktop}\\data.hwp', f'{desktop}\\{filename}')


def main():
    if __name__ == '__main__':
        df = read_excel('data.xlsx')
        length = len(df)
        desktop = getDesktop()
        for i in range(length):
            copy_hwp_document(desktop, f'data{i}.hwp')
        for i in range(length):
            writing_data(df, i, f'{desktop}\\data{i}.hwp')

main()

