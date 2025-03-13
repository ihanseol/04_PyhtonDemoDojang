import pyautogui

from pyhwpx import Hwp
from FileProcessing_V4_20250211 import FileBase
import os
import time


# function OnScriptMacro_그림지우기()
# {
# 	HAction.GetDefault("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
# 	with (HParameterSet.HDeleteCtrls)
# 	{
# 		CreateItemArray("DeleteCtrlType", 1);
# 		DeleteCtrlType.Item(0) = 10;
# 	}
# 	HAction.Execute("DeleteCtrls", HParameterSet.HDeleteCtrls.HSet);
# }


def delete_images(hwp):
    pset = hwp.HParameterSet.HDeleteCtrls.HSet
    hwp.HAction.GetDefault("DeleteCtrls", pset)
    hwp.HParameterSet.HDeleteCtrls.CreateItemArray("DeleteCtrlType", 1)
    hwp.HParameterSet.HDeleteCtrls.DeleteCtrlType.SetItem(1, 10)
    hwp.HAction.Execute("DeleteCtrls", pset)
    hwp.Save()


def main():
    fb = FileBase()

    hwp_list = fb.get_file_filter('d:\\05_Send\\', "*.hwpx")
    print(hwp_list)

    hwp = Hwp(True)

    for file in hwp_list:
        hwp.open(file)
        print(f"file : {file}")
        # delete_images(hwp)
        pyautogui.hotkey('alt','shift', '8')
        time.sleep(1)
        hwp.Save()
        hwp.close()
    hwp.quit()


if __name__ == "__main__":
    main()
