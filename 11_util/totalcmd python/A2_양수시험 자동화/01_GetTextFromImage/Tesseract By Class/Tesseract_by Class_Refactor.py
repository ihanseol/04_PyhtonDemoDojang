import cv2
import pytesseract
from PIL import Image
import pyautogui


class ImageCaptureReader:
    def __init__(self, resize_factor=1):
        self.resize_factor = resize_factor
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract'

    @staticmethod
    def capture_area_to_file(area, filename):
        pyautogui.screenshot(region=area).save(filename, quality=95)

    def read_text_from_image(self, image_path, use_english=False, perform_replacement=True):
        if self.resize_factor >= 2:
            image_path = self.resize_image(image_path)

        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        processed_image_path = f"{image_path}_processed.jpg"
        cv2.imwrite(processed_image_path, gray)

        config = self.get_tesseract_config(use_english)
        text = pytesseract.image_to_string(Image.open(processed_image_path), config=config)

        return self.replace_strings(text) if perform_replacement else text

    def resize_image(self, image_path) -> str:
        img = Image.open(image_path)
        original_size = img.size
        resized_size = tuple([int(dim * self.resize_factor) for dim in original_size])
        img = img.resize(resized_size, Image.Resampling.LANCZOS)
        resized_image_path = f"{image_path}_resized.jpg"
        img.save(resized_image_path)
        return resized_image_path

    @staticmethod
    def get_tesseract_config(use_english) -> str:
        if use_english:
            return '-l eng --oem 3 --psm 7'
        else:
            return '-l kor --oem 3 --psm 11'

    @staticmethod
    def replace_strings(text):
        replacements = ['\n', '$', 'TT', ' ', 'Tr', 'tr', ';', 'Guess', 'G']
        for r in replacements:
            text = text.replace(r, '')
        return text

    def capture_and_read_groundwater(self) -> object:
        result = []
        areas_filenames = [
            ([2430, 530, 105, 33], 'screenshot_01.jpg'),
            ([2190, 566, 105, 33], 'screenshot_02.jpg'),
            ([2190, 601, 105, 33], 'screenshot_03.jpg'),
            ([2430, 601, 105, 33], 'screenshot_04.jpg'),
            ([2430, 691, 105, 46], 'screenshot_05.jpg'),
            ([2190, 691, 105, 46], 'screenshot_06.jpg'),
            ([2190, 743, 105, 46], 'screenshot_07.jpg'),
        ]

        for i, (area, filename) in enumerate(areas_filenames, 1):
            self.capture_area_to_file(area, filename)
            text = self.read_text_from_image(filename, use_english=i > 3)
            result.append(text)
            print(text)

        return result


if __name__ == "__main__":
    image_reader = ImageCaptureReader()
    result = image_reader.capture_and_read_groundwater()
    print(result)


