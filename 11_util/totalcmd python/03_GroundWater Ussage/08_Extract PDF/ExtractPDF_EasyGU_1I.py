import fitz  # PyMuPDF
import easygui
import json
from pathlib import Path


def extract_pdf_text_info(pdf_path, page_num=0, save_to_file=False):
    """
    Extract detailed text information from a PDF page.

    Args:
        pdf_path (str): Path to the PDF file
        page_num (int): Page number to extract (0-indexed)
        save_to_file (bool): Whether to save results to a JSON file

    Returns:
        list: List of dictionaries containing text information
    """
    try:
        doc = fitz.open(pdf_path)

        # Check if page number is valid
        if page_num >= len(doc):
            print(f"Warning: Page {page_num} doesn't exist. PDF has {len(doc)} pages.")
            page_num = 0

        page = doc[page_num]
        text_dict = page.get_text("dict")

        extracted_info = []

        for block_idx, block in enumerate(text_dict["blocks"]):
            if block["type"] == 0:  # Text block
                for line_idx, line in enumerate(block["lines"]):
                    for span_idx, span in enumerate(line["spans"]):
                        # Extract comprehensive information
                        info = {
                            "block_id": block_idx,
                            "line_id": line_idx,
                            "span_id": span_idx,
                            "font_name": span["font"],
                            "font_size": round(span["size"], 2),
                            "font_flags": span["flags"],  # Bold, italic, etc.
                            "font_color": span["color"],  # Color as integer
                            "text": span["text"],
                            "bbox": {
                                "x0": round(span["bbox"][0], 2),
                                "y0": round(span["bbox"][1], 2),
                                "x1": round(span["bbox"][2], 2),
                                "y1": round(span["bbox"][3], 2)
                            },
                            "is_bold": bool(span["flags"] & 2 ** 4),
                            "is_italic": bool(span["flags"] & 2 ** 1),
                        }

                        extracted_info.append(info)

                        # Print formatted output
                        color_hex = f"#{span['color']:06x}" if span['color'] != 0 else "#000000"
                        flags_str = []
                        if info["is_bold"]:
                            flags_str.append("Bold")
                        if info["is_italic"]:
                            flags_str.append("Italic")
                        flags_display = ", ".join(flags_str) if flags_str else "Normal"

                        print(f"Block {block_idx}, Line {line_idx}, Span {span_idx}:")
                        print(f"  Font: {info['font_name']}")
                        print(f"  Size: {info['font_size']}")
                        print(f"  Style: {flags_display}")
                        print(f"  Color: {color_hex}")
                        print(
                            f"  Position: ({info['bbox']['x0']}, {info['bbox']['y0']}) to ({info['bbox']['x1']}, {info['bbox']['y1']})")
                        print(f"  Text: '{info['text']}'")
                        print("-" * 50)

        # Save to JSON file if requested
        if save_to_file and extracted_info:
            output_file = Path(pdf_path).stem + "_text_info.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(extracted_info, f, ensure_ascii=False, indent=2)
            print(f"\nResults saved to: {output_file}")

        doc.close()
        return extracted_info

    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return []


def analyze_all_pages(pdf_path):
    """Analyze text information for all pages in the PDF."""
    try:
        doc = fitz.open(pdf_path)
        print(f"PDF has {len(doc)} pages")

        for page_num in range(len(doc)):
            print(f"\n{'=' * 60}")
            print(f"PAGE {page_num + 1}")
            print(f"{'=' * 60}")
            extract_pdf_text_info(pdf_path, page_num)

        doc.close()

    except Exception as e:
        print(f"Error: {str(e)}")


def main():
    # File selection dialog
    pdf_path = easygui.fileopenbox(
        title="PDF 파일 선택",
        filetypes=["*.pdf", "PDF files"]
    )

    if pdf_path:
        print(f"Selected file: {pdf_path}")

        # Ask user what they want to do
        choices = [
            "첫 번째 페이지만 분석",
            "모든 페이지 분석",
            "특정 페이지 분석",
            "결과를 JSON 파일로 저장"
        ]

        choice = easygui.choicebox("분석 옵션을 선택하세요:", "PDF 분석", choices)

        if choice == choices[0]:  # First page only
            extract_pdf_text_info(pdf_path, 0)

        elif choice == choices[1]:  # All pages
            analyze_all_pages(pdf_path)

        elif choice == choices[2]:  # Specific page
            page_num = easygui.integerbox("페이지 번호를 입력하세요 (1부터 시작):", "페이지 선택", 1)
            if page_num:
                extract_pdf_text_info(pdf_path, page_num - 1)

        elif choice == choices[3]:  # Save to JSON
            extract_pdf_text_info(pdf_path, 0, save_to_file=True)
    else:
        print("파일 선택이 취소되었습니다.")


if __name__ == "__main__":
    main()