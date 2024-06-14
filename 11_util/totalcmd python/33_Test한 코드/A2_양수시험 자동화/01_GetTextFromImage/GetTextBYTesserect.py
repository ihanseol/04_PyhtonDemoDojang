import pyautogui
from PIL import Image
import pytesseract
import re


PROGRAM_PATH = r'C:\WHPA\AQTEver3.4(170414)\AQTW32.EXE'
ISAQTOPEN = False
DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5
IS_BLOCK = True


def replace_comma_to_dot(text):
    if ',' in text:
        text = text.replace(',', '.')
    # print('after :', text)
    return text


def extract_real_numbers(text):
    # Define a regular expression pattern to match real numbers
    pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern matches floating-point numbers or integers

    # Use the findall function from the re module to extract all matches
    real_numbers = re.findall(pattern, text)

    # Convert the matched strings to actual floating-point numbers
    real_numbers = [float(number) for number in real_numbers]
    numeric_value = float(real_numbers[0])

    return numeric_value


# Example usage:
text = "There are 3.14 apples and -2.5 oranges."
numbers = extract_real_numbers(text)
print("Real numbers in the text:", numbers)


# capture in Main Screen
def capture_in_main_screen():
    im1 = pyautogui.screenshot(region=(1026, 263, 144, 24))  # T
    im1.save(DIRECTORY + 'screenshot_t.jpg', quality=95)
    image1 = Image.open(DIRECTORY + 'screenshot_t.jpg')

    im2 = pyautogui.screenshot(region=(1026, 282, 144, 24))  # S
    im2.save(DIRECTORY + 'screenshot_s.jpg', quality=95)
    image2 = Image.open(DIRECTORY + 'screenshot_s.jpg')

    text1 = pytesseract.image_to_string(image1, config="--psm 7")
    text2 = pytesseract.image_to_string(image2, config="--psm 7")

    text1 = replace_comma_to_dot(text1)
    val_T = extract_real_numbers(text1)
    print(val_T)

    text2 = replace_comma_to_dot(text2)
    val_S = extract_real_numbers(text2)
    print(val_S)

    return [val_T, val_S]


# capture in Print Preview
def capture_in_Preview():
    im1 = pyautogui.screenshot(region=(996, 1208, 130, 22))  # T
    im1.save(DIRECTORY + 'screenshot_t.jpg', quality=95)
    image1 = Image.open(DIRECTORY + 'screenshot_t.jpg')
    text1 = pytesseract.image_to_string(image1, config="--psm 7")

    im2 = pyautogui.screenshot(region=(1326, 1208, 93, 16))  # S
    im2.save(DIRECTORY + 'screenshot_s.jpg', quality=95)
    image2 = Image.open(DIRECTORY + 'screenshot_s.jpg')
    text2 = pytesseract.image_to_string(image2, config="--psm 7")

    text1 = replace_comma_to_dot(text1)
    val_T = extract_real_numbers(text1)
    print(val_T)

    text2 = replace_comma_to_dot(text2)
    val_S = extract_real_numbers(text2)
    print(val_S)

    return [val_T, val_S]



result = capture_in_main_screen()
print(result[0], result[1])

