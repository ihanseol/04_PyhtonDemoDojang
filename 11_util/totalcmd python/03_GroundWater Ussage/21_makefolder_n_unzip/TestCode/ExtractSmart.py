import os
import sys
import subprocess
import re


def smart_extract(archive_path: str, rar_executable: str) -> list[str] | None:
    """
    WinRAR를 사용하여 압축 파일의 내용을 조건부로 해제합니다.
    - 단일 폴더가 있으면 그 안에 바로 해제합니다.
    - 여러 파일이나 폴더가 있으면 압축 파일 이름으로 폴더를 만들고 그 안에 해제합니다.
    """

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


def check_for_single_folder(file_list_output: list[str] | None) -> tuple[bool, str | None]:
    if not file_list_output:
        return False, None

    lines = file_list_output
    # WinRAR 목록의 실제 내용이 시작하는 위치를 찾습니다.
    content_start_index = -1
    for i, line in enumerate(lines):
        if line.strip().startswith('---'):
            content_start_index = i + 1
            break

    if content_start_index == -1:
        print("경고: 파일 목록 헤더를 찾을 수 없습니다.")
        return False, None

    # 모든 파일/폴더 경로를 저장할 리스트
    paths = []

    for line in lines[content_start_index:]:
        # '----' 라인 이후의 내용 중 실제 파일/폴더 경로를 추출합니다.
        # 공백으로 시작하고, Name: 또는 '----' 라인이 아닌 유효한 라인만 처리
        if line.strip() and not line.strip().startswith('Name:') and not line.strip().startswith('---'):
            # 경로가 포함된 부분만 추출
            parts = line.split()
            if len(parts) > 4:
                path = " ".join(parts[4:])
                paths.append(path)

    if not paths:
        return False, None

    # 최상위 폴더/파일 이름을 추출합니다.
    top_level_items = set()
    for path in paths:
        # 경로의 첫 번째 부분을 분리 (예: '00_My Application' 또는 'readme.txt')
        parts = path.replace('\\', '/').split('/')
        if parts:
            top_level_items.add(parts[0])

    # 최상위 항목이 하나뿐인지 확인
    if len(top_level_items) == 1:
        single_folder_name = list(top_level_items)[0]
        # 해당 항목이 폴더인지 확인 (경로 목록에서 해당 이름 뒤에 '\' 또는 '/'가 붙어있는지 확인)
        # 예: '00_My Application'이 단일 폴더인지
        is_directory = any(
            path.startswith(single_folder_name + '\\') or path.startswith(single_folder_name + '/') for path in paths)

        if is_directory:
            print(f"단일 최상위 폴더를 감지했습니다: {single_folder_name}")
            return True, single_folder_name
        else:
            print(f"최상위 항목이 하나지만, 폴더가 아닌 파일입니다: {single_folder_name}")
            return False, None
    else:
        print(f"최상위 항목이 여러 개입니다: {top_level_items}")
        return False, None


if __name__ == "__main__":
    # WinRAR 실행 파일 경로 설정 (환경에 맞게 수정)
    rar_path = r"C:\Program Files\WinRAR\Rar.exe"  # GUI보다 콘솔 버전(Rar.exe)이 더 안정적일 수 있습니다.
    winrar_path = r"C:\Program Files\WinRAR\WinRar.exe"  # GUI보다 콘솔 버전(Rar.exe)이 더 안정적일 수 있습니다.

    if len(sys.argv) < 2:
        print("사용법: python extract_smart.py <압축파일경로>")
        sys.exit(1)

    archive_file = sys.argv[1]
    file_content = smart_extract(archive_file, rar_path)

    is_single_folder, folder_name = check_for_single_folder(file_content)

    if is_single_folder:
        print("단일 폴더를 감지했습니다. 바로 압축을 해제합니다.")
        extract_command = [winrar_path, 'x', "-Y", archive_file]
    else:
        print("단일 폴더가 아닙니다. 새 폴더를 만들고 압축을 해제합니다.")
        extract_command = [winrar_path, 'x', '-ad', "-Y", archive_file]

    try:
        subprocess.run(extract_command, check=True)
        print("압축 해제가 완료되었습니다.")
    except subprocess.CalledProcessError as e:
        print(f"압축 해제 중 오류 발생: {e}")
    except Exception as e:
        print(f"예기치 않은 오류 발생: {e}")
