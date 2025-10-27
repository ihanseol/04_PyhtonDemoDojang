import pymupdf
import re
from pyhwpx import Hwp
from pathlib import Path
import os
import shutil
from merge_hwp_files import merge_hwp_files
from FileManger_V0_20250406 import FileBase


def get_qc_yongdo(pdf_name, page):
    #wqtr : water quality test report
    #wqc : water quality certificate
    #qc : quality certificate

    doc = pymupdf.open(pdf_name)
    water_ok = ''

    if page > len(doc):
        doc.close()
        return {}

    page_obj = doc.load_page(page - 1)
    text = page_obj.get_text("text")  # Or "blocks" for better table handling if needed
    doc.close()

    lines = [line.strip() for line in text.split('\n') if line.strip()]
    print(lines)

    for line in lines:
        if "음용수" in line:
            print(line, "found 음용수")
            return "음용수"

        if "전용상수도" in line:
            print(line, "found 음용수")
            return "음용수"
        
        if "먹는물" in line:
            print(line, "found 음용수")
            return "음용수"


        if "생활용수" in line:
            print(line, "found 생활용수")
            return "생활용수"

        if "농업용수" in line:
            print(line, "found 농업용수")
            return "농업용수"

        if "공업용수" in line:
            print(line, "found 공업용수")
            return "공업용수"

    return None


def main():
    fb = FileBase()
    file_list = fb.get_file_filter(".", "*.pdf")
    pdf_name = file_list[0]

    result = get_yongdo_hanwool(pdf_name, 1)
    print(result)


if __name__ == "__main__":
    main()
