# # 주어진 경로
# path = "D:/09_hardRain/09_ihanseol - 2024/07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청"
#
# # 슬래시를 기준으로 분리
# path_parts = path.replace('/', '\\').split('\\')
#
# # 각 항목을 줄 단위로 출력
# for part in path_parts:
#     print(part)

import os
import FileProcessing_V3 as FP

fp = FP.FileProcessing()


def unfold_path(folder_path):
    # 경로 유효성 검사를 추가 (가정: fp 모듈의 check_path 함수 사용)
    if fp.check_path(folder_path):
        # 슬래시를 역슬래시로 바꾸고 분리
        parts = folder_path.replace('/', '\\').split('\\')

        # 각 부분을 줄 단위로 출력하고 리스트에 추가
        for part in parts:
            print(part)

        # 분리된 경로 부분들을 반환
        return parts
    else:
        # 경로가 유효하지 않은 경우 빈 리스트 반환
        return []


# 사용 예시
folder_path = "D:/09_hardRain/09_ihanseol - 2024/07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청"

# 주어진 경로 리스트
path_list = [
    'D:',
    '09_hardRain',
    '09_ihanseol - 2024',
    '07_공업용 - 세종, 주안레미콘 2개공, 연장허가 - 현윤이엔씨, 보완보고서 , 청주기상청'
]

# os.path.join을 사용하여 경로 결합
joined_path = os.path.join(*path_list)
print(joined_path)

joined_path = os.path.join(*path_list[:-1])
joined_p = '\\'.join(path_list[:-1])
print(joined_path)
print(joined_p)




#
#
# # 함수 호출
result = unfold_path(folder_path)
print(result)
