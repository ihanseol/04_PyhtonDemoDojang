from pyhwpx import Hwp  # 임포트
from FileManger_V0_20250406 import FileBase
import os
import glob


def pagesetup(hwp):
    my_page = {'위쪽': 25, '머리말': 10, '왼쪽': 27, '오른쪽': 23, '제본여백': 0, '꼬리말': 10, '아래쪽': 13, '제본타입': 0, '용지방향': 0,
               '용지길이': 297, '용지폭': 210}

    hwp.set_pagedef(my_page, "cur")
    print(my_page)


def merge_hwp_files(ofilename='ex_wt_result.hwp', mode='normal'):
    # def merge_hwp_files(ofilename='01_취합본.hwp'):
    hwp = Hwp(visible=False)  # 한/글 실행
    fb = FileBase()

    # 작업할 디렉토리를 명시적으로 설정 (예: "C:/Users/Username/Documents")
    target_dir = "D:\\05_Send"

    # 작업 디렉토리로 변경
    os.chdir(target_dir)

    # 끼워넣기
    # file_list = [i for i in os.listdir() if i.endswith(".hwpx")]
    file_list = fb.get_file_filter(".", "ex_water*.hwp*")

    if mode == 'normal':
        pass
    else:
        reversed_list = file_list[::-1]
        file_list = reversed_list

    print(file_list)

    hwp.open(file_list[0])  # 첫 번째(0) 파일 열기
    for i in file_list[1:]:  # 첫 번째(0) 파일은 제외하고 두 번째(1)파일부터 아래 들여쓰기한 코드 반복
        hwp.MoveDocEnd()  # 한/글의 문서 끝으로 이동해서
        #  hwp.BreakPage()  # <----------------------- 페이지나누기(Ctrl-Enter)
        hwp.insert_file(i)  # 문서끼워넣기(기본값은 섹션, 글자, 문단, 스타일 모두 유지??)

    hwp.HAction.Run("MoveRight")
    hwp.HAction.Run('SelectAll')
    pagesetup(hwp)
    hwp.save_as(ofilename)  # 반복이 끝났으면 "취합본.hwp"로 다른이름으로저장
    hwp.Quit()  # 한/글 프로그램 종료
    remove_filelist_files(file_list)


def remove_filelist_files(file_list):
    """Removes all *.hwpx files within the specified directory."""
    directory = "D:\\05_Send"

    for file in file_list:
        try:
            file_path = directory + "\\" + file
            os.remove(file_path)
            print(f"Removed: {file_path}")
        except OSError as e:
            print(f"Error deleting {file_path}: {e}")


if __name__ == "__main__":
    merge_hwp_files()
