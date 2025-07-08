import time
import os
from FileManger_V0_20250406 import FileBase
from pyhwpx import Hwp

XL_BASE = "d:\\05_Send"


def get_desktop():
    desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
    return desktop


def EraseTableShade(hwp):
    pset = hwp.HParameterSet.HCellBorderFill
    hwp.HAction.GetDefault("NoneTableCellShade", pset.HSet)
    pset.FillAttr.type = hwp.BrushType("NullBrush|WinBrush")
    hwp.HAction.Execute("NoneTableCellShade", pset.HSet)
    hwp.HAction.Run("Cancel")


def countdown(n):
    print(' Please Move the Command Window to Side ! ')
    while n > 0:
        print(n)
        time.sleep(1)
        n -= 1
    print("Time's up!")


def hwp_py_func():
    hwp = Hwp()
    hwp.clipboard_to_pyfunc()


def exam_table_search(hwp, n="", startrow=0):
    """
        한/글 문서의 idx번째 표를 현재 폴더에 filename으로 csv포맷으로 저장한다.
        filename을 지정하지 않는 경우 "./result.csv"가 기본값이다.
    """
    start_pos = hwp.GetPos()
    table_list = []

    for ctrl in hwp.ctrl_list:
        if ctrl.UserDesc == "표":
            table_list.append(ctrl)

    for ctrl in table_list:
        hwp.set_pos_by_set(ctrl.GetAnchorPos(0))
        hwp.FindCtrl()
        hwp.ShapeObjTableSelCell()
        hwp.TableCellBlock()  # 셀블록
        hwp.TableCellBlockExtend()  # 셀블록 확장
        hwp.TableCellBlockExtend()  # 전체 셀 선택
        EraseTableShade(hwp)
        # hwp.run_script_macro("OnScriptMacro_배경색지우기")

    return None


def main1():
    hwp_py_func()


def main():
    hwp = Hwp(visible=True)
    fb = FileBase()

    hwp_files = fb.get_file_filter(XL_BASE)
    print(hwp_files[0])
    hwp.open(hwp_files[0])
    exam_table_search(hwp)
    hwp.save()
    hwp.close()


if __name__ == "__main__":
    # main1()
    main()
