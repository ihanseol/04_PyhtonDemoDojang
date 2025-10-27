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


def get_qc_yongdo(pdf_name, page):
    # wqtr : water quality test report
    # wqc : water quality certificate
    # qc : quality certificate

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
    key_map = {
        '수소이온농도': 'pH',
        '염소이온': 'Chloride',
        '질산성질소': 'Nitrate_Nitrogen',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '시안': 'Cyanide',
        '수은': 'Mercury',
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion',
        '페놀': 'Phenol',
        '납': 'Lead',
        '크롬': 'Chromium',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
        '트리클로로에틸렌': 'Trichloroethylene',
        '테트라클로로에틸렌': 'Tetrachloroethylene'
    }
    # 'key' : 'item'

    data = {}
    i = start_idx

    line_title = []
    line_result = []

    for j in range(1, 16):
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
        '질산성질소': 'Nitrate_Nitrogen',
        '염소이온': 'Chloride',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '시안': 'Cyanide',
        '수은': 'Mercury',
        '페놀': 'Phenol',
        '납': 'Lead',
        '크롬': 'Chromium',

        '트리클로로에틸렌': 'Trichloroethylene',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane',
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion'
    }
    # 'key' : 'item'

    data = {}
    i = start_idx

    line_title = []
    line_result = []

    for j in range(1, 16):
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
    key_map = {
        '수소이온농도': 'pH',
        '질산성질소': 'Nitrate_Nitrogen',
        '염소이온': 'Chloride',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '수은': 'Mercury',
        '납': 'Lead',
        '크롬': 'Chromium',
        '페놀': 'Phenol',
        '시안': 'Cyanide',
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion',
        '트리클로로에틸렌': 'Trichloroethylene',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane'
    }

    # Korean to English mapping for your specified 20 items (only matches present ones)
    # 'key' : 'item'

    data = {}
    i = start_idx

    line_title = []
    line_result = []

    for j in range(1, 16):
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
        '질산성질소': 'Nitrate_Nitrogen',
        '염소이온': 'Chloride',
        '카드뮴': 'Cadmium',
        '비소': 'Arsenic',
        '수은': 'Mercury',
        '납': 'Lead',
        '크롬': 'Chromium',
        '페놀': 'Phenol',
        '시안': 'Cyanide',
        '다이아지논': 'Diazinon',
        '파라티온': 'Parathion',
        '트리클로로에틸렌': 'Trichloroethylene',
        '테트라클로로에틸렌': 'Tetrachloroethylene',
        '1,1,1-트리클로로에탄': '1,1,1-Trichloroethane'
    }
    # 'key' : 'item'

    data = {}
    i = start_idx + 4

    line_result = []
    line_title = ['수소이온농도', '총대장균군', '질산성질소', '염소이온', '카드뮴', '비소', '시안', '수은', '다이아지논', '파라티온', '페놀', '납', '크롬',
                  '트리클로로에틸렌', '테트라클로로에틸렌', '1,1,1-트리클로로에탄', '벤젠', '톨루엔', '에틸벤젠', '크실렌']
    for j in range(1, 16):
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
