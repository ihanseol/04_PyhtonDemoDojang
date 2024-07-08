import tkinter as tk
from tkinter import filedialog
import os


def select_folder():
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨깁니다.
    os.chdir("d:\\09_hardRain\\09_ihanseol - 2024\\")
    print("cwd :", os.getcwd())

    folder_path = filedialog.askdirectory()  # 폴더 선택 대화 상자를 엽니다.
    if folder_path:
        print("선택한 폴더:", folder_path)
    else:
        print("폴더를 선택하지 않았습니다.")


def select_folder2(initial_dir):
    root = tk.Tk()
    root.withdraw()  # 메인 윈도우를 숨깁니다.
    folder_path = filedialog.askdirectory(initialdir=initial_dir)  # 초기 디렉토리를 설정하여 폴더 선택 대화 상자를 엽니다.
    if folder_path:
        print("선택한 폴더:", folder_path)
    else:
        print("폴더를 선택하지 않았습니다.")


if __name__ == "__main__":
    initial_directory = "d:\\09_hardRain\\09_ihanseol - 2024\\"  # 원하는 초기 디렉토리 경로로 변경하세요.
    select_folder2(initial_directory)
