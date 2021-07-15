# https://youtu.be/8y_72SYZEGY

import pandas as pd
import os
import re

def Excel_RA (file,SPath,dfM,dfH,df1):
    df2 = pd.read_excel(SPath + "/" + file, header=None)

    for ind in df2.index:
        if not pd.isna(df2.values[ind,df2.columns.size -1]):
            h_row = ind
            break
    df2 = pd.read_excel(SPath + "/" + file,
                        skiprows=h_row)

    for index, row in dfM.iterrows():
        df2.rename(columns={row[0]:row[1]},inplace = True)

    df2 = df2[dfH.Header]
    result = pd.concat([df1,df2]).drop_duplicates()

    return result
df = []

df1 = pd.DataFrame(df)
dfH = pd.read_excel("D:/Work/RPA/Tricks_Office/Total_Order_Format.xlsx",
                    sheet_name="Head")
dfM = pd.read_excel("D:/Work/RPA/Tricks_Office/Total_Order_Format.xlsx",
                    sheet_name="Mapping")
SPath = "D:/Work/RPA/Tricks_Office/Sample/ToDo"

files = [x for x in os.listdir(SPath) if re.match('.*[.]xls',x)]
for file in files:
    df1=Excel_RA(file, SPath, dfM, dfH, df1)

print(df1)

#
# df1 = pd.read_excel("D:/Work/RPA/Tricks_Office/Sample/ToDo/네이버.xlsx")
# df2 = pd.read_excel("D:/Work/RPA/Tricks_Office/Sample/ToDo/옥션.xls")
#
#
# def M_Excel(file,SPath,df):
#     df3 = pd.read_excel(SPath + "/" + file,header=None)
#
#     for ind in df3.index:
#         if not pd.isna(df3.values[ind,df3.columns.size -1]):
#             h_row = ind
#             break
#     df3 = pd.read_excel(SPath + "/" + file,
#                         skiprows=h_row)
#
#     frames = [df, df3]
#
#     result = pd.concat(frames).drop_duplicates()
#
#     return result
# #
# df = pd.read_excel("D:/Work/RPA/Tricks_Office/Sample/ToDo/네이버.xlsx")
# file = "네이버3.xlsx"
# SPath = "D:/Work/RPA/Tricks_Office/Sample/ToDo"
# df = M_Excel(file,SPath,df)
# print (df)