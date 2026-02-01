import re
import os
import shutil
import time
import datetime
from pyhwpx import Hwp
from pathlib import Path
from FileManger_V0_20250406 import FileBase
import psutil

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
            # 프로세스가 이미 종료되었거나 권한 문제 발생 시 무시
            pass

    if killed_count > 0:
        print(f"--- 총 {killed_count}개의 프로세스를 종료했습니다. ---")
    else:
        print("대상 프로세스를 찾지 못했습니다.")


def delete_table(hwp, page_index):
    hwp.goto_page(page_index)
    hwp.Delete()


def is_image(hwp, page_index):
    hwp.goto_page(page_index)
    hwp.MoveRight()
    hwp.goto_addr("A2")
    hwp.SelectCtrlFront()
    if hwp.CurSelectedCtrl.UserDesc == "그림":
        hwp.Cancel()
        return True
    else:
        hwp.Cancel()
        return False


def remove_empty_table(hwp, hwp_path):
    hwp.open(hwp_path)
    page_count = hwp.PageCount

    for i in range(page_count, 0, -1):
        print(f'reve_empty_table : page{i}')
        if not is_image(hwp, i):
            delete_table(hwp, i)


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



def remove_empty_pagemain():
    fb = FileBase()
    hwp_files = fb.get_file_filter(".", "*.hwp*")

    if not hwp_files:
        print("No PDF files found in current directory")
        return

    hwp_path = hwp_files[0]
    print(f"Processing PDF: {hwp_path}\n")

    hwp = Hwp(visible=False)
    hwp.open(hwp_path)
    remove_empty_table(hwp, hwp_path)
    remove_empty_page(hwp)
    hwp.Quit(save=True)


def main():
    fb = FileBase()
    hwp_files = fb.get_file_filter(".", "*.hwp*")

    if not hwp_files:
        print("No PDF files found in current directory")
        return

    hwp_path = hwp_files[0]
    print(f"Processing PDF: {hwp_path}\n")

    hwp = Hwp(visible=False)
    hwp.open(hwp_path)
    remove_empty_table(hwp, hwp_path)
    remove_empty_page(hwp)
    hwp.Quit(save=True)


if __name__ == "__main__":
    main()
    terminate_all_hwp()



