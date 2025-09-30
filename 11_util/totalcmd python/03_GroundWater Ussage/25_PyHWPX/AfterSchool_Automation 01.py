# https://youtu.be/F3snEXUDCEU
# [아래한글 자동화] 필드를 활용한 "방과후프로그램출석부" 자동 제작 AtoZ


from pyhwpx import Hwp

hwp = Hwp()

hwp.insert_text("안녕하세요? 반갑습니다.")
hwp.BreakPara()
hwp.save_as("안녕하세요.hwpx")
hwp.quit()

hwp.open("안녕하세요.hwpx")
hwp.set_font(Height=40, FaceName="D2coding")

# 자동화의 핵심, 필드
#  입력 , 개체, 필드입력 , Ctrl+K,E
#

from pyhwpx import Hwp

hwp = Hwp()
hwp.put_field_text("name", "일코")

hwp.clear_field_text()

d = {
    "name": "일코",
    "age": "70",
    "hobby": "코딩",
    "spec": "오류"
}

hwp.put_field_text(d)

d = {
    "name": ["일코", "이코", "삼코", "사코", "오코"],
    "age": ["70", "30", "20", "10", "40"],
    "hobby": ["코딩", "김치", "당구", "영화", "주식"],
    "spec": ["오류", "전주", "서도", "연", "디버깅"]
}

hwp.put_field_text(d)

import pandas as pd
df = pd.DataFrame(d)

print(df)

hwp.clear_field_text()

hwp.put_field_text(df)
hwp.save()
hwp.quit()


