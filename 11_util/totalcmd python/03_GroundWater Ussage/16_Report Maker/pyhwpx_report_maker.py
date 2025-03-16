import os
from pyhwpx import Hwp
from FileProcessing_V4_20250211 import FileBase
import time
import pyautogui


class WellType:
    def __init__(self, _directory='D:\\05_Send\\'):
        self.DANGYE_INCLUDE = False
        self.REPORT_YES = True
        self.N_WELL = 1
        self.Directory = _directory
        self.determin_well_type()

    def determin_well_type(self):
        fb = FileBase(self.Directory)
        import re

        jpg_files = fb.get_jpg_filter(".", "a1-*.jpg")
        prt_files = fb.get_file_filter(".", "p*.jpg")

        if len(jpg_files) == 4:
            self.DANGYE_INCLUDE = True
        else:
            self.DANGYE_INCLUDE = False

        if len(prt_files):
            self.REPORT_YES = True
        else:
            self.REPORT_YES = False

        jpg_files = fb.get_jpg_filter(".", "a*.jpg")
        last_string = ''.join(jpg_files[-1:])
        match = re.search(r"(\d+)-", last_string)  # Find digits followed by a hyphen
        extracted_number = 1
        if match:
            extracted_number = match.group(1)  # Group 1 captures the digits
            print(extracted_number)  # Output: 11
        else:
            print("Number not found in the expected format.")

        self.N_WELL = int(extracted_number)

    def print(self):
        if self.DANGYE_INCLUDE:
            print("-- 단계포함, include dangye --")
        else:
            print("-- 단계제외, exclude dangye --")

        print(f"Number of Well : {self.N_WELL}")


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def goto_page(hwp, n):
    hwp.goto_page(n)
    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run("MoveDown")


def get_last_page(hwp):
    hwp.MovePos(3)
    return hwp.current_page


def load_image_from_send(hwp, fname):
    print(fname)
    hwp.insert_picture(os.path.join(r"d:\05_Send", fname), treat_as_char=True, embedded=True, sizeoption=0)


def print_report(hwp, well_no, wt):
    fb = FileBase()
    a_insert = [1, 5, 9, 13]  # 단계포함하는, 지열공같은 관정개발
    b_insert = [1, 5, 9]  # 단계제외한
    c_insert = [1, 2, 3, 4]
    d_insert = [1, 2, 3]

    insert_final = []

    if wt.DANGYE_INCLUDE:
        if wt.REPORT_YES:
            insert_final = a_insert
        else:
            insert_final = c_insert
    else:
        if wt.REPORT_YES:
            insert_final = b_insert
        else:
            insert_final = d_insert

    print(os.getcwd())
    jpg_files = fb.get_jpg_filter("d:\\05_Send", f"a{well_no}-*.jpg")
    print("jpg_files", jpg_files)

    for i, a_page in enumerate(insert_final):
        print(f"page: {a_page} , i : {i}")
        goto_page(hwp, a_page)
        load_image_from_send(hwp, jpg_files[i])

        pjpg_files = fb.get_jpg_filter(".", f"p{well_no}-{i + 1}*.jpg")

        for k in range(len(pjpg_files)):
            goto_page(hwp, a_page + k + 1)
            load_image_from_send(hwp, pjpg_files[k])
    hwp.Save()
    hwp.close()


def prepare_empty_paper(wt):
    fb = FileBase()
    source_file = ""
    for i in range(1, wt.N_WELL + 1):
        if wt.DANGYE_INCLUDE:
            if wt.REPORT_YES:
                source_file = fb.join_path_tofilename(
                    r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\A1_AQTESOLV_STEP",
                    f"w{i}_AQTESOLV.hwpx")
            else:
                source_file = fb.join_path_tofilename(
                    r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\A1_AQTESOLV_STEP",
                    f"00_w{i}_AQTESOLV.hwpx")
        else:
            if wt.REPORT_YES:
                source_file = fb.join_path_tofilename(
                    r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\A2_AQTESOLV_LONG",
                    f"w{i}_AQTESOLV_Long.hwpx")
            else:
                source_file = fb.join_path_tofilename(
                    r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\A2_AQTESOLV_LONG",
                    f"00_w{i}_AQTESOLV_Long.hwpx")

        fb.copy_file(source_file, "d:\\05_Send")


def main():
    wt = WellType()
    wt.print()
    fb = FileBase()

    prepare_empty_paper(wt)

    hwp = Hwp(visible=False)

    for i in range(1, wt.N_WELL + 1):
        if wt.DANGYE_INCLUDE:
            if wt.REPORT_YES:
                hwp.open(f"d:\\05_Send\\w{i}_AQTESOLV.hwpx")
            else:
                hwp.open(f"d:\\05_Send\\00_w{i}_AQTESOLV.hwpx")
        else:
            if wt.REPORT_YES:
                hwp.open(f"d:\\05_Send\\w{i}_AQTESOLV_Long.hwpx")
            else:
                hwp.open(f"d:\\05_Send\\00_w{i}_AQTESOLV_Long.hwpx")

        print(f"w{i}_AQTESOLV.hwpx")
        print_report(hwp, i, wt)
        hwp.close()
    hwp.quit()


if __name__ == "__main__":
    main()
