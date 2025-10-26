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


def get_data_hanwool(pdf_name, page):
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

    if lines[-6] == '적합':
        water_ok = '적합'
    else:
        water_ok = '부적합'

    # Find start of results table (look for key items or NO patterns)
    start_idx = None
    for i, line in enumerate(lines):
        if line == '1':
            start_idx = i - 1
            break

    if start_idx is None:
        return {}

    # Korean to English mapping for your specified 20 items (only matches present ones)
    # 'key' : 'item'
    key_map = {
        '총대장균군': 'Total_Coliform',
        '수소이온농도': 'pH',
        '염소이온': 'Chloride',
        '질산성질소': 'Nitrate_Nitrogen',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '시안': 'Cyanide',
        '수은': 'Mercury',
        '파라티온': 'Parathion',
        '다이아지논': 'Diazinon',
        '페놀': 'Phenol',
        '납': 'Lead',
        '크롬': 'Chromium',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '트리클로로에틸렌': 'Trichloroethylene',
        '벤젠': 'Benzene',
        '톨루엔': 'Toluene',
        '에틸벤젠': 'Ethylbenzene',
        '크실렌': 'Xylene'
    }

    data = {}
    i = start_idx

    line_title = []
    line_result = []

    for j in range(1, 21):
        line_title.append(lines[i + 2])
        line_result.append(lines[i + 3])
        i += 4

    # print(line_title)
    # print(line_result)

    for i, item in enumerate(key_map):
        data[key_map[item]] = line_result[i]
        print(item, data[key_map[item]])

    data['water_ok'] = water_ok

    print('=' * 100)
    print(data)

    return data



def get_data_kiwii(pdf_name, page):
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

    if lines[-3] == '적합':
        water_ok = '적합'
    else:
        water_ok = '부적합'

    # Find start of results table (look for key items or NO patterns)
    start_idx = None
    for i, line in enumerate(lines):
        if line == '1':
            start_idx = i - 1
            break

    if start_idx is None:
        return {}

    # Korean to English mapping for your specified 20 items (only matches present ones)
    key_map = {
        '수소이온농도': 'pH',
        '총대장균군': 'Total_Coliform',
        '질산성질소': 'Nitrate_Nitrogen',
        '염소이온': 'Chloride',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '시안': 'Cyanide',
        '수은': 'Mercury',
        '페놀': 'Phenol',
        '납': 'Lead',
        '트리클로로에틸렌': 'Trichloroethylene',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
        '벤젠': 'Benzene',
        '톨루엔': 'Toluene',
        '에틸벤젠': 'Ethylbenzene',
        '크실렌': 'Xylene',
        '크롬': 'Chromium',
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion'
    }
    # 'key' : 'item'

    data = {}
    i = start_idx

    line_title = []
    line_result = []

    for j in range(1, 21):
        line_title.append(lines[i + 2])
        line_result.append(lines[i + 4])
        i += 4

    # print(line_title)
    # print(line_result)

    for i, item in enumerate(key_map):
        data[key_map[item]] = line_result[i]
        print(item, data[key_map[item]])

    data['water_ok'] = water_ok

    print('=' * 100)
    print(data)

    return data


def main():
    fb = FileBase()
    file_list = fb.get_file_filter(".", "*.pdf")
    pdf_name = file_list[0]

    result = get_data_kiwii(pdf_name, 1)
    print(result)


if __name__ == "__main__":
    main()
