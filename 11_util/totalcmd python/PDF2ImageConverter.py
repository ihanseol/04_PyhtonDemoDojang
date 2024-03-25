
import os
import ctypes
from PIL import Image
from pdf2image import convert_from_path, convert_from_bytes

def pdf_to_jpg(pdf_path):
    # Convert each page of the PDF to a JPEG image
    images = convert_from_path(pdf_path, dpi=300)
    # Save each image as a JPEG file
    for i, image in enumerate(images):
        image.save(f"{pdf_path[:-4]}_page{i+1}.jpg", "JPEG")



user32 = ctypes.windll.user32
user32.BlockInput(True)


# Get a list of all PDF files in the current directory
pdf_files = [f for f in os.listdir() if f.endswith('.pdf')]

# Convert each PDF file to a JPEG image
for pdf_file in pdf_files:
    print(pdf_file)
    pdf_to_jpg(pdf_file)


user32.BlockInput(False)


