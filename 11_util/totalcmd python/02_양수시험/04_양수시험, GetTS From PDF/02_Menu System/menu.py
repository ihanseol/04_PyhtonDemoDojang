import keyboard
import os


def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_menu(options, selected_index):
    """
    Displays the menu options with the currently selected option highlighted.

    Args:
        options (list): List of menu options.
        selected_index (int): Index of the currently selected option.
    """
    clear_console()
    print("=== MENU ===")
    for i, option in enumerate(options):
        if i == selected_index:
            print(f"> {option}")  # Highlight the selected option
        else:
            print(f"  {option}")
    print("============")


def run_menu(menu_options):
    """
    Runs the interactive console menu.

    Args:
        menu_options (list): List of menu options.

    Returns:
        str: The selected menu option.
    """
    current_index = 0
    display_menu(menu_options, current_index)

    while True:
        # Wait for a key press
        event = keyboard.read_event(suppress=True)

        if event.event_type == keyboard.KEY_DOWN:
            if event.name == "up":
                # Move selection up
                current_index = (current_index - 1) % len(menu_options)
            elif event.name == "down":
                # Move selection down
                current_index = (current_index + 1) % len(menu_options)
            elif event.name == "enter":
                # Select the current option
                clear_console()
                return menu_options[current_index]

        # Redraw the menu after each key press
        display_menu(menu_options, current_index)


if __name__ == "__main__":
    # Define the menu options
    menu_options = ["Option 1", "Option 2", "Option 3", "Exit"]

    # Run the menu and get the selected option
    selected_option = run_menu(menu_options)
    print(f"You selected: {selected_option}")