import os


def combine_bas_files():
    """
    지정된 폴더의 모든 .bas 파일을 하나의 파일로 합칩니다.

    Args:
        source_folder (str): .bas 파일이 있는 폴더 경로. 기본값은 'downloads'입니다.
        output_file (str): 합쳐진 내용을 저장할 파일 이름. 기본값은 'combined.bas'입니다.
    """

    source_folder = os.path.expanduser('~/Downloads')
    output_file = r'd:\05_Send\combined.bas'

    # 소스 폴더가 존재하는지 확인합니다.
    if not os.path.isdir(source_folder):
        print(f"오류: '{source_folder}' 폴더를 찾을 수 없습니다.")
        return

    # 합쳐진 내용을 저장할 파일을 쓰기 모드로 엽니다.
    with open(output_file, 'w', encoding='utf-8') as outfile:
        print(f"'{source_folder}' 폴더의 .bas 파일을 합치는 중...")

        # 폴더 내 모든 파일 목록을 가져옵니다.
        for filename in os.listdir(source_folder):
            # 파일 확장자가 '.bas'인지 확인합니다.
            if filename.endswith('.bas'):
                file_path = os.path.join(source_folder, filename)

                # 파일인지 확인하고 내용을 읽습니다.
                if os.path.isfile(file_path):
                    print(f"  - '{filename}' 파일 추가...")
                    try:
                        with open(file_path, 'r', encoding='utf-8') as infile:
                            content = infile.read()
                            # 파일 내용을 합쳐진 파일에 씁니다.
                            outfile.write(f"\n'--- 시작: {filename} ---\n")
                            outfile.write(content)
                            outfile.write(f"\n'--- 끝: {filename} ---\n\n")
                    except Exception as e:
                        print(f"    경고: '{filename}' 파일을 읽는 중 오류가 발생했습니다: {e}")

    print(f"\n모든 .bas 파일이 '{output_file}'에 성공적으로 합쳐졌습니다.")


# 함수를 실행합니다.
if __name__ == "__main__":
    combine_bas_files()
