import os
import pandas as pd

file_name = r"c:\Users\minhwasoo\Downloads\금산_2023-10-30.csv"
df = pd.read_csv(file_name, skiprows=7, encoding='cp949')
df.columns = ['date', 'code', 'data']
data_column = df['data']

# Add a 'month' column for sorting
df['month'] = [i % 12 + 1 for i in range(len(df))]


# Pivot the table
pivot_df = df.pivot_table(index=df.index // 12, columns='month', values='data', aggfunc='first')

# Rename the columns with month names
month_names = ['{}월'.format(i) for i in range(1, 13)]
pivot_df.columns = month_names


# Pivot the table
pivot_df = df.pivot_table(index=df.index // 12, columns='month', values='data', aggfunc='first')

# Rename the columns with month names
month_names = ['{}월'.format(i) for i in range(1, 13)]
pivot_df.columns = month_names


years = range(1993, 1993 + 30)
pivot_df['year'] = years
# pivot_df.set_index('year', inplace=True)

pdf = pivot_df

#Get the last column name
last_column = pdf.columns[-1]
# Move the last column to the first position
pdf = pdf[[last_column] + [col for col in pdf if col != last_column]]

for i in range(len(pdf)):
    print(pdf.iloc[i])

