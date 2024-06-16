from PIL import Image
import pytesseract

FILE_NAME = r'c:\Users\minhwasoo\Documents\Downloads\w3_screenshot_02_S.jpg'


def tessract_test():
    image2 = Image.open(FILE_NAME)
    # text2 = pytesseract.image_to_string(image2, config="--psm 7")
    text2 = pytesseract.image_to_string(image2, config="-l eng  --psm 7")

    print(text2)


def main():
    tessract_test()


if __name__ == '__main__':
    main()
