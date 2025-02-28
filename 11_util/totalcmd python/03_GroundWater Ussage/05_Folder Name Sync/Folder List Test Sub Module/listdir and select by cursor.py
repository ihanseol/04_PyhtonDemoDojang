import os
import curses


def list_directories_in_current_path(path=r"d:/09_hardRain/"):
    if os.path.isdir(path):
        os.chdir(path)
    current_path = os.getcwd()
    directories = [d for d in os.listdir(current_path) if os.path.isdir(os.path.join(current_path, d))]
    return directories


def main(stdscr):
    directories = list_directories_in_current_path()

    if not directories:
        print("No directories found in the current path.")
        return

    curses.curs_set(0)  # Hide the cursor
    current_selection = 0

    while True:
        stdscr.clear()

        # Display directories
        for idx, directory in enumerate(directories):
            if idx == current_selection:
                stdscr.addstr(idx, 0, directory, curses.A_REVERSE)
            else:
                stdscr.addstr(idx, 0, directory)

        key = stdscr.getch()

        if key == curses.KEY_UP:
            current_selection = (current_selection - 1) % len(directories)
        elif key == curses.KEY_DOWN:
            current_selection = (current_selection + 1) % len(directories)
        elif key == ord('\n'):  # Enter key
            break

    selected_directory = directories[current_selection]
    stdscr.clear()
    stdscr.addstr(0, 0, f"Selected directory: {selected_directory}")
    stdscr.refresh()
    stdscr.getch()  # Wait for another key press


if __name__ == "__main__":
    curses.wrapper(main)
