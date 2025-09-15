import configparser
import os
import sys
import shutil
from datetime import datetime


def set_coreldraw_config():
    # ConfigParser 객체 생성
    config = configparser.ConfigParser()
    config.comment_prefixes = (';', '#')

    try:
        # 기존 파일 읽기
        config.read('tcer.ini', encoding='utf-8')

        # Program_CorelDraw 섹션이 없으면 생성
        if 'Program_CorelDraw' not in config:
            config.add_section('Program_CorelDraw')
            print("Program_CorelDraw 섹션을 새로 생성했습니다.")

        # 현재 설정 확인
        print("=== 현재 설정 ===")
        corel_section = config['Program_CorelDraw']
        current_path = corel_section.get('FullPath', '설정되지 않음')
        current_mdi = corel_section.get('MDI', '설정되지 않음')

        print(f"FullPath: {current_path}")
        print(f"MDI: {current_mdi}")

        print("\n=== 새 설정 적용 ===")

        # CorelDraw 설정
        config['Program_CorelDraw'][
            'FullPath'] = r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2019\Programs64\CorelDRW.exe'
        config['Program_CorelDraw']['MDI'] = '1'

        print("FullPath: CorelDRAW 2019로 설정")
        print("MDI: 1로 설정")

        # 파일에 저장하기 전에 주석 처리된 2021 버전 라인 추가
        # configparser는 주석을 직접 쓸 수 없으므로 수동으로 파일 조작
        save_config_with_comments(config)

        print("\n✓ 설정이 성공적으로 저장되었습니다.")

        # 저장 후 확인
        print("\n=== 저장된 설정 확인 ===")
        verify_config()

    except Exception as e:
        print(f"오류 발생: {e}")


def save_config_with_comments(version='2019'):
    """주석이 포함된 설정을 파일에 저장"""

    # 먼저 configparser로 기본 저장
    # with open('tcer.ini', 'w', encoding='utf-8') as f:
    #     config.write(f)

    # 파일을 다시 읽어서 Program_CorelDraw 섹션에 주석 추가
    with open('tcer.ini', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Program_CorelDraw 섹션을 찾아서 주석 라인 추가
    new_lines = []
    in_corel_section = False
    comment_added = False

    for line in lines:
        line_stripped = line.strip()

        # CorelDraw 섹션 시작
        if line_stripped == "[Program_CorelDraw]":
            in_corel_section = True
            new_lines.append(line)
            continue

        # 다른 섹션 시작
        if line_stripped.startswith("[") and line_stripped != "[Program_CorelDraw]":
            in_corel_section = False

        # CorelDraw 섹션 내에서 FullPath 다음에 주석 라인 추가
        if in_corel_section and 'FullPath=' in line and not comment_added:
            # new_lines.append(line)  # 현재 FullPath 라인

            if version == '2019':
                new_lines.append(
                    'FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2019\\Programs64\\CorelDRW.exe\n')
                new_lines.append(
                    ';FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2021\\Programs64\\CorelDRW.exe\n')
            else:
                new_lines.append(
                    'FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2021\\Programs64\\CorelDRW.exe\n')
                new_lines.append(
                    ';FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2019\\Programs64\\CorelDRW.exe\n')
            comment_added = True
            continue

        new_lines.append(line)

    # 수정된 내용을 파일에 저장
    with open('tcer.ini', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)


def verify_config():
    """설정 확인"""
    config = configparser.ConfigParser()
    config.comment_prefixes = (';', '#')
    config.read('tcer.ini', encoding='utf-8')

    if 'Program_CorelDraw' in config:
        corel_section = config['Program_CorelDraw']
        print(f"FullPath: {corel_section.get('FullPath')}")
        print(f"MDI: {corel_section.get('MDI')}")

        # 파일 경로 존재 여부 확인
        full_path = corel_section.get('FullPath')
        if full_path and os.path.exists(full_path):
            print("✓ 경로가 유효합니다.")
        elif full_path:
            print("✗ 경로를 찾을 수 없습니다.")


def switch_to_2021():
    """2021 버전으로 변경하는 함수"""
    config = configparser.ConfigParser()
    config.comment_prefixes = (';', '#')
    config.read('tcer.ini', encoding='utf-8')

    if 'Program_CorelDraw' in config:
        print("CorelDRAW 2021로 변경합니다...")
        config['Program_CorelDraw'][
            'FullPath'] = r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2021\Programs64\CorelDRW.exe'

        # 2019를 주석으로, 2021을 활성화하는 방식으로 저장
        with open('tcer.ini', 'r', encoding='utf-8') as f:
            content = f.read()

        # 2019를 주석으로 변경하고 2021을 활성화
        content = content.replace(
            'FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2019\\Programs64\\CorelDRW.exe',
            ';FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2019\\Programs64\\CorelDRW.exe'
        )
        content = content.replace(
            ';FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2021\\Programs64\\CorelDRW.exe',
            'FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2021\\Programs64\\CorelDRW.exe'
        )

        with open('tcer.ini', 'w', encoding='utf-8') as f:
            f.write(content)

        print("✓ CorelDRAW 2021로 변경되었습니다.")


def switch_to_2019():
    """2019 버전으로 변경하는 함수"""
    config = configparser.ConfigParser()
    config.comment_prefixes = (';', '#')
    config.read('tcer.ini', encoding='utf-8')

    if 'Program_CorelDraw' in config:
        print("CorelDRAW 2019로 변경합니다...")
        config['Program_CorelDraw'][
            'FullPath'] = r'c:\Program Files\Corel\CorelDRAW Graphics Suite 2019\Programs64\CorelDRW.exe'

        # 2019를 주석으로, 2021을 활성화하는 방식으로 저장
        with open('tcer.ini', 'r', encoding='utf-8') as f:
            content = f.read()

        # 2021를 주석으로 변경하고 2019을 활성화
        content = content.replace(
            'FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2021\\Programs64\\CorelDRW.exe',
            ';FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2021\\Programs64\\CorelDRW.exe'
        )
        content = content.replace(
            ';FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2019\\Programs64\\CorelDRW.exe',
            'FullPath=c:\\Program Files\\Corel\\CorelDRAW Graphics Suite 2019\\Programs64\\CorelDRW.exe'
        )

        with open('tcer.ini', 'w', encoding='utf-8') as f:
            f.write(content)

        print("✓ CorelDRAW 2019로 변경되었습니다.")


def read_corel_version():
    # ConfigParser 객체 생성
    config = configparser.ConfigParser()

    # 세미콜론(;)을 주석으로 인식하도록 설정
    config.comment_prefixes = (';', '#')

    try:
        # tcer.ini 파일 읽기 (UTF-8 인코딩)
        config.read('tcer.ini', encoding='utf-8')

        print("=== Program_CorelDraw 섹션 정보 ===")

        # Program_CorelDraw 섹션이 존재하는지 확인
        if 'Program_CorelDraw' in config:
            corel_section = config['Program_CorelDraw']

            # 각 설정값 읽기
            full_path = corel_section.get('FullPath', '설정되지 않음')
            mdi = corel_section.get('MDI', '설정되지 않음')

            print(f"FullPath: {full_path}")
            print(f"MDI: {mdi}")

            # 현재 활성화된 경로 분석
            if full_path != '설정되지 않음':
                if '2019' in full_path:
                    print("→ 현재 CorelDRAW 2019 버전이 활성화되어 있습니다.")
                    return '2019'
                elif '2021' in full_path:
                    print("→ 현재 CorelDRAW 2021 버전이 활성화되어 있습니다.")
                    return '2021'
                else:
                    print("→ 버전 정보를 확인할 수 없습니다.")

                # 파일 존재 여부 확인
                if os.path.exists(full_path):
                    print("✓ 경로가 유효합니다.")
                else:
                    print("✗ 경로를 찾을 수 없습니다.")

            print()

            # 섹션의 모든 키-값 쌍 출력
            print("모든 설정 항목:")
            for key, value in corel_section.items():
                print(f"  {key} = {value}")

        else:
            print("Program_CorelDraw 섹션을 찾을 수 없습니다.")

    except FileNotFoundError:
        print("tcer.ini 파일을 찾을 수 없습니다.")
    except configparser.Error as e:
        print(f"ConfigParser 오류: {e}")
    except Exception as e:
        print(f"기타 오류: {e}")


def copy_tcer_ini(dest_dir, backup_existing=True):
    """
    Copy tcer.ini to the given destination directory.

    Args:
        dest_dir (str): Target directory path.
        backup_existing (bool): If True, backup existing file before overwrite.
    """
    # 현재 디렉토리에 tcer.ini 있다고 가정
    src_file = os.path.join(os.getcwd(), "tcer.ini")
    if not os.path.isfile(src_file):
        raise FileNotFoundError(f"Source file not found: {src_file}")

    # 대상 디렉토리 준비
    os.makedirs(dest_dir, exist_ok=True)
    dest_file = os.path.join(dest_dir, "tcer.ini")

    # 백업 옵션 처리
    if os.path.exists(dest_file) and backup_existing:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = os.path.join(dest_dir, f"tcer_{timestamp}.bak")
        shutil.move(dest_file, backup_file)

    # 파일 복사
    shutil.copy2(src_file, dest_file)
    print(f"Copied {src_file} → {dest_file}")


# 실행
if __name__ == "__main__":
    print("=== CorelDRAW 설정 관리 ===")
    print("기본 설정을 Tcer.ini에서 읽어서 버전은 2019와 2021버전으로 스위칭 합니다.")
    # save_config_with_comments(version='2021')

    if read_corel_version() == '2019':
        switch_to_2021()
    else:
        switch_to_2019()

    copy_tcer_ini(r"c:\Program Files\totalcmd\plugins\utils\util_tcer", backup_existing=False)

    line = input('엔터키를 입력하세요 ...')

    # 사용 예시
    # copy_tcer_ini(r"C:\backup")  # 기존 파일 있으면 백업 후 덮어쓰기
    # copy_tcer_ini(r"D:\configs", backup_existing=False)  # 그냥 덮어쓰기

    #
    # print("=== CorelDRAW 설정 관리 ===")
    # print("1. 기본 설정 (2019 버전)")
    # set_coreldraw_config()
    #
    # print("\n" + "=" * 50)
    # print("2021 버전으로 변경하려면 switch_to_2021() 함수를 호출하세요.")
    # print("예: switch_to_2021()")
