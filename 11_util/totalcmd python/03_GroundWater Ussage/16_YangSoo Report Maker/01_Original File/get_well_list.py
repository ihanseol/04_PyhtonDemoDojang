import os
from FileProcessing_V4_20250211 import FileBase
import time
import re


def get_welllist(r_type):
    fb = FileBase()
    jpg_files = fb.get_file_filter(".", "*-1_page1*.jpg")

    print("number of jpgfiles :", len(jpg_files))
    print(jpg_files)
    print("-" * 50)

    return_well_list = []
    for well in jpg_files:
        print(well)
        if r_type:
            return_well_list.append(well.split("-1")[0])
        else:
            match = re.search(r"(\d+)", well)
            return_well_list.append(int(match.group(1)))


    return return_well_list




def main():

    well = get_welllist(True)

    print("-"*50)
    print(well[0])


if __name__ == "__main__":
    main()
