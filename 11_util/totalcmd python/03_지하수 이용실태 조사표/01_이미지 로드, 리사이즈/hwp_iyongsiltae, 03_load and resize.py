from hwpapi.core import App
import os
import FileProcessing_CLASS as fpc

HWP_INPUT = "iyong_empty.hwp"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def hwpunit_to_mili(hwpunit):  # MiliToHwpUnit메서드의 반대. 계산 귀찮아서 만들어둠.
    return hwpunit / 7200 * 25.4  # 1 inch = 7200 HWPUNIT, 1mm = 283.465 HWPUNIT


def ctrl_to_move(hwp, ctrl):  # 그리기객체나 표 등 컨트롤 오브젝트로 이동하는 함수
    position_set = ctrl.GetAnchorPos(0)  # 현재 선택된 컨트롤의 position파라미터 추출
    position = (position_set.Item("List"), position_set.Item("Para"), position_set.Item("Pos"))  # 튜플로 변환
    hwp.SetPos(*position)  # 해당 position로 커서(캐럿) 이동


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


def load_image_from_send(app):
    hwp = app.api
    fp = fpc.FileProcessing()
    jpg_files = fp.get_jpg_files()
    print(jpg_files)

    desktop = get_desktop()
    app.open(f"{desktop}\\{HWP_INPUT}")

    hwp.Run('SelectAll')
    hwp.Run("Delete")

    print('-' * 80)
    if jpg_files:
        for fname in jpg_files:
            hwp.InsertPicture(os.path.join(r"d:\05_Send", fname), True, 0)
            hwp.MovePos(3)
            print(fname)
    print('-' * 80)


def resize_image(hwp):
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
            image_size(hwp, paper_width, left_margin, right_margin, gutter_len, gutter_type)
            print(ctrl.CtrlID, i)
            i += 1
        else:  # 컨트롤아이디가 그리기객체가 아니면
            pass  # 그냥 넘어가기
        ctrl = ctrl.Next  # 다음 컨트롤로 이동


def main():
    app: App = App(None, False)
    hwp = app.api

    load_image_from_send(app)
    resize_image(hwp)

    hwp.Save()
    hwp.Run("FileQuit")


if __name__ == "__main__":
    main()
