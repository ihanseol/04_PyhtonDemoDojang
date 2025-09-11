
import configparser
import os

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
            elif '2021' in full_path:
                print("→ 현재 CorelDRAW 2021 버전이 활성화되어 있습니다.")
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


#
#     # 주석 처리된 CorelDraw 경로들 확인 (직접 파일 읽기)
#     print("=== 주석 처리된 CorelDraw 설정들 ===")
#     with open('tcer.ini', 'r', encoding='utf-8') as f:
#         lines = f.readlines()
#
#     in_corel_section = False
#     for i, line in enumerate(lines, 1):
#         line_stripped = line.strip()
#
#         # CorelDraw 섹션 시작 확인
#         if line_stripped == "[Program_CorelDraw]":
#             in_corel_section = True
#             continue
#
#         # 다른 섹션 시작되면 CorelDraw 섹션 종료
#         if line_stripped.startswith("[") and line_stripped != "[Program_CorelDraw]":
#             in_corel_section = False
#
#         # CorelDraw 섹션 내의 주석 처리된 라인들 출력
#         if in_corel_section and line_stripped.startswith(';') and 'FullPath' in line_stripped:
#             print(f"  라인 {i}: {line_stripped}")
#
#     print()
#
#     # 전체 섹션 목록 출력 (참고용)
#     print("=== 파일 내 전체 섹션 목록 ===")
#     for section_name in config.sections():
#         if 'Program_' in section_name:
#             print(f"  {section_name}")
#
# except FileNotFoundError:
#     print("tcer.ini 파일을 찾을 수 없습니다.")
# except configparser.Error as e:
#     print(f"ConfigParser 오류: {e}")
# except Exception as e:
#     print(f"기타 오류: {e}")
