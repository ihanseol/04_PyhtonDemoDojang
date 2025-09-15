import fitz # PyMuPDF
import sys

# 명령줄 인수에서 PDF 파일 경로 가져오기
# 예: python your_script.py "C:\Users\User\Documents\my_document.pdf"
if len(sys.argv) < 2:
    print("사용법: python your_script.py <pdf_file_path>")
    sys.exit(1)

pdf_path = sys.argv[1]

try:
    doc = fitz.open(pdf_path)
    page = doc[0] # Get the first page
    text_dict = page.get_text("dict") # Get text in dictionary format

    for block in text_dict["blocks"]:
        if block["type"] == 0: # It's a text block
            for line in block["lines"]:
                for span in line["spans"]:
                    font_name = span["font"]
                    font_size = span["size"]
                    text = span["text"]
                    bbox = span["bbox"] # Bounding box of the text span
                    print(f"Font: {font_name}, Size: {font_size:.2f}, Text: {text}, Bbox: {bbox}")

    doc.close()

except Exception as e:
    print(f"오류 발생: {e}")
    sys.exit(1)