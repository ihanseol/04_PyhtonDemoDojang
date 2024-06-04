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


def main():
    load_image_from_send()


if __name__ == "__main__":
    main()
