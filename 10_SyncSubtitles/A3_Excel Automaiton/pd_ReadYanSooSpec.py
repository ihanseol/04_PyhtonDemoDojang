import pandas as pd

# Load the Excel file into a pandas DataFrame
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")

# Choose the row you want to print (e.g., the first row, which has an index of 0)
row_index = 0
# Select the row using iloc and print it
print(df.iloc[row_index])


def print_excel_byrow():
    length = len(df)
    print("*" * 50)
    for i in range(0, length):
        print(df.iloc[i])
        print(df["gong"].iloc[i])
        print("-" * 50)


def print_excel_byfield():
    # Get the header (column names)
    header = df.columns.tolist()

    for i in range(len(df)):
        print(df.iloc[i])
        print("-" * 50)
        for field in header:
            data = df[field].iloc[i]
            print(f"{field}: {data}")
        print("-" * 50)




def get_excel_row(df, row_index):
    result = []
    result = list(df.iloc[row_index, :])
    return result


# def get_excel_row(df, row_index):
#     field_list = df.columns.tolist()
#     cell_value = []
#     for field in range(len(field_list)):
#         cell_value.append(df.iat[row_index, field])
#
#     return cell_value


for i in range(len(df)):
    row_values = get_excel_row(df, i)

    gong = row_values[0]
    simdo = row_values[1]
    q = row_values[2]
    natural = row_values[3]
    stable = row_values[4]

    print(f"{gong}\t{simdo}\t{q}\t{natural}\t{stable}")
    print("-" * 30)
