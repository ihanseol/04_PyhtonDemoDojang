import time
from hwpapi.core import App
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


def main():
    try:
        with open(FORMULA_SOURCE, 'r', encoding='cp949') as file:
            app = App(None, True)
            for line in file:
                if line.startswith('W'):
                    print(line)
                    Write_Formula(line)

    except Exception as e:
        print(f"An error occurred, {FORMULA_SOURCE} : ", e)
        MyMessageBox(f" File Not Found .... {FORMULA_SOURCE} ")

    app.api.Run("SelectAll");
    app.api.Run("ParagraphShapeAlignCenter");
    app.api.Run("Cancel");


if __name__ == '__main__':
    main()
