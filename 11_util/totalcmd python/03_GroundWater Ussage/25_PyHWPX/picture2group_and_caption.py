# https://youtu.be/-frQQX_zs_0

# N개의 그림을 2개씩 Select한후 "개체묶기" 후 캡션 입력
# 과정을 N개 그림 반복하려고 하는데 개체 묶기 커맨드만 알면 나머지는 가능해 보이는데,
# 개체 묶기 커맨드가 있을까 ?, 이것은 녹화가 안됨

# 그림을 묶으려면 그림을 선택해야 하는데 마우스로만 선택되지 않나요 ?


# 매크로녹화
# 미리 그림 두개를 선택을 한뒤
# 다음에 메크로 녹화를 해준다.


# 마우스 우클릭 - Shift+F10 으로 대체해준다.
# pip install --upgrade pyhwpx
#

import pyhwpx
from pyhwpx import Hwp

hwp = Hwp()
# print(pyhwpx.__version__)
# 레코드 녹화 해결

# hwp.HAction.Run("ShapeObjGroup")
# hwp.ShapeObjGroup()

co = hwp.current_page
cl = hwp.ctrl_list
print(cl)

img_list = [i for i in hwp.ctrl_list if i.UserDesc == "그림"]
print(img_list)
print(len(img_list))

hwp.select_ctrl(img_list[:4])
hwp.select_ctrl(img_list[-1], option=0)
hwp.select_ctrl(img_list[3], option=0)

hwp.select_ctrl([img_list[0], img_list[1]])
hwp.select_ctrl([img_list[0], img_list[0].Next])

for i in img_list[::2]:
    hwp.select_ctrl([i, i.Next])
    hwp.ShapeObjGroup()


def test01():
    hwp.select_ctrl(hwp.LastCtrl)
    hwp.ShapeObjAttachCaption()
    hwp.SelectAll()
    hwp.Delete()
    hwp.insert_text("hello world")
    hwp.CloseEx()


def test02():
    hwp.ShapeObjAttachCaption(text="안녕하세용 반가워요")
    hwp.ShapeObjAttachCaption(text="안녕하세용 반가워요", add_num=False)


def test03():
    img_list_1 = [i for i in hwp.ctrl_list if i.UserDesc == "그림"]

    for idx, i in enumerate(img_list_1[::2], start=1):
        hwp.select_ctrl([i, i.Next])
        hwp.ShapeObjGroup()
        hwp.ShapeObjAttachCaption(text=f"{idx}번째 그룹", add_num=False)

    hwp.Cancel()



hwp.find_replace_all(r"(\d+번) 그룹개체입니다.",r"그룹개체 \1입니다.", regex=True)


