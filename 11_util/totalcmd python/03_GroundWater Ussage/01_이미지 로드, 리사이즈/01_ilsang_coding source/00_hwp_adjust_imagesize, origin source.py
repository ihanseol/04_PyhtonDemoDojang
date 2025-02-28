from tkinter import Tk  # GUI로 파일 선택하기 위한 모듈
from tkinter.filedialog import askopenfilename  # 파일선택창

import win32com.client as win32  # 한/글 열기 위한 모듈


def hwp_init(filename):  # 한/글 여는 코드가 길어서 미리 만들어둠
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")  # 한/글 객체 생성
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")  # 보안모듈 실행
    hwp.Open(filename)  # GUI에서 선택한 파일 열기
    hwp.XHwpWindows.Item(0).Visible = True  # 한/글 창 숨김해제(초기에는 백그라운드상태)
    # hwp.HAction.Run("FrameFullScreen")  # 전체화면
    return hwp  # hwp객체 리턴


def Hwp유닛을_밀리미터로(HWP유닛):  # MiliToHwpUnit메서드의 반대. 계산 귀찮아서 만들어둠.
    return HWP유닛 / 7200 * 25.4  # 1 inch = 7200 HWPUNIT, 1mm = 283.465 HWPUNIT


def ctrl로_이동하기(ctrl):  # 그리기객체나 표 등 컨트롤 오브젝트로 이동하는 함수
    위치세트 = ctrl.GetAnchorPos(0)  # 현재 선택된 컨트롤의 위치파라미터 추출
    위치 = (위치세트.Item("List"), 위치세트.Item("Para"), 위치세트.Item("Pos"))  # 튜플로 변환
    hwp.SetPos(*위치)  # 해당 위치로 커서(캐럿) 이동


def 캡션복사():
    hwp.HAction.Run("ShapeObjCaption")
    hwp.HAction.Run("SelectAll")
    hwp.HAction.Run("Copy")
    hwp.HAction.Run("CloseEx")


def 사이즈조정():
    hwp.FindCtrl()  # 해당 객체 선택
    이미지액션 = hwp.CreateAction("ShapeObjDialog")  # 이미지수정액선 실행준비
    이미지세트 = 이미지액션.CreateSet()  # 이미지수정을 위한 파라미터 배열(비어있음) 생성
    이미지액션.GetDefault(이미지세트)  # 빈 파라미터 배열에 현재문서의 값을 채워넣음
    기존너비 = Hwp유닛을_밀리미터로(이미지세트.Item("Width"))  # 선택 이미지의 현재너비 저장
    기존높이 = Hwp유닛을_밀리미터로(이미지세트.Item("Height"))  # 선택 이미지의 현재높이 저장
    변경쪽너비 = 종이너비 - 좌측여백 - 우측여백 - (0 if 제본타입 == 2 else 제본여백)  # 변경할 쪽너비 계산
    파라미터셋 = 이미지세트.CreateItemSet("ShapeObject", "ShapeObject")  # 이미지 수정을 위한 파라미터셋 생성
    파라미터셋.SetItem("Width", hwp.MiliToHwpUnit(변경쪽너비))  # 이미지너비 변경값 입력
    파라미터셋.SetItem("Height", hwp.MiliToHwpUnit(기존높이 * 변경쪽너비 / 기존너비))  # 이미지높이 변경값 입력
    이미지액션.Execute(파라미터셋)  # 입력한 값 적용


def 캡션붙여넣기():
    hwp.HAction.Run("ShapeObjCaption")
    hwp.HAction.Run("SelectAll")
    hwp.HAction.Run("Paste")
    hwp.HAction.Run("CloseEx")


if __name__ == '__main__':  # 메인함수 파트
    root = Tk()  # GUI(그래픽 유저 인터페이스) 인스턴스 생성
    filename = askopenfilename()  # 파일열기창 실행
    root.destroy()  # 파일선택 후 tkinter 종료
    hwp = hwp_init(filename=filename)  # 위에서 정의한 한/글 열기 함수
    페이지액션 = hwp.CreateAction("PageSetup")  # 페이지셋업 액션 실행준비
    페이지세트 = 페이지액션.CreateSet()  # 페이지 설정을 위한 파라미터 배열(비어있음) 생성
    페이지액션.GetDefault(페이지세트)  # 파라미터에 현재문서의 값을 채워넣음
    종이너비 = Hwp유닛을_밀리미터로(페이지세트.Item("PageDef").Item("PaperWidth"))  # 채워넣은 값 중 종이너비
    좌측여백 = Hwp유닛을_밀리미터로(페이지세트.Item("PageDef").Item("LeftMargin"))  # 채워넣은 값 중 좌측여백
    우측여백 = Hwp유닛을_밀리미터로(페이지세트.Item("PageDef").Item("RightMargin"))  # 채워넣은 값 중 우측여백
    제본여백 = Hwp유닛을_밀리미터로(페이지세트.Item("PageDef").Item("GutterLen"))  # 채워넣은 값 중 제본여백
    제본타입 = Hwp유닛을_밀리미터로(페이지세트.Item("PageDef").Item("GutterType"))  # 0:한쪽, 1:맞쪽, 2: 위쪽

    ctrl = hwp.HeadCtrl  # 문서 중 첫번째 컨트롤 선택
    while ctrl != None:  # 마지막 컨트롤까지 순회할 것.
        if ctrl.CtrlID == "gso":  # 컨트롤아이디가 그리기객체(gso)이면
            ctrl로_이동하기(ctrl)  # 위에서 정의한 이동함수
            캡션복사()
            사이즈조정()
            캡션붙여넣기()
        else:  # 컨트롤아이디가 그리기객체가 아니면
            pass  # 그냥 넘어가기
        ctrl = ctrl.Next  # 다음 컨트롤로 이동