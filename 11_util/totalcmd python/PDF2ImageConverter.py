import os
import ctypes
from PIL import Image
from natsort import natsorted
from pdf2image import convert_from_path, convert_from_bytes

DIRECTORY = "d:\\05_Send\\"


def pdf_to_jpg(pdf_path):
    # Convert each page of the PDF to a JPEG image
    images = convert_from_path(pdf_path, dpi=300)
    # Save each image as a JPEG file
    for i, image in enumerate(images):
        image.save(f"{pdf_path[:-4]}_page{i + 1}.jpg", "JPEG")


os.chdir(DIRECTORY)
files = os.listdir()

pdf_files = [f for f in files if f.endswith('.pdf')]
pdf_files = natsorted(pdf_files)

# Convert each PDF file to a JPEG image
for pdf_file in pdf_files:
    try:
        print(pdf_file)
        pdf_to_jpg(pdf_file)
    except Exception as e:
        print(f"An error occurred, {pdf_file} : ", e)


