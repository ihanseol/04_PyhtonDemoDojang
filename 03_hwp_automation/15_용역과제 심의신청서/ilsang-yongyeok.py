"""
누름틀 및 필드가 매겨져 있지 않은 한/글 문서를 취합할 때에는
별 수 없이 본문 좌표나 표의 셀을 직접 탐색해야 합니다.
다만, 모든 취합문서의 포맷(표나 셀 갯수 등)이 동일한 조건이라면
필드를 통한 작업과 크게 별다르지 않게
엑셀문서로 취합할 수 있습니다.
이번 영상은 필드가 매겨져 있지 않은 예제를 들어
한/글 표를 탐색하는 과정부터 엑셀로의 취합,
그리고 pyinstaller를 통한 컴파일 과정까지 
실시간으로 진행해보는
약 50분 분량의 라이브코딩 영상입니다.

파이썬의 기본문법 중에서는 문자열메서드인 strip, split 및
리스트 컴프리헨션 등이 사용되었습니다.
"""

import os
from tkinter.filedialog import askopenfilenames

import win32com.client as win32


# 선택한 셀의 텍스트 추출하는 함수
def get_text():
    hwp.InitScan(Range=0xff)
    total_text = ""
    state = 2
    while state not in [0, 1]:
        state, text = hwp.GetText()
        total_text += text
    hwp.ReleaseScan()
    return total_text


# 파일목록 선택하기
filelist = askopenfilenames(title="취합할 아래아한글 파일을 선택해주세요.",
                            initialdir=os.getcwd(),
                            filetypes=[("아래아한글파일", "*.hwp *.hwpx")])

# 아래아한글 실행
hwp = win32.gencache.EnsureDispatch("hwpframe.hwpobject")
hwp.XHwpWindows.Item(0).Visible = True
hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")

# 엑셀 실행
excel = win32.gencache.EnsureDispatch("Excel.Application")
wb = excel.Workbooks.Open(r"C:\Users\smj02\Desktop\통합 문서1.xlsx")
ws = wb.Worksheets(1)
excel.Visible = True

# 선택한 아래아한글을 하나씩 순회하면서
for file in filelist:
    hwp.Open(file)  # 한/글 문서를 열고

    # 첫 번째 표를 탐색
    ctrl = hwp.HeadCtrl
    while ctrl:
        if ctrl.CtrlID == "tbl":
            hwp.SetPosBySet(ctrl.GetAnchorPos(0))
            break
        else:
            ctrl = ctrl.Next

    # 찾아낸 첫 번째 표 안에 진입(A1셀 선택상태)
    hwp.FindCtrl()
    hwp.Run("ShapeObjTableSelCell")

    # 전체 셀의 각각의 값을 파이썬 리스트로 추출
    contents = []
    contents.append(get_text())  # 첫 번째 셀 값 넣어주고 나서
    while hwp.HAction.Run("TableRightCell"):
        contents.append(get_text())  # 우측으로 이동하면서 모든 셀 값 추출

    # contents 리스트 중 엑셀로 옮길 값만 추출
    과제명 = contents[1]
    신청부서 = contents[3].split("\r\n")[0].replace("/", "")
    과제담당관 = contents[3].split("\r\n")[1].replace("/", "")
    담당공무원 = contents[5]

    연구방식_ = ["위탁형", "공동연구형", "자문형"]
    연구방식 = [i.strip() for i in contents[7].split("(")][1:]
    for idx, text in enumerate(연구방식):
        if not text.startswith(")"):
            연구방식 = 연구방식_[idx]
            break

    연구시작 = contents[9].split("~")[0].strip()
    연구종료 = contents[9].split("~")[1].split("(")[0].strip()
    연구기간 = contents[9].split("(")[1].replace(")", "")

    예산항목_ = ["포괄", "사업별"]
    예산항목 = [i.strip() for i in contents[12].split("(")[1:]]
    for idx, text in enumerate(예산항목):
        if text.startswith(")"):
            pass
        else:
            예산항목 = 예산항목_[idx]

    예상금액 = contents[15]
    연구필요성 = contents[17]
    중복검토방법 = contents[21].split("\r\n")[1].replace("-", "").strip()
    
    중복성여부_ = ["있다", "없다"]
    중복성여부 = [i.strip() for i in contents[21].split("\r\n")[2].split("(")][1:]
    for idx, text in enumerate(중복성여부):
        if not text.startswith(")"):
            중복성여부 = 중복성여부_[idx]
    
    연구내용 = contents[23]
    연구결과활용방안 = contents[25]

    # 추출한 값들을 엑셀파일에 입력
    입력행 = len(ws.UsedRange()) + 1  # 추가할 행번호 계산
    ws.Range(ws.Cells(입력행, 1), ws.Cells(입력행, 15)).Value = (
        과제명, 신청부서, 과제담당관, 담당공무원, 연구방식, 연구시작, 연구종료, 연구기간, 예산항목, 예상금액,
        연구필요성, 중복검토방법, 중복성여부, 연구내용, 연구결과활용방안
    )

# 모든 한/글 문서의 순회를 마쳤으면 
wb.Save()  # 엑셀파일 저장
hwp.Clear()  # 한/글 프로그램 비우기
hwp.Quit()  # 한/글 프로그램 종료