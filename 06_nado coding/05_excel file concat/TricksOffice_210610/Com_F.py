from os import walk
import os
from datetime import datetime
import pandas as pd

def FileList(TPath,RPath):
    FName = []
    Path = []
    Fsize = []
    FMDate = []

    for (dirpath, dirnames, filenames) in walk(TPath):
        for file in filenames:
            FName.append(file)
            Path.append(dirpath)
            Fsize.append(os.stat(dirpath + '/' + file).st_size)
            m_date = os.stat(dirpath + '/' + file).st_mtime
            mm_date = datetime.fromtimestamp(m_date).strftime('%Y-%m-%d %H:%M:%S')
            FMDate.append(mm_date)

    p_dict = {'FileName': FName, 'Path': Path, 'FileSize': Fsize, 'Mod_Time':FMDate}

    df = pd.DataFrame(p_dict)

    df.to_excel(RPath + "/" + "FileList.xlsx")
