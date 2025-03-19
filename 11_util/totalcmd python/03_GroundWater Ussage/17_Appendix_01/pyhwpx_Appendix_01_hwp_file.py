import os
import time
import pandas as pd
from pyhwpx import Hwp
from make_appendix import AppendixMaker
import shutil

XL_INPUT = "appendix_01.xlsx"
XL_BASE = "d:\\05_Send"
HWP_INPUT = "appendix_01(field).hwpx"
HWP_OUTPUT = "appendix_01(result).hwpx"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def countdown(n):
    print(' Please Move the Command Window to Side ! ')
    while n > 0:
        print(n)
        time.sleep(1)
        n -= 1
    print("Time's up!")


def initial_work():
    desktop = get_desktop()

    try:
        excel = pd.read_excel(f"{XL_BASE}\\{XL_INPUT}")
    except FileNotFoundError:
        return "Error: XLSX file must located your d:/05_Send/ folder."

    hwp = Hwp(visible=False)
    return hwp, excel


def initial_opencopy(hwp, excel):
    desktop = get_desktop()

    if not hwp.open(f"{desktop}\\{HWP_INPUT}"):
        print("Error: 'iyong(field).hwp' file must locate your desktop folder.")
        return False

    field_list = [i for i in hwp.get_field_list(0, 0x02).split("\x02")]
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


def copy_work(hwp, excel, field_list):
    for page, address in enumerate(excel.address):
        for field in field_list:
            data = excel[field].iloc[page]
            write_data = " " if pd.isna(data) else data

            field_tag = f'{field}{{{{{page}}}}}'
            hwp.MoveToField(field_tag)
            hwp.PutFieldText(field_tag, write_data)

        print(f'{page + 1}:{address}')


def end_work(hwp, excel):
    hwp.save_as(f"d:/05_Send/{HWP_OUTPUT}")
    hwp.quit()


def main():
    desktop = get_desktop()

    # 시작할때, 한글에 집어넣기 위한 엑셀데이타파일을 만들어준다.
    appendix_maker = AppendixMaker()
    appendix_maker.run()
    countdown(1)

    shutil.copy(r"c:\Program Files\totalcmd\ini\02_python\appendix_01(field).hwpx", desktop)

    # 필드에 값을 넣어 완성본을 만드는 과정
    hwp, excel = initial_work()
    field_list = initial_opencopy(hwp, excel)
    copy_work(hwp, excel, field_list)
    end_work(hwp, excel)
    print('------------------------------------------------------')

    os.remove(desktop + f"\\{HWP_INPUT}")


if __name__ == "__main__":
    main()
