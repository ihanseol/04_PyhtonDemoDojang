import pandas as pd

# Create a DataFrame
data = {
    'A': [1, 2, 3],
    'B': [4, 5, 6],
    'C': [7, 8, 9]
}

df = pd.DataFrame(data)


print(df)

print("")


# Transpose the DataFrame using the T attribute
df_transposed = df.T

# Alternatively, use the transpose() method
df_transposed = df.transpose()

# Display the transposed DataFrame
print(df_transposed)