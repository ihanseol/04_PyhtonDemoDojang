import fitz # PyMuPDF
import easygui

# 파일 선택 다이얼로그 열기
pdf_path = easygui.fileopenbox(title="PDF 파일 선택", filetypes=["*.pdf"])

# 사용자가 파일을 선택했을 경우에만 실행
if pdf_path:
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
else:
    print("파일 선택이 취소되었습니다.")


