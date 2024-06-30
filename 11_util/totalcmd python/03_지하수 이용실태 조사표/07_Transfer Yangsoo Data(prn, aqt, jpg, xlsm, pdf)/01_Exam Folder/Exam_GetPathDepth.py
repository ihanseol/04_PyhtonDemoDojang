import tkinter as tk
from tkinter import filedialog
import FileProcessing_V3 as FP

fp = FP.FileProcessing('')


def select_folder2(initial_dir=''):
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨깁니다.
    folder_path = filedialog.askdirectory(initialdir=initial_dir)  # 초기 디렉토리를 설정하여 폴더 선택 대화 상자를 엽니다.

    if folder_path:
        print("선택한 폴더:", folder_path)
    else:
        print("폴더를 선택하지 않았습니다.")

    return folder_path


def unfold_path(folder_path):
    if fp.check_path(folder_path):
        parts = folder_path.replace('/', '\\').split('\\')

        for part in parts:
            print(part)

        return parts
    else:
        return []


def join_path(folder_list, n=0):
    """
    :param folder_list:
       this is a list of folders of disect
        ['D:', '09_hardRain', '09_ihanseol - 2024', '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청']

    :param n:
        끝에서 부터 몇자리까지 할것인가
        0 : 전체패스
        1 : 끝에서 부터 한자리 전까지 합침

        n 이 양수 이면 -를 부치고
        n 이 음수이면 그냥 쓰고
    :return:
    """
    if n == 0:
        return "\\".join(folder_list[:])
    elif n > 0:
        return "\\".join(folder_list[:-n])
    else:
        return "\\".join(folder_list[:n])


def main_job2():
    spath = select_folder2()
    # spath = "D:/05_Send"
    print(spath)
    print('-' * 60)
    path_list = unfold_path(spath)

    print(path_list[:])
    print(path_list[:-2])
    print(path_list[:-3])

    print('-' * 60)
    print(path_list)
    print('-' * 60)
    print(join_path(path_list))


# def main_job(path1):
#     fp2 = FP.FileProcessing()
#     print(fp2.resolve_path(path1))
#     print('-' * 60)
#     aa = fp2.resolve_path()
#     print(aa)
#     print('-' * 60)
#
#     if not aa:
#         print('this is work ...')

# def main():
# if len(sys.argv) > 1:
#     first_arg = sys.argv[1]
#     print("첫 번째 사용자 인수:", first_arg)
# else:
#     print("사용자 인수가 없습니다.")
#     main_job(sys.argv[0])


if __name__ == '__main__':
    # main()
    main_job2()
