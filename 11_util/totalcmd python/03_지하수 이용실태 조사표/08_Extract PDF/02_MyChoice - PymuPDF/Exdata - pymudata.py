import fitz  # PyMuPDF


# Function to extract values
def extract_values_from_pdf(pdf_path):
    document = fitz.open(pdf_path)
    page = document.load_page(0)
    text = page.get_text()

    # Initialize variables to store T, S, and X values
    T_value = None
    S_value = None
    X_value = None

    lines = text.split('\n')
    for line in lines:
        if line.startswith('T ='):
            T_value = float(line.split('=')[1].strip().split()[0])
        if line.startswith('S ='):
            S_value = float(line.split('=')[1].strip())
        if line.strip() == 'Observation Wells':
            index = lines.index(line)
            X_value = float(lines[index + 5])

    return T_value, S_value, X_value


pdf_path = 'a1-2.pdf'

# Extract and print the values
T, S, X = extract_values_from_pdf(pdf_path)
print(f"T = {T}")
print(f"S = {S}")
print(f"X = {X}")
