import os
import sys
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
import shutil
from folder_and_files_Inside_ZIP import print_archive_contents


SEND_PATH = "d:\\05_Send\\"


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

def main():
    winrar_path = r"C:\Program Files\WinRAR\WinRar.exe"

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
    print(f"2, target : {target_dir}")

    print(os.getcwd())
    # input("Press Enter to Proced ...")

    try:
        with open(source_file, 'r', encoding='cp949') as file:
            for line in file:
                clean_path = line.replace("\n", "").replace("\\", "\\\\")
                print(clean_path)

                num_files = print_archive_contents(clean_path)
                if num_files == 1:
                    is_single_folder = True
                else:
                    is_single_folder = False

                if is_single_folder:
                    extract_command = [winrar_path, 'x', "-Y", clean_path, target_dir]
                else:
                    extract_command = [winrar_path, 'x', '-ad', "-Y", clean_path, target_dir]

                try:
                    subprocess.run(extract_command, check=True)
                    print("압축 해제가 완료되었습니다.")
                except subprocess.CalledProcessError as e:
                    print(f"압축 해제 중 오류 발생: {e}")
                except Exception as e:
                    print(f"예기치 않은 오류 발생: {e}")

    except Exception as e:
        print(f" an error occurred, {source_file} : ", e)
        MyMessageBox(f" file Not Found .... {source_file} ")

    # _ = input("Press Enter to Proced ...")
    os.remove(source_file)


if __name__ == "__main__":
    main()
    # main2()
