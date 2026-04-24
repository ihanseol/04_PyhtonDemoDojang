# 2026/04/21
# 목적 : 목차를 찾아서, 목차파일을 생성해주는데 목적이 있다.
# 그동안 목차를 저일하는데, 그냥 하나하나 검색하고 적어주고
# 이것을 무한반복했는데
# 이것을 코드로 바꾸어 주려한다.
#
import sys
import glob
import os
import shutil
import time

from pyhwpx import Hwp
from pathlib import Path
import psutil


def terminate_all_hwp():
    for proc in psutil.process_iter(['name']):
        try:
            # 프로세스 이름에 'hwp'가 포함되어 있는지 확인 (대소문자 구분 안 함)
            if 'hwp' in proc.info['name'].lower():
                proc.kill()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass


def get_first_file(path, extension):
    # path/*.ext 패턴 생성
    pattern = os.path.join(path, f"*{extension}")
    files = glob.glob(pattern)

    for f in files:
        if os.path.isfile(f):
            return f
    return None


def progress_bar(iteration, total, prefix='', suffix='', length=30, fill='█'):
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    # 마지막에 공백을 조금 추가하여 이전 잔상을 지워줍니다.
    sys.stdout.write(f'\r{prefix} |{bar}| {percent}% {suffix}   ')
    sys.stdout.flush()  # 출력 즉시 버퍼를 비움


def copy_file(source, destination):
    try:
        # 파일 복사 (메타데이터 포함)
        shutil.copy2(source, destination)
        print(f"Success: {source} -> {destination}")
    except FileNotFoundError:
        print("Error: 원본 파일을 찾을 수 없습니다.")
    except PermissionError:
        print("Error: 권한이 없습니다.")
    except Exception as e:
        print(f"Error: {e}")


def delete_insert_field(hwp):
    """
        # functionOnScriptMacro_누름틀지우기()
        # {
        #     HAction.GetDefault("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
        #     with (HParameterSet.HDeleteCtrls)
        #     {
        #     CreateItemArray("DeleteCtrlType", 1);
        #     DeleteCtrlType.Item(0) = 17;
        #     }
        #     HAction.Execute("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
        #     }
        # }
    """

    pset = hwp.HParameterSet.HDeleteCtrls
    hwp.HAction.GetDefault("DeleteCtrls", pset.HSet)
    pset.CreateItemArray("DeleteCtrlType", 1)
    pset.DeleteCtrlType.SetItem(0, 17)
    hwp.HAction.Execute("DeleteCtrls", pset.HSet)


def get_pages_with_text_scan(hwp, search_text):
    """
    문서 내 특정 텍스트가 포함된 모든 페이지 번호를 반환
    """
    pages = set()

    if not hwp.init_scan():
        return []

    try:
        while True:
            state, text = hwp.get_text()
            if state <= 1:  # 문서 끝 또는 오류
                break

            if search_text in text:
                # 텍스트가 발견된 위치로 캐럿 이동 후 페이지 번호 획득
                hwp.move_pos(201)
                page_no = hwp.KeyIndicator()[3]
                pages.add(page_no)
                # pg = hwp.XHwpDocuments.Active_XHwpDocument.XHwpDocumentInfo.CurrentPrintPage
                # pages.add(pg)

        return sorted(list(pages))
    finally:
        hwp.release_scan()


def process_table_of_contents_01(file_path, target_list):
    """
    목록 리스트를 순회하며 페이지 번호를 검색하고 결과를 반환
    """
    # hwp = Hwp()
    hwp = Hwp(visible=False)
    hwp.open(file_path)

    results = {}
    l = len(target_list)

    print(f"--- 파일 분석 시작: {file_path} ---")
    for i, target in enumerate(target_list):
        pages = get_pages_with_text_scan(hwp, target)
        progress_bar(i + 1, l, prefix='Progress:', suffix='Complete', length=50)
        current_page = hwp.KeyIndicator()[3]
        results[target] = current_page

    # hwp.quit()
    
    return results


def make_duplicate_list(target_list):
    new_list = []
    target_indices = {4, 7, 11, 12}

    for i, data in enumerate(target_list, start=1):
        new_list.append(data)
        if i in target_indices:
            new_list.append(data)

    return new_list


def write_table_of_contents(target_list):
    print("-- Enter write_table_of_contents(target_list) --", flush=True)

    hwp = Hwp(visible=False)
    hwp.open(r"d:\06_Send2\목차.hwp")

    field_list = [i for i in hwp.get_field_list(0, 0x02).split("\x02")]

    # print("--- make new_list ---", flush=True)
    new_list = make_duplicate_list(target_list)

    previous_field = "save_field"
    total_len = len(new_list)

    for i, (field, data) in enumerate(zip(field_list, new_list), 1):
        # 진행률 표시
        progress_bar(i, total_len, prefix='Progress:', suffix='Writing Data...', length=50)
        time.sleep(.05)
        suffix = "{{1}}" if field == previous_field else "{{0}}"
        field_tag = f"{field}{suffix}"

        hwp.MoveToField(field_tag)
        hwp.PutFieldText(field_tag, data)

        previous_field = field

    # 루프 종료 후 줄바꿈
    print()

    delete_insert_field(hwp)
    hwp.save()
    hwp.quit()


if __name__ == "__main__":
    terminate_all_hwp()
    copy_file(r"c:\Program Files\totalcmd\hwp\목차.hwp", r"d:\06_Send2\목차.hwp")

    # 1. 설정
    # FILE_NAME = r"d:\06_Send3\A1_세종시 연서면 신대리 571 - 2026 영향조사서.hwp"
    FILE_NAME = get_first_file("d:\\05_Send", "hwp")

    # 2. 검색할 목차 리스트
    TOC_TARGETS = [
        "영향조사 결과의 요약",
        "지하수 이용방안",
        "조사서 작성에 관한 사항",
        "II. 수문지질현황 및 원수의 개발가능량",
        "2. 조사지역의 지하수 함양량, 개발가능량 조사",
        "3. 신규 지하수 개발가능량 산정",
        "III. 적정취수량 및 영향범위 산정",
        "2. 적정취수량과 영향반경",
        "3. 잠재오염원과 영향범위",
        "4. 지하수의 개발로 인하여 주변지역에 미치는 영향의 범위 및 정도",
        "IV. 수질의 적정성 평가",
        "Ⅴ. 시설설치계획",
        "2. 사후 관리방안",
        "<  참 고 문 헌  >",
        "<  부    록  >"
    ]

    # 3. 실행
    toc_results = process_table_of_contents_01(FILE_NAME, TOC_TARGETS)

    # 4. 활용 (예: 최종 결과 요약)
    print("\n--- 최종 목차 요약 ---")
    for text, pg in toc_results.items():
        print(f"{text}: {pg}")

    result = list(toc_results.values())
    write_table_of_contents(result)
