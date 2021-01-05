
# https://youtu.be/MOd8pkeA__k


import pyautogui


# i = pyautogui.locateCenterOnScreen('7.png')
# pyautogui.click(i)


print(pyautogui.position())

pyautogui.screenshot('1.png', region=(1324, 768, 30, 30))

num1 = pyautogui.locateCenterOnScreen('1.png')
pyautogui.click(num1)


