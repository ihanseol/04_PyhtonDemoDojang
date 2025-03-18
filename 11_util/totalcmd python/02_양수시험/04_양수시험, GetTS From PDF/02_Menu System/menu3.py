import keyboard
import os
import time


def clear_screen():
    # OS에 따라 콘솔 지우기
    os.system('cls' if os.name == 'nt' else 'clear')


# ANSI 색상 코드
COLOR_RESET = "\033[0m"
BG_WHITE_FG_BLACK = "\033[47;30m"  # 흰색 배경, 검은색 글씨
SELECTED_BG = "\033[7m"  # 반전 색상 (선택된 항목용)


class MenuBar:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.running = True

    def display_menu(self):
        clear_screen()
        print("Use ←→ arrows to navigate, Enter to select:\n")

        # 메뉴바 문자열 생성
        menu_items = []
        for i, option in enumerate(self.options):
            if i == self.selected:
                # 선택된 항목: 반전 색상
                menu_items.append(f"{SELECTED_BG} {option.upper()} {COLOR_RESET}")
            else:
                # 기본 항목: 흰색 배경, 검은색 글씨
                menu_items.append(f"{BG_WHITE_FG_BLACK} {option} {COLOR_RESET}")

        # 항목들을 | 로 연결
        menu_bar = " | ".join(menu_items)
        print(menu_bar)
        print("\n" + "=" * (len(menu_bar) // 2))  # ANSI 코드 때문에 길이 조정

    def move_left(self):
        if self.selected > 0:
            self.selected -= 1
            self.display_menu()

    def move_right(self):
        if self.selected < len(self.options) - 1:
            self.selected += 1
            self.display_menu()

    def select(self):
        self.running = False
        return self.options[self.selected]

    def run(self):
        # 키 바인딩
        keyboard.on_press_key("left", lambda _: self.move_left())
        keyboard.on_press_key("right", lambda _: self.move_right())
        keyboard.on_press_key("enter", lambda _: self.select())

        # 초기 메뉴 표시
        self.display_menu()

        # 선택될 때까지 실행
        while self.running:
            time.sleep(0.1)

        # 키 바인딩 해제
        keyboard.unhook_all()
        return self.options[self.selected]


# 사용 예시
def main():
    menu_options = [
        "File",
        "Edit",
        "View",
        "Help",
        "Exit"
    ]

    menu = MenuBar(menu_options)
    selected_option = menu.run()

    clear_screen()
    print(f"You selected: {selected_option}")

    # 선택 처리
    if selected_option == "File":
        print("Opening File menu...")
    elif selected_option == "Edit":
        print("Opening Edit menu...")
    elif selected_option == "View":
        print("Opening View menu...")
    elif selected_option == "Help":
        print("Showing Help...")
    elif selected_option == "Exit":
        print("Goodbye!")


if __name__ == "__main__":
    main()