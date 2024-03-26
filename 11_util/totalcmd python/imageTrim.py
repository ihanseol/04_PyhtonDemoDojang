import os
import ctypes

from PIL import Image, ImageChops
from natsort import natsorted
from pdf2image import convert_from_path, convert_from_bytes

DIRECTORY = "d:\\05_Send\\"


def pdf_to_jpg(pdf_path):
    # Convert each page of the PDF to a JPEG image
    images = convert_from_path(pdf_path, dpi=300)
    # Save each image as a JPEG file
    for i, image in enumerate(images):
        image.save(f"{pdf_path[:-4]}_page{i + 1}.jpg", "JPEG")


def image_trim(input_filename):
    image = Image.open(input_filename)
    bg = Image.new(image.mode, image.size, image.getpixel((0, 0)))
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        cropped_image: Image = image.crop(bbox)

    cropped_image.save(input_filename)


def main_job():
    os.chdir(DIRECTORY)
    files = os.listdir()
    image_files = [f for f in files if f.endswith('.jpg')]
    image_files = natsorted(image_files)

    for image_file in image_files:
        try:
            print(image_file)
            image_trim(image_file)
        except Exception as e:
            print(f"An error occurred, {image_file} : ", e)


if __name__ == "__main__":
    main_job()
