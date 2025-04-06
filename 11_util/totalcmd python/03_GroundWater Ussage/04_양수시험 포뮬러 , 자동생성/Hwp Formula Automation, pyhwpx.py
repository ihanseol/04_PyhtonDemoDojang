import time
from pyhwpx import Hwp
import pyautogui
import pyperclip
import tkinter as tk
from tkinter import messagebox
import keyboard
import os

FORMULA_SOURCE = "d:\\05_Send\\YangSoo.csv"


class ConsoleMenu:
    # ANSI 색상 코드
    COLOR_RESET = "\033[0m"
    INVERTED = "\033[7m"  # 반전 색상 (흰색 배경, 검은색 글씨)

    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.running = True

    @staticmethod
    def clear_screen():
        # Clear console based on OS
        os.system('cls' if os.name == 'nt' else 'clear')

    def display_menu(self):
        self.clear_screen()
        print("Use ↑↓ arrows to navigate, Enter to select:\n")
        for i, option in enumerate(self.options):
            if i == self.selected:
                # 선택된 항목에 반전 색상 적용
                print(f"{self.INVERTED}> {option} {self.COLOR_RESET}")
            else:
                print(f"  {option}")

    def move_up(self):
        if self.selected > 0:
            self.selected -= 1
            self.display_menu()
        else:
            self.selected = len(self.options) - 1
            self.display_menu()

    def move_down(self):
        if self.selected < len(self.options) - 1:
            self.selected += 1
            self.display_menu()
        else:
            self.selected = 0
            self.display_menu()

    def select(self):
        self.running = False
        return self.options[self.selected]

    def run(self):
        # Bind arrow keys and enter
        keyboard.on_press_key("up", lambda _: self.move_up())
        keyboard.on_press_key("left", lambda _: self.move_up())
        keyboard.on_press_key("down", lambda _: self.move_down())
        keyboard.on_press_key("right", lambda _: self.move_down())
        keyboard.on_press_key("enter", lambda _: self.select())

        # Display initial menu
        self.display_menu()

        # Keep running until selection is made
        while self.running:
            time.sleep(0.1)

        # Unbind keys after selection
        keyboard.unhook_all()
        return self.options[self.selected]


# end of ConsoleMenu


def write_formula(formula_string, inject_yes):
    pyautogui.keyDown('ctrl')
    pyautogui.press('n')
    pyautogui.press('m')
    pyautogui.keyUp('ctrl')

    pyperclip.copy(formula_string)
    pyautogui.hotkey('ctrl', 'v')

    if inject_yes:
        pyautogui.hotkey('ctrl', 'tab')
        pyperclip.copy(formula_string)
        pyautogui.hotkey('ctrl', 'v')

    pyautogui.hotkey('shift', 'esc')  # close formula editor window
    time.sleep(0.5)

    pyautogui.press('enter')


def my_message_box(message):
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


def on_script_macro_line_spacing(hwp, spacing):
    pset = hwp.HParameterSet.HParaShape
    hwp.HAction.GetDefault("ParagraphShape", pset.HSet)
    pset.LineSpacing = spacing

    hwp.HAction.Execute("ParagraphShape", pset.HSet)
    hwp.HAction.Run("Cancel")


def main():
    menu_options = [
        "   Do Not Inject Ctrl Tab For Formula    ",
        "   Inject Ctrl Tab For Formula           "
    ]

    inject_yes: bool = False

    menu = ConsoleMenu(menu_options)
    selected_option = menu.run()

    if "Do Not" in selected_option:
        inject_yes = False
    else:
        inject_yes = True

    try:
        with open(FORMULA_SOURCE, 'r', encoding='cp949') as file:
            hwp = Hwp(new=True, visible=True)
            for line in file:
                if line.startswith('W'):
                    print(line)
                    write_formula(line, inject_yes)

    except Exception as e:
        print(f"An error occurred, {FORMULA_SOURCE} : ", e)
        my_message_box(f" File Not Found .... {FORMULA_SOURCE} ")

    hwp.Run("SelectAll")
    hwp.Run("ParagraphShapeAlignCenter")
    on_script_macro_line_spacing(hwp, 210)
    hwp.Run("Cancel")

    hwp.save_as(f"d:/05_Send/formula.hwp")
    hwp.quit()


if __name__ == '__main__':
    main()
