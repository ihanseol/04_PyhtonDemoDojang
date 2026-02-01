from pyhwpx import Hwp
from pathlib import Path
from FileManger_V0_20250406 import FileBase
import psutil

HWP_BASE = r"d:\09_hardRain\10_ihanseol - 2025\00_data\04_Reference Data\12_보고서, 부록\00_UsedWell\\"
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
            # 프로세스가 이미 종료되었거나 권한 문제 발생 시 무시
            pass

    if killed_count > 0:
        print(f"--- 총 {killed_count}개의 프로세스를 종료했습니다. ---")
    else:
        print("대상 프로세스를 찾지 못했습니다.")


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
    terminate_all_hwp()



