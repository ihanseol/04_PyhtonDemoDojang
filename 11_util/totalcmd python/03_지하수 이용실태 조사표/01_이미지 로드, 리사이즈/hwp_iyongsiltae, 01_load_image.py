from hwpapi.core import App
import os
import FileProcessing_CLASS as fpc
import win32com.client as win32

HWP_INPUT = "iyong_empty.hwp"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def load_image_from_send():
    app = App(None, False)

    fp = fpc.FileProcessing()
    jpg_files = fp.get_jpg_files()
    print(jpg_files)

    desktop = get_desktop()
    app.open(f"{desktop}\\{HWP_INPUT}")
    hwp = app.api
    hwp.Run('SelectAll')
    hwp.Run("Delete")

    print('-'*60)
    if jpg_files:
        for fname in jpg_files:
            hwp.InsertPicture(os.path.join(r"d:\05_Send", fname), True, 0)
            hwp.MovePos(3)
            print(fname)
    print('-' * 60)

    hwp.Save()
    hwp.Run("FileQuit")

def save_s(hwp):
    pset = hwp.HParameterSet.HSaveAsImage
    hwp.HAction.GetDefault("PictureSaveAsAll", pset.HSet)
    hwp.HAction.Execute("PictureSaveAsAll", pset.HSet)

    hwp.HAction.GetDefault("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)  # 다른이름으로 저장 액션 생성
    hwp.HParameterSet.HFileOpenSave.filename = "C:\\Users\\minhwasoo\\Desktop\\iyong_empty_complete.hwp"
    # 원래파일명#페이지.hwp로 저장
    hwp.HParameterSet.HFileOpenSave.Format = "HWP"  # 포맷은 Native HWP
    hwp.HAction.Execute("FileSaveAs_S", hwp.HParameterSet.HFileOpenSave.HSet)  # 다른이름저장 실행



def main():
    load_image_from_send()


if __name__ == "__main__":
    main()
