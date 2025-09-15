import fitz


def extract_fonts(pdf_path, output_dir="extracted_fonts"):
    """
    PDF에서 임베드된 폰트 스트림을 추출하여 파일로 저장합니다.
    """
    # PyMuPDF에서 폰트 파일을 저장할 디렉토리 생성
    import os
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    doc = fitz.open(pdf_path)

    # PDF의 모든 객체(xref)를 순회합니다.
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref)

            # 폰트 객체인지 확인
            if b"/FontFile" in obj or b"/FontFile2" in obj or b"/FontFile3" in obj:
                # 폰트 스트림 데이터 추출
                stream = doc.extract_font(xref)

                # 파일 확장자 결정 (FontFile2는 TrueType)
                if b"/FontFile2" in obj:
                    ext = ".ttf"
                elif b"/FontFile3" in obj:
                    ext = ".otf"
                else:  # FontFile (Type1)
                    ext = ".pfb"

                # 폰트 이름 정보 추출 (가능하다면)
                font_name = "unknown"
                for key, val in doc.xref_dict(xref).items():
                    if key.endswith(b"/BaseFont"):
                        font_name = val.decode().strip()
                        if font_name.startswith('SCMYNU+'):  # 서브셋 이름 제거
                            font_name = font_name[6:]
                        break

                # 파일 저장 경로 설정
                output_path = os.path.join(output_dir, f"{font_name}_{xref}{ext}")

                with open(output_path, "wb") as f:
                    f.write(stream)

                print(f"추출된 폰트: {output_path}")

        except Exception as e:
            # 오류가 발생하면 건너뜁니다. 모든 xref가 유효한 폰트 객체는 아닙니다.
            continue

    doc.close()

# 사용 예시
# pdf_file_path = "your_document.pdf"
# extract_fonts(pdf_file_path)