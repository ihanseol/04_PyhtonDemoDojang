import cv2
import pytesseract
from PIL import Image
from screeninfo import get_monitors
import pygetwindow as gw
import pyautogui
import winsound


def change_window(name_title) -> None:
    gwindows = gw.getWindowsWithTitle(name_title)

    if gwindows:
        window = gwindows[0]
        window.activate()
        if not window.isMaximized:
            window.maximize()
    else:
        print(f"No  {name_title} found.")


def get_current_window() -> str:
    active_window = gw.getActiveWindow()
    return active_window.title


def beep(frequency=1000, duration=1000) -> None:
    frequency = 1000
    duration = 1000
    winsound.Beep(frequency, duration)


if __name__ == "__main__":
    change_window(name_title="Chrome")
    beep()
