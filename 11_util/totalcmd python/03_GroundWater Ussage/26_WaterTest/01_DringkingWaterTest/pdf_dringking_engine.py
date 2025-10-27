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

NOF_INSPECTION = int(46)

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
            "일반세균": "General_bacteria",
            "총대장균군": "Total_coliforms",
            "분원성대장균": "Fecal_coliforms",
            "납": "Lead",
            "불소": "Fluoride",
            "비소": "Arsenic",
            "세레늄": "Selenium",
            "수은": "Mercury",
            "시안": "Cyanide",
            "크롬": "Chromium",
            "염소이온": "Chloride_ion",
            "암모니아성질소": "Ammonia_nitrogen",
            "질산성질소": "Nitrate_nitrogen",
            "카드뮴": "Cadmium",
            "붕소": "Boron",
            "페놀": "Phenol",
            "다이아지논": "Diazinon",
            "파라티온": "Parathion",
            "페니트로티온": "Fenitrothion",
            "카바릴": "Carbaryl",
            "1,1,1-트리클로로에탄": "1,1,1-Trichloroethane",
            "테트라클로로에틸렌": "Tetrachloroethylene",
            "트리클로로에틸렌": "Trichloroethylene",
            "디클로로메탄": "Dichloromethane",
            "벤젠": "Benzene",
            "톨루엔": "Toluene",
            "에틸벤젠": "Ethylbenzene",
            "크실렌": "Xylene",
            "1,1-디클로로에틸렌": "1,1-Dichloroethylene",
            "사염화탄소": "Carbon_tetrachloride",
            "1,2-디브로모-3-클로로프로판": "1,2-Dibromo-3-chloropropane",
            "1,4-다이옥산": "1,4-Dioxane",
            "경도": "Hardness",
            "과망간산칼륨소비량": "Potassium_permanganate_consumption",
            "냄새": "Odor",
            "맛": "Taste",
            "동": "Copper",
            "색도": "Color",
            "세제": "Detergents",
            "수소이온농도": "pH",
            "아연": "Zinc",
            "철": "Iron",
            "망간": "Manganese",
            "탁도": "Turbidity",
            "황산이온": "Sulfate_ion",
            "알루미늄": "Aluminum"
        }

    data = {}
    i = start_idx

    line_title = []
    line_result = []

    for j in range(1, NOF_INSPECTION + 1):
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


def get_data_malgeunmul(pdf_name, page):
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

    if lines[10] == '적합':
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
        '총대장균군': 'Total_Coliform',
        '수소이온농도': 'pH',
        '질산성질소': 'Nitrate_Nitrogen',
        '염소이온': 'Chloride',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '크롬': 'Chromium',
        '수은': 'Mercury',
        '납': 'Lead',
        '페놀': 'Phenol',
        '시안': 'Cyanide',
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '트리클로로에틸렌': 'Trichloroethylene',
        '벤젠': 'Benzene',
        '톨루엔': 'Toluene',
        '에틸벤젠': 'Ethylbenzene',
        '크실렌': 'Xylene'
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


# 누리생명과학연구원
# 이것은 스캔한걸 OCR로 바꿔서 보니, 엉망이라 지금은 미정이다.

def get_data_nurilife(pdf_name, page):
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


    for i in range(1,10):
        if '종합결과' in lines[-i]:
            if '부적합' in lines[-i] :
                water_ok = '부적합'
            else:
                water_ok = '적합'
            break

    # Find start of results table (look for key items or NO patterns)
    start_idx = None
    for i, line in enumerate(lines):
        if line == '검사항목':
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
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion',
        '페놀': 'Phenol',
        '납': 'Lead',
        '크롬': 'Chromium',
        '트리클로로에틸렌': 'Trichloroethylene',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
        '벤젠': 'Benzene',
        '톨루엔': 'Toluene',
        '에틸벤젠': 'Ethylbenzene',
        '크실렌': 'Xylene'
    }
    # 'key' : 'item'

    data = {}
    i = start_idx + 4

    line_result = []
    line_title = ['수소이온농도', '총대장균군', '질산성질소', '염소이온', '카드뮴', '비소', '시안', '수은', '다이아지논', '파라티온', '페놀', '납', '크롬',
                  '트리클로로에틸렌', '테트라클로로에틸렌', '1,1,1-트리클로로에탄', '벤젠', '톨루엔', '에틸벤젠', '크실렌']
    for j in range(1, 21):
        line_result.append(lines[i + 2])
        i += 3

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

    result = get_data_hanwool(pdf_name, 1)
    # result = get_data_malgeunmul(pdf_name, 1)
    # result = get_data_kiwii(pdf_name, 1)
    # result = get_data_nurilife(pdf_name, 1)

    print(result)


if __name__ == "__main__":
    main()
