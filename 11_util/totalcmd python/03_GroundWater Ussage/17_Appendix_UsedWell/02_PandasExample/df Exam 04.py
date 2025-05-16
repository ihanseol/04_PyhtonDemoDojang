import pandas as pd

# Load your data
df = pd.read_excel('data.xlsx')
length = len(df)

# Print with specific column widths and formatting
print(f"{'gong':<6}{'address':<15}{'simdo':<6}{'well':<6}{'hp':<6}{'q':<6}{'purpose':<8}{'inout':<5}")
print("-" * 70)  # Separator line

for i in range(length):
    row = df.iloc[i]
    print(
        f"{row['gong']:<6}{row['address']:<15}{row['simdo']:<6}{row['well_diameter']:<6}{row['hp']:<6}{row['q']:<6}{row['purpose']:<8}{row['inout']:<5}")
