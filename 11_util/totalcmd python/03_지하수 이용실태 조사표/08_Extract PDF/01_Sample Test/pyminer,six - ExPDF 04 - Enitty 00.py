from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal, LTTextLineHorizontal


def extract_entity_from_pdf(pdf_path):
    # This function will extract the text within the specified bounding box
    entity_text = ""
    target_box = (373.080, 156.449, 472.575, 193.650)  # Bounding box coordinates

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                # Check if the element is within the target bounding box
                if (target_box[0] <= element.x0 <= target_box[2] and
                        target_box[1] <= element.y0 <= target_box[3]):
                    entity_text += element.get_text()

    return entity_text.strip()


# Example usage
pdf_path = 'a1-2.pdf'
entity = extract_entity_from_pdf(pdf_path)
# print("Extracted Entity:", entity)

entity_text = entity.split('\n')[2]
print(entity_text)


