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


def main():
    fb = FileBase()

    fb.copy_file(HWP_BASE + "\\wt_image.hwp", SEND)
    hwp = Hwp(visible=False)

    hwp.open(f"d:\\05_Send\\wt_image.hwp")
    page_count = hwp.PageCount

    jpg_files = fb.get_file_filter(SEND, "*.jpg")
    jpg_count = len(jpg_files)

    for i, file_name in enumerate(jpg_files):
        _goto_page(hwp, i + 1)
        print(i, file_name)
        hwp.insert_picture(SEND + file_name)

    for i in range(page_count - 1, jpg_count - 1, -1):
        _delete_page(hwp, i + 1)

    remove_empty_page(hwp)
    pagesetup(hwp)

    hwp.save_as("01_WaterAnalysis_Report.hwp")
    hwp.quit()
    fb.delete_file(Path(SEND + "wt_image.hwp"))


if __name__ == "__main__":
    main()
    terminate_all_hwp()
