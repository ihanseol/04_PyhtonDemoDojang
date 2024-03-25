import pandas as pd

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")

# Get the header (column names)
header = df.columns.tolist()

# Print the header
print("Header:", header)


