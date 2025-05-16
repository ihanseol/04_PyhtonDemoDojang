import pandas as pd

# Load your data
df = pd.read_excel('data.xlsx')
length = len(df)


# Load the Excel file (replace 'data.xlsx' with your filename)
df = pd.read_excel('data.xlsx')

# Filter rows where 'inout' is "O" and calculate sum of 'q'
q_sum_for_inout_O = df.loc[df['inout'] == "O", 'q'].sum()

# Print the result
print(f"Sum of q where inout is 'O': {q_sum_for_inout_O}")


# Define column width for proper alignment
format_string = "{:<6} {:<15} {:<5} {:<5} {:<5} {:<5} {:<7} {:<5}"

# Print header
print(format_string.format("gong", "address", "simdo", "well", "hp", "q", "purpose", "inout"))
print("-" * 70)  # Separator line

# Print each row with aligned columns
for i in range(length):
    print(format_string.format(
        df.iloc[i]['gong'],
        df.iloc[i]['address'],
        df.iloc[i]['simdo'],
        df.iloc[i]['well_diameter'],
        df.iloc[i]['hp'],
        df.iloc[i]['q'],
        df.iloc[i]['purpose'],
        df.iloc[i]['inout']
    ))



