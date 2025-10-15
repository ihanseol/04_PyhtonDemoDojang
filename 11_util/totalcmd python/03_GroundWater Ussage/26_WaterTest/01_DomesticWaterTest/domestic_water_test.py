import pymupdf
import re


def get_data(pdf_name, page):
    doc = pymupdf.open(pdf_name)
    if page > len(doc):
        doc.close()
        return {}

    page_obj = doc.load_page(page - 1)
    text = page_obj.get_text("text")  # Or "blocks" for better table handling if needed
    doc.close()

    # Split into lines and filter non-empty
    print('='*100)
    for line in text.split('\n'):
        print(line)

    print('=' * 100)

    lines = [line.strip() for line in text.split('\n') if line.strip()]

    # Find start of results table (look for key items or NO patterns)
    start_idx = None
    for i, line in enumerate(lines):
        if line == '1':
            start_idx = i-1
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

    print(line_title)
    print(line_result)

    for i, item in enumerate(key_map):
        data[key_map[item]] = line_result[i]
        print(item, data[key_map[item]])

    return data


def main():
    pdf_name = r"d:\05_Send\수질성적서_대구시경찰청.pdf"
    result = get_data(pdf_name, 1)
    print(result)


if __name__ == "__main__":
    main()
