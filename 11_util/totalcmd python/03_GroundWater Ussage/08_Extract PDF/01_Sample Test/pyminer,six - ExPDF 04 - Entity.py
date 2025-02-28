from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextBoxHorizontal


#
# def extract_values_from_pdf(pdf_path):
#     x_value, t_value, s_value = None, None, None
#
#     # Define bounding boxes for the values
#     bbox_x = (373.080, 156.449, 472.575, 193.650)
#     bbox_t = (89.400, 91.650, 220.125, 122.370)
#     bbox_s = (313.320, 91.650, 378.328, 102.930)
#
#     for page_layout in extract_pages(pdf_path):
#         for element in page_layout:
#             if isinstance(element, LTTextBoxHorizontal):
#                 text = element.get_text().strip()
#                 print(f"Element text: '{text}'")  # Debugging line
#                 # Extract X value
#                 if (bbox_x[0] <= element.x0 <= bbox_x[2] and
#                         bbox_x[1] <= element.y0 <= bbox_x[3]):
#                     for line in text.split('\n'):
#                         if 'X' in line:
#                             x_value = line.split()[1]
#                             print(f"Found X value: {x_value}")  # Debugging line
#
#                 # Extract T value
#                 if (bbox_t[0] <= element.x0 <= bbox_t[2] and
#                         bbox_t[1] <= element.y0 <= bbox_t[3]):
#                     for line in text.split('\n'):
#                         if 'T =' in line:
#                             t_value = line.split('=')[-1].strip()
#                             print(f"Found T value: {t_value}")  # Debugging line
#
#                 # Extract S value
#                 if (bbox_s[0] <= element.x0 <= bbox_s[2] and
#                         bbox_s[1] <= element.y0 <= bbox_s[3]):
#                     for line in text.split('\n'):
#                         if 'S =' in line:
#                             s_value = line.split('=')[-1].strip()
#                             print(f"Found S value: {s_value}")  # Debugging line
#
#     return x_value, t_value, s_value


def extract_values_from_pdf(pdf_path):
    x_value, t_value, s_value = None, None, None

    # Define bounding boxes for the values
    bbox_x = (373.080, 156.449, 472.575, 193.650)
    bbox_t = (89.400, 91.650, 220.125, 122.370)
    bbox_s = (313.320, 91.650, 378.328, 102.930)

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextBoxHorizontal):
                text = element.get_text().strip()
                # print(f"Element text: '{text}'")  # Debugging line
                # Extract X value
                if (bbox_x[0] <= element.x0 <= bbox_x[2] and
                        bbox_x[1] <= element.y0 <= bbox_x[3]):
                    x_value = text

                # Extract T value
                if (bbox_t[0] <= element.x0 <= bbox_t[2] and
                        bbox_t[1] <= element.y0 <= bbox_t[3]):
                    t_value = text

                # Extract S value
                if (bbox_s[0] <= element.x0 <= bbox_s[2] and
                        bbox_s[1] <= element.y0 <= bbox_s[3]):
                    s_value = text

    return x_value, t_value, s_value


# Example usage
pdf_path = 'a1-2.pdf'
x, t, s = extract_values_from_pdf(pdf_path)
print("X value:", x)
print("T value:", t)
print("S value:", s)
