import fitz  # PyMuPDF


def extract_values_from_pdf_recover(pdf_path):
    document = fitz.open(pdf_path)

    page = document.load_page(0)
    text = page.get_text("text")

    T_value = None
    S_value = None
    X_value = None

    lines = text.split('\n')
    S_value = float(lines[-2].split('=')[1])
    T_value = float(lines[-3].split('=')[1].split(' ')[1])

    for line in lines:
        if 'Observation Wells' in line:
            index = lines.index(line)
            X_value = float(lines[index + 5])
            break

    return T_value, S_value, X_value


pdf_path = 'a1step.pdf'
T, S, X = extract_values_from_pdf_recover(pdf_path)

print(f"T = {T}")
print(f"S = {S}")
print(f"X = {X}")
