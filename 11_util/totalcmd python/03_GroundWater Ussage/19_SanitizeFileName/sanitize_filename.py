import os
import re
from pyhwpx import Hwp

company_name = ""
gongo_title = ""


def sanitize_filename(filename: str, replacement: str = "_") -> str:
    """
    경로 저장시 삽입불가한 문자들을 지정문자로 치환하는 함수

    ChatGPT의 도움을 받아 정의하였으나,
    파이썬 외부모듈 중에서는 pathvalidate가 가장 완성도나 인기가 높은 듯.
    https://github.com/thombashi/pathvalidate

    Args:
        filename: 기존 파일경로 문자열
        replacement: 금칙문자 를 교체할 문자(기본값은 "_")

    Returns:
        경로 문자열에 사용 가능한 문자열만 남기고, 금칙문자들은 모두 "_"로 치환한 경로 문자열

    Example:
        >>> fname = 'fi:l*e/p\"a?t>h|.t<xt'
        >>> print(sanitize_filename(fname, "")
        file/path.txt
    """
    forbidden_chars = r'[\\/:"*?<>|]'
    sanitized = re.sub(forbidden_chars, replacement, filename)

    # 예약어 필터링
    reserved_names = {
        "CON", "PRN", "AUX", "NUL",
        *["COM" + str(i) for i in range(1, 10)],
        *["LPT" + str(i) for i in range(1, 10)]
    }
    base_name = sanitized.split('.')[0].upper()
    if base_name in reserved_names:
        sanitized = "_" + sanitized
    return sanitized


# os.chdir(r"./실습파일")
try:  # 중간에 오류가 나서 프로그램이 종료되더라도, 아래 finally절의 아래아한글 종료 코드가 실행되도록 함.
    hwp = Hwp(new=True, visible=False)  # 새 아래아한글 창을 백그라운드에서 실행
    hwp.open("천페이지문서쪼개기.hwpx")

    # 전체 페이지 카운트하기(작업진도를 출력하기 위함)
    total = 1
    while hwp.find("공고명"):
        total += 1

    # 본격적인 쪼개기 코드
    # 공고 구분 방법 : 모든 공고의 첫 번째 표 A2 셀의 문자열이 "공고명"이므로!!
    #                  다음 "공고명"을 찾아가서 셀주소가 A2이면??
    #                  이전페이지까지만 블록선택해서 pdf로 저장하고 지우면 됨ㅎ

    current = 1  # 진행상황을 화면에 출력할 때 사용하는 변수( "[123/400]" 방식)

    while hwp.set_pos(3, 0, 0):  # 기업명이 있는 셀(B1)로 이동 반복하면서
        company_name = hwp.get_selected_text()  # 셀의 문자열을 기업명 변수에 저장
        company_name = sanitize_filename(company_name, replacement="")  # 파일명에 쓸 예정이므로 금칙글자 제거
        hwp.TableLowerCell()  # 아래 셀(B2: 공고명)로 이동
        gongo_title = hwp.get_selected_text()  # 셀의 문자열을 공고명 변수에 저장
        gongo_title = sanitize_filename(gongo_title, "")  # 마찬가지로 금칙글자 제거
        if not hwp.find("공고명"):  # 다음 공고가 없으면(마지막 공고인 경우에는)
            break  # while문 종료
        if hwp.get_cell_addr() == "A2":  # 다음 공고의 "공고명"이라는 셀로 이동했는데 셀주소가 A2면?
            hwp.CloseEx()  # 표 왼쪽으로 나와서
            hwp.MoveLeft()  # 이전 페이지 마지막으로 커서를 옮긴 후
            hwp.MoveSelDocBegin()  # 문서 시작점까지 선택(공고 1개 전체선택)

            # 기존에 동일한 이름의 공고명 파일이 있는지 조사하고,
            # 동일파일이 있으면 파일명 뒤에 "_숫자" 붙여주기

            i = 1  # 파일명 중복시 파일 뒤에 붙일 숫자
            if f"{company_name}_{gongo_title}.pdf" in os.listdir():  # 만약 동일명의 파일이 기존에 만들어져 있으면
                while f"{company_name}_{gongo_title}_{i}.pdf" in os.listdir():  # "공고명"을 "공고명_1"로 바꿔보고 그래도 있으면
                    i += 1  # "공고명_2", "공고명_3" 등, 없는 숫자가 나올 때까지 반복
                gongo_title = f"{gongo_title}_{i}"  # 없는 숫자 i로 공고명 최종 변경 완료

            hwp.save_block_as(f"{company_name}_{gongo_title}.pdf", format="PDF")  # pdf로 저장
            hwp.Delete()  # 저장한 페이지 삭제
            hwp.Delete()  # 빈 페이지 삭제
            print(f"[{current / total * 100:0.1f}%][{current}/{total}]{company_name}_{gongo_title}")  # 작업진도 출력
            current += 1  # 진도 + 1

    # 마지막 한 개의 공고만 남아있는 상태로 위의 while문 반복이 종료됐다.
    # 기업명과 공고명 변수에는 정제까지 완료된 올바른 값들이 저장된 상태이다.
    # 파일명 중복검사를 거친 후 pdf로 저장하기만 하면 모든 작업 끝!

    i = 1  # 파일명 중복시 파일 뒤에 붙일 숫자
    if f"{company_name}_{gongo_title}.pdf" in os.listdir():  # 만약 동일명의 파일이 기존에 만들어져 있으면
        while f"{company_name}_{gongo_title}_{i}.pdf" in os.listdir():  # "공고명"을 "공고명_1"로 바꿔보고 그래도 있으면
            i += 1  # "공고명_2", "공고명_3" 등, 없는 숫자가 나올 때까지 반복
        gongo_title = f"{gongo_title}_{i}"  # 없는 숫자 i로 공고명 최종 변경 완료

    # 중복검사도 끝났따! pdf 저장하고 끝내자.
    hwp.save_as(f"{company_name}_{gongo_title}.pdf", format="PDF")  # (저장포맷은 무조건 대문자)
    print("완료!")

finally:  # 만약 중간에 어떤 오류가 발생하더라도(심지어 Ctrl-C로 직접종료하는 경우에도)
    # 아래 두 줄 코드는 무조건 실행한다. (물론 오류가 발생하지 않더라도 꼭 실행한다는 의미임!)
    hwp.clear()  # 현재 열려 있는 문서의 변경사항 버리고 파일 닫기
    hwp.quit()  # 한/글 프로그램도 종료하기. 끝!
