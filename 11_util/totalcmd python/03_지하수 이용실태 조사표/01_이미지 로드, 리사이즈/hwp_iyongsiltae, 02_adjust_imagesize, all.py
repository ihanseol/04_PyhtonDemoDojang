from tkinter.filedialog import askopenfilename  # 파일선택창
import win32com.client as win32  # 한/글 열기 위한 모듈


def hwp_init(filename):  # 한/글 여는 코드가 길어서 미리 만들어둠
    hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")  # 한/글 객체 생성
    hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")  # 보안모듈 실행
    hwp.Open(filename)  # GUI에서 선택한 파일 열기
    hwp.XHwpWindows.Item(0).Visible = False  # 한/글 창 숨김해제(초기에는 백그라운드상태)
    # hwp.HAction.Run("FrameFullScreen")  # 전체화면
    return hwp  # hwp객체 리턴


def hwpunit_to_mili(hwpunit):  # MiliToHwpUnit메서드의 반대. 계산 귀찮아서 만들어둠.
    return hwpunit / 7200 * 25.4  # 1 inch = 7200 HWPUNIT, 1mm = 283.465 HWPUNIT


def ctrl_to_move(hwp, ctrl):  # 그리기객체나 표 등 컨트롤 오브젝트로 이동하는 함수
    position_set = ctrl.GetAnchorPos(0)  # 현재 선택된 컨트롤의 position파라미터 추출
    position = (position_set.Item("List"), position_set.Item("Para"), position_set.Item("Pos"))  # 튜플로 변환
    hwp.SetPos(*position)  # 해당 position로 커서(캐럿) 이동


def copy_caption(hwp):
    hwp.HAction.Run("ShapeObjCaption")
    hwp.HAction.Run("SelectAll")
    hwp.HAction.Run("Copy")
    hwp.HAction.Run("CloseEx")


def image_size(hwp, paper_width, left_margin, right_margin, gutter_len, gutter_type):
    hwp.FindCtrl()  # 해당 객체 선택
    image_action = hwp.CreateAction("ShapeObjDialog")  # 이미지수정액선 실행준비
    image_set = image_action.CreateSet()  # 이미지수정을 위한 파라미터 배열(비어있음) 생성
    image_action.GetDefault(image_set)  # 빈 파라미터 배열에 현재문서의 값을 채워넣음
    p_width = hwpunit_to_mili(image_set.Item("Width"))  # 선택 이미지의 현재너비 저장
    p_height = hwpunit_to_mili(image_set.Item("Height"))  # 선택 이미지의 현재높이 저장
    after_width = paper_width - left_margin - right_margin - (0 if gutter_type == 2 else gutter_len)  # 변경할 쪽너비 계산
    pset = image_set.CreateItemSet("ShapeObject", "ShapeObject")  # 이미지 수정을 위한 pset 생성
    pset.SetItem("Width", hwp.MiliToHwpUnit(after_width))  # 이미지너비 변경값 입력
    pset.SetItem("Height", hwp.MiliToHwpUnit(p_height * after_width / p_width))  # 이미지높이 변경값 입력
    image_action.Execute(pset)  # 입력한 값 적용


def paste_caption(hwp):
    hwp.HAction.Run("ShapeObjCaption")
    hwp.HAction.Run("SelectAll")
    hwp.HAction.Run("Paste")
    hwp.HAction.Run("CloseEx")


def main():
    # root = Tk()  # GUI(그래픽 유저 인터페이스) 인스턴스 생성
    filename = askopenfilename()  # 파일열기창 실행
    # root.destroy()  # 파일선택 후 tkinter 종료

    hwp = hwp_init(filename=filename)  # 위에서 정의한 한/글 열기 함수

    page_action = hwp.CreateAction("PageSetup")  # 페이지셋업 액션 실행준비
    page_set = page_action.CreateSet()  # 페이지 설정을 위한 파라미터 배열(비어있음) 생성
    page_action.GetDefault(page_set)  # 파라미터에 현재문서의 값을 채워넣음

    paper_width = hwpunit_to_mili(page_set.Item("PageDef").Item("PaperWidth"))  # 채워넣은 값 중 paper_width
    left_margin = hwpunit_to_mili(page_set.Item("PageDef").Item("LeftMargin"))  # 채워넣은 값 중 left_margin
    right_margin = hwpunit_to_mili(page_set.Item("PageDef").Item("RightMargin"))  # 채워넣은 값 중 right_margin
    gutter_len = hwpunit_to_mili(page_set.Item("PageDef").Item("GutterLen"))  # 채워넣은 값 중 gutter_len
    gutter_type = hwpunit_to_mili(page_set.Item("PageDef").Item("GutterType"))  # 0:한쪽, 1:맞쪽, 2: 위쪽

    print('-' * 80)
    i = 0
    ctrl = hwp.HeadCtrl  # 문서 중 첫번째 컨트롤 선택
    while ctrl:  # 마지막 컨트롤까지 순회할 것.
        if ctrl.CtrlID == "gso":  # 컨트롤아이디가 그리기객체(gso)이면
            ctrl_to_move(hwp, ctrl)  # 위에서 정의한 이동함수
            # copy_caption(hwp)
            image_size(hwp, paper_width, left_margin, right_margin, gutter_len, gutter_type)
            print(ctrl.CtrlID, i)
            i += 1
            # paste_caption(hwp)
        else:  # 컨트롤아이디가 그리기객체가 아니면
            pass  # 그냥 넘어가기
        ctrl = ctrl.Next  # 다음 컨트롤로 이동

    hwp.Save()
    hwp.Run("FileQuit")


if __name__ == '__main__':  # 메인함수 파트
    main()
