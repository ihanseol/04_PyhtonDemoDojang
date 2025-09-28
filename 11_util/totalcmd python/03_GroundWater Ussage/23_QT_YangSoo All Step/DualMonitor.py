import pyautogui
import pygetwindow as gw
from screeninfo import get_monitors

import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

import subprocess
import win32gui
import win32con
import win32com.client as win32
import threading



def move_window_to_second_monitor(window_title):
    """
    Moves the specified window to the center of the second monitor in a dual-monitor setup.

    Args:
        window_title (str): The title of the window to move.
    """

    # Callback function for EnumDisplayMonitors
    def enum_monitor_callback(monitor, hdc, lprc, data):
        data.append(lprc)
        return True

    # Enumerate all monitors
    monitors = []
    win32gui.EnumDisplayMonitors(None, None, enum_monitor_callback, monitors)

    if len(monitors) < 2:
        print("Not enough monitors detected. Need at least 2.")
        return

    # Get the second monitor's rectangle (lprc: left, top, right, bottom)
    second_monitor = monitors[1]  # Index 0 is primary, 1 is secondary
    mon_left, mon_top, mon_right, mon_bottom = second_monitor

    # Find the window by title
    hwnd = win32gui.FindWindow(None, window_title)
    if not hwnd:
        print(f"Window with title '{window_title}' not found.")
        return

    # Get the current window size
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    # Calculate new position: center on second monitor
    new_left = mon_left + ((mon_right - mon_left) - width) // 2
    new_top = mon_top + ((mon_bottom - mon_top) - height) // 2

    # Move the window (SWP_NOSIZE to keep size, HWND_TOP to bring to front)
    win32gui.SetWindowPos(hwnd, win32con.HWND_TOP, new_left, new_top, 0, 0,
                          win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

    print(f"Window '{window_title}' moved to second monitor at position ({new_left}, {new_top}).")


# Example usage
if __name__ == "__main__":
    # Replace 'Notepad' with your actual window title
    move_window_to_second_monitor('Notepad')