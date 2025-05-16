import pandas as pd

# Load your data
df = pd.read_excel('data.xlsx')
length = len(df)

# Print with specific column widths and better number formatting
print(f"{'gong':<6}{'address':<15}{'simdo':<6}{'well':<6}{'hp':<6}{'q':<6}{'purpose':<8}{'inout':<5}")
print("-" * 70)  # Separator line

for i in range(length):
    row = df.iloc[i]
    print(
        f"{row['gong']:<6}{row['address']:<15}{int(row['simdo']):<6}{int(row['well_diameter']):<6}{row['hp']:<6.1f}{row['q']:<6.2f}{row['purpose']:<8}{row['inout']:<5}")




