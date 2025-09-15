#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
EasyGUI 사용법 예시 모음
설치: pip install easygui
"""

import easygui

def example_msgbox():
    """메시지 박스 예시"""
    print("1. 메시지 박스 예시")
    
    # 기본 메시지 박스
    easygui.msgbox("안녕하세요! 이것은 기본 메시지 박스입니다.")
    
    # 제목과 메시지가 있는 박스
    easygui.msgbox("이것은 커스텀 메시지입니다.", "커스텀 제목")
    
    # 긴 메시지
    long_msg = """이것은 긴 메시지입니다.
    여러 줄로 나누어진 텍스트를
    표시할 수 있습니다.
    
    공백 줄도 포함할 수 있습니다."""
    easygui.msgbox(long_msg, "긴 메시지 예시")


def example_buttons():
    """버튼 선택 예시"""
    print("2. 버튼 선택 예시")
    
    # 확인/취소 선택
    if easygui.ccbox("계속하시겠습니까?", "확인"):
        print("사용자가 '확인'을 선택했습니다.")
    else:
        print("사용자가 '취소'를 선택했습니다.")
    
    # 예/아니오 선택
    if easygui.ynbox("저장하시겠습니까?", "저장 확인"):
        print("사용자가 '예'를 선택했습니다.")
    else:
        print("사용자가 '아니오'를 선택했습니다.")
    
    # 커스텀 버튼들
    choice = easygui.buttonbox("어떤 작업을 하시겠습니까?", 
                              "작업 선택",
                              ["새로 만들기", "열기", "저장", "종료"])
    print(f"사용자 선택: {choice}")


def example_input():
    """입력 받기 예시"""
    print("3. 입력 받기 예시")
    
    # 문자열 입력
    name = easygui.enterbox("이름을 입력하세요:", "이름 입력")
    if name:
        print(f"입력된 이름: {name}")
    
    # 기본값이 있는 입력
    email = easygui.enterbox("이메일을 입력하세요:", 
                            "이메일 입력", 
                            default="user@example.com")
    if email:
        print(f"입력된 이메일: {email}")
    
    # 비밀번호 입력 (마스킹)
    password = easygui.passwordbox("비밀번호를 입력하세요:", "비밀번호 입력")
    if password:
        print(f"비밀번호 길이: {len(password)} 글자")


def example_integer():
    """정수 입력 예시"""
    print("4. 정수 입력 예시")
    
    # 정수 입력
    age = easygui.integerbox("나이를 입력하세요:", "나이 입력", 
                            default=25, lowerbound=0, upperbound=150)
    if age is not None:
        print(f"입력된 나이: {age}")
    
    # 범위 제한 없는 정수
    number = easygui.integerbox("숫자를 입력하세요:", "숫자 입력")
    if number is not None:
        print(f"입력된 숫자: {number}")


def example_choice():
    """선택 목록 예시"""
    print("5. 선택 목록 예시")
    
    # 단일 선택
    colors = ["빨강", "파랑", "초록", "노랑", "보라"]
    color = easygui.choicebox("좋아하는 색을 선택하세요:", 
                             "색상 선택", colors)
    if color:
        print(f"선택된 색상: {color}")
    
    # 다중 선택
    fruits = ["사과", "바나나", "오렌지", "포도", "딸기", "수박"]
    selected_fruits = easygui.multchoicebox("좋아하는 과일들을 선택하세요:", 
                                           "과일 선택", fruits)
    if selected_fruits:
        print(f"선택된 과일들: {selected_fruits}")


def example_file_operations():
    """파일 관련 예시"""
    print("6. 파일 관련 예시")
    
    # 파일 열기
    filename = easygui.fileopenbox("파일을 선택하세요:", "파일 열기")
    if filename:
        print(f"선택된 파일: {filename}")
    
    # 특정 확장자 파일만 선택
    image_file = easygui.fileopenbox("이미지 파일을 선택하세요:", 
                                   "이미지 열기",
                                   filetypes=["*.jpg", "*.png", "*.gif", "*.bmp"])
    if image_file:
        print(f"선택된 이미지: {image_file}")
    
    # 파일 저장
    save_filename = easygui.filesavebox("저장할 파일명을 입력하세요:", 
                                       "파일 저장", 
                                       default="untitled.txt")
    if save_filename:
        print(f"저장할 파일: {save_filename}")
    
    # 디렉토리 선택
    directory = easygui.diropenbox("디렉토리를 선택하세요:", "디렉토리 선택")
    if directory:
        print(f"선택된 디렉토리: {directory}")


def example_text_display():
    """텍스트 표시 예시"""
    print("7. 텍스트 표시 예시")
    
    # 긴 텍스트 표시 (스크롤 가능)
    long_text = """이것은 매우 긴 텍스트입니다.
여러 줄로 구성되어 있으며,
사용자는 스크롤해서 전체 내용을 볼 수 있습니다.

이런 식으로 파일 내용이나
긴 설명을 보여줄 때 유용합니다.

더 많은 내용...
더 많은 내용...
더 많은 내용...

마지막 줄입니다."""
    
    easygui.textbox("긴 텍스트 표시", "텍스트 뷰어", long_text)


def example_code_display():
    """코드 표시 예시"""
    print("8. 코드 표시 예시")
    
    # 코드 내용 (등폭 폰트로 표시)
    code_content = '''def hello_world():
    """간단한 함수 예시"""
    print("Hello, World!")
    
    for i in range(5):
        print(f"Count: {i}")
    
    return "완료"

# 함수 호출
result = hello_world()
print(result)'''
    
    easygui.codebox("파이썬 코드 예시", "코드 뷰어", code_content)


def example_multiform():
    """다중 필드 입력 예시"""
    print("9. 다중 필드 입력 예시")
    
    # 여러 필드를 한 번에 입력받기
    msg = "사용자 정보를 입력하세요:"
    title = "사용자 등록"
    fieldNames = ["이름", "이메일", "전화번호", "주소"]
    fieldValues = ["", "user@example.com", "010-1234-5678", "서울시"]
    
    fieldValues = easygui.multenterbox(msg, title, fieldNames, fieldValues)
    
    if fieldValues:
        print("입력된 정보:")
        for i, field in enumerate(fieldNames):
            print(f"{field}: {fieldValues[i]}")
    else:
        print("사용자가 취소했습니다.")


def example_multpassword():
    """다중 비밀번호 입력 예시"""
    print("10. 다중 비밀번호 입력 예시")
    
    msg = "로그인 정보를 입력하세요:"
    title = "로그인"
    fieldNames = ["사용자명", "비밀번호"]
    fieldValues = ["admin", ""]
    
    # 두 번째 필드(비밀번호)를 마스킹
    values = easygui.multpasswordbox(msg, title, fieldNames, fieldValues)
    
    if values:
        print(f"사용자명: {values[0]}")
        print(f"비밀번호 길이: {len(values[1])} 글자")


def example_exception_handling():
    """예외 처리 예시"""
    print("11. 예외 처리 예시")
    
    try:
        # 사용자가 취소하거나 ESC를 누를 경우를 처리
        name = easygui.enterbox("이름을 입력하세요 (취소 가능):", "이름 입력")
        
        if name is None:
            print("사용자가 취소했습니다.")
        elif name.strip() == "":
            print("빈 문자열이 입력되었습니다.")
        else:
            print(f"입력된 이름: {name}")
            
    except Exception as e:
        print(f"오류 발생: {e}")


def run_all_examples():
    """모든 예시 실행"""
    print("EasyGUI 예시 프로그램을 시작합니다...\n")
    
    # 사용자에게 실행할 예시 선택
    examples = [
        "메시지 박스",
        "버튼 선택",
        "입력 받기",
        "정수 입력",
        "선택 목록",
        "파일 관련",
        "텍스트 표시",
        "코드 표시",
        "다중 필드 입력",
        "다중 비밀번호",
        "예외 처리",
        "모든 예시 실행"
    ]
    
    choice = easygui.choicebox("실행할 예시를 선택하세요:", 
                              "EasyGUI 예시", examples)
    
    if choice:
        if choice == "메시지 박스":
            example_msgbox()
        elif choice == "버튼 선택":
            example_buttons()
        elif choice == "입력 받기":
            example_input()
        elif choice == "정수 입력":
            example_integer()
        elif choice == "선택 목록":
            example_choice()
        elif choice == "파일 관련":
            example_file_operations()
        elif choice == "텍스트 표시":
            example_text_display()
        elif choice == "코드 표시":
            example_code_display()
        elif choice == "다중 필드 입력":
            example_multiform()
        elif choice == "다중 비밀번호":
            example_multpassword()
        elif choice == "예외 처리":
            example_exception_handling()
        elif choice == "모든 예시 실행":
            example_msgbox()
            example_buttons()
            example_input()
            example_integer()
            example_choice()
            example_file_operations()
            example_text_display()
            example_code_display()
            example_multiform()
            example_multpassword()
            example_exception_handling()
    
    print("\n예시 실행이 완료되었습니다.")


if __name__ == "__main__":
    # EasyGUI 설치 확인
    try:
        import easygui
        run_all_examples()
    except ImportError:
        print("EasyGUI가 설치되지 않았습니다.")
        print("다음 명령어로 설치하세요: pip install easygui")
