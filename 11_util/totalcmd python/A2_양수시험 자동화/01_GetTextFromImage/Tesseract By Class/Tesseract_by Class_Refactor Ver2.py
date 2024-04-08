"""
imageCapture Constraint
2024/04/07

imagecapture : 2560x1440
this is must run chrome debug window in total commander

https://www.gims.go.kr/igis_infomap.do

01_지하수용도 (YongDo) : 2430,530   105x46
02_지하수세부용도 (Sebu): 2190, 566  105x46
03_심도 (Simdo ): 2190x601  105x32
04_굴착직경 (WellDiameter): 2430x601  101x32
05_동력장치마력 (WellHP) : 2430x691 105x46
06_양수능력 (WellQ): 2190x691 - 105x46
07_토출관 (WellTochul ): 2190x743 - 105x46

"""

import cv2
import pytesseract
from PIL import Image
from screeninfo import get_monitors
import pygetwindow as gw
import pyautogui
import winsound


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

    @staticmethod
    def change_window(name_title) -> None:
        gwindows = gw.getWindowsWithTitle(name_title)

        if gwindows:
            window = gwindows[0]
            window.activate()
            if not window.isMaximized:
                window.maximize()
        else:
            print(f"No  {name_title} found.")

    @staticmethod
    def get_current_window() -> str:
        active_window = gw.getActiveWindow()
        return active_window.title

    @staticmethod
    def beep(frequency=1000, duration=1000) -> None:
        frequency = 1000
        duration = 1000
        winsound.Beep(frequency, duration)

    @staticmethod
    def get_screen_width() -> int:
        screen = get_monitors()[0]
        return screen.width

    def capture_and_read_groundwater(self) -> object:
        result = []
        screen_2560x1440 = [
            ([2434, 543, 105, 33], 'screenshot_01.jpg'),
            ([2194, 581, 105, 33], 'screenshot_02.jpg'),
            ([2194, 619, 105, 33], 'screenshot_03.jpg'),
            ([2434, 619, 105, 33], 'screenshot_04.jpg'),
            ([2434, 707, 105, 46], 'screenshot_05.jpg'),
            ([2194, 707, 105, 46], 'screenshot_06.jpg'),
            ([2194, 760, 105, 46], 'screenshot_07.jpg'),
        ]

        screen_1920x1200 = [
            ([1792, 544, 105, 34], 'screenshot_01.jpg'),
            ([1552, 580, 105, 34], 'screenshot_02.jpg'),
            ([1552, 616, 105, 34], 'screenshot_03.jpg'),
            ([1792, 616, 105, 34], 'screenshot_04.jpg'),
            ([1792, 707, 105, 46], 'screenshot_05.jpg'),
            ([1552, 707, 105, 46], 'screenshot_06.jpg'),
            ([1552, 759, 105, 46], 'screenshot_07.jpg'),
        ]

        if self.get_screen_width() == 2560:
            areas_filenames = screen_2560x1440
        else:
            areas_filenames = screen_1920x1200

        self.change_window(name_title="Chrome")

        for i, (area, filename) in enumerate(areas_filenames, 1):
            self.capture_area_to_file(area, filename)
            text = self.read_text_from_image(filename, use_english=i > 3)
            result.append(text)
            print(text)

        self.beep()
        return result


if __name__ == "__main__":
    image_reader = ImageCaptureReader(resize_factor=3)
    result = image_reader.capture_and_read_groundwater()
    print(result)
