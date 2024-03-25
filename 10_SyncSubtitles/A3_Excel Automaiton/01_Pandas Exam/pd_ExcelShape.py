import pandas as pd

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")

# Get the number of rows and columns
num_rows, num_cols = df.shape

# Print the number of rows and columns
print("Number of rows:", num_rows)
print("Number of columns:", num_cols)

print(len(df))

