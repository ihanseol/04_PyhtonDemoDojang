import os
import shutil
import pandas as pd
from hwpapi.core import App

XL_INPUT = "iyong_template.xlsx"
XL_BASE = "d:\\05_Send"
HWP_INPUT = "iyong(field).hwp"
HWP_OUTPUT = "iyong(result).hwp"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def initial_work():
    desktop = get_desktop()

    try:
        excel = pd.read_excel(f"{XL_BASE}\\{XL_INPUT}")
    except FileNotFoundError:
        return "Error: XLSX file must located your d:/05_Send/ folder."

    app = App(None, False)
    return app, excel


def initial_opencopy(app, excel):
    desktop = get_desktop()

    try:
        shutil.copyfile(f"{desktop}\\{HWP_INPUT}", f"{desktop}\\{HWP_OUTPUT}")
        app.open(f"{desktop}\\{HWP_OUTPUT}")
    except FileNotFoundError:
        return "Error: 'iyong(field).hwp' file must locate your desktop folder."

    hwp = app.api

    field_list = [i for i in hwp.GetFieldList().split("\x02")]
    print(len(field_list), field_list)

    hwp.Run('SelectAll')
    hwp.Run('Copy')
    hwp.MovePos(3)

    print('------------------------------------------------------')
    print('page copy started ...')
    print(len(excel))

    for i in range(len(excel) - 1):
        hwp.Run('Paste')
        hwp.MovePos(3)

    print(f'{len(excel)} page copy completed ...')
    print('------------------------------------------------------')
    return field_list


"""
def copy_work(app, excel, field_list):
    hwp = app.api
    for page in range(len(excel)):
        for field in field_list:
            data = excel[field].iloc[page]
            # if type(data) == str:
            if pd.isna(data):
                write_data = " "
            else:
                write_data = data

            hwp.MoveToField(f'{field}{{{{{page}}}}}')
            hwp.PutFieldText(f'{field}{{{{{page}}}}}', write_data)

        print(f'{page + 1}:{excel.address[page]}')

"""


def copy_work(app, excel, field_list):
    hwp = app.api

    for page, address in enumerate(excel.address):
        for field in field_list:
            data = excel[field].iloc[page]
            write_data = " " if pd.isna(data) else data

            field_tag = f'{field}{{{{{page}}}}}'
            hwp.MoveToField(field_tag)
            hwp.PutFieldText(field_tag, write_data)

        print(f'{page + 1}:{address}')


def end_work(app, excel):
    app.api.Save()
    app.quit()


def save_s(hwp):
    pset = hwp.HParameterSet.HSaveAsImage
    hwp.HAction.GetDefault("PictureSaveAsAll", pset.HSet)
    hwp.HAction.Execute("PictureSaveAsAll", pset.HSet)

    hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)  # 다른이름으로 저장 액션 생성
    hwp.HParameterSet.HFileOpenSave.filename = "C:\\Users\\minhwasoo\\Desktop\\iyong_empty_complete.hwp"
    # 원래파일명#페이지.hwp로 저장
    hwp.HParameterSet.HFileOpenSave.Format = "HWP"  # 포맷은 Native HWP
    hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)  # 다른이름저장 실행


def main():
    app, excel = initial_work()
    field_list = initial_opencopy(app, excel)
    copy_work(app, excel, field_list)
    end_work(app, excel)
    print('------------------------------------------------------')


if __name__ == "__main__":
    main()
