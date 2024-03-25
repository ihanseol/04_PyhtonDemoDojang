import pandas as pd

# create DataFrame
df = pd.DataFrame({'team': ['A', 'A', 'A', 'B', 'B', 'B'],
                   'points': [11, 7, 8, 10, 13, 13],
                   'assists': [5, 7, 7, 9, 12, 9],
                   'rebounds': [11, 8, 10, 6, 6, 5]})

#   team  points  assists  rebounds
# 0    A      11        5        11
# 1    A       7        7         8
# 2    A       8        7        10
# 3    B      10        9         6
# 4    B      13       12         6
# 5    B      13        9         5

print(df.iloc[1, 0:4])

# 1    A       7        7         8


# Print only the 'points' column for a particular row
row_index = 1  # Row index you want to print
points_value = df.loc[row_index, 'points']
print(points_value)
print("-"*40)

print(df.loc[row_index, 'team'])
print(df.loc[row_index, 'points'])
print(df.loc[row_index, 'assists'])
print(df.loc[row_index, 'rebounds'])

print("-"*40)

print(df.loc[row_index, df[row_index].tolist()])


