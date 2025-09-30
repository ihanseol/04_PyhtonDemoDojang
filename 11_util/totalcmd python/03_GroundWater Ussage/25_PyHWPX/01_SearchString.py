from pyhwpx import Hwp

hwp = Hwp()

hwp.MoveDocBegin()
while hwp.find(r"\(.*?\)", regex=True, UseWildCards=False):
    hwp.set_font(ShadeColor="Yellow", TextColor="Red")

hwp.MoveDocBegin()
while hwp.find("("):
    # spos = hwp.get_pos()
    spos = hwp.get_selected_pos()[1:4]
    hwp.find(")")
    epos = hwp.get_pos()

    # data like this
    #(True, 0, 1, 2, 0, 3, 4)
    # 0, 문단번호, 글자오프셋
    # 0, 1, 2 --> 시작위치의 구역
    # 0, 3, 4 --> 끝위치의 구역

    hwp.select_text_by_get_pos(spos, epos)
    hwp.set_font(ShadeColor="Yellow", TextColor="Red")
    hwp.Cancel()


hwp.MoveDocBegin()
while hwp.find("("):
    # spos = hwp.get_pos()
    spos = hwp.get_selected_pos()[4:]
    hwp.find(")")
    epos = hwp.get_selected_pos()[1:4]

    # data like this
    #(True, 0, 1, 2, 0, 3, 4)
    # 0, 문단번호, 글자오프셋
    # 0, 1, 2 --> 시작위치의 구역
    # 0, 3, 4 --> 끝위치의 구역

    hwp.select_text_by_get_pos(spos, epos)
    hwp.set_font(TextColor="Purple")
    hwp.Cancel()






