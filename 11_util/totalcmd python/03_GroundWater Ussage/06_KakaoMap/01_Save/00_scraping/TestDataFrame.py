import pandas as pd

# Define the data as a list of dictionaries
data = [
    {'Area': '보은', 'name': 'BoEun', 'Code': 226, 'aCode': 55, 'switch': 54},
    {'Area': '서청주', 'name': 'SeoCheongJu', 'Code': 181, 'aCode': 56, 'switch': 54},
    {'Area': '제천', 'name': 'JaeCheon', 'Code': 221, 'aCode': 57, 'switch': 54},
    {'Area': '청주', 'name': 'CheongJu', 'Code': 131, 'aCode': 58, 'switch': 54},
    {'Area': '추풍령', 'name': 'ChuPungNyeong', 'Code': 135, 'aCode': 59, 'switch': 54},
    {'Area': '충주', 'name': 'ChungJu', 'Code': 127, 'aCode': 60, 'switch': 54},
    {'Area': '대전', 'name': 'DaeJeon', 'Code': 133, 'aCode': 28, 'switch': 28},
    {'Area': '세종', 'name': 'SeJong', 'Code': 239, 'aCode': 134, 'switch': 132},
    {'Area': '금산', 'name': 'GeumSan', 'Code': 238, 'aCode': 62, 'switch': 61},
    {'Area': '보령', 'name': 'BoRyung', 'Code': 235, 'aCode': 63, 'switch': 61},
    {'Area': '부여', 'name': 'BuYeo', 'Code': 236, 'aCode': 64, 'switch': 61},
    {'Area': '서산', 'name': 'SeoSan', 'Code': 129, 'aCode': 65, 'switch': 61},
    {'Area': '천안', 'name': 'CheonAn', 'Code': 232, 'aCode': 66, 'switch': 61},
    {'Area': '홍성', 'name': 'HongSung', 'Code': 177, 'aCode': 67, 'switch': 61},
]

# Create a DataFrame from the data
df = pd.DataFrame(data)

# Accessing a specific cell
value = df.at[2, 'Area']
print(f"Value at row 2, 'Area' column: {value}")

# Accessing an entire row
row = df.iloc[3]
print(f"Row at index 3:\n{row}")

# Accessing an entire column
column = df['name']
print(f"Column 'name':\n{column}")

AreaSelection = '대전'

myCode = df[df['Area'] == AreaSelection]['Code'].values[0]
mySwitch = df[df['Area'] == AreaSelection]['switch'].values[0]

one_string = f"ztree_{mySwitch}_switch"
two_string = f"{AreaSelection} ({myCode})"

print(f"Value for '홍성' in 'Code' column: {myCode}, 'switch' : {mySwitch}")
print(f"one_string : {one_string}")
print(f"two_string : {two_string}")



