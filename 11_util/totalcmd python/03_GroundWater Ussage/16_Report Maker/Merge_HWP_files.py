from pyhwpx import Hwp  # 임포트
import os

hwp = Hwp()  # 한/글 실행

# 작업할 디렉토리를 명시적으로 설정 (예: "C:/Users/Username/Documents")
target_dir = "D:\\05_Send"

# 작업 디렉토리로 변경
os.chdir(target_dir)

# 끼워넣기
file_list = [i for i in os.listdir() if i.endswith(".hwpx")]
hwp.open(file_list[0])  # 첫 번째(0) 파일 열기
for i in file_list[1:]:  # 첫 번째(0) 파일은 제외하고 두 번째(1)파일부터 아래 들여쓰기한 코드 반복
    hwp.MoveDocEnd()  # 한/글의 문서 끝으로 이동해서
    hwp.BreakPage()  # <----------------------- 페이지나누기(Ctrl-Enter)
    hwp.insert_file(i)  # 문서끼워넣기(기본값은 섹션, 글자, 문단, 스타일 모두 유지??)
hwp.save_as("취합본.hwp")  # 반복이 끝났으면 "취합본.hwp"로 다른이름으로저장

hwp.Quit()  # 한/글 프로그램 종료