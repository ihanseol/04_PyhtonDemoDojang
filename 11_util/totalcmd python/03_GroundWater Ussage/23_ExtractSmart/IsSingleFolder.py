import os
import sys
import re
import subprocess


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


def is_single_folder(archive_path, winrar_path=r"C:\Program Files\WinRAR\RAR.exe") -> tuple[bool, str | None]:
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

    for _ in dir_list:
        print(_)

    if not dir_list:
        return False, None
    else:
        # first_line = str(dir_list[0])

        first_line = get_editor_name(dir_list[0])
        for line in dir_list:
            result_line = line.split('\\')[0]
            if result_line == first_line:
                continue
            else:
                return False, first_line

    return True, first_line


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python extract_smart.py <압축파일경로>")
        sys.exit(1)

    archive_file = sys.argv[1]
    is_single, folder_name = is_single_folder(archive_file)

    if is_single:
        # print(f"압축 파일은 단일 폴더 구조입니다.")
        print(f"압축 파일은 단일 폴더 구조입니다.", folder_name )
    else:
        # print("압축 파일은 단일 폴더 구조가 아닙니다.")
        print("압축 파일은 단일 폴더 구조가 아닙니다.", folder_name)
