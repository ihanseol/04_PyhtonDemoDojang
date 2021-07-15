import pandas as pd

# 원본 Dataframe에 추가로 읽어온 엑셀 파일의 Data Frame을 병합
def Excel_M(file,SPath,df):
    l_row=0
    df1=pd.read_excel(SPath + "/" + file, header=None)
    for x in df1.index:
        if not pd.isna(df1.values[x,df1.columns.size-1]) :
            l_row = x
            break

    df1=pd.read_excel(SPath + "/" + file, skiprows = l_row)

    frames = pd.concat([df1, df]).drop_duplicates()
    return frames

def Excel_ReA(file,SPath,dfMap,dfH,dfs):
    l_row=0
    df1=pd.read_excel(SPath + "/" + file, header=None)
    for x in df1.index:
        if not pd.isna(df1.values[x,df1.columns.size-1]) :
            l_row = x
            break

    df1=pd.read_excel(SPath + "/" + file, skiprows = l_row)
    for index, row in dfMap.iterrows():
        df1.rename(columns = {row[0]:row[1]}, inplace = True)
    frames = pd.DataFrame(df1,columns=dfH.Header)
    frames = pd.concat([dfs, frames]).drop_duplicates()
    return frames
