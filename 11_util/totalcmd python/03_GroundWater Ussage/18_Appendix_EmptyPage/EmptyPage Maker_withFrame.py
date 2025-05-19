from pyhwpx import Hwp
from pathlib import Path
from FileManger_V0_20250406 import FileBase

HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell\\"
SEND = "d:\\05_Send\\"


def _goto_page(hwp, page_num):
    """Navigate to specific page in HWP document."""
    hwp.goto_page(page_num)
    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run("MoveDown")

def pagesetup(hwp):
    my_page = {'위쪽': 20, '머리말': 10, '왼쪽': 20, '오른쪽': 20, '제본여백': 0, '꼬리말': 10, '아래쪽': 13, '제본타입': 0, '용지방향': 0,
               '용지길이': 297, '용지폭': 210}

    hwp.set_pagedef(my_page, "cur")
    print(my_page)


def main():
    fb = FileBase()

    fb.copy_file(HWP_BASE + "EmptyPage_Frame.hwpx", SEND)
    hwp = Hwp(visible=False)

    hwp.open(f"d:\\05_Send\\EmptyPage_Frame.hwpx")

    jpg_files = fb.get_file_filter(SEND, "*.jpg")
    for i, file_name in enumerate(jpg_files):
        _goto_page(hwp, i + 1)
        print(i, file_name)
        hwp.insert_picture(SEND + file_name)

    pagesetup(hwp)

    hwp.save_as("01_SaveFile.hwpx")
    hwp.quit()
    fb.delete_file(Path(SEND + "EmptyPage_Frame.hwpx"))


if __name__ == "__main__":
    main()
