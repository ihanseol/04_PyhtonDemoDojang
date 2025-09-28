from pyhwpx import Hwp
from pathlib import Path
from FileManger_V0_20250406 import FileBase

HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell\\"
SEND = "d:\\05_Send\\"


def main():
    fb = FileBase()

    fb.copy_file(HWP_BASE + "EmptyPage.hwpx", SEND)
    hwp = Hwp(visible=False)

    hwp.open(f"d:\\05_Send\\EmptyPage.hwpx")

    jpg_files = fb.get_file_filter(SEND, "*.jpg")
    for i, file_name in enumerate(jpg_files):
        hwp.goto_page(i+1)
        print(i, file_name)
        hwp.insert_picture(SEND + file_name)

    hwp.save_as("01_SaveFile.hwpx")
    hwp.quit()
    fb.delete_file(Path(SEND + "EmptyPage.hwpx"))


if __name__ == "__main__":
    main()
