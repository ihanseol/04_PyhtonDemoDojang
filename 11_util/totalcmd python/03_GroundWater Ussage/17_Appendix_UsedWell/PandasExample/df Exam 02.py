import pandas as pd

# Load the Excel file (replace 'data.xlsx' with your filename)
df = pd.read_excel('data.xlsx')

# Calculate the sum of the 'q' column
q_sum = df['q'].sum()

# Print the result
print(f"Sum of q column: {q_sum}")