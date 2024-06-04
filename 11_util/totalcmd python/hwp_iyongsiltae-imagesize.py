from hwpapi.core import App
import os
import FileProcessing_CLASS as fpc
import pyperclip

HWP_INPUT = "iyong_empty.hwp"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def hwpunit_to_milimeter(hwpunit):  # MiliToHwpUnit메서드의 반대. 계산 귀찮아서 만들어둠.
    return hwpunit / 7200 * 25.4  # 1 inch = 7200 HWPUNIT, 1mm = 283.465 HWPUNIT

def imagesize(hwp):
    hwp.FindCtrl()  # 해당 객체 선택
    image_action = hwp.CreateAction("ShapeObjDialog")  # 이미지수정액선 실행준비
    image_set = image_action.CreateSet()  # 이미지수정을 위한 파라미터 배열(비어있음) 생성
    image_action.GetDefault(image_set)  # 빈 파라미터 배열에 현재문서의 값을 채워넣음
    
    d_width = hwpunit_to_milimeter(image_set.Item("Width"))  # 선택 이미지의 현재너비 저장
    d_height = hwpunit_to_milimeter(image_set.Item("Height"))  # 선택 이미지의 현재높이 저장
    변경쪽너비 = 종이너비 - 좌측여백 - 우측여백 - (0 if 제본타입 == 2 else 제본여백)  # 변경할 쪽너비 계산
    
    parameter_set = image_set.CreateItemSet("ShapeObject", "ShapeObject")  # 이미지 수정을 위한 parameter_set 생성
    parameter_set.SetItem("Width", hwp.MiliToHwpUnit(변경쪽너비))  # 이미지너비 변경값 입력
    parameter_set.SetItem("Height", hwp.MiliToHwpUnit(d_height * 변경쪽너비 / d_width))  # 이미지높이 변경값 입력
    
    image_action.Execute(parameter_set)  # 입력한 값 적용
    


def initial_work():
    app = App(None, True)

    fp = fpc.FileProcessing()
    jpg_files = fp.get_jpg_files()

    print(jpg_files)
    return app, jpg_files


def initial_opencopy(app, jpg_files):
    desktop = get_desktop()
    app.open(f"{desktop}\\{HWP_INPUT}")
    hwp = app.api

    if jpg_files:
        for filename in jpg_files:
            hwp.InsertPicture(os.path.join(r"d:\05_Send", filename))
            hwp.MovePos(3)


def end_work(app):
    app.api.Save()
    app.quit()


def main():
    app: App
    app, jpg_files = initial_work()
    initial_opencopy(app, jpg_files)
    end_work(app)
    print('------------------------------------------------------')


if __name__ == "__main__":
    main()
