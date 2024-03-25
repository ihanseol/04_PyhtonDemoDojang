import pandas as pd

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")

# Get all values in the first row of a specific column using numerical index
column_index = 1  # Assuming you want the second column (index 1)

# Check if the column index exists in the DataFrame
if column_index < len(df.columns):
    values_in_column = df.iloc[:, column_index].tolist()  # Use iloc to access column by numerical index

    # Print the values in the column
    print("Values in column", column_index, ":", values_in_column)
else:
    print("Column index", column_index, "does not exist in the DataFrame.")

print("-"*90)

# Specify the row index and column index
row_index = 0
column_index = 2

# Select the cell using iloc
cell_value = df.iloc[row_index, column_index]

# Print the cell value
print("Cell value at row", row_index, "and column", column_index, ":", cell_value)
