import win32com.client
import win32com.client as win32
import time
import pandas as pd
import re
import os
from natsort import natsorted

DIRECTORY = "d:\\05_Send\\"
df = pd.read_excel(r"d:\05_Send\YanSoo_Spec.xlsx")
DEBUG_YES = True


def initial_delete_ouputfile():
    folder_path = r"c:/Users/minhwasoo/Documents/"
    files = os.listdir(folder_path)
    xlsmfiles = [f for f in files if f.endswith('.xlsm')]

    if xlsmfiles:
        for file in xlsmfiles:
            print(file)

            if os.path.exists(folder_path+file):
                os.remove(folder_path+file)
                print(f"{file} has been removed successfully.")
            else:
                print(f"The file {file} does not exist in the folder {folder_path}.")


def main():
    initial_delete_ouputfile()


if __name__ == "__main__":
    main()
