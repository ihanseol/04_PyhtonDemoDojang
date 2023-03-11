import pyautogui

res = pyautogui.locateOnScreen("max.png")
print(res)
res = pyautogui.locateOnScreen("max_black.png")
print(res)


# res = pyautogui.locateOnScreen(r'd:\05_Send\max.png', region=(2560, 0, 2560, 1440))
# print(res)

# res = pyautogui.locateOnScreen(r'd:\05_Send\max_black.png', region=(2560, 0, 2560, 1440))
# print(res)

