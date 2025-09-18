import os
import sys
import re
import subprocess
import tkinter as tk
from tkinter import messagebox
import shutil

from numpy.matlib import empty

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


def smart_extract(archive_path: str) -> list[str] | None:
    """
    WinRAR를 사용하여 압축 파일의 내용을 조건부로 해제합니다.
    - 단일 폴더가 있으면 그 안에 바로 해제합니다.
    - 여러 파일이나 폴더가 있으면 압축 파일 이름으로 폴더를 만들고 그 안에 해제합니다.
    """

    rar_executable = r"C:\Program Files\WinRAR\RAR.exe"
    print(f"smart_extract:  archive path = {archive_path}")

    if not os.path.exists(archive_path):
        print(f"오류: 파일을 찾을 수 없습니다 - {archive_path}")
        return None

    # 압축 파일 내부의 내용물 목록을 가져옵니다.
    # 'v' (verbose list) 명령어를 사용하여 목록을 확인합니다.
    try:
        # 'l -v'는 유효한 rar 명령이 아니므로 'v'로 수정합니다.
        command = [rar_executable, 'v', archive_path]
        result = subprocess.run(command, capture_output=True, text=True, check=True, encoding='cp949')
        output_lines = result.stdout.strip().split('\n')
        return output_lines

    except subprocess.CalledProcessError as e:
        print(f"RAR 실행 오류: {e}")
        return None
    except FileNotFoundError:
        print(f"오류: RAR 실행 파일을 찾을 수 없습니다. 경로를 확인하세요: {rar_executable}")
        return None


def parse_winrar_line(line):
    """
    WinRAR 'v' 명령어 출력의 한 줄을 파싱하여 각 그룹을 반환합니다.

    :param line: WinRAR 출력의 한 줄 문자열
    :return: (attributes, size, date, time, name) 튜플 또는 None
    """
    # 주어진 형식을 정확히 파싱하기 위한 정규 표현식
    # 1. Attributes: (I..D...)
    # 2. Size: 숫자 (공백 포함)
    # 3. Date: YYYY-MM-DD 형식
    # 4. Time: HH:MM 형식
    # 5. Name: 나머지 모든 문자열 (공백 포함)
    pattern = r"^\s*(?P<attributes>\S+)\s+(?P<size>\d+)\s+(?P<date>\d{4}-\d{2}-\d{2})\s+(?P<time>\d{2}:\d{2})\s+(?P<name>.*)$"

    match = re.match(pattern, line)

    if match:
        return (
            match.group('attributes').strip(),
            match.group('size').strip(),
            match.group('date').strip(),
            match.group('time').strip(),
            match.group('name').strip()
        )
    return None


def get_editor_name(given_string):
    parts = given_string.split('\\')
    print(parts)

    return parts[0]


def check_for_single_folder(archive_path, winrar_path=r"C:\Program Files\WinRAR\RAR.exe") -> tuple[bool, str | None]:
    """
    Checks if the given archive contains exactly one top-level folder.

    Parameters
    ----------
    archive_path : str
        Path to the archive file (.rar, .zip, etc.)
    winrar_path : str
        Path to WinRAR's RAR.exe CLI tool

    Returns
    -------
    bool
        True if the archive contains exactly one top-level folder,
        False otherwise.
    """
    if not os.path.exists(archive_path):
        raise FileNotFoundError(f"Archive not found: {archive_path}")
    if not os.path.exists(winrar_path):
        raise FileNotFoundError(f"WinRAR not found: {winrar_path}")

    # Run WinRAR list command
    result = subprocess.run(
        [winrar_path, "l", "-vc", archive_path],
        capture_output=True,
        text=True,
        encoding="cp949",  # WinRAR 기본 인코딩 (cp437, 한글은 cp949일 수도 있음)
        errors="ignore"
    )

    output = result.stdout
    lines = output.splitlines()

    dir_list = []

    for line in lines[9:]:
        line = line.strip()
        parts = parse_winrar_line(line)
        if parts:
            attributes, size, date, time, name = parts
            if attributes == "I..D...":
                dir_list.append(name)

    # print(dir_list)

    if not dir_list:
        return False, None
    else:

        first_line = get_editor_name(dir_list[0])
        for line in dir_list:
            result_line = line.split('\\')[0]
            if result_line == first_line:
                continue
            else:
                return False, first_line

    return True, first_line


def main2():
    # clean_path = "d:\\11_exaData\\06_util\\99_Game\\01_ToatalCommander Plugin\\00_Program Data\\00_My Application.rar"
    clean_path = "d:\\11_exaData\\06_util\\99_Game\\01_ToatalCommander Plugin\\00_Program Data\\25_Editor.rar"

    is_single_folder, folder_name = check_for_single_folder(clean_path)
    print('is_single_folder =', is_single_folder, 'folder_name =', folder_name)


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

                # file_content = smart_extract(clean_path)
                # print(file_content)
                #
                is_single_folder, folder_name = check_for_single_folder(clean_path)
                print('is_single_folder =', is_single_folder, 'folder_name =', folder_name)

                # input("please enter 1...")

                if is_single_folder:
                    print("단일 폴더를 감지했습니다. 바로 압축을 해제합니다.")
                    extract_command = [winrar_path, 'x', "-Y", clean_path, target_dir]
                else:
                    print("단일 폴더가 아닙니다. 새 폴더를 만들고 압축을 해제합니다.")
                    extract_command = [winrar_path, 'x', '-ad', "-Y", clean_path, target_dir]

                # input("please enter 2...")

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
