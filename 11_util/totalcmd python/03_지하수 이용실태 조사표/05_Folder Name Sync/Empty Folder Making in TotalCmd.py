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


def get_lastdirectory(path):
    print(path)

    if os.path.isdir(path):
        normalized_path = os.path.normpath(path)
        last_part = os.path.basename(normalized_path)
        return last_part
    else:
        _ = input("Do you want to Exit")
        return "The given path is not a directory."


def main():
    os.chdir(SEND_PATH)
    # Print the number of arguments (including the script name)
    print(f"Number of arguments: {len(sys.argv)}")

    # Print the script name
    print(f"Script name: {sys.argv[0]}")

    # Print all arguments one by one
    for i, arg in enumerate(sys.argv[1:], start=1):
        # arg_temp = arg.replace('"', '\\')
        # print(f"Argument {i}: {arg_temp}")
        print(f"Argument {i}: {arg}")

    # print_debug('this is parsing argument ', '-')
    # source_dir = sys.argv[1].replace('"', '\\')
    # target_dir = sys.argv[2].replace('"', '\\')

    local_appdata = os.getenv('LOCALAPPDATA')

    source_file = local_appdata + "\\Temp\\" + os.path.basename(sys.argv[1])
    target_dir = sys.argv[2]

    copy_file(source_file, SEND_PATH + "dir_list.txt")
    source_file = "dir_list.txt"
    os.chdir(target_dir)

    print(f"1, source : {source_file}")
    print(f"1, target : {target_dir}")

    _ = input("Press Enter to Proced ...")

    print(os.getcwd())

    try:
        with open(source_file, 'r', encoding='cp949') as file:
            for line in file:
                clean_path = line.replace("\n", "")
                lastdir = get_lastdirectory(clean_path)
                create_folder(lastdir)

    except Exception as e:
        print(f"An error occurred, {source_file} : ", e)
        MyMessageBox(f" File Not Found .... {source_file} ")

    _ = input("Press Enter to Proced ...")
    os.remove(SEND_PATH + source_file)


if __name__ == "__main__":
    main()
