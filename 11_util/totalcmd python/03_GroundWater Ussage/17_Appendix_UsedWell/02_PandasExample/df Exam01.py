import pandas as pd

# Load the Excel file (replace 'data.xlsx' with your filename)
df = pd.read_excel('data.xlsx')

# Display the first 5 rows of the DataFrame
print("First 5 rows:")
print(df.head())

# Display basic information about the DataFrame
print("\nDataFrame info:")
print(df.info())

# Get basic statistics of numerical columns
print("\nDataFrame statistics:")
print(df.describe())

# Access specific columns
print("\nWell diameter column:")
print(df['well_diameter'])

# Access specific rows
print("\nRow at index 3:")
print(df.iloc[3])

# Access specific cell (row 2, column 'hp')
print("\nHP value at row 2:")
print(df.iloc[2]['hp'])

# Filter data (e.g., rows where hp > 0.5)
print("\nRows where hp > 0.5:")
print(df[df['hp'] > 0.5])

# Sort data (e.g., sort by well_diameter in descending order)
print("\nSorted by well_diameter (descending):")
print(df.sort_values(by='well_diameter', ascending=False))

# Group by a column and aggregate
print("\nGroup by purpose and count:")
print(df.groupby('purpose').count()['gong'])

# Add a new column (example: calculating a new value)
df['hp_q_ratio'] = df['hp'] / df['q']
print("\nDataFrame with new column:")
print(df)

# Save modified DataFrame to a new Excel file
# df.to_excel('modified_data.xlsx', index=False)