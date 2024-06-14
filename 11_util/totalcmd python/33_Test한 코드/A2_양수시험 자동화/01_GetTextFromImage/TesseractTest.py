from PIL import Image
import pytesseract


def tessract_test():
    image2 = Image.open('test.png')
    # text2 = pytesseract.image_to_string(image2, config="--psm 7")
    text2 = pytesseract.image_to_string(image2, lang="kor")

    print(text2)


def main():
    tessract_test()


if __name__ == '__main__':
    main()
