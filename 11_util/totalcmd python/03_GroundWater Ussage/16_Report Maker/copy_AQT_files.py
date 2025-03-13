

from pyhwpx import Hwp
from FileProcessing_V4_20250211 import FileBase
import pyautogui
import os
import time



class WellType:
    def __init__(self, _directory='D:\\05_Send\\'):
        self.DANGYE_INCLUDE = False
        self.N_WELL = 1
        self.Directory = _directory
        self.determin_well_type()

    def determin_well_type(self):
        fb = FileBase(self.Directory)
        jpg_files = fb.get_jpg_filter(".", "a1*.jpg")
        if len(jpg_files) == 4:
            self.DANGYE_INCLUDE = True
        else:
            self.DANGYE_INCLUDE = False

        jpg_files = fb.get_jpg_filter(".", "a*.jpg")
        last = ''.join(jpg_files[-1:])
        self.N_WELL = int(last[1])

    def print(self):
        if self.DANGYE_INCLUDE:
            print("-- 단계포함, include dangye --")
        else:
            print("-- 단계제외, exclude dangye --")

        print(f"Number of Well : {self.N_WELL}")


def main():
    fb = FileBase()
    wt = WellType()

    for i in range(1, wt.N_WELL+1):
        source = fb.join_path_tofilename("d:\\09_hardRain\\10_ihanseol - 2025\\00_data\\04_Reference Data\\12_보고서, 부록\\A1_AQTESOLV_STEP", f"w{i}_AQTESOLV.hwpx")
        fb.copy_file(source,"d:\\05_Send")



if __name__ == "__main__":
    main()




