# https://youtu.be/F3snEXUDCEU
# [아래한글 자동화] 필드를 활용한 "방과후프로그램출석부" 자동 제작 AtoZ
#
# 표에, 칸을 죽선택 p, Ctrl+N,K
#
# pip install pyinstaller
# pyinstaller -F --add-binary="FilePathCheckerModule.dll:."  filename.py
# deactivate
# python -m venv venv
# 가상환경 만들고, pyinstaller, pyhwpx, filepathchecker.dll 이렇게만 넣어두고
# 빌드 해주면, 파일사이즈가 최적이 된다.


def Test_original():
    from pyhwpx import Hwp
    import pandas as pd

    hwp = Hwp()

    df = pd.read_excel(r"d:\05_Send\pythonProject\03_GroundWater Ussage\25_PyHWPX\name.xlsx")
    print(df)

    # 데이타 프레임에서 농구왕이라는 행들만 추려서 가져오기

    # df[df["프로그램명"] == "내일은 축구왕"]
    # print(df[df["프로그램명"].str.endswith("축구왕")])
    # print(df[df["프로그램명"].str.contains("농구")])

    hwp.open(r"c:\Users\minhwasoo\Documents\출석부.hwp")

    hwp.put_field_text(
        df[df["프로그램명"] == '내일은 농구왕']
    )

    print(len(df[df["프로그램명"] == '내일은 농구왕']))

    hwp.put_field_text("연번", list(range(1, len(df[df["프로그램명"] == '내일은 농구왕']) + 1)))

    print(df["프로그램명"].iloc[0])

    # hwp.save_as(f"{df["프로그램명"].iloc[0]}.hwp")

    hwp.save_as(f"{df[df['프로그램명'] == '내일은 농구왕']['프로그램명'].iloc[0]}.hwp")

    print(df[df["프로그램명"] == '내일은 농구왕'])
    print(len(df[df["프로그램명"] == '내일은 농구왕']))
    print(df[df["프로그램명"] == '내일은 농구왕']["프로그램명"].iloc[0])

    for i in df["프로그램명"].unique():
        print(i)

    print(df["프로그램명"])


# 이셀 안에서 다 끝내버리겠다.!!!
def test01():
    from pyhwpx import Hwp
    import pandas as pd
    from tkinter.filedialog import askopenfilename

    hwp = Hwp()

    xlsx = askopenfilename(title="학생명단 엑셀파일을 선택해주세요")
    hwpx = askopenfilename(title="출석부 서식 한글파일을  선택해주세요")

    df = pd.read_excel(xlsx)
    print(df)

    for cat in df["프로그램명"].unique():
        hwp.open(hwpx)
        df_cat = df[df["프로그램명"] == cat]
        hwp.put_field_text(df_cat)
        hwp.put_field_text("연번", list(range(1, len(df_cat) + 1)))
        hwp.save_as(f"방과후프로그램출석부_{cat}.hwp")
        hwp.clear()

    hwp.msgbox("작업이 완료 되었습니다.")
    hwp.quit()
