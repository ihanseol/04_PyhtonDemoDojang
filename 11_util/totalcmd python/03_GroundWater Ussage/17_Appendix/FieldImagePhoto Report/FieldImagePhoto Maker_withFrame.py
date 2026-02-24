from pyhwpx import Hwp
from pathlib import Path
from FileManger_V0_20250406 import FileBase
import psutil

# HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell\\"

HWP_BASE = r"d:\09_hardRain\11_ihanseol - 2026\00_data\04_Reference Data\17_WaterAnalysis_Report"
SEND = "d:\\05_Send\\"


def terminate_all_hwp():
    """
    프로세스 이름이 'hwp'로 시작하는 모든 실행 파일을 찾아 종료합니다.
    """
    killed_count = 0
    print("이름이 'hwp'로 시작하는 모든 프로세스 종료를 시작합니다...")

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name']

            # 프로세스 이름이 존재하고, 'hwp'로 시작하는지 확인 (대소문자 무시)
            if process_name and process_name.lower().startswith('hwp'):
                proc.kill()
                print(f"종료됨: {process_name} (PID: {proc.info['pid']})")
                killed_count += 1

        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
            # 프로세스가 이미 종료되었거나 권한 문제 발생 시 무시

    if killed_count > 0:
        print(f"--- 총 {killed_count}개의 프로세스를 종료했습니다. ---")
    else:
        print("대상 프로세스를 찾지 못했습니다.")


def _goto_page(hwp, page_num):
    """Navigate to specific page in HWP document."""
    hwp.goto_page(page_num)
    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run("MoveDown")


def _goto_page_one(hwp, page_num):
    """Navigate to specific page in HWP document."""
    hwp.goto_page(page_num)
    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveDown")


def _goto_page_two(hwp, page_num):
    """Navigate to specific page in HWP document."""
    hwp.goto_page(page_num)
    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveDown")
    hwp.HAction.Run("MoveDown")


def resize_object_43(hwp):
    # 선택된 개체의 속성을 변경합니다.
    # 35149 HWPUNIT ≒ 124mm / 26362 HWPUNIT ≒ 93mm
    hwp.resize_image(width=35149, height=26362, unit="hwpunit")


def _delete_page(hwp, page_num):
    """Navigate to specific page in HWP document."""
    hwp.goto_page(page_num)
    hwp.Delete()
    print(f"{page_num} page are deleted.")


def is_empty_mypage(hwp, page_index):
    ret = hwp.get_page_text(page_index - 1).replace("\r\n", "").replace(" ", "")
    print(f'page{page_index} : {ret}')
    if ret == '':
        return True
    else:
        return False


def remove_empty_page(hwp):
    for i in range(hwp.PageCount, 0, -1):
        if is_empty_mypage(hwp, i):
            hwp.goto_page(i)
            hwp.DeletePage()


def pagesetup(hwp):
    my_page = {'위쪽': 20, '머리말': 10, '왼쪽': 20, '오른쪽': 20, '제본여백': 0, '꼬리말': 10, '아래쪽': 13, '제본타입': 0, '용지방향': 0,
               '용지길이': 297, '용지폭': 210}

    hwp.set_pagedef(my_page, "cur")
    print(my_page)


def _align_center_all(hwp):
    # 1. 문서의 맨 마지막으로 이동
    hwp.MovePos(3)  # 3은 문서 끝(MovePosEnd)을 의미합니다.

    # 2. 전체 선택 (Ctrl + A)
    hwp.SelectAll()

    # 3. 가운데 정렬 적용
    # 'ParagraphShape' 액션을 사용하여 정렬 방식(AlignType)을 2(가운데)로 설정합니다.
    hwp.ParagraphShapeAlignCenter()

    # 선택 영역 해제 (원할 경우)
    hwp.Run("Cancel")


def main():
    fb = FileBase()

    fb.copy_file(HWP_BASE + "\\FieldImage_Photo.hwp", SEND)
    hwp = Hwp(visible=False)

    hwp.open(f"d:\\05_Send\\FieldImage_Photo.hwp")
    page_count = hwp.PageCount

    jpg_files = fb.get_file_filter(SEND, "*.jpg")
    jpg_count = len(jpg_files) // 2

    for i in range(jpg_count):
        print(f"{i + 1}. {jpg_files[i]}")

        _goto_page_one(hwp, i + 1)
        hwp.insert_picture(SEND + jpg_files[i * 2 + 1])
        hwp.resize_image(width=35149, height=26362, unit="hwpunit")

        _goto_page_two(hwp, i + 1)
        hwp.insert_picture(SEND + jpg_files[i * 2])
        hwp.resize_image(width=35149, height=26362, unit="hwpunit")

    _align_center_all(hwp)

    for i in range(page_count - 1, jpg_count - 1, -1):
        _delete_page(hwp, i + 1)

    remove_empty_page(hwp)
    pagesetup(hwp)

    hwp.save_as("01_FieldImage_Report.hwp")
    hwp.quit()
    fb.delete_file(Path(SEND + "FieldImage_Photo.hwp"))


if __name__ == "__main__":
    main()
    terminate_all_hwp()
