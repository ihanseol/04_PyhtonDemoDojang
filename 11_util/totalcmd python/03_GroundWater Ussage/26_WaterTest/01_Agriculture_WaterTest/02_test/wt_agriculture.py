import pymupdf
import re
from pyhwpx import Hwp
from pathlib import Path
import os
import shutil
import time
import datetime
from merge_hwp_files import merge_hwp_files
from FileManger_V0_20250406 import FileBase
from pdf_agriculture_engine import get_data_hanwool


class LifeWater:
    def __init__(self, mydic):
        """Initialize the document generator with default paths."""
        self.base_dir = Path("d:/05_Send")
        self.hwp_template = "wt_agriculture.hwp"
        self.template_source = Path("c:/Program Files/totalcmd/hwp") / self.hwp_template
        self.desktop = self.get_desktop_path()

        if mydic:
            self.ph = mydic['pH']
            self.chloride = mydic['Chloride']
            self.nitrogen = mydic['Nitrate_Nitrogen']
            self.cadmium = mydic['Cadmium']
            self.arsenic = mydic['Arsenic']
            self.cyanide = mydic['Cyanide']
            self.mercury = mydic['Mercury']
            self.diazinon = mydic['Diazinon']
            self.parathion = mydic['Parathion']
            self.phenol = mydic['Phenol']
            self.lead = mydic['Lead']
            self.chromium = mydic['Chromium']
            self.trichloroethane = mydic['1,1,1-Trichloroethane']
            self.trichloroethylene = mydic['Trichloroethylene']
            self.tetrachloroethylene = mydic['Tetrachloroethylene']
            self.water_ok = mydic['water_ok']


    @staticmethod
    def get_desktop_path():
        """Get the path to the user's desktop."""
        return Path(os.environ['USERPROFILE']) / 'Desktop'

    def get_hwp_name(self):
        return self.desktop / self.hwp_template

    def get_hwp_template(self):
        return self.template_source


def extract_number(given_string: str) -> int | None:
    """
    Extracts the first continuous sequence of digits from a given string
    and returns it as an integer.

    Args:
        given_string: The string to search (e.g., 'w-20', 'item_34b').

    Returns:
        The extracted number as an integer, or None if no digits are found.
    """
    # Regular expression to find one or more consecutive digits (\d+).
    # re.search scans through the string looking for any location where
    # the pattern produces a match.
    match = re.search(r'\d+', given_string)

    if match:
        # match.group(0) returns the matching substring (e.g., "20")
        # We convert it to an integer before returning.
        return int(match.group(0))

    # Return None if no numeric sequence was found in the string.
    return None


def hwp_write_text(hwp, place_holder, data):
    hwp.MoveToField(f"{place_holder}")
    hwp.PutFieldText(f"{place_holder}", f"{data}")


def hwp_part(well, lw_water):
    hwp = Hwp(visible=False)

    file_path = lw_water.get_hwp_template()
    hwp.open(str(file_path))
    index = extract_number(well)

    # 테이블리스트를 가져옴
    table_list = [i for i in hwp.ctrl_list if i.UserDesc == "표"]
    print(table_list)

    hwp_write_text(hwp, 'index', index)
    hwp_write_text(hwp, 'water_ok', lw_water.water_ok)

    hwp_write_text(hwp, 'well', well)
    hwp_write_text(hwp, 'ph', lw_water.ph)
    hwp_write_text(hwp, 'chloride', lw_water.chloride)
    hwp_write_text(hwp, 'nitrogen', lw_water.nitrogen)

    hwp_write_text(hwp, 'cadmium', lw_water.cadmium)
    hwp_write_text(hwp, 'arsenic', lw_water.arsenic)
    hwp_write_text(hwp, 'cyanide', lw_water.cyanide)
    hwp_write_text(hwp, 'mercury', lw_water.mercury)
    hwp_write_text(hwp, 'diazinon', lw_water.diazinon)

    hwp_write_text(hwp, 'parathion', lw_water.parathion)
    hwp_write_text(hwp, 'phenol', lw_water.phenol)
    hwp_write_text(hwp, 'lead', lw_water.lead)
    hwp_write_text(hwp, 'chromium', lw_water.chromium)

    hwp_write_text(hwp, 'trichloroethane', lw_water.trichloroethane)
    hwp_write_text(hwp, 'trichloroethylene', lw_water.trichloroethylene)
    hwp_write_text(hwp, 'tetrachloroethylene', lw_water.tetrachloroethylene)


    hwp.save_as(f"d:\\05_Send\\ex_agriculture_{well}.hwp")
    hwp.Quit(save=False)


def main():
    fb = FileBase()
    file_list = fb.get_file_filter(".", "*.pdf")

    # pdf_name = r"d:\05_Send\수질성적서_대구시경찰청.pdf"
    pdf_name = file_list[0]

    doc = pymupdf.open(pdf_name)
    len_doc = len(doc)
    doc.close()

    for i in range(1, len_doc + 1):
        result = get_data_hanwool(pdf_name, i)

        lw_water = LifeWater(result)
        print('=' * 100)
        print(f"ph: {lw_water.ph}")

        well = "W-" + str(i)
        hwp_part(well, lw_water)

    merge_hwp_files()


if __name__ == "__main__":
    main()
