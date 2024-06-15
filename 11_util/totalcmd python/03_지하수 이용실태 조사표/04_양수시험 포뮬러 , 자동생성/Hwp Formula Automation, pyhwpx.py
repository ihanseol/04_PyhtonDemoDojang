import time
from pyhwpx import Hwp
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import messagebox

FORMULA_SOURCE = "d:\\05_Send\\YangSoo.csv"


def Write_Formula(formula_string):
    pyautogui.keyDown('ctrl')
    pyautogui.press('n')
    pyautogui.press('m')
    pyautogui.keyUp('ctrl')

    pyperclip.copy(formula_string)
    pyautogui.hotkey('ctrl', 'v')

    pyautogui.hotkey('shift', 'esc')
    time.sleep(1)

    pyautogui.press('enter')


def MyMessageBox(message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Notice", message)


"""
    function OnScriptMacro_줄간격()
    {
        HAction.Run("SelectAll");
        HAction.GetDefault("ParagraphShape", HParameterSet.HParaShape.HSet);
        with (HParameterSet.HParaShape)
        {
            LineSpacing = 300;
        }
        HAction.Execute("ParagraphShape", HParameterSet.HParaShape.HSet);
        HAction.Run("Cancel");
    }

"""


def OnScriptMacro_LineSpacing(hwp, spacing):
    pset = hwp.HParameterSet.HParaShape
    hwp.HAction.GetDefault("ParagraphShape", pset.HSet)
    pset.LineSpacing = spacing

    hwp.HAction.Execute("ParagraphShape", pset.HSet)
    hwp.HAction.Run("Cancel")


def main():
    try:
        with open(FORMULA_SOURCE, 'r', encoding='cp949') as file:
            hwp = Hwp(visible=True)
            for line in file:
                if line.startswith('W'):
                    print(line)
                    Write_Formula(line)

    except Exception as e:
        print(f"An error occurred, {FORMULA_SOURCE} : ", e)
        MyMessageBox(f" File Not Found .... {FORMULA_SOURCE} ")

    hwp.Run("SelectAll")
    hwp.Run("ParagraphShapeAlignCenter")
    OnScriptMacro_LineSpacing(hwp, 200)
    hwp.Run("Cancel")

    hwp.save_as(f"d:/05_Send/formula.hwp")
    hwp.quit()


if __name__ == '__main__':
    main()
