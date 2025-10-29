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
from pdf_domestic_engine import get_data_hanwool


class LifeWater:
    def __init__(self, mydic):
        """Initialize the document generator with default paths."""
        self.base_dir = Path("d:/05_Send")
        self.hwp_template = "wt_domestic.hwp"
        self.template_source = Path("c:/Program Files/totalcmd/hwp") / self.hwp_template
        self.desktop = self.get_desktop_path()

        if mydic:
            self.ecoli = mydic['Total_Coliform']
            self.ph = mydic['pH']
            self.chloride = mydic['Chloride']
            self.nitrogen = mydic['Nitrate_Nitrogen']
            self.cadmium = mydic['Cadmium']
            self.arsenic = mydic['Arsenic']
            self.cyanide = mydic['Cyanide']
            self.mercury = mydic['Mercury']
            self.parathion = mydic['Parathion']
            self.diazinon = mydic['Diazinon']
            self.phenol = mydic['Phenol']
            self.lead = mydic['Lead']
            self.chromium = mydic['Chromium']
            self.trichloroethane = mydic['1,1,1-Trichloroethane']
            self.tetrachloroethylene = mydic['Tetrachloroethylene']
            self.trichloroethylene = mydic['Trichloroethylene']
            self.benzene = mydic['Benzene']
            self.toluene = mydic['Toluene']
            self.ethylbenzene = mydic['Ethylbenzene']
            self.xylene = mydic['Xylene']
            self.water_ok = mydic['water_ok']

    @staticmethod
    def get_desktop_path():
        """Get the path to the user's desktop."""
        return Path(os.environ['USERPROFILE']) / 'Desktop'

    def get_hwp_name(self):
        return self.desktop / self.hwp_template


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
    hwp.open(r"c:\Users\minhwasoo\Desktop\wt_domestic.hwp")

    index = extract_number(well)

    # 테이블리스트를 가져옴
    Table_list = [i for i in hwp.ctrl_list if i.UserDesc == "표"]
    print(Table_list)

    hwp_write_text(hwp, 'index', index)
    hwp_write_text(hwp, 'well', well)
    hwp_write_text(hwp, 'ecoli', lw_water.ecoli)
    hwp_write_text(hwp, 'ph', lw_water.ph)
    hwp_write_text(hwp, 'chloride', lw_water.chloride)
    hwp_write_text(hwp, 'nitrogen', lw_water.nitrogen)
    hwp_write_text(hwp, 'water_ok', lw_water.water_ok)

    hwp_write_text(hwp, 'cadmium', lw_water.cadmium)
    hwp_write_text(hwp, 'arsenic', lw_water.arsenic)
    hwp_write_text(hwp, 'cyanide', lw_water.cyanide)
    hwp_write_text(hwp, 'mercury', lw_water.mercury)

    hwp_write_text(hwp, 'parathion', lw_water.parathion)
    hwp_write_text(hwp, 'diazinon', lw_water.diazinon)
    hwp_write_text(hwp, 'phenol', lw_water.phenol)
    hwp_write_text(hwp, 'lead', lw_water.lead)
    hwp_write_text(hwp, 'chromium', lw_water.chromium)
    hwp_write_text(hwp, 'trichloroethane', lw_water.trichloroethane)
    hwp_write_text(hwp, 'tetrachloroethylene', lw_water.tetrachloroethylene)
    hwp_write_text(hwp, 'trichloroethylene', lw_water.trichloroethylene)
    hwp_write_text(hwp, 'benzene', lw_water.benzene)
    hwp_write_text(hwp, 'toluene', lw_water.toluene)
    hwp_write_text(hwp, 'ethylbenzene', lw_water.ethylbenzene)
    hwp_write_text(hwp, 'xylene', lw_water.xylene)

    hwp.save_as(f"d:\\05_Send\\ex_domestic_{well}.hwp")
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
        print(f"총대장균군: {lw_water.water_ok}")

        well = "W-" + str(i)
        hwp_part(well, lw_water)

    merge_hwp_files()


if __name__ == "__main__":
    main()
