import re
import os
import shutil
import time
import datetime
from pyhwpx import Hwp
from pathlib import Path


def empty_example():
    hwp.get_page_text(3).replace("\r\n", "").replace(" ", "")


def delete_table(hwp, page_index):
    hwp.goto_page(page_index)
    hwp.Delete()


def is_image(hwp, page_index):
    hwp.goto_page(page_index)
    hwp.MoveRight()
    hwp.goto_addr("A2")
    hwp.SelectCtrlFront()
    if hwp.CurSelectedCtrl.UserDesc == "그림":
        hwp.Cancel()
        return True
    else:
        hwp.Cancel()
        return False


def remove_empty_page(hwp):
    hwp.MoveDocBegin()
    for i in range(hwp.PageCount, 0, -1):
        if hwp.is_empty_page(i):
            hwp.goto_page(i)
            hwp.DeletePage()


def main():
    hwp = Hwp(visible=True)
    hwp.open(r"d:\05_Send\01_AqtSolveReport.hwp")
    page_count = hwp.PageCount

    # 테이블리스트를 가져옴
    Table_list = [i for i in hwp.ctrl_list if i.UserDesc == "표"]
    print("Table_list", len(Table_list))
    print("Page_Count", page_count)

    ret = is_image(hwp, 32)
    print(ret)

    for i in range(page_count, 0, -1):
        print(i)
        if not is_image(hwp, i):
            delete_table(hwp, i)

    remove_empty_page(hwp)
    hwp.Quit(save=True)


if __name__ == __main__():
    main()
