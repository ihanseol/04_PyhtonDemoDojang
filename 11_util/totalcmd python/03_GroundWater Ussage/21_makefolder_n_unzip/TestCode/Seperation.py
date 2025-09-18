import re


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


# 주어진 텍스트
given_text = """
    I..D...         0  2025-09-17 02:24  00_My Application
    ..A....    712490  2025-02-14 18:28  00_My Application\\01_DDU\\DDU v18.0.9.2\\DDU Logs\\2025-02-14__18-27-18_DDULog.xml
    ..A....   1670840  2025-01-31 02:18  00_My Application\\01_DDU\\DDU v18.0.9.2\\Display Driver Uninstaller.exe
    ..A....    720384  2025-01-31 01:30  00_My Application\\01_DDU\\DDU v18.0.9.2\\Display Driver Uninstaller.pdb
    ..A....      1524  2018-08-15 04:20  00_My Application\\01_DDU\\DDU v18.0.9.2\\Issues and solutions.txt
    ..A....      1087  2025-01-25 07:19  00_My Application\\01_DDU\\DDU v18.0.9.2\\License.txt
"""

# 각 줄을 읽어 파싱하고 출력
dir_list = []
for line in given_text.strip().split('\n'):
    parts = parse_winrar_line(line)
    if parts:
        attributes, size, date, time, name = parts
        if attributes == "I..D...":
            dir_list.append(name)
        # print(f"{{{attributes}}} {{{size}}} {{{date}}} {{{time}}} {{{name}}}")
        # print(f"{name}")

print(dir_list)

