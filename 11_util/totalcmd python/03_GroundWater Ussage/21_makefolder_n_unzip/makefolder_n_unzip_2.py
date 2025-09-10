import os
import zipfile
import rarfile
import py7zr
# py7zr 라이브러리 추가
import os
import sys
import tkinter as tk
from tkinter import messagebox
import shutil

SEND_PATH = "D:\\05_Send\\"


def print_debug(msg='', chr='*', len=180):
    print(chr * len)
    print(msg)
    print(chr * len)


def MyMessageBox(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Notice", message)


def copy_file(source_file, target_file):
    try:
        # Copy the file from source to target
        shutil.copy(source_file, target_file)
        print(f"File copied successfully from {source_file} to {target_file}")
        return True
    except FileNotFoundError:
        print(f"Source file not found: {source_file}")
        return False
    except PermissionError:
        print(f"Permission denied. Could not copy to {target_file}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False


def create_folder(path):
    try:
        os.mkdir(path)
        print(f"Folder created successfully: {path}")
    except FileExistsError:
        print(f"Folder already exists: {path}")
    except PermissionError:
        print(f"Permission denied: {path}")
    except Exception as e:
        print(f"An error occurred: {e}")


def is_zipfile(extension):
    return extension.lower() in ['.zip', '.rar', '.7z']


def get_zipfile(path):
    print(path)

    normalized_path = os.path.normpath(path)
    last_part = os.path.basename(normalized_path)
    filename_without_ext, extension = os.path.splitext(last_part)

    if not os.path.isdir(path) and is_zipfile(extension):
        return filename_without_ext


def do_unzip(source_path, target_dir):
    # Check if the file is a .zip file
    if source_path.lower().endswith('.zip'):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        with zipfile.ZipFile(source_path, 'r') as zip_ref:
            zip_ref.extractall(target_dir)

        print(f"압축해제 완료: {source_path} -> {target_dir}")

    # Check if the file is a .rar file
    elif source_path.lower().endswith('.rar'):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        try:
            with rarfile.RarFile(source_path, 'r') as rar_ref:
                rar_ref.extractall(target_dir)
            print(f"압축해제 완료: {source_path} -> {target_dir}")
        except rarfile.RarError as e:
            print(f"오류 발생: {source_path} 압축 해제 실패 - {e}")

    # Check if the file is a .7z file
    elif source_path.lower().endswith('.7z'):
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)

        try:
            with py7zr.SevenZipFile(source_path, mode='r') as sz_ref:
                sz_ref.extractall(path=target_dir)
            print(f"압축해제 완료: {source_path} -> {target_dir}")
        except py7zr.Bad7zFile as e:
            print(f"오류 발생: {source_path} 압축 해제 실패 - {e}")


# 2025/9/11일  목요일
# 토탈커맨더에서 사용하기 위한 목적으로 만들었고
# 소스파일이 토탈커맨더에서 인자를 처리하기 위한 파일위치가 되기에
# 다음처럼 코드가 쓰여진다.


def main():
    print(f"Number of arguments: {len(sys.argv)}")
    print(f"Script name: {sys.argv[0]}")

    for i, arg in enumerate(sys.argv[1:], start=1):
        print(f"Argument {i}: {arg}")

    local_appdata = os.getenv('LOCALAPPDATA')

    source_file = local_appdata + "\\Temp\\" + os.path.basename(sys.argv[1])
    target_dir = sys.argv[2]

    copy_file(source_file, SEND_PATH + "dir_list.txt")
    source_file = SEND_PATH + "dir_list.txt"
    os.chdir(target_dir)

    print(f"1, source : {source_file}")
    print(f"1, target : {target_dir}")

    # _ = input("Press Enter to Proced ...")

    print(os.getcwd())

    try:
        with open(source_file, 'r', encoding='cp949') as file:
            for line in file:
                clean_path = line.replace("\n", "")
                zip_filename = get_zipfile(clean_path)
                create_folder(os.path.join(target_dir, zip_filename))
                do_unzip(clean_path, os.path.join(target_dir, zip_filename))

    except Exception as e:
        print(f"An error occurred, {source_file} : ", e)
        MyMessageBox(f" File Not Found .... {source_file} ")

    # _ = input("Press Enter to Proced ...")
    os.remove(source_file)


if __name__ == "__main__":
    main()
