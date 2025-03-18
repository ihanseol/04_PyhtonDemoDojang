import os
from pyhwpx import Hwp
from FileProcessing_V4_20250211 import FileBase
import time
import re


class WellType:
    def __init__(self, _directory='D:\\05_Send\\'):
        self.DANGYE_INCLUDE = False
        self.REPORT_YES = True
        self.N_WELL = 1
        self.Directory = _directory
        self.determin_well_type()

    def determin_well_type(self):
        fb = FileBase(self.Directory)
        jpg_files = fb.get_file_filter(".", "w1-*.jpg")

        if len(jpg_files) == 6:
            self.DANGYE_INCLUDE = True
        else:
            self.DANGYE_INCLUDE = False

        jpg_files = fb.get_jpg_filter(".", "w*.jpg")
        last_string = ''.join(jpg_files[-1:])

        match = re.search(r"(\d+)-", last_string)  # Find digits followed by a hyphen
        extracted_number = 1
        if match:
            extracted_number = match.group(1)  # Group 1 captures the digits
            print(extracted_number)  # Output: 11
        else:
            match = re.search(r"(\d+)", last_string)  # Find digits followed by a hyphen
            extracted_number = match.group(1)
            print("Number not found in the expected format.")

        self.N_WELL = int(extracted_number)

    def print(self):
        if self.DANGYE_INCLUDE:
            print("-- 단계포함, include dangye --")
        else:
            print("-- 단계제외, exclude dangye --")

        print(f"Number of Well : {self.N_WELL}")


def goto_page(hwp, n):
    hwp.goto_page(n)
    if n == 1:
        hwp.HAction.Run("MoveRight")
        hwp.HAction.Run("MoveDown")
    else:
        hwp.HAction.Run("MoveRight")


def get_last_page(hwp):
    hwp.MovePos(3)
    return hwp.current_page


def load_image_from_send(hwp, fname):
    print(fname)
    hwp.insert_picture(os.path.join(r"d:\05_Send", fname), treat_as_char=True, embedded=True, sizeoption=0)


def print_report(hwp, well_no, wt):
    fb = FileBase()
    insert_final = []

    print(os.getcwd())
    if wt.DANGYE_INCLUDE:
        # 단계포함
        jpg_files = fb.get_jpg_filter("d:\\05_Send", f"w{well_no}-*.jpg")
    else:
        # 단계제외, 장기양수시험일보만
        jpg_files = fb.get_jpg_filter("d:\\05_Send", f"w{well_no}_*.jpg")

    print("jpg_files", jpg_files)

    for i in range(1, len(jpg_files) + 1):
        goto_page(hwp, i)
        load_image_from_send(hwp, jpg_files[i - 1])
    hwp.Save()
    hwp.close()


def prepare_empty_paper(wt):
    fb = FileBase()
    source_file = ""
    for i in range(1, wt.N_WELL + 1):
        if wt.DANGYE_INCLUDE:
            source_file = fb.join_path_tofilename(
                r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\A3_YangSoo_Report",
                f"A{i}_YangSoo_Step.hwpx")

        else:
            source_file = fb.join_path_tofilename(
                r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\A3_YangSoo_Report",
                f"B{i}_YangSoo_Long.hwpx")

        fb.copy_file(source_file, "d:\\05_Send")


def main():
    wt = WellType()
    wt.print()
    fb = FileBase()

    prepare_empty_paper(wt)

    hwp = Hwp(visible=False)

    for i in range(1, wt.N_WELL + 1):
        if wt.DANGYE_INCLUDE:
            hwp.open(f"d:\\05_Send\\A{i}_YangSoo_Step.hwpx")
        else:
            hwp.open(f"d:\\05_Send\\B{i}_YangSoo_Long.hwpx")

        print(f"w{i} Report ...")
        print_report(hwp, i, wt)
        hwp.close()
    hwp.quit()


if __name__ == "__main__":
    main()
