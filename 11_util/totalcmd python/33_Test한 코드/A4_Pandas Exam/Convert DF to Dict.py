import pandas as pd

# Example DataFrame
df = pd.DataFrame({
    'name': ['Command Prompt', 'PowerShell', 'Ubuntu'],
    'icon': [None, 'C:\\path\\to\\icon.png', None]
})

# Convert the DataFrame to a dictionary
# Choose the 'records' orient to get a list of row dictionaries

print('************************************************'*3)

df_dict = df.to_dict(orient='records')
print("df_dict = df.to_dict(orient='records')")
print(df_dict)

print('************************************************'*3)

df_dict = df.to_dict(orient='dict')
print("df_dict = df.to_dict(orient='dict')")
print(df_dict)

print('************************************************'*3)

df_dict = df.to_dict(orient='series')
print("df_dict = df.to_dict(orient='series')")
print(df_dict)

print('************************************************'*3)

df_dict = df.to_dict(orient='list')
print("df_dict = df.to_dict(orient='list')")
print(df_dict)


print('************************************************'*3)

df_dict = df.to_dict(orient='index')
print("df_dict = df.to_dict(orient='index')")
print(df_dict)

