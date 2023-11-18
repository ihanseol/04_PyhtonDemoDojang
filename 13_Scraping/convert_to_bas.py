import os
import datetime
import pandas as pd

Area = {
    "대전" : "DaeJeon",
    "금산" : "GeumSan",
    "보령" : "BoRyung",
    "부여" : "BuYeo",
    "서산" : "SeoSan",
    "천안" : "CheonAn"
}


def read_weather_data(fname):
    df = pd.read_csv(fname, skiprows=7, encoding='cp949')
    df.columns = ['date', 'code', 'data']
    data_column = df['data']

    # Add a 'month' column for sorting
    df['month'] = [i % 12 + 1 for i in range(len(df))]

    # Pivot the table
    pivot_df = df.pivot_table(index=df.index // 12, columns='month', values='data', aggfunc='first')

    # Rename the columns with month names
    # month_names = ['{}월'.format(i) for i in range(1, 13)]
    month_names = [f'{i}월' for i in range(1, 13)]
    pivot_df.columns = month_names

    current_year = datetime.datetime.now().year
    start_year = current_year - 30

    years = range(start_year, start_year + 30)
    pivot_df['year'] = years
    # pivot_df.set_index('year', inplace=True)

    pdf = pivot_df

    # Get the last column name
    last_column = pdf.columns[-1]
    # Move the last column to the first position
    pdf = pdf[[last_column] + [col for col in pdf if col != last_column]]

    # for i in range(len(pdf)):
    #     print(pdf.iloc[i])

    return pdf


# --------------------------------------------------------------------------------
# Open a file for writing (if it doesn't exist, it will be created)

#
# def write_bas_data(fname):
#     eng_area_name = Area["대전"] + ".bas"
#
#     if "금산" in fname:
#         eng_area_name = Area["금산"]
#     if "대전" in fname:
#         eng_area_name = Area["대전"]
#     if "보령" in fname:
#         eng_area_name = Area["보령"]
#     if "부여" in fname:
#         eng_area_name = Area["부여"]
#     if "서산" in fname:
#         eng_area_name = Area["서산"]
#     if "천안" in fname:
#         eng_area_name = Area["천안"]
#
#     eng_fname = eng_area_name + ".bas"
#
#     with open(eng_fname, 'w') as file:
#         # Write some content to the file
#         file.write(f'Function data_{eng_area_name.upper()}() As Variant\n')
#         file.write('\n')
#         file.write('    Dim myArray() As Variant\n')
#         file.write('    ReDim myArray(1 To 30, 1 To 13)\n')
#         file.write('\n')
#
#     df = read_weather_data(fname)
#     for i in range(len(df)):
#         list_a = list(df.iloc[i])
#         list_a[0] = int(list_a[0])
#         print(list_a)
#         for j, data in enumerate(list_a, start=1):
#             with open(eng_fname, 'a') as file:
#                 file.write(f"    myArray({i + 1}, {j}) = {data}\n")
#                 if (j % 13 == 0): file.write('\n')
#
#     with open(eng_fname, 'a') as file:
#         file.write(f'    data_{eng_area_name.upper()} = myArray\n')
#         file.write('\n')
#         file.write('End Function\n')


def write_bas_data(fname):
    # Define a mapping of Korean area names to English area names
    area_mapping = {
        "금산": "Geumsan",
        "대전": "Daejeon",
        "보령": "BoRyung",
        "부여": "Buyeo",
        "서산": "Seosan",
        "천안": "Cheonan"
    }

    # Extract the area name from the file name
    for korean_name, english_name in area_mapping.items():
        if korean_name in fname:
            eng_area_name = english_name
            break
    else:
        eng_area_name = "Unknown"  # If no match is found

    # Generate the English file name
    eng_fname = eng_area_name + ".bas"

    # Write content to the file
    with open(eng_fname, 'w') as file:
        file.write(f'Function data_{eng_area_name.upper()}() As Variant\n')
        file.write('\n')
        file.write('    Dim myArray() As Variant\n')
        file.write('    ReDim myArray(1 To 30, 1 To 13)\n')
        file.write('\n')

        # Read weather data and write it to the file
        df = read_weather_data(fname)
        for i, row in df.iterrows():
            list_a = [int(row[0])] + list(row[1:])
            print(list_a)
            for j, data in enumerate(list_a, start=1):
                file.write(f"    myArray({i + 1}, {j}) = {data}\n")
                if j % 13 == 0:
                    file.write('\n')

        file.write(f'    data_{eng_area_name.upper()} = myArray\n')
        file.write('\n')
        file.write('End Function\n')


def get_filename():
    download_folder = os.path.expanduser("~\\Downloads\\")
    os.chdir(download_folder)
    files = os.listdir(download_folder)
    files = [file for file in files if file.endswith('.csv')]

    return files


def main():
    fnames = get_filename()
    if len(fnames) == 0:
        print(".csv file is not found ...")
        exit()

    for f in fnames:
        print(f)
        write_bas_data(f)

if __name__ == "__main__":
    main()

