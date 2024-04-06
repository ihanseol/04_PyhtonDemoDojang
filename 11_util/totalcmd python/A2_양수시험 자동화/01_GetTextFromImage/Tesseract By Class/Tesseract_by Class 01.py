# https://pi000.tistory.com/entry/Python-%EC%9D%B4%EB%AF%B8%EC%A7%80%ED%8C%8C%EC%9D%BC%EC%9D%98-%ED%95%9C%EA%B8%80-%EC%9D%BD%EC%96%B4%EC%98%A4%EA%B8%B0pytesseract

import cv2
import pytesseract
from PIL import Image


class ImageCaptureReaderClass:
    def __init__(self, image_name, resizeFactor=1):
        self.image_name = image_name
        self.resizeFactor = resizeFactor
        self.IsImageResize = False
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


if __name__ == "__main__":
    my_object = ImageCaptureReaderClass('test.png')
    text = my_object.getImageReader(StringReplaceYES=True)
    print(text)
