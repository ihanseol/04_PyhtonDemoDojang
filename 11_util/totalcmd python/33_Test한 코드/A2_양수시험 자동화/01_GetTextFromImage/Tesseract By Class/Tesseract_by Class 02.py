# https://pi000.tistory.com/entry/Python-%EC%9D%B4%EB%AF%B8%EC%A7%80%ED%8C%8C%EC%9D%BC%EC%9D%98-%ED%95%9C%EA%B8%80-%EC%9D%BD%EC%96%B4%EC%98%A4%EA%B8%B0pytesseract

import cv2
import pyautogui
import pytesseract
from PIL import Image
import re

DIRECTORY = "d:\\05_Send\\"
DELAY = 0.5



"""
imageCapture Constraint
2024/04/07

imagecapture : 2560x1440
edge full screen
https://www.gims.go.kr/igis_infomap.do

01_지하수용도 (YongDo) : 2430,530   105x46
02_지하수세부용도 (Sebu): 2190, 566  105x46
03_심도 (Simdo ): 2190x601  105x32
04_굴착직경 (WellDiameter): 2430x601  101x32
05_동력장치마력 (WellHP) : 2430x691 105x46
06_양수능력 (WellQ): 2190x691 - 105x46
07_토출관 (WellTochul ): 2190x743 - 105x46

"""


class ImageCaptureReaderClass:
    def __init__(self, image_name, resizeFactor=1):
        self.image_name = image_name
        self.resizeFactor = resizeFactor
        self.getImageReader()

    def DetermineResizeYES(self):
        if self.resizeFactor >= 2:
            self.ResizeImage()
            return True
        else:
            return False

    def ResizeImage(self):
        img = Image.open(self.image_name)

        width, height = img.size
        asp_rat = width / height

        new_width = width * self.resizeFactor
        new_height = height * self.resizeFactor

        new_rat = new_width / new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        else:
            new_width = round(new_height * asp_rat)
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img.save(self.image_name + '_resized.jpg')

    def getImageReader(self, StringReplaceYES=False):
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

            """
            config = '-l kor+eng --oem 3 --psm 11'
            config = '-l kor --oem 3'
            config = '-l kor'
            """

            config = '-l kor+eng --oem 3 --psm 11'

            if self.DetermineResizeYES():
                ImgPath = self.image_name + '_resized.jpg'
            else:
                ImgPath = self.image_name

            image = cv2.imread(ImgPath)

            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(ImgPath, gray)

            text = pytesseract.image_to_string(Image.open(ImgPath), config=config)
            if StringReplaceYES:
                text = self.setStringReplacer(text)
            return text

        except Exception as e:
            print(f" _________ getImageReader __________ {e}")

    def setStringReplacer(self, strText):
        try:
            strText = strText.replace('\n', '')
            strText = strText.replace('$', '')
            strText = strText.replace('TT', '')
            strText = strText.replace(' ', '')
            strText = strText.replace('Tr', '')
            strText = strText.replace('tr', '')
            strText = strText.replace(';', '')
            strText = strText.replace('Guess', '')
            strText = strText.replace('G', '')
            return strText

        except Exception as e:
            print(f" ____ setStringReplacer _____ {e}")


def replace_comma_to_dot(text):
    if ',' in text:
        text = text.replace(',', '.')
    # print('after :', text)
    return text


def extract_real_numbers(text):
    pattern = r'[-+]?\d*\.\d+|\d+'  # This pattern matches floating-point numbers or integers
    real_numbers = re.findall(pattern, text)
    real_numbers = [float(number) for number in real_numbers]
    numeric_value = float(real_numbers[0])

    return numeric_value



"""
imageCapture Constraint
2024/04/07

imagecapture : 2560x1440
edge full screen
https://www.gims.go.kr/igis_infomap.do

01_지하수용도 (YongDo) : 2430,530   105x46
02_지하수세부용도 (Sebu): 2190, 566  105x46
03_심도 (Simdo ): 2190x601  105x32
04_굴착직경 (WellDiameter): 2430x601  101x32
05_동력장치마력 (WellHP) : 2430x691 105x46
06_양수능력 (WellQ): 2190x691 - 105x46
07_토출관 (WellTochul ): 2190x743 - 105x46

"""


# capture in Print Preview
def capture_in_groundwater():
    pyautogui.screenshot(region=(2430, 530, 105, 33)).save(DIRECTORY + 'screenshot_01.jpg', quality=95)
    pyautogui.screenshot(region=(2190, 566, 105, 33)).save(DIRECTORY + 'screenshot_02.jpg', quality=95)
    pyautogui.screenshot(region=(2190, 601, 105, 33)).save(DIRECTORY + 'screenshot_03.jpg', quality=95)
    pyautogui.screenshot(region=(2430, 601, 105, 33)).save(DIRECTORY + 'screenshot_04.jpg', quality=95)
    pyautogui.screenshot(region=(2430, 691, 105, 33)).save(DIRECTORY + 'screenshot_05.jpg', quality=95)
    pyautogui.screenshot(region=(2190, 691, 105, 46)).save(DIRECTORY + 'screenshot_06.jpg', quality=95)
    pyautogui.screenshot(region=(2190, 743, 105, 46)).save(DIRECTORY + 'screenshot_07.jpg', quality=95)

    image1 = Image.open(DIRECTORY + 'screenshot_01.jpg')
    text1 = pytesseract.image_to_string(image1, config="-l kor  --psm 11")

    image2 = Image.open(DIRECTORY + 'screenshot_02.jpg')
    text2 = pytesseract.image_to_string(image2, config="-l kor  --psm 11")

    image3 = Image.open(DIRECTORY + 'screenshot_03.jpg')
    text3 = pytesseract.image_to_string(image3, config="--psm 7")

    image4 = Image.open(DIRECTORY + 'screenshot_04.jpg')
    text4 = pytesseract.image_to_string(image4, config="--psm 7")

    image5 = Image.open(DIRECTORY + 'screenshot_05.jpg')
    text5 = pytesseract.image_to_string(image5, config="--psm 7")

    image6 = Image.open(DIRECTORY + 'screenshot_06.jpg')
    text6 = pytesseract.image_to_string(image6, config="--psm 7")

    image7 = Image.open(DIRECTORY + 'screenshot_07.jpg')
    text7 = pytesseract.image_to_string(image7, config="--psm 7")

    print(text1, text2)
    print(text3, text4, text5, text6, text7)



if __name__ == "__main__":
    # my_object = ImageCaptureReaderClass('test.png')
    # text = my_object.getImageReader(StringReplaceYES=True)
    # print(text)

    capture_in_groundwater()
