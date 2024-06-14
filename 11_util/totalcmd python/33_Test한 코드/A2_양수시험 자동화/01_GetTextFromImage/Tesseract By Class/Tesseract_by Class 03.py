# https://pi000.tistory.com/entry/Python-%EC%9D%B4%EB%AF%B8%EC%A7%80%ED%8C%8C%EC%9D%BC%EC%9D%98-%ED%95%9C%EA%B8%80-%EC%9D%BD%EC%96%B4%EC%98%A4%EA%B8%B0pytesseract

import cv2
import pyautogui
import pytesseract
from PIL import Image


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
    def __init__(self, image_name='void_filename', resizeFactor=1):
        self.image_name = image_name
        self.resizeFactor = resizeFactor
        self.getImageReader()

    def SetImageName(self, image_name):
        self.image_name = image_name

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

    def getImageReader(self, config_type=1, StringReplaceYES=False):
        try:
            pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

            """
            config = '-l kor+eng --oem 3 --psm 11'
            config = '-l kor --oem 3'
            config = '-l kor'
            """
            if config_type == 1:
                config = '-l kor --oem 3 --psm 11'
            else:
                config = '-l eng --oem 3 --psm 7'

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

    def capture_image(self, area, save_path):
        pyautogui.screenshot(region=(area[0], area[1], area[2], area[3])).save(save_path, quality=95)

    def capture_in_groundwater(self):
        areas_with_filenames = [
            ([2430, 530, 105, 33], 'screenshot_01.jpg'),
            ([2190, 566, 105, 33], 'screenshot_02.jpg'),
            ([2190, 601, 105, 33], 'screenshot_03.jpg'),
            ([2430, 601, 105, 33], 'screenshot_04.jpg'),
            ([2430, 691, 105, 46], 'screenshot_05.jpg'),
            ([2190, 691, 105, 46], 'screenshot_06.jpg'),
            ([2190, 743, 105, 46], 'screenshot_07.jpg'),
        ]

        for area, filename in areas_with_filenames:
            self.capture_image(area, filename)

        for i, (area, filename) in enumerate(areas_with_filenames, 1):
            self.SetImageName(filename)
            if i > 3:
                text = self.getImageReader(2, StringReplaceYES=True)
            else:
                text = self.getImageReader(1, StringReplaceYES=True)
            print(text)


    def setStringReplacer(self, strText) -> object:
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


if __name__ == "__main__":
    my_object = ImageCaptureReaderClass()
    my_object.capture_in_groundwater()