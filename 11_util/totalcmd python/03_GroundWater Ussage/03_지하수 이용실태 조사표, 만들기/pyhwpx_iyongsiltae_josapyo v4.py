from pyhwpx import Hwp
import os
import pandas as pd

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

    hwp = Hwp(visible=False)
    return hwp, excel


def initial_opencopy(hwp, excel):
    desktop = get_desktop()

    if not hwp.open(f"{desktop}\\{HWP_INPUT}"):
        print("Error: 'iyong(field).hwp' file must locate your desktop folder.")
        return False

    field_list = [i for i in hwp.get_field_list(0,0x02).split("\x02")]
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
    hwp, excel = initial_work()
    field_list = initial_opencopy(hwp, excel)
    copy_work(hwp, excel, field_list)
    hwp.delete_all_fields()
    end_work(hwp, excel)
    print('------------------------------------------------------')


if __name__ == "__main__":
    main()
