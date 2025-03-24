import shutil
import os
import keyboard
import time
from FileProcessing_V4_refactored import FileManager


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


YangSoo_Folder = r"d:\12_dev\02_Excel2\01_Acquifer Pumping Test\01_양수시험"
original_file_path = "d:/05_Send/A1_ge_OriginalSaveFile.xlsm"
destination_folder = "d:/05_Send/"


def duplicate_and_rename_file(original_path, destination_folder, cnt):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    destination_path = os.path.join(destination_folder, f"A{cnt}_ge_OriginalSaveFile.xlsm")
    shutil.copy(original_path, destination_path)
    return destination_path


def get_user_input():
    while True:
        try:
            n = int(input("Enter the number of times to loop: "))
            if n <= 0:
                print("Please enter a positive integer.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    return n


def main():
    menu_options = [
        "   집수정    ",
        "   지열공    ",
    ]

    # print(len(menu_options))

    menu = ConsoleMenu(menu_options)
    selected_option = menu.run()

    fm = FileManager()
    if "집수정" in selected_option:
        source = fm.get_file_filter(YangSoo_Folder, 'A1*집수정*.xlsm')[-1:]
    else:
        source = fm.get_file_filter(YangSoo_Folder, 'A1*지열공*.xlsm')[-1:]

    my_source = ''.join(source)
    print(my_source)
    if source:
        fm.copy_file(my_source, original_file_path)

    n = get_user_input()
    print("You entered:", n)
    for i in range(2, n + 1):
        new_file_path = duplicate_and_rename_file(original_file_path, destination_folder, i)
        print(f"File duplicated and renamed to: {new_file_path}")


if __name__ == "__main__":
    main()
