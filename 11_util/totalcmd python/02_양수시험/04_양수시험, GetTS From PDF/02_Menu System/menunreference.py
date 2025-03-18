import keyboard
import os
import time


def clear_screen():
    # Clear console based on OS
    os.system('cls' if os.name == 'nt' else 'clear')


# ANSI 색상 코드
COLOR_RESET = "\033[0m"
INVERTED = "\033[7m"  # 반전 색상 (흰색 배경, 검은색 글씨)


class ConsoleMenu:
    def __init__(self, options):
        self.options = options
        self.selected = 0
        self.running = True

    def display_menu(self):
        clear_screen()
        print("Use ↑↓ arrows to navigate, Enter to select:\n")
        for i, option in enumerate(self.options):
            if i == self.selected:
                # 선택된 항목에 반전 색상 적용
                print(f"{INVERTED}> {option} {COLOR_RESET}")
            else:
                print(f"  {option}")

    def move_up(self):
        if self.selected > 0:
            self.selected -= 1
            self.display_menu()

    def move_down(self):
        if self.selected < len(self.options) - 1:
            self.selected += 1
            self.display_menu()

    def select(self):
        self.running = False
        return self.options[self.selected]

    def run(self):
        # Bind arrow keys and enter
        keyboard.on_press_key("up", lambda _: self.move_up())
        keyboard.on_press_key("down", lambda _: self.move_down())
        keyboard.on_press_key("enter", lambda _: self.select())

        # Display initial menu
        self.display_menu()

        # Keep running until selection is made
        while self.running:
            time.sleep(0.1)

        # Unbind keys after selection
        keyboard.unhook_all()
        return self.options[self.selected]


# Example usage
def main():
    menu_options = [
        "Start Game   ",
        "Settings     ",
        "Help         ",
        "Exit         "
    ]

    menu = ConsoleMenu(menu_options)
    selected_option = menu.run()

    clear_screen()
    print(f"You selected: {selected_option}")

    # Handle the selection
    if selected_option == "Start Game":
        print("Starting game...")
    elif selected_option == "Settings":
        print("Opening settings...")
    elif selected_option == "Help":
        print("Showing help...")
    elif selected_option == "Exit":
        print("Goodbye!")


if __name__ == "__main__":
    main()
