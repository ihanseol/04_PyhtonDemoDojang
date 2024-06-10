from pyhwpx import Hwp
import os

HWP_INPUT = "iyong_empty.hwp"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def load_image_from_send(hwp):
    jpg_files = [f for f in os.listdir("d:\\05_Send\\") if f.endswith('.jpg')]
    print(jpg_files)

    print('-' * 80)
    if jpg_files:
        for fname in jpg_files:
            hwp.InsertPicture(os.path.join(r"d:\05_Send", fname), True, 0)
            hwp.MovePos(3)
            print(fname)
    print('-' * 80)


def open_and_pagesetup(hwp):
    my_page = {'아래쪽': 13, '꼬리말': 5, '제본여백': 0, '제본타입': 0, '머리말': 5, '용지방향': 0, '왼쪽': 27,
               '용지길이': 297, '용지폭': 210, '오른쪽': 16, '위쪽': 25}

    open_result = hwp.open(f"{HWP_INPUT}")
    hwp.set_pagedef(my_page, "cur")
    print(my_page)


def main():
    hwp = Hwp(visible=False)

    open_and_pagesetup(hwp)
    load_image_from_send(hwp)

    hwp.save_as("d:/05_Send/iyong_empty_complete.hwp")
    hwp.quit()


if __name__ == "__main__":
    main()
